# -*- coding: utf-8 -*-
"""Enerji Yatırım Destekleri Veri Envanteri 2026 — Excel üretici.
Kullanım: python3 gen_envanter.py  → ../Enerji-Yatirim-Destekleri-Envanteri-2026.xlsx
"""
import json, os, sys
from datetime import date
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.formatting.rule import CellIsRule, FormulaRule
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from veri import *                      # noqa
from ek2_ek5 import EK2, EK5
from cazibe import CAZIBE_EK1, DEPREM_EK2
from ykh import YKH
from yek import YEKDEM, YEKDEM_NOT
AJANS = json.load(open(os.path.join(HERE, "ajans.json"), encoding="utf-8"))

OUT = os.path.join(os.path.dirname(HERE), "Enerji-Yatirim-Destekleri-Envanteri-2026.xlsx")

F = "Arial"
NAVY = "0B1F33"
f_title = Font(name=F, size=14, bold=True, color=NAVY)
f_sub = Font(name=F, size=10, italic=True, color="475467")
f_head = Font(name=F, size=10, bold=True, color="FFFFFF")
f_body = Font(name=F, size=10, color="0F1B2A")
f_bold = Font(name=F, size=10, bold=True, color="0F1B2A")
f_link = Font(name=F, size=10, color="1F4FD1", underline="single")
f_input = Font(name=F, size=10, bold=True, color="0000FF")
fill_head = PatternFill("solid", fgColor=NAVY)
fill_input = PatternFill("solid", fgColor="FFF2CC")
fill_zebra = PatternFill("solid", fgColor="F5F7FA")
thin = Side(style="thin", color="D5DCE4")
border = Border(left=thin, right=thin, top=thin, bottom=thin)
wrap = Alignment(wrap_text=True, vertical="top")
center = Alignment(horizontal="center", vertical="top", wrap_text=True)

TAG_STYLE = {  # öncelik: TEY > YOR > VAR > HES > DUY > MEV
    "TEY": ("FFF3DC", "8F5200"), "YOR": ("EEF1F4", "475467"), "VAR": ("F3EFFE", "6941C6"),
    "HES": ("E5F3F0", "0B7A6E"), "DUY": ("E6F1FB", "0A6D9C"), "MEV": ("1D3048", "FFFFFF"),
}
ORDER = ["TEY", "YOR", "VAR", "HES", "DUY", "MEV"]


def tag_text(code):
    parts = [p.strip() for p in str(code).split(",") if p.strip()]
    return " + ".join(ETIKET[p][0] for p in parts)


def tag_cell(c, code):
    parts = [p.strip() for p in str(code).split(",") if p.strip()]
    c.value = tag_text(code)
    key = next((k for k in ORDER if k in parts), "MEV")
    bg, fg = TAG_STYLE[key]
    c.fill = PatternFill("solid", fgColor=bg)
    c.font = Font(name=F, size=9, bold=True, color=fg)
    c.alignment = center
    c.border = border


def sheet(wb, name, title, sub, headers, widths, first=False):
    ws = wb.active if first else wb.create_sheet(name)
    ws.title = name
    ws["A1"] = title; ws["A1"].font = f_title
    ws["A2"] = sub; ws["A2"].font = f_sub
    for i, (h, w) in enumerate(zip(headers, widths), start=1):
        c = ws.cell(row=4, column=i, value=h)
        c.font = f_head; c.fill = fill_head; c.alignment = Alignment(wrap_text=True, vertical="center"); c.border = border
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.row_dimensions[4].height = 30
    ws.freeze_panes = "A5"
    ws.sheet_view.showGridLines = False
    return ws


def put(ws, r, c, v, font=None, align=None, fmt=None, fill=None):
    cell = ws.cell(row=r, column=c, value=v)
    cell.font = font or f_body
    cell.alignment = align or wrap
    cell.border = border
    if fmt: cell.number_format = fmt
    if fill: cell.fill = fill
    return cell


def finish(ws, ncols, last_row):
    ws.auto_filter.ref = f"A4:{get_column_letter(ncols)}{max(last_row, 5)}"


wb = Workbook()

# ============================================================ 1. OKUMA KILAVUZU
ws = sheet(wb, "Okuma Kılavuzu", "Enerji Yatırım Destekleri Veri Envanteri 2026",
           f"Türkiye'de enerji yatırımları için kamu destekleri, uygunluk kuralları ve il katmanı · Son kontrol: {KONTROL}",
           ["Bölüm", "Açıklama"], [34, 120], first=True)
