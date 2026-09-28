# Bright Correct - dikey (9:16) reklam filmi oluşturucu
#
# Kullanım:
#   python3 render.py                 -> cikti/ara/video.mp4 (sessiz)
#   python3 render.py --stills 1,5.2  -> belirtilen saniyelerden PNG kareler
import math
import os
import subprocess
import sys

import cv2
import numpy as np

from prep import ROOT, prep

W, H, FPS = 1080, 1920, 30
DUR = 34.5
NFRAMES = int(round(DUR * FPS))
OUT_DIR = os.path.join(ROOT, 'cikti')

cv2.setNumThreads(1)


# --- Yumuşatma (easing) fonksiyonları ---
def clamp01(u):
    return 0.0 if u < 0 else 1.0 if u > 1 else u


def ease_out_cubic(u):
    return 1 - (1 - clamp01(u)) ** 3


def ease_out_quart(u):
    return 1 - (1 - clamp01(u)) ** 4


def ease_in_cubic(u):
    return clamp01(u) ** 3


def ease_in_quad(u):
    return clamp01(u) ** 2


def ease_in_out_sine(u):
    return 0.5 - 0.5 * math.cos(math.pi * clamp01(u))


def ease_in_out_cubic(u):
    u = clamp01(u)
    return 4 * u ** 3 if u < 0.5 else 1 - (-2 * u + 2) ** 3 / 2


def smoothstep(a, b, x):
    u = clamp01((x - a) / (b - a))
    return u * u * (3 - 2 * u)


EASE = {'out': ease_out_cubic, 'inout': ease_in_out_sine, 'lin': clamp01}


def T(tx, ty):
    return np.array([[1, 0, tx], [0, 1, ty], [0, 0, 1]], np.float64)


def S(s):
    return np.array([[s, 0, 0], [0, s, 0], [0, 0, 1]], np.float64)


def to3(A):
    return np.vstack([A, [0, 0, 1]])


# --- Kamera ---
class Cam:
    """Anahtar kareler: (t, f, cx, cy[, ease]); f = görseli kadraja sığdıran ölçeğe göre zoom,
    (cx, cy) = kadraj merkezinin kaynak görseldeki konumu."""

    def __init__(self, img_w, img_h, keys):
        self.s0 = max(W / img_w, H / img_h)
        self.iw, self.ih = img_w, img_h
        self.keys = keys

    def at(self, t):
        k = self.keys
        if t <= k[0][0]:
            return k[0][1:4]
        for a, b in zip(k, k[1:]):
            if t <= b[0]:
                e = EASE[b[4] if len(b) > 4 else 'inout']((t - a[0]) / (b[0] - a[0]))
                f = math.exp(math.log(a[1]) + (math.log(b[1]) - math.log(a[1])) * e)
                return f, a[2] + (b[2] - a[2]) * e, a[3] + (b[3] - a[3]) * e
        return k[-1][1:4]

    def affine(self, t, zoom=1.0, focus=None):
        f, cx, cy = self.at(t)
        s = self.s0 * f
        # kadraj dışına taşmayı engelle
        hx, hy = W / (2 * s), H / (2 * s)
        cx = min(max(cx, hx), self.iw - hx)
        cy = min(max(cy, hy), self.ih - hy)
        A = np.array([[s, 0, W / 2 - s * cx], [0, s, H / 2 - s * cy]], np.float64)
        if zoom != 1.0:
            px, py = focus if focus is not None else (W / 2, H / 2)
            A = A * zoom
            A[0, 2] += (1 - zoom) * px
            A[1, 2] += (1 - zoom) * py
        return A

    def project(self, t, x, y):
        A = self.affine(t)
        return A[0, 0] * x + A[0, 2], A[1, 1] * y + A[1, 2]


# --- Yazı bloklarının animasyonu ---
def pad(p, r):
    return cv2.copyMakeBorder(p, r, r, r, r, cv2.BORDER_CONSTANT, value=0) if r > 0 else p


