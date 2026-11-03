# -*- coding: utf-8 -*-
# İME ön raporu içeriği (KOÜ Teknoloji Fakültesi İME Yönergesi ve Rapor Yazım Kurallarına göre).
# Blok türleri: ('h1',t) bölüm başlığı · ('h2',t) 2. derece · ('h3',t) 3. derece · ('p',t) paragraf
# ('fig',dosya,genişlik_cm,altyazı) · ('tbl',başlık,[sütun_cm],[[satır]])
# Kurallar: şekil ve tablolar sayfanın üstünde (başlıklardan hemen sonra) yer alır; kısaltma ilk geçtiği
# yerde bir kez açıklanır; anlatım üçüncü şahıs; 1. ve 2. derece başlıklarda bağlaçlar küçük harf.

AD = '[Ad SOYAD]'
DONEM = 'GÜZ'
YIL = '2026–2027'

ONSOZ = [
    "Bu rapor, Kocaeli Üniversitesi Teknoloji Fakültesi Enerji Sistemleri Mühendisliği Bölümü "
    "İşletmede Mesleki Eğitim (İME) uygulaması kapsamında, Enerjisa Enerji A.Ş. Müşteri Çözümleri "
    "iş birimine bağlı Enerji Verimliliği ekibinde yürütülen çalışmaların ilk yedi haftasını "
    "(21.09.2026 – 03.11.2026) kapsayan ön rapordur. Ön rapor, sekizinci hafta sonundaki yarıyıl içi "
    "değerlendirme için hazırlanmış olup İME sonunda teslim edilecek esas raporun temelini oluşturmaktadır.",
    "Raporda anlatılan çalışmaların önemli bir bölümü, birimin yürüttüğü gerçek müşteri projeleriyle "
    "ilgilidir. İME Yönergesinin 8. maddesi ve işletmenin gizlilik kuralları gereği müşteri adları, "
    "sözleşme bedelleri, birim fiyatlar ve gerçek tüketim verileri rapora alınmamış; müşteriler "
    "sektörleriyle anılmış (ör. bir beyaz et üretim tesisi), sayısal değerler gerektiğinde yaklaşık "
    "mertebeleriyle verilmiştir. Rapordaki şekiller, İME süresince hazırlanan çıktıların ekran "
    "görüntüleridir ve müşteri bilgisi içermemektedir.",
    "Çalışma döneminin, Türkiye Emisyon Ticaret Sistemi Yönetmeliğinin yayımlanması ve 2026 yılı "
    "yatırım teşvik düzenlemeleriyle aynı zamana denk gelmesi, güncel mevzuatın uygulamaya "
    "dönüştürülmesi konusunda çalışma olanağı sağlamıştır.",
    "İME süresince görevleri planlayan ve çalışmaları yönlendiren İME sorumlusu [Unvan Ad SOYAD]'a "
    "(Enerjisa Enerji A.Ş.), projelerde bilgi ve deneyimlerini paylaşan Enerji Verimliliği ekibine "
    "(Enerjisa Enerji A.Ş.) ve İME sürecini izleyen denetçi öğretim elemanı [Unvan Ad SOYAD]'a "
    "(Kocaeli Üniversitesi) teşekkür edilir.",
]

OZET = [
    "Bu ön rapor, Enerjisa Enerji A.Ş. Müşteri Çözümleri – Enerji Verimliliği biriminde 21.09.2026 – "
    "03.11.2026 tarihleri arasında yürütülen İşletmede Mesleki Eğitim çalışmalarını kapsamaktadır. "
    "Çalışmaların amacı, enerji sistemleri mühendisliği bilgisinin enerji verimliliği hizmetlerinde; "
    "mevzuat analizi, yatırım desteği değerlendirmesi, ön fizibilite ve proje yönetimi süreçlerinde "
    "uygulanmasıdır.",
    "Bu dönemde dört ana konuda çalışılmıştır. Birincisinde Türkiye Emisyon Ticaret Sistemi (TR ETS) "
    "Yönetmeliği incelenmiş, sanayi müşterilerinin kapsam ve kategori durumunu belirleyen bir karar şeması "
    "ve etkileşimli bir karar aracı hazırlanmıştır. İkincisinde 18 destek programını, 81 ilin bölgesel "
    "kurallarını ve 2026 parasal eşiklerini içeren bir veri envanteri ile harita tabanlı bir destek analiz "
    "aracı oluşturulmuştur. Üçüncüsünde, yaklaşık iki haftalık bir çalışmayla sanayi tesislerinde atık ısı "
    "geri kazanımı ön fizibilitesi için şema tabanlı bir veri formu geliştirilmiştir; form dokuz ünite türü "
    "için proses haritaları, ön hesap, Excel çıktısı ve yönetici paneli içermektedir. Dördüncüsünde, bir "
    "beyaz et üretim tesisinde kurulacak biyogaz tesisi projesi için iş birliği, yönetim, risk ve maliyet "
    "sunumları hazırlanmış, reaktör ısıtmasında kullanılacak ısı pompasının çalışma sıcaklıkları incelenmiş "
    "ve tesise saha ziyareti yapılmıştır.",
    "Yöntem olarak mevzuat metinlerinin madde düzeyinde incelenmesi, kural tabloları ve veri envanteri "
    "oluşturulması, ısıl hesaplar (gaz özellikleri, organik Rankine çevrimi (ORC) verimi, ısı depolama, "
    "ısı pompası performansı) ve proje yönetimi araçları kullanılmıştır.",
    "Ara sonuç olarak; karbon fiyatlandırmasının ve devlet desteklerinin enerji verimliliği yatırımlarının "
    "fizibilitesini doğrudan değiştirdiği, müşteriden standart biçimde veri toplanmasının ön fizibilitenin "
    "hızını ve güvenilirliğini artırdığı, ısı pompası gibi uygulamalarda ise ekipmanın çalışma sınırlarının "
    "proje başında doğrulanması gerektiği görülmüştür.",
]

# Alfabetik sıra (Yazım Kuralları 2.9); Yunan harfleri sonda
SIMGELER = [
    ('°C', 'Santigrat derece; sıcaklık'),
    ('cp', 'Özgül ısı, kJ/kgK'),
    ('Hz', 'Hertz; frekans'),
    ('K', 'Kelvin; sıcaklık farkı'),
    ('kV', 'Kilovolt; gerilim'),
    ('kW, MW', 'Kilovat, megavat; güç'),
    ('kWh, MWh, TWh', 'Kilovatsaat, megavatsaat, teravatsaat; enerji'),
    ('kWth', 'Kilovat ısıl güç'),
    ('m³/h', 'Metreküp/saat; hacimsel debi'),
    ('ṁ', 'Kütlesel debi, kg/s'),
    ('MB', 'Megabayt; dosya boyutu'),
    ('mbar, Pa, mmSS', 'Milibar, pascal, milimetre su sütunu; basınç'),
    ('MWp', 'Megavat-pik; güneş panellerinin standart test koşullarındaki gücü'),
    ('Nm³', 'Normal metreküp; 0 °C ve 1 atm koşullarında gaz hacmi'),
    ('P(t)', 'Zamana bağlı ısıl güç, kW'),
    ('Q', 'Isıl güç, kW'),
    ('Sm³', 'Standart metreküp; doğal gaz hacmi'),
    ('T', 'Sıcaklık, °C'),
    ('t CO₂e', 'Ton karbondioksit eşdeğeri'),
    ('V̇', 'Hacimsel debi, m³/h'),
    ('ρ', 'Yoğunluk, kg/m³'),
]

KISALTMALAR = [
    ('AYEDAŞ', 'İstanbul Anadolu Yakası Elektrik Dağıtım A.Ş.'),
    ('AYESAŞ', 'İstanbul Anadolu Yakası Elektrik Perakende Satış A.Ş.'),
    ('BREF', 'Mevcut en iyi teknikler referans belgesi (Best Available Techniques Reference Document)'),
    ('COP', 'Isı pompası veya soğutma grubunun performans katsayısı (Coefficient of Performance)'),
    ('EAO', 'Emre amadelik oranı'),
    ('EDAŞ', 'Elektrik dağıtım anonim şirketi'),
    ('EKA', 'Enerji ve Karbon Azaltım Desteği'),
    ('EPC', 'Tasarım, tedarik ve kurulumun tek sözleşmede verildiği anahtar teslim proje modeli (Engineering, Procurement and Construction)'),
    ('EPS', 'Enerji Performans Sözleşmesi'),
    ('EPSAŞ', 'Elektrik perakende satış anonim şirketi'),
    ('ETS', 'Emisyon Ticaret Sistemi'),
    ('GES', 'Güneş enerjisi santrali'),
    ('HTML', 'Web sayfası biçimlendirme dili (HyperText Markup Language)'),
    ('ID fan', 'Emiş fanı (Induced Draft Fan)'),
    ('İME', 'İşletmede Mesleki Eğitim'),
    ('İRD', 'İzleme, raporlama ve doğrulama'),
    ('İSG', 'İş sağlığı ve güvenliği'),
    ('KOİ', 'Kimyasal oksijen ihtiyacı'),
    ('KOSGEB', 'Küçük ve Orta Ölçekli İşletmeleri Geliştirme ve Destekleme İdaresi Başkanlığı'),
    ('LPG', 'Sıvılaştırılmış petrol gazı (Liquefied Petroleum Gas)'),
    ('m.', 'Madde (mevzuat atıflarında)'),
    ('MEDAS', 'Merkezi Elektronik Doğrulayıcı Kuruluş Atama Sistemi'),
    ('ORC', 'Organik Rankine çevrimi (Organic Rankine Cycle)'),
    ('P&ID', 'Boru ve enstrüman şeması (Piping and Instrumentation Diagram)'),
    ('PDF', 'Taşınabilir belge biçimi (Portable Document Format)'),
    ('PFD', 'Proses akış şeması (Process Flow Diagram)'),
    ('RACI', 'İşi yapan, onaylayan, görüşü alınan, bilgilendirilen (Responsible, Accountable, Consulted, Informed)'),
    ('RDF', 'Atıktan türetilmiş yakıt (Refuse Derived Fuel)'),
    ('SAM', 'Ulaşılabilir pazar (Serviceable Available Market)'),
    ('SCADA', 'Merkezi denetim ve veri toplama sistemi (Supervisory Control and Data Acquisition)'),
    ('SKDM', 'Sınırda Karbon Düzenleme Mekanizması'),
    ('SOM', 'Hedef pazar (Serviceable Obtainable Market)'),
    ('SPO', 'Elektrik üretiminin, kurulu gücün tam yükte üreteceği enerjiye oranı (panel göstergesi)'),
    ('SWOT', 'Güçlü yönler, zayıf yönler, fırsatlar, tehditler'),
    ('TAM', 'Toplam pazar (Total Addressable Market)'),
    ('TL', 'Türk lirası'),
    ('TR ETS', 'Türkiye Emisyon Ticaret Sistemi'),
    ('TSE', 'Türk Standardları Enstitüsü'),
    ('TÜBİTAK', 'Türkiye Bilimsel ve Teknolojik Araştırma Kurumu'),
    ('VAP', 'Verimlilik Artırıcı Proje'),
    ('YEKA', 'Yenilenebilir Enerji Kaynak Alanı'),
    ('YEKDEM', 'Yenilenebilir Enerji Kaynakları Destekleme Mekanizması'),
    ('YKH', 'Yerel Kalkınma Hamlesi'),
]