rows = [
    ("Amaç", "Belirli bir enerji yatırımı için hangi kamu desteğine, hangi şartla, hangi ilde ve ne kadar erişilebileceğini gösteren karar motoruna veri sağlamak. Her satır kaynak, madde ve etiket taşır."),
    ("Kapsam", "9903 sayılı Karar (THP, YKH, Stratejik, Öncelikli, Hedef, bölgesel), Yeşil Dönüşüm Programı, VAP, EPS, EKA, KOSGEB, TÜBİTAK 1832, HIT-30, YEKDEM, lisanssız üretim, YEKA 2026, kalkınma ajansları."),
    ("Destek sınıfları", "Yatırım desteği (hibe, vergi, faiz, KDV, gümrük, SGK) · Performans desteği (EKA) · Gelir/piyasa desteği (YEKDEM, lisanssız ihtiyaç fazlası) · Kapasite tahsisi (YEKA) · Ar-Ge desteği (1832). Sınıflar karıştırılmamalı; YEKDEM bir yatırım hibesi değildir."),
    ("Yöntem", "Resmî Gazete PDF'leri (taranmış ekler dahil), Bakanlık duyuruları ve usul-esas belgeleri doğrudan okundu. Resmî Gazete'ye erişilemeyen yerlerde Lexpera konsolide metinleri kullanıldı. İkincil kaynaktan gelen her bilgi 'Teyit edilecek' etiketlidir."),
    ("Yeniden değerleme oranı", "Parasal eşikler sayfasındaki sarı hücre (%25,49) değiştirildiğinde hesaplanan 2026 tutarları kendiliğinden güncellenir. 2027 için yeni oran girilip ilan edilen tutarlarla karşılaştırılabilir."),
    ("Sayfalar", "Programlar · Destek Unsurları · Uygunluk Kuralları · Yatırım Türü Matrisi · Matris Gerekçeleri · İller · Bölgesel Kurallar · YKH Konuları · Kümülasyon · Parasal Eşikler 2026 · YEKDEM Fiyatları · Gümrük (EK-4) · Takvim ve Çağrılar · Kaynaklar · Teyit Listesi"),
    ("Uyarı", "Ön değerlendirme verisidir. Destek kararı ilgili kurumun incelemesiyle verilir; başvuru öncesinde güncel mevzuat ve ilanlar kontrol edilmelidir."),
]
r = 5
for a, b in rows:
    put(ws, r, 1, a, f_bold); put(ws, r, 2, b); r += 1
r += 1
put(ws, r, 1, "Etiket", f_head, fill=fill_head); put(ws, r, 2, "Anlamı", f_head, fill=fill_head); r += 1
for k, (lab, desc) in ETIKET.items():
    tag_cell(ws.cell(row=r, column=1), k); put(ws, r, 2, desc); r += 1
r += 1
put(ws, r, 1, "Öne çıkan bulgular", f_head, fill=fill_head); put(ws, r, 2, "", f_head, fill=fill_head); r += 1
bulgu = [
    ("KOSGEB KOBİ Enerji Verimliliği", "KOSGEB sitesinde 'Yürürlükten Kaldırılan Destekler' altında; güncel program listesinde yok."),
    ("İl farkının sınırı", "9903'te vergi indirimi ve faiz oranları programa bağlı; il değişince asgari tutar, SGK süresi, Hedef faizi (4-6. bölge), İstanbul istisnası ve geçici m.3-4 değişir."),
    ("Geçici m.3-4 (31.12.2026)", "Deprem ilçeleri ile Cazibe Merkezleri illerindeki OSB imalat yatırımları 6. bölge desteklerinden yararlanır; müracaat için son tarih 31.12.2026."),
    ("GES'te EK-3 şartı", "240 kW altı (çatı dahil) ve modernizasyon niteliğindeki GES yatırımları 9903'te desteklenmez; öz tüketimde teşvik sözleşme gücüyle sınırlı."),
    ("Li-ion batarya gümrüğü", "8507.60 lityum iyon aküler EK-4'te: teşvik belgesi olsa da gümrük muafiyeti yok. İnverter, trafo, PV modül ve ısı pompası listede değil."),
    ("Çimento ve temel çelik", "EK-3 dışı veya dar; bu sektörlerde enerji verimliliği için 9903'e yol Yeşil Dönüşüm Programı."),
    ("Ekosistem geliştirme planı", "KOBİ olmayan ve vergi indirimi alan yatırımcı, SYT'nin en az %2'si tutarında plan uygulamakla yükümlü (9903 m.5/9)."),
    ("LÜY m.37/10", "Dağıtım ve görevli tedarik şirketlerinin ortakları ve kontrolündeki şirketler, kendi dağıtım bölgelerinde lisanssız RES/GES başvurusu yapamaz; ESCO modelinde başvuru sahibi müşteri olmalı."),
    ("Lisanssız 10 yıl sonrası", "11415 sayılı CBK: ihtiyaç fazlası, aynı tip lisanslı tesisin YEKDEM fiyatının %90'ından alınır; PTF'yi aşamaz."),
    ("Kümülasyon", "Aynı ekipman için VAP, EPS, 9903 ve KOSGEB'den yalnız biri. VAP ile EKA tamamlayıcı."),
]
for a, b in bulgu:
    put(ws, r, 1, a, f_bold); put(ws, r, 2, b); r += 1
ws.freeze_panes = None

# ============================================================ 2. PROGRAMLAR
SINIF = {"P01": "Yatırım desteği", "P02": "Yatırım desteği", "P03": "Yatırım desteği", "P04": "Yatırım desteği",
         "P05": "Yatırım desteği", "P06": "Yatırım desteği", "P07": "Yatırım desteği", "P08": "Yatırım desteği",
         "P09": "Yatırım desteği", "P10": "Performans desteği", "P11": "Yatırım desteği", "P12": "Yatırım desteği",
         "P13": "Ar-Ge desteği", "P14": "Yatırım desteği", "P15": "Gelir / piyasa desteği", "P16": "Gelir / piyasa düzenlemesi",
         "P17": "Kapasite tahsisi", "P18": "Yatırım desteği"}
