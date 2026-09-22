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

FONT = "Archivo, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"
MONO = "'IBM Plex Mono', 'SFMono-Regular', Consolas, monospace"

out = []
def add(s): out.append(s)
def e(t): return escape(str(t), quote=True)
def tru(t): return t.replace("i", "İ").upper()

# ───────────────────────── içerik modeli ─────────────────────────
NODE = {k: (title, sub) for k, _sh, _x, _y, _w, _h, title, sub, _p in M.NODES}
PANEL_TXT = {k: (heading, lines) for k, _x, _y, _w, _h, heading, lines, _p in M.PANELS}

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

def tblock(x, top, lines, size, weight, color, lh, anchor="middle"):
    parts = "".join(f'<tspan x="{x}" dy="{0 if i == 0 else lh}">{e(l)}</tspan>'
                    for i, l in enumerate(lines))
    add(f'<text x="{x}" y="{top + size * 0.80}" text-anchor="{anchor}" font-family="{FONT}" '
        f'font-size="{size}" font-weight="{weight}" fill="{color}">{parts}</text>')

def box(cx, cy, w, h, title, sub=None, fill=NEUTRAL, stroke=NEUT_ST, tcol=INK, scol=MUTED,
        r=10, sw=1.7, ts=15, ss=11.5, dash=None, shadow=False):
    x, y = cx - w / 2, cy - h / 2
    if shadow:
        add(f'<rect x="{x + 1}" y="{y + 3}" width="{w}" height="{h}" rx="{r}" '
            f'fill="#14212A" opacity="0.055"/>')
    d = f' stroke-dasharray="{dash}"' if dash else ""
    add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" '
        f'stroke="{stroke}" stroke-width="{sw}"{d}/>')
    tl = wrap(title, int((w - 34) / (ts * 0.505)))
    sl = wrap(sub, int((w - 34) / (ss * 0.505))) if sub else []
    th, sh_ = len(tl) * ts * 1.2, len(sl) * ss * 1.28
    gap = 7 if sl else 0
    top = cy - (th + gap + sh_) / 2
    tblock(cx, top, tl, ts, 600, tcol, ts * 1.2)
    if sl:
        tblock(cx, top + th + gap, sl, ss, 400, scol, ss * 1.28)

def diamond(cx, cy, w, h, title, ref=None):
    add(f'<polygon points="{cx},{cy - h/2} {cx + w/2},{cy} {cx},{cy + h/2} {cx - w/2},{cy}" '
        f'fill="{NEUTRAL}" stroke="{NEUT_ST}" stroke-width="1.9"/>')
    tl = wrap(title, 46)
    tblock(cx, cy - len(tl) * 15 * 1.2 / 2, tl, 15, 600, INK, 15 * 1.2)
    if ref:
        add(f'<text x="{cx}" y="{cy + h/2 + 21}" text-anchor="middle" font-family="{MONO}" '
            f'font-size="11" fill="{FAINT}">{e(ref)}</text>')

def panel(x, y, w, heading, lines, fill=PANEL, stroke=PANEL_ST):
    slot, pad, yy = len(out), 18, y + 52
    for ln in lines:
        if not ln:
            yy += 9
        elif ln.startswith("•"):
            body = ln.lstrip("• ").strip()
            for i, l in enumerate(wrap(body, int((w - 2 * pad - 12) / 6.05))):
                add(f'<text x="{x + pad}" y="{yy}" font-family="{FONT}" font-size="12" '
                    f'fill="{INK}">{e(("•  " if i == 0 else "    ") + l)}</text>')
                yy += 16
            yy += 3
        elif len(ln) < 34 and ln == tru(ln):
            add(f'<text x="{x + pad}" y="{yy}" font-family="{FONT}" font-size="11" '
                f'font-weight="700" letter-spacing="1.1" fill="{MUTED}">{e(ln)}</text>')
            yy += 20
        else:
            for l in wrap(ln, int((w - 2 * pad) / 6.10)):
                add(f'<text x="{x + pad}" y="{yy}" font-family="{FONT}" font-size="12" '
                    f'fill="{INK}">{e(l)}</text>')
                yy += 16
            yy += 5
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
RES_Y, STEP0, PITCH, BW, BH = 1430, 1576, 126, 420, 84
RAIL_X, RAIL_W = 48, 344
IRD_LOOP, ETS_LOOP = 962, 1602

def sy(i): return STEP0 + i * PITCH

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
    f'Dört soruyu tesis bazında yanıtlayın; kapsam durumunuz, tesis kategoriniz ve '
    f'takvimli yükümlülükleriniz aşağıda.</text>')
add(f'<text x="48" y="181" font-family="{MONO}" font-size="11.5" fill="{FAINT}">'
    f'Dayanak: Türkiye Emisyon Ticaret Sistemi Yönetmeliği — Resmî Gazete 27.08.2026 / 33353</text>')

