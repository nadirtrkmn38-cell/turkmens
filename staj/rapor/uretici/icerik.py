# -*- coding: utf-8 -*-
# İME ön raporu içeriği. Blok türleri:
# ('h1',t) bölüm başlığı · ('h2',t) 2. derece · ('h3',t) 3. derece · ('p',t) paragraf
# ('li',t) madde (asılı girinti) · ('fig',dosya,genişlik_cm,altyazı) · ('tbl',başlık,[sütun_cm],[[satır]])

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
    "Çalışmalarım süresince bilgi ve deneyimlerini paylaşan İME sorumlusu [Unvan Ad SOYAD]'a "
    "(Enerjisa Enerji A.Ş.), Enerji Verimliliği ekibine ve denetçi öğretim elemanı [Unvan Ad SOYAD]'a "
    "(Kocaeli Üniversitesi) teşekkür ederim.",
]

OZET = [
    "Bu ön rapor, Enerjisa Enerji A.Ş. Müşteri Çözümleri – Enerji Verimliliği biriminde 21.09.2026 – "
    "03.11.2026 tarihleri arasında yürütülen İşletmede Mesleki Eğitim çalışmalarını kapsamaktadır. "
    "Çalışmaların amacı, enerji sistemleri mühendisliği bilgisinin enerji verimliliği hizmetlerinde; "
    "mevzuat analizi, yatırım desteği değerlendirmesi, proje yönetimi ve ön fizibilite süreçlerinde "
    "uygulanmasıdır.",
    "Bu dönemde dört ana konuda çalışılmıştır. Birincisinde, 27.08.2026 tarihinde yayımlanan Türkiye "
    "Emisyon Ticaret Sistemi (TR ETS) Yönetmeliği incelenmiş; sanayi müşterilerinin kapsam ve kategori "
    "durumunu belirleyen bir karar şeması ile etkileşimli bir karar aracı hazırlanmıştır. İkincisinde, "
    "enerji yatırımlarına yönelik 18 destek programını, 81 ilin bölgesel kurallarını ve 2026 parasal "
    "eşiklerini içeren 16 sayfalık bir veri envanteri oluşturulmuş ve bu envanterden harita tabanlı bir "
    "destek analiz aracı üretilmiştir. Üçüncüsünde, bir beyaz et üretim tesisinde kurulacak biyogaz "
    "tesisi projesi için iş birliği, yönetim, risk ve maliyet sunumları hazırlanmış; reaktör ısıtmasında "
    "kullanılacak ısı pompasının çalışma sıcaklıkları incelenmiş ve tesise saha ziyareti yapılmıştır. "
    "Dördüncüsünde, birim direktörü için bir enerji portföy yönetim paneli, bir müşteri veri toplama "
    "formu ve ön fizibilite hesap aracı üzerinde çalışılmıştır.",
    "Yöntem olarak mevzuat metinlerinin madde düzeyinde incelenmesi, kural tabloları ve veri envanteri "
    "oluşturulması, termodinamik çevrim hesapları ve proje yönetimi araçları (iş kırılım yapısı, "
    "sorumluluk matrisi, arayüz yönetimi) kullanılmıştır.",
    "Ara sonuç olarak; karbon fiyatlandırmasının ve devlet desteklerinin enerji verimliliği "
    "yatırımlarının fizibilitesini doğrudan değiştirdiği, ısı pompası gibi uygulamalarda ise ekipmanın "
    "çalışma sınırlarının proje başında doğrulanması gerektiği görülmüştür.",
]

SIMGELER = [
    ('°C', 'Santigrat derece, sıcaklık'),
    ('kW, MW', 'Kilovat, megavat; güç'),
    ('kWh, MWh, TWh', 'Kilovatsaat, megavatsaat, teravatsaat; enerji'),
    ('MWp', 'Megavat-pik; güneş panellerinin standart koşullardaki kurulu gücü'),
    ('m³/h', 'Metreküp/saat; hacimsel debi'),
    ('Sm³', 'Standart metreküp; doğal gaz hacmi'),
    ('t CO₂e', 'Ton karbondioksit eşdeğeri'),
]

KISALTMALAR = [
    ('AYEDAŞ', 'İstanbul Anadolu Yakası Elektrik Dağıtım A.Ş.'),
    ('COP', 'Isı pompası performans katsayısı (Coefficient of Performance)'),
    ('EAO', 'Emre amadelik oranı'),
    ('EDAŞ', 'Elektrik dağıtım anonim şirketi'),
    ('EKA', 'Enerji ve Karbon Azaltım Desteği'),
    ('EPC', 'Tasarım, tedarik ve kurulumun tek sözleşmede verildiği anahtar teslim proje modeli (Engineering, Procurement and Construction)'),
    ('EPS', 'Enerji Performans Sözleşmesi'),
    ('EPSAŞ', 'Elektrik perakende satış anonim şirketi'),
    ('GES', 'Güneş enerjisi santrali'),
    ('İME', 'İşletmede Mesleki Eğitim'),
    ('İRD', 'İzleme, raporlama ve doğrulama'),
    ('İSG', 'İş sağlığı ve güvenliği'),
    ('KOSGEB', 'Küçük ve Orta Ölçekli İşletmeleri Geliştirme ve Destekleme İdaresi Başkanlığı'),
    ('MEDAS', 'Merkezi Elektronik Doğrulayıcı Kuruluş Atama Sistemi'),
    ('P&ID', 'Boru ve enstrüman şeması (Piping and Instrumentation Diagram)'),
    ('PFD', 'Proses akış şeması (Process Flow Diagram)'),
    ('RACI', 'İşi yapan, onaylayan, görüşü alınan, bilgilendirilen (Responsible, Accountable, Consulted, Informed)'),
    ('RDF', 'Atıktan türetilmiş yakıt (Refuse Derived Fuel)'),
    ('SKDM', 'Sınırda Karbon Düzenleme Mekanizması'),
    ('SPO', 'Elektrik üretiminin, kurulu gücün tam yükte üreteceği enerjiye oranı (panel göstergesi)'),
    ('SWOT', 'Güçlü yönler, zayıf yönler, fırsatlar, tehditler'),
    ('TAM, SAM, SOM', 'Toplam, ulaşılabilir ve hedef pazar'),
    ('TR ETS', 'Türkiye Emisyon Ticaret Sistemi'),
    ('TSE', 'Türk Standardları Enstitüsü'),
    ('TÜBİTAK', 'Türkiye Bilimsel ve Teknolojik Araştırma Kurumu'),
    ('VAP', 'Verimlilik Artırıcı Proje'),
    ('YEKA', 'Yenilenebilir Enerji Kaynak Alanı'),
    ('YEKDEM', 'Yenilenebilir Enerji Kaynakları Destekleme Mekanizması'),
    ('YKH', 'Yerel Kalkınma Hamlesi'),
]

