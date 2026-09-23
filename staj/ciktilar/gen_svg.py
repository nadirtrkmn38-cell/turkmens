# -*- coding: utf-8 -*-
"""TR ETS kapsam belirleme şeması — baskı/PDF için SVG üreteci.

İçerik miro_import.py'deki modelden okunur; burada yalnız yerleşim ve
görsel dil tanımlanır. Böylece drawio dosyası ile PDF aynı metni paylaşır.
"""
from html import escape
import miro_import as M

W = 1900

# ───────────────────────── görsel dil ─────────────────────────
INK      = "#14212A"
MUTED    = "#58666B"
FAINT    = "#8A9499"
LINE     = "#C8D0CE"
GROUND   = "#FAFBF8"
CARD     = "#FFFFFF"
PANEL    = "#F1F4F0"
PANEL_ST = "#CFD6D1"
NEUTRAL  = "#E8ECE8"
NEUT_ST  = "#A6B0AB"
ACCENT   = "#0B5D58"

GREEN_F, GREEN_S, GREEN_T = "#DCEBDD", "#2C6A3B", "#1A4224"
AMBER_F, AMBER_S, AMBER_T = "#F8EAD1", "#95600A", "#563806"
RED_F,   RED_S,   RED_T   = "#F6E1DE", "#8C2A24", "#551916"
EVENT_F, EVENT_S          = "#E6EAEF", "#83909F"
OPP_F,   OPP_S,   OPP_T   = "#E3EFEC", "#0B5D58", "#11332F"

FONT = "Archivo, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"
MONO = "'IBM Plex Mono', 'SFMono-Regular', Consolas, monospace"

out = []
def add(s): out.append(s)
def e(t): return escape(str(t), quote=True)
def tru(t): return t.replace("i", "İ").upper()

# ───────────────────────── içerik modeli ─────────────────────────
NODE = {k: (title, sub) for k, _sh, _x, _y, _w, _h, title, sub, _p in M.NODES}
PANEL_TXT = {k: (heading, lines) for k, _x, _y, _w, _h, heading, lines, _p in M.PANELS}
WHO = M.WHO

def split_badge(sub):
    for tag in ("CEZA RİSKİ", "DIŞ OLAY"):
        if sub.startswith(tag + " · "):
            return tag, sub[len(tag) + 3:]
    return None, sub

# ───────────────────────── çizim yardımcıları ─────────────────────────
def wrap(text, maxchars):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if len(t) <= maxchars:
            cur = t
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines

