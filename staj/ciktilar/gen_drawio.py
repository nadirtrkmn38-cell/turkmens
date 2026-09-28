# -*- coding: utf-8 -*-
"""miro_import.py içindeki modelden düzenlenebilir bir .drawio dosyası üretir.

Bağlayıcılar serbest bırakılmaz: her kenarın çıkış/giriş noktası ve dönüş
noktaları açıkça verilir, böylece oklar kutuların üzerinden geçmez ve
etiketler üst üste binmez.
"""
from html import escape
from math import ceil
from miro_import import NODES, EDGES, PANELS, PAL, TITLE, WHO, PRICE_ROLES, sy, IRD_X, ETS_X, RES_Y, CX

cells, eid = [], 2
idmap, geom = {}, {}

def add(s):
    cells.append(s)

def esc(t):
    return escape(str(t), quote=True)

# ───────────────────── kenar yönlendirme tablosu ─────────────────────
# (kaynak, hedef, etiket) -> (çıkışX, çıkışY, girişX, girişY, dönüş noktaları, etiket kayması)
IRD_LOOP_X, ETS_LOOP_X = 960, 1030
R = {
    ("start", "k1", ""):                       (.5, 1, .5, 0, [], None),
    ("k1", "out1", "HAYIR"):                    (1, .5, 0, .5, [], None),
    ("k1", "k4", "EVET"):                      (.5, 1, .5, 0, [], None),
    ("k4", "ird", "≤ 50.000 · Kategori A"):    (0, .5, .5, 0, [(IRD_X, 700)], (-60, 0)),
    ("k4", "ets", "> 50.000 · Kategori B ve C"):
        (.5, 1, .5, 0, [(CX, 860), (ETS_X, 860)], (60, -12)),

    ("i4", "i2", "her sistem yılı için tekrarlanır"):
        (1, .5, 1, .5, [(IRD_LOOP_X, sy(3)), (IRD_LOOP_X, sy(1))], None),
    ("e10", "e4", "her sistem yılı için tekrarlanır"):
        (0, .5, 0, .5, [(ETS_LOOP_X, sy(9)), (ETS_LOOP_X, sy(3))], (-20, 0)),

    ("i4", "kayit", ""):        (0, .5, .02, 0, [(415, sy(3)), (415, sy(9) + 120)], None),
    ("e10", "kayit", ""):       (.5, 1, .8, 0, [], None),
    ("p_ozel", "k4", ""):       (0, .5, 1, .5, [], None),
    ("p_dikkat", "e3", ""):     (0, .5, 1, .5, [], None),
    ("p_biz", "e9", ""):        (0, .5, 1, .5, [], None),
}
DEFAULT_ROUTE = (.5, 1, .5, 0, [], None)

# ───────────────────── elmas boyutlarını büyüt ─────────────────────
DIAMOND_PAD = (90, 45)     # metin elmasın içine sığsın

def node_style(pal, shape):
    p = PAL[pal]
    base = "shape=rhombus;" if shape == "rhombus" else "rounded=1;arcSize=14;"
    return (base + f"whiteSpace=wrap;html=1;fillColor={p['fill']};strokeColor={p['border']};"
            f"fontColor={p['text']};strokeWidth=2;fontFamily=Helvetica;verticalAlign=middle;"
            f"align=center;spacingLeft=10;spacingRight=10;")

def node_label(title, sub, sub_px=10, who=None):
    t = f"&lt;b&gt;{esc(title)}&lt;/b&gt;"
    if sub:
        t += (f"&lt;br&gt;&lt;font style=&quot;font-size:{sub_px}px&quot;&gt;"
              f"{esc(sub)}&lt;/font&gt;")
    if who:
        t += (f"&lt;br&gt;&lt;font style=&quot;font-size:{sub_px}px&quot; color=&quot;#0b5d58&quot;&gt;"
              f"&lt;b&gt;KİM:&lt;/b&gt; {esc(who)}&lt;/font&gt;")
    return t