# ---------------------------------------------------------------- çerçeveli sayfalar
# bolum: 1..5 (5 = Ekler). toc: içindekilerde görünecek başlıklar [(seviye, metin)]
FRAMES = []
def F(id, bolum, title, date, blocks, toc=None):
    FRAMES.append(dict(id=id, bolum=bolum, title=title, date=date, blocks=blocks,
                       toc=toc if toc is not None else [(3, title)]))

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
          "sayılı İklim Kanunu'na dayanılarak hazırlanan Türkiye Emisyon Ticaret Sistemi (TR ETS) "
          "Yönetmeliğinin yayımlanmasıyla belirli kapasitenin üzerindeki sanayi tesisleri için sera gazı "
          "emisyonları bir maliyet kalemine dönüşmektedir. Aynı dönemde yatırım teşvik sisteminin 9903 sayılı "
          "Karar ile yeniden düzenlenmesi ve verimlilik destek programlarının 2026 tutarlarının güncellenmesi, "
          "enerji verimliliği yatırımlarının fizibilitesini etkileyen yeni bir çerçeve oluşturmuştur."),
    ('p', "İME'den beklentiler şöyle belirlenmiştir:"),
    ('li', "(a) Mevzuatın müşteri için anlaşılır ve uygulanabilir araçlara dönüştürülmesi,"),
    ('li', "(b) Enerji verimliliği projelerinin teknik ve ekonomik ön değerlendirmesinde deneyim kazanılması,"),
    ('li', "(c) Gerçek bir yatırım projesinde proje organizasyonu ile sözleşme ve paydaş yönetiminin gözlemlenmesi,"),
    ('li', "(d) Saha çalışmalarına katılım."),
    ('p', "Raporun ikinci bölümünde işletme tanıtılmış, üçüncü bölümünde haftalık çalışmalar tarih sırasıyla "
          "açıklanmış, dördüncü bölümünde ise ilk yedi haftanın ara sonuçları ve öneriler verilmiştir."),
], toc=[(1, 'BÖLÜM 1. GİRİŞ')])

F('b2a', 2, 'Bölüm 2. İşletme bilgileri', '21.09–03.11.2026', [
    ('h1', 'BÖLÜM 2. İŞLETME BİLGİLERİ'),
    ('h2', '2.1 İşletmenin Adı, Adresi ve Faaliyet Alanı'),
    ('p', "İME uygulaması, Enerjisa Enerji A.Ş.'nin Müşteri Çözümleri iş birimine bağlı Enerji Verimliliği "
          "ekibinde yapılmaktadır. Şirketin genel müdürlüğü Barbaros Mahallesi, Begonya Sokak, Nida Kule "
          "Ataşehir Batı Sitesi No: 1/1, Ataşehir/İstanbul adresindedir."),
    ('p', "Şirketin faaliyetleri üç iş kolunda toplanmaktadır. Dağıtım iş kolunda Başkent EDAŞ, İstanbul "
          "Anadolu Yakası Elektrik Dağıtım A.Ş. (AYEDAŞ) ve Toroslar EDAŞ, lisanslı bölgelerinde 36 kV altındaki "
          "şebekeler üzerinden elektrik dağıtımı yapmaktadır. Perakende iş kolunda Başkent EPSAŞ, AYESAŞ ve "
          "Toroslar EPSAŞ bu bölgelerde görevli tedarik şirketi olarak elektrik satmaktadır. Müşteri Çözümleri "
          "iş kolu ise ülke genelinde GES kurulumu, enerji verimliliği uygulamaları, kojenerasyon, yeşil enerji "
          "tedariki ve elektrikli araç şarj hizmetleri sunmaktadır."),
    ('h2', '2.2 Kısa Tarihçe ve Ortaklık Yapısı'),
    ('p', "1996 yılında kurulan Enerjisa Enerji'nin sermayesinin %40'ı Hacı Ömer Sabancı Holding A.Ş.'ye, "
          "%40'ı E.ON International Participations N.V.'ye aittir; kalan %20 halka açıktır. Şirket hisseleri "
          "8 Şubat 2018'den bu yana Borsa İstanbul'da ENJSA koduyla işlem görmektedir. Elektrikli araç şarj "
          "ağı Eşarj'ın çoğunluk hissesi 2018 yılında satın alınmıştır. Şirketin 2025 Entegre Faaliyet "
          "Raporu'ndan derlenen temel göstergeleri Tablo 2.1'de verilmiştir."),
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
], toc=[(1, 'BÖLÜM 2. İŞLETME BİLGİLERİ'), (2, '2.1 İşletmenin Adı, Adresi ve Faaliyet Alanı'),
        (2, '2.2 Kısa Tarihçe ve Ortaklık Yapısı')])

F('b2b', 2, 'Bölüm 2. İşletme bilgileri (devam)', '21.09–03.11.2026', [
    ('h2', '2.3 Çalışan Sayısı ve Organizasyon'),
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
    ('h2', '2.4 Hizmetler, Tedarik Yöntemi ve Hedef Pazar'),
    ('p', "Enerji verimliliği hizmetleri, Enerji Performans Sözleşmesi (EPS) ve performansa dayalı uzun "
          "vadeli satış modelleriyle sunulmaktadır. Bu modellerde yatırım şirket tarafından yapılmakta, "
          "müşteri yatırım bedelini sağlanan tasarruf veya üretilen enerji üzerinden ödemekte, şirket ise "
          "santralin emre amadelik ve performans değerlerini sözleşmeyle garanti etmektedir. Müşteri çözümleri "
          "portföyünde GES'lerin yanı sıra kojenerasyon ve trijenerasyon santralleri bulunmaktadır."),
    ('p', "Anahtar teslim (EPC) projelerde şirket ana yüklenici olarak tasarım, tedarik, kurulum ve devreye "
          "alma sorumluluğunu üstlenmekte; ekipman ve uzmanlık gerektiren saha işleri proje bazında satın alma "
          "süreçleriyle tedarikçi ve alt yüklenicilerden temin edilmektedir."),
    ('p', "Hedef pazar; enerji yoğun sanayi tesisleri, organize sanayi bölgelerindeki orta ölçekli "
          "işletmeler, hastane ve üniversite gibi kampüsler ile alışveriş merkezi ve otel gibi ticari "
          "binalardır. Müşteri çözümleri hizmetleri dağıtım bölgeleriyle sınırlı olmayıp ülke genelinde "
          "sunulmaktadır."),
], toc=[(2, '2.3 Çalışan Sayısı ve Organizasyon'), (2, '2.4 Hizmetler, Tedarik Yöntemi ve Hedef Pazar')])

