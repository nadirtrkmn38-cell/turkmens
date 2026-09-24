#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TR ETS kapsam belirleme şemasının etkileşimli sürümünü üretir.

İçerik miro_import.py'deki modelden okunur; yerleşim ve davranış
ets-karar-araci.tpl.html şablonundadır. Böylece PDF, drawio ve etkileşimli
araç aynı metni paylaşır.

Kullanım:  python3 gen_interaktif.py   →   ets-karar-araci.html
"""
import json
import os

import miro_import as M

HERE = os.path.dirname(os.path.abspath(__file__))

nodes = {k: {"t": t, "s": s} for (k, _, _, _, _, _, t, s, _) in M.NODES}
panels = {k: {"t": t, "l": lines} for (k, _, _, _, _, t, lines, _) in M.PANELS}
data = {"nodes": nodes, "who": M.WHO, "panels": panels, "roles": M.PRICE_ROLES}

tpl = open(os.path.join(HERE, "ets-karar-araci.tpl.html"), encoding="utf-8").read()
assert "/*@DATA@*/null" in tpl
out = tpl.replace("/*@DATA@*/null", json.dumps(data, ensure_ascii=False).replace("</", "<\\/"))
open(os.path.join(HERE, "ets-karar-araci.html"), "w", encoding="utf-8").write(out)
print("ets-karar-araci.html üretildi —", len(out) // 1024, "KB")