# ---------------------------------------------------------------- çerçeveli ("Yapılan İş") sayfalar
# bolum: 1..5 (5 = Ekler). Bir çerçeve sayfaya sığmazsa üretici, son blokları "(devam)" sayfasına taşır.
FRAMES = []
def F(id, bolum, title, date, blocks):
    FRAMES.append(dict(id=id, bolum=bolum, title=title, date=date, blocks=blocks))

F('b1', 1, 'Bölüm 1. Giriş', '21.09–03.11.2026', [
    ('h1', 'BÖLÜM 1. GİRİŞ'),
    ('p', "Enerji Sistemleri Mühendisliği; enerjinin üretimi, iletimi, dağıtımı ve verimli kullanımını, "
          "yenilenebilir enerji teknolojilerini, enerji ekonomisini ve enerji mevzuatını birlikte ele alan bir "
          "disiplindir. İME uygulamasının yapıldığı Enerjisa Enerji A.Ş., elektrik dağıtımı ve perakende "
          "satışının yanı sıra Müşteri Çözümleri iş birimi aracılığıyla sanayi ve ticari müşterilere güneş "
          "enerjisi santrali (GES), kojenerasyon ve trijenerasyon, atık ısı geri kazanımı ve enerji verimliliği "
          "projeleri sunmaktadır. Bu nedenle işletme, bölümde alınan termodinamik, ısı transferi, elektrik "
          "tesisleri, yenilenebilir enerji ve enerji ekonomisi derslerinin doğrudan uygulandığı bir çalışma "
          "ortamı sağlamaktadır."),
    ('p', "Konunun önemi, 2026 yılında enerji ve iklim mevzuatında yaşanan değişikliklerle artmıştır. 7552 "
          "sayılı İklim Kanunu'na dayanılarak hazırlanan TR ETS Yönetmeliğinin yayımlanmasıyla belirli "
          "kapasitenin üzerindeki sanayi tesisleri için sera gazı emisyonları bir maliyet kalemine "
          "dönüşmektedir. Aynı dönemde yatırım teşvik sisteminin 9903 sayılı Karar ile yeniden düzenlenmesi ve "
          "verimlilik destek programlarının 2026 tutarlarının güncellenmesi, enerji verimliliği yatırımlarının "
          "fizibilitesini etkileyen yeni bir çerçeve oluşturmuştur."),
    ('p', "İME'den beklentiler; (a) mevzuatın müşteri için anlaşılır ve uygulanabilir araçlara "
          "dönüştürülmesi, (b) enerji verimliliği projelerinin teknik ve ekonomik ön değerlendirmesinde "
          "deneyim kazanılması, (c) gerçek bir yatırım projesinde proje organizasyonu ile sözleşme ve paydaş "
          "yönetiminin gözlemlenmesi ve (d) saha çalışmalarına katılım olarak belirlenmiştir."),
    ('p', "Raporun ikinci bölümünde işletme tanıtılmış, üçüncü bölümünde haftalık çalışmalar tarih sırasıyla "
          "açıklanmış, dördüncü bölümünde ise ilk yedi haftanın ara sonuçları ve öneriler verilmiştir."),
])

F('b2a', 2, 'Bölüm 2. İşletme bilgileri', '21.09–03.11.2026', [
    ('h1', 'BÖLÜM 2. İŞLETME BİLGİLERİ'),
    ('h2', '2.1. İşletmenin Adı, Adresi ve Faaliyet Alanı'),
    ('p', "İME uygulaması, Enerjisa Enerji A.Ş.'nin Müşteri Çözümleri iş birimine bağlı Enerji Verimliliği "
          "ekibinde yapılmaktadır. Şirketin genel müdürlüğü Barbaros Mahallesi, Begonya Sokak, Nida Kule "
          "Ataşehir Batı Sitesi No: 1/1, Ataşehir/İstanbul adresindedir."),
    ('p', "Şirketin faaliyetleri üç iş kolunda toplanmaktadır. Dağıtım iş kolunda Başkent EDAŞ, İstanbul "
          "Anadolu Yakası Elektrik Dağıtım A.Ş. (AYEDAŞ) ve Toroslar EDAŞ, lisanslı bölgelerinde 36 kV altındaki "
          "şebekeler üzerinden elektrik dağıtımı yapmaktadır. Perakende iş kolunda Başkent EPSAŞ, İstanbul "
          "Anadolu Yakası Elektrik Perakende Satış A.Ş. (AYESAŞ) ve Toroslar EPSAŞ bu bölgelerde görevli tedarik "
          "şirketi olarak elektrik satmaktadır. Müşteri Çözümleri iş kolu ise ülke genelinde GES kurulumu, "
          "enerji verimliliği uygulamaları, kojenerasyon, yeşil enerji tedariki ve elektrikli araç şarj "
          "hizmetleri sunmaktadır."),
    ('h2', '2.2. Kısa Tarihçe ve Ortaklık Yapısı'),
    ('p', "1996 yılında kurulan Enerjisa Enerji'nin sermayesinin %40'ı Hacı Ömer Sabancı Holding A.Ş.'ye, "
          "%40'ı E.ON International Participations N.V.'ye aittir; kalan %20 halka açıktır. Şirket hisseleri "
          "8 Şubat 2018'den bu yana Borsa İstanbul'da ENJSA koduyla işlem görmektedir. Elektrikli araç şarj "
          "ağı Eşarj'ın çoğunluk hissesi 2018 yılında satın alınmıştır. Şirketin 2025 Entegre Faaliyet "
          "Raporu'ndan derlenen temel göstergeleri Tablo 2.1'de verilmiştir."),
])

F('b2b', 2, 'Bölüm 2. İşletme bilgileri (devam)', '21.09–03.11.2026', [
    ('tbl', 'Tablo 2.1 Enerjisa Enerji A.Ş. temel göstergeleri (Enerjisa 2025)', [8.0, 6.0], [
        ['Gösterge', 'Değer'],
        ['Dağıtım bölgesi', '3 bölge, 14 il'],
        ['Hizmet verilen nüfus', '22,3 milyon'],
        ['Perakende portföyü', 'yaklaşık 11 milyon müşteri'],
        ['Yıllık elektrik satışı', '47,55 TWh'],
        ['Çalışan sayısı', '10.671'],
        ['Müşteriler için kurulan GES kapasitesi', '146,4 MWp'],
        ['Elektrikli araç şarj soketi', '2.455'],
    ]),
    ('h2', '2.3. Çalışan Sayısı ve Organizasyon'),
    ('p', "2025 yılı sonu itibarıyla şirketin 10.671 çalışanı bulunmaktadır. Bunların 3.992'si beyaz yaka "
          "(mühendis, uzman ve idari personel), 6.679'u mavi yaka (teknisyen ve saha personeli) olarak "
          "sınıflandırılmaktadır. Mavi yaka çalışanlar ağırlıklı olarak dağıtım şebekesinin işletme ve "
          "bakımında görev almaktadır."),
    ('p', "Organizasyon; dağıtım, perakende ve müşteri çözümleri iş birimleri ile bunlara hizmet veren "
          "finans, insan kaynakları, hukuk, bilgi teknolojileri ve satın alma gibi destek fonksiyonlarından "
          "oluşmaktadır. Müşteri Çözümleri iş birimi, kurumsal müşterilere sunulan çözümleri \"İşimin "
          "Enerjisi\" adıyla yürütmektedir. İME'nin yapıldığı Enerji Verimliliği ekibi; müşteri tesislerinde "
          "verimlilik fırsatlarının belirlenmesi, ön fizibilite ve fizibilite çalışmaları, teklif hazırlığı, "
          "proje yönetimi ve devreye alınan santrallerin performans takibi işlerini yürütmektedir."),
])

F('b2c', 2, 'Bölüm 2. İşletme bilgileri (devam)', '21.09–03.11.2026', [
    ('h2', '2.4. Hizmetler, Tedarik Yöntemi ve Hedef Pazar'),
    ('p', "Enerji verimliliği hizmetleri, Enerji Performans Sözleşmesi (EPS) ve performansa dayalı uzun "
          "vadeli satış modelleriyle sunulmaktadır. Bu modellerde yatırım şirket tarafından yapılmakta, "
          "müşteri yatırım bedelini sağlanan tasarruf veya üretilen enerji üzerinden ödemekte, şirket ise "
          "santralin emre amadelik ve performans değerlerini sözleşmeyle garanti etmektedir. Müşteri çözümleri "
          "portföyünde GES'lerin yanı sıra kojenerasyon ve trijenerasyon santralleri bulunmaktadır."),
    ('p', "Şirket bir üretim işletmesi olmadığından hammadde kullanmamaktadır; perakende satışa konu elektrik "
          "enerjisi elektrik piyasasından tedarik edilmektedir. Anahtar teslim (EPC) projelerde şirket ana "
          "yüklenici olarak tasarım, tedarik, kurulum ve devreye alma sorumluluğunu üstlenmekte; ekipman ve "
          "uzmanlık gerektiren saha işleri proje bazında satın alma süreçleriyle tedarikçi ve alt "
          "yüklenicilerden temin edilmektedir."),
    ('p', "Hedef pazar; enerji yoğun sanayi tesisleri, organize sanayi bölgelerindeki orta ölçekli "
          "işletmeler, hastane ve üniversite gibi kampüsler ile alışveriş merkezi ve otel gibi ticari "
          "binalardır. Müşteri çözümleri hizmetleri dağıtım bölgeleriyle sınırlı olmayıp ülke genelinde "
          "sunulmaktadır."),
])

# ---------------- Bölüm 3
F('w1a', 3, '3.1.1. Oryantasyon ve birimin tanınması', '21.09.2026', [
    ('h1', 'BÖLÜM 3. YAPILAN ÇALIŞMALAR'),
    ('p', "Bu bölümde İME süresince yapılan çalışmalar hafta hafta ve tarih sırasıyla verilmiştir. Alt "
          "başlıklar, haftalık çalışma tablolarındaki sayfa numaralarıyla eşleşmektedir."),
    ('h2', '3.1. Birinci Hafta (21.09.2026 – 25.09.2026)'),
    ('h3', '3.1.1. Oryantasyon ve birimin tanınması'),
    ('p', "İME'nin ilk gününde kurum içi giriş işlemleri tamamlanmış, çalışma bilgisayarı teslim alınmış ve "
          "kurumsal sistemlere erişim tanımlanmıştır. Ofiste bulunan ekip üyeleriyle tanışılmış, Enerji "
          "Verimliliği ekibinin görev alanları ve çalışma düzeni hakkında bilgi alınmıştır."),
    ('p', "Gün genel olarak oryantasyon şeklinde geçmiştir. Sonraki haftalarda yararlanılmak üzere birimde "
          "kullanılan yazılım ve platformlar, müşteri portföyünün yapısı, saha ziyaretlerine katılım olanağı "
          "ve İME süresince üstlenilecek somut işler gibi konular not edilmiştir."),
])