H = ["ID", "Program", "Kurum", "Destek sınıfı", "Niteliği", "2026 durumu", "Başvuru kanalı", "Başvuru dönemi", "Hedef yatırımcı", "Dayanak", "Etiket", "Kaynak", "Not", "Son kontrol"]
ws = sheet(wb, "Programlar", "Programlar", "Her program bir satır. Destek sınıfı sütunu, yatırım desteğini gelir/piyasa desteğinden ayırır.", H,
           [7, 38, 28, 20, 26, 22, 28, 22, 32, 26, 16, 12, 40, 12])
for i, p in enumerate(PROGRAM):
    r = 5 + i
    pid, ad, kurum, nit, durum, kanal, donem, hedef, dayanak, et, kay, notu = p
    vals = [pid, ad, kurum, SINIF[pid], nit, durum, kanal, donem, hedef, dayanak, None, kay, notu, KONTROL]
    for c, v in enumerate(vals, 1):
        put(ws, r, c, v, f_bold if c in (1, 2) else None)
    tag_cell(ws.cell(row=r, column=11), et)
last = 4 + len(PROGRAM)
ws.conditional_formatting.add(f"F5:F{last}", FormulaRule(formula=['ISNUMBER(SEARCH("kaldırıldı",F5))'], fill=PatternFill("solid", fgColor="FDF0EF"), font=Font(name=F, color="B42318", bold=True)))
ws.conditional_formatting.add(f"F5:F{last}", FormulaRule(formula=['ISNUMBER(SEARCH("kapanıyor",F5))'], fill=PatternFill("solid", fgColor="FFF5E8"), font=Font(name=F, color="B54708", bold=True)))
ws.conditional_formatting.add(f"F5:F{last}", FormulaRule(formula=['ISNUMBER(SEARCH("teyit",F5))'], fill=PatternFill("solid", fgColor="FFF3DC")))
finish(ws, len(H), last)
PROG_LAST = last

# ============================================================ 3. DESTEK UNSURLARI
H = ["Program ID", "Program", "Destek unsuru", "Oran / ölçü", "2026 üst sınır", "Süre", "Hesap", "Dayanak", "Etiket", "Kaynak"]
ws = sheet(wb, "Destek Unsurları", "Destek unsurları", "Program adı Programlar sayfasından formülle gelir.", H, [11, 32, 34, 44, 24, 22, 22, 26, 18, 12])
for i, d in enumerate(DESTEK):
    r = 5 + i
    pid, unsur, oran, lim, sure, hes, day, et, kay = d
    put(ws, r, 1, pid, f_bold)
    put(ws, r, 2, f"=IFERROR(INDEX(Programlar!$B$5:$B${PROG_LAST},MATCH(A{r},Programlar!$A$5:$A${PROG_LAST},0)),\"\")")
    for c, v in enumerate([unsur, oran, lim, sure, hes, day], 3):
        put(ws, r, c, v)
    tag_cell(ws.cell(row=r, column=9), et)
    put(ws, r, 10, kay)
finish(ws, len(H), 4 + len(DESTEK))

# ============================================================ 4. UYGUNLUK KURALLARI
H = ["Kural ID", "Program(lar)", "Alan", "Operatör", "Değer", "Birim", "Sonuç", "Açıklama", "Dayanak", "Etiket", "Kaynak"]
ws = sheet(wb, "Uygunluk Kuralları", "Makine tarafından kontrol edilebilir uygunluk kuralları",
           "Sonuç: Şart (sağlanmazsa uygun değil) · Engel (varsa uygun değil) · Uyarı · Bilgi. Alan adları karar motorundaki değişkenlere karşılık gelir.",
           H, [9, 12, 30, 9, 44, 9, 9, 44, 30, 18, 11])
for i, k in enumerate(KURAL):
    r = 5 + i
    prog, alan, op, deg, birim, son, acik, day, et, kay = k
    for c, v in enumerate([f"R{i+1:03d}", prog, alan, op, deg, birim, son, acik, day], 1):
        put(ws, r, c, v, f_bold if c == 1 else None, center if c in (4, 6, 7) else None)
    tag_cell(ws.cell(row=r, column=10), et)
    put(ws, r, 11, kay)
last = 4 + len(KURAL)
for val, bg, fg in [("Engel", "FDF0EF", "B42318"), ("Şart", "ECF7F0", "067647"), ("Uyarı", "FFF5E8", "B54708")]:
    ws.conditional_formatting.add(f"G5:G{last}", CellIsRule(operator="equal", formula=[f'"{val}"'], fill=PatternFill("solid", fgColor=bg), font=Font(name=F, bold=True, color=fg)))
finish(ws, len(H), last)