def add_patch(frame, patch, M):
    """patch'i (yerel koordinat -> çıktı, 3x3 M) çerçeveye ekle."""
    h, w = patch.shape[:2]
    c = np.array([[0, 0, 1], [w, 0, 1], [0, h, 1], [w, h, 1]], np.float64) @ M[:2].T
    x0 = max(0, int(math.floor(c[:, 0].min())) - 3)
    x1 = min(W, int(math.ceil(c[:, 0].max())) + 3)
    y0 = max(0, int(math.floor(c[:, 1].min())) - 3)
    y1 = min(H, int(math.ceil(c[:, 1].max())) + 3)
    if x1 <= x0 or y1 <= y0:
        return
    Ml = M[:2].copy()
    Ml[0, 2] -= x0
    Ml[1, 2] -= y0
    out = cv2.warpAffine(patch, Ml, (x1 - x0, y1 - y0), flags=cv2.INTER_LANCZOS4,
                         borderMode=cv2.BORDER_CONSTANT, borderValue=0)
    frame[y0:y1, x0:x1] += out


def soft_blur(p, sigma):
    r = int(math.ceil(sigma * 3)) + 1
    p = pad(p, r)
    return cv2.GaussianBlur(p, (0, 0), sigma), r


def draw_block(frame, blk, an, t, A3):
    kind = an['kind']
    t0 = an['t']
    if t < t0:
        return
    if kind == 'rise':
        # satır satır: bulanıktan netleşerek yukarı süzülme
        dur, dy0, bl0 = an.get('dur', 0.85), an.get('dy', 18), an.get('blur', 4.0)
        bands = blk.bands if an.get('lines', True) else [(0, blk.h)]
        for i, (b0, b1) in enumerate(bands):
            u = (t - t0 - i * an.get('stagger', 0.08)) / dur
            if u <= 0:
                continue
            e = ease_out_cubic(u)
            a = ease_out_cubic(u * 1.35)
            dy = dy0 * (1 - e)
            bl = bl0 * (1 - ease_out_quart(u))
            p = blk.d[b0:b1]
            r = 0
            if bl > 0.25:
                p, r = soft_blur(p, bl)
            if a < 0.999:
                p = p * a
            add_patch(frame, p, A3 @ T(blk.x0 - r, blk.y0 + b0 - r + dy))
    elif kind == 'track':
        # harf aralığı açıktan kapanarak (logo tipi giriş)
        u = (t - t0) / an.get('dur', 1.2)
        e = ease_out_quart(u)
        a = ease_out_cubic(u * 1.3)
        spread = an.get('spread', 0.4) * (1 - e)
        bl = an.get('blur', 2.5) * (1 - e)
        mid = blk.w / 2.0
        offs = [(c - mid) * spread for (_, _, c) in blk.strips]
        pw = int(math.ceil(max(abs(o) for o in offs))) + 2
        canvas = np.zeros((blk.h, blk.w + 2 * pw + 2, 3), np.float32)
        for (s0, s1, _), o in zip(blk.strips, offs):
            x = pw + s0 + o
            xi = int(math.floor(x))
            fr = x - xi
            strip = blk.d[:, s0:s1]
            canvas[:, xi:xi + s1 - s0] += strip * (1 - fr)
            canvas[:, xi + 1:xi + 1 + s1 - s0] += strip * fr
        r = 0
        if bl > 0.25:
            canvas, r = soft_blur(canvas, bl)
        add_patch(frame, canvas * a, A3 @ T(blk.x0 - pw - r, blk.y0 - r))
    elif kind == 'draw':
        # çizgi çizilir gibi açılma
        u = (t - t0) / an.get('dur', 0.6)
        e = ease_in_out_cubic(u)
        soft = an.get('soft', 12.0)
        dirn = an.get('dir', 'lr')
        n = blk.h if dirn == 'tb' else blk.w
        pos = e * (n + soft) - soft / 2
        co = np.arange(n, dtype=np.float32)
        if dirn == 'rl':
            co = n - 1 - co
        m = np.clip((pos - co) / soft + 0.5, 0, 1)
        p = blk.d * (m[:, None, None] if dirn == 'tb' else m[None, :, None])
        add_patch(frame, p, A3 @ T(blk.x0, blk.y0))
    elif kind == 'pop':
        # ikon: hafif büyüyerek belirme
        u = (t - t0) / an.get('dur', 0.7)
        e = ease_out_cubic(u)
        a = ease_out_cubic(u * 1.4)
        sc = an.get('from', 0.8) + (1 - an.get('from', 0.8)) * e
        bl = an.get('blur', 3.0) * (1 - e)
        p, r = (blk.d, 0)
        if bl > 0.25:
            p, r = soft_blur(p, bl)
        M = A3 @ T(blk.cx, blk.cy) @ S(sc) @ T(-(blk.w / 2 + r), -(blk.h / 2 + r))
        add_patch(frame, p * a, M)
    elif kind == 'fade':
        a = ease_in_out_sine((t - t0) / an.get('dur', 0.8))
        add_patch(frame, blk.d * a, A3 @ T(blk.x0, blk.y0))