F('w1b', 3, '3.1.2. TR ETS Yönetmeliğinin incelenmesi', '22.09.2026', [
    ('h3', '3.1.2. TR ETS Yönetmeliğinin incelenmesi'),
    ('tbl', 'Tablo 3.1 TR ETS tesis kategorileri', [3.0, 5.5, 5.5], [
        ['Kategori', 'Yıllık emisyon (t CO₂e)', 'Yükümlülük'],
        ['A', '≤ 50.000', 'Yalnızca İRD'],
        ['B', '50.001 – 500.000', 'ETS ve İRD'],
        ['C', '> 500.000', 'ETS ve İRD'],
    ]),
    ('p', "27.08.2026 tarihli ve 33353 sayılı Resmî Gazete'de yayımlanan TR ETS Yönetmeliği ile EK-1 – EK-7 "
          "ekleri, birimin sanayi müşterilerine yapacağı bilgilendirmelere temel oluşturmak amacıyla madde "
          "madde incelenmiştir."),
    ('p', "Kapsam, EK-1'deki faaliyet listesine bağlıdır. Listede enerji, metal, mineral, selüloz-kâğıt ve "
          "kimya gruplarında 25 faaliyet bulunmakta ve eşikler üretim kapasitesine göre tanımlanmaktadır. "
          "Yakma faaliyetinde tesisteki tüm yakma ünitelerinin anma ısıl güçleri toplanmakta; 3 MW altındaki "
          "üniteler ile münhasıran biyokütle kullanan üniteler toplama katılmamaktadır. Bir EK-1 faaliyetini "
          "yürüten işletmenin diğer EK-1 faaliyetleri ise kapasiteye bakılmaksızın kapsama girmektedir "
          "(m. 27/2)."),
    ('p', "Kapsamdaki tesisler, kurulu kapasiteye göre ihtiyatlı biçimde hesaplanan yıllık emisyonlarına göre "
          "üç kategoriye ayrılmaktadır (Tablo 3.1). ETS yükümlülükleri yalnızca B ve C kategorilerini "
          "kapsamakta, A kategorisindeki tesisler ise yalnızca izleme, raporlama ve doğrulama (İRD) yükümlüsü "
          "olmaktadır (m. 5/1)."),
    ('p', "Ar-Ge tesisleri, münhasıran biyokütle kullanan tesisler ve askerî unsurlar kapsam dışındadır "
          "(m. 2/2). Okul, üniversite, hastane ve savunma sanayi tesisleri ETS dışında tutulmakla birlikte İRD "
          "yükümlülükleri sürmektedir (m. 5/2-3). Doğal gaz ve ham petrol iletimi ile depolanması ise birinci "
          "uygulama dönemi sonuna kadar geçici olarak ETS dışındadır (Geçici m. 6)."),
])

F('w1c', 3, '3.1.3. Yükümlülük süreci ve kapsam şeması', '22.09.2026', [
    ('h3', '3.1.3. Yükümlülük süreci ve kapsam şeması'),
    ('fig', 'fig_ets_agac.png', 13.8, 'Şekil 3.1 TR ETS kapsam belirleme şemasının karar adımları'),
    ('p', "Yönetmelikteki yükümlülükler, bir işletmenin izlemesi gereken sırayla çıkarılmıştır: sera gazı "
          "emisyon izni başvurusu (m. 6-8, EK-3; izin beş yıl geçerlidir), izlemenin başlamasından en az altı "
          "ay önce sunulan izleme planı (m. 28/3), yıllık izleme, Merkezi Elektronik Doğrulayıcı Kuruluş Atama "
          "Sistemi (MEDAS) üzerinden atanan ve ISO/IEC 17029'a göre akredite doğrulayıcı kuruluşa doğrulatma "
          "(m. 30, m. 33/2), 30 Nisan'a kadar raporlama (m. 29), Ulusal Tahsisat Planının yayımlanmasından "
          "sonra 30 gün içinde ücretsiz tahsisat başvurusu (m. 14/2) ve kasım ayının son iş gününe kadar "
          "tahsisat teslimi (m. 16/1)."),
    ('p', "Emisyon, faaliyet verisi, emisyon faktörü ve oksidasyon faktörünün çarpımıyla hesaplanmakta "
          "(EK-6), biyokütlenin emisyon faktörü sıfır kabul edilmektedir. Ücretsiz tahsisat ise kıyas değeri, "
          "ücretsiz tahsisat oranı, sektörel faaliyet katsayısı ve faaliyet seviyesinin çarpımıdır (m. 13/7). "
          "Bu formül, enerji verimliliği önlemleriyle faaliyet seviyesi düşen alt tesislerde ücretsiz "
          "tahsisatın da azalacağını göstermektedir."),
    ('p', "İncelenen hükümleri müşteriye anlatabilmek için evet/hayır mantığıyla ilerleyen bir kapsam "
          "belirleme şeması hazırlanmıştır (Şekil 3.1). Şemanın ilk sürümünde izleme planının izin "
          "başvurusundan sonra gösterilmesi (oysa EK-3 uyarınca başvurunun ekidir), yıllık döngünün kapalı "
          "çevrim olarak gösterilmemesi ve kalıcı istisna ile geçici istisnanın aynı düğümde birleştirilmesi "
          "gibi hatalar tespit edilerek düzeltilmiştir."),
])

F('w1d', 3, '3.1.4. Şemanın sadeleştirilmesi ve karar aracı', '23–24.09.2026', [
    ('h3', '3.1.4. Şemanın sadeleştirilmesi ve karar aracı'),
    ('fig', 'fig_ets_arac.png', 12.5, 'Şekil 3.2 ETS kapsam karar aracı (örnek tesis verisiyle)'),
    ('p', "Şemanın müşteri sunumlarında kullanılabilmesi için karar akışındaki dört soru ikiye indirilmiştir: "
          "tesiste bir EK-1 faaliyeti yürütülüp yürütülmediği ve kurulu kapasiteye göre yıllık emisyonun kaç "
          "ton CO₂e olduğu. Müşteri portföyünde nadir görülen istisnalar akıştan çıkarılarak \"Özel durumlar\" "
          "başlıklı yan nota taşınmıştır. Her yükümlülük adımına başvurunun nereye yapıldığını ve işlemi hangi "
          "kurumun yürüttüğünü gösteren bir satır eklenmiş; \"Başkanlık\", \"Kurul\" gibi kısa atıflar "
          "yönetmeliğin 4. maddesindeki tanımlara göre kurumların tam adlarıyla yazılmıştır."),
    ('p', "24.09.2026 tarihinde şemanın etkileşimli sürümü olan ETS kapsam karar aracı hazırlanmıştır "
          "(Şekil 3.2). Kullanıcı üç adımda faaliyet türünü, yakma ünitelerini ve özel durumları girmekte; araç "
          "toplam anma ısıl gücünü, kapasiteye göre emisyonu, kategoriyi, yükümlülük adımlarını, rapor ve "
          "tahsisat teslim tarihlerini ve geç raporlama cezasını hesaplamaktadır. Yakıt listesine atıktan "
          "türetilmiş yakıt (RDF) eklenmiş, proses emisyonu kapasiteden otomatik hesaplanacak şekilde "
          "düzenlenmiştir. Her değerin niteliği \"örnek\", \"varsayım\", \"hesaplanan\", \"ilan edilmedi\" ve "
          "\"mevzuat dışı\" etiketleriyle gösterilmiştir."),
])

F('w1e', 3, '3.1.5. Enerji portföy yönetim paneli', '23–24.09.2026', [
    ('h3', '3.1.5. Enerji portföy yönetim paneli'),
    ('fig', 'fig_panel.png', 10.5, 'Şekil 3.3 Enerji portföy yönetim paneli, verimlilik sekmesi (örnek verilerle)'),
    ('p', "Birim direktörünün GES ve enerji verimliliği santrallerinden oluşan portföyü tek ekrandan "
          "izleyebilmesi için bir enerji portföy yönetim paneli tasarlanmıştır (Şekil 3.3). Panel \"GES "
          "Üretim\" ve \"Verimlilik\" sekmelerinden oluşmakta; her sekmede portföy durum özeti, il bazında "
          "portföy haritası, gerçekleşen ve beklenen üretimi karşılaştıran grafik ve santral bazında alarm ve "
          "kayıp listesi bulunmaktadır."),
    ('p', "Santral performansı iki göstergeyle izlenmektedir: emre amadelik oranı (EAO), çalışma süresinin "
          "dönem süresine oranıdır; SPO ise elektrik üretiminin, kurulu gücün dönem boyunca tam yükte "
          "üreteceği enerjiye oranıdır. Göstergeler kurulu güçle ağırlıklandırılarak sözleşmedeki garanti "
          "değerleriyle karşılaştırılmakta ve santraller \"garanti üstü\", \"sınırda\" ve \"garanti altı\" "
          "olarak renklendirilmektedir. Verimlilik sekmesinde elektrik, buhar ve doğal gaz tasarrufu, aynı "
          "enerjinin ayrı üretimine göre; şebeke verimi %52,5, kazan verimi %90, soğutma grubunun performans "
          "katsayısı (COP) 5 ve doğal gazın ısıl değeri 9,59 kWh/Sm³ kabulleriyle hesaplanmaktadır. 24.09.2026 "
          "tarihinde panelin yenilenen sürümü için önceki ve sonraki ekran görüntülerini, değişiklik listesini "
          "ve varsayımları içeren bir değişiklik raporu hazırlanmıştır."),
])

F('w1f', 3, '3.1.6. İş planı taslağı şablonu', '24.09.2026', [
    ('h3', '3.1.6. İş planı taslağı şablonu'),
    ('p', "Birimde yeni hizmet ve proje fikirlerinin yönetime aynı biçimde sunulabilmesi için kurumsal sunum "
          "şablonuyla yedi slaytlık, doldurulabilir bir iş planı taslağı hazırlanmıştır."),
    ('p', "Şablonun ilk bölümünde amaç ve hedefler yer almaktadır: tek ve ölçülebilir bir amaç cümlesi, "
          "\"neden şimdi\" sorusuna mevzuat, pazar ve kurum yetkinliği açısından yanıt ile müşteri sayısı, "
          "yıllık gelir ve pazar payı hedefleri. Ardından güçlü ve zayıf yönler, fırsatlar ve tehditler (SWOT) "
          "analizi ile olasılık–etki matrisi üzerinde konumlandırılan riskler ve her risk için azaltma adımları "
          "gelmektedir."),
    ('p', "Sonraki bölümlerde müşteri segmentleri (büyük sanayi tesisleri, organize sanayi bölgelerindeki orta "
          "ölçekli işletmeler, kamu binaları ve hastaneler, ticari binalar) her segment için profil, ihtiyaç, "
          "değer önerisi ve öncelikle; pazar büyüklüğü toplam pazar (TAM), ulaşılabilir pazar (SAM) ve hedef "
          "pazar (SOM) hesabıyla; son bölümde ise dört fazlı yol haritası ve yönetimden istenen karar "
          "verilmektedir."),
    ('p', "Şablon görselleri slaytlara normal görünümde düzenlenebilecek biçimde yerleştirilmiş, içerik "
          "tıklamayla sırayla açılacak şekilde animasyonlarla hazırlanmıştır. Şablonun amacı, farklı kişilerin "
          "hazırladığı iş planlarının aynı sorulara yanıt vermesini ve birbiriyle karşılaştırılabilmesini "
          "sağlamaktır."),
])

