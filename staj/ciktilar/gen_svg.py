# -*- coding: utf-8 -*-
"""TR ETS kapsam belirleme karar ağacı — SVG üreteci."""
from html import escape

W, H = 1900, 3060

INK      = "#16232B"
MUTED    = "#5C6A66"
FAINT    = "#8B948F"
LINE     = "#C9CFC6"
GROUND   = "#FBFBF8"
PANEL    = "#F1F3ED"
PANEL_ST = "#CDD3C8"
NEUTRAL  = "#E9ECE5"
NEUT_ST  = "#A9B2A6"
ACCENT   = "#0C5F5A"

GREEN_F, GREEN_S, GREEN_T = "#DCEBDD", "#2E6B3C", "#1C4426"
AMBER_F, AMBER_S, AMBER_T = "#F8EBD3", "#9A6208", "#5A3A05"
RED_F,   RED_S,   RED_T   = "#F6E2DF", "#8F2B25", "#591A16"
EVENT_F, EVENT_S          = "#E7EAEF", "#8892A1"

FONT = "Archivo, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"
MONO = "'IBM Plex Mono', 'SFMono-Regular', Consolas, monospace"

out = []
def add(s): out.append(s)

def e(t): return escape(str(t), quote=True)

def tru(t):
    """Türkçe büyük harf: i -> İ."""
    return t.replace("i", "İ").upper()

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

def text_block(cx, top, lines, size, weight, color, lh=None, anchor="middle", x=None):
    lh = lh or size * 1.28
    xx = cx if x is None else x
    parts = []
    for i, ln in enumerate(lines):
        parts.append(f'<tspan x="{xx}" dy="{0 if i==0 else lh}">{e(ln)}</tspan>')
    add(f'<text x="{xx}" y="{top + size*0.80}" text-anchor="{anchor}" '
        f'font-family="{FONT}" font-size="{size}" font-weight="{weight}" '
        f'fill="{color}">{"".join(parts)}</text>')

def node(cx, cy, w, h, title, sub=None, fill=NEUTRAL, stroke=NEUT_ST,
         tcol=INK, scol=None, r=8, sw=1.6, title_size=15, sub_size=11.5, dash=None):
    x, y = cx - w/2, cy - h/2
    d = f' stroke-dasharray="{dash}"' if dash else ""
    add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')
    tl = wrap(title, int((w - 30) / (title_size * 0.50)))
    sl = wrap(sub, int((w - 30) / (sub_size * 0.50))) if sub else []
    th = len(tl) * title_size * 1.22
    sh = len(sl) * sub_size * 1.26
    gap = 6 if sl else 0
    top = cy - (th + gap + sh) / 2
    text_block(cx, top, tl, title_size, 600, tcol, title_size*1.22)
    if sl:
        text_block(cx, top + th + gap, sl, sub_size, 400, scol or MUTED, sub_size*1.26)

def diamond(cx, cy, w, h, title, ref=None):
    pts = f"{cx},{cy-h/2} {cx+w/2},{cy} {cx},{cy+h/2} {cx-w/2},{cy}"
    add(f'<polygon points="{pts}" fill="{NEUTRAL}" stroke="{NEUT_ST}" stroke-width="1.8"/>')
    tl = wrap(title, 46)
    th = len(tl) * 15 * 1.22
    text_block(cx, cy - th/2, tl, 15, 600, INK, 15*1.22)
    if ref:
        add(f'<text x="{cx}" y="{cy + h/2 + 20}" text-anchor="middle" font-family="{MONO}" '
            f'font-size="11" fill="{FAINT}">{e(ref)}</text>')

def panel(x, y, w, h, heading, body_lines, fill=PANEL, stroke=PANEL_ST, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" '
        f'stroke="{stroke}" stroke-width="1.4"{d}/>')
    add(f'<text x="{x+18}" y="{y+30}" font-family="{FONT}" font-size="12.5" font-weight="700" '
        f'letter-spacing="1.2" fill="{ACCENT}">{e(tru(heading))}</text>')
    yy = y + 54
    for kind, txt in body_lines:
        if kind == "h":
            add(f'<text x="{x+18}" y="{yy}" font-family="{FONT}" font-size="11" font-weight="700" '
                f'letter-spacing="1.1" fill="{MUTED}">{e(tru(txt))}</text>')
            yy += 19
        elif kind == "b":
            for i, ln in enumerate(wrap(txt, int((w-46)/6.05))):
                pre = "•  " if i == 0 else "    "
                add(f'<text x="{x+18}" y="{yy}" font-family="{FONT}" font-size="12" '
                    f'fill="{INK}">{e(pre + ln)}</text>')
                yy += 16
            yy += 3
        elif kind == "p":
            for ln in wrap(txt, int((w-40)/6.05)):
                add(f'<text x="{x+18}" y="{yy}" font-family="{FONT}" font-size="12" '
                    f'fill="{INK}">{e(ln)}</text>')
                yy += 16
            yy += 6
        elif kind == "n":
            for ln in wrap(txt, int((w-40)/6.30)):
                add(f'<text x="{x+18}" y="{yy}" font-family="{FONT}" font-size="11.5" '
                    f'fill="{MUTED}">{e(ln)}</text>')
                yy += 15
            yy += 5
        elif kind == "s":
            yy += 8