# ============================================================ 5. MATRİS GEREKÇELERİ (uzun tablo)
tur_ad = dict(TUR); prog_ad = dict(MPROG)
H = ["Anahtar", "Tür ID", "Yatırım türü", "Program ID", "Program", "Durum", "Gerekçe", "Dayanak", "Etiket"]
wsg = sheet(wb, "Matris Gerekçeleri", "Yatırım türü × program gerekçeleri",
            "Matris bu tablodan INDEX/MATCH ile beslenir. Durum: ✔ uygun · ◐ koşullu · ✖ kapsam dışı. Satır eklenirse matris kendiliğinden güncellenir.",
            H, [12, 8, 34, 10, 16, 8, 60, 30, 18])
for i, m in enumerate(M):
    r = 5 + i
    t, p, d, g, day, et = m
    put(wsg, r, 1, f'=B{r}&"|"&D{r}', Font(name=F, size=9, color="7A8699"))
    for c, v in enumerate([t, tur_ad[t], p, prog_ad[p], d, g, day], 2):
        put(wsg, r, c, v, None, center if c in (2, 4, 6) else None)
    tag_cell(wsg.cell(row=r, column=9), et)
G_LAST = 4 + len(M)
finish(wsg, len(H), G_LAST)

# ============================================================ 6. YATIRIM TÜRÜ MATRİSİ
ws = wb.create_sheet("Yatırım Türü Matrisi", index=4)
ws.sheet_view.showGridLines = False
ws["A1"] = "Yatırım türü × program matrisi"; ws["A1"].font = f_title
ws["A2"] = "✔ uygun · ◐ koşullu · ✖ kapsam dışı · — ilgisiz/değerlendirilmedi. Gerekçe ve madde için 'Matris Gerekçeleri' sayfasına bakın."; ws["A2"].font = f_sub
ws.column_dimensions["A"].width = 7; ws.column_dimensions["B"].width = 44
put(ws, 3, 1, "", f_head, fill=fill_head); put(ws, 3, 2, "Program ID →", f_head, fill=fill_head)
put(ws, 4, 1, "ID", f_head, fill=fill_head); put(ws, 4, 2, "Yatırım türü", f_head, fill=fill_head)
for j, (pid, pad) in enumerate(MPROG):
    col = 3 + j
    put(ws, 3, col, pid, Font(name=F, size=9, color="FFFFFF"), center, fill=fill_head)
    put(ws, 4, col, pad, f_head, Alignment(wrap_text=True, vertical="center", horizontal="center"), fill=fill_head)
    ws.column_dimensions[get_column_letter(col)].width = 11
ws.row_dimensions[4].height = 42
for i, (tid, tad) in enumerate(TUR):
    r = 5 + i
    put(ws, r, 1, tid, f_bold); put(ws, r, 2, tad, f_bold)
    for j in range(len(MPROG)):
        col = get_column_letter(3 + j)
        put(ws, r, 3 + j, f"=IFERROR(INDEX('Matris Gerekçeleri'!$F$5:$F${G_LAST},MATCH($A{r}&\"|\"&{col}$3,'Matris Gerekçeleri'!$A$5:$A${G_LAST},0)),\"—\")",
            Font(name=F, size=12, bold=True), Alignment(horizontal="center", vertical="center"))
last = 4 + len(TUR); lastc = get_column_letter(2 + len(MPROG))
rng = f"C5:{lastc}{last}"
for val, bg, fg in [("✔", "ECF7F0", "067647"), ("◐", "FFF5E8", "B54708"), ("✖", "FDF0EF", "B42318"), ("—", "F5F7FA", "98A2B3")]:
    ws.conditional_formatting.add(rng, CellIsRule(operator="equal", formula=[f'"{val}"'], fill=PatternFill("solid", fgColor=bg), font=Font(name=F, size=12, bold=True, color=fg)))
ws.freeze_panes = "C5"
r = last + 2
put(ws, r, 2, "Özet (formül)", f_head, fill=fill_head)
for j in range(len(MPROG)):
    put(ws, r, 3 + j, "", f_head, fill=fill_head)
for k, (lab, sym) in enumerate([("✔ uygun tür sayısı", "✔"), ("◐ koşullu tür sayısı", "◐"), ("✖ kapsam dışı tür sayısı", "✖")]):
    rr = r + 1 + k
    put(ws, rr, 2, lab, f_bold)
    for j in range(len(MPROG)):
        col = get_column_letter(3 + j)
        put(ws, rr, 3 + j, f'=COUNTIF({col}$5:{col}${last},"{sym}")', f_body, Alignment(horizontal="center"))

# ============================================================ 7. BÖLGESEL KURALLAR
H = ["Bölge", "İl sayısı", "Asgari sabit yatırım 2026 (TL)", "SGK işveren desteği süresi (yıl)", "SGK işveren desteği oranı", "Sigorta primi işçi hissesi", "Hedef yatırımda faiz", "Alt bölge etkisi (m.22)", "Not", "Dayanak"]
ws = sheet(wb, "Bölgesel Kurallar", "Bölgeye göre değişen kurallar (9903)",
           "İl sayısı İller sayfasından, asgari tutar Parasal Eşikler 2026 sayfasından formülle gelir.", H, [8, 9, 18, 16, 14, 18, 12, 40, 44, 26])