def bwrap(text, maxchars):
    """Satır sayısını artırmadan satırları dengeler (son satırda tek kelime kalmasın)."""
    base = wrap(text, maxchars)
    if len(base) < 2:
        return base
    for m in range(-(-len(text) // len(base)), maxchars + 1):
        cand = wrap(text, m)
        if len(cand) == len(base):
            base = cand
            break
    for i in range(1, len(base)):                  # "·" satır başında kalmasın
        if base[i].startswith("· "):
            base[i - 1] += " ·"
            base[i] = base[i][2:]
    return base

def pwrap(text, maxchars, sep=" · "):
    """" · " ile ayrılmış parçaları satır başına taşımadan paketler."""
    lines = []
    for part in text.split(sep):
        if lines and len(lines[-1]) + len(sep) + len(part) <= maxchars:
            lines[-1] += sep + part
        else:
            lines += bwrap(part, maxchars)
    alt = bwrap(text, maxchars)
    if len(alt) < len(lines):
        lines = alt
        for i in range(1, len(lines)):          # "·" satır başında kalmasın
            if lines[i].startswith("· "):
                lines[i - 1] += " ·"
                lines[i] = lines[i][2:]
    return lines

def tblock(x, top, lines, size, weight, color, lh, anchor="middle"):
    parts = "".join(f'<tspan x="{x}" dy="{0 if i == 0 else lh}">{e(l)}</tspan>'
                    for i, l in enumerate(lines))
    add(f'<text x="{x}" y="{top + size * 0.80}" text-anchor="{anchor}" font-family="{FONT}" '
        f'font-size="{size}" font-weight="{weight}" fill="{color}">{parts}</text>')

def who_pill(x, y, stroke):
    add(f'<rect x="{x}" y="{y}" width="30" height="15" rx="7.5" fill="{stroke}"/>')
    add(f'<text x="{x + 15}" y="{y + 10.8}" text-anchor="middle" font-family="{MONO}" '
        f'font-size="9" font-weight="600" letter-spacing="0.6" fill="#FFFFFF">KİM</text>')

FOOT = 46

def box(cx, cy, w, h, title, sub=None, fill=NEUTRAL, stroke=NEUT_ST, tcol=INK, scol=MUTED,
        r=10, sw=1.7, ts=15, ss=11.5, dash=None, shadow=False, who=None, smax=None):
    x, y = cx - w / 2, cy - h / 2
    if shadow:
        add(f'<rect x="{x + 1}" y="{y + 3}" width="{w}" height="{h}" rx="{r}" '
            f'fill="#14212A" opacity="0.055"/>')
    d = f' stroke-dasharray="{dash}"' if dash else ""
    add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" '
        f'stroke="{stroke}" stroke-width="{sw}"{d}/>')
    mid = cy
    if who:
        fy = y + h - FOOT
        mid = y + (h - FOOT) / 2
        add(f'<path d="M{x + sw/2},{fy} H{x + w - sw/2} V{y + h - r} Q{x + w - sw/2},{y + h - sw/2} '
            f'{x + w - r},{y + h - sw/2} H{x + r} Q{x + sw/2},{y + h - sw/2} {x + sw/2},{y + h - r} Z" '
            f'fill="#FFFFFF" opacity="0.6"/>')
        add(f'<line x1="{x + sw/2}" y1="{fy}" x2="{x + w - sw/2}" y2="{fy}" stroke="{stroke}" '
            f'stroke-width="1" opacity="0.35"/>')
        wl = pwrap(who, int((w - 62 - 18) / 5.6))
        by = fy + (FOOT - (len(wl) - 1) * 15) / 2 + 4.2
        who_pill(x + 24, by - 11, stroke)
        for j, l in enumerate(wl):
            add(f'<text x="{x + 62}" y="{by + j * 15}" font-family="{FONT}" font-size="11.5" '
                f'font-weight="600" fill="{tcol}">{e(l)}</text>')
    tl = bwrap(title, int((w - 34) / (ts * 0.505)))
    sl = bwrap(sub, smax or int((w - 34) / (ss * 0.505))) if sub else []
    th, sh_ = len(tl) * ts * 1.2, len(sl) * ss * 1.28
    gap = 7 if sl else 0
    top = mid - (th + gap + sh_) / 2
    tblock(cx, top, tl, ts, 600, tcol, ts * 1.2)
    if sl:
        tblock(cx, top + th + gap, sl, ss, 400, scol, ss * 1.28)
    return mid

def diamond(cx, cy, w, h, title, ref=None):
    add(f'<polygon points="{cx},{cy - h/2} {cx + w/2},{cy} {cx},{cy + h/2} {cx - w/2},{cy}" '
        f'fill="{NEUTRAL}" stroke="{NEUT_ST}" stroke-width="1.9"/>')
    tl = wrap(title, 46)
    tblock(cx, cy - len(tl) * 15 * 1.2 / 2, tl, 15, 600, INK, 15 * 1.2)
    if ref:
        add(f'<text x="{cx + w/4 + 16}" y="{cy + h/4 + 16}" font-family="{MONO}" '
            f'font-size="11" fill="{FAINT}">{e(ref)}</text>')

def column(x, yy, w, lines):
    """Panel satırlarını x..x+w aralığına dizer, bitiş y'sini döndürür."""
    for ln in lines:
        if not ln:
            yy += 9
        elif ln.startswith("•"):
            body = ln.lstrip("• ").strip()
            for i, l in enumerate(wrap(body, int((w - 12) / 6.05))):
                add(f'<text x="{x}" y="{yy}" font-family="{FONT}" font-size="12" '
                    f'fill="{INK}">{e(("•  " if i == 0 else "    ") + l)}</text>')
                yy += 16
            yy += 3
        elif len(ln) < 60 and ln == tru(ln):
            add(f'<text x="{x}" y="{yy + 4}" font-family="{FONT}" font-size="11" '
                f'font-weight="700" letter-spacing="1.1" fill="{MUTED}">{e(ln)}</text>')
            yy += 24
        else:
            for l in wrap(ln, int(w / 6.10)):
                add(f'<text x="{x}" y="{yy}" font-family="{FONT}" font-size="12" '
                    f'fill="{INK}">{e(l)}</text>')
                yy += 16
            yy += 5
    return yy

def panel(x, y, w, heading, lines, fill=PANEL, stroke=PANEL_ST):
    slot, pad = len(out), 18
    if "||" in lines:
        # başlıktan önceki giriş paragrafı tam genişlikte, kalanı iki sütunda
        n = 0
        while n < len(lines) and not (lines[n] == tru(lines[n]) and len(lines[n]) < 60):
            n += 1
        top = column(x + pad, y + 52, w - 2 * pad, lines[:n]) + 6 if n else y + 52
        rest = lines[n:]
        k, gut = rest.index("||"), 56
        cw = (w - 2 * pad - gut) / 2
        yy = max(column(x + pad, top, cw, rest[:k]),
                 column(x + pad + cw + gut, top, cw, rest[k + 1:]))
        add(f'<line x1="{x + pad + cw + gut / 2}" y1="{top - 8}" x2="{x + pad + cw + gut / 2}" '
            f'y2="{yy - 6}" stroke="{stroke}" stroke-width="1.2"/>')
    else:
        yy = column(x + pad, y + 52, w - 2 * pad, lines)
    h = yy - y + 12
    out.insert(slot, f'<text x="{x + pad}" y="{y + 31}" font-family="{FONT}" font-size="12.5" '
                     f'font-weight="700" letter-spacing="1.2" fill="{ACCENT}">{e(tru(heading))}</text>')
    out.insert(slot, f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{fill}" '
                     f'stroke="{stroke}" stroke-width="1.4"/>')
    return h

def draw_panel(x, y, w, key, **kw):
    heading, lines = PANEL_TXT[key]
    return panel(x, y, w, heading, lines, **kw)

def conn(pts, label=None, lx=None, ly=None, anchor="middle", color="#66746F"):
    add(f'<polyline points="{" ".join(f"{a},{b}" for a, b in pts)}" fill="none" '
        f'stroke="{color}" stroke-width="1.9" stroke-linejoin="round" marker-end="url(#ar)"/>')
    if label:
        add(f'<text x="{lx}" y="{ly}" text-anchor="{anchor}" font-family="{FONT}" '
            f'font-size="11.5" font-weight="600" fill="{MUTED}">{e(label)}</text>')

def label(x, y, lines, anchor="start"):
    for i, (txt, bold) in enumerate(lines):
        add(f'<text x="{x}" y="{y + i * 16}" text-anchor="{anchor}" font-family="{FONT}" '
            f'font-size="{12 if bold else 11.5}" font-weight="{700 if bold else 500}" '
            f'fill="{INK if bold else MUTED}">{e(txt)}</text>')

def hint(pts, color="#A8B2AD"):
    add(f'<polyline points="{" ".join(f"{a},{b}" for a, b in pts)}" fill="none" '
        f'stroke="{color}" stroke-width="1.4" stroke-dasharray="5 5" stroke-linejoin="round"/>')

def badge(x, y, label, fill):
    w = 12 + len(label) * 6.7
    add(f'<rect x="{x}" y="{y}" width="{w}" height="21" rx="10.5" fill="{fill}"/>')
    add(f'<text x="{x + w/2}" y="{y + 14.6}" text-anchor="middle" font-family="{FONT}" '
        f'font-size="10.5" font-weight="700" letter-spacing="0.6" fill="#FFFFFF">{e(label)}</text>')

def chapter(x, y, num, title):
    add(f'<rect x="{x}" y="{y - 15}" width="30" height="21" rx="5" fill="{ACCENT}"/>')
    add(f'<text x="{x + 15}" y="{y}" text-anchor="middle" font-family="{MONO}" font-size="12" '
        f'font-weight="600" fill="#FFFFFF">{e(num)}</text>')
    add(f'<text x="{x + 42}" y="{y}" font-family="{FONT}" font-size="13" font-weight="700" '
        f'letter-spacing="1.7" fill="{ACCENT}">{e(tru(title))}</text>')

def stepnum(cx, cy, n, stroke):
    add(f'<circle cx="{cx}" cy="{cy}" r="13" fill="{CARD}" stroke="{stroke}" stroke-width="1.6"/>')
    add(f'<text x="{cx}" y="{cy + 4.2}" text-anchor="middle" font-family="{MONO}" '
        f'font-size="11.5" font-weight="600" fill="{stroke}">{n}</text>')

# ───────────────────────── yerleşim ─────────────────────────
CX, OX = 940, 1520
IRD_X, ETS_X = 660, 1310
BW, BH, PITCH = 420, 128, 166
RAIL_X, RAIL_W = 48, 344
IRD_LOOP, ETS_LOOP = 962, 1012
RIGHT_X, RIGHT_W = 1556, 296
K1_Y, K4_Y, DW, DH = 452, 652, 440, 130

add(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} @H@" width="{W}" height="@H@" '
    f'role="img" aria-label="Türkiye Emisyon Ticaret Sistemi kapsam belirleme karar şeması">')