def conn(pts, label=None, lx=None, ly=None, dash=None, color="#6E7B76", anchor="middle"):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    path = " ".join(f"{x},{y}" for x, y in pts)
    add(f'<polyline points="{path}" fill="none" stroke="{color}" stroke-width="1.8" '
        f'stroke-linejoin="round" marker-end="url(#ar)"{d}/>')
    if label:
        add(f'<text x="{lx}" y="{ly}" text-anchor="{anchor}" font-family="{FONT}" font-size="11.5" '
            f'font-weight="600" fill="{MUTED}">{e(label)}</text>')

def plain(pts, dash=None, color="#A6B0AA"):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    path = " ".join(f"{x},{y}" for x, y in pts)
    add(f'<polyline points="{path}" fill="none" stroke="{color}" stroke-width="1.4" '
        f'stroke-linejoin="round"{d}/>')

def badge(x, y, label, fill=RED_S):
    w = 11 + len(label) * 6.6
    add(f'<rect x="{x}" y="{y}" width="{w}" height="21" rx="10.5" fill="{fill}"/>')
    add(f'<text x="{x + w/2}" y="{y+14.5}" text-anchor="middle" font-family="{FONT}" '
        f'font-size="10.5" font-weight="700" letter-spacing="0.6" fill="#FFFFFF">{e(label)}</text>')

# ───────────────────────── canvas ─────────────────────────
add(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
    f'role="img" aria-label="Türkiye Emisyon Ticaret Sistemi kapsam belirleme karar ağacı ve '
    f'yükümlülük akışı">')
