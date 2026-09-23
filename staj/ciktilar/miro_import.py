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
     "izleme, raporlama ve doğrulama (İRD) sürer.", "amber"),
    ("ets", "round_rectangle", ETS_X, RES_Y, 440, 110,
     "ETS KAPSAMINDA",
     "Sera gazı emisyon izni + izleme, raporlama ve doğrulama + her yıl emisyona denk tahsisat teslimi.", "red"),

    # ── İRD hattı ──
    ("i1", "round_rectangle", IRD_X, sy(0), BW, BH,
     "İzleme planını onaylatın", "İlk izlemeden en az 6 ay önce İklim Değişikliği Başkanlığına sunulur (m. 28/3)", "amber"),
    ("i2", "round_rectangle", IRD_X, sy(1), BW, BH,
     "Emisyonları izleyin", "Emisyon = Faaliyet verisi × Emisyon faktörü × Oksidasyon faktörü", "amber"),
    ("i3", "round_rectangle", IRD_X, sy(2), BW, BH,
     "Akredite kuruluşa doğrulatın",
     "Doğrulanmamış rapor sunulamaz · doğrulayıcı ISO/IEC 17029 akreditasyonlu olmalı (m. 30/1 · m. 33/2)", "amber"),
    ("i4", "round_rectangle", IRD_X, sy(3), BW, BH,
     "30 Nisan'a kadar raporlayın",
     "CEZA RİSKİ · Bir önceki takvim yılının doğrulanmış emisyonu — gecikmede Kategori A için 627.450 ₺ (m. 29 · m. 35)", "amber"),

    # ── ETS hattı ──
    ("e1", "round_rectangle", ETS_X, sy(0), BW, BH,
     "İzleme planını ve İzleme Metodolojisi Planını hazırlayın",
     "İzlemeye başlamadan en az 6 ay önce sunulur · ikisi de izin başvurusunun ekidir "
     "(m. 28/3 · m. 13/4 · EK-3 · EK-4)", "red"),
    ("e2", "round_rectangle", ETS_X, sy(1), BW, BH,
     "Yetkili personeli belirleyin",
     "Kategori B: en az 1 yıl deneyimli 1 kişi · Kategori C: en az 2 yıl deneyimli 2 kişi · "
     "mühendislik veya fen fakültesi mezunu (EK-3/9)", "red"),
    ("e3", "round_rectangle", ETS_X, sy(2), BW, BH,
     "Sera gazı emisyon izni başvurusu",
     "Planlar ve personel bilgisiyle EK-3 dosyası · azami 60 gün · 5 yıl geçerli (m. 7-8)", "red"),
    ("e4", "round_rectangle", ETS_X, sy(3), BW, BH,
     "Emisyonları izleyin", "Alt tesis bazında: ürün, ölçülebilir ısı, yakıt, üretim süreci", "red"),
    ("e5", "round_rectangle", ETS_X, sy(4), BW, BH,
     "Akredite kuruluşa doğrulatın",
     "Doğrulanmamış rapor sunulamaz · 4734 sayılı Kamu İhale Kanununa tabi işletmeler MEDAS dışındadır (m. 30)", "red"),
    ("e6", "round_rectangle", ETS_X, sy(5), BW, BH,
     "30 Nisan — rapor + faaliyet seviyesi", "CEZA RİSKİ · İkisi birlikte sunulur (m. 29 · m. 13/5)", "red"),
    ("e7", "round_rectangle", ETS_X, sy(6), BW, BH,
     "Ulusal Tahsisat Planı yayımlanır",
     "DIŞ OLAY · Raporların son teslim tarihinden itibaren 60 gün içinde (m. 11/2)", "event"),
    ("e8", "round_rectangle", ETS_X, sy(7), BW, BH,
     "Ücretsiz tahsisat başvurusu", "Ulusal Tahsisat Planının yayımından itibaren 30 gün · geç başvuruda bedel %50 artırımlı (m. 14)", "red"),
    ("e9", "round_rectangle", ETS_X, sy(8), BW, BH,
     "Açığı kapatın",
     "Birincil piyasa (ihale) · İkincil piyasa · Karbon kredisiyle denkleştirme · Bankalama ve ödünç alma", "red"),
    ("e10", "round_rectangle", ETS_X, sy(9), BW, BH,
     "Tahsisatı teslim edin", "CEZA RİSKİ · Kasım son iş günü, ek rezervde Aralık son iş günü · eksik "
     "her tahsisat için son 3 ay ortalama fiyatın 2 katı ceza (m. 16 · 7552 s. Kanun m. 14)", "red"),

    ("kayit", "round_rectangle", (IRD_X + ETS_X) // 2, sy(9) + 190, 1100, 90,
     "Sürekli yükümlülükler — her iki profil için",
     "Tüm veri ve bilgi kayıtlarını en az 10 yıl saklayın (m. 37) · Faaliyet, tesis niteliği, "
     "kategori veya izin sahibi değişikliklerini 30 gün içinde İklim Değişikliği Başkanlığına bildirin (m. 9/1 · m. 34/4-5)", "start"),
]