for key, shape, cx, cy, w, h, title, sub, pal in NODES:
    eid += 1
    idmap[key] = str(eid)
    if shape == "rhombus":
        w, h = w + DIAMOND_PAD[0], h + DIAMOND_PAD[1]
        fs, sp = 12, 10
    elif key in ("ird", "ets", "out1", "out2", "kayit"):
        fs, sp = 14, 11
    else:
        fs, sp = 12, 10
    if key in WHO:
        h += 34
    geom[key] = (cx, cy, w, h)
    add(f'<mxCell id="{eid}" value="{node_label(title, sub, sp, WHO.get(key))}" '
        f'style="{node_style(pal, shape)}fontSize={fs};" vertex="1" parent="1">'
        f'<mxGeometry x="{cx - w // 2}" y="{cy - h // 2}" width="{w}" height="{h}" '
        f'as="geometry"/></mxCell>')

# ───────────────────── paneller: yüksekliği içeriğe göre ─────────────────────
def panel_height(w, heading, lines, fs=11):
    cpl = max(20, int((w - 24) / (fs * 0.52)))
    n = 2  # başlık + boşluk
    for ln in lines:
        n += max(1, ceil(len(ln) / cpl)) if ln else 1
    return int(30 + n * (fs * 1.42) + 16)

LEFT_X, LEFT_TOP, LEFT_GAP = 220, 276, 28
stack = LEFT_TOP