lx, ly = 1400, 44
add(f'<rect x="{lx}" y="{ly}" width="452" height="128" rx="10" fill="{CARD}" '
    f'stroke="{LINE}" stroke-width="1.4"/>')
add(f'<text x="{lx + 18}" y="{ly + 27}" font-family="{FONT}" font-size="11" font-weight="700" '
    f'letter-spacing="1.2" fill="{MUTED}">RENK ANAHTARI</text>')
for i, (f_, s_, t_) in enumerate([
        (GREEN_F, GREEN_S, "Yükümlülük yok — sistem hiç uygulanmaz"),
        (AMBER_F, AMBER_S, "Yalnızca izleme, raporlama ve doğrulama"),
        (RED_F,   RED_S,   "Tam ETS — izin, İRD ve tahsisat teslimi"),
        (NEUTRAL, NEUT_ST, "Karar ve yardımcı bilgi")]):
    yy = ly + 49 + i * 21
    add(f'<rect x="{lx + 18}" y="{yy - 10}" width="24" height="14" rx="4" fill="{f_}" '
        f'stroke="{s_}" stroke-width="1.5"/>')
    add(f'<text x="{lx + 52}" y="{yy + 1}" font-family="{FONT}" font-size="12" '
        f'fill="{INK}">{e(t_)}</text>')

add(f'<line x1="48" y1="210" x2="{W - 48}" y2="210" stroke="{INK}" stroke-width="2"/>')

# ── bölüm 1 ──
chapter(48, 252, "01", "Kapsam ve kategori belirleme")
add(f'<text x="470" y="252" font-family="{FONT}" font-size="11.5" fill="{FAINT}">'
    f'Soldaki sütun yardımcı bilgidir, akışın parçası değildir.</text>')

rail = 288
for key in ("p_ek1", "p_20mw", "p_kural", "p_istisna"):
    rail += draw_panel(RAIL_X, rail, RAIL_W, key) + 26

t, _ = NODE["start"]
box(CX, 322, 320, 58, t, None, fill=CARD, r=29, ts=15)

for key, cy, w, h in (("k1", 452, 440, 130), ("k2", 664, 440, 130),
                      ("k3", 884, 476, 136), ("k4", 1104, 440, 130)):
    title, ref = NODE[key]
    diamond(CX, cy, w, h, title, ref)

for key, cy in (("out1", 452), ("out2", 664)):
    t, s_ = NODE[key]
    box(OX, cy, 420, 88, t, s_, fill=GREEN_F, stroke=GREEN_S, tcol=GREEN_T, scol=GREEN_T,
        r=20, ts=16, shadow=True)

conn([(CX, 351), (CX, 385)])
conn([(CX + 220, 452), (OX - 212, 452)], "HAYIR", (CX + 220 + OX - 212) / 2, 442)
conn([(CX, 517), (CX, 597)], "EVET", CX - 26, 562, anchor="end")
conn([(CX + 220, 664), (OX - 212, 664)], "EVET", (CX + 220 + OX - 212) / 2, 654)
conn([(CX, 729), (CX, 814)], "HAYIR", CX - 26, 778, anchor="end")
conn([(CX, 952), (CX, 1037)], "HAYIR", CX - 26, 1000, anchor="end")

# ── bölüm 2 ──
add(f'<line x1="48" y1="1310" x2="{W - 48}" y2="1310" stroke="{LINE}" stroke-width="1.4"/>')
chapter(470, 1354, "02", "Profilinize göre yükümlülükler")

t, s_ = NODE["ird"]
box(IRD_X, RES_Y, 440, 106, t, s_, fill=AMBER_F, stroke=AMBER_S, tcol=AMBER_T, scol=AMBER_T,
    r=20, ts=16, shadow=True)
t, s_ = NODE["ets"]
box(ETS_X, RES_Y, 440, 106, t, s_, fill=RED_F, stroke=RED_S, tcol=RED_T, scol=RED_T,
    r=20, ts=16, shadow=True)

conn([(CX - 238, 884), (600, 884), (600, RES_Y - 53)],
     "EVET — kategoriden bağımsız", 594, 874, anchor="end")
conn([(CX - 220, 1104), (742, 1104), (742, RES_Y - 53)],
     "≤ 50.000 · Kategori A", 736, 1094, anchor="end")
conn([(CX + 220, 1104), (1180, 1104), (1180, RES_Y - 53)],
     "50.001 – 500.000 · Kategori B", 1188, 1094, anchor="start")
conn([(CX, 1169), (CX, 1230), (1424, 1230), (1424, RES_Y - 53)],
     "> 500.000 · Kategori C", 1432, 1220, anchor="start")