# ---------------- Bölüm 3
F('w1a', 3, '3.1.1 Oryantasyon ve birimin tanınması', '21.09.2026', [
    ('h1', 'BÖLÜM 3. YAPILAN ÇALIŞMALAR'),
    ('p', "Bu bölümde İME süresince yapılan çalışmalar hafta hafta ve tarih sırasıyla verilmiştir. Alt "
          "başlıklar, haftalık çalışma tablolarındaki sayfa numaralarıyla eşleşmektedir."),
    ('h2', '3.1 Birinci Hafta (21.09.2026 – 25.09.2026)'),
    ('h3', '3.1.1 Oryantasyon ve birimin tanınması'),
    ('p', "İME'nin ilk gününde kurum içi giriş işlemleri tamamlanmış, çalışma bilgisayarı teslim alınmış ve "
          "kurumsal sistemlere erişim tanımlanmıştır. Ofiste bulunan ekip üyeleriyle tanışılmış, Enerji "
          "Verimliliği ekibinin görev alanları ve çalışma düzeni hakkında bilgi alınmıştır."),
    ('p', "Gün genel olarak oryantasyon şeklinde geçmiştir. Sonraki haftalarda yararlanılmak üzere birimde "
          "kullanılan yazılım ve platformlar, müşteri portföyünün yapısı, saha ziyaretlerine katılım olanağı "
          "ve İME süresince üstlenilecek somut işler gibi konular not edilmiştir."),
], toc=[(1, 'BÖLÜM 3. YAPILAN ÇALIŞMALAR'), (2, '3.1 Birinci Hafta (21.09.2026 – 25.09.2026)'),
        (3, '3.1.1 Oryantasyon ve birimin tanınması')])

F('w1b', 3, '3.1.2 TR ETS Yönetmeliğinin incelenmesi', '22.09.2026', [
    ('h3', '3.1.2 TR ETS Yönetmeliğinin incelenmesi'),
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
    ('tbl', 'Tablo 3.1 TR ETS tesis kategorileri', [3.0, 5.5, 5.5], [
        ['Kategori', 'Yıllık emisyon (t CO₂e)', 'Yükümlülük'],
        ['A', '≤ 50.000', 'Yalnızca İRD'],
        ['B', '50.001 – 500.000', 'ETS ve İRD'],
        ['C', '> 500.000', 'ETS ve İRD'],
    ]),
    ('p', "Ar-Ge tesisleri, münhasıran biyokütle kullanan tesisler ve askerî unsurlar kapsam dışındadır "
          "(m. 2/2). Okul, üniversite, hastane ve savunma sanayi tesisleri ETS dışında tutulmakla birlikte İRD "
          "yükümlülükleri sürmektedir (m. 5/2-3). Doğal gaz ve ham petrol iletimi ile depolanması ise birinci "
          "uygulama dönemi sonuna kadar geçici olarak ETS dışındadır (Geçici m. 6)."),
])

F('w1c', 3, '3.1.3 Yükümlülük süreci ve kapsam şeması', '22.09.2026', [
    ('h3', '3.1.3 Yükümlülük süreci ve kapsam şeması'),
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
    ('fig', 'fig_ets_agac.png', 15.0, 'Şekil 3.1 TR ETS kapsam belirleme şemasının karar adımları'),
])

F('w1d', 3, '3.1.4 Şemanın sadeleştirilmesi ve karar aracı', '23–24.09.2026', [
    ('h3', '3.1.4 Şemanın sadeleştirilmesi ve karar aracı'),
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
    ('fig', 'fig_ets_arac.png', 13.5, 'Şekil 3.2 ETS kapsam karar aracı (örnek tesis verisiyle)'),
])

F('w1e', 3, '3.1.5 Enerji portföy yönetim paneli', '23–24.09.2026', [
    ('h3', '3.1.5 Enerji portföy yönetim paneli'),
    ('p', "Birim direktörünün GES ve enerji verimliliği santrallerinden oluşan portföyü tek ekrandan "
          "izleyebilmesi için bir enerji portföy yönetim paneli tasarlanmıştır. Panel \"GES Üretim\" ve "
          "\"Verimlilik\" sekmelerinden oluşmakta; her sekmede portföy durum özeti, il bazında portföy "
          "haritası, gerçekleşen ve beklenen üretimi karşılaştıran grafik ve santral bazında alarm ve kayıp "
          "listesi bulunmaktadır."),
    ('p', "Santral performansı iki göstergeyle izlenmektedir: emre amadelik oranı (EAO), çalışma süresinin "
          "dönem süresine oranıdır; SPO ise elektrik üretiminin, kurulu gücün dönem boyunca tam yükte "
          "üreteceği enerjiye oranıdır. Göstergeler kurulu güçle ağırlıklandırılarak sözleşmedeki garanti "
          "değerleriyle karşılaştırılmakta ve santraller \"garanti üstü\", \"sınırda\" ve \"garanti altı\" "
          "olarak renklendirilmektedir. Verimlilik sekmesinde elektrik, buhar ve doğal gaz tasarrufu, aynı "
          "enerjinin ayrı üretimine göre; şebeke verimi %52,5, kazan verimi %90, soğutma grubu COP değeri 5 ve "
          "doğal gazın ısıl değeri 9,59 kWh/Sm³ kabulleriyle hesaplanmaktadır (Şekil 3.3). 24.09.2026 "
          "tarihinde panelin yenilenen sürümü için önceki ve sonraki ekran görüntülerini, değişiklik listesini "
          "ve varsayımları içeren bir değişiklik raporu hazırlanmıştır."),
    ('fig', 'fig_panel.png', 11.5, 'Şekil 3.3 Enerji portföy yönetim paneli, verimlilik sekmesi (örnek verilerle)'),
])