# --- Parıltı (yıldız) efekti ---
def star_sprite(L=48):
    y, x = np.mgrid[-L:L + 1, -L:L + 1].astype(np.float32)
    r = np.sqrt(x * x + y * y)
    core = np.exp(-(r / 2.2) ** 2)
    h = np.exp(-(y / 1.0) ** 2) * np.exp(-np.abs(x) / (L * 0.26))
    v = np.exp(-(x / 1.0) ** 2) * np.exp(-np.abs(y) / (L * 0.26))
    xr, yr = (x + y) / 1.4142, (x - y) / 1.4142
    d = np.exp(-(yr / 0.8) ** 2) * np.exp(-np.abs(xr) / (L * 0.1)) + np.exp(-(xr / 0.8) ** 2) * np.exp(-np.abs(yr) / (L * 0.1))
    halo = 0.3 * np.exp(-(r / (L * 0.22)) ** 2)
    s = core + 0.85 * (h + v) + 0.35 * d + halo
    s = s / s.max()
    return np.dstack([s * 1.0, s * 0.97, s * 0.88]).astype(np.float32)


STAR = star_sprite()
STAR_L = 48


def draw_glint(frame, x, y, size, amt, rot):
    k = size / STAR_L
    M = T(x, y) @ np.array([[math.cos(rot), -math.sin(rot), 0], [math.sin(rot), math.cos(rot), 0], [0, 0, 1]]) @ S(k) @ T(-STAR_L, -STAR_L)
    add_patch(frame, STAR * (255.0 * amt), M)


def glint_env(t, tg):
    dt = t - tg
    if dt < -0.14 or dt > 0.9:
        return 0.0
    if dt < 0:
        return ease_out_cubic((dt + 0.14) / 0.14)
    return math.exp(-dt / 0.22)


# --- Sahne ---
PLATES = {}


class Scene:
    def __init__(self, n, t0, t1, cam, anims, tcam=None, glints=(), intro_blur=None):
        self.n, self.t0, self.t1 = n, t0, t1
        self.cam, self.tcam = cam, tcam
        self.anims, self.glints = anims, glints
        self.intro_blur = intro_blur

    def render(self, t, zoom=1.0, focus=None, blur=0.0):
        plate = PLATES[self.n]
        A = self.cam.affine(t, zoom, focus)
        frame = cv2.warpAffine(plate.clean, A, (W, H), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REFLECT101)
        A3 = to3((self.tcam or self.cam).affine(t, zoom, focus))
        for an in self.anims:
            draw_block(frame, plate.blocks[an['id']], an, t, A3)
        for (tg, gx, gy, size) in self.glints:
            e = glint_env(t, tg)
            if e > 0.003:
                x, y = A[0, 0] * gx + A[0, 2], A[1, 1] * gy + A[1, 2]
                draw_glint(frame, x, y, 1.5 * size * zoom * (0.75 + 0.25 * e), e, 0.35 * (t - tg))
        if self.intro_blur:
            ta, tb, b0 = self.intro_blur
            blur = max(blur, b0 * (1 - ease_out_cubic((t - ta) / (tb - ta))))
        if blur > 0.3:
            frame = cv2.GaussianBlur(frame, (0, 0), blur)
        return frame