for i, b in enumerate(BOLGE):
    r = 5 + i
    bno, sure, oran, isci, faiz, notu = b
    put(ws, r, 1, bno, f_bold, center)
    put(ws, r, 2, f"=COUNTIF(İller!$C$5:$C$85,A{r})", None, center)
    put(ws, r, 3, f"=IF(A{r}<=2,'Parasal Eşikler 2026'!$G$7,'Parasal Eşikler 2026'!$G$8)", None, None, "#,##0")
    put(ws, r, 4, sure, None, center)
    put(ws, r, 5, oran, None, center)
    put(ws, r, 6, isci, None, center)
    put(ws, r, 7, faiz, None, center)
    put(ws, r, 8, "OSB/endüstri bölgesi veya EK-5 ilçesi: bir alt bölgenin SGK süresi; ikisi birden: iki alt bölge. 6. bölgede +2 yıl." if bno < 6 else "OSB/EK-5: bölgedeki süreye +2 yıl.")
    put(ws, r, 9, notu)
    put(ws, r, 10, "9903 m.18, m.19, m.22, m.10/3")
finish(ws, len(H), 10)
r = 12
put(ws, r, 1, "TYKH", f_bold); put(ws, r, 2, ""); put(ws, r, 3, ""); put(ws, r, 4, "8 (6. bölge 12)", None, center)
for c in range(5, 11): put(ws, r, c, "")
ws.cell(row=r, column=9, value="THP, YKH ve Stratejik Hamle'de SGK desteği bölgeden bağımsız 8 yıl (m.18/3).")

# ============================================================ 8. İLLER
H = ["Plaka", "İl", "Bölge (EK-2)", "Asgari sabit yatırım 2026 (TL)", "SGK işveren süresi (yıl)", "Hedef yatırımda faiz", "İstanbul istisnası", "Cazibe EK-1 ili (geçici m.4, OSB imalat → 6. bölge, 31.12.2026)",
     "Deprem ilçeleri (geçici m.3 → 6. bölge, 31.12.2026)", "EK-5 alt bölge ilçeleri (SGK)", "Yerel yatırım konuları (YKH 2026)", "Enerji bağlantılı yerel konu", "Kalkınma ajansı", "Ajans ofisi / YDO", "Telefon", "E-posta", "Web",
     "Enerjisa dağıtım bölgesi (LÜY m.37/10)", "Etiketler"]
ws = sheet(wb, "İller", "İl katmanı · 81 il",
           "Bölge: 9903 EK-2 (RG 30.05.2025). Asgari tutar, SGK süresi ve Hedef faizi formülle gelir. Ajans verisi ka.gov.tr; yerel konular RG 31.01.2026 EK-1.",
           H, [6, 14, 8, 15, 10, 10, 26, 16, 34, 34, 60, 30, 26, 26, 16, 26, 22, 18, 30])
iller = sorted(PLAKA.items(), key=lambda x: x[1])
bolge_of = {il: b for b, lst in EK2.items() for il in lst}
for i, (il, pl) in enumerate(iller):
    r = 5 + i
    put(ws, r, 1, pl, None, center, "00")
    put(ws, r, 2, il, f_bold)
    put(ws, r, 3, bolge_of[il], f_bold, center)
    put(ws, r, 4, f"=IF(C{r}<=2,'Parasal Eşikler 2026'!$G$7,'Parasal Eşikler 2026'!$G$8)", None, None, "#,##0")
    put(ws, r, 5, f"=IFERROR(INDEX('Bölgesel Kurallar'!$D$5:$D$10,MATCH(C{r},'Bölgesel Kurallar'!$A$5:$A$10,0)),\"\")", None, center)
    put(ws, r, 6, f"=IFERROR(INDEX('Bölgesel Kurallar'!$G$5:$G$10,MATCH(C{r},'Bölgesel Kurallar'!$A$5:$A$10,0)),\"\")", None, center)
    put(ws, r, 7, f'=IF(B{r}="İstanbul","Hedef\'te vergi indirimi yok; Öncelikli (c) ve (j) İstanbul hariç; madencilik desteklenmez","—")')
    put(ws, r, 8, "Evet" if il in CAZIBE_EK1 else "—", None, center)
    put(ws, r, 9, ", ".join(DEPREM_EK2.get(il, [])) or "—")
    put(ws, r, 10, ", ".join(EK5.get(il, [])) or "—")
    konular = YKH[il]
    put(ws, r, 11, " · ".join(f"{k+1}) {t}" for k, t in enumerate(konular)))
    en = [t for t in konular if any(key.lower() in t.lower() for key in YKH_ENERJI)]
    put(ws, r, 12, " · ".join(en) or "—")
    aj = AJANS.get(il, [{}])[0]
    put(ws, r, 13, aj.get("ajans", ""))
    put(ws, r, 14, aj.get("ofis", ""))
    put(ws, r, 15, aj.get("tel", "") or "—")
    put(ws, r, 16, aj.get("eposta", "") or "—")
    w = put(ws, r, 17, aj.get("web", ""), f_link)
    if aj.get("web"): w.hyperlink = aj["web"]
    put(ws, r, 18, ENERJISA_DAGITIM.get(il, "—"), f_bold if il in ENERJISA_DAGITIM else None)
    put(ws, r, 19, "Bölge, EK-5, Cazibe, deprem: Mevzuat · YKH: Mevzuat · Ajans: Duyuru · Enerjisa sütunu: Teyit edilecek · Enerji bağlantısı: Yorum", Font(name=F, size=8, color="7A8699"))
