# -*- coding: utf-8 -*-
"""miro_import.py içindeki modelden düzenlenebilir bir .drawio dosyası üretir."""
from html import escape
from miro_import import NODES, EDGES, PANELS, PAL, TITLE

cells, eid = [], 2
idmap = {}

def add(s):
    cells.append(s)

def style(pal, shape="rounded", extra=""):
    p = PAL[pal]
    base = {
        "rounded": "rounded=1;arcSize=12;",
        "rect": "rounded=0;",
        "rhombus": "shape=rhombus;",
    }[shape]
    return (base + f"whiteSpace=wrap;html=1;fillColor={p['fill']};strokeColor={p['border']};"
            f"fontColor={p['text']};strokeWidth=2;fontFamily=Helvetica;verticalAlign=middle;"
            + extra)

def label(title, sub):
    t = escape(title)
    return f"&lt;b&gt;{t}&lt;/b&gt;" + (f"&lt;br&gt;&lt;font style='font-size:10px'&gt;{escape(sub)}&lt;/font&gt;" if sub else "")

for key, shape, cx, cy, w, h, title, sub, pal in NODES:
    eid += 1
    idmap[key] = str(eid)
    sh = "rhombus" if shape == "rhombus" else "rounded"
    add(f'<mxCell id="{eid}" value="{label(title, sub)}" style="{style(pal, sh)}fontSize=13;" '
        f'vertex="1" parent="1"><mxGeometry x="{cx - w//2}" y="{cy - h//2}" width="{w}" '
        f'height="{h}" as="geometry"/></mxCell>')

for key, cx, cy, w, h, heading, lines, pal in PANELS:
    eid += 1
    idmap[key] = str(eid)
    body = f"&lt;b&gt;{escape(heading)}&lt;/b&gt;&lt;br&gt;" + "&lt;br&gt;".join(
        escape(ln) if ln else "&amp;nbsp;" for ln in lines)
    add(f'<mxCell id="{eid}" value="{body}" style="{style(pal, "rect")}'
        f'align=left;verticalAlign=top;fontSize=10;spacing=8;strokeWidth=1;" '
        f'vertex="1" parent="1"><mxGeometry x="{cx - w//2}" y="{cy - h//2}" width="{w}" '
        f'height="{h}" as="geometry"/></mxCell>')

k, cx, cy, w, h, t, s, pal = TITLE
eid += 1
add(f'<mxCell id="{eid}" value="{label(t, s)}" style="text;html=1;align=left;'
    f'verticalAlign=middle;fontSize=26;fontColor=#16232b;fontFamily=Helvetica;" vertex="1" '
    f'parent="1"><mxGeometry x="{cx - w//2}" y="{cy - h//2}" width="{w}" height="{h}" '
    f'as="geometry"/></mxCell>')

for src, dst, lab, dashed in EDGES:
    if src not in idmap or dst not in idmap:
        continue
    eid += 1
    st = ("edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;strokeColor=#6e7b76;strokeWidth=2;"
          "fontSize=11;fontColor=#5c6a66;endArrow=block;endFill=1;"
          + ("dashed=1;" if dashed else ""))
    add(f'<mxCell id="{eid}" value="{escape(lab)}" style="{st}" edge="1" parent="1" '
        f'source="{idmap[src]}" target="{idmap[dst]}"><mxGeometry relative="1" as="geometry"/></mxCell>')

xml = ('<mxfile host="app.diagrams.net"><diagram name="ETS Kapsam Pusulası">'
       '<mxGraphModel dx="1400" dy="900" grid="1" gridSize="10" page="1" pageScale="1" '
       'pageWidth="1900" pageHeight="3100" background="#fbfbf8" math="0" shadow="0">'
       '<root><mxCell id="0"/><mxCell id="1" parent="0"/>'
       + "".join(cells) +
       '</root></mxGraphModel></diagram></mxfile>')

open("ETS-Karar-Agaci.drawio", "w", encoding="utf-8").write(xml)
print("düğüm:", len(NODES), "panel:", len(PANELS), "bağlayıcı:", len(EDGES))
