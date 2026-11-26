# -*- coding: utf-8 -*-
# İME raporu içeriği (KOÜ Teknoloji Fakültesi İME Yönergesi ve Rapor Yazım Kurallarına göre).
# Blok türleri: ('h1',t) bölüm başlığı · ('h2',t) 2. derece · ('h3',t) 3. derece · ('p',t) paragraf
# ('fig',dosya,genişlik_cm,altyazı) · ('tbl',başlık,[sütun_cm],[[satır]])
# Kurallar: şekil ve tablolar sayfanın üstünde (başlıklardan hemen sonra) yer alır; kısaltma ilk geçtiği
# yerde bir kez açıklanır; anlatım üçüncü şahıs; 1. ve 2. derece başlıklarda bağlaçlar küçük harf.

AD = '[Ad SOYAD]'
DONEM = 'GÜZ'
YIL = '2026–2027'
ONSOZ_TARIH = 'Aralık 2026'

ONSOZ = [
    "Bu rapor, Kocaeli Üniversitesi Teknoloji Fakültesi Enerji Sistemleri Mühendisliği Bölümü "
    "İşletmede Mesleki Eğitim (İME) uygulaması kapsamında, Enerjisa Enerji A.Ş. Müşteri Çözümleri "
    "iş birimine bağlı Enerji Verimliliği ekibinde 21.09.2026 – 25.12.2026 tarihleri arasında yürütülen "
    "çalışmaları kapsamaktadır. İlk yedi haftanın çalışmaları yarıyıl içi değerlendirme için hazırlanan "
    "ön raporda özetlenmiş; bu rapor, ön raporun bütün İME süresini kapsayacak biçimde genişletilmiş "
    "hâlidir.",
    "Raporda anlatılan çalışmaların önemli bir bölümü, birimin yürüttüğü gerçek müşteri projeleriyle "
    "ilgilidir. İME Yönergesinin 8. maddesi ve işletmenin gizlilik kuralları gereği müşteri adları, "
    "sözleşme bedelleri, birim fiyatlar ve gerçek tüketim verileri rapora alınmamış; müşteriler "
    "sektörleriyle anılmış (ör. bir beyaz et üretim tesisi), sayısal değerler gerektiğinde yaklaşık "
    "mertebeleriyle verilmiştir. Rapordaki şekiller, İME süresince hazırlanan çıktıların ekran "
    "görüntüleri ve çizimleridir; veri formunun tanıtımında kullanılan firma ve değerler örnektir ve "
    "gerçek bir tesise ait değildir.",
    "Çalışma döneminin, Türkiye Emisyon Ticaret Sistemi Yönetmeliğinin yayımlanması ve 2026 yılı "
    "yatırım teşvik düzenlemeleriyle aynı zamana denk gelmesi, güncel mevzuatın uygulamaya "
    "dönüştürülmesi konusunda çalışma olanağı sağlamıştır. İME süresinin önemli bir bölümü ise birimin "
    "müşteriden veri toplama sürecini yeniden tasarlayan atık ısı ön fizibilite veri formuna ayrılmış; "
    "formun yönetime sunulması, yapılan teknik çalışmanın karar vericilere anlatılması deneyimini "
    "kazandırmıştır.",
    "İME süresince görevleri planlayan ve çalışmaları yönlendiren İME sorumlusu [Unvan Ad SOYAD]'a "
    "(Enerjisa Enerji A.Ş.), projelerde bilgi ve deneyimlerini paylaşan Enerji Verimliliği ekibine "
    "(Enerjisa Enerji A.Ş.) ve İME sürecini izleyen denetçi öğretim elemanı [Unvan Ad SOYAD]'a "
    "(Kocaeli Üniversitesi) teşekkür edilir.",
]

OZET = [
    "Bu rapor, Enerjisa Enerji A.Ş. Müşteri Çözümleri – Enerji Verimliliği biriminde 21.09.2026 – "
    "25.12.2026 tarihleri arasında yürütülen 14 haftalık İşletmede Mesleki Eğitim çalışmalarını "
    "kapsamaktadır. Çalışmaların amacı, enerji sistemleri mühendisliği bilgisinin enerji verimliliği "
    "hizmetlerinde; mevzuat analizi, yatırım desteği değerlendirmesi, ön fizibilite ve proje yönetimi "
    "süreçlerinde uygulanmasıdır.",
    "İME süresince dört ana konuda çalışılmıştır. Birincisinde Türkiye Emisyon Ticaret Sistemi (TR ETS) "
    "Yönetmeliği incelenmiş, sanayi müşterilerinin kapsam ve kategori durumunu belirleyen bir karar şeması "
    "ve etkileşimli bir karar aracı hazırlanmıştır. İkincisinde 18 destek programını, 81 ilin bölgesel "
    "kurallarını ve 2026 parasal eşiklerini içeren bir veri envanteri ile harita tabanlı bir destek analiz "
    "aracı oluşturulmuştur. Üçüncüsü ve en kapsamlısı, atık ısı geri kazanımı ön fizibilitesi için "
    "geliştirilen şema tabanlı veri formudur. 13 ünite türü için proses şemaları, yaklaşık 116 mühendislik "
    "kontrol kuralı, ön hesap, Excel çıktısı ve yönetici paneli içeren form, örnek verilerle doğrulanarak "
    "birim direktörüne sunulmuş ve ardından güneş enerjisi santrali (GES) ünitesiyle genişletilmiştir. "
    "Dördüncüsünde, bir beyaz et üretim tesisinde kurulacak biyogaz tesisi "
    "projesi için iş birliği, yönetim, risk ve maliyet sunumları hazırlanmış, reaktör ısıtmasında kullanılacak ısı "
    "pompasının çalışma sıcaklıkları incelenmiş ve tesise saha ziyareti yapılmıştır.",
    ('plan', "İME'nin son haftalarında formun biyogaz bölümleri numaralı şema düzenine taşınmış, hesap "
             "varsayımları güncellenmiş, form pilot uygulamada denenmiş ve birime teslim edilmiştir."),
    "Yöntem olarak mevzuat metinlerinin madde düzeyinde incelenmesi, kural tabloları ve veri envanteri "
    "oluşturulması, ısıl hesaplar (gaz özellikleri, organik Rankine çevrimi (ORC) verimi, ısı depolama, "
    "ısı pompası performansı, yanma stokiyometrisi), hesap sonuçlarının bağımsız bir hesap tablosu "
    "yazılımıyla doğrulanması ve proje yönetimi araçları kullanılmıştır.",
    "Sonuç olarak; karbon fiyatlandırmasının ve devlet desteklerinin enerji verimliliği yatırımlarının "
    "fizibilitesini doğrudan değiştirdiği, müşteriden veri toplamanın serbest yazışmadan tasarlanmış bir "
    "sürece dönüştürülmesinin ön fizibilitenin hızını ve güvenilirliğini artırdığı, hatalı verinin "
    "mühendislik kurallarıyla müşteri ekranında yakalanabileceği ve ısı pompası gibi uygulamalarda "
    "ekipmanın çalışma sınırlarının proje başında doğrulanması gerektiği görülmüştür.",
]