IL_LAST = 4 + len(iller)
ws.conditional_formatting.add(f"C5:C{IL_LAST}", CellIsRule(operator="equal", formula=["6"], fill=PatternFill("solid", fgColor="ECF7F0")))
ws.conditional_formatting.add(f"H5:H{IL_LAST}", CellIsRule(operator="equal", formula=['"Evet"'], fill=PatternFill("solid", fgColor="FFF5E8"), font=Font(name=F, bold=True, color="B54708")))
ws.conditional_formatting.add(f"R5:R{IL_LAST}", FormulaRule(formula=[f'R5<>"—"'], fill=PatternFill("solid", fgColor="FDF0EF")))
ws.freeze_panes = "C5"
finish(ws, len(H), IL_LAST)

# ============================================================ 9. YKH KONULARI (uzun)
H = ["İl", "Bölge", "Sıra", "Yerel yatırım konusu", "Enerji bağlantılı?", "Kalkınma ajansı"]
ws = sheet(wb, "YKH Konuları", "Yerel Kalkınma Hamlesi · 81 il × 4 konu (324)",
           "Yerel Yatırım Konuları Listesi Tebliği EK-1 (RG 31.01.2026/33154). Başlıklar kısaltıldı; tam metin RG'dedir. Bölge ve ajans İller sayfasından formülle gelir.",
           H, [16, 8, 6, 70, 14, 28])
r = 5
for il, _ in iller:
    for k, t in enumerate(YKH[il]):
        put(ws, r, 1, il, f_bold)
        put(ws, r, 2, f"=IFERROR(INDEX(İller!$C$5:$C${IL_LAST},MATCH(A{r},İller!$B$5:$B${IL_LAST},0)),\"\")", None, center)
        put(ws, r, 3, k + 1, None, center)
        put(ws, r, 4, t)
        put(ws, r, 5, "Evet" if any(key.lower() in t.lower() for key in YKH_ENERJI) else "—", None, center)
        put(ws, r, 6, f"=IFERROR(INDEX(İller!$M$5:$M${IL_LAST},MATCH(A{r},İller!$B$5:$B${IL_LAST},0)),\"\")")
        r += 1
ws.conditional_formatting.add(f"E5:E{r-1}", CellIsRule(operator="equal", formula=['"Evet"'], fill=PatternFill("solid", fgColor="E5F3F0"), font=Font(name=F, bold=True, color="0B7A6E")))
finish(ws, len(H), r - 1)

# ============================================================ 10. KÜMÜLASYON
H = ["Destek A", "Destek B", "Birlikte kullanılabilir mi?", "Açıklama", "Dayanak", "Etiket"]
ws = sheet(wb, "Kümülasyon", "Hangi destekler birlikte kullanılabilir?",
           "Aynı yatırım veya ekipman için. 'Belirsiz' satırları Teyit Listesi'ndedir.", H, [26, 26, 14, 64, 34, 18])
for i, k in enumerate(KUM):
    r = 5 + i
    a, b, bir, acik, day, et = k
    put(ws, r, 1, a, f_bold); put(ws, r, 2, b, f_bold); put(ws, r, 3, bir, f_bold, center); put(ws, r, 4, acik); put(ws, r, 5, day)
    tag_cell(ws.cell(row=r, column=6), et)
last = 4 + len(KUM)
for val, bg, fg in [("Hayır", "FDF0EF", "B42318"), ("Evet", "ECF7F0", "067647"), ("Koşullu", "FFF5E8", "B54708"), ("Belirsiz", "EEF1F4", "475467")]:
    ws.conditional_formatting.add(f"C5:C{last}", CellIsRule(operator="equal", formula=[f'"{val}"'], fill=PatternFill("solid", fgColor=bg), font=Font(name=F, bold=True, color=fg)))
finish(ws, len(H), last)

# ============================================================ 11. PARASAL EŞİKLER
ws = sheet(wb, "Parasal Eşikler 2026", "Parasal eşikler 2026",
           "Hesaplanan = baz × (1 + yeniden değerleme oranı). Kullanılacak değer: ilan edilen varsa o, yoksa hesaplanan.",
           ["Kalem", "Dayanak", "Baz tutar (TL)", "2026 ilan edilen (TL)", "Hesaplanan 2026 (TL)", "İlan / hesap farkı", "Kullanılacak 2026 değeri (TL)", "Etiket", "Kaynak", "Not"],
           [44, 22, 16, 18, 18, 12, 20, 22, 10, 40])