add('<defs><marker id="ar" viewBox="0 0 10 10" refX="9.2" refY="5" markerWidth="7" '
    'markerHeight="7" orient="auto-start-reverse">'
    '<path d="M0,0 L10,5 L0,10 z" fill="#66746F"/></marker></defs>')
add(f'<rect width="{W}" height="@H@" fill="{GROUND}"/>')

# ── başlık ──
add(f'<text x="48" y="76" font-family="{FONT}" font-size="12.5" font-weight="700" '
    f'letter-spacing="2.1" fill="{ACCENT}">TÜRKİYE EMİSYON TİCARET SİSTEMİ · TESİS DEĞERLENDİRMESİ</text>')
add(f'<text x="48" y="124" font-family="{FONT}" font-size="37" font-weight="700" '
    f'letter-spacing="-0.8" fill="{INK}">İşletmem ETS kapsamına giriyor mu?</text>')
add(f'<text x="48" y="155" font-family="{FONT}" font-size="15" fill="{MUTED}">'
    f'İki soruyu tesis bazında yanıtlayın; kapsam durumunuz, tesis kategoriniz ve '
    f'takvimli yükümlülükleriniz aşağıda.</text>')
add(f'<text x="48" y="181" font-family="{MONO}" font-size="11.5" fill="{FAINT}">'
    f'Dayanak: Türkiye Emisyon Ticaret Sistemi Yönetmeliği — Resmî Gazete 27.08.2026 / 33353</text>')