F('w1g', 3, '3.1.7. Biyogaz projesi iş birliği sunumu', '25.09.2026', [
    ('h3', '3.1.7. Biyogaz projesi iş birliği sunumu'),
    ('fig', 'fig_raci.png', 12.5, 'Şekil 3.4 İş paketleri için RACI sorumluluk matrisi'),
    ('p', "Bir beyaz et üretim tesisinde kurulacak biyogaz tesisi projesi için müşteriye sunulacak bir iş "
          "birliği sunumu hazırlanmıştır. Projede Enerjisa, EPC modeliyle ana yüklenici olarak tasarım, "
          "tedarik, kurulum ve devreye almayı tek sözleşmeyle üstlenmekte; uzmanlık gerektiren saha işleri ise "
          "müşteri sözleşmesiyle uyumlu alt sözleşmelerle alt yüklenicilere verilmektedir."),
    ('p', "Organizasyon modelinde müşteri ve Enerjisa yöneticilerinden oluşan bir yönlendirme komitesi ile "
          "müşteriye tek muhatap olan bir proje müdürü tanımlanmış; mühendislik, planlama, kalite ve iş "
          "sağlığı ve güvenliği (İSG) ile satın alma fonksiyonları proje müdürüne bağlanmıştır. Proje; proje "
          "yönetimi ve mühendislik, tedarik, inşaat, mekanik montaj, elektrik ve otomasyon ile test, devreye "
          "alma ve kabul olmak üzere altı iş paketine ayrılmış ve her paket için kapsam, sınır noktaları ve "
          "teslimatlar tanımlanmıştır. Sorumluluklar; işi yapan, onaylayan, görüşü alınan ve bilgilendirilen "
          "tarafları gösteren sorumluluk matrisiyle (RACI) verilmiştir (Şekil 3.4). Alt yükleniciler "
          "arasındaki ekipman kaidesi, motor–pano bağlantısı ve sinyal listesi gibi arayüzler bir kayıt "
          "listesinde izlenmekte; her arayüzün bir sorumlusu ve kapanış tarihi bulunmaktadır."),
])

F('w1h', 3, '3.1.8. Genel müdür sunumu', '25.09.2026', [
    ('h3', '3.1.8. Genel müdür sunumu'),
    ('p', "Aynı proje için müşterinin genel müdürüne yapılacak sunum hazırlanmış ve geri bildirimlere göre "
          "birkaç kez revize edilmiştir. Sunumun ilk bölümünde müşterinin sorumlulukları sıralanmıştır: "
          "sözleşme ve detay mühendislik çıktılarının onayı, inşaat ruhsatı ve izinler, zemin ve temel "
          "imalatları, elektrik ve sıcak su/buhar besleme noktalarının hazırlanması, entegrasyon için "
          "kazanların planlı olarak durdurulması ve performans testi ile kabullere katılım."),
    ('p', "İkinci bölümde alt yükleniciler ve kapsamları verilmiştir. Mühendislik alt yüklenicisi kütle ve "
          "enerji dengesi hesaplarını, reaktör tasarımını (hacim, boyut, malzeme), zemin etüdünü, temel ve "
          "statik hesapları, proses akış şeması (PFD) ile boru ve enstrüman şemasını (P&ID), elektrik tek hat "
          "şemasını, otomasyon mimarisini ve teknik şartnameleri hazırlamaktadır. Mekanik alt yüklenici reaktör, "
          "boru hattı ve ekipman montajını; elektrik ve otomasyon alt yüklenicisi ise montaj ve devreye alma "
          "işlerini üstlenmektedir."),
    ('p', "Üçüncü bölümde proje takvimi ve kritik tarihler gösterilmiştir. Takvimde yaklaşık 37 iş günü süren "
          "detay mühendislik, on bir paket hâlinde ekipman satın alma ve imalat, müşterinin ruhsat ve temel "
          "işlerinden sonra yapılacak saha teslimi, yaklaşık 120 iş günü süren mekanik montaj, elektrik ve "
          "otomasyon montajı ile devreye alma birbirine bağlı iş kalemleri olarak sıralanmıştır. Revizyonlarda "
          "tüm metinler okunabilirlik için tek yazı tipine geçirilmiş, taşmalar giderilmiş ve kazan alt "
          "yüklenicisi için ayrı bir kart eklenmiştir."),
])

F('w2a', 3, '3.2.1. Enerji yatırımı destekleri veri envanteri', '28.09.2026', [
    ('h2', '3.2. İkinci Hafta (28.09.2026 – 02.10.2026)'),
    ('h3', '3.2.1. Enerji yatırımı destekleri veri envanteri'),
    ('p', "Müşterilerin enerji yatırımlarında yararlanabileceği devlet desteklerinin tek kaynaktan "
          "izlenebilmesi için 16 sayfalık bir veri envanteri (Excel) oluşturulmuştur. Envanterde 18 program yer "
          "almaktadır: 9903 sayılı Karar kapsamındaki Teknoloji Hamlesi, Yerel Kalkınma Hamlesi (YKH), "
          "Stratejik Hamle, Öncelikli ve Hedef Yatırımlar ile bölgesel teşvikler; Yeşil Dönüşüm Programı; "
          "Enerji ve Tabii Kaynaklar Bakanlığının Verimlilik Artırıcı Proje (VAP), EPS ve Enerji ve Karbon "
          "Azaltım (EKA) destekleri; Küçük ve Orta Ölçekli İşletmeleri Geliştirme ve Destekleme İdaresi "
          "Başkanlığı (KOSGEB) programları; Türkiye Bilimsel ve Teknolojik Araştırma Kurumu (TÜBİTAK) 1832 "
          "programı; HIT-30; Yenilenebilir Enerji Kaynakları Destekleme Mekanizması (YEKDEM); lisanssız "
          "üretim; Yenilenebilir Enerji Kaynak Alanı (YEKA) 2026 yarışmaları ve kalkınma ajansı programları."),
    ('p', "Envanterin sayfaları; programlar, destek unsurları, uygunluk kuralları, yatırım türü matrisi ve "
          "gerekçeleri, bölgesel kurallar, 81 ilin teşvik bölgesi ve YKH konuları, desteklerin birlikte "
          "kullanımı, 2026 parasal eşikleri, YEKDEM fiyatları, gümrük muafiyeti listesi, başvuru takvimi, "
          "kaynaklar ve teyit listesinden oluşmaktadır. Parasal eşikler 2026 yılı için %25,49 yeniden "
          "değerleme oranıyla güncellenmiş; örneğin VAP hibe üst limiti 27.092.663 TL, EKA üst limiti "
          "18.061.775 TL olarak hesaplanmıştır. Her satırda ilgili madde numarası ve resmî kaynak belirtilmiş, "
          "kesinleşmemiş bilgiler teyit listesine alınmıştır."),
    ('p', "Envanterde, dağıtım şirketlerinin kendi bölgelerinde lisanssız üretim başvurusu yapamaması "
          "(m. 37/10) gibi şirketin hizmet modelini doğrudan etkileyen kısıtlar ayrıca işaretlenmiştir."),
])

F('w2b', 3, '3.2.2. Destek analiz aracı ve harita', '28.09.2026', [
    ('h3', '3.2.2. Destek analiz aracı ve harita'),
    ('fig', 'fig_destek.png', 12.5, 'Şekil 3.5 Enerji yatırımı destek analiz aracı (örnek senaryo: 1 MW çatı GES)'),
    ('p', "Envanterdeki veriler bir Python betiğiyle okunarak tarayıcıda çalışan, kurulum gerektirmeyen bir "
          "destek analiz aracına aktarılmıştır; araç envanter güncellendiğinde yeniden üretilebilmektedir. "
          "Kullanıcı sırasıyla konumu (il, ilçe, organize sanayi bölgesi), işletme bilgilerini ve yatırım "
          "türünü (çatı GES, atık ısı, kojenerasyon, tesis içi batarya depolama, ısı pompası, biyokütle vb.) "
          "girmekte; araç her program için \"uygun\", \"koşullu\" veya \"uygun değil\" sonucunu madde "
          "numarası ve 2026 tutarıyla vermektedir (Şekil 3.5)."),
    ('p', "Harita dört katmandan oluşmaktadır: teşvik bölgeleri, geçici 6. bölge uygulaması, enerji konulu "
          "YKH yatırım konuları ve Enerjisa dağıtım bölgeleri. AYEDAŞ yalnızca İstanbul'un Anadolu yakasına "
          "hizmet verdiğinden dağıtım katmanında İstanbul, Anadolu ve Avrupa yakası olarak ikiye ayrılmıştır. "
          "Harita geometrisinde Anadolu yakasının eksik olduğu ve İstanbul ile Kocaeli arasında boşluk "
          "göründüğü tespit edilmiş, İstanbul sınırı iki parçalı olarak yeniden oluşturulmuştur. Araçta ayrıca "
          "il kartı, iki ilin karşılaştırması, açık çağrılar ve kalkınma ajansı iletişim bilgileri bulunmaktadır."),
])

F('w2c', 3, '3.2.3. Aracın tanıtımı ve ETS–SKDM değerlendirmesi', '29.09.2026', [
    ('h3', '3.2.3. Aracın tanıtımı ve ETS–SKDM değerlendirmesi'),
    ('p', "Destek aracı, birim yöneticilerine kısa bir bilgilendirme e-postasıyla tanıtılmıştır. E-postada "
          "yatırım türü ve ile göre uygun programlar, şartlar ve 2026 tutarları, uygunluk kontrolleri, harita "
          "katmanları, il kartı ve resmî kaynaklar madde madde özetlenmiştir."),
    ('p', "Aynı gün demir-çelik sektöründe elektrifikasyonun (ör. elektrik ark ocağına geçiş) TR ETS ve Avrupa "
          "Birliği Sınırda Karbon Düzenleme Mekanizması (SKDM) yükümlülüklerine etkisi değerlendirilmiştir. "
          "ETS kapsamı faaliyete ve kapasiteye bağlıdır; saatte 2,5 tonun üzerindeki pik demir veya çelik "
          "üretimi kapsamdadır ve kullanılan enerjinin türü kapsamı değiştirmemektedir. Tüketilen elektriğin "
          "emisyonu ise dolaylı sayılmakta ve elektriği üreten santrale yazılmaktadır; bu nedenle "
          "elektrifikasyon, tesisin doğrudan emisyonunu ve teslim etmesi gereken tahsisat miktarını "
          "azaltmaktadır."),
    ('p', "SKDM'de demir-çelik ürünleri üretim yönteminden bağımsız olarak kapsamdadır ve bu sektörde şimdilik "
          "yalnızca doğrudan emisyonlar hesaba katılmaktadır. Elektrifiye üretimde ürüne gömülü emisyon ve SKDM "
          "maliyeti düşmekte, ancak beyan yükümlülüğü sürmektedir; Türkiye'de fiilen ödenen karbon bedeli SKDM "
          "yükümlülüğünden düşülebilmektedir. Yalnızca 20 MW toplam anma ısıl gücü eşiğiyle kapsama giren "
          "sektörlerde elektrifikasyonla eşiğin altına inilmesi kapsam dışına çıkmayı sağlayabilir; demir-çelik "
          "bu gruba girmemektedir."),
    ('p', "Değerlendirme, elektrifikasyonun bir muafiyet değil maliyet azaltımı sağladığını ve bu farkın "
          "müşteriye açıkça anlatılması gerektiğini göstermiştir."),
])