F('w1f', 3, '3.1.6 İş planı taslağı şablonu', '24.09.2026', [
    ('h3', '3.1.6 İş planı taslağı şablonu'),
    ('p', "Birimde yeni hizmet ve proje fikirlerinin yönetime aynı biçimde sunulabilmesi için kurumsal sunum "
          "şablonuyla yedi slaytlık, doldurulabilir bir iş planı taslağı hazırlanmıştır. Şablonun bölümleri ve "
          "her bölümde istenen bilgiler şöyle düzenlenmiştir:"),
    ('li', "(1) Amaç ve hedefler: tek ve ölçülebilir bir amaç cümlesi; \"neden şimdi\" sorusuna mevzuat, pazar "
           "ve kurum yetkinliği açısından yanıt; müşteri sayısı, yıllık gelir ve pazar payı hedefleri."),
    ('li', "(2) Güçlü ve zayıf yönler, fırsatlar ve tehditler (SWOT) analizi."),
    ('li', "(3) Riskler ve fırsatlar: olasılık–etki matrisi üzerinde konumlandırılan riskler ve her risk için "
           "azaltma adımı."),
    ('li', "(4) Müşteri segmentleri: büyük sanayi tesisleri, organize sanayi bölgelerindeki orta ölçekli "
           "işletmeler, kamu binaları ve hastaneler, ticari binalar; her segment için profil, ihtiyaç, değer "
           "önerisi ve öncelik."),
    ('li', "(5) Pazar büyüklüğü: toplam (TAM), ulaşılabilir (SAM) ve hedef (SOM) pazarın hesabı ile veri "
           "kaynakları."),
    ('li', "(6) Müşteri hedefi ve yol haritası: dört fazlı uygulama planı ve yönetimden istenen karar."),
    ('p', "Şablon görselleri slaytlara normal görünümde düzenlenebilecek biçimde yerleştirilmiş, içerik "
          "tıklamayla sırayla açılacak şekilde animasyonlarla hazırlanmıştır. Şablonun amacı, farklı kişilerin "
          "hazırladığı iş planlarının aynı sorulara yanıt vermesini ve birbiriyle karşılaştırılabilmesini "
          "sağlamaktır."),
])

F('w1g', 3, '3.1.7 Biyogaz projesi iş birliği sunumu', '25.09.2026', [
    ('h3', '3.1.7 Biyogaz projesi iş birliği sunumu'),
    ('p', "Bir beyaz et üretim tesisinde kurulacak biyogaz tesisi projesi için müşteriye sunulacak bir iş "
          "birliği sunumu hazırlanmıştır. Projede Enerjisa, ana yüklenici olarak tasarım, tedarik, kurulum ve "
          "devreye almayı tek sözleşmeyle üstlenmektedir (EPC); uzmanlık gerektiren saha işleri ise müşteri "
          "sözleşmesiyle uyumlu alt sözleşmelerle alt yüklenicilere verilmektedir."),
    ('p', "Organizasyon modelinde müşteri ve Enerjisa yöneticilerinden oluşan bir yönlendirme komitesi ile "
          "müşteriye tek muhatap olan bir proje müdürü tanımlanmış; mühendislik, planlama, kalite ve iş "
          "sağlığı ve güvenliği (İSG) ile satın alma fonksiyonları proje müdürüne bağlanmıştır. Proje; proje "
          "yönetimi ve mühendislik, tedarik, inşaat, mekanik montaj, elektrik ve otomasyon ile test, devreye "
          "alma ve kabul olmak üzere altı iş paketine ayrılmış ve her paket için kapsam, sınır noktaları ve "
          "teslimatlar tanımlanmıştır. Sorumluluklar RACI matrisiyle gösterilmiştir (Şekil 3.4). Alt "
          "yükleniciler arasındaki ekipman kaidesi, motor–pano bağlantısı ve sinyal listesi gibi arayüzler bir "
          "kayıt listesinde izlenmekte; her arayüzün bir sorumlusu ve kapanış tarihi bulunmaktadır."),
    ('fig', 'fig_raci.png', 14.0, 'Şekil 3.4 İş paketleri için RACI sorumluluk matrisi'),
])