lx, ly = 1400, 36
add(f'<rect x="{lx}" y="{ly}" width="452" height="152" rx="10" fill="{CARD}" '
    f'stroke="{LINE}" stroke-width="1.4"/>')
add(f'<text x="{lx + 18}" y="{ly + 27}" font-family="{FONT}" font-size="11" font-weight="700" '
    f'letter-spacing="1.2" fill="{MUTED}">ANAHTAR</text>')
for i, (f_, s_, t_) in enumerate([
        (GREEN_F, GREEN_S, "Yükümlülük yok — sistem hiç uygulanmaz"),
        (AMBER_F, AMBER_S, "Yalnızca izleme, raporlama ve doğrulama"),
        (RED_F,   RED_S,   "Tam ETS — sarıdakilere ek olarak izin ve tahsisat teslimi"),
        (NEUTRAL, NEUT_ST, "Karar ve yardımcı bilgi"),
        (None,    MUTED,   "Başvurunun yapıldığı ve işlemi yürüten kurum")]):
    yy = ly + 49 + i * 21
    if f_:
        add(f'<rect x="{lx + 18}" y="{yy - 10}" width="24" height="14" rx="4" fill="{f_}" '
            f'stroke="{s_}" stroke-width="1.5"/>')
        tx = lx + 52
    else:
        who_pill(lx + 18, yy - 11, s_)
        tx = lx + 58
    add(f'<text x="{tx}" y="{yy + 1}" font-family="{FONT}" font-size="12" '
        f'fill="{INK}">{e(t_)}</text>')