F('w2d', 3, '3.2.4. Biyogaz projesi risk değerlendirme sunumu', '28.09–02.10.2026', [
    ('h3', '3.2.4. Biyogaz projesi risk değerlendirme sunumu'),
    ('p', "Biyogaz tesisi projesi için müşteriye sunulacak risk değerlendirme sunumu üzerinde çalışılmıştır. "
          "Sunumda proje riskleri kategorilere ayrılmış ve proje takvimindeki ilgili aşamalarla "
          "ilişkilendirilmiştir; kategori ve takvim slaytları yeniden düzenlenmiştir. 30.09 ve 01.10.2026 "
          "tarihlerinde sunum üzerindeki çalışmaya devam edilmiştir."),
    ('p', "02.10.2026 tarihinde sunumun son hâli hazırlanmıştır. Sunum dosyasının boyutu 12,6 MB olduğundan "
          "e-postayla gönderilmesi güçtü. Dosyada kullanılmayan 14 slayt yerleşimi ve 16 gömülü görsel "
          "kaldırılarak boyut, slaytların görünümü değiştirilmeden 0,62 MB'a düşürülmüştür. Düzenlemeden sonra "
          "slaytlar önceki sürümle sayfa sayfa karşılaştırılarak görünümün korunduğu kontrol edilmiştir."),
])

# ---- 3. ve 4. hafta: atık ısı geri kazanımı ön fizibilite veri formu (≈ 2 hafta)
F('w3a', 3, '3.3.1. Ön fizibilite veri formunun amacı ve kapsamı', '05–07.10.2026', [
    ('h2', '3.3. Üçüncü Hafta (05.10.2026 – 09.10.2026)'),
    ('h3', '3.3.1. Ön fizibilite veri formunun amacı ve kapsamı'),
    ('p', "Üçüncü ve dördüncü haftalarda birimin atık ısı geri kazanımı projelerinde kullanılmak üzere bir ön "
          "fizibilite veri formu geliştirilmiştir. Formun amacı, müşteri tesisindeki atık ısı potansiyelinin ön "
          "değerlendirmesi için gereken verilerin eksiksiz, aynı biçimde ve doğru birimlerle toplanmasıdır. "
          "Birimde Excel taslakları üzerinden yürütülen bu süreç, müşterinin doğrudan doldurabileceği ve her "
          "sorunun ne istendiğini açıkladığı bir forma dönüştürülmüştür; formdaki hesaplar birimin mevcut hesap "
          "taslaklarıyla aynı tutulmuştur."),
    ('p', "Formun kapsamı, ORC ile atık ısıdan elektrik üretimine uygun başlıca ısı kaynaklarına göre "
          "belirlenmiştir: demir-çelik tesislerinde tav fırını ve elektrik ark ocağı, çimento fırını (ön "
          "ısıtıcı gazı ve klinker soğutucu), alüminyum ergitme fırını, genel amaçlı fırınlar ve kazanlar. "
          "Bunlara biyogaz tesisi, proses ısı pompası ve mahal ısıtma ısı pompası üniteleri ile meyve suyu, "
          "süt ve peynir, dondurma ve tavuk entegre tesisleri için biyogaz sektör formları eklenmiştir. Bir "
          "tesiste aynı türden birden fazla ünite (ör. iki tav fırını) ayrı ayrı tanımlanabilmektedir."),
    ('p', "Form tek bir HTML dosyasıdır; kurulum ve internet bağlantısı gerektirmeden tarayıcıda çalışmaktadır. "
          "Girilen yanıtlar herhangi bir sunucuya gönderilmeden kullanıcının bilgisayarında saklanmakta, "
          "paylaşım Excel dosyasıyla yapılmaktadır. Form; başlangıç, firma ve iletişim, ünite sayfaları, saha "
          "ve yerleşim, belgeler ve fotoğraflar ile özet ve gönderim adımlarından oluşmakta ve her adımda "
          "yanıtlanan temel soruların oranı gösterilmektedir."),
])

F('w3b', 3, '3.3.2. Şema tabanlı form yapısı', '07–09.10.2026', [
    ('h3', '3.3.2. Şema tabanlı form yapısı'),
    ('p', "Formdaki tüm sorular tek bir şema dosyasında tanımlanmıştır. Aynı şemadan HTML formu, dolu Excel "
          "çıktısı ve müşterinin isterse Excel üzerinde doldurabileceği boş şablon üretilmektedir. Böylece bir "
          "soru eklendiğinde veya değiştirildiğinde üç çıktı birlikte güncellenmekte ve aralarında tutarsızlık "
          "oluşmamaktadır. Şemada yaklaşık 250 soru bulunmaktadır."),
    ('p', "Her soru için yanıt türü (metin, sayı, iki değer, seçenek, çoklu seçim, evet/hayır), birim, uyarı "
          "aralığı, açıklama metni ve önem düzeyi tanımlanmıştır. Temel sorular ilerleme oranına girmekte; "
          "örneğin tav fırını sayfasında 16, ark ocağı sayfasında 18 temel soru bulunmaktadır. Debi için Nm³/h, "
          "gerçek m³/h ve kg/h, basınç için Pa, mmSS ve mbar birimleri seçilebilmekte; gerçek debi, gaz "
          "sıcaklığı kullanılarak normal debiye çevrilmektedir. Sorular önceki yanıtlara göre açılıp "
          "kapanmakta, gizlenen bir sorunun eski değeri hesaba katılmamaktadır."),
    ('p', "Fanlar için yalnızca etiket değeri değil fiili çalışma noktası istenmektedir: çekilen güçle birlikte "
          "debi kontrol şekli sorulmakta, frekans sürücüsü seçilirse ortalama frekans (Hz), damper seçilirse "
          "ortalama damper açıklığı (%) girilmektedir. Bu bilgi, mevcut fanların atık ısı eşanjörünün "
          "getireceği ek basınç kaybını karşılayıp karşılayamayacağının değerlendirilmesine yardımcı "
          "olmaktadır."),
])

F('w3c', 3, '3.3.3. Proses haritaları ve ölçüm noktaları', '07–09.10.2026', [
    ('h3', '3.3.3. Proses haritaları ve ölçüm noktaları'),
    ('fig', 'fig_onfiz_tav.png', 12.5, 'Şekil 3.6 Ön fizibilite veri formunda tav fırını proses haritası ve ölçüm noktaları'),
    ('p', "Her ünite türü için seçimlere göre canlı olarak yeniden çizilen bir proses şeması hazırlanmıştır "
          "(Şekil 3.6). Şemalarda birimin taslak çizimleriyle aynı renk dili kullanılmıştır: mavi hava, altın "
          "rengi doğal gaz, yeşil malzeme hattını göstermekte, sıcak gaz hatları ise 20–1200 °C ölçeğinde "
          "sıcaklığa göre renklendirilmektedir. Ölçüm noktaları numaralı balonlarla gösterilmekte ve bu "
          "numaralar Excel çıktısındaki sıra numaralarıyla aynıdır. Kullanıcı bir soruya geldiğinde şemadaki "
          "ilgili nokta vurgulanmakta, girilen değer şemada numaranın yanına yazılmaktadır."),
    ('p', "Şemalar tesisteki düzene göre değişmektedir. Tav fırınında yanma havası ön ısıtma sistemi "
          "(reküperatör, rejeneratif brülör veya ön ısıtma yok) ve baca hattında ekonomizer bulunup "
          "bulunmadığı; ark ocağında ana gaz hattının soğutma şekli; çimento fırınında klinker soğutucunun "
          "tipi; alüminyum fırınında oksijenle yakma kullanılıp kullanılmadığı, şemayı ve sorulan ölçüm "
          "noktalarını belirlemektedir. Şemanın yanında, girilen verilerle hesaplanan geri kazanılabilir ısı "
          "ön göstergesi (kWth) yer almaktadır."),
])

F('w4a', 3, '3.4.1. Ön hesap yöntemi', '12–16.10.2026', [
    ('h2', '3.4. Dördüncü Hafta (12.10.2026 – 16.10.2026)'),
    ('h3', '3.4.1. Ön hesap yöntemi'),
    ('p', "Formdaki ön hesap, girilen verilerle tesisin atık ısı potansiyeline ilişkin bilgi amaçlı bir "
          "gösterge üretmektedir. Hesapta birimin Excel taslaklarındaki bağıntılar kullanılmış, Excel "
          "çıktısındaki \"Ön Hesap\" sayfası aynı hesabı formüllerle yapacak şekilde düzenlenmiştir. Gaz "
          "yoğunluğu ρ = 1,29·273/(T + 273), kütlesel debi ṁ = V̇·ρ/3600 ve baca gazının özgül ısısı "
          "cp(T) = 4,1868·(−10⁻⁸·T² + 8·10⁻⁵·T + 0,2478) bağıntılarıyla hesaplanmaktadır."),
    ('p', "Geri kazanılabilir ısıl güç Q = ṁ·cp(Tort)·(Tgiriş − Tsınır) bağıntısıyla bulunmaktadır. Burada "
          "Tsınır, gazın asit çiy noktası ve mevcut proses ihtiyaçları dikkate alınarak soğutulabileceği en "
          "düşük sıcaklıktır: tav fırınında reküperatör sonrası 150 °C, doğal gaz ve sıvılaştırılmış petrol "
          "gazı (LPG) yakan kazanlarda 120 °C, fuel-oil ve kömürde 150 °C, çimento ön ısıtıcı gazında kurutma "
          "ihtiyacına göre 180–230 °C, klinker soğutucu havasında 150 °C alınmıştır. Baca gazı debisi "
          "bilinmiyorsa doğal gaz tüketimi ve baca gazındaki O₂ ölçümünden tahmin edilmektedir."),
])

