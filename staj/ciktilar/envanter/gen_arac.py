# -*- coding: utf-8 -*-
"""Etkileşimli aracın (v2) envanterden üretilmesi.
Kullanım: python3 gen_arac.py → ../enerji-destek-araci.html
Veri: veri.py, ek2_ek5.py, cazibe.py, ykh.py, yek.py, ajans.json (Excel envanteriyle aynı kaynak).
"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from veri import *  # noqa
from ek2_ek5 import EK2, EK5
from cazibe import CAZIBE_EK1, DEPREM_EK2
from ykh import YKH
from yek import YEKDEM, YEKDEM_NOT

AJANS = json.load(open(os.path.join(HERE, "ajans.json"), encoding="utf-8"))
AJANS.setdefault("Uşak", [{"ajans": "Zafer Kalkınma Ajansı", "ofis": "Uşak Yatırım Destek Ofisi", "tel": "", "eposta": "usakydo@zafer.gov.tr", "web": "https://zafer.gov.tr/"}])
ORAN = 0.2549

bolge_of = {il: b for b, lst in EK2.items() for il in lst}
iller = []
for il, pl in sorted(PLAKA.items(), key=lambda x: x[1]):
    a = AJANS.get(il, [{}])[0]
    iller.append(dict(il=il, pl=pl, b=bolge_of[il], cz=il in CAZIBE_EK1, dp=DEPREM_EK2.get(il, []), ek5=EK5.get(il, []),
                      ykh=YKH[il], ajans=a.get("ajans", ""), ofis=a.get("ofis", ""), tel=a.get("tel", ""), ep=a.get("eposta", ""),
                      web=a.get("web", ""), ejs=ENERJISA_DAGITIM.get(il, "")))

# Parasal eşikler: kullanılacak değer = ilan, yoksa baz × (1+oran)
def val(e):
    kalem, day, baz, ilan, hes, et, kay, notu = e
    return ilan if ilan is not None else round(baz * (1 + ORAN))
EK = {e[0]: val(e) for e in ESIK}
esik = dict(
    asg12=EK["Asgari sabit yatırım · 1-2. bölge"], asg36=EK["Asgari sabit yatırım · 3-6. bölge"],
    strYt=EK["Stratejik Hamle asgari · yüksek teknoloji"], strDiger=EK["Stratejik Hamle asgari · diğer"],
    strYesil=EK["Yeşil/dijital dönüşüm → Stratejik eşiği"], oncYt=EK["Öncelikli · yüksek teknoloji asgari"],
    oncOyt=EK["Öncelikli · orta-yüksek teknoloji asgari"], faizThp=EK["Faiz desteği üst sınırı · THP/YKH"],
    faizStr=EK["Faiz desteği üst sınırı · Stratejik"], faizOnc=EK["Faiz desteği üst sınırı · Öncelikli"],
    faizHedef=EK["Faiz desteği üst sınırı · Hedef"], makBirim=EK["Makine desteği birim fiyat alt sınırı"],
    makStr=EK["Makine desteği üst sınırı · Stratejik"], makThp=EK["Makine desteği üst sınırı · THP/YKH"],
    vapCap=EK["VAP hibe üst sınırı (2025 → 2026)"], ekaCap=EK["EKA hibe üst sınırı (2025 → 2026)"],
    vapMin=EK["VAP asgari proje bedeli (01.07.2026'dan)"], vapMuh=EK["VAP · mühendis hazırlarsa azami proje bedeli"],
    epsMin=EK["EPS asgari yatırım bedeli"], kosGes=EK["KOSGEB YSDP · GES üst limiti"], kosTemiz=EK["KOSGEB YSDP · temiz ve döngüsel üst limiti"],
    oran=ORAN)
esikTag = {e[0]: e[5] for e in ESIK}

SINIF = {"P10": "Performans desteği", "P13": "Ar-Ge desteği", "P15": "Gelir / piyasa desteği", "P16": "Gelir / piyasa desteği", "P17": "Kapasite tahsisi"}
data = dict(
    kontrol=KONTROL, etiket={k: v for k, v in ETIKET.items()}, esik=esik,
    iller=iller, bolge=[dict(b=b[0], sgk=b[1], oran=b[2], isci=b[3], faiz=b[4], notu=b[5]) for b in BOLGE],
    prog={p[0]: dict(ad=p[1], kurum=p[2], nit=p[3], durum=p[4], kanal=p[5], donem=p[6], hedef=p[7], day=p[8], et=p[9], kay=p[10], notu=p[11],
                     sinif=SINIF.get(p[0], "Yatırım desteği")) for p in PROGRAM},
    destek=[dict(p=d[0], u=d[1], o=d[2], l=d[3], s=d[4], day=d[6], et=d[7]) for d in DESTEK],
    tur=[dict(id=t[0], ad=t[1]) for t in TUR], mprog=[p[0] for p in MPROG],
    m=[dict(t=x[0], p=x[1], d=x[2], g=x[3], day=x[4], et=x[5]) for x in M],
    kum=[dict(a=k[0], b=k[1], c=k[2], d=k[3], day=k[4], et=k[5]) for k in KUM],
    takvim=[dict(a=t[0], b=t[1], o=t[2], p=t[3], et=t[4], kay=t[5]) for t in TAKVIM],
    kaynak=[dict(id=k[0], ad=k[1], tur=k[2], tarih=k[3], url=k[4], notu=k[5]) for k in KAYNAK],
    teyit=[dict(id=t[0], konu=t[1], neden=t[2]) for t in TEYIT],
    yekdem=[dict(ad=y[0], f=y[1], s=y[2], tb=y[3], tv=y[4], yk=y[5], yks=y[6], n=y[7]) for y in YEKDEM], yekNot=YEKDEM_NOT,
    ek4=[dict(g=e[0], t=e[1], d=e[2], en=e[3]) for e in EK4],
    ykhEnerji=YKH_ENERJI, kural=len(KURAL),
)

tpl = open(os.path.join(HERE, "arac.tpl.html"), encoding="utf-8").read()
v1 = open(os.path.join(os.path.dirname(HERE), "enerji-destek-araci.html"), encoding="utf-8").read()
css = re.search(r"<style>(.*?)</style>", v1, re.S).group(1)
if "/*V2-CSS*/" in css:          # yeniden üretimde ekleri çift eklememek için
    css = css.split("/*V2-CSS*/")[0]
out = tpl.replace("/*__CSS__*/", css).replace("/*__DATA__*/", json.dumps(data, ensure_ascii=False, separators=(",", ":")))
open(os.path.join(os.path.dirname(HERE), "enerji-destek-araci.html"), "w", encoding="utf-8").write(out)
print("ok", len(out))