add(f'<line x1="48" y1="210" x2="{W - 48}" y2="210" stroke="{INK}" stroke-width="2"/>')

# ── bölüm 1: iki soru ──
chapter(48, 252, "01", "Kapsam ve kategori belirleme")
add(f'<text x="470" y="252" font-family="{FONT}" font-size="11.5" fill="{FAINT}">'
    f'Soldaki sütun yardımcı bilgidir, akışın parçası değildir.</text>')

t, _ = NODE["start"]
box(CX, 322, 320, 58, t, None, fill=CARD, r=29, ts=15)

for key, cy in (("k1", K1_Y), ("k4", K4_Y)):
    title, ref = NODE[key]
    diamond(CX, cy, DW, DH, title, ref)
    add(f'<text x="{CX - DW / 2 + 66}" y="{cy - 28}" text-anchor="end" font-family="{MONO}" '
        f'font-size="12" font-weight="600" letter-spacing="1" fill="{ACCENT}">'
        f'SORU {1 if key == "k1" else 2}</text>')

t, s_ = NODE["out1"]
box(OX, K1_Y, 420, 88, t, s_, fill=GREEN_F, stroke=GREEN_S, tcol=GREEN_T, scol=GREEN_T,
    r=20, ts=16, shadow=True)

conn([(CX, 351), (CX, K1_Y - DH / 2 - 2)])
conn([(CX + DW / 2, K1_Y), (OX - 212, K1_Y)], "HAYIR", (CX + DW / 2 + OX - 212) / 2, K1_Y - 10)
conn([(CX, K1_Y + DH / 2), (CX, K4_Y - DH / 2 - 2)], "EVET", CX - 14, K1_Y + DH / 2 + 42,
     anchor="end")

# özel durumlar paneli — EVET okuna bağlı yan not
OZ_Y = 522
oz_h = draw_panel(ETS_X, OZ_Y, W - 48 - ETS_X, "p_ozel")
hint([(ETS_X, OZ_Y + 30), (CX + 6, OZ_Y + 30)])

# ── ikinci sorudan sonuçlara ──
Y_C = max(OZ_Y + oz_h + 52, K4_Y + DH / 2 + 60)
DIV2 = Y_C + 40
RES_Y = DIV2 + 150
conn([(CX - DW / 2, K4_Y), (IRD_X, K4_Y), (IRD_X, RES_Y - 55)])
label(IRD_X - 12, K4_Y + 44, [("≤ 50.000 t CO₂e", True), ("Kategori A", False)], anchor="end")
conn([(CX, K4_Y + DH / 2), (CX, Y_C), (ETS_X, Y_C), (ETS_X, RES_Y - 55)])
label(CX + 18, Y_C - 26, [("> 50.000 t CO₂e", True),
                          ("Kategori B: 50.001 – 500.000 · Kategori C: > 500.000", False)])

# ── bölüm 2 ──
add(f'<line x1="422" y1="{DIV2}" x2="{IRD_X - 24}" y2="{DIV2}" stroke="{LINE}" stroke-width="1.4"/>')
add(f'<line x1="{IRD_X + 24}" y1="{DIV2}" x2="{ETS_X - 24}" y2="{DIV2}" stroke="{LINE}" stroke-width="1.4"/>')
add(f'<line x1="{ETS_X + 24}" y1="{DIV2}" x2="{W - 48}" y2="{DIV2}" stroke="{LINE}" stroke-width="1.4"/>')
chapter(IRD_X + 44, DIV2 + 44, "02", "Profilinize göre yükümlülükler")
add(f'<text x="{IRD_X + 44}" y="{DIV2 + 70}" font-family="{FONT}" font-size="11.5" fill="{FAINT}">'
    f'Tüm başvuru ve bildirimler, İklim Değişikliği Başkanlığınca kurulan elektronik sistem üzerinden yapılır (m. 34/6).</text>')

t, s_ = NODE["ird"]
box(IRD_X, RES_Y, 440, 108, t, s_, fill=AMBER_F, stroke=AMBER_S, tcol=AMBER_T, scol=AMBER_T,
    r=20, ts=16, shadow=True)