F('w4b', 3, '3.4.2. ORC verim eğrisi ve yıllık sonuçlar', '12–16.10.2026', [
    ('h3', '3.4.2. ORC verim eğrisi ve yıllık sonuçlar'),
    ('tbl', 'Tablo 3.2 Ön hesapta kullanılan başlıca varsayımlar', [8.5, 5.5], [
        ['Varsayım', 'Değer'],
        ['ORC net elektrik verimi, kaynak 400 °C ve üzeri', '%18 – %22'],
        ['ORC net elektrik verimi, kaynak 250 °C', '%12 – %15'],
        ['Tav fırını reküperatör sonrası soğutma sınırı', '150 °C'],
        ['Doğal gaz / LPG baca gazı alt sınırı', '120 °C'],
        ['Yıllık çalışma süresi, sürekli / hafta sonu duruşlu', '8.000 / 6.000 saat'],
        ['Ark ocağı yıllık çalışma günü', '340 gün'],
        ['Elektrik üretiminin CO₂ etkisi', '0,44 t CO₂/MWh'],
    ]),
    ('p', "ORC net elektrik verimi, kaynak sıcaklığına bağlı doğrusal bir eğriyle tanımlanmıştır: 250 °C'de "
          "%12–15, 400 °C ve üzerinde %18–22 alınmakta, iki nokta arasında doğrusal değişmektedir (Tablo 3.2). "
          "Birden fazla ısı akışı bulunan ünitelerde verim, her akışın ısıl gücüyle ağırlıklandırılarak "
          "hesaplanmaktadır. Elektrik gücü geri kazanılabilir ısı ile bu verimin çarpımıdır ve sonuç tek bir "
          "değer yerine alt–üst aralık olarak verilmektedir."),
    ('p', "Yıllık elektrik üretimi, elektrik gücünün yıllık çalışma süresiyle çarpımıdır. Çalışma süresi "
          "girilmemişse çalışma rejimine göre varsayılan değer kullanılmakta ve sonucun hangi varsayıma "
          "dayandığı ekranda belirtilmektedir. Üretilecek elektriğin şebeke elektriğinin yerini alacağı "
          "kabulüyle CO₂ azaltımı da hesaplanmaktadır. Tüm varsayımlar ünite bazında değiştirilebilmekte; "
          "ekrandaki gösterge, hesaplama sayfası ve Excel çıktısı aynı değerleri kullanmaktadır."),
])

F('w4c', 3, '3.4.3. Ark ocağı döküm profili ve ısı depolama', '12–16.10.2026', [
    ('h3', '3.4.3. Ark ocağı döküm profili ve ısı depolama'),
    ('fig', 'fig_onfiz_eaf.png', 13.0, 'Şekil 3.7 Ön fizibilite veri formunda ark ocağı proses şeması ve ölçüm noktaları'),
    ('p', "Elektrik ark ocağında gazlar yanma odası, su soğutmalı kanal, filtre ve emiş fanından (ID fan) "
          "geçerek bacaya ulaşmaktadır (Şekil 3.7). Gaz sıcaklığı ve debisi döküm çevrimi boyunca büyük ölçüde "
          "değiştiğinden ortalama değerler yeterli olmamakta, bu nedenle ark ocağı sayfasına döküm çevrimi "
          "profili eklenmiştir. Kullanıcı ölçüm verisini (zaman, gaz sıcaklığı, debi ve faz) tabloya "
          "yapıştırabilmekte ya da faz süreleri ve sıcaklıklarından oluşan bir faz tablosu girebilmektedir. "
          "Form bu verilerden ısıl güç serisini P(t) = ṁ·cp·(T − 150 °C) bağıntısıyla hesaplayıp grafikte "
          "göstermektedir."),
    ('p', "Kesikli çalışan bir kaynaktan ORC'yi sürekli beslemek için ısı depolama gerekmektedir. Isıl gücün "
          "ortalamadan sapmaları zamana göre toplanmakta, bu kümülatif farkın en büyük ve en küçük değeri "
          "arasındaki fark gerekli depolama kapasitesini vermektedir. Bu enerjiyi 270/85 °C arasında çalışan "
          "kızgın yağ ile depolayacak tankın hacmi de hesaplanmaktadır. Profil verisi yoksa ark süresinin "
          "döküm süresine oranıyla kaba bir tahmin yapılmakta; gösterim için kullanılan örnek veri gerçek bir "
          "tesise ait olmayan sentetik veridir."),
])

F('w4d', 3, '3.4.4. Excel çıktısı, saha krokisi ve belgeler', '12–16.10.2026', [
    ('h3', '3.4.4. Excel çıktısı, saha krokisi ve belgeler'),
    ('p', "Formun Excel çıktısında her ünite için ayrı bir sayfa oluşturulmaktadır. Sayfalarda sıra numarası, "
          "parametre, değer, birim, durum, öncelik ve not/veri kaynağı sütunları yer almakta; durum sütunu "
          "formülle \"tamamlandı\" veya \"eksik\" olarak renklendirilmektedir. Bunlara ön hesap ve özet "
          "sayfaları eklenmekte, biyogaz sektör formlarında atık, atıksu ve kimyasal oksijen ihtiyacı (KOİ) "
          "değerleri için 12 aylık dağılım sayfası oluşturulmaktadır. Müşterinin doldurup gönderdiği Excel "
          "dosyası forma geri yüklenebilmekte, böylece yanıtlar ve şemalar aynı ekranda incelenebilmektedir."),
    ('p', "Saha ve yerleşim adımında ızgara üzerinde sürükle-bırak yöntemiyle çizilen bir saha krokisi "
          "bulunmaktadır. Krokide ısı kaynağı, ORC için ayrılabilecek alan, trafo ve soğutma kulesi "
          "yerleştirilmekte; bir bağlantının gerçek uzunluğu girildiğinde ölçek yeniden hesaplanmakta ve ORC "
          "alanının bu öğelere uzaklıkları bulunmaktadır."),
    ('p', "Belgeler adımında vaziyet planı, baca ve kanal fotoğrafları, proses akış şeması, merkezi denetim ve "
          "veri toplama (SCADA) sistemi trend görüntüleri, fan ve motor etiket fotoğrafları, emisyon ve toz "
          "analiz raporları, enerji etüt raporu ile biyogaz için atık, atıksu ve çamur analizleri ayrı "
          "başlıklar altında istenmektedir. Fotoğraflar Excel'e küçültülerek eklenmekte, diğer belgeler "
          "e-posta sınırlarına uyması için 15 MB'lık paketlere bölünmektedir. Gönderim adımında Outlook'ta "
          "Excel dosyası ekli, gönderilmeye hazır bir e-posta taslağı oluşturulmaktadır."),
])

F('w4e', 3, '3.4.5. Yönetici paneli ve müşteriye özel form', '12–16.10.2026', [
    ('h3', '3.4.5. Yönetici paneli ve müşteriye özel form'),
    ('p', "Formun birim içinde kullanılan bölümü olarak bir yönetici paneli hazırlanmıştır. Panelde müşteri "
          "kayıtları, işlem geçmişi, ekip listesi, karşılaştırma, kılavuz ve ayarlar sekmeleri bulunmakta; "
          "kayıtlar ekip üyelerinin erişebildiği ortak bir klasörde tutulmaktadır. Hesaplama sekmesi, açık "
          "formdaki verilerle ünite türüne göre ayrıntılı hesap yapmakta ve varsayımların ünite bazında "
          "değiştirilmesine olanak vermektedir."),
    ('p', "Yeni bir müşteri kaydı oluşturulduğunda ünite türleri, müşteri bilgileri ile sorumlu satış ve enerji "
          "verimliliği çalışanları seçilerek müşteriye özel bir form üretilmektedir. Bu dosyadan yönetici "
          "paneli ve birime ait hesap ayrıntıları çıkarılmakta, ünite türleri kilitlenmektedir. Müşteri "
          "formunda yalnızca geri kazanılabilir ısı gösterilmekte, ORC elektrik gücü ise yalnızca birimin "
          "kullandığı sürümde görünmektedir. Müşteriden gelen Excel veya ZIP dosyası panele yüklendiğinde "
          "yanıtlar, proses şemaları, ön hesap ve kontrol uyarıları birlikte görüntülenmektedir."),
])

F('w4f', 3, '3.4.6. Maliyet ve ödeme planı sunumu', '13–15.10.2026', [
    ('h3', '3.4.6. Maliyet ve ödeme planı sunumu'),
    ('p', "13.10.2026 tarihinde biyogaz tesisi projesinin maliyet ve ödeme planı sunumuna girecek maliyet "
          "kalemleri derlenmiş, 14 ve 15.10.2026 tarihlerinde sunum sayfaları düzenlenmiştir. Sunumun ilk "
          "sayfası düzeltilmiş, ikinci sayfadaki çok satırlı maliyet listesi yöneticinin tek bakışta "
          "okuyabileceği biçimde 12 ana maliyet kalemi ve 4 genel gider kalemi olarak birleştirilmiştir."),
    ('p', "Kontrol sırasında ödeme planındaki oranların toplamının %100 yerine %110 olduğu tespit edilmiş ve "
          "düzeltilmesi gerektiği not edilmiştir. Bu tespit, sunumlardaki oran ve toplamların sunumdan önce "
          "çapraz kontrol edilmesi gerektiğini göstermiştir."),
])

F('w5a', 3, '3.5.1. Biyogaz üniteleri ve sektör formları', '19–23.10.2026', [
    ('h2', '3.5. Beşinci Hafta (19.10.2026 – 23.10.2026)'),
    ('h3', '3.5.1. Biyogaz üniteleri ve sektör formları'),
    ('p', "19–23.10.2026 tarihlerinde veri formunun biyogaz ve ısı pompası üniteleri üzerinde çalışılmıştır. "
          "Biyogaz ünitesinde tesis türü (fermentörlü biyogaz tesisi, endüstriyel atıksu anaerobik reaktörü, "
          "arıtma çamuru çürütücüsü veya çöp gazı), biyogazın kullanımı (gaz motoru ile kojenerasyon veya "
          "kazan) ve yardımcı ekipmanlar (gaz kurutucu, kükürt giderme, basınçlandırma, gaz balonu) "
          "sorulmaktadır. Gaz motoru egzozunun kükürtlü asit yoğuşmasını önlemek için en fazla 180 °C'ye kadar "
          "soğutulabileceği, metan oranı girilmemişse %55 ve metanın alt ısıl değerinin 9,97 kWh/Nm³ alınacağı "
          "kabul edilmiştir."),
    ('p', "Meyve suyu ve konsantre, süt ve peynir, dondurma ile tavuk entegre ve kesim tesisleri için ayrı "
          "sektör formları hazırlanmıştır. Bu formlarda atık türleri ve miktarları ile atıksu debisi ve KOİ "
          "değerleri aylık olarak istenmekte, her atık türü için kuru madde, organik madde, biyogaz verimi ve "
          "metan oranının literatürdeki ön gösterge değerleri kullanılmaktadır. Atıksudan biyogaz potansiyeli, "
          "anaerobik arıtmada %75 KOİ giderimi ve giderilen her kilogram KOİ için 0,35 Nm³ metan kabulüyle "
          "hesaplanmaktadır."),
    ('p', "Hesaplanan biyogazdan elektrik ve ısı üretimi, yeni bir gaz motoru için %43 elektrik ve %50 ısıl "
          "verim kabulüyle bulunmaktadır. Sektör formlarında atıkların ve atıksuyun çıktığı adımlar ile ısı ve "
          "soğutma kullanan adımlar, Avrupa Birliği'nin gıda-içecek-süt ve mezbaha sektörleri için hazırladığı "
          "mevcut en iyi teknikler referans belgeleriyle (BREF) uyumlu biçimde listelenmektedir."),
])