ws["D3"] = "2025 yeniden değerleme oranı →"; ws["D3"].font = f_bold; ws["D3"].alignment = Alignment(horizontal="right")
ws["E3"] = 0.2549; ws["E3"].font = f_input; ws["E3"].fill = fill_input; ws["E3"].number_format = "0.00%"; ws["E3"].border = border
ws["F3"] = "VUK mük. 298; VAP ve EKA 2025→2026 tutarlarıyla birebir doğrulandı (K32)."; ws["F3"].font = f_sub
# İlk iki satır asgari yatırım olmalı (G7, G8'e başka sayfalardan atıf var)
start = 7
put(ws, 5, 1, "Satır 7 ve 8'deki değerler İller ve Bölgesel Kurallar sayfalarında kullanılır.", f_sub)
for i, e in enumerate(ESIK):
    r = start + i
    kalem, day, baz, ilan, hes, et, kay, notu = e
    put(ws, r, 1, kalem, f_bold); put(ws, r, 2, day)
    put(ws, r, 3, baz, None, None, "#,##0")
    put(ws, r, 4, ilan, None, None, "#,##0")
    put(ws, r, 5, f"=IF(C{r}=\"\",\"\",ROUND(C{r}*(1+$E$3),0))" if hes else "", None, None, "#,##0")
    put(ws, r, 6, f"=IF(AND(ISNUMBER(D{r}),ISNUMBER(E{r})),D{r}/E{r}-1,\"\")", None, center, "+0.0%;-0.0%;0.0%")
    put(ws, r, 7, f"=IF(ISNUMBER(D{r}),D{r},E{r})", f_bold, None, "#,##0")
    tag_cell(ws.cell(row=r, column=8), et)
    put(ws, r, 9, kay); put(ws, r, 10, notu)
ESIK_LAST = start + len(ESIK) - 1
ws.auto_filter.ref = None
ws.freeze_panes = "A5"

# ============================================================ 12. YEKDEM
H = ["Kaynak tipi", "Uygulama fiyatı (TL kuruş/kWh)", "Uygulama fiyatı (TL/kWh)", "Süre (yıl)", "Taban (USD cent/kWh)", "Tavan (USD cent/kWh)", "Yerli katkı (TL kuruş/kWh)", "Yerli katkı süresi (yıl)", "10 yılı dolan lisanssız: %90 fiyat (kuruş, baz)", "Not"]
ws = sheet(wb, "YEKDEM Fiyatları", "YEKDEM · 7189 sayılı CBK EK-1 (baz fiyatlar)",
           "RG 01.05.2023/32177. 01.07.2021-31.12.2030 arasında işletmeye giren YEK belgeli tesisler. Fiyatlar aylık güncellenir; bu tablo baz değerdir.", H,
           [44, 14, 12, 8, 12, 12, 13, 12, 18, 44])
for i, y in enumerate(YEKDEM):
    r = 5 + i
    ad, fiy, sure, tb, tv, yk, yks, notu = y
    put(ws, r, 1, ad, f_bold)
    put(ws, r, 2, fiy, None, center, "0.00")
    put(ws, r, 3, f"=B{r}/100", None, center, "0.0000")
    put(ws, r, 4, sure, None, center)
    put(ws, r, 5, tb, None, center, "0.00"); put(ws, r, 6, tv, None, center, "0.00")
    put(ws, r, 7, yk, None, center, "0.00"); put(ws, r, 8, yks, None, center)
    put(ws, r, 9, f"=ROUND(B{r}*0.9,2)", None, center, "0.00")
    put(ws, r, 10, notu)
r = 6 + len(YEKDEM)
put(ws, r, 1, "Güncelleme formülü", f_bold); ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=10); put(ws, r, 2, YEKDEM_NOT)
put(ws, r + 1, 1, "10 yıl sonrası (lisanssız)", f_bold); ws.merge_cells(start_row=r + 1, start_column=2, end_row=r + 1, end_column=10)
put(ws, r + 1, 2, "11415 sayılı CBK (RG 13.06.2026): 10 yılı dolan lisanssız YEK tesisinde ihtiyaç fazlası, aynı tip lisanslı tesisin güncel YEKDEM fiyatının %90'ından görevli tedarik şirketince alınır; saatlik PTF'yi aşamaz. I sütunu baz fiyat üzerinden örnektir; güncel aylık fiyatla hesaplanmalıdır.")
put(ws, r + 2, 1, "Etiket", f_bold); tag_cell(ws.cell(row=r + 2, column=2), "MEV"); put(ws, r + 2, 3, "Kaynak: K19, K20")
finish(ws, len(H), 4 + len(YEKDEM))

# ============================================================ 13. GÜMRÜK (EK-4)
H = ["GTİP", "Tanım", "Gümrük muafiyeti", "Enerji bağlantısı", "Dayanak"]
ws = sheet(wb, "Gümrük (EK-4)", "9903 EK-4 · gümrük muafiyetinden yararlanamayan makineler (enerji ile ilgili olanlar)",
           "EK-4 toplam 233 kalem; burada enerji yatırımlarını ilgilendirenler ve listede olmadığı doğrulanan başlıca kalemler var. EK-4 makineleri muafiyetsiz ithal edilip SYT'ye dahil edilebilir (m.13/2).",
           H, [36, 52, 24, 34, 22])
for i, e in enumerate(EK4):
    r = 5 + i
    for c, v in enumerate(e, 1):
        put(ws, r, c, v, f_bold if c == 1 else None)