t, s_ = NODE["ets"]
box(ETS_X, RES_Y, 440, 108, t, s_, fill=RED_F, stroke=RED_S, tcol=RED_T, scol=RED_T,
    r=20, ts=16, shadow=True)

STEP0 = RES_Y + 54 + 40 + BH / 2
def sy(i): return STEP0 + i * PITCH

def track(cx, keys, fill, stroke, tcol, scol):
    ys = []
    for i, key in enumerate(keys):
        cy = sy(i)
        ys.append(cy)
        title, sub = NODE[key]
        tag, sub = split_badge(sub)
        ev = tag == "DIŞ OLAY"
        f, st, tc = (EVENT_F, EVENT_S, INK) if ev else (fill, stroke, tcol)
        mid = box(cx, cy, BW, BH, title, sub, fill=f, stroke=st, tcol=tc,
                  scol=(MUTED if ev else scol), ts=14.5, ss=11, shadow=True, who=WHO.get(key))
        stepnum(cx - BW / 2, mid, i + 1, st)
        if key == "e9":
            add(f'<rect x="{cx - BW/2 - 7}" y="{cy - BH/2 - 7}" width="{BW + 14}" '
                f'height="{BH + 14}" rx="15" fill="none" stroke="{OPP_S}" stroke-width="2.4"/>')
            badge(cx - BW / 2 + 26, cy - BH / 2 - 18, "★ FIRSAT ALANI", OPP_S)
        if tag:
            badge(cx + BW / 2 - (96 if tag == "CEZA RİSKİ" else 84), cy - BH / 2 - 11,
                  tag, RED_S if tag == "CEZA RİSKİ" else EVENT_S)
        if i:
            conn([(cx, ys[i - 1] + BH / 2), (cx, cy - BH / 2 - (9 if key == "e9" else 2))])
    return ys

conn([(IRD_X, RES_Y + 54), (IRD_X, sy(0) - BH / 2 - 2)])
conn([(ETS_X, RES_Y + 54), (ETS_X, sy(0) - BH / 2 - 2)])
iy = track(IRD_X, ["i1", "i2", "i3", "i4"], AMBER_F, AMBER_S, AMBER_T, "#6B4A10")
ey = track(ETS_X, ["e%d" % n for n in range(1, 11)], RED_F, RED_S, RED_T, "#6E2A24")

conn([(IRD_X, iy[-1] + BH / 2), (IRD_X, iy[-1] + BH / 2 + 38), (IRD_LOOP, iy[-1] + BH / 2 + 38),
      (IRD_LOOP, iy[1]), (IRD_X + BW / 2 + 2, iy[1])],
     "her sistem yılı için tekrarlanır", 806, iy[-1] + BH / 2 + 28)
conn([(ETS_X, ey[-1] + BH / 2), (ETS_X, ey[-1] + BH / 2 + 38), (ETS_LOOP, ey[-1] + BH / 2 + 38),
      (ETS_LOOP, ey[3]), (ETS_X - BW / 2 - 2, ey[3])],
     "her sistem yılı için tekrarlanır", 1160, ey[-1] + BH / 2 + 28)

draw_panel(RIGHT_X, sy(2) - 84, RIGHT_W, "p_dikkat", fill="#FFF6F4", stroke=RED_S)
hint([(RIGHT_X, sy(2)), (ETS_X + BW / 2, sy(2))], color=RED_S)
TAK_Y = sy(4) - 70
tk_h = draw_panel(RIGHT_X, TAK_Y, RIGHT_W, "p_takvim", fill=CARD, stroke=ACCENT)
BIZ_Y = max(sy(8) - 150, TAK_Y + tk_h + 30)
bh_ = draw_panel(RIGHT_X, BIZ_Y, RIGHT_W, "p_biz", fill=OPP_F, stroke=OPP_S)
hint([(RIGHT_X, sy(8)), (ETS_X + BW / 2 + 7, sy(8))], color=OPP_S)