F('w5b', 3, '3.5.2. Isı pompası modülü', '19–23.10.2026', [
    ('h3', '3.5.2. Isı pompası modülü'),
    ('p', "Proses ısı pompası ünitesinde ısı kaynağının (atıksu, soğutma suyu, egzoz veya atık hava) debisi ve "
          "sıcaklıkları ile ısıtılacak akışkanın giriş ve çıkış sıcaklıkları sorulmakta; buhar üretimi "
          "istenirse buhar basıncından doyma sıcaklığı hesaplanmaktadır. COP, kaynak ve ısıtılan akışkanın "
          "logaritmik ortalama sıcaklıklarıyla bulunan Lorenz COP değerinin 0,5 ile çarpımı olarak "
          "hesaplanmaktadır. Buharlaştırıcı ve yoğuşturucuda 5 K sıcaklık yaklaşımı, kirli veya korozif "
          "kaynaklarda ara devre için ek 3 K alınmakta ve COP en fazla 7 ile sınırlanmaktadır."),
    ('p', "Hesap kademeli kurulmuştur: kaynak, ısıtılan akışkanın dönüş sıcaklığından en az 10 K sıcaksa önce "
          "bir eşanjörle doğrudan ön ısıtma yapılmakta, kalan ısıyı ısı pompası karşılamaktadır. Isı "
          "pompasının ısıl gücü, kalan kaynak ısısı ile COP/(COP − 1) oranının çarpımıdır ve girilen ısı "
          "ihtiyacıyla sınırlandırılmaktadır. Mahal ısıtma ısı pompasında ısı ihtiyacı girilmemişse ısıtma "
          "sezonu için ortalama 40 W/m² ısı yükü ve yılda 2.200 saat ısıtma süresi kabul edilmektedir. Bu "
          "modül üzerinde çalışılırken biyogaz tesisi projesindeki reaktör ısıtma uygulaması ayrıca "
          "incelenmiştir."),
])

F('w5c', 3, '3.5.3. Isı pompası çalışma sıcaklıkları', '21.10.2026', [
    ('h3', '3.5.3. Isı pompası çalışma sıcaklıkları'),
    ('fig', 'fig_isi_pompasi.png', 13.5, 'Şekil 3.8 Ara devreli ısı pompası düzeninde sıcaklık seviyeleri'),
    ('p', "Biyogaz tesisinde reaktör sıcaklığının korunması için reaktörden çıkan atıksuyun ısısını geri "
          "kazanıp reaktöre giden suya aktaracak bir ısı pompası öngörülmüştür. Atıksu tarafındaki sıcaklıklar "
          "birbirine çok yakındır: ısının alındığı reaktör çıkış suyu yaklaşık 33 °C, ısıtılan reaktör besleme "
          "suyu ise 37 °C'dir. Isı pompası doğrudan bu sıcaklıklarla çalışsaydı evaporatör ile kondenser "
          "arasındaki sıcaklık farkı yaklaşık 15 °C olacak, kompresör basınç oranı 1,5 dolayında kalacaktı. "
          "Standart endüstriyel ısı pompalarında kompresörün yağlanması ve genleşme vanasının kontrolü belirli "
          "bir asgari basınç farkı gerektirdiğinden bu çalışma noktası uygun değildir."),
    ('p', "Çözüm olarak ısı pompası atıksuya doğrudan bağlanmamış; iki eşanjör ile ısı pompası arasında temiz "
          "su dolaşan ara devreler kullanılmıştır (Şekil 3.8). Aynı ısı daha az suyla taşındığında suyun "
          "sıcaklık değişimi büyümektedir. Ara devre debisi atıksu debisinin yaklaşık üçte biri seçildiğinde "
          "ısı pompası kaynak tarafında 31/22 °C, kullanım tarafında 36/46 °C ile çalışmakta; evaporatör "
          "yaklaşık 20 °C, kondenser yaklaşık 48 °C sıcaklığa ulaşmakta ve sıcaklık farkı yaklaşık 28 °C'ye "
          "çıkmaktadır. Atıksu sıcaklıkları ise değişmemektedir."),
])

F('w5d', 3, '3.5.4. Çalışma noktalarının karşılaştırılması', '21–23.10.2026', [
    ('h3', '3.5.4. Çalışma noktalarının karşılaştırılması'),
    ('tbl', 'Tablo 3.3 Isı pompası çalışma noktalarının karşılaştırılması', [5.2, 4.4, 4.4], [
        ['', 'Ara devre farkı atıksuyla aynı', 'Önerilen ara devre'],
        ['Evaporatör / kondenser', '26 / 41 °C', '20 / 48 °C'],
        ['Sıcaklık farkı', '≈ 15 °C (çok düşük)', '≈ 28 °C (standart)'],
        ['Kompresör basınç oranı', '≈ 1,5', '≈ 2,2'],
        ['Beklenen COP', 'standart makine çalışmaz', '5,5 – 6'],
        ['Ara devre debisi', 'atıksu debisine eşit', 'atıksu debisinin ≈ 1/3\'ü'],
    ]),
    ('p', "İki çalışma noktası, R1234ze, R134a ve amonyak soğutucu akışkanlarının özellikleri kullanılarak "
          "karşılaştırılmıştır (Tablo 3.3). Yaklaşık 0,6 MW ısıl yük için kompresörün elektrik tüketimi "
          "100–115 kW mertebesinde bulunmuştur. Ön hesapta kullanılan COP 6,5 değerinin iyimser olduğu, "
          "fizibilitede 5,5–6 aralığının kullanılmasının daha gerçekçi olacağı belirtilmiştir. Ara devrede "
          "daha az su dolaştığından pompalar, borular ve eşanjörler de küçülmektedir."),
    ('p', "15 °C'lik ayrı bir ısı kaynağı aranmasının uygun olmadığı da gösterilmiştir: daha soğuk bir kaynak "
          "ısı pompasının aşması gereken sıcaklık farkını büyütüp elektrik tüketimini artıracak, 33 °C'deki "
          "atıksuyun yaklaşık 0,5 MW'lık ısısı ise kullanılmadan atılacaktır. Sonraki adımlar; üreticilerden "
          "belirlenen çalışma noktası için teklif ve COP teyidi alınması, atıksu tarafında katı ve yağa uygun "
          "geniş kanallı plakalı eşanjör seçilmesi ve fabrikanın soğutma yükü verisinin toplanması olarak "
          "belirlenmiştir. Çalışma bir bilgi notu olarak hazırlanmış; 22 ve 23.10.2026 tarihlerinde bu "
          "çalışmaya devam edilmiştir."),
])

F('w6a', 3, '3.6.1. Biyogaz tesisi saha ziyareti', '26.10.2026', [
    ('h2', '3.6. Altıncı Hafta (26.10.2026 – 30.10.2026)'),
    ('h3', '3.6.1. Biyogaz tesisi saha ziyareti'),
    ('p', "Enerji Verimliliği ekibiyle birlikte biyogaz tesisinin kurulacağı beyaz et üretim tesisine saha "
          "ziyareti yapılmıştır. Ziyarete Türk Standardları Enstitüsü (TSE) ekibi de katılmış, görüşmede "
          "projenin yararlanabileceği devlet yatırım destekleri ele alınmıştır."),
    ('p', "Görüşmenin konusu, ikinci haftada hazırlanan destek envanterindeki programlarla doğrudan "
          "ilişkilidir. Biyogaz yatırımında 9903 sayılı Karar kapsamındaki teşvikler, üretilen elektrik için "
          "YEKDEM ve lisanssız üretim (öz tüketim) düzenlemeleri ile verimlilik destekleri değerlendirilebilecek "
          "başlıca seçeneklerdir. Ziyaret, ilk haftalarda sunumları hazırlanan projenin müşteri tesisinde ve "
          "paydaşlarla birlikte ele alınmasını sağlamıştır."),
    ('p', "28, 29 ve 30.10.2026 tarihlerinde Cumhuriyet Bayramı ve şirketin köprü izni nedeniyle "
          "çalışılmamıştır."),
])

F('w6b', 3, '3.6.2. Ön fizibilite veri formunun denetimi', '27.10.2026', [
    ('h3', '3.6.2. Ön fizibilite veri formunun denetimi'),
    ('p', "Veri formunun biyogaz dışındaki üniteleri baştan sona denetlenmiştir. Denetimde ORC verim eğrisinin "
          "tüm hesaplarda ve Excel çıktısında aynı biçimde kullanılması, ısı pompası satırlarındaki değerler, "
          "şemalarda birbirinin üzerine binen etiketler ve hesaplanması gerekirken sabit metin olarak yazılmış "
          "ifadeler kontrol edilmiş, bulunan hatalar düzeltilmiştir. Formun müşteri verisiyle çalışacağı "
          "dikkate alınarak kullanıcı girdilerinin sayfaya güvenli biçimde aktarıldığı da kontrol edilmiş ve "
          "bir güvenlik açığına rastlanmamıştır. Yapılan değişiklikler bir değişiklik listesinde kayıt altına "
          "alınmıştır."),
    ('p', "Denetim, hesap araçlarında sonuçların doğruluğu kadar sabit yazılmış değerlerin ve ekran düzeninin "
          "de kontrol edilmesi gerektiğini göstermiştir; ekranda yanlış satırda görünen doğru bir değer, "
          "kullanıcıyı bir hesap hatası kadar yanıltabilmektedir."),
])

F('w7a', 3, '3.7.1. Destek değerlendirmesi ve ön rapor', '02–03.11.2026', [
    ('h2', '3.7. Yedinci Hafta (02.11.2026 – 06.11.2026)'),
    ('h3', '3.7.1. Destek değerlendirmesi ve ön rapor'),
    ('p', "02.11.2026 tarihinde saha ziyaretinin ardından biyogaz projesi için destek seçeneklerinin "
          "değerlendirilmesine devam edilmiştir. 03.11.2026 tarihinde ilk yedi haftanın çalışma kayıtları "
          "derlenmiş ve İME ön raporu hazırlanmıştır. Haftanın kalan günlerine ait çalışmalar esas rapora "
          "eklenecektir."),
])