def A_(i, t, **kw):
    d = dict(id=i, t=t)
    d.update(kw)
    return d


def rise(i, t, **kw):
    return A_(i, t, kind='rise', **kw)


def track(i, t, **kw):
    return A_(i, t, kind='track', **kw)


def draw(i, t, **kw):
    return A_(i, t, kind='draw', **kw)


def pop(i, t, **kw):
    return A_(i, t, kind='pop', **kw)


def header(t, sp=0.5):
    return [track('hdr_t', t, dur=1.3, spread=sp), track('hdr_s', t + 0.15, dur=1.3, spread=sp * 0.7),
            draw('hdr_l', t + 0.3, dir='rl', dur=0.7), draw('hdr_r', t + 0.3, dir='lr', dur=0.7)]


def build_scenes():
    sc = []
    # 1) Damlalık - "Bilimin gücü leke karşıtı bakımda."
    sc.append(Scene(3, 0.0, 5.6, Cam(941, 1672, [(0.0, 1.0, 470.5, 836), (5.6, 1.08, 486, 800)]),
                    header(0.375) + [
                        rise('l1', 1.125, dur=0.95, dy=26, blur=7),
                        rise('l2', 1.5, dur=0.95, dy=26, blur=7),
                        rise('l3', 1.875, dur=0.95, dy=26, blur=7),
                        draw('dash', 2.4375, dur=0.5)],
                    glints=[(2.8125, 538, 876, 70), (3.375, 462, 526, 48), (4.125, 538, 876, 90)],
                    intro_blur=(0.0, 1.1, 10.0)))
    # 2) "Bright Correct" isim girişi
    sc.append(Scene(7, 4.5, 7.9, Cam(941, 1672, [(4.5, 1.08, 470.5, 836), (7.9, 1.0, 470.5, 836, 'out')]),
                    header(5.25) + [
                        rise('bright', 5.25, dur=1.0, dy=30, blur=8, lines=False),
                        rise('correct', 5.625, dur=1.0, dy=30, blur=8, lines=False),
                        track('s1', 6.0, dur=1.05, spread=0.3),
                        track('s2', 6.1875, dur=1.05, spread=0.3)],
                    glints=[(6.5625, 542, 1098, 80)]))
    # 3) Cilt - üç fayda
    sc.append(Scene(1, 7.1, 13.9, Cam(1092, 1440, [(7.1, 1.30, 780, 820), (9.2, 1.03, 428, 722, 'out'),
                                                   (13.9, 1.05, 426, 712)]),
                    [track('bc', 8.25, dur=1.1, spread=0.35), draw('rule', 8.625, dur=0.5),
                     rise('h1', 8.625, dur=0.9, dy=28, blur=7, lines=False),
                     rise('h2', 8.8125, dur=0.9, dy=28, blur=7, lines=False),
                     rise('h3', 9.0, dur=0.9, dy=28, blur=7, lines=False),
                     rise('h4', 9.1875, dur=0.9, dy=28, blur=7, lines=False)] +
                    [x for k, t in (('1', 9.75), ('2', 10.5), ('3', 11.25)) for x in (
                        rise(f'c{k}t', t, dur=0.7, dy=14, blur=3),
                        draw(f'c{k}l', t + 0.1, dur=0.65),
                        rise(f'c{k}b', t + 0.3, dur=0.7, dy=12, blur=3, stagger=0.07))],
                    ))
    # 4) Aktif içerikler
    sc.append(Scene(2, 13.1, 19.9, Cam(941, 1672, [(13.1, 1.0, 470.5, 836), (19.9, 1.07, 462, 836)]),
                    [x for p, t in (('n', 13.875), ('a', 15.375), ('t', 16.875)) for x in (
                        track(f'{p}_t', t, dur=1.0, spread=0.22, blur=3),
                        draw(f'{p}_r', t + 0.25, dur=0.5),
                        rise(f'{p}_b', t + 0.4, dur=0.7, dy=12, blur=3, stagger=0.08))]))
    # 5) İçermez listesi (yazılar sabit kamerada, arka plan hafif yaklaşır -> derinlik)
    sc.append(Scene(6, 19.1, 24.4, Cam(941, 1672, [(19.1, 1.22, 400, 700), (20.5, 1.0, 470.5, 836, 'out'),
                                                   (24.4, 1.06, 478, 850)]),
                    [x for i in range(6) for x in (
                        pop(f'i{i + 1}', 20.25 + 0.375 * i, dur=0.7, **{'from': 0.82}),
                        rise(f'l{i + 1}', 20.37 + 0.375 * i, dur=0.7, dy=10, blur=3, stagger=0.06))],
                    tcam=Cam(941, 1672, [(19.1, 1.0, 470.5, 836)]),
                    glints=[(22.5, 336, 512, 60)]))
    # 6) Kişiselleştirme
    sc.append(Scene(5, 23.6, 29.6, Cam(1024, 1536, [(23.6, 1.10, 560, 760), (25.0, 1.0, 490, 768, 'out'),
                                                    (29.6, 1.06, 520, 768)]),
                    [rise('h1', 24.75, dur=0.9, dy=26, blur=7, lines=False),
                     rise('h2', 24.9375, dur=0.9, dy=26, blur=7, lines=False),
                     rise('h3', 25.125, dur=0.9, dy=26, blur=7, lines=False)] +
                    [x for k, t in (('1', 25.875), ('2', 26.25), ('3', 26.625)) for x in (
                        pop(f'i{k}', t, dur=0.7, **{'from': 0.8}),
                        draw(f'b{k}', t + 0.1, dir='tb', dur=0.45),
                        rise(f'l{k}', t + 0.15, dur=0.7, dy=12, blur=3, stagger=0.07))],
                    tcam=Cam(1024, 1536, [(23.6, 1.0, 490, 768)])))
    # 7) Kapanış - ürün
    sc.append(Scene(4, 28.5, DUR, Cam(941, 1672, [(28.5, 1.12, 470.5, 900), (31.5, 1.0, 470.5, 836, 'out'),
                                                  (DUR, 1.035, 470.5, 850)]),
                    header(29.25) + [
                        rise('bright', 29.625, dur=1.0, dy=30, blur=8, lines=False),
                        rise('correct', 29.8125, dur=1.0, dy=30, blur=8, lines=False),
                        track('s1', 30.375, dur=1.05, spread=0.3),
                        track('s2', 30.5625, dur=1.05, spread=0.3),
                        draw('p_r', 30.9375, dur=0.5),
                        rise('para', 31.125, dur=0.8, dy=12, blur=3, stagger=0.09)],
                    tcam=Cam(941, 1672, [(28.5, 1.04, 470.5, 850), (31.5, 1.0, 470.5, 836, 'out'),
                                         (DUR, 1.01, 470.5, 838)]),
                    glints=[(32.25, 424, 812, 70), (32.625, 332, 948, 55), (33.0, 604, 1428, 60)]))
    return sc