t, s_ = NODE["kayit"]
CONT_Y = ey[-1] + BH / 2 + 148
box((IRD_X + ETS_X) / 2, CONT_Y, 1100, 92, t, s_, fill=CARD, stroke=NEUT_ST,
    r=12, ts=15, ss=11.5, dash="6 5", smax=104)
hint([(IRD_X, iy[-1] + BH / 2 + 38), (IRD_X, CONT_Y - 46)])
hint([(ETS_X, ey[-1] + BH / 2 + 38), (ETS_X, CONT_Y - 46)])

# ── referans rayı: kesintisiz ──
rail = 288
for key in ("p_ek1", "p_20mw", "p_kural", "p_kisalt", "p_ceza", "p_hesap", "p_gaz"):
    warn = key == "p_ceza"
    rail += draw_panel(RAIL_X, rail, RAIL_W, key, fill="#FFF6F4" if warn else PANEL,
                       stroke=RED_S if warn else PANEL_ST) + 26

# ── bölüm 3: fiyat, en altta ──
SEC3 = max(CONT_Y + 86, rail + 20, BIZ_Y + bh_ + 40)
add(f'<line x1="48" y1="{SEC3}" x2="{W - 48}" y2="{SEC3}" stroke="{LINE}" stroke-width="1.4"/>')
chapter(48, SEC3 + 44, "03", "Fiyatı kim, neye göre belirler")
c3 = SEC3 + 72
n_r, g_r = len(M.PRICE_ROLES), 16
w_r = (W - 96 - g_r * (n_r - 1)) / n_r
rl = [bwrap(txt, int((w_r - 36) / 5.75)) for _, txt in M.PRICE_ROLES]
role_h = 58 + max(len(x) for x in rl) * 16
for i, ((who_, _), lines_) in enumerate(zip(M.PRICE_ROLES, rl)):
    rx = 48 + i * (w_r + g_r)
    last = i == n_r - 1
    add(f'<rect x="{rx}" y="{c3}" width="{w_r}" height="{role_h}" rx="10" '
        f'fill="{OPP_F if last else CARD}" stroke="{OPP_S if last else LINE}" stroke-width="1.4"/>')
    add(f'<clipPath id="rc{i}"><rect x="{rx}" y="{c3}" width="{w_r}" height="{role_h}" rx="10"/></clipPath>')
    add(f'<rect x="{rx}" y="{c3}" width="5" height="{role_h}" fill="{ACCENT}" clip-path="url(#rc{i})"/>')
    add(f'<text x="{rx + 20}" y="{c3 + 30}" font-family="{FONT}" font-size="13.5" font-weight="700" '
        f'fill="{INK}">{e(who_)}</text>')
    for j, l in enumerate(lines_):
        add(f'<text x="{rx + 20}" y="{c3 + 54 + j * 16}" font-family="{FONT}" font-size="12" '
            f'fill="{MUTED}">{e(l)}</text>')
c3 += role_h + 20
h_fiyat = draw_panel(48, c3, W - 96, "p_fiyat")

# ── alt bilgi ──
FY = c3 + h_fiyat + 34
add(f'<line x1="48" y1="{FY}" x2="{W - 48}" y2="{FY}" stroke="{LINE}" stroke-width="1.2"/>')
add(f'<text x="48" y="{FY + 27}" font-family="{FONT}" font-size="11.5" fill="{FAINT}">'
    f'Bu şema bilgilendirme amaçlıdır ve ön değerlendirme niteliğindedir. Kesin kapsam belirlemesi '
    f'tesisin kapasite raporu, yakma ünitelerinin anma ısıl güçleri ve onaylı izleme planı üzerinden '
    f'yapılır; nihai yetki Çevre, Şehircilik ve İklim Değişikliği Bakanlığına bağlı İklim Değişikliği Başkanlığındadır.</text>')
add(f'<text x="{W - 48}" y="{FY + 27}" text-anchor="end" font-family="{MONO}" font-size="11.5" '
    f'fill="{FAINT}">RG 27.08.2026 / 33353</text>')

add('</svg>')

H = int(FY + 62)
open("ets-karar-agaci.svg", "w", encoding="utf-8").write("\n".join(out).replace("@H@", str(H)))
print(f"SVG üretildi — {W} x {H}")
