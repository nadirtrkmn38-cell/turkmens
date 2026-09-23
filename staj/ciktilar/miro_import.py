#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TR ETS kapsam belirleme karar şemasını Miro board'una NATIF (düzenlenebilir)
şekiller ve bağlayıcılar olarak kurar.

Kullanım
────────
1. https://miro.com/app/settings/user-profile/apps adresinden "Create new app"
   ile bir uygulama oluştur. Scope olarak boards:read ve boards:write seç,
   ardından "Install app and get OAuth token" ile token al.
2. Board kimliğini adres çubuğundan al:  miro.com/app/board/<BOARD_ID>/
3. Çalıştır:
       export MIRO_TOKEN="alınan_token"
       python3 miro_import.py --board "uXjVHjigcw8="
   Kuru çalıştırma (hiçbir şey göndermez, sadece sayar):
       python3 miro_import.py --board "..." --dry-run

Not: Şekiller boş bir board'a kurulur. Mevcut board'daki öğeler silinmez;
temiz bir sonuç için yeni board açman önerilir.
"""

import argparse, json, os, sys, time, urllib.parse, urllib.request, urllib.error

API = "https://api.miro.com/v2"

# ───────────────────────────── palet ─────────────────────────────
PAL = {
    "neutral": dict(fill="#e9ece5", border="#a9b2a6", text="#16232b"),
    "start":   dict(fill="#ffffff", border="#a9b2a6", text="#16232b"),
    "green":   dict(fill="#dcebdd", border="#2e6b3c", text="#1c4426"),
    "amber":   dict(fill="#f8ebd3", border="#9a6208", text="#5a3a05"),
    "red":     dict(fill="#f6e2df", border="#8f2b25", text="#591a16"),
    "event":   dict(fill="#e7eaef", border="#8892a1", text="#16232b"),
    "panel":   dict(fill="#f1f3ed", border="#cdd3c8", text="#16232b"),
    "warn":    dict(fill="#fff6f5", border="#8f2b25", text="#591a16"),
    "opportunity": dict(fill="#e3efec", border="#0b5d58", text="#11332f"),
}

CX, IRD_X, ETS_X = 940, 660, 1310
RES_Y, PITCH, BW, BH = 980, 150, 420, 100
STEP0 = 1120

def sy(i):
    return STEP0 + i * PITCH

# ───────────────────── düğümler ─────────────────────
# (anahtar, biçim, cx, cy, genişlik, yükseklik, başlık, alt satır, palet)
NODES = [
    ("start", "round_rectangle", CX, 300, 320, 60,
     "Tesis değerlendirmesini başlat", "", "start"),

    ("k1", "rhombus", CX, 432, 440, 150,
     "Tesiste EK-1 listesindeki bir faaliyet yürütülüyor mu?", "m. 27/2 · EK-1", "neutral"),
    ("k4", "rhombus", CX, 700, 440, 150,
     "Kurulu kapasiteye göre ihtiyatlı hesaplanan yıllık emisyon kaç ton CO₂e?",
     "m. 4 · m. 5/1", "neutral"),

    ("out1", "round_rectangle", 1520, 432, 420, 90,
     "KAPSAM DIŞI", "Hiçbir yükümlülük doğmaz. Tahsisat, izin, izleme ve raporlama yok.", "green"),

    ("ird", "round_rectangle", IRD_X, RES_Y, 440, 110,
     "ETS DIŞI — İRD YÜKÜMLÜSÜ",
     "Kategori A ve ETS dışı bırakılan özel tesisler. Tahsisat almaz, teslim etmezsiniz; "
     "izleme, raporlama ve doğrulama sürer.", "amber"),
    ("ets", "round_rectangle", ETS_X, RES_Y, 440, 110,
     "ETS KAPSAMINDA",
     "İzin + izleme, raporlama, doğrulama + her yıl emisyona denk tahsisat teslimi.", "red"),

    # ── İRD hattı ──
    ("i1", "round_rectangle", IRD_X, sy(0), BW, BH,
     "İzleme planını onaylatın", "İlk izlemeden en az 6 ay önce Başkanlığa sunulur (m. 28/3)", "amber"),
    ("i2", "round_rectangle", IRD_X, sy(1), BW, BH,
     "Emisyonları izleyin", "Emisyon = Faaliyet verisi × Emisyon faktörü × Oksidasyon faktörü", "amber"),
    ("i3", "round_rectangle", IRD_X, sy(2), BW, BH,
     "Akredite kuruluşa doğrulatın",
     "MEDAS ataması · ISO/IEC 17029 akreditasyonu (m. 30 · m. 33/2)", "amber"),
    ("i4", "round_rectangle", IRD_X, sy(3), BW, BH,
     "30 Nisan'a kadar raporlayın",
     "CEZA RİSKİ · Bir önceki takvim yılının doğrulanmış emisyonu — gecikmede Kategori A için 627.450 ₺ (m. 29 · m. 35)", "amber"),

    # ── ETS hattı ──
    ("e1", "round_rectangle", ETS_X, sy(0), BW, BH,
     "Yetkili personeli atayın", "Kategori B: 1 kişi · Kategori C: 2 kişi (EK-3)", "red"),
    ("e2", "round_rectangle", ETS_X, sy(1), BW, BH,
     "İzleme planı ve İzleme Metodolojisi Planını hazırlayın",
     "İkisi de izin başvurusunun ekidir (EK-3 · EK-4)", "red"),
    ("e3", "round_rectangle", ETS_X, sy(2), BW, BH,
     "Sera gazı emisyon izni başvurusu", "EK-3 ile başvuru · azami 60 gün · 5 yıl geçerli (m. 7-8)", "red"),
    ("e4", "round_rectangle", ETS_X, sy(3), BW, BH,
     "Emisyonları izleyin", "Alt tesis bazında: ürün, ölçülebilir ısı, yakıt, üretim süreci", "red"),
    ("e5", "round_rectangle", ETS_X, sy(4), BW, BH,
     "Akredite kuruluşa doğrulatın",
     "Doğrulanmamış rapor sunulamaz · 4734 sayılı Kanuna tabi işletmeler MEDAS dışıdır (m. 30)", "red"),
    ("e6", "round_rectangle", ETS_X, sy(5), BW, BH,
     "30 Nisan — rapor + faaliyet seviyesi", "CEZA RİSKİ · İkisi birlikte sunulur (m. 29 · m. 13/5)", "red"),
    ("e7", "round_rectangle", ETS_X, sy(6), BW, BH,
     "Ulusal Tahsisat Planı yayımlanır",
     "DIŞ OLAY · Raporların son teslim tarihinden itibaren 60 gün içinde (m. 11/2)", "event"),
    ("e8", "round_rectangle", ETS_X, sy(7), BW, BH,
     "Ücretsiz tahsisat başvurusu", "UTP + 30 gün · geç başvuruda bedel %50 artırımlı (m. 14)", "red"),
    ("e9", "round_rectangle", ETS_X, sy(8), BW, BH,
     "Açığı kapatın",
     "Birincil piyasa (ihale) · İkincil piyasa · Karbon kredisiyle denkleştirme · Bankalama ve ödünç alma", "red"),
    ("e10", "round_rectangle", ETS_X, sy(9), BW, BH,
     "Tahsisatı teslim edin", "CEZA RİSKİ · Kasım son iş günü · ek rezerv kullananlarda Aralık (m. 16)", "red"),

    ("kayit", "round_rectangle", (IRD_X + ETS_X) // 2, sy(9) + 190, 1100, 90,
     "Sürekli yükümlülükler — her iki profil için",
     "Tüm veri ve bilgi kayıtlarını en az 10 yıl saklayın (m. 37) · Faaliyet, tesis niteliği, "
     "kategori veya izin sahibi değişikliklerini 30 gün içinde Başkanlığa bildirin (m. 9/1 · m. 34/4-5)", "start"),
]

# ───────────────────── kim ne yapar ─────────────────────
# Her adımın altındaki "KİM" satırı: başvurunun yapıldığı yer ve işlemi yürüten kurum.
WHO = {
    "i1": "İklim Değişikliği Başkanlığı onaylar",
    "i2": "İşletme · onaylı izleme planına göre",
    "i3": "MEDAS doğrulayıcı atar · TÜRKAK akredite eder",
    "i4": "Başkanlığa, elektronik sistem üzerinden",
    "e1": "İşletme belirler · bilgileri izin başvurusunda",
    "e2": "İşletme hazırlar · Başkanlık onaylar",
    "e3": "Başvuru Başkanlığa · Başkanlık değerlendirir",
    "e4": "İşletme · onaylı izleme planına göre",
    "e5": "MEDAS doğrulayıcı atar · TÜRKAK akredite eder",
    "e6": "Başkanlığa, elektronik sistem üzerinden",
    "e7": "Başkanlık hazırlar · Karbon Piyasası Kurulu onaylar",
    "e8": "Başvuru Başkanlığa · transfer EPDK usulüyle İKS'den",
    "e9": "İhale ve ikincil piyasa · Piyasa İşletmecisi (EPİAŞ)",
    "e10": "İKS üzerinden teslim · Piyasa İşletmecisi (EPİAŞ)",
}

# ───────────────────── bağlayıcılar ─────────────────────
# (kaynak, hedef, etiket, kesikli mi)
EDGES = [
    ("start", "k1", "", False),
    ("k1", "out1", "HAYIR", False),
    ("k1", "k4", "EVET", False),
    ("k4", "ird", "≤ 50.000 · Kategori A", False),
    ("k4", "ets", "> 50.000 · Kategori B ve C", False),

    ("ird", "i1", "", False),
    ("i1", "i2", "", False),
    ("i2", "i3", "", False),
    ("i3", "i4", "", False),
    ("i4", "i2", "her sistem yılı için tekrarlanır", False),

    ("ets", "e1", "", False),
    ("e1", "e2", "", False),
    ("e2", "e3", "", False),
    ("e3", "e4", "", False),
    ("e4", "e5", "", False),
    ("e5", "e6", "", False),
    ("e6", "e7", "", False),
    ("e7", "e8", "", False),
    ("e8", "e9", "", False),
    ("e9", "e10", "", False),
    ("e10", "e4", "her sistem yılı için tekrarlanır", False),

    ("i4", "kayit", "", True),
    ("e10", "kayit", "", True),
    ("p_ozel", "k4", "", True),
    ("p_dikkat", "e3", "", True),
    ("p_biz", "e9", "", True),
]

# ───────────────────── bilgi panelleri ─────────────────────
# (anahtar, cx, cy, genişlik, yükseklik, başlık, satırlar, palet)
PANELS = [
    ("p_ek1", 220, 590, 344, 630, "EK-1 FAALİYETLERİ (ÖZET)", [
        "ENERJİ",
        "• Yakıtların yakılması — tesisteki TÜM yakma ünitelerinin toplam anma ısıl gücü ≥ 20 MW",
        "• Petrol rafinasyonu — ≥ 20 MW",
        "• Kok üretimi — eşik yok",
        "METAL",
        "• Cevher kavurma, sinterleme, peletleme",
        "• Demir-çelik üretimi ve dökümü — > 2,5 ton/saat",
        "• Demirli metal işleme — ≥ 20 MW",
        "• Birincil alüminyum ve alümina",
        "• İkincil alüminyum, demir dışı metaller — ≥ 20 MW",
        "MİNERAL",
        "• Klinker — ≥ 500 t/gün (döner fırın)",
        "• Kireç, dolomit, magnezit — ≥ 50 t/gün",
        "• Cam — ≥ 20 t/gün · Seramik — ≥ 75 t/gün",
        "• Mineral elyaf yalıtım — ≥ 20 t/gün",
        "• Alçı taşı ürünleri — ≥ 20 MW",
        "SELÜLOZ VE KÂĞIT",
        "• Selüloz üretimi — eşik yok",
        "• Kâğıt, mukavva, karton — ≥ 20 t/gün",
        "KİMYA",
        "• Karbon siyahı — ≥ 20 MW",
        "• Nitrik asit, adipik asit, glioksal, amonyak",
        "• Organik kimyasallar — ≥ 100 t/gün",
        "• Hidrojen ve sentez gazı — ≥ 5 t/gün",
        "• Soda külü ve sodyum bikarbonat",
        "",
        "Tam liste 25 faaliyettir. Ayrıntı için EK-1'e bakınız.",
    ], "panel"),

    ("p_20mw", 220, 1062, 344, 270, "ANMA ISIL GÜCÜ NASIL TOPLANIR?", [
        "Tesisteki tüm yakma ünitelerinin anma ısıl güçleri TOPLANIR: kazan, brülör, türbin, "
        "ısıtıcı, ocak, insineratör, kalsinatör, döner fırın, fırın, kurutucu, motor, yakıt "
        "hücresi, yakma bacası, termal veya katalitik yakma sonrası ünitesi.",
        "",
        "3 MW altındaki üniteler ve münhasıran biyokütle kullananlar bu toplama GİRMEZ.",
        "Toplam 20 MW ve üzeriyse tesis EK-1 kapsamındadır.",
    ], "panel"),

    ("p_kural", 220, 1347, 344, 250, "EN ÇOK KAÇIRILAN ÜÇ KURAL", [
        "• Aynı kategorideki faaliyetlerin kapasiteleri toplanarak eşiğe bakılır.",
        "• Eşik kurulu kapasiteye bakar, fiilî üretime değil.",
        "• EK-1'deki bir faaliyeti yürüten işletmenin aynı tesisteki diğer EK-1 faaliyetleri, "
        "kapasite gözetilmeksizin kapsama dâhil olur (m. 27/2).",
    ], "panel"),

    ("p_kisalt", 220, 1500, 344, 260, "KURUMLAR VE KISALTMALAR", [
        "• Başkanlık — İklim Değişikliği Başkanlığı",
        "• KPK — Karbon Piyasası Kurulu (Bakan başkanlığında)",
        "• EPDK — Enerji Piyasası Düzenleme Kurumu",
        "• Piyasa İşletmecisi — EPİAŞ",
        "• İKS — İşlem Kayıt Sistemi; Piyasa İşletmecisi işletir",
        "• MEDAS — Merkezi Elektronik Doğrulayıcı Kuruluş Atama Sistemi",
        "• TÜRKAK — Türk Akreditasyon Kurumu",
    ], "panel"),

    ("p_ceza", 220, 1992, 344, 400, "İDARİ PARA CEZALARI (m. 35)", [
        "Doğrulanmış raporu süresinde sunmayanlara, tesis kategorisine göre:",
        "",
        "• Kategori A — ≤ 50.000 t · 627.450 ₺",
        "• Kategori B — 50.001–250.000 t · 1.254.900 ₺",
        "• Kategori B — 250.001–500.000 t · 2.509.800 ₺",
        "• Kategori C — 500.001–2.000.000 t · 4.392.150 ₺",
        "• Kategori C — > 2.000.000 t · 6.274.500 ₺",
        "",
        "ETS kapsamındaki işletmelere bu tutarlar İKİ KAT uygulanır.",
        "İzinsiz faaliyet ayrı bir ceza kalemidir: 1.254.900 – 12.549.000 ₺.",
    ], "warn"),

    ("p_dikkat", 1730, sy(2) + 20, 250, 200, "DİKKAT", [
        "İzin 5 yıl geçerli. Bitiminden en az 6 ay önce yenileme başvurusu zorunlu (m. 8).",
        "",
        "İzinsiz faaliyetin cezası 1.254.900 – 12.549.000 ₺ (m. 35).",
        "",
        "Geçiş: Kanun'un yürürlüğünden itibaren 3 yıl içinde izin alınmalıdır. Bu süre içinde "
        "bir kereye mahsus izinli sayılırsınız (Geçici m. 2).",
    ], "warn"),

    ("p_hesap", 220, 2400, 344, 320, "İKİ HESAP", [
        "Emisyon = Faaliyet verisi × Emisyon faktörü × Oksidasyon faktörü (EK-6)",
        "Biyokütlenin emisyon faktörü sıfır kabul edilir.",
        "",
        "Ücretsiz tahsisat = Kıyas değeri × Ücretsiz tahsisat oranı × Sektörel faaliyet "
        "katsayısı × Faaliyet seviyesi (m. 13/7)",
        "",
        "Açık = Doğrulanmış emisyon − Ücretsiz tahsisat",
        "Bu fark her yıl piyasadan satın alınır. Azaltım yatırımlarının geri ödeme hesabına "
        "bu kalem de girer.",
    ], "panel"),

    ("p_gaz", 220, 2760, 344, 260, "KAPSAMDAKİ SERA GAZLARI (EK-2)", [
        "• Karbondioksit (CO₂)",
        "• Metan (CH₄)",
        "• Diazot oksit (N₂O)",
        "• Hidroflorokarbonlar (HFC)",
        "• Perflorokarbonlar (PFC)",
        "• Kükürt heksaflorür (SF₆)",
        "",
        "Kategori hesabında biyokütle kaynaklı CO₂ hariç, transfer edilen CO₂ dâhil tutulur (m. 4).",
    ], "panel"),

    ("p_biz", 1730, sy(8) + 100, 250, 300, "★ BİZİM DEVREYE GİRDİĞİMİZ YER", [
        "Açık, her yıl piyasadan satın alınan bir maliyet kalemidir. Açığı küçültmek hem bu "
        "maliyeti hem de fiyat riskini azaltır.",
        "",
        "NE YAPABİLİRİZ",
        "• Enerji etüdü ile azaltım potansiyelinin tespiti",
        "• Atık ısı geri kazanımı, buhar ve kondenstop iyileştirmesi, izolasyon",
        "• Motor, sürücü (VSD) ve basınçlı hava sistemleri verimliliği",
        "• Yakıt dönüşümü ve biyokütle — biyokütlenin emisyon faktörü sıfır kabul edilir (EK-6)",
        "• Elektrifikasyon ile tesis içi yakma emisyonunun azaltılması",
        "• Çatı GES ve öz tüketim, YEK-G ile yeşil elektrik tedariki",
        "• ISO 50001 enerji yönetim sistemi kurulumu",
        "• Sayaçlama ve veri altyapısı — İRD yükümlülüğüyle aynı altyapıyı besler",
        "• Fizibilite: geri ödeme ve NBD hesabına tahsisat maliyetinin dâhil edilmesi",
        "• VAP destekleriyle yatırım maliyetinin düşürülmesi",
    ], "opportunity"),

    ("p_ozel", 1580, 620, 542, 230, "ÖZEL DURUMLAR — AYRICA DEĞERLENDİRİLİR", [
        "EK-1 faaliyeti yürütse de aşağıdaki tesisler farklı değerlendirilir. Tesisiniz bu "
        "gruptaysa ayrı bir inceleme yapılmalıdır.",
        "YÖNETMELİK DIŞI",
        "• Ar-Ge tesis veya bölümleri, münhasıran biyokütle kullanan tesisler, askerî unsurlar (m. 2/2)",
        "ETS DIŞI, İRD SÜRER",
        "• Kalıcı: okul, üniversite, hastane ve savunma sanayi kuruluşlarına ait tesisler (m. 5/2-3)",
        "• Geçici: doğal gaz ve ham petrol iletimi ve depolanması, birinci uygulama dönemi "
        "sonuna kadar (Geçici m. 6)",
    ], "panel"),

    ("p_fiyat", 950, 3300, 1804, 380, "FİYAT OLUŞUMU VE YETKİLİ KURUMLAR", [
        "Tahsisatın sabit bir tarifesi yoktur; fiyat piyasada oluşur. Devlet fiyatı doğrudan "
        "koymaz, arzı ve sınırları belirler.",
        "ARZ — ÜST SINIR",
        "ETS üst sınırı emisyon yoğunluğu temelli belirlenir ve Ulusal Tahsisat Planı ile "
        "açıklanır. Birincil piyasada satışa sunulacak tahsisat miktarını Karbon Piyasası "
        "Kurulu tespit eder (m. 11 · m. 23/2).",
        "BİRİNCİL PİYASA — İHALE",
        "Tahsisatlar, Başkanlıkça belirlenen ihale takvimine göre ihaleyle satılır. Takvim, UTP "
        "yayımından sonraki 15 iş günü içinde Piyasa İşletmecisinin internet sitesinde ilan "
        "edilir (m. 17).",
        "İKİNCİL PİYASA — ARZ VE TALEP",
        "Sürekli ticaret yöntemiyle işletilir; fiyat alıcı ve satıcıların emirlerine göre oluşur "
        "(m. 18).",
        "FİYAT ARALIĞI VE İSTİKRAR",
        "Asgari ve azami tahsisat fiyatı aralıklarını belirlemeye Karbon Piyasası Kurulu "
        "yetkilidir; kararlar Başkanlıkça resmî internet sayfasında ilan edilir. Piyasa istikrar "
        "rezervi, dolaşımdaki tahsisat miktarı ve fiyatlar değerlendirilerek devreye alınır "
        "(m. 19 · m. 21/1).",
        "||",
        "EK REZERV FİYATI",
        "Son 3 ayın birincil ve ikincil piyasa ağırlıklı ortalama fiyatlarından yüksek olanının "
        "%50 fazlası; azami fiyatı Başkanlık ve EPDK koordineli belirler (m. 16/6).",
        "KARBON KREDİSİYLE DENKLEŞTİRME",
        "Yurt içi projelerden elde edilen karbon kredileri, teslim yükümlülüğünün Karbon Piyasası "
        "Kurulunca belirlenen oranını geçmemek üzere kullanılabilir (m. 25/1).",
        "PİYASANIN İŞLEYİŞİ",
        "İKS'yi ve birincil ile ikincil ETS piyasasını Piyasa İşletmecisi (EPİAŞ) işletir. "
        "Piyasa işleyişinin usul ve esaslarını Bakanlık, Enerji ve Tabii Kaynaklar Bakanlığı ve "
        "SPK ile koordineli olarak EPDK belirler. TOBB başkanlığındaki Danışma Kurulu, Karbon "
        "Piyasası Kuruluna sunulmak üzere istişari kararlar alır (m. 4/1-k · m. 21/3 · m. 22/1 · m. 24).",
    ], "panel"),

    ("p_lejant", 1620, 150, 460, 170, "RENK ANAHTARI", [
        "YEŞİL — yükümlülük yok, sistem hiç uygulanmaz",
        "SARI — yalnızca izleme, raporlama ve doğrulama",
        "KIRMIZI — tam ETS: izin, İRD ve tahsisat teslimi",
        "GRİ — yardımcı bilgi, akışın parçası değil",
        "KİM — başvurunun yapıldığı ve işlemi yürüten kurum",
    ], "start"),
]

# ───────────────────── fiyatta kimin rolü ne ─────────────────────
# (kurum, rolü) — fiyat bölümünün üstündeki tek bakışta özet
PRICE_ROLES = [
    ("Karbon Piyasası Kurulu",
     "Satışa sunulacak tahsisat miktarını, asgari–azami fiyat aralığını ve karbon kredisi "
     "oranını belirler (m. 21/1 · m. 23/2 · m. 25/1)"),
    ("İklim Değişikliği Başkanlığı",
     "İhale takvimini ve istikrar rezervine aktarılacak miktarı belirler, Kurul kararlarını "
     "ilan eder (m. 17/1 · m. 19/2 · m. 21/1)"),
    ("EPDK",
     "ETS piyasasının ve İşlem Kayıt Sisteminin usul ve esaslarını belirler "
     "(m. 21/3 · m. 22/5)"),
    ("Piyasa İşletmecisi (EPİAŞ)",
     "İhaleleri ve ikincil piyasayı organize edip işletir, İşlem Kayıt Sistemini yürütür "
     "(m. 4/1-k · m. 22/1)"),
    ("Piyasa katılımcıları",
     "Fiyat birincil piyasada ihaleyle, ikincil piyasada alış ve satış emirleriyle oluşur "
     "(m. 17 · m. 18)"),
]

TITLE = ("baslik", 700, 120, 1200, 120,
         "İşletmem ETS kapsamına giriyor mu?",
         "Türkiye Emisyon Ticaret Sistemi · Tesis değerlendirmesi — "
         "Dayanak: RG 27.08.2026 / 33353", "start")


# ───────────────────────────── API ─────────────────────────────
def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def post(path, payload, token):
    req = urllib.request.Request(
        API + path,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": "Bearer " + token,
                 "Content-Type": "application/json",
                 "Accept": "application/json"},
        method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)
    except urllib.error.HTTPError as ex:
        body = ex.read().decode("utf-8", "replace")
        raise SystemExit(f"\nMiro API hatası {ex.code} — {path}\n{body}\n")


def shape_payload(cx, cy, w, h, shape, title, sub, pal):
    p = PAL[pal]
    content = f"<p><strong>{esc(title)}</strong></p>"
    if sub:
        content += f"<p>{esc(sub)}</p>"
    return {
        "data": {"content": content, "shape": shape},
        "style": {
            "fillColor": p["fill"], "borderColor": p["border"], "color": p["text"],
            "borderWidth": "2", "fontFamily": "open_sans", "fontSize": "14",
            "textAlign": "center", "textAlignVertical": "middle",
        },
        "position": {"x": cx, "y": cy, "origin": "center"},
        "geometry": {"width": w, "height": h},
    }


def panel_payload(cx, cy, w, h, heading, lines, pal):
    p = PAL[pal]
    content = f"<p><strong>{esc(heading)}</strong></p>"
    for ln in lines:
        content += "<p>" + (esc(ln) if ln else "&nbsp;") + "</p>"
    return {
        "data": {"content": content, "shape": "rectangle"},
        "style": {
            "fillColor": p["fill"], "borderColor": p["border"], "color": p["text"],
            "borderWidth": "1", "fontFamily": "open_sans", "fontSize": "11",
            "textAlign": "left", "textAlignVertical": "top",
        },
        "position": {"x": cx, "y": cy, "origin": "center"},
        "geometry": {"width": w, "height": h},
    }


def connector_payload(a, b, label, dashed):
    body = {
        "startItem": {"id": a},
        "endItem": {"id": b},
        "shape": "elbowed",
        "style": {
            "strokeColor": "#6e7b76", "strokeWidth": "2",
            "strokeStyle": "dashed" if dashed else "normal",
            "endStrokeCap": "arrow",
        },
    }
    if label:
        body["captions"] = [{"content": esc(label), "position": "50%"}]
    return body


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--board", required=True, help="Board ID, ör. uXjVHjigcw8=")
    ap.add_argument("--token", default=os.environ.get("MIRO_TOKEN", ""))
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    total = len(NODES) + len(PANELS) + 1 + len(EDGES)
    if a.dry_run:
        print(f"Kuru çalıştırma: {len(NODES)} şekil, {len(PANELS)+1} panel, "
              f"{len(EDGES)} bağlayıcı — toplam {total} öğe. Hiçbir istek gönderilmedi.")
        return
    if not a.token:
        raise SystemExit("Token yok. MIRO_TOKEN ortam değişkenini ayarla veya --token ver.")

    bid = urllib.parse.quote(a.board, safe="")
    ids = {}
    n = 0

    for key, shape, cx, cy, w, h, title, sub, pal in NODES:
        if key in WHO:
            sub = f"{sub} — KİM: {WHO[key]}"
        r = post(f"/boards/{bid}/shapes",
                 shape_payload(cx, cy, w, h, shape, title, sub, pal), a.token)
        ids[key] = r["id"]; n += 1
        print(f"[{n}/{total}] şekil: {title[:48]}")
        time.sleep(0.12)

    for key, cx, cy, w, h, heading, lines, pal in PANELS:
        lines = [ln for ln in lines if ln != "||"]
        r = post(f"/boards/{bid}/shapes",
                 panel_payload(cx, cy, w, h, heading, lines, pal), a.token)
        ids[key] = r["id"]; n += 1
        print(f"[{n}/{total}] panel: {heading[:48]}")
        time.sleep(0.12)

    k, cx, cy, w, h, t, s, pal = TITLE
    post(f"/boards/{bid}/shapes",
         {**shape_payload(cx, cy, w, h, "rectangle", t, s, pal),
          "style": {**shape_payload(cx, cy, w, h, "rectangle", t, s, pal)["style"],
                    "fontSize": "24", "borderWidth": "0", "fillColor": "#fbfbf8"}}, a.token)
    n += 1
    print(f"[{n}/{total}] başlık")
    time.sleep(0.12)

    for src, dst, label, dashed in EDGES:
        if src not in ids or dst not in ids:
            print(f"     atlandı: {src} → {dst}")
            continue
        post(f"/boards/{bid}/connectors",
             connector_payload(ids[src], ids[dst], label, dashed), a.token)
        n += 1
        print(f"[{n}/{total}] ok: {src} → {dst}")
        time.sleep(0.12)

    print("\nTamamlandı. Board'u açıp Ctrl+A ile hepsini seçip "
          "Arrange menüsünden hizalayabilirsin.")


if __name__ == "__main__":
    main()