BOTTOM_KEYS = ("p_fiyat",)
bottom = []
for key, cx, cy, w, h, heading, lines, pal in PANELS:
    lines = [ln for ln in lines if ln != "||"]
    if key in BOTTOM_KEYS:
        bottom.append((key, w, heading, lines, pal))
        continue
    eid += 1
    idmap[key] = str(eid)
    p = PAL[pal]
    hh = panel_height(w, heading, lines)
    body = f"&lt;b&gt;{esc(heading)}&lt;/b&gt;&lt;br&gt;&lt;br&gt;" + "&lt;br&gt;".join(
        (esc(ln) if ln else "&amp;nbsp;") for ln in lines)
    if cx == LEFT_X:                       # sol sütun: üst üste dizilir
        top = stack
        stack += hh + LEFT_GAP
    else:
        top = cy - h // 2
    geom[key] = (cx, top + hh // 2, w, hh)
    add(f'<mxCell id="{eid}" value="{body}" style="rounded=0;whiteSpace=wrap;html=1;'
        f'fillColor={p["fill"]};strokeColor={p["border"]};fontColor={p["text"]};strokeWidth=1;'
        f'fontFamily=Helvetica;fontSize=11;align=left;verticalAlign=top;spacing=10;" '
        f'vertex="1" parent="1"><mxGeometry x="{cx - w // 2}" y="{top}" width="{w}" '
        f'height="{hh}" as="geometry"/></mxCell>')

# ───────────────────── fiyat bölümü: en altta ─────────────────────
ytop = max(stack, max(gy + gh // 2 for _gx, gy, _gw, gh in geom.values())) + 60
n = len(PRICE_ROLES)
rw = (1804 - 16 * (n - 1)) // n
for i, (org, txt) in enumerate(PRICE_ROLES):
    eid += 1
    add(f'<mxCell id="{eid}" value="&lt;b&gt;{esc(org)}&lt;/b&gt;&lt;br&gt;{esc(txt)}" '
        f'style="rounded=1;arcSize=8;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#0b5d58;'
        f'fontColor=#16232b;fontFamily=Helvetica;fontSize=11;align=left;verticalAlign=top;spacing=10;" '
        f'vertex="1" parent="1"><mxGeometry x="{48 + i * (rw + 16)}" y="{ytop}" width="{rw}" '
        f'height="96" as="geometry"/></mxCell>')
ytop += 96 + 20
for key, w, heading, lines, pal in bottom:
    eid += 1
    idmap[key] = str(eid)
    p = PAL[pal]
    hh = panel_height(w, heading, lines)
    body = f"&lt;b&gt;{esc(heading)}&lt;/b&gt;&lt;br&gt;&lt;br&gt;" + "&lt;br&gt;".join(
        (esc(ln) if ln else "&amp;nbsp;") for ln in lines)
    add(f'<mxCell id="{eid}" value="{body}" style="rounded=0;whiteSpace=wrap;html=1;'
        f'fillColor={p["fill"]};strokeColor={p["border"]};fontColor={p["text"]};strokeWidth=1;'
        f'fontFamily=Helvetica;fontSize=11;align=left;verticalAlign=top;spacing=10;" '
        f'vertex="1" parent="1"><mxGeometry x="48" y="{ytop}" width="{w}" '
        f'height="{hh}" as="geometry"/></mxCell>')
    geom[key] = (48 + w // 2, ytop + hh // 2, w, hh)
    ytop += hh + 30
PAGE_H = ytop + 40

# ───────────────────── başlık ─────────────────────
k, cx, cy, w, h, t, s, pal = TITLE
eid += 1
add(f'<mxCell id="{eid}" value="&lt;b&gt;{esc(t)}&lt;/b&gt;&lt;br&gt;&lt;br&gt;'
    f'&lt;font style=&quot;font-size:12px&quot;&gt;{esc(s)}&lt;/font&gt;" '
    f'style="text;html=1;align=left;verticalAlign=middle;fontSize=26;fontColor=#16232b;'
    f'fontFamily=Helvetica;" vertex="1" parent="1">'
    f'<mxGeometry x="{cx - w // 2}" y="{cy - h // 2}" width="{w}" height="{h}" '
    f'as="geometry"/></mxCell>')

# ───────────────────── kenarlar ─────────────────────
for src, dst, lab, dashed in EDGES:
    if src not in idmap or dst not in idmap:
        continue
    ex, ey, nx, ny, pts, off = R.get((src, dst, lab), DEFAULT_ROUTE)
    eid += 1
    st = ("edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;jettySize=auto;orthogonalLoop=1;"
          "strokeColor=#6e7b76;strokeWidth=2;fontSize=11;fontColor=#4a5854;"
          "labelBackgroundColor=#fbfbf8;endArrow=block;endFill=1;"
          f"exitX={ex};exitY={ey};exitDx=0;exitDy=0;entryX={nx};entryY={ny};entryDx=0;entryDy=0;"
          + ("dashed=1;" if dashed else ""))
    inner = ""
    if pts:
        inner += "<Array as=\"points\">" + "".join(
            f'<mxPoint x="{x}" y="{y}"/>' for x, y in pts) + "</Array>"
    if off:
        inner += f'<mxPoint as="offset" x="{off[0]}" y="{off[1]}"/>'
    add(f'<mxCell id="{eid}" value="{esc(lab)}" style="{st}" edge="1" parent="1" '
        f'source="{idmap[src]}" target="{idmap[dst]}">'
        f'<mxGeometry relative="1" as="geometry">{inner}</mxGeometry></mxCell>')

xml = ('<mxfile host="app.diagrams.net"><diagram name="ETS Kapsam Pusulası" id="ets-0">'
       '<mxGraphModel dx="1400" dy="900" grid="1" gridSize="10" guides="1" tooltips="1" '
       'connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1900" '
       f'pageHeight="{PAGE_H}" background="#fbfbf8" math="0" shadow="0">'
       '<root><mxCell id="0"/><mxCell id="1" parent="0"/>'
       + "".join(cells) +
       '</root></mxGraphModel></diagram></mxfile>')

open("ETS-Karar-Agaci.drawio", "w", encoding="utf-8").write(xml)
print("düğüm:", len(NODES), "panel:", len(PANELS), "kenar:", len(EDGES))