add('<defs><marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
    f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#6E7B76"/></marker></defs>')
add(f'<rect width="{W}" height="{H}" fill="{GROUND}"/>')

# ───────────────────────── header ─────────────────────────
add(f'<text x="48" y="74" font-family="{FONT}" font-size="12.5" font-weight="700" '
    f'letter-spacing="2" fill="{ACCENT}">TÜRKİYE EMİSYON TİCARET SİSTEMİ · TESİS DEĞERLENDİRMESİ</text>')
add(f'<text x="48" y="120" font-family="{FONT}" font-size="36" font-weight="700" '
    f'letter-spacing="-0.7" fill="{INK}">İşletmem ETS kapsamına giriyor mu?</text>')
add(f'<text x="48" y="150" font-family="{FONT}" font-size="15" fill="{MUTED}">'
    f'Dört soruyu tesis bazında yanıtlayın; kapsam durumunuz, tesis kategoriniz ve '
    f'takvimli yükümlülük listeniz aşağıda.</text>')
add(f'<text x="48" y="176" font-family="{MONO}" font-size="11.5" fill="{FAINT}">'
    f'Dayanak: Türkiye Emisyon Ticaret Sistemi Yönetmeliği — Resmî Gazete 27.08.2026 / 33353</text>')

# legend
lx, ly = 1400, 46
add(f'<rect x="{lx}" y="{ly}" width="452" height="122" rx="8" fill="#FFFFFF" '
    f'stroke="{LINE}" stroke-width="1.4"/>')
add(f'<text x="{lx+18}" y="{ly+26}" font-family="{FONT}" font-size="11" font-weight="700" '
    f'letter-spacing="1.2" fill="{MUTED}">RENK ANAHTARI</text>')
for i, (f_, s_, t_) in enumerate([
        (GREEN_F, GREEN_S, "Yükümlülük yok — sistem hiç uygulanmaz"),
        (AMBER_F, AMBER_S, "Yalnızca izleme, raporlama ve doğrulama"),
        (RED_F,   RED_S,   "Tam ETS — izin, İRD ve tahsisat teslimi")]):
    yy = ly + 48 + i * 25
    add(f'<rect x="{lx+18}" y="{yy-11}" width="26" height="15" rx="4" fill="{f_}" '
        f'stroke="{s_}" stroke-width="1.5"/>')
    add(f'<text x="{lx+54}" y="{yy+1}" font-family="{FONT}" font-size="12.5" '
        f'fill="{INK}">{e(t_)}</text>')

add(f'<line x1="48" y1="206" x2="{W-48}" y2="206" stroke="{INK}" stroke-width="2"/>')

# ─────────────────── band 1 heading ───────────────────
add(f'<text x="48" y="248" font-family="{FONT}" font-size="13" font-weight="700" '
    f'letter-spacing="1.8" fill="{ACCENT}">BÖLÜM 1 — KAPSAM VE KATEGORİ BELİRLEME</text>')
add(f'<text x="452" y="248" font-family="{FONT}" font-size="11.5" fill="{FAINT}">'
    f'Soldaki sütun yardımcı bilgidir; akışın parçası değildir.</text>')

# ─────────────────── left information column ───────────────────
PX, PW = 48, 344

panel(PX, 276, PW, 626, "EK-1 faaliyetleri (özet)", [
    ("h", "Enerji"),
    ("b", "Yakıtların yakılması — tesisteki TÜM yakma ünitelerinin toplam anma ısıl gücü ≥ 20 MW"),
    ("b", "Petrol rafinasyonu — ≥ 20 MW"),
    ("b", "Kok üretimi — eşik yok"),
    ("h", "Metal"),
    ("b", "Cevher kavurma, sinterleme, peletleme"),
    ("b", "Demir-çelik üretimi ve dökümü — > 2,5 ton/saat"),
    ("b", "Demirli metal işleme — ≥ 20 MW"),
    ("b", "Birincil alüminyum ve alümina"),
    ("b", "İkincil alüminyum, demir dışı metaller — ≥ 20 MW"),
    ("h", "Mineral"),
    ("b", "Klinker — ≥ 500 t/gün (döner fırın)"),
    ("b", "Kireç, dolomit, magnezit — ≥ 50 t/gün"),
    ("b", "Cam — ≥ 20 t/gün · Seramik — ≥ 75 t/gün"),
    ("b", "Mineral elyaf yalıtım — ≥ 20 t/gün"),
    ("b", "Alçı taşı ürünleri — ≥ 20 MW"),
    ("h", "Selüloz ve kâğıt"),
    ("b", "Selüloz üretimi — eşik yok"),
    ("b", "Kâğıt, mukavva, karton — ≥ 20 t/gün"),
    ("h", "Kimya"),
    ("b", "Karbon siyahı — ≥ 20 MW"),
    ("b", "Nitrik asit, adipik asit, glioksal, amonyak"),
    ("b", "Organik kimyasallar — ≥ 100 t/gün"),
    ("b", "Hidrojen ve sentez gazı — ≥ 5 t/gün"),
    ("b", "Soda külü ve sodyum bikarbonat"),
    ("s", ""),
    ("n", "Tam liste 25 faaliyettir. Ayrıntı için EK-1'e bakınız."),
])

panel(PX, 928, PW, 268, "Toplam anma ısıl gücü nasıl hesaplanır?", [
    ("p", "Tesisteki tüm yakma ünitelerinin anma ısıl güçleri TOPLANIR: kazan, brülör, türbin, "
          "ısıtıcı, ocak, insineratör, kalsinatör, döner fırın, fırın, kurutucu, motor, yakıt "
          "hücresi, yakma bacası, termal veya katalitik yakma sonrası ünitesi."),
    ("n", "3 MW altındaki üniteler ve münhasıran biyokütle kullananlar bu toplama GİRMEZ."),
    ("n", "Toplam 20 MW ve üzeriyse tesis EK-1 kapsamındadır."),
])

panel(PX, 1222, PW, 250, "En çok kaçırılan üç kural", [
    ("b", "Aynı kategorideki faaliyetlerin kapasiteleri toplanarak eşiğe bakılır."),
    ("b", "Eşik kurulu kapasiteye bakar, fiilî üretime değil. Düşük kapasite kullanımı kapsam dışı bırakmaz."),
    ("b", "EK-1'deki bir faaliyeti yürüten işletmenin aynı tesisteki diğer EK-1 faaliyetleri, "
          "kapasite gözetilmeksizin kapsama dâhil olur (m. 27/2)."),
])

panel(PX, 1498, PW, 214, "İstisnaların süresi", [
    ("b", "Kategori A — kalıcı olarak ETS dışı, İRD sürer"),
    ("b", "Okul, üniversite, hastane, savunma sanayi — kalıcı istisna (m. 5/2-3)"),
    ("b", "Gaz ve ham petrol iletimi-depolaması — yalnızca birinci uygulama dönemi sonuna "
          "kadar (Geçici m. 6)"),
])

# ─────────────────── decision chain ───────────────────
CX = 940
node(CX, 300, 300, 56, "Tesis değerlendirmesini başlat", fill="#FFFFFF", stroke=NEUT_ST, r=28)

diamond(CX, 432, 430, 128, "Tesiste EK-1 listesindeki bir faaliyet yürütülüyor mu?", "m. 27/2 · EK-1")
diamond(CX, 640, 430, 128, "Ar-Ge tesisi, münhasıran biyokütle kullanan tesis veya askerî unsur mu?", "m. 2/2")
diamond(CX, 856, 470, 132, "Okul, üniversite, hastane, savunma sanayi veya gaz / ham petrol iletim-depolama tesisi mi?", "m. 5/2-3 · Geçici m. 6")
diamond(CX, 1072, 430, 128, "Kurulu kapasiteye göre ihtiyatlı hesaplanan yıllık emisyon kaç ton CO₂e?", "m. 4 · m. 5/1")

conn([(CX, 328), (CX, 366)])
conn([(CX, 496), (CX, 574)], "HAYIR", CX - 26, 540, anchor="end")
conn([(CX, 704), (CX, 788)], "HAYIR", CX - 26, 750, anchor="end")
conn([(CX, 922), (CX, 1006)], "HAYIR", CX - 26, 968, anchor="end")

# outcomes right
OX = 1520
node(OX, 432, 420, 82, "KAPSAM DIŞI", "Hiçbir yükümlülük doğmaz. Tahsisat, izin, izleme ve raporlama yok.",
     fill=GREEN_F, stroke=GREEN_S, tcol=GREEN_T, scol=GREEN_T, r=20, title_size=16)
node(OX, 640, 420, 82, "YÖNETMELİK DIŞI", "İstisna yalnızca ilgili tesis veya tesis bölümü için geçerlidir.",
     fill=GREEN_F, stroke=GREEN_S, tcol=GREEN_T, scol=GREEN_T, r=20, title_size=16)

conn([(CX + 215, 432), (OX - 210, 432)], "EVET", (CX + 215 + OX - 210) / 2, 422)
conn([(CX + 215, 640), (OX - 210, 640)], "EVET", (CX + 215 + OX - 210) / 2, 630)


# ─────────────────── band 2 ───────────────────
add(f'<line x1="48" y1="1300" x2="{W-48}" y2="1300" stroke="{LINE}" stroke-width="1.4"/>')
add(f'<text x="452" y="1344" font-family="{FONT}" font-size="13" font-weight="700" '
    f'letter-spacing="1.8" fill="{ACCENT}">BÖLÜM 2 — PROFİLİNİZE GÖRE YÜKÜMLÜLÜKLER</text>')

IRD_X, ETS_X = 660, 1310
RES_Y = 1420

node(IRD_X, RES_Y, 440, 104, "ETS DIŞI — İRD YÜKÜMLÜSÜ",
     "Tahsisat almaz, teslim etmezsiniz. Kategoriniz yine de belirlenir: ceza kademesi ve "
     "personel şartı kategoriye bağlıdır.",
     fill=AMBER_F, stroke=AMBER_S, tcol=AMBER_T, scol=AMBER_T, r=20, title_size=16)
node(ETS_X, RES_Y, 440, 104, "ETS KAPSAMINDA",
     "İzin + izleme, raporlama, doğrulama + her yıl emisyona denk tahsisat teslimi.",
     fill=RED_F, stroke=RED_S, tcol=RED_T, scol=RED_T, r=20, title_size=16)

# K3 EVET  →  İRD  (kategori sorusuna uğramaz)
conn([(CX - 235, 856), (600, 856), (600, RES_Y - 52)],
     "EVET — kategoriden bağımsız", 596, 846, anchor="end")
# K4 branches
conn([(CX - 215, 1072), (700, 1072), (700, RES_Y - 52)], "≤ 50.000 · Kategori A", 694, 1062, anchor="end")
conn([(CX + 215, 1072), (1200, 1072), (1200, RES_Y - 52)], "50.001 – 500.000 · Kategori B", 1208, 1062, anchor="start")
conn([(CX, 1136), (CX, 1180), (1420, 1180), (1420, RES_Y - 52)], "> 500.000 · Kategori C", 1428, 1170, anchor="start")

# istisna süre paneli → İRD
plain([(PX + PW, 1605), (414, 1605), (414, RES_Y), (IRD_X - 222, RES_Y)], dash="5 5")

PITCH, BW, BH = 128, 420, 86
def step(cx, i, title, sub=None, y0=1560, **kw):
    cy = y0 + i * PITCH
    node(cx, cy, BW, BH, title, sub, **kw)
    return cy

ird_kw = dict(fill=AMBER_F, stroke=AMBER_S, tcol=AMBER_T, scol="#6B4A10", title_size=14.5)
ets_kw = dict(fill=RED_F, stroke=RED_S, tcol=RED_T, scol="#6E2A24", title_size=14.5)

conn([(IRD_X, RES_Y + 52), (IRD_X, 1560 - BH/2 - 6)])
conn([(ETS_X, RES_Y + 52), (ETS_X, 1560 - BH/2 - 6)])

ird = [
    ("İzleme planını onaylatın", "İlk izlemeden en az 6 ay önce Başkanlığa sunulur (m. 28/3)"),
    ("Emisyonları izleyin", "Emisyon = Faaliyet verisi × Emisyon faktörü × Oksidasyon faktörü"),
    ("Akredite kuruluşa doğrulatın", "MEDAS ataması · ISO/IEC 17029 (m. 30)"),
    ("30 Nisan'a kadar raporlayın", "Bir önceki takvim yılının doğrulanmış emisyonu (m. 29) · gecikmede Kategori A için 627.450 ₺"),
]
ird_y = []
for i, (t, s) in enumerate(ird):
    ird_y.append(step(IRD_X, i, t, s, **ird_kw))
    if i == 3:
        badge(IRD_X + BW/2 - 84, ird_y[i] - BH/2 - 11, "CEZA RİSKİ", fill=AMBER_S)
    if i:
        conn([(IRD_X, ird_y[i-1] + BH/2), (IRD_X, ird_y[i] - BH/2 - 6)])

ets = [
    ("Yetkili personeli atayın", "Kategori B: 1 kişi · Kategori C: 2 kişi (EK-3)", None),
    ("İzleme planı ve İzleme Metodolojisi Planını hazırlayın", "İkisi de izin başvurusunun ekidir (EK-3 · EK-4)", None),
    ("Sera gazı emisyon izni başvurusu", "EK-3 ile başvuru · azami 60 gün · 5 yıl geçerli (m. 7-8)", None),
    ("Emisyonları izleyin", "Alt tesis bazında: ürün, ölçülebilir ısı, yakıt, üretim süreci", None),
    ("Akredite kuruluşa doğrulatın", "Doğrulanmamış rapor sunulamaz (m. 30)", None),
    ("30 Nisan — rapor + faaliyet seviyesi", "İkisi birlikte sunulur (m. 29 · m. 13/5)", "CEZA RİSKİ"),
    ("Ulusal Tahsisat Planı yayımlanır", "Raporların son teslim tarihinden itibaren 60 gün içinde (m. 11/2)", "DIŞ OLAY"),
    ("Ücretsiz tahsisat başvurusu", "UTP + 30 gün · geç başvuruda bedel %50 artırımlı (m. 14)", None),
    ("Açığı kapatın", "Birincil piyasa (ihale) · İkincil piyasa · Karbon kredisiyle denkleştirme · Bankalama ve ödünç alma", None),
    ("Tahsisatı teslim edin", "Kasım son iş günü · ek rezerv kullananlarda Aralık (m. 16)", "CEZA RİSKİ"),
]
ets_y = []
for i, (t, s, bg) in enumerate(ets):
    kw = dict(ets_kw)
    if bg == "DIŞ OLAY":
        kw = dict(fill=EVENT_F, stroke=EVENT_S, tcol=INK, scol=MUTED, title_size=14.5)
    ets_y.append(step(ETS_X, i, t, s, **kw))
    if i:
        conn([(ETS_X, ets_y[i-1] + BH/2), (ETS_X, ets_y[i] - BH/2 - 6)])
    if bg == "CEZA RİSKİ":
        badge(ETS_X + BW/2 - 84, ets_y[i] - BH/2 - 11, "CEZA RİSKİ")
    if bg == "DIŞ OLAY":
        badge(ETS_X + BW/2 - 72, ets_y[i] - BH/2 - 11, "DIŞ OLAY", fill=EVENT_S)

# yearly loops
conn([(IRD_X, ird_y[-1] + BH/2), (IRD_X, ird_y[-1] + BH/2 + 36), (940, ird_y[-1] + BH/2 + 36),
      (940, ird_y[1]), (IRD_X + BW/2 + 6, ird_y[1])],
     "her sistem yılı için tekrarlanır", 800, ird_y[-1] + BH/2 + 26)
conn([(ETS_X, ets_y[-1] + BH/2), (ETS_X, ets_y[-1] + BH/2 + 36), (1562, ets_y[-1] + BH/2 + 36),
      (1562, ets_y[3]), (ETS_X + BW/2 + 6, ets_y[3])],
     "her sistem yılı için tekrarlanır", 1436, ets_y[-1] + BH/2 + 26)

# izin uyarısı  (akışın parçası değil — kesikli yan not)
panel(1606, ets_y[2] - 88, 250, 176, "Dikkat", [
    ("n", "İzin 5 yıl geçerli. Bitiminden en az 6 ay önce yenileme başvurusu zorunlu (m. 8)."),
    ("n", "İzinsiz faaliyetin cezası 1.254.900 – 12.549.000 ₺ (m. 35)."),
], fill="#FFF6F5", stroke=RED_S, dash="4 4")
plain([(1606, ets_y[2]), (ETS_X + BW/2, ets_y[2])], dash="4 4", color=RED_S)

panel(PX, 1790, PW, 404, "İdari para cezaları (m. 35)", [
    ("n", "Doğrulanmış raporu süresinde sunmayanlara, tesis kategorisine göre:"),
    ("s", ""),
    ("b", "Kategori A — ≤ 50.000 t · 627.450 ₺"),
    ("b", "Kategori B — 50.001–250.000 t · 1.254.900 ₺"),
    ("b", "Kategori B — 250.001–500.000 t · 2.509.800 ₺"),
    ("b", "Kategori C — 500.001–2.000.000 t · 4.392.150 ₺"),
    ("b", "Kategori C — > 2.000.000 t · 6.274.500 ₺"),
    ("s", ""),
    ("n", "ETS kapsamındaki işletmelere bu tutarlar İKİ KAT uygulanır."),
    ("n", "İzinsiz faaliyet ayrı bir ceza kalemidir: 1.254.900 – 12.549.000 ₺."),
], fill="#FFF6F5", stroke=RED_S)

# sürekli yükümlülük — her iki kolon için ortak
CONT_Y = ets_y[-1] + BH/2 + 120
node((IRD_X + ETS_X) / 2, CONT_Y, 1100, 74,
     "Kayıtları 10 yıl saklayın",
     "Tüm veriler ve bilgi kayıtları en az 10 yıl saklanır, talep hâlinde idarenin incelemesine "
     "sunulur. Bu, yukarıdaki adımların tamamı için geçerli sürekli bir yükümlülüktür (m. 37).",
     fill="#FFFFFF", stroke=NEUT_ST, r=10, title_size=15, dash="5 5")
plain([(IRD_X, ird_y[-1] + BH/2 + 34), (IRD_X, CONT_Y - 37)], dash="5 5")
plain([(ETS_X, ets_y[-1] + BH/2 + 34), (ETS_X, CONT_Y - 37)], dash="5 5")

# footer
FY = CONT_Y + 78
add(f'<line x1="48" y1="{FY}" x2="{W-48}" y2="{FY}" stroke="{LINE}" stroke-width="1.2"/>')
add(f'<text x="48" y="{FY+26}" font-family="{FONT}" font-size="11.5" fill="{FAINT}">'
    f'Bu şema bilgilendirme amaçlıdır ve ön değerlendirme niteliğindedir. Kesin kapsam belirlemesi '
    f'tesisin kapasite raporu, yakma ünitelerinin anma ısıl güçleri ve onaylı izleme planı üzerinden '
    f'yapılır; nihai yetki İklim Değişikliği Başkanlığı’ndadır.</text>')
add(f'<text x="{W-48}" y="{FY+26}" text-anchor="end" font-family="{MONO}" font-size="11.5" '
    f'fill="{FAINT}">RG 27.08.2026 / 33353</text>')

add('</svg>')

svg = "\n".join(out)
open("ets-karar-agaci.svg", "w", encoding="utf-8").write(svg)
print("height used:", FY + 40, "declared:", H)