def track(cx, keys, fill, stroke, tcol, scol):
    ys = []
    for i, key in enumerate(keys):
        cy = sy(i)
        ys.append(cy)
        title, sub = NODE[key]
        tag, sub = split_badge(sub)
        f, st, tc = (EVENT_F, EVENT_S, INK) if tag == "DIŞ OLAY" else (fill, stroke, tcol)
        box(cx, cy, BW, BH, title, sub, fill=f, stroke=st, tcol=tc,
            scol=(MUTED if tag == "DIŞ OLAY" else scol), ts=14.5, ss=11, shadow=True)
        stepnum(cx - BW / 2, cy, i + 1, st)
        if tag:
            badge(cx + BW / 2 - (96 if tag == "CEZA RİSKİ" else 84), cy - BH / 2 - 11,
                  tag, RED_S if tag == "CEZA RİSKİ" else EVENT_S)
        if i:
            conn([(cx, ys[i - 1] + BH / 2), (cx, cy - BH / 2 - 7)])
    return ys

conn([(IRD_X, RES_Y + 53), (IRD_X, sy(0) - BH / 2 - 7)])
conn([(ETS_X, RES_Y + 53), (ETS_X, sy(0) - BH / 2 - 7)])
iy = track(IRD_X, ["i1", "i2", "i3", "i4"], AMBER_F, AMBER_S, AMBER_T, "#6B4A10")
ey = track(ETS_X, ["e%d" % n for n in range(1, 11)], RED_F, RED_S, RED_T, "#6E2A24")

conn([(IRD_X, iy[-1] + BH / 2), (IRD_X, iy[-1] + BH / 2 + 38), (IRD_LOOP, iy[-1] + BH / 2 + 38),
      (IRD_LOOP, iy[1]), (IRD_X + BW / 2 + 7, iy[1])],
     "her sistem yılı için tekrarlanır", 806, iy[-1] + BH / 2 + 28)
conn([(ETS_X, ey[-1] + BH / 2), (ETS_X, ey[-1] + BH / 2 + 38), (ETS_LOOP, ey[-1] + BH / 2 + 38),
      (ETS_LOOP, ey[3]), (ETS_X + BW / 2 + 7, ey[3])],
     "her sistem yılı için tekrarlanır", 1456, ey[-1] + BH / 2 + 28)

draw_panel(1626, sy(2) - 96, 226, "p_dikkat", fill="#FFF6F4", stroke=RED_S)
hint([(1626, sy(2)), (ETS_X + BW / 2, sy(2))], color=RED_S)
hint([(RAIL_X + RAIL_W, RES_Y), (IRD_X - BW / 2 - 10, RES_Y)])

t, s_ = NODE["kayit"]
CONT_Y = ey[-1] + BH / 2 + 148
box((IRD_X + ETS_X) / 2, CONT_Y, 1100, 92, t, s_, fill=CARD, stroke=NEUT_ST,
    r=12, ts=15, ss=11.5, dash="6 5")
hint([(IRD_X, iy[-1] + BH / 2 + 38), (IRD_X, CONT_Y - 46)])
hint([(ETS_X, ey[-1] + BH / 2 + 38), (ETS_X, CONT_Y - 46)])

# ── referans rayının devamı ──
rail = max(rail, 1470)
for key in ("p_ceza", "p_hesap", "p_gaz"):
    fl = "#FFF6F4" if key == "p_ceza" else PANEL
    st = RED_S if key == "p_ceza" else PANEL_ST
    rail += draw_panel(RAIL_X, rail, RAIL_W, key, fill=fl, stroke=st) + 26

# ── alt bilgi ──
FY = max(CONT_Y + 70, rail + 16)
add(f'<line x1="48" y1="{FY}" x2="{W - 48}" y2="{FY}" stroke="{LINE}" stroke-width="1.2"/>')
add(f'<text x="48" y="{FY + 27}" font-family="{FONT}" font-size="11.5" fill="{FAINT}">'
    f'Bu şema bilgilendirme amaçlıdır ve ön değerlendirme niteliğindedir. Kesin kapsam belirlemesi '
    f'tesisin kapasite raporu, yakma ünitelerinin anma ısıl güçleri ve onaylı izleme planı üzerinden '
    f'yapılır; nihai yetki İklim Değişikliği Başkanlığı’ndadır.</text>')
add(f'<text x="{W - 48}" y="{FY + 27}" text-anchor="end" font-family="{MONO}" font-size="11.5" '
    f'fill="{FAINT}">RG 27.08.2026 / 33353</text>')

add('</svg>')

H = int(FY + 62)
open("ets-karar-agaci.svg", "w", encoding="utf-8").write("\n".join(out).replace("@H@", str(H)))
print(f"SVG üretildi — {W} x {H}")