last = 4 + len(EK4)
ws.conditional_formatting.add(f"C5:C{last}", CellIsRule(operator="equal", formula=['"Muafiyet yok"'], fill=PatternFill("solid", fgColor="FDF0EF"), font=Font(name=F, bold=True, color="B42318")))
ws.conditional_formatting.add(f"C5:C{last}", FormulaRule(formula=['ISNUMBER(SEARCH("uygulanabilir",C5))'], fill=PatternFill("solid", fgColor="ECF7F0"), font=Font(name=F, bold=True, color="067647")))
finish(ws, len(H), last)

# ============================================================ 14. TAKVİM
H = ["Başlangıç", "Bitiş", "Olay", "Program", "Durum (bugüne göre)", "Etiket", "Kaynak"]
ws = sheet(wb, "Takvim ve Çağrılar", "Takvim ve açık çağrılar",
           "Durum sütunu TODAY() ile her açılışta yeniden hesaplanır.", H, [12, 12, 62, 30, 26, 18, 12])
for i, t in enumerate(TAKVIM):
    r = 5 + i
    bas, bit, olay, pid, et, kay = t
    put(ws, r, 1, date.fromisoformat(bas), None, center, "DD.MM.YYYY")
    put(ws, r, 2, date.fromisoformat(bit), None, center, "DD.MM.YYYY")
    put(ws, r, 3, olay, f_bold)
    put(ws, r, 4, f"=IFERROR(INDEX(Programlar!$B$5:$B${PROG_LAST},MATCH(\"{pid}\",Programlar!$A$5:$A${PROG_LAST},0)),\"{pid}\")")
    put(ws, r, 5, f'=IF(B{r}<TODAY(),"Geçti",IF(A{r}>TODAY(),IF(A{r}-TODAY()<=30,"Yaklaşıyor · "&(A{r}-TODAY())&" gün","İleri tarih"),"Açık · "&(B{r}-TODAY())&" gün kaldı"))', f_bold, center)
    tag_cell(ws.cell(row=r, column=6), et)
    put(ws, r, 7, kay)
last = 4 + len(TAKVIM)
ws.conditional_formatting.add(f"E5:E{last}", FormulaRule(formula=['LEFT(E5,4)="Açık"'], fill=PatternFill("solid", fgColor="ECF7F0"), font=Font(name=F, bold=True, color="067647")))
ws.conditional_formatting.add(f"E5:E{last}", FormulaRule(formula=['LEFT(E5,10)="Yaklaşıyor"'], fill=PatternFill("solid", fgColor="FFF5E8"), font=Font(name=F, bold=True, color="B54708")))
ws.conditional_formatting.add(f"E5:E{last}", CellIsRule(operator="equal", formula=['"Geçti"'], font=Font(name=F, color="98A2B3")))
finish(ws, len(H), last)

# ============================================================ 15. KAYNAKLAR
H = ["ID", "Kaynak", "Tür", "Tarih / sayı", "Bağlantı", "Not", "Erişim"]
ws = sheet(wb, "Kaynaklar", "Kaynaklar", "Diğer sayfalardaki 'Kaynak' sütunu bu kimliklere atıf yapar.", H, [6, 52, 20, 30, 50, 52, 11])
for i, k in enumerate(KAYNAK):
    r = 5 + i
    kid, ad, tur, tarih, url, notu = k
    put(ws, r, 1, kid, f_bold); put(ws, r, 2, ad); put(ws, r, 3, tur); put(ws, r, 4, tarih)
    c = put(ws, r, 5, url, f_link if url else None)
    if url: c.hyperlink = url
    put(ws, r, 6, notu); put(ws, r, 7, KONTROL, None, center)
    if tur.startswith("İkincil"):
        for cc in range(1, 8): ws.cell(row=r, column=cc).fill = PatternFill("solid", fgColor="FFF8E6")
finish(ws, len(H), 4 + len(KAYNAK))

# ============================================================ 16. TEYİT LİSTESİ
H = ["ID", "Konu", "Neden", "Nasıl teyit edilir", "İlgili sayfa", "Durum"]
ws = sheet(wb, "Teyit Listesi", "Teyit bekleyen bilgiler", "Durum sütunu kullanıcı içindir (açılır liste).", H, [7, 40, 54, 40, 22, 14])
dv = DataValidation(type="list", formula1='"Açık,Teyit edildi,Düzeltildi"', allow_blank=True)
ws.add_data_validation(dv)
for i, t in enumerate(TEYIT):
    r = 5 + i
    for c, v in enumerate(t, 1):
        put(ws, r, c, v, f_bold if c == 1 else None)
    c = put(ws, r, 6, "Açık", f_input, center, fill=fill_input); dv.add(c)
finish(ws, len(H), 4 + len(TEYIT))

# ---- yazdırma ve genel ayarlar
for s in wb.worksheets:
    s.page_setup.orientation = "landscape"
    s.page_setup.fitToWidth = 1
    s.sheet_properties.pageSetUpPr.fitToPage = True
    s.page_setup.fitToHeight = 0

wb.save(OUT)
print(OUT)