# ---------------- Bölüm 4
F('b4a', 4, 'Bölüm 4. Sonuçlar ve öneriler', '03.11.2026', [
    ('h1', 'BÖLÜM 4. SONUÇLAR ve ÖNERİLER'),
    ('p', "Bu bölümde İME'nin ilk yedi haftasına ait ara sonuçlar verilmiştir; bölüm esas raporda "
          "tamamlanacaktır."),
    ('h2', '4.1. Elde Edilen Kazanımlar'),
    ('p', "(1) Mevzuat metinlerini madde düzeyinde okuyup müşterinin karar vermesini sağlayacak şema ve "
          "araçlara dönüştürme becerisi kazanılmıştır. Şemaların denetiminde mevzuattaki adım sırasına ve "
          "kalıcı–geçici istisna ayrımına dikkat etmenin önemi görülmüştür."),
    ('p', "(2) Karbon fiyatının enerji verimliliği yatırımlarının fizibilitesine girdiği öğrenilmiştir. "
          "Tahsisat açığı her yıl piyasadan satın alınan bir maliyet kalemi olduğundan azaltım projelerinin "
          "geri ödeme hesabına tahsisat fiyatı da eklenmelidir."),
    ('p', "(3) Atık ısı geri kazanımı için veri toplama ve ön hesap süreci uçtan uca tasarlanmış; gaz "
          "özellikleri, soğutma sınırları, ORC verimi, ısı depolama ve ısı pompası performansı gibi ısıl "
          "hesaplar, veri yapısı, birim dönüşümü ve Excel bütünleşmesiyle birlikte uygulanmıştır."),
    ('p', "(4) Anahtar teslim bir yatırım projesinde iş kırılım yapısı, sorumluluk matrisi, arayüz yönetimi "
          "ve iletişim düzeni gibi proje yönetimi araçları uygulamalı olarak kullanılmıştır."),
    ('p', "(5) Termodinamik ve ısı transferi bilgisi ısı pompası çalışma noktasının belirlenmesinde "
          "uygulanmış; bir ekipmanın kâğıt üzerindeki verimi kadar çalışma sınırlarının da kontrol edilmesi "
          "gerektiği görülmüştür."),
    ('p', "(6) Yöneticilere yönelik kısa e-posta, sunum ve bilgi notu hazırlama ile bir veri envanterini tek "
          "kaynak olarak kullanıp ondan araç üretme konularında deneyim kazanılmıştır."),
])

F('b4b', 4, 'Bölüm 4. Sonuçlar ve öneriler (devam)', '03.11.2026', [
    ('h2', '4.2. Öneriler'),
    ('p', "(1) Destek envanteri birimde tek veri kaynağı olarak kullanılmalı; parasal eşikler her yıl yeniden "
          "değerleme oranıyla, program şartları ise mevzuat değiştikçe teyit listesi üzerinden "
          "güncellenmelidir."),
    ('p', "(2) TR ETS kapsamındaki müşteriler için hazırlanan fizibilitelerde, enerji maliyeti tasarrufunun "
          "yanında tahsisat açığındaki azalma da ayrı bir kalem olarak gösterilmeli; ancak faaliyet seviyesi "
          "düşen alt tesislerde ücretsiz tahsisatın da azalacağı (m. 13/7) hesaba katılmalıdır."),
    ('p', "(3) Ön fizibilite veri formu saha ziyaretinden önce müşteriye gönderilmeli, ziyarette yalnızca "
          "eksik ölçümlere odaklanılmalıdır. Formdaki ön hesap sonuçları, fizibilite aşamasında yerinde "
          "ölçümlerle doğrulanmalıdır."),
    ('p', "(4) Sunumlarda ve hesap araçlarında her değerin \"ölçülen\", \"varsayım\" veya \"hesaplanan\" "
          "olduğu etiketlenmeli; oran ve toplamlar sunumdan önce çapraz kontrol edilmelidir. Maliyet sunumunda "
          "tespit edilen %110'luk ödeme planı toplamı bu ihtiyacı göstermektedir."),
    ('p', "(5) Isı pompası gibi düşük sıcaklık farkıyla çalışan uygulamalarda üreticiden çalışma noktası ve "
          "COP teyidi proje başında alınmalı; ara devre tasarımı gibi çözümler eşanjör ve pompa "
          "boyutlandırmasıyla birlikte ele alınmalıdır."),
    ('h2', '4.3. Kalan Döneme İlişkin Beklentiler'),
    ('p', "İME'nin kalan döneminde saha ölçümleri ve enerji etütlerine katılım, biyogaz projesinin mühendislik "
          "ve satın alma aşamalarının izlenmesi ve TR ETS kapsamındaki bir tesiste verimlilik önlemlerinin "
          "karbon fiyatı altında değerlendirilmesine yönelik veri toplanması hedeflenmektedir."),
])

# ---------------- Ekler
F('ek1', 5, 'Ek-1 İME süresince hazırlanan çıktılar', '21.09–03.11.2026', [
    ('h1', 'EKLER'),
    ('h2', 'Ek-1 İME Süresince Hazırlanan Çıktılar'),
    ('tbl', '', [3.4, 7.8, 2.8], [
        ['Tarih', 'Çıktı', 'Biçim'],
        ['22–23.09.2026', 'TR ETS kapsam belirleme şeması ve A4 rehber', 'PDF, draw.io'],
        ['24.09.2026', 'ETS kapsam karar aracı', 'HTML'],
        ['23–24.09.2026', 'Enerji portföy yönetim paneli ve değişiklik raporu', 'HTML, PDF, Word'],
        ['24.09.2026', 'İş planı taslağı şablonu', 'PowerPoint'],
        ['25.09.2026', 'Biyogaz projesi iş birliği ve genel müdür sunumları', 'PowerPoint'],
        ['28.09.2026', 'Enerji yatırımı destekleri veri envanteri 2026', 'Excel'],
        ['28.09.2026', 'Destek analiz aracı ve kullanım kılavuzu', 'HTML, PDF'],
        ['28.09–02.10.2026', 'Biyogaz projesi risk değerlendirme sunumu', 'PowerPoint'],
        ['05–16.10.2026', 'Atık ısı geri kazanımı ön fizibilite veri formu', 'HTML, Excel'],
        ['14–15.10.2026', 'Maliyet ve ödeme planı sunumu', 'PowerPoint'],
        ['19–23.10.2026', 'Veri formunun biyogaz ve ısı pompası üniteleri', 'HTML'],
        ['21.10.2026', 'Isı pompası çalışma sıcaklıkları bilgi notu', 'HTML'],
        ['27.10.2026', 'Veri formu denetimi ve değişiklik listesi', 'Metin'],
    ]),
])

# ---------------------------------------------------------------- haftalık çalışma tabloları
# (tarih, iş, [çerçeve id], saat). saat None → boş.
HAFTALAR = [
 ('21.09.2026', '25.09.2026', [
  ('21.09.2026', 'Oryantasyon: giriş işlemleri, ekiple tanışma, birimin çalışma düzeni', ['w1a'], 8),
  ('22.09.2026', 'TR ETS Yönetmeliği ve eklerinin incelenmesi; kapsam belirleme şeması', ['w1b', 'w1c'], 8),
  ('23.09.2026', 'ETS şemasının sadeleştirilmesi; enerji portföy yönetim paneli tasarımı', ['w1d', 'w1e'], 8),
  ('24.09.2026', 'ETS kapsam karar aracı; iş planı taslağı şablonu; panel değişiklik raporu', ['w1d', 'w1e', 'w1f'], 8),
  ('25.09.2026', 'Biyogaz projesi iş birliği sunumu ve genel müdür sunumu', ['w1g', 'w1h'], 8),
 ]),
 ('28.09.2026', '02.10.2026', [
  ('28.09.2026', 'Enerji yatırımı destekleri veri envanteri ve destek analiz aracı', ['w2a', 'w2b'], 8),
  ('29.09.2026', 'Destek aracının tanıtımı; elektrifikasyonun karbon yükümlülüklerine etkisi', ['w2c'], 8),
  ('30.09.2026', 'Biyogaz projesi risk değerlendirme sunumu', ['w2d'], 8),
  ('01.10.2026', 'Risk değerlendirme sunumu (devam)', ['w2d'], 8),
  ('02.10.2026', 'Risk değerlendirme sunumunun son hâli ve dosyanın paylaşıma hazırlanması', ['w2d'], 8),
 ]),
 ('05.10.2026', '09.10.2026', [
  ('05.10.2026', 'Ön fizibilite veri formunun kapsamının belirlenmesi', ['w3a'], 8),
  ('06.10.2026', 'Atık ısı ön fizibilite veri formunun ilk sürümü', ['w3a'], 8),
  ('07.10.2026', 'Veri formunun uçtan uca incelenmesi; şema tabanlı yapı', ['w3a', 'w3b'], 8),
  ('08.10.2026', 'Ön fizibilite veri formunun geliştirilmesi (devam)', ['w3b', 'w3c'], 8),
  ('09.10.2026', 'Ön fizibilite veri formunun geliştirilmesi (devam)', ['w3b', 'w3c'], 8),
 ]),
 ('12.10.2026', '16.10.2026', [
  ('12.10.2026', 'Ön fizibilite veri formunun geliştirilmesi (devam)', ['w4a', 'w4b', 'w4c', 'w4d', 'w4e'], 8),
  ('13.10.2026', 'Biyogaz projesi maliyet kalemlerinin derlenmesi', ['w4f'], 8),
  ('14.10.2026', 'Maliyet ve ödeme planı sunumu: 12 ana kalem ve 4 genel gider', ['w4f'], 8),
  ('15.10.2026', 'Maliyet sunumu (devam): sayfa düzeni ve ödeme oranlarının kontrolü', ['w4f'], 8),
  ('16.10.2026', 'Ön fizibilite veri formunun geliştirilmesi (devam)', ['w4a', 'w4b', 'w4c', 'w4d', 'w4e'], 8),
 ]),
 ('19.10.2026', '23.10.2026', [
  ('19.10.2026', 'Veri formu: biyogaz ve ısı pompası üniteleri', ['w5a', 'w5b'], 8),
  ('20.10.2026', 'Veri formu: biyogaz ve ısı pompası üniteleri (devam)', ['w5a', 'w5b'], 8),
  ('21.10.2026', 'Reaktör ısıtması için ısı pompası çalışma sıcaklıkları bilgi notu', ['w5c', 'w5d'], 8),
  ('22.10.2026', 'Isı pompası çalışması (devam)', ['w5d'], 8),
  ('23.10.2026', 'Isı pompası çalışması (devam)', ['w5d'], 8),
 ]),
 ('26.10.2026', '30.10.2026', [
  ('26.10.2026', 'Biyogaz tesisi saha ziyareti; devlet destekleri görüşmesi', ['w6a'], 8),
  ('27.10.2026', 'Ön fizibilite veri formunun biyogaz dışı ünitelerinin denetimi', ['w6b'], 8),
  ('28.10.2026', 'Köprü izni', [], 0),
  ('29.10.2026', 'Resmî tatil (Cumhuriyet Bayramı)', [], 0),
  ('30.10.2026', 'Köprü izni', [], 0),
 ]),
 ('02.11.2026', '06.11.2026', [
  ('02.11.2026', 'Biyogaz projesi destek seçeneklerinin değerlendirilmesi', ['w7a'], 8),
  ('03.11.2026', 'Çalışma kayıtlarının derlenmesi ve İME ön raporunun hazırlanması', ['w7a'], 8),
  ('04.11.2026', '', [], None),
  ('05.11.2026', '', [], None),
  ('06.11.2026', '', [], None),
 ]),
 ('09.11.2026', '13.11.2026', [
  ('09.11.2026', '', [], None), ('10.11.2026', '', [], None), ('11.11.2026', '', [], None),
  ('12.11.2026', '', [], None), ('13.11.2026', '', [], None),
 ]),
]

# Kullanıcının teyit etmesi gereken (yakın işin devamı olarak doldurulan) günler
TAHMINI = ['30.09.2026', '01.10.2026', '05.10.2026', '08.10.2026', '09.10.2026', '12.10.2026', '13.10.2026',
           '16.10.2026', '19.10.2026', '20.10.2026', '22.10.2026', '23.10.2026', '02.11.2026', '03.11.2026']