F('w1h', 3, '3.1.8 Genel müdür sunumu', '25.09.2026', [
    ('h3', '3.1.8 Genel müdür sunumu'),
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

F('w2a', 3, '3.2.1 Enerji yatırımı destekleri veri envanteri', '28.09.2026', [
    ('h2', '3.2 İkinci Hafta (28.09.2026 – 02.10.2026)'),
    ('h3', '3.2.1 Enerji yatırımı destekleri veri envanteri'),
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
], toc=[(2, '3.2 İkinci Hafta (28.09.2026 – 02.10.2026)'), (3, '3.2.1 Enerji yatırımı destekleri veri envanteri')])

F('w2b', 3, '3.2.2 Destek analiz aracı ve harita', '28.09.2026', [
    ('h3', '3.2.2 Destek analiz aracı ve harita'),
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
    ('fig', 'fig_destek.png', 13.5, 'Şekil 3.5 Enerji yatırımı destek analiz aracı (örnek senaryo: 1 MW çatı GES)'),
])

F('w2c', 3, '3.2.3 Aracın tanıtımı ve ETS–SKDM değerlendirmesi', '29.09.2026', [
    ('h3', '3.2.3 Aracın tanıtımı ve ETS–SKDM değerlendirmesi'),
    ('p', "Destek aracı, birim yöneticilerine kısa bir bilgilendirme e-postasıyla tanıtılmıştır. E-postada "
          "yatırım türü ve ile göre uygun programlar, şartlar ve 2026 tutarları, uygunluk kontrolleri, harita "
          "katmanları, il kartı ve resmî kaynaklar madde madde özetlenmiştir."),
    ('p', "Aynı gün demir-çelik sektöründe elektrifikasyonun (ör. elektrik ark ocağına geçiş) TR ETS ve Avrupa "
          "Birliği Sınırda Karbon Düzenleme Mekanizması (SKDM) yükümlülüklerine etkisi değerlendirilmiş ve şu "
          "sonuçlara varılmıştır:"),
    ('li', "(1) ETS kapsamı faaliyete ve kapasiteye bağlıdır. Saatte 2,5 tonun üzerindeki pik demir veya çelik "
           "üretimi kapsamdadır; kullanılan enerjinin türü kapsamı değiştirmez."),
    ('li', "(2) Tüketilen elektriğin emisyonu dolaylı sayılır ve elektriği üreten santrale yazılır. Bu nedenle "
           "elektrifikasyon, tesisin doğrudan emisyonunu ve teslim etmesi gereken tahsisat miktarını azaltır."),
    ('li', "(3) SKDM'de demir-çelik ürünleri üretim yönteminden bağımsız olarak kapsamdadır ve bu sektörde "
           "şimdilik yalnızca doğrudan emisyonlar hesaba katılmaktadır. Elektrifiye üretimde ürüne gömülü "
           "emisyon ve SKDM maliyeti düşer, ancak beyan yükümlülüğü sürer. Türkiye'de fiilen ödenen karbon "
           "bedeli SKDM yükümlülüğünden düşülebilir."),
    ('li', "(4) Yalnızca 20 MW toplam anma ısıl gücü eşiğiyle kapsama giren sektörlerde, elektrifikasyonla "
           "eşiğin altına inilmesi kapsam dışına çıkmayı sağlayabilir; demir-çelik bu gruba girmez."),
    ('p', "Değerlendirme, elektrifikasyonun bir muafiyet değil maliyet azaltımı sağladığını ve bu farkın "
          "müşteriye açıkça anlatılması gerektiğini göstermiştir."),
])

F('w2d', 3, '3.2.4 Biyogaz projesi risk değerlendirme sunumu', '28.09–02.10.2026', [
    ('h3', '3.2.4 Biyogaz projesi risk değerlendirme sunumu'),
    ('p', "Biyogaz tesisi projesi için müşteriye sunulacak risk değerlendirme sunumu üzerinde çalışılmıştır. "
          "Sunumda proje riskleri kategorilere ayrılmış ve proje takvimindeki ilgili aşamalarla "
          "ilişkilendirilmiştir; kategori ve takvim slaytları yeniden düzenlenmiştir. 30.09 ve 01.10.2026 "
          "tarihlerinde sunum üzerindeki çalışmaya devam edilmiştir."),
    ('p', "02.10.2026 tarihinde sunumun son hâli hazırlanmıştır. Sunum dosyasının boyutu 12,6 MB olduğundan "
          "e-postayla gönderilmesi güçtü. Dosyada kullanılmayan 14 slayt yerleşimi ve 16 gömülü görsel "
          "kaldırılarak boyut, slaytların görünümü değiştirilmeden 0,62 MB'a düşürülmüştür. Düzenlemeden sonra "
          "slaytlar önceki sürümle sayfa sayfa karşılaştırılarak görünümün korunduğu kontrol edilmiştir."),
])

F('w3a', 3, '3.3.1 Enerji verimliliği veri toplama formu', '05–06.10.2026', [
    ('h2', '3.3 Üçüncü Hafta (05.10.2026 – 09.10.2026)'),
    ('h3', '3.3.1 Enerji verimliliği veri toplama formu'),
    ('p', "Enerji verimliliği ön etüdüne başlamadan önce müşteriden istenen verilerin eksiksiz ve aynı biçimde "
          "toplanabilmesi için bir veri toplama formu hazırlanmıştır. 05.10.2026 tarihinde formda yer alacak "
          "veri başlıkları üzerinde çalışılmış, 06.10.2026 tarihinde form tarayıcıda çalışan bir HTML dosyası "
          "olarak hazırlanmıştır."),
    ('p', "Formun tasarımında müşteri verilerinin gizliliği dikkate alınmıştır. Girilen veriler herhangi bir "
          "sunucuya gönderilmemekte, yalnızca kullanıcının tarayıcısında saklanmaktadır. Bu sayede doldurma "
          "işlemi yarıda kalsa bile veriler aynı bilgisayarda korunmakta; birimle paylaşım ise müşterinin formu "
          "Excel dosyası olarak dışa aktarmasıyla yapılmaktadır. Bu yaklaşım verinin müşterinin kontrolünde "
          "kalmasını sağlamakla birlikte, farklı bilgisayarlarda doldurulan formların ayrıca birleştirilmesini "
          "gerektirmektedir."),
], toc=[(2, '3.3 Üçüncü Hafta (05.10.2026 – 09.10.2026)'), (3, '3.3.1 Enerji verimliliği veri toplama formu')])

F('w3b', 3, '3.3.2 Ön fizibilite hesap aracının incelenmesi', '07–09.10.2026', [
    ('h3', '3.3.2 Ön fizibilite hesap aracının incelenmesi'),
    ('p', "Birimin ön fizibilite formuna dahil olan hesap aracı uçtan uca incelenmiştir. Araç, müşteriden "
          "alınan sınırlı veriyle biyogaz, ısı pompası ve benzeri enerji verimliliği yatırımlarının teknik ve "
          "ekonomik ön değerlendirmesini yapmak üzere tasarlanmıştır. Belirli bir müşteriye özgü değildir; "
          "biyogaz tesisi projesinde kullanılabileceği gibi farklı projelere de uygulanabilmektedir."),
    ('p', "İncelemede her hesap modülü için girdilerin birimleri, kabul edilen değerler, ara hesap adımları ve "
          "sonuçların ekranda gösterimi kontrol edilmiştir. Biyogaz modülünde hesap zinciri girdiden sonuca "
          "doğru adım adım izlenmiş, her ara sonucun bir sonraki adıma doğru birimle aktarılıp aktarılmadığı "
          "denetlenmiştir. 08 ve 09.10.2026 tarihlerinde incelemeye devam edilmiştir."),
    ('p', "Bu çalışma, ön fizibilite aşamasında kullanılan bir aracın sonuçlarının, yatırım kararına esas "
          "olacak fizibiliteye taşınmadan önce varsayımlarıyla birlikte denetlenmesi gerektiğini göstermiştir."),
])

F('w4a', 3, '3.4.1 Maliyet ve ödeme planı sunumu', '12–16.10.2026', [
    ('h2', '3.4 Dördüncü Hafta (12.10.2026 – 16.10.2026)'),
    ('h3', '3.4.1 Maliyet ve ödeme planı sunumu'),
    ('p', "Bu hafta biyogaz tesisi projesinin maliyet ve ödeme planı sunumu üzerinde çalışılmıştır. 13.10.2026 "
          "tarihinde sunuma girecek maliyet kalemleri derlenmiş, 14 ve 15.10.2026 tarihlerinde sunum sayfaları "
          "düzenlenmiştir."),
    ('p', "Sunumun ilk sayfası düzeltilmiştir. İkinci sayfada çok sayıda satırdan oluşan maliyet listesi, "
          "yöneticinin tek bakışta okuyabileceği biçimde 12 ana maliyet kalemi ve 4 genel gider kalemi olarak "
          "birleştirilmiştir. Kontrol sırasında ödeme planındaki oranların toplamının %100 yerine %110 olduğu "
          "tespit edilmiş ve düzeltilmesi gerektiği not edilmiştir. Bu tespit, sunumlarda yer alan oran ve "
          "toplamların sunumdan önce çapraz kontrol edilmesi gerektiğini göstermiştir."),
    ('p', "12 ve 16.10.2026 tarihlerinde ön fizibilite hesap aracının incelenmesine devam edilmiştir."),
], toc=[(2, '3.4 Dördüncü Hafta (12.10.2026 – 16.10.2026)'), (3, '3.4.1 Maliyet ve ödeme planı sunumu')])

F('w5a', 3, '3.5.1 Isı pompası çalışma sıcaklıkları', '19–21.10.2026', [
    ('h2', '3.5 Beşinci Hafta (19.10.2026 – 23.10.2026)'),
    ('h3', '3.5.1 Isı pompası çalışma sıcaklıkları'),
    ('p', "Biyogaz tesisinde reaktör sıcaklığının korunması için reaktörden çıkan atıksuyun ısısını geri "
          "kazanıp reaktöre giden suya aktaracak bir ısı pompası öngörülmüştür. Atıksu tarafındaki sıcaklıklar "
          "birbirine çok yakındır: ısının alındığı reaktör çıkış suyu yaklaşık 33 °C, ısıtılan reaktör besleme "
          "suyu ise 37 °C'dir. Isı pompası doğrudan bu sıcaklıklarla çalışsaydı evaporatör ile kondenser "
          "arasındaki sıcaklık farkı yaklaşık 15 °C olacak, kompresör basınç oranı 1,5 dolayında kalacaktı. "
          "Standart endüstriyel ısı pompalarında kompresörün yağlanması ve genleşme vanasının kontrolü belirli "
          "bir asgari basınç farkı gerektirdiğinden bu çalışma noktası uygun değildir."),
    ('p', "Çözüm olarak ısı pompası atıksuya doğrudan bağlanmamış; iki eşanjör ile ısı pompası arasında temiz "
          "su dolaşan ara devreler kullanılmıştır (Şekil 3.6). Aynı ısı daha az suyla taşındığında suyun "
          "sıcaklık değişimi büyümektedir. Ara devre debisi atıksu debisinin yaklaşık üçte biri seçildiğinde "
          "ısı pompası kaynak tarafında 31/22 °C, kullanım tarafında 36/46 °C ile çalışmakta; evaporatör "
          "yaklaşık 20 °C, kondenser yaklaşık 48 °C sıcaklığa ulaşmakta ve sıcaklık farkı yaklaşık 28 °C'ye "
          "çıkmaktadır. Atıksu sıcaklıkları ise değişmemektedir."),
    ('fig', 'fig_isi_pompasi.png', 14.5, 'Şekil 3.6 Ara devreli ısı pompası düzeninde sıcaklık seviyeleri'),
], toc=[(2, '3.5 Beşinci Hafta (19.10.2026 – 23.10.2026)'), (3, '3.5.1 Isı pompası çalışma sıcaklıkları')])

F('w5b', 3, '3.5.2 Çalışma noktalarının karşılaştırılması', '21–23.10.2026', [
    ('h3', '3.5.2 Çalışma noktalarının karşılaştırılması'),
    ('p', "İki çalışma noktası, R1234ze, R134a ve amonyak soğutucu akışkanlarının özellikleri kullanılarak "
          "karşılaştırılmıştır (Tablo 3.2)."),
    ('tbl', 'Tablo 3.2 Isı pompası çalışma noktalarının karşılaştırılması', [5.2, 4.6, 4.6], [
        ['', 'Ara devre farkı atıksuyla aynı', 'Önerilen ara devre'],
        ['Evaporatör / kondenser', '26 / 41 °C', '20 / 48 °C'],
        ['Sıcaklık farkı', '≈ 15 °C (çok düşük)', '≈ 28 °C (standart)'],
        ['Kompresör basınç oranı', '≈ 1,5', '≈ 2,2'],
        ['Beklenen COP', 'standart makine çalışmaz', '5,5 – 6'],
        ['Ara devre debisi', 'atıksu debisine eşit', 'atıksu debisinin ≈ 1/3\'ü'],
    ]),
    ('p', "Yaklaşık 0,6 MW ısıl yük için kompresörün elektrik tüketimi 100–115 kW mertebesinde bulunmuştur. "
          "Ön hesapta kullanılan COP 6,5 değerinin iyimser olduğu, fizibilitede 5,5–6 aralığının kullanılmasının "
          "daha gerçekçi olacağı belirtilmiştir. Ara devrede daha az su dolaştığından pompalar, borular ve "
          "eşanjörler de küçülmektedir."),
    ('p', "15 °C'lik ayrı bir ısı kaynağı aranmasının uygun olmadığı da gösterilmiştir: daha soğuk bir kaynak "
          "ısı pompasının aşması gereken sıcaklık farkını büyütüp elektrik tüketimini artıracak, 33 °C'deki "
          "atıksuyun yaklaşık 0,5 MW'lık ısısı ise kullanılmadan atılacaktır. Sonraki adımlar; üreticilerden "
          "belirlenen çalışma noktası için teklif ve COP teyidi alınması, atıksu tarafında katı ve yağa uygun "
          "geniş kanallı plakalı eşanjör seçilmesi ve fabrikanın soğutma yükü verisinin toplanması olarak "
          "belirlenmiştir. Çalışma bir bilgi notu olarak hazırlanmış; 22 ve 23.10.2026 tarihlerinde bu "
          "çalışmaya devam edilmiştir."),
])

F('w6a', 3, '3.6.1 Biyogaz tesisi saha ziyareti', '26.10.2026', [
    ('h2', '3.6 Altıncı Hafta (26.10.2026 – 30.10.2026)'),
    ('h3', '3.6.1 Biyogaz tesisi saha ziyareti'),
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
], toc=[(2, '3.6 Altıncı Hafta (26.10.2026 – 30.10.2026)'), (3, '3.6.1 Biyogaz tesisi saha ziyareti')])

F('w6b', 3, '3.6.2 Ön fizibilite hesap aracının denetimi', '27.10.2026', [
    ('h3', '3.6.2 Ön fizibilite hesap aracının denetimi'),
    ('p', "Ön fizibilite hesap aracının biyogaz dışındaki üniteleri denetlenmiştir. Denetimde verim eğrisinin "
          "hesapta doğru kullanılması, ısı pompası satırlarındaki değerler, ekran yerleşiminde birbirinin "
          "üzerine binen alanlar ve hesaplanması gerekirken sabit metin olarak yazılmış ifadeler kontrol "
          "edilmiş, bulunan hatalar düzeltilmiştir. Aracın müşteri verisiyle çalışacağı dikkate alınarak "
          "kullanıcı girdilerinin sayfaya güvenli biçimde aktarıldığı da kontrol edilmiş ve bir güvenlik "
          "açığına rastlanmamıştır. Yapılan değişiklikler bir değişiklik listesinde kayıt altına alınmıştır."),
    ('p', "Bu çalışma, hesap araçlarında sonuçların doğruluğu kadar sabit yazılmış değerlerin ve ekran "
          "düzeninin de denetlenmesi gerektiğini göstermiştir; ekranda yanlış satırda görünen doğru bir değer, "
          "kullanıcıyı bir hesap hatası kadar yanıltabilmektedir."),
])

F('w7a', 3, '3.7.1 Destek değerlendirmesi ve ön rapor', '02–03.11.2026', [
    ('h2', '3.7 Yedinci Hafta (02.11.2026 – 06.11.2026)'),
    ('h3', '3.7.1 Destek değerlendirmesi ve ön rapor'),
    ('p', "02.11.2026 tarihinde saha ziyaretinin ardından biyogaz projesi için destek seçeneklerinin "
          "değerlendirilmesine devam edilmiştir. 03.11.2026 tarihinde ilk yedi haftanın çalışma kayıtları "
          "derlenmiş ve İME ön raporu hazırlanmıştır. Haftanın kalan günlerine ait çalışmalar esas rapora "
          "eklenecektir."),
], toc=[(2, '3.7 Yedinci Hafta (02.11.2026 – 06.11.2026)'), (3, '3.7.1 Destek değerlendirmesi ve ön rapor')])

# ---------------- Bölüm 4
F('b4a', 4, 'Bölüm 4. Sonuçlar ve öneriler', '03.11.2026', [
    ('h1', 'BÖLÜM 4. SONUÇLAR VE ÖNERİLER'),
    ('p', "Bu bölümde İME'nin ilk yedi haftasına ait ara sonuçlar verilmiştir; bölüm esas raporda "
          "tamamlanacaktır."),
    ('h2', '4.1 Elde Edilen Kazanımlar'),
    ('li', "(1) Mevzuat metinlerini madde düzeyinde okuyup müşterinin karar vermesini sağlayacak şema ve "
           "araçlara dönüştürme becerisi kazanılmıştır. Şemaların denetiminde mevzuattaki adım sırasına ve "
           "kalıcı–geçici istisna ayrımına dikkat etmenin önemi görülmüştür."),
    ('li', "(2) Karbon fiyatının enerji verimliliği yatırımlarının fizibilitesine girdiği öğrenilmiştir. "
           "Tahsisat açığı her yıl piyasadan satın alınan bir maliyet kalemi olduğundan azaltım projelerinin "
           "geri ödeme hesabına tahsisat fiyatı da eklenmelidir."),
    ('li', "(3) Anahtar teslim bir yatırım projesinde iş kırılım yapısı, sorumluluk matrisi, arayüz yönetimi ve "
           "iletişim düzeni gibi proje yönetimi araçları uygulamalı olarak kullanılmıştır."),
    ('li', "(4) Termodinamik ve ısı transferi bilgisi ısı pompası çalışma noktasının belirlenmesinde "
           "uygulanmış; bir ekipmanın kâğıt üzerindeki verimi kadar çalışma sınırlarının da kontrol edilmesi "
           "gerektiği görülmüştür."),
    ('li', "(5) Yöneticilere yönelik kısa e-posta, sunum ve bilgi notu hazırlama ile bir veri envanterini tek "
           "kaynak olarak kullanıp ondan araç üretme konularında deneyim kazanılmıştır."),
], toc=[(1, 'BÖLÜM 4. SONUÇLAR VE ÖNERİLER'), (2, '4.1 Elde Edilen Kazanımlar')])

F('b4b', 4, 'Bölüm 4. Sonuçlar ve öneriler (devam)', '03.11.2026', [
    ('h2', '4.2 Öneriler'),
    ('li', "(1) Destek envanteri birimde tek veri kaynağı olarak kullanılmalı; parasal eşikler her yıl yeniden "
           "değerleme oranıyla, program şartları ise mevzuat değiştikçe teyit listesi üzerinden "
           "güncellenmelidir. Böylece müşteriye verilen tutarların güncelliği güvence altına alınabilir."),
    ('li', "(2) TR ETS kapsamındaki müşteriler için hazırlanan fizibilitelerde, enerji maliyeti tasarrufunun "
           "yanında tahsisat açığındaki azalma da ayrı bir kalem olarak gösterilmeli; ancak faaliyet seviyesi "
           "düşen alt tesislerde ücretsiz tahsisatın da azalacağı (m. 13/7) hesaba katılmalıdır."),
    ('li', "(3) Ön fizibilite formlarında ve sunumlarda her değerin \"ölçülen\", \"varsayım\" veya "
           "\"hesaplanan\" olduğu etiketlenmeli; oran ve toplamlar sunumdan önce çapraz kontrol edilmelidir. "
           "Maliyet sunumunda tespit edilen %110'luk ödeme planı toplamı bu ihtiyacı göstermektedir."),
    ('li', "(4) Isı pompası gibi düşük sıcaklık farkıyla çalışan uygulamalarda üreticiden çalışma noktası ve "
           "COP teyidi proje başında alınmalı; ara devre tasarımı gibi çözümler eşanjör ve pompa "
           "boyutlandırmasıyla birlikte ele alınmalıdır."),
    ('h2', '4.3 Kalan Döneme İlişkin Beklentiler'),
    ('p', "İME'nin kalan döneminde saha ölçümleri ve enerji etütlerine katılım, biyogaz projesinin mühendislik "
          "ve satın alma aşamalarının izlenmesi ve TR ETS kapsamındaki bir tesiste verimlilik önlemlerinin "
          "karbon fiyatı altında değerlendirilmesine yönelik veri toplanması hedeflenmektedir."),
], toc=[(2, '4.2 Öneriler'), (2, '4.3 Kalan Döneme İlişkin Beklentiler')])

# ---------------- Ekler
F('ek1', 5, 'Ek-1 İME süresince hazırlanan çıktılar', '21.09–03.11.2026', [
    ('h1', 'EKLER'),
    ('h2', 'Ek-1 İME Süresince Hazırlanan Çıktılar'),
    ('tbl', '', [3.2, 8.6, 3.2], [
        ['Tarih', 'Çıktı', 'Biçim'],
        ['22–23.09.2026', 'TR ETS kapsam belirleme şeması ve A4 rehber', 'PDF, draw.io'],
        ['24.09.2026', 'ETS kapsam karar aracı', 'HTML'],
        ['23–24.09.2026', 'Enerji portföy yönetim paneli ve değişiklik raporu', 'HTML, PDF, Word'],
        ['24.09.2026', 'İş planı taslağı şablonu', 'PowerPoint'],
        ['25.09.2026', 'Biyogaz projesi iş birliği sunumu ve genel müdür sunumu', 'PowerPoint'],
        ['28.09.2026', 'Enerji yatırımı destekleri veri envanteri 2026', 'Excel'],
        ['28.09.2026', 'Enerji yatırımı destek analiz aracı ve kullanım kılavuzu', 'HTML, PDF'],
        ['28.09–02.10.2026', 'Biyogaz projesi risk değerlendirme sunumu', 'PowerPoint'],
        ['06.10.2026', 'Enerji verimliliği veri toplama formu', 'HTML'],
        ['14–15.10.2026', 'Maliyet ve ödeme planı sunumu', 'PowerPoint'],
        ['21.10.2026', 'Isı pompası çalışma sıcaklıkları bilgi notu', 'HTML'],
        ['27.10.2026', 'Ön fizibilite hesap aracı değişiklik listesi', 'Metin'],
    ]),
], toc=[(1, 'EKLER'), (2, 'Ek-1 İME Süresince Hazırlanan Çıktılar')])

# ---------------------------------------------------------------- haftalık tablolar
# (tarih, gün, iş, [çerçeve id], saat). saat None → boş; '*' ile işaretli günler tahminidir.
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
  ('29.09.2026', 'Destek aracının yöneticilere tanıtımı; demir-çelikte elektrifikasyonun ETS ve SKDM değerlendirmesi', ['w2c'], 8),
  ('30.09.2026', 'Biyogaz projesi risk değerlendirme sunumu', ['w2d'], 8),
  ('01.10.2026', 'Risk değerlendirme sunumu (devam)', ['w2d'], 8),
  ('02.10.2026', 'Risk değerlendirme sunumunun son hâli ve dosyanın paylaşıma hazırlanması', ['w2d'], 8),
 ]),
 ('05.10.2026', '09.10.2026', [
  ('05.10.2026', 'Veri toplama formu için veri başlıklarının belirlenmesi', ['w3a'], 8),
  ('06.10.2026', 'Enerji verimliliği veri toplama formunun hazırlanması', ['w3a'], 8),
  ('07.10.2026', 'Ön fizibilite hesap aracının uçtan uca incelenmesi', ['w3b'], 8),
  ('08.10.2026', 'Ön fizibilite hesap aracının incelenmesi (devam)', ['w3b'], 8),
  ('09.10.2026', 'Ön fizibilite hesap aracının incelenmesi (devam)', ['w3b'], 8),
 ]),
 ('12.10.2026', '16.10.2026', [
  ('12.10.2026', 'Ön fizibilite hesap aracının incelenmesi (devam)', ['w4a'], 8),
  ('13.10.2026', 'Biyogaz projesi maliyet kalemlerinin derlenmesi', ['w4a'], 8),
  ('14.10.2026', 'Maliyet ve ödeme planı sunumu: 12 ana kalem ve 4 genel gider', ['w4a'], 8),
  ('15.10.2026', 'Maliyet sunumu (devam): sayfa düzeni ve ödeme oranlarının kontrolü', ['w4a'], 8),
  ('16.10.2026', 'Ön fizibilite hesap aracının incelenmesi (devam)', ['w4a'], 8),
 ]),
 ('19.10.2026', '23.10.2026', [
  ('19.10.2026', 'Reaktör ısıtması için ısı pompası çalışması', ['w5a'], 8),
  ('20.10.2026', 'Isı pompası çalışması (devam)', ['w5a'], 8),
  ('21.10.2026', 'Isı pompası çalışma sıcaklıkları bilgi notu', ['w5a', 'w5b'], 8),
  ('22.10.2026', 'Isı pompası çalışması (devam)', ['w5b'], 8),
  ('23.10.2026', 'Isı pompası çalışması (devam)', ['w5b'], 8),
 ]),
 ('26.10.2026', '30.10.2026', [
  ('26.10.2026', 'Biyogaz tesisi saha ziyareti; TSE ile devlet destekleri görüşmesi', ['w6a'], 8),
  ('27.10.2026', 'Ön fizibilite hesap aracının biyogaz dışı ünitelerinin denetimi', ['w6b'], 8),
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
           '16.10.2026', '19.10.2026', '20.10.2026', '22.10.2026', '23.10.2026',
           '02.11.2026', '03.11.2026']