# Geçişler: ripple = damla dalgası, zoom = bulanık yakınlaşma, bloom = ışık patlaması
TRANS = [
    dict(kind='ripple', t0=4.5, t1=5.6, a=0, b=1, pa=(505, 905)),
    dict(kind='zoom', t0=7.1, t1=7.9, a=1, b=2, fa=(485, 1075), fb=(830, 820)),
    dict(kind='bloom', t0=13.1, t1=13.9, a=2, b=3, light=(0.85, 0.1)),
    dict(kind='zoom', t0=19.1, t1=19.9, a=3, b=4, fa=(700, 1420), fb=(330, 470)),
    dict(kind='bloom', t0=23.6, t1=24.4, a=4, b=5, light=(0.12, 0.1)),
    dict(kind='ripple', t0=28.5, t1=29.6, a=5, b=6, pb=(470, 1150)),
]

# Işık süpürmesi (başlangıç, bitiş, güç)
SWEEPS = [(5.25, 6.375, 0.22), (31.875, 33.0, 0.33)]

YY, XX = np.mgrid[0:H, 0:W].astype(np.float32)
MAXD = math.hypot(W, H)


def ripple(fa, fb, u, P):
    px, py = float(P[0]), float(P[1])
    dx, dy = XX - px, YY - py
    d = np.sqrt(dx * dx + dy * dy) + 1e-3
    rmax = max(math.hypot(px - cx, py - cy) for cx in (0, W) for cy in (0, H)) + 160
    r = rmax * (0.18 * u + 0.82 * u * u)
    sig = 26 + 26 * u
    amp = 30 * (1 - 0.45 * u)
    x = (d - r) / sig
    disp = amp * 1.65 * (-x) * np.exp(-0.5 * x * x)
    r2 = r * 0.72 - 30
    if r2 > 0:
        x2 = (d - r2) / (sig * 0.8)
        disp += 0.4 * amp * 1.65 * (-x2) * np.exp(-0.5 * x2 * x2)
    mx = XX + disp * dx / d
    my = YY + disp * dy / d
    A = cv2.remap(fa, mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT101)
    B = cv2.remap(fb, mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT101)
    inside = np.clip((r - d) / 10 + 0.5, 0, 1)[..., None]
    out = A * (1 - inside) + B * inside
    light = 0.5 + 0.5 * np.cos(np.arctan2(dy, dx) + 2.3)
    rim = np.exp(-((d - r + 0.3 * sig) / (0.32 * sig)) ** 2) * light * (1 - 0.6 * u)
    shade = np.exp(-((d - r - 0.8 * sig) / (0.5 * sig)) ** 2) * (1 - u)
    out += rim[..., None] * np.array([120, 112, 96], np.float32)
    out -= shade[..., None] * 16
    # çarpma anındaki küçük parlama
    if u < 0.25:
        fl = (1 - u / 0.25) ** 2 * np.exp(-(d / 60) ** 2)
        out += fl[..., None] * np.array([120, 112, 96], np.float32)
    return out