# ───────────────────── kim ne yapar ─────────────────────
# Her adımın altındaki "KİM" satırı: başvurunun yapıldığı yer ve işlemi yürüten kurum.
WHO = {
    "i1": "İklim Değişikliği Başkanlığı onaylar",
    "i2": "İşletme · İklim Değişikliği Başkanlığınca onaylanan izleme planına göre",
    "i3": "Doğrulayıcıyı İklim Değişikliği Başkanlığının MEDAS sistemi atar · "
          "Türk Akreditasyon Kurumu akredite eder",
    "i4": "İklim Değişikliği Başkanlığına, elektronik sistem üzerinden",
    "e1": "İşletme hazırlar · İklim Değişikliği Başkanlığı onaylar",
    "e2": "İşletme belirler · kendi personeli yoksa bu nitelikte dış uzman görevlendirebilir",
    "e3": "Başvuru İklim Değişikliği Başkanlığına yapılır ve orada değerlendirilir",
    "e4": "İşletme · İklim Değişikliği Başkanlığınca onaylanan izleme planına göre",
    "e5": "Doğrulayıcıyı İklim Değişikliği Başkanlığının MEDAS sistemi atar · "
          "Türk Akreditasyon Kurumu akredite eder",
    "e6": "İklim Değişikliği Başkanlığına, elektronik sistem üzerinden",
    "e7": "İklim Değişikliği Başkanlığı hazırlar · Karbon Piyasası Kurulu onaylar",
    "e8": "Başvuru İklim Değişikliği Başkanlığına · aktarım Enerji Piyasası Düzenleme "
          "Kurumu usulüyle",
    "e9": "İhaleyi ve ikincil piyasayı Enerji Piyasaları İşletme A.Ş. (EPİAŞ) işletir",
    "e10": "İşlem Kayıt Sistemi üzerinden · sistemi Enerji Piyasaları İşletme A.Ş. (EPİAŞ) işletir",
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
        "• Yakıtların yakılması — tesisteki TÜM yakma ünitelerinin toplam anma ısıl gücü ≥ 20 MW (tehlikeli ve belediye atıklarının yakılması hariç)",
        "• Petrol rafinasyonu — ≥ 20 MW",
        "• Kok üretimi — eşik yok",
        "METAL",
        "• Cevher kavurma, sinterleme, peletleme",
        "• Demir-çelik üretimi ve dökümü — ≥ 2,5 ton/saat",
        "• Demirli metal işleme — ≥ 20 MW",
        "• Birincil alüminyum ve alümina",
        "• İkincil alüminyum, demir dışı metaller — ≥ 20 MW",
        "MİNERAL",
        "• Klinker — döner fırında ≥ 500 t/gün, diğer ocaklarda > 50 t/gün",
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
        "hücresi, kimyasal döngüsel yakma ünitesi, yakma bacası, termal veya katalitik yakma "
        "sonrası ünitesi.",
        "",
        "3 MW altındaki üniteler ve münhasıran biyokütle kullananlar bu toplama GİRMEZ. Yalnız "
        "devreye alma ve durdurmada fosil yakıt kullanan biyokütle üniteleri de münhasıran "
        "biyokütle sayılır (EK-1).",
        "Toplam 20 MW ve üzeriyse tesis EK-1 kapsamındadır.",
    ], "panel"),

    ("p_kural", 220, 1347, 344, 250, "EN ÇOK KAÇIRILAN ÜÇ KURAL", [
        "• Aynı kategorideki faaliyetlerin kapasiteleri toplanarak eşiğe bakılır.",
        "• Eşik kurulu kapasiteye bakar, fiilî üretime değil.",
        "• EK-1'deki bir faaliyeti yürüten işletmenin aynı tesisteki diğer EK-1 faaliyetleri, "
        "kapasite gözetilmeksizin kapsama dâhil olur (m. 27/2).",
    ], "panel"),

    ("p_kisalt", 220, 1500, 344, 260, "KISALTMALAR", [
        "• ETS — Emisyon Ticaret Sistemi",
        "• İRD — İzleme, raporlama ve doğrulama",
        "• EPDK — Enerji Piyasası Düzenleme Kurumu",
        "• EPİAŞ — Enerji Piyasaları İşletme A.Ş.; yönetmelikteki adıyla Piyasa İşletmecisi",
        "• MEDAS — Merkezi Elektronik Doğrulayıcı Kuruluş Atama Sistemi; İklim Değişikliği "
        "Başkanlığınca kurulur",
        "• TÜRKAK — Türk Akreditasyon Kurumu",
        "",
        "Karbon Piyasası Kurulu, Çevre, Şehircilik ve İklim Değişikliği Bakanı başkanlığında "
        "toplanır; sekretaryasını İklim Değişikliği Başkanlığı yürütür (m. 23/1).",
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
        "",
        "TAHSİSAT TESLİM ETMEMEK",
        "Teslim edilmeyen her tahsisat için, son 3 ayın birincil ve ikincil piyasa ortalama "
        "fiyatlarından yüksek olanının 2 katı idari para cezası (7552 sayılı İklim Kanunu m. 14). "
        "Ceza borcu silmez: eksik miktar ertesi yılın teslim yükümlülüğüne eklenir (m. 16/2).",
    ], "warn"),

    ("p_takvim", IRD_X, sy(6), 440, 420, "ÖRNEK TAKVİM — 2027 SİSTEM YILI", [
        "Her yıl aynı döngü tekrarlanır; tarihler 2027 emisyonları için örnektir.",
        "",
        "• 1 Ocak – 31 Aralık 2027 — emisyon ve faaliyet seviyesi izlenir",
        "• 30 Nisan 2028 — doğrulanmış emisyon ve faaliyet seviyesi raporları; İklim "
        "Değişikliği Başkanlığı en fazla 1 ay uzatabilir (m. 29/1)",
        "• En geç 29 Haziran 2028 — Ulusal Tahsisat Planı yayımlanır: 30 Nisan + 60 gün (m. 11/2)",
        "• Plan + 30 gün, en geç 29 Temmuz 2028 — ücretsiz tahsisat başvurusu (m. 14/2)",
        "• 30 Kasım 2028 — tahsisat teslimi: Kasım'ın son iş günü (m. 16/1)",
        "• 29 Aralık 2028 — ek rezerv kullananlar için teslim: Aralık'ın son iş günü (m. 16/7)",
        "",
        "Plan daha erken yayımlanırsa başvuru süresi de o tarihten itibaren işler.",
    ], "panel"),

    ("p_dikkat", 1730, sy(2) + 20, 250, 420, "SERA GAZI EMİSYON İZNİ NEDİR?", [
        "ETS kapsamındaki bir işletmenin, emisyona yol açan faaliyetini sürdürebilmesi için "
        "İklim Değişikliği Başkanlığından alması zorunlu izindir (m. 4 · m. 6). Tesisin "
        "izlemeyi onaylı plana göre yapacağını ve teslim yükümlülüğünü üstlendiğini gösterir.",
        "BAŞVURU DOSYASI (EK-3)",
        "• İşletme ve tesis bilgileri, hammaddeler",
        "• İzleme planı ve İzleme Metodolojisi Planı",
        "• Yetkili personel belgeleri, başvuru bedeli",
        "SÜREÇ VE SÜRE",
        "• Her tesis için ayrı izin; aynı adresteki tesisler tek izin (m. 7/2)",
        "• Azami 60 günde değerlendirilir; eksikler 3 ayda tamamlanmazsa ret (m. 7)",
        "• 5 yıl geçerli; bitiminden en az 6 ay önce yenileme başvurusu (m. 8)",
        "• Değişiklikler 30 gün içinde bildirilir (m. 9)",
        "İPTAL VE CEZA",
        "• Yanıltıcı beyan, faaliyetin sona ermesi veya teslim yükümlülüğünün yerine "
        "getirilmemesi halinde iptal edilir (m. 10)",
        "• İzinsiz faaliyet cezası 1.254.900 – 12.549.000 ₺ (m. 35)",
        "• Geçiş: 7552 sayılı İklim Kanununun yürürlüğünden itibaren 3 yıl içinde izin "
        "alınmalıdır; bu sürede bir kereye mahsus izinli sayılırsınız. Karbon Piyasası "
        "Kurulu kararıyla İklim Değişikliği Başkanlığı süreyi 2 yıla kadar uzatabilir "
        "(Geçici m. 2).",
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
        "• Motor, değişken hızlı sürücü (VSD) ve basınçlı hava sistemleri verimliliği",
        "• Yakıt dönüşümü ve biyokütle — biyokütlenin emisyon faktörü sıfır kabul edilir (EK-6)",
        "• Elektrifikasyon ile tesis içi yakma emisyonunun azaltılması",
        "• Çatı güneş enerjisi santrali (GES) ve öz tüketim; YEK-G (Yenilenebilir Enerji Kaynak Garanti) belgeli yeşil elektrik tedariki",
        "• ISO 50001 enerji yönetim sistemi kurulumu",
        "• Sayaçlama ve veri altyapısı — izleme, raporlama ve doğrulama yükümlülüğüyle aynı altyapıyı besler",
        "• Fizibilite: geri ödeme ve net bugünkü değer (NBD) hesabına tahsisat maliyetinin dâhil edilmesi",
        "• Verimlilik Artırıcı Proje (VAP) destekleriyle yatırım maliyetinin düşürülmesi",
    ], "opportunity"),

    ("p_ozel", 1580, 620, 542, 230, "ÖZEL DURUMLAR — AYRICA DEĞERLENDİRİLİR", [
        "EK-1 faaliyeti yürütse de aşağıdaki tesisler farklı değerlendirilir. Tesisiniz bu "
        "gruptaysa ayrı bir inceleme yapılmalıdır.",
        "YÖNETMELİK DIŞI",
        "• Araştırma-geliştirme (Ar-Ge) tesis veya bölümleri, münhasıran biyokütle kullanan tesisler, askerî unsurlar (m. 2/2)",
        "ETS DIŞI — İZLEME, RAPORLAMA VE DOĞRULAMA SÜRER",
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
        "Tahsisatlar, İklim Değişikliği Başkanlığınca belirlenen ihale takvimine göre ihaleyle "
        "satılır. Takvim, Ulusal Tahsisat Planının yayımından sonraki 15 iş günü içinde Enerji "
        "Piyasaları İşletme A.Ş. (EPİAŞ) internet sitesinde ilan edilir (m. 17).",
        "İKİNCİL PİYASA — ARZ VE TALEP",
        "Ücretsiz dağıtılan veya ihalede alınan tahsisatların sonradan alınıp satıldığı "
        "piyasadır. Sürekli ticaret yöntemiyle işletilir; fiyat alış ve satış emirlerinin "
        "eşleşmesiyle oluşur (m. 4/1-s · m. 18). Piyasa katılımcıları ETS kapsamındaki "
        "işletmelerdir (m. 4/1-ff).",
        "FİYAT ARALIĞI VE İSTİKRAR",
        "Asgari ve azami tahsisat fiyatı aralıklarını belirlemeye Karbon Piyasası Kurulu "
        "yetkilidir; kararlar İklim Değişikliği Başkanlığının resmî internet sayfasında ilan "
        "edilir. Piyasa istikrar rezervi, dolaşımdaki tahsisat miktarı ve fiyatlar "
        "değerlendirilerek devreye alınır (m. 19 · m. 21/1). Bu fiyat aralıkları ek rezerv ve "
        "tamamlayıcı tahsisat fiyatı mekanizmasına uygulanmaz (m. 21/2).",
        "||",
        "EK REZERV FİYATI",
        "Asgari fiyat: son 3 ayın birincil ve ikincil piyasa ağırlıklı ortalama fiyatlarından "
        "yüksek olanının %50 fazlası. Azami fiyatı İklim Değişikliği Başkanlığı ve Enerji "
        "Piyasası Düzenleme Kurumu koordineli belirler (m. 16/6). İhale yapılmamışsa spot "
        "piyasa fiyatları esas alınır (Geçici m. 5).",
        "TAMAMLAYICI TAHSİSAT FİYATI",
        "İşletmelerin talebi üzerine, İklim Değişikliği Başkanlığının belirlediği ihalelerde "
        "teslim edilecek tahsisatlar için ilave bir birincil piyasa fiyat mekanizması "
        "işletilebilir; başvuru Enerji Piyasaları İşletme A.Ş. aracılığıyla yapılır (m. 20).",
        "KARBON KREDİSİYLE DENKLEŞTİRME",
        "Türkiye sınırları içindeki projelerden elde edilen karbon kredileri, teslim "
        "yükümlülüğünün Karbon Piyasası Kurulunca belirlenen oranını geçmemek üzere "
        "kullanılabilir (m. 25/1).",
        "PİYASANIN İŞLEYİŞİ",
        "İşlem Kayıt Sistemini ve birincil ile ikincil ETS piyasasını Enerji Piyasaları İşletme "
        "A.Ş. (EPİAŞ) işletir. Piyasa işleyişinin usul ve esaslarını Çevre, Şehircilik ve İklim "
        "Değişikliği Bakanlığı, Enerji ve Tabii Kaynaklar Bakanlığı ve Sermaye Piyasası Kurulu ile "
        "koordineli olarak Enerji Piyasası Düzenleme Kurumu belirler. Türkiye Odalar ve Borsalar "
        "Birliği Başkanı başkanlığındaki Danışma Kurulu, Karbon Piyasası Kuruluna sunulmak üzere "
        "istişari kararlar alır (m. 4/1-k · m. 21/3 · m. 22/1 · m. 24).",
    ], "panel"),

    ("p_lejant", 1620, 150, 460, 170, "RENK ANAHTARI", [
        "YEŞİL — yükümlülük yok, sistem hiç uygulanmaz",
        "SARI — yalnızca izleme, raporlama ve doğrulama",
        "KIRMIZI — tam ETS: izin, izleme-raporlama-doğrulama ve tahsisat teslimi",
        "GRİ — yardımcı bilgi, akışın parçası değil",
        "KİM — başvurunun yapıldığı ve işlemi yürüten kurum",
    ], "start"),
]