# Alfabetik sıra (Yazım Kuralları 2.9); Yunan harfleri sonda
SIMGELER = [
    ('°C', 'Santigrat derece; sıcaklık'),
    ('cp', 'Özgül ısı, kJ/kgK'),
    ('GWh, TWh', 'Gigavatsaat, teravatsaat; enerji'),
    ('Hz', 'Hertz; frekans'),
    ('K', 'Kelvin; sıcaklık farkı'),
    ('kV', 'Kilovolt; gerilim'),
    ('kW, MW', 'Kilovat, megavat; güç'),
    ('kWe', 'Kilovat elektrik gücü'),
    ('kWh, MWh', 'Kilovatsaat, megavatsaat; enerji'),
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
    ('PLC', 'Programlanabilir mantık denetleyicisi (Programmable Logic Controller)'),
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
def F(id, bolum, title, date, blocks, plan=False):
    FRAMES.append(dict(id=id, bolum=bolum, title=title, date=date, blocks=blocks, plan=plan))

F('b1', 1, 'Bölüm 1. Giriş', '21.09–25.12.2026', [
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
    ('p', "Raporun ikinci bölümünde işletme tanıtılmış, üçüncü bölümünde 14 haftalık çalışmalar hafta hafta ve "
          "tarih sırasıyla açıklanmış, dördüncü bölümünde ise elde edilen kazanımlar, İME'den beklentilerin "
          "değerlendirmesi ve öneriler verilmiştir."),
])

F('b2a', 2, 'Bölüm 2. İşletme bilgileri', '21.09–25.12.2026', [
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

F('b2b', 2, 'Bölüm 2. İşletme bilgileri (devam)', '21.09–25.12.2026', [
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

F('b2c', 2, 'Bölüm 2. İşletme bilgileri (devam)', '21.09–25.12.2026', [
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
    ('fig', 'fig_destek.png', 11.8, 'Şekil 3.5 Enerji yatırımı destek analiz aracı (örnek senaryo: 1 MW çatı GES)'),
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
          "derlenmiş ve sekizinci hafta sonundaki yarıyıl içi değerlendirme için İME ön raporu "
          "hazırlanmıştır."),
])

F('w7b', 3, '3.7.2. Veri formunun tanıtıma hazırlanması', '04–06.11.2026', [
    ('h3', '3.7.2. Veri formunun tanıtıma hazırlanması'),
    ('p', "Haftanın kalan günlerinde ön fizibilite veri formunun birim direktörüne tanıtılması için hazırlık "
          "yapılmıştır. Bütün ünite türlerinin tek bir oturumda gösterilebilmesi amacıyla 13 ünitenin "
          "tamamına örnek değerler girilen bir örnek veri dosyası hazırlanmıştır. Örnek değerler gerçek bir "
          "tesise ait değildir; her ünitenin tipik işletme koşullarını yansıtacak biçimde seçilmiş, tav "
          "fırını, ark ocağı ve çimento fırını gibi yüksek sıcaklıklı kaynaklar ile ısı pompası ve biyogaz "
          "gibi düşük sıcaklıklı uygulamalar aynı dosyada temsil edilmiştir."),
    ('p', "Ark ocağı ünitesine 50 dakikalık döküm çevrimini yedi faza ayıran bir döküm profili, meyve suyu "
          "tesisine yalnızca Haziran–Ocak aylarında üretim yapılan sezonluk bir aylık dağılım girilmiştir. "
          "Böylece formun kesikli çalışan kaynaklar ve dönemsel üretim için kullandığı hesapların da "
          "gösterimde denenebilmesi sağlanmıştır."),
    ('p', "Örnek dosya, formun kaydedilmiş Excel dosyasını geri yükleme özelliğiyle kullanılmaktadır. Dosya "
          "yüklendiğinde 13 ünite yanıtlarıyla birlikte açılmakta ve özet adımında tüm üniteler \"ön "
          "değerlendirmeye hazır\" görünmektedir. Örnek dosyaya belge eklenmediğinden fotoğraf ve yerleşim "
          "planı yüklemeleri eksik kalmakta, ilerleme göstergesi %99 (193 temel sorudan 191'i) olarak "
          "görünmektedir."),
])

F('w8a', 3, '3.8.1. Örnek veri sonuçlarının doğrulanması', '09–10.11.2026', [
    ('h2', '3.8. Sekizinci Hafta (09.11.2026 – 13.11.2026)'),
    ('h3', '3.8.1. Örnek veri sonuçlarının doğrulanması'),
    ('p', "Örnek veri dosyasındaki ünitelerin ön gösterge sonuçları Tablo 3.4'te verilmiştir."),
    ('tbl', 'Tablo 3.4 Örnek veri dosyasındaki ünitelerin ön gösterge sonuçları', [4.2, 5.7, 4.6], [
        ['Ünite', 'Örnek girdi', 'Ön gösterge'],
        ['Tav fırını', '120 t/h; fırın çıkışı 950 °C, 42.000 Nm³/h', '≈ 5.050 kWth; 809–995 kWe'],
        ['Elektrik ark ocağı', '120 t/döküm; 900 °C, 90.000 Nm³/h', '≈ 25.300 kWth; 4.550–5.560 kWe'],
        ['Çimento fırını', '5.000 t/gün klinker; ön ısıtıcı 330 °C', '≈ 27.300 kWth; 3.920–4.840 kWe'],
        ['Alüminyum ergitme fırını', '40 t/şarj; reküperatör çıkışı 550 °C', '≈ 2.970 kWth; 534–653 kWe'],
        ['Cam ergitme fırını', '250 t/gün; 1.350 °C, 22.000 Nm³/h', '≈ 3.340 kWth; 601–735 kWe'],
        ['Buhar kazanı', '20 t/h buhar; baca gazı 240 °C', '≈ 707 kWth'],
        ['Proses ısı pompası', 'kaynak 32/27 °C; sıcak su 60/80 °C', '≈ 466 kWth; COP 3,5'],
        ['Mahal ısıtma ısı pompası', 'egzoz havası 28/18 °C, 60.000 m³/h', '≈ 245 kWth; COP 5'],
        ['Meyve suyu tesisi', '600 t/gün; Haziran–Ocak', '≈ 9.490 Nm³/gün biyogaz; 989 kWe'],
        ['Süt ve peynir tesisi', '500 t/gün süt', '≈ 11.100 Nm³/gün biyogaz; 1.130 kWe'],
        ['Dondurma tesisi', '80 t/gün', '≈ 1.920 Nm³/gün biyogaz; 202 kWe'],
        ['Tavuk entegre tesisi', '150.000 adet/gün', '≈ 17.700 Nm³/gün biyogaz; 1.910 kWe'],
        ['Biyogaz tesisi', '550 Nm³/h biyogaz; egzoz 470 °C', '≈ 1.040 kWth; 112–137 kWe'],
    ], 18),   # uzun tablo: Yazım Kuralları 2.2 uyarınca 9 punto
    ('p', "Tablo 3.4'te atık ısı ünitelerinde geri kazanılabilir ısıl güç ve ORC elektrik gücü aralığı, ısı "
          "pompası ünitelerinde ısıl güç ve COP, biyogaz sektör formlarında ise günlük biyogaz üretimi ve gaz "
          "motoruyla elde edilebilecek elektrik gücü gösterilmektedir."),
    ('p', "Sonuçlar üç yoldan karşılaştırılmıştır: formun ekranındaki gösterge, formdan indirilen Excel "
          "dosyasının forma geri yüklenmesiyle elde edilen sonuç ve Excel dosyasındaki formüllerin bağımsız "
          "bir hesap tablosu yazılımında (LibreOffice) yeniden hesaplanmasıyla bulunan değerler. 10.11.2026 "
          "tarihli sürümde 13 ünitenin sonuçları üç yolda da birebir aynı bulunmuştur. Özet adımındaki toplam "
          "satırları, ORC ünitelerinin yıllık elektrik üretimini (82,3–101 GWh) ve kazan ile proses ısı "
          "pompasının yakıt tasarrufunu (≈ 9.720 MWh) toplamaktadır; sektör formlarındaki gaz motoru "
          "elektriği bu toplama katılmamaktadır."),
])

F('w8b', 3, '3.8.2. Örnek ünitelerde ön hesap', '10.11.2026', [
    ('h3', '3.8.2. Örnek ünitelerde ön hesap'),
    ('p', "Gösterimde ayrıntılı ele alınmak üzere alüminyum ergitme fırını ve proses ısı pompası üniteleri "
          "seçilmiş, bu ünitelerin hesap adımları elle de izlenmiştir. Örnek alüminyum ergitme fırını 40 "
          "t/şarj kapasiteli, reküperatörlü bir yankılı (reverber) fırındır ve yılda 300 gün, günde dört "
          "şarjla çalışmaktadır. Reküperatör çıkışındaki 550 °C ve 18.000 Nm³/h gazın kütlesel debisi "
          "ṁ = 18.000·1,29/3600 ≈ 6,45 kg/s'dir. Gaz 150 °C'ye kadar soğutulduğunda ortalama sıcaklık "
          "350 °C, özgül ısı cp(350) ≈ 1,15 kJ/kgK olmakta ve geri kazanılabilir ısıl güç "
          "Q ≈ 6,45·1,15·(550 − 150) ≈ 2.970 kW bulunmaktadır (bkz. 3.4.1)."),
    ('p', "Kaynak sıcaklığı 400 °C'nin üzerinde olduğundan ORC net elektrik verimi %18–22 alınmakta (bkz. "
          "Tablo 3.2); elektrik gücü 534–653 kWe, yıllık 7.200 saatlik çalışmayla yıllık elektrik üretimi "
          "3,84–4,7 GWh olarak hesaplanmaktadır. Şarj kapısının üstündeki davlumbazdan emilen 90 °C'deki "
          "40.000 Nm³/h hava 60 °C'ye kadar soğutulduğunda yaklaşık 435 kWth sağlamakta, ancak sıcaklığı "
          "düşük olduğundan ORC hesabına katılmamaktadır. Ünitede \"Önerilen sistem\" seçeneği açıldığında "
          "ORC şemada reküperatör çıkışına yerleşmekte ve iki akışın toplamı yaklaşık 3.400 kWth olarak "
          "gösterilmektedir."),
    ('p', "Proses ısı pompası örneğinde ısı kaynağı, amonyaklı soğutma sisteminin 32 °C'de çıkıp 27 °C'ye "
          "soğutulan 120 m³/h suyudur ve kaynakta yaklaşık 698 kWth ısı bulunmaktadır. Yıkama ve "
          "pastörizasyonda kullanılan 20 m³/h sıcak suyun 60 °C'den 80 °C'ye ısıtılması için gereken ısıl "
          "güç Q = (20·1000/3600)·4,19·(80 − 60) ≈ 466 kW'tır. Lorenz yöntemiyle (bkz. 3.5.2) COP ≈ 3,5 "
          "bulunmakta, ısı pompasının elektrik tüketimi yaklaşık 135 kW olmakta ve mevcut doğal gaz kazanı "
          "takviye olarak kalmaktadır. Ön göstergede bu ünite için yılda yaklaşık 377.390 Sm³ doğal gaz "
          "tasarrufu gösterilmektedir."),
    ('p', "Hesaplama sayfasında her adım kullanılan formülle birlikte gösterilmektedir. ORC verimi gibi bir "
          "varsayım değiştirildiğinde ekrandaki sonuç ve Excel çıktısı birlikte güncellenmekte, varsayılan "
          "değerlere tek adımda dönülebilmektedir."),
])

F('w8c', 3, '3.8.3. Yönetici özeti', '10.11.2026', [
    ('h3', '3.8.3. Yönetici özeti'),
    ('p', "10.11.2026 tarihinde veri formu için birim direktörüne yönelik bir yönetici özeti hazırlanmıştır. "
          "Özette formun 13 ünite türünü kapsayan, kurulum ve internet bağlantısı gerektirmeyen tek bir HTML "
          "dosyası olduğu belirtilmiş; kullanım akışı, dosyanın iki kez el değiştirdiği dört adımlı bir süreç "
          "olarak özetlenmiştir: Enerji Verimliliği ekibi müşteri kaydını açmakta, satış sorumlusu formu "
          "müşteriye iletmekte, müşteri formu doldurup göndermekte ve ekip dönen dosyayı yönetici panelinde "
          "değerlendirmektedir."),
    ('p', "Öne çıkan özellikler olarak formüllerin birimin hesap taslaklarından alındığı ve 13 üniteli örnek "
          "dosyayla doğrulandığı, formun kütle ve enerji dengesine aykırı değerlerde uyarı verdiği, örnek "
          "alüminyum fırınında yaklaşık 3.400 kWth ısı ve 534–653 kWe ORC gücü, örnek proses ısı pompasında "
          "ise yaklaşık 466 kWth ısıl güç ve 3,5 COP hesaplandığı belirtilmiştir. Müşterinin ORC sonuçlarını "
          "ve fiyatları görmediği de vurgulanmıştır."),
    ('p', "Özetin son bölümünde yönetimin karar vermesi beklenen dört konu sıralanmıştır: pilot uygulama "
          "bölgesi ve müşteri sayısı, panel kayıtlarının tutulacağı ortak veri klasörü ve erişim listesi, ORC "
          "verimi, enerji fiyatları ve emisyon faktörü varsayımlarının onaylanması ve biyogaz formlarının "
          "diğer ünitelerdeki numaralı şema düzenine taşınması."),
])

F('w8d', 3, '3.8.4. Canlı gösterim senaryosu', '10.11.2026', [
    ('h3', '3.8.4. Canlı gösterim senaryosu'),
    ('p', "Aynı gün formun canlı gösterimi için 15 dakikalık bir senaryo hazırlanmıştır. Senaryoda her adım "
          "için ekranda yapılacak işlem ve verilecek ana mesaj tablo hâlinde yazılmıştır. Gösterim; ünite "
          "kategorilerinin tanıtılması, yönetici panelinde yeni kayıt açılması ve örnek Excel dosyasının "
          "yüklenmesi, alüminyum ergitme fırınında şemanın ve önerilen sistemin gösterilmesi, tav fırınında "
          "bir kontrol uyarısının canlı oluşturulması, proses ısı pompası, özet ve gönderim adımı, hesaplama "
          "sayfası ve yönetici özetindeki karar konularıyla kapanış sırasıyla kurgulanmıştır."),
    ('p', "Uyarı örneği için tav fırınında reküperatör girişi debisine fırın çıkışındaki 42.000 Nm³/h'den "
          "düşük bir değerin (30.000 Nm³/h) yazılması öngörülmüştür. İki nokta arasında gaz debisi "
          "azalamayacağından form bu girişte kütle dengesi uyarısı vermekte, uyarı hem ilgili sorunun altında "
          "hem de özet adımında görünmektedir. Gösterimden sonra değerin eski hâline döndürülmesi senaryoya "
          "not edilmiştir."),
    ('p', "Senaryoya sunumdan bir gün önce tamamlanacak bir hazırlık listesi ile olası aksaklıklar için bir "
          "yedek plan eklenmiştir: sayfa takılırsa yenilenmesi (girilen veri otomatik kaydedildiğinden "
          "kaybolmaz), projektör çözünürlüğü düşükse yakınlaştırmanın azaltılması, veri kaybolursa örnek "
          "dosyanın yeniden yüklenmesi, e-posta uygulaması yoksa yalnızca Excel indirmenin gösterilmesi ve "
          "dosya açılmazsa aynı sıranın ekran görüntüleriyle anlatılması. Senaryonun sonuna sık sorulabilecek "
          "sorular ve kısa yanıtları eklenmiştir."),
])

F('w8e', 3, '3.8.5. Sunum metni ve kullanım akışı', '11–13.11.2026', [
    ('h3', '3.8.5. Sunum metni ve kullanım akışı'),
    ('fig', 'fig_akis.png', 14.0, 'Şekil 3.9 Veri formunun kullanım akışı ve dosyaların el değiştirmesi'),
    ('p', "Haftanın son günlerinde canlı gösterim senaryosu yaklaşık 20 dakikalık bir sunum metnine "
          "dönüştürülmüştür. Sunum, sorunu anlatan bir açılış slaytından sonra üç HTML dosyası üzerinden canlı "
          "anlatım ve bir kapanış slaytı olarak kurgulanmıştır. Bu dosyalar yönetici paneli, satış dosyası ve "
          "müşteri formudur; formun kullanım akışı ve dosyanın hangi adımda kimde olduğu Şekil 3.9'da "
          "gösterilmiştir."),
    ('p', "Akışta Enerji Verimliliği ekibi yönetici panelinde müşteri kaydını açıp istenecek ünite türlerini ve "
          "satış sorumlusunu seçmekte, \"Satışa gönder\" komutu satış dosyasını ekinde taşıyan bir e-posta "
          "taslağı oluşturmaktadır. Satış dosyası yalnızca satış ekibine yöneliktir; satış sorumlusu müşteri "
          "firmasını, yetkilisini, e-posta adresini ve yanıt beklenen tarihi girdiğinde alıcısı müşteri "
          "yetkilisi, bilgi alıcıları enerji verimliliği uzmanı ve ekip adresi olan ve müşteri formunu "
          "ekinde taşıyan e-posta taslağı hazırlanmaktadır. Müşterinin gönderdiği yanıtlar Excel dosyası, "
          "belge eklendiyse ZIP paketi olarak birime ulaşmakta ve yönetici panelinde açılmaktadır. Böylece "
          "her adımda ilgili kişiye kalan tek iş e-postayı göndermek olmaktadır."),
])

F('w9a', 3, '3.9.1. Direktör sunumu', '16–17.11.2026', [
    ('h2', '3.9. Dokuzuncu Hafta (16.11.2026 – 20.11.2026)'),
    ('h3', '3.9.1. Direktör sunumu'),
    ('tbl', 'Tablo 3.5 Direktör sunumunun bölümleri', [4.4, 2.8, 7.3], [
        ['Bölüm', 'Süre (dk)', 'Ekranda gösterilen'],
        ['1. Açılış ve sorun', '0:00–2:00', 'Açılış slaytı: eksik ve hatalı verinin yol açtığı yazışma ve bekleme'],
        ['2. Yönetici paneli', '2:00–4:30', 'Kayıt, ekip ve ayar sekmeleri; yeni müşteri kaydı ve ünite seçimi'],
        ['3. Satış dosyası', '4:30–6:30', 'Müşteri bilgileri ve hazır e-posta taslağı'],
        ['4. Müşteri formu', '6:30–8:00', 'Karşılama sayfası; firma ve iletişim bilgileri'],
        ['5. Tav fırını', '8:00–10:30', 'Şemaya bağlı sorular ve canlı kontrol uyarısı'],
        ['6. Ön gösterge', '10:30–12:00', 'Girdiler değiştikçe güncellenen ısıl potansiyel'],
        ['7. Diğer üniteler', '12:00–14:30', 'Isı pompası ve biyogaz formları, atıksu arıtma çizimi, aylık dağılım'],
        ['8. Saha ve belgeler', '14:30–17:00', 'Ölçekli saha krokisi, belge listesi ve ZIP paketi'],
        ['9. Özet ve gönderim', '17:00–18:30', 'Eksik sorular, toplam potansiyel ve e-posta taslağı'],
        ['10. Kapanış', '18:30–20:00', 'Kapanış slaytı ve sorular'],
    ]),
    ('p', "Veri formu, hazırlanan sunum metniyle 17.11.2026 tarihinde birim direktörüne tanıtılmıştır "
          "(Tablo 3.5). Sunumdan önce hazırlık listesindeki adımlar tamamlanmış; üç HTML dosyası, örnek veri "
          "dosyası, örnek saha uydu görüntüsü ve açılış slaytı aynı klasöre konmuş, örnek veri müşteri formuna "
          "yüklenmiş ve dosyalar tarayıcıda ayrı sekmelerde açılmıştır. Süre yetmezse ark ocağı ve sektör "
          "formlarının kısaca geçilmesi, ön gösterge ile gönderim adımlarının ise kısaltılmaması "
          "kararlaştırılmıştır."),
    ('p', "Sunum, birimin ön fizibilite için müşteriden çok sayıda teknik veri (baca gazı sıcaklıkları, "
          "debiler, fan güçleri, yakıt tüketimi, çalışma saatleri, yerleşim planı ve fotoğraflar) istediği, bu "
          "verilerin ise çoğu zaman eksik veya hatalı geldiği tespitiyle açılmıştır. Eksik her bilgi yeni bir "
          "yazışma ve bekleme süresi doğurmakta, yanlış bir debi veya birim ise potansiyeli olduğundan büyük ya "
          "da küçük göstererek yanlış karara yol açabilmektedir. Bu nedenle ön fizibiliteyi başlatmak için "
          "gereken verinin toplanması çoğu zaman çalışmanın kendisinden uzun sürmektedir."),
])

F('w9b', 3, '3.9.2. Veri kalitesi kuralları ve ön gösterge', '17.11.2026', [
    ('h3', '3.9.2. Veri kalitesi kuralları ve ön gösterge'),
    ('p', "Sunumun teknik bölümünde, hatalı verinin birime ulaşmadan müşteri ekranında yakalanması için "
          "forma eklenen yaklaşık 116 mühendislik kuralı anlatılmıştır. Kurallar fiziksel olarak mümkün "
          "olmayan değerleri (ısı akış yönü, kütle ve enerji korunumu, yanma stokiyometrisi) ve sektörde "
          "olağan aralığın dışında kalan değerleri denetlemektedir. Canlı örnekte tav fırınının yanma havası "
          "fanı çıkışındaki debi 36.000 Nm³/h'den 25.000 Nm³/h'ye düşürülmüştür. Form, fırının yaktığı doğal "
          "gazdan stokiyometrik oranla gereken yanma havasını yaklaşık 31.300 Nm³/h olarak hesapladığından bu "
          "değerin altındaki girişte eksik yanma uyarısı vermektedir. Aynı oranla baca gazı debisinin yakıt "
          "tüketimiyle uyumu da denetlenmekte, olağan dışı değerlerde \"birimi kontrol ediniz\" uyarısı "
          "gösterilmektedir."),
    ('p', "Uyarılar gönderimi engellememekte, ancak hatalı değerin müşteri tarafından gönderimden önce "
          "görülmesini sağlamaktadır; bu yönüyle kurallar veri toplama sürecine eklenmiş bir kalite kapısı "
          "işlevi görmektedir. Ön gösterge ise müşteriyle yapılan bir toplantıda tek bir ünitenin temel "
          "sorularının birkaç dakikada doldurulup potansiyelin anında görülmesini sağlamaktadır. Örnek tav "
          "fırınında yaklaşık 5.050 kWth, örnek dosyadaki tüm ünitelerde toplam yaklaşık 65.700 kWth geri "
          "kazanılabilir ısı gösterilmektedir. Müşteri yalnızca ısıl potansiyeli görmekte; elektrik üretimi, "
          "tasarruf ve yatırım hesapları yalnızca birimin kullandığı yönetici panelinde yapılmaktadır."),
    ('p', "Sunumda formun geliştirilmesinde yapay zekâ desteğinden yararlanıldığı, ancak formun kendisinin "
          "tamamen çevrimdışı ve kurallara dayalı çalıştığı belirtilmiştir. Müşteri verisi doldurulduğu "
          "bilgisayarda kalmakta ve yalnızca müşteri gönderdiğinde birime ulaşmaktadır. Hesap sonuçlarının ön "
          "tahmin niteliğinde olduğu, kesin değerlerin fizibilite aşamasında belirleneceği vurgulanmıştır."),
])

F('w9c', 3, '3.9.3. Sunumun değerlendirilmesi', '18–20.11.2026', [
    ('h3', '3.9.3. Sunumun değerlendirilmesi'),
    ('p', "Sunumun ardından yönetici özetinde karar beklenen konular gözden geçirilmiş ve formun bir sonraki "
          "sürümünde yapılacak değişiklikler listelenmiştir. Listede müşteriden beklenmeyen tasarım "
          "ayrıntılarının formdan çıkarılması, tesisin ölçüm ve veri altyapısına ilişkin soruların "
          "genişletilmesi ve birimin portföyündeki diğer hizmetler için de veri toplanabilmesi öne çıkmıştır. "
          "19 ve 20.11.2026 tarihlerinde bu değişiklikler üzerinde çalışılmıştır."),
    ('p', "Sunum hazırlığı, teknik bir aracın yönetime anlatılmasında aracın bütün özelliklerinin değil "
          "çözdüğü sorunun ve karar gerektiren konuların öne çıkarılması gerektiğini göstermiştir. Canlı "
          "gösterimin bir senaryoya, hazırlık listesine ve yedek plana bağlanması ise sunum sırasında "
          "oluşabilecek teknik aksaklıkların riskini azaltmıştır."),
])

F('w10a', 3, '3.10.1. Veri formunun yeni sürümü', '23–26.11.2026', [
    ('h2', '3.10. Onuncu Hafta (23.11.2026 – 27.11.2026)'),
    ('h3', '3.10.1. Veri formunun yeni sürümü'),
    ('p', "23.11.2026 tarihinde veri formunun yeni sürümü hazırlanmıştır. Bu sürümde forma güneş enerjisi "
          "santrali (GES) ünitesi ve bu ünitenin şeması eklenmiştir. Böylece atık ısı geri kazanımı, ısı "
          "pompası ve biyogaz fırsatlarının yanında tesisin GES potansiyeline ilişkin veriler de aynı formla "
          "toplanabilmekte, birimin portföyündeki farklı hizmetler için müşteriden tek seferde veri "
          "istenebilmektedir."),
    ('p', "Tesisin ölçüm ve veri altyapısına ilişkin sorular genişletilmiştir. SCADA sorusunun altına "
          "tesisteki programlanabilir mantık denetleyicilerinin (PLC) ve ölçüm enstrümanlarının listesi "
          "eklenmiş, verilerin bir bulut platformunda tutulduğu durumlar için ayrı alt sorular "
          "tanımlanmıştır. Bu bilgiler, ön hesapta kullanılan sıcaklık ve debi değerlerinin tesiste hangi "
          "noktalarda ölçüldüğünü ve geçmiş verilere nasıl ulaşılabileceğini fizibilite öncesinde "
          "göstermektedir. Isı pompası bölümünden ise müşteriden beklenmeyen bir tasarım ayrıntısı olan "
          "soğutucu akışkan çıkarılmıştır."),
    ('p', "Formdaki tüm sorular tek bir şema dosyasında tanımlandığından (bkz. 3.3.2) yeni ünite ve sorular "
          "HTML formuna, dolu Excel çıktısına ve boş Excel şablonuna birlikte yansımıştır. Haftanın sonraki "
          "günlerinde yeni sürüm üzerinde çalışılmaya devam edilmiş, 26.11.2026 tarihinde ayrıca İME raporu "
          "için çalışma kayıtları derlenmiştir."),
])

F('w10b', 3, '3.10.2. Yeni sürümün örnek verilerle denenmesi', '27.11.2026', [
    ('h3', '3.10.2. Yeni sürümün örnek verilerle denenmesi'),
    ('p', "27.11.2026 tarihinde yeni sürüm örnek veri dosyasıyla denenmiş; GES ünitesinin Excel çıktısında ve "
          "boş Excel şablonunda yer aldığı, yeni veri altyapısı sorularının önceki yanıtlara göre doğru açılıp "
          "kapandığı ve önceki sürümle hazırlanan Excel dosyalarının yeni sürüme sorunsuz yüklendiği kontrol "
          "edilmiştir."),
], plan=True)

# ---------------- 11.–14. haftalar: henüz yaşanmadı; sarı vurgulu PLAN taslağıdır, gerçekleşince düzeltilir
F('w11a', 3, '3.11.1. Biyogaz formlarında numaralı şema düzeni', '30.11–04.12.2026', [
    ('h2', '3.11. On Birinci Hafta (30.11.2026 – 04.12.2026)'),
    ('h3', '3.11.1. Biyogaz formlarında numaralı şema düzeni'),
    ('p', "On birinci haftada biyogaz sektör formlarının, diğer ünitelerde olduğu gibi numaralı şema düzenine "
          "taşınması üzerinde çalışılmıştır. Atık haritası ile atıksu arıtma tesisi çizimindeki ölçüm "
          "noktalarına numara verilmiş ve aynı numaraların formdaki soru satırlarında ve Excel çıktısındaki "
          "sıra numaralarında kullanılması sağlanmıştır."),
    ('p', "Bu düzenlemeyle sektör formları ile diğer ünite formları arasındaki kullanım farkı ortadan kalkmış, "
          "müşterinin şemadaki bir numaradan ilgili soruya ve Excel'deki satıra doğrudan ulaşabilmesi "
          "sağlanmıştır. Değişikliklerin ardından biyogaz formlarının hesapları örnek veri dosyasıyla yeniden "
          "denetlenmiştir."),
], plan=True)

F('w12a', 3, '3.12.1. Varsayımların güncellenmesi ve pilot hazırlığı', '07–11.12.2026', [
    ('h2', '3.12. On İkinci Hafta (07.12.2026 – 11.12.2026)'),
    ('h3', '3.12.1. Varsayımların güncellenmesi ve pilot hazırlığı'),
    ('p', "Ön hesapta kullanılan ORC verim eğrisi, enerji fiyatları ve elektrik üretiminin emisyon faktörü "
          "birimle birlikte gözden geçirilmiş, onaylanan değerler formun varsayılan değerlerine "
          "işlenmiştir."),
    ('p', "Pilot uygulama için yönetici paneli kayıtlarının tutulacağı ortak klasör ve erişim listesi "
          "hazırlanmış, satış ekibinin satış dosyasını kullanabilmesi için kısa bir kullanım kılavuzu "
          "yazılmıştır."),
], plan=True)

F('w13a', 3, '3.13.1. Formun pilot uygulamada denenmesi', '14–18.12.2026', [
    ('h2', '3.13. On Üçüncü Hafta (14.12.2026 – 18.12.2026)'),
    ('h3', '3.13.1. Formun pilot uygulamada denenmesi'),
    ('p', "Form, pilot uygulama için belirlenen müşterilere satış ekibi aracılığıyla gönderilmiş; dönen "
          "dosyalar yönetici panelinde açılarak yanıtların eksiksizliği, kontrol uyarıları ve ön hesap "
          "sonuçları incelenmiştir."),
    ('p', "Müşterilerin zorlandığı sorular ve en sık eksik kalan veriler kayda alınmış, açıklama metinleri ve "
          "uyarı sınırları bu geri bildirimlere göre düzenlenmiştir."),
], plan=True)

F('w14a', 3, "3.14.1. Devir teslim ve İME'nin tamamlanması", '21–25.12.2026', [
    ('h2', '3.14. On Dördüncü Hafta (21.12.2026 – 25.12.2026)'),
    ('h3', "3.14.1. Devir teslim ve İME'nin tamamlanması"),
    ('p', "Son haftada formun güncel sürümü, sürüm notları ve teknik açıklamalarıyla birlikte birime teslim "
          "edilmiş; şema dosyasının, hesap varsayımlarının ve Excel çıktılarının nasıl güncelleneceği ekip "
          "üyelerine aktarılmıştır."),
    ('p', "İME süresince hazırlanan çıktılar ortak klasörde düzenlenmiş, çalışma kayıtları tamamlanmış ve İME "
          "sorumlusuyla dönemin genel değerlendirmesi yapılmıştır."),
], plan=True)

# ---------------- Bölüm 4
F('b4a', 4, 'Bölüm 4. Sonuçlar ve öneriler', '21.09–25.12.2026', [
    ('h1', 'BÖLÜM 4. SONUÇLAR ve ÖNERİLER'),
    ('p', "Bu bölümde İME süresince yapılan çalışmalardan elde edilen kazanım ve beceriler, İME'den "
          "beklentilerin ne ölçüde karşılandığı ve işletmenin hizmet süreçlerine yönelik görüş ve öneriler "
          "verilmiştir."),
    ('h2', '4.1. Elde Edilen Kazanımlar ve Beceriler'),
    ('p', "(1) Mevzuat metinlerini madde düzeyinde okuyup müşterinin karar vermesini sağlayacak şema ve "
          "araçlara dönüştürme becerisi kazanılmıştır. Şemaların denetiminde mevzuattaki adım sırasına ve "
          "kalıcı–geçici istisna ayrımına dikkat etmenin önemi görülmüştür."),
    ('p', "(2) Karbon fiyatının enerji verimliliği yatırımlarının fizibilitesine girdiği öğrenilmiştir. "
          "Tahsisat açığı her yıl piyasadan satın alınan bir maliyet kalemi olduğundan azaltım projelerinin "
          "geri ödeme hesabına tahsisat fiyatı da eklenmelidir."),
    ('p', "(3) Atık ısı geri kazanımı için veri toplama ve ön hesap süreci uçtan uca tasarlanmıştır. Gaz "
          "özellikleri, soğutma sınırları, ORC verimi, ısı depolama, ısı pompası performansı ve yanma "
          "stokiyometrisi gibi ısıl hesaplar; veri yapısı, birim dönüşümü ve Excel bütünleşmesiyle birlikte "
          "uygulanmış, termodinamik ve ısı transferi derslerindeki bağıntıların bir mühendislik aracında "
          "kural ve kontrol olarak nasıl kullanılabileceği görülmüştür."),
    ('p', "(4) Hesap sonuçlarını ekranda, Excel çıktısında ve bağımsız bir hesap tablosu yazılımında "
          "karşılaştırarak doğrulama alışkanlığı kazanılmıştır. Denetimler, sonuçların doğruluğu kadar sabit "
          "yazılmış değerlerin ve ekran düzeninin de kontrol edilmesi gerektiğini göstermiştir."),
])

F('b4b', 4, 'Bölüm 4. Sonuçlar ve öneriler (devam)', '21.09–25.12.2026', [
    ('p', "(5) Anahtar teslim bir yatırım projesinde iş kırılım yapısı, sorumluluk matrisi, arayüz yönetimi "
          "ve iletişim düzeni gibi proje yönetimi araçları uygulamalı olarak kullanılmıştır. Isı pompası "
          "çalışma noktası örneğinde bir ekipmanın kâğıt üzerindeki verimi kadar çalışma sınırlarının da "
          "kontrol edilmesi gerektiği görülmüştür."),
    ('p', "(6) Yönetime yönelik yönetici özeti, canlı gösterim senaryosu, sunum metni ve bilgi notu "
          "hazırlanmış; teknik bir çalışmayı çözdüğü sorun ve karar gerektiren konular üzerinden anlatma "
          "becerisi geliştirilmiştir."),
    ('p', "(7) Satış ekibi, teknik ekip ve müşteri arasındaki iş akışını birlikte tasarlama deneyimi "
          "kazanılmıştır. Müşteriye giden belgede hangi bilginin gösterileceği, hangisinin yalnızca birimde "
          "kalacağı gibi gizlilik ve rol ayrımı kararlarının teknik tasarımın bir parçası olduğu "
          "görülmüştür."),
    ('h2', "4.2. İME'den Beklentilerin Değerlendirilmesi"),
    ('p', "Giriş bölümünde belirlenen beklentilerden mevzuatın müşteri için anlaşılır araçlara "
          "dönüştürülmesi, TR ETS kapsam karar aracı ve destek analiz aracıyla karşılanmıştır. Enerji "
          "verimliliği projelerinin teknik ve ekonomik ön değerlendirmesinde deneyim kazanılması beklentisi "
          "atık ısı ön fizibilite veri formu ve ısı pompası çalışmasıyla, gerçek bir yatırım projesinde proje "
          "organizasyonu ile sözleşme ve paydaş yönetiminin gözlemlenmesi beklentisi ise biyogaz tesisi "
          "projesinin sunumlarıyla karşılanmıştır."),
    ('p', "Saha çalışmalarına katılım beklentisi, biyogaz tesisinin kurulacağı beyaz et üretim tesisine "
          "yapılan saha ziyaretiyle kısmen karşılanmıştır. Enerji etütlerine ve yerinde ölçümlere daha fazla "
          "katılım, ön fizibilite formunun ürettiği ön hesapların sahada nasıl doğrulandığının görülmesi "
          "açısından yararlı olacaktır.", 'plan'),
])

F('b4c', 4, 'Bölüm 4. Sonuçlar ve öneriler (devam)', '21.09–25.12.2026', [
    ('h2', '4.3. Görüş ve Öneriler'),
    ('p', "Enerji Verimliliği biriminin hizmet modeli, yatırımın şirket tarafından yapılıp bedelinin "
          "sağlanan tasarruf veya üretilen enerji üzerinden geri alındığı performansa dayalı sözleşmelere "
          "dayanmaktadır. Bu modelde ön fizibilitenin hızı ve doğruluğu, hem teklif sürecinin süresini hem "
          "de şirketin üstlendiği performans riskini doğrudan belirlemektedir. Aşağıdaki öneriler bu nedenle "
          "müşteri verisinin toplanmasına, hesap varsayımlarının yönetimine ve sonuçların doğrulanmasına "
          "odaklanmaktadır."),
    ('p', "(1) Ön fizibilite veri formu birimde müşteriden veri toplamanın varsayılan yöntemi olarak "
          "kullanılmalı, form saha ziyaretinden önce müşteriye gönderilmeli ve ziyarette yalnızca eksik "
          "ölçümlere odaklanılmalıdır. Formun tek bir güncel sürümü ortak klasörde tutulmalı, değişiklikler "
          "sürüm notlarıyla kayıt altına alınmalıdır."),
    ('p', "(2) ORC verim eğrisi, enerji fiyatları ve emisyon faktörü gibi varsayımlar birimce onaylanmış tek "
          "bir listede tutulmalı ve yılda en az bir kez gözden geçirilmelidir. Formdaki ön hesap sonuçları "
          "fizibilite aşamasında yerinde ölçümlerle doğrulanmalı, ölçüm ile ön hesap arasındaki farklar "
          "formun kurallarını iyileştirmek için kullanılmalıdır."),
    ('p', "(3) Destek envanteri birimde tek veri kaynağı olarak kullanılmalı; parasal eşikler her yıl yeniden "
          "değerleme oranıyla, program şartları ise mevzuat değiştikçe teyit listesi üzerinden "
          "güncellenmelidir."),
    ('p', "(4) TR ETS kapsamındaki müşteriler için hazırlanan fizibilitelerde, enerji maliyeti tasarrufunun "
          "yanında tahsisat açığındaki azalma da ayrı bir kalem olarak gösterilmeli; ancak faaliyet seviyesi "
          "düşen alt tesislerde ücretsiz tahsisatın da azalacağı (m. 13/7) hesaba katılmalıdır."),
])

F('b4d', 4, 'Bölüm 4. Sonuçlar ve öneriler (devam)', '21.09–25.12.2026', [
    ('p', "(5) Sunumlarda ve hesap araçlarında her değerin \"ölçülen\", \"varsayım\" veya \"hesaplanan\" "
          "olduğu etiketlenmeli; oran ve toplamlar sunumdan önce çapraz kontrol edilmelidir. Maliyet "
          "sunumunda tespit edilen %110'luk ödeme planı toplamı bu ihtiyacı göstermektedir."),
    ('p', "(6) Isı pompası gibi düşük sıcaklık farkıyla çalışan uygulamalarda üreticiden çalışma noktası ve "
          "COP teyidi proje başında alınmalı; ara devre tasarımı gibi çözümler eşanjör ve pompa "
          "boyutlandırmasıyla birlikte ele alınmalıdır."),
    ('p', "(7) Portföy yönetim panelindeki emre amadelik ve performans göstergeleri, santrallerin sözleşme "
          "garanti değerleriyle birlikte düzenli olarak izlenmeli; garanti değerinin altına düşen santraller "
          "için kök neden analizi standart bir rapor biçimine bağlanmalıdır."),
    ('p', "Genel olarak İME, enerji sistemleri mühendisliği eğitiminde edinilen bilginin mevzuat, ekonomi ve "
          "müşteri ilişkileriyle birlikte ele alındığı bir çalışma ortamı sağlamıştır. Hazırlanan araçların "
          "birimin günlük çalışmalarında kullanılabilir durumda olması, İME'nin en somut çıktısıdır."),
])

# ---------------- Ekler
F('ek1', 5, 'Ek-1 İME süresince hazırlanan çıktılar', '21.09–25.12.2026', [
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
        ['04–10.11.2026', 'Veri formu örnek veri dosyası (13 ünite)', 'Excel'],
        ['10.11.2026', 'Veri formu yönetici özeti ve canlı gösterim senaryosu', 'Metin'],
        ['10–17.11.2026', 'Direktör sunumu metni, açılış ve kapanış slaytları', 'Metin, PowerPoint'],
        ['23.11.2026', 'Veri formunun GES ünitesi eklenmiş yeni sürümü', 'HTML, Excel'],
        ('plan', ['30.11–04.12.2026', 'Biyogaz formlarında numaralı şema düzeni', 'HTML']),
        ('plan', ['07–11.12.2026', 'Satış ekibi için veri formu kullanım kılavuzu', 'PDF']),
        ('plan', ['21–25.12.2026', 'Veri formunun teslim sürümü ve sürüm notları', 'HTML, Metin']),
    ], 18),   # uzun tablo: Yazım Kuralları 2.2 uyarınca 9 punto
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
  ('04.11.2026', 'Veri formunun direktör tanıtımına hazırlanması', ['w7b'], 8),
  ('05.11.2026', 'Veri formu: 13 üniteli örnek veri dosyasının hazırlanması', ['w7b'], 8),
  ('06.11.2026', 'Örnek veri dosyası: döküm profili ve aylık dağılım', ['w7b'], 8),
 ]),
 ('09.11.2026', '13.11.2026', [
  ('09.11.2026', 'Örnek veri sonuçlarının üç yoldan karşılaştırılması', ['w8a'], 8),
  ('10.11.2026', 'Sonuçların doğrulanması; yönetici özeti ve canlı gösterim senaryosu', ['w8a', 'w8b', 'w8c', 'w8d'], 8),
  ('11.11.2026', 'Sunum metninin hazırlanması; kullanım akışının anlatımı', ['w8e'], 8),
  ('12.11.2026', 'Sunum metni (devam); açılış ve kapanış slaytları', ['w8e'], 8),
  ('13.11.2026', 'Sunum metninin gözden geçirilmesi', ['w8e'], 8),
 ]),
 ('16.11.2026', '20.11.2026', [
  ('16.11.2026', 'Sunum hazırlık listesinin tamamlanması ve prova', ['w9a'], 8),
  ('17.11.2026', 'Veri formunun birim direktörüne sunulması', ['w9a', 'w9b'], 8),
  ('18.11.2026', 'Karar konularının gözden geçirilmesi; yeni sürüm değişiklik listesi', ['w9c'], 8),
  ('19.11.2026', 'Veri formunun yeni sürümü üzerinde çalışma', ['w9c'], 8),
  ('20.11.2026', 'Veri formunun yeni sürümü (devam)', ['w9c'], 8),
 ]),
 ('23.11.2026', '27.11.2026', [
  ('23.11.2026', 'Veri formu yeni sürümü: GES ünitesi ve şeması; veri altyapısı soruları', ['w10a'], 8),
  ('24.11.2026', 'Veri formunun yeni sürümü (devam)', ['w10a'], 8),
  ('25.11.2026', 'Veri formunun yeni sürümü (devam)', ['w10a'], 8),
  ('26.11.2026', 'Veri formu (devam); İME çalışma kayıtlarının derlenmesi', ['w10a'], 8),
  ('27.11.2026', 'Yeni sürümün örnek verilerle denenmesi', ['w10b'], 8),
 ]),
 ('30.11.2026', '04.12.2026', [
  ('30.11.2026', 'Biyogaz sektör formlarında ölçüm noktalarının numaralandırılması', ['w11a'], 8),
  ('01.12.2026', 'Atık haritası ve atıksu arıtma çiziminde numaralı düzen', ['w11a'], 8),
  ('02.12.2026', 'Numaraların soru satırları ve Excel çıktısıyla eşleştirilmesi', ['w11a'], 8),
  ('03.12.2026', 'Biyogaz formlarının örnek verilerle denetimi', ['w11a'], 8),
  ('04.12.2026', 'Biyogaz formlarında numaralı düzenin tamamlanması', ['w11a'], 8),
 ]),
 ('07.12.2026', '11.12.2026', [
  ('07.12.2026', 'Ön hesap varsayımlarının birimle gözden geçirilmesi', ['w12a'], 8),
  ('08.12.2026', 'Onaylanan varsayımların forma işlenmesi', ['w12a'], 8),
  ('09.12.2026', 'Pilot uygulama için ortak klasör ve erişim listesi', ['w12a'], 8),
  ('10.12.2026', 'Satış ekibi için kullanım kılavuzu', ['w12a'], 8),
  ('11.12.2026', 'Kullanım kılavuzu (devam)', ['w12a'], 8),
 ]),
 ('14.12.2026', '18.12.2026', [
  ('14.12.2026', 'Formun pilot müşterilere gönderilmesi', ['w13a'], 8),
  ('15.12.2026', 'Pilot uygulamanın izlenmesi', ['w13a'], 8),
  ('16.12.2026', 'Dönen dosyaların yönetici panelinde incelenmesi', ['w13a'], 8),
  ('17.12.2026', 'Geri bildirimlere göre düzenlemeler', ['w13a'], 8),
  ('18.12.2026', 'Geri bildirimlere göre düzenlemeler (devam)', ['w13a'], 8),
 ]),
 ('21.12.2026', '25.12.2026', [
  ('21.12.2026', 'Formun teslim sürümü ve sürüm notları', ['w14a'], 8),
  ('22.12.2026', 'Teknik açıklamaların hazırlanması', ['w14a'], 8),
  ('23.12.2026', 'Ekibe aktarım ve devir teslim', ['w14a'], 8),
  ('24.12.2026', 'Çıktıların ortak klasörde düzenlenmesi', ['w14a'], 8),
  ('25.12.2026', "İME'nin genel değerlendirmesi; çalışma kayıtlarının tamamlanması", ['w14a'], 8),
 ]),
]

# Yakın işin devamı olarak doldurulan, kullanıcının teyit etmesi gereken günler (raporda işaretlenmez)
TAHMINI = ['30.09.2026', '01.10.2026', '05.10.2026', '08.10.2026', '09.10.2026', '12.10.2026', '13.10.2026',
           '16.10.2026', '19.10.2026', '20.10.2026', '22.10.2026', '23.10.2026', '02.11.2026', '03.11.2026',
           '04.11.2026', '05.11.2026', '06.11.2026', '09.11.2026', '11.11.2026', '12.11.2026', '13.11.2026',
           '16.11.2026', '17.11.2026', '18.11.2026', '19.11.2026', '20.11.2026', '24.11.2026', '25.11.2026',
           '26.11.2026']

# Henüz yaşanmamış günler: raporda sarı vurguyla basılır. Gün gerçekleşince metni düzeltip listeden çıkarın;
# ilgili çerçevelerden plan=True'yu ve bloklardaki 'plan' işaretini kaldırın. Sarı vurgulu rapor teslim edilmez.
PLAN = ['27.11.2026'] + ['%02d.%02d.2026' % (g, a) for a, gunler in
                         ((11, (30,)), (12, (1, 2, 3, 4, 7, 8, 9, 10, 11, 14, 15, 16, 17, 18, 21, 22, 23, 24, 25)))
                         for g in gunler]