def radial(fx, fy, rad):
    return np.exp(-((XX - fx * W) ** 2 + (YY - fy * H) ** 2) / (2 * rad * rad)).astype(np.float32)


LEAKS = {i: radial(*tr['light'], 0.6 * H) for i, tr in enumerate(TRANS) if tr['kind'] == 'bloom'}


def screen(img, light):
    return 255.0 - (255.0 - img) * (1.0 - light / 255.0)


def glow(frame, amount, thr=200.0):
    small = cv2.resize(frame, (W // 4, H // 4), interpolation=cv2.INTER_AREA)
    lum = small @ np.array([0.299, 0.587, 0.114], np.float32)
    hl = np.clip((lum - thr) / (255 - thr), 0, 1) ** 1.5
    b = cv2.GaussianBlur(small * hl[..., None], (0, 0), 7)
    return frame + cv2.resize(b, (W, H), interpolation=cv2.INTER_LINEAR) * amount


def compose(t, scenes):
    for i, tr in enumerate(TRANS):
        if tr['t0'] <= t < tr['t1']:
            sa, sb = scenes[tr['a']], scenes[tr['b']]
            u = (t - tr['t0']) / (tr['t1'] - tr['t0'])
            if tr['kind'] == 'ripple':
                if 'pa' in tr:
                    P = sa.cam.project(tr['t0'], *tr['pa'])
                else:
                    P = sb.cam.project(tr['t0'], *tr['pb'])
                return ripple(sa.render(t), sb.render(t), u, P)
            if tr['kind'] == 'zoom':
                ua, ub = clamp01(u / 0.58), clamp01((u - 0.42) / 0.58)
                mix = smoothstep(0.36, 0.64, u)
                out = 0
                if mix < 1:
                    Pa = sa.cam.project(t, *tr['fa'])
                    out = sa.render(t, 1 + 0.34 * ease_in_cubic(ua), Pa, 16 * ease_in_quad(ua)) * (1 - mix)
                if mix > 0:
                    Pb = sb.cam.project(t, *tr['fb'])
                    zb = 1 + 0.34 * (1 - ease_out_cubic(ub))
                    out = out + sb.render(t, zb, Pb, 16 * (1 - ease_out_cubic(ub))) * mix
                return out + 22 * math.sin(math.pi * u) ** 2
            if tr['kind'] == 'bloom':
                mix = smoothstep(0.32, 0.68, u)
                za = 1 + 0.05 * ease_in_out_sine(u)
                zb = 1.05 - 0.05 * ease_in_out_sine(u)
                out = 0
                if mix < 1:
                    out = sa.render(t, za) * (1 - mix)
                if mix > 0:
                    out = out + sb.render(t, zb) * mix
                L = math.sin(math.pi * u) ** 1.5
                leak = (LEAKS[i] * 0.8 + 0.2) * (L * 0.24 * 255)
                out = screen(out, leak[..., None] * np.array([1.0, 0.9, 0.74], np.float32))
                return glow(out, 0.4 * L, thr=185)
    # geçiş dışındaysa en son başlamış sahne görünür
    for s in reversed(scenes):
        if s.t0 <= t:
            return s.render(t)
    raise ValueError(t)


# --- Altın toz partikülleri ---
RNG = np.random.default_rng(7)
NP = 90
P_X = RNG.uniform(0, W, NP)
P_Y = RNG.uniform(0, H, NP)
P_Z = RNG.uniform(0, 1, NP) ** 1.6
P_SW = RNG.uniform(0.07, 0.22, NP)
P_PH = RNG.uniform(0, 2 * np.pi, NP)
P_TW = RNG.uniform(0.4, 1.6, NP)
P_B = RNG.uniform(0.35, 1.0, NP)
P_WARM = RNG.uniform(0, 1, NP)

PART_ENV = [(0, 0.0), (0.8, 0.45), (4.4, 0.5), (5.0, 0.9), (6.2, 0.45), (8.0, 0.3), (19.0, 0.3),
            (24.0, 0.4), (28.3, 0.5), (29.0, 1.0), (33.6, 0.95), (DUR, 0.0)]


def envelope(keys, t):
    for (ta, va), (tb, vb) in zip(keys, keys[1:]):
        if ta <= t <= tb:
            return va + (vb - va) * ease_in_out_sine((t - ta) / (tb - ta))
    return keys[-1][1]


def particles(frame, t):
    env = envelope(PART_ENV, t)
    if env < 0.01:
        return frame
    for k in range(NP):
        z = P_Z[k]
        sig = 0.9 + 3.6 * z * z
        x = (P_X[k] + (4 + 16 * z) * math.sin(2 * math.pi * P_SW[k] * t + P_PH[k])) % (W + 60) - 30
        y = (P_Y[k] - (7 + 30 * z) * t) % (H + 60) - 30
        tw = 0.6 + 0.4 * math.sin(2 * math.pi * P_TW[k] * t + P_PH[k] * 3)
        amp = 255 * env * P_B[k] * tw * (0.9 if z < 0.5 else 0.55) * 0.55
        r = int(math.ceil(3 * sig))
        xi, yi = int(x), int(y)
        x0, x1, y0, y1 = max(0, xi - r), min(W, xi + r + 1), max(0, yi - r), min(H, yi + r + 1)
        if x1 <= x0 or y1 <= y0:
            continue
        gx = np.exp(-((np.arange(x0, x1) - x) ** 2) / (2 * sig * sig))
        gy = np.exp(-((np.arange(y0, y1) - y) ** 2) / (2 * sig * sig))
        g = (gy[:, None] * gx[None, :] * amp).astype(np.float32)
        col = np.array([1.0, 0.86 + 0.08 * P_WARM[k], 0.62 + 0.25 * P_WARM[k]], np.float32)
        reg = frame[y0:y1, x0:x1]
        reg += (g[..., None] * col) * np.clip(1.0 - reg / 255.0, 0.0, 1.0)
    return frame


def sweep(frame, t):
    for (ta, tb, k) in SWEEPS:
        if ta <= t <= tb:
            u = ease_in_out_sine((t - ta) / (tb - ta))
            # sol üstten sağ alta çapraz ışık bandı
            nx, ny = 0.6, 0.8
            pos = -500 + u * (W * nx + H * ny + 1000)
            dist = XX * nx + YY * ny - pos
            band = np.exp(-(dist / 170) ** 2) * 0.7 + np.exp(-(dist / 45) ** 2) * 0.5
            lum = np.clip(frame.mean(axis=2) / 255.0, 0, 1)
            gain = (band * k * (0.25 + lum ** 2))[..., None]
            return frame + gain * np.array([255, 246, 228], np.float32)
    return frame


VIG = None
GRAIN = None


def post(frame, t):
    global VIG, GRAIN
    if VIG is None:
        rr = np.sqrt(((XX - W / 2) / (W / 2)) ** 2 * 0.75 + ((YY - H / 2) / (H / 2)) ** 2)
        VIG = (1 - 0.2 * np.clip((rr - 0.45) / 0.75, 0, 1) ** 1.6)[..., None].astype(np.float32)
        g = np.random.default_rng(3).standard_normal((12, H, W)).astype(np.float32)
        GRAIN = np.stack([cv2.GaussianBlur(x, (0, 0), 0.65) for x in g])
        GRAIN /= GRAIN.std()
    frame = sweep(frame, t)
    frame = glow(frame, 0.32)
    frame = particles(frame, t)
    frame = frame * VIG
    fade = min(ease_in_out_sine(t / 0.55), 1 - ease_in_out_sine((t - (DUR - 0.7)) / 0.7))
    if fade < 1:
        frame = frame * fade
    i = int(t * FPS)
    frame = frame + GRAIN[i % 12][..., None] * 1.3
    return np.clip(frame, 0, 255).astype(np.uint8)


SCENES = None


def init():
    global SCENES
    for n in (1, 2, 3, 4, 5, 6, 7):
        PLATES[n] = prep(n)
    SCENES = build_scenes()


def render_frame(i):
    t = i / FPS
    return post(compose(t, SCENES), t)


def ffmpeg_exe():
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


def main():
    init()
    args = sys.argv[1:]
    if args and args[0] == '--stills':
        out = args[2] if len(args) > 2 else os.path.join(OUT_DIR, 'kareler')
        os.makedirs(out, exist_ok=True)
        for s in args[1].split(','):
            t = float(s)
            img = post(compose(t, SCENES), t)
            cv2.imwrite(os.path.join(out, f'kare_{t:06.2f}.png'), cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
            print('kare', t)
        return
    from multiprocessing import Pool
    os.makedirs(OUT_DIR, exist_ok=True)
    os.makedirs(os.path.join(OUT_DIR, 'ara'), exist_ok=True)
    video = os.path.join(OUT_DIR, 'ara', 'video.mp4')
    cmd = [ffmpeg_exe(), '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}',
           '-r', str(FPS), '-i', '-', '-vf', 'scale=out_color_matrix=bt709:out_range=tv,format=yuv420p',
           '-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-maxrate', '14M', '-bufsize', '28M',
           '-profile:v', 'high', '-level', '4.2',
           '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-color_range', 'tv',
           '-movflags', '+faststart', video]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    with Pool(int(os.environ.get('JOBS', os.cpu_count() or 2))) as pool:
        for i, fr in enumerate(pool.imap(render_frame, range(NFRAMES), chunksize=2)):
            proc.stdin.write(fr.tobytes())
            if i % 60 == 0:
                print(f'{i}/{NFRAMES}', flush=True)
    proc.stdin.close()
    proc.wait()
    print('yazıldı:', video)


if __name__ == '__main__':
    main()