# ───────────────────── fiyatta kimin rolü ne ─────────────────────
# (kurum, rolü) — fiyat bölümünün üstündeki tek bakışta özet
PRICE_ROLES = [
    ("Karbon Piyasası Kurulu",
     "Çevre, Şehircilik ve İklim Değişikliği Bakanı başkanlığında toplanır. Satışa sunulacak "
     "tahsisat miktarını, asgari–azami fiyat aralığını ve karbon kredisi oranını belirler "
     "(m. 21/1 · m. 23 · m. 25/1)"),
    ("İklim Değişikliği Başkanlığı",
     "İhale takvimini ve istikrar rezervine aktarılacak miktarı belirler, Karbon Piyasası "
     "Kurulu kararlarını ilan eder (m. 17/1 · m. 19/2 · m. 21/1)"),
    ("Enerji Piyasası Düzenleme Kurumu",
     "ETS piyasasının ve İşlem Kayıt Sisteminin usul ve esaslarını belirler "
     "(m. 21/3 · m. 22/5)"),
    ("Enerji Piyasaları İşletme A.Ş.",
     "EPİAŞ, yönetmelikteki adıyla Piyasa İşletmecisi. İhaleleri ve ikincil piyasayı "
     "işletir, İşlem Kayıt Sistemini yürütür (m. 4/1-k · m. 22/1)"),
    ("Piyasa katılımcıları",
     "ETS kapsamındaki işletmeler. Fiyat birincil piyasada ihaleyle, ikincil piyasada alış "
     "ve satış emirleriyle oluşur (m. 4/1-ff · m. 17 · m. 18)"),
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
