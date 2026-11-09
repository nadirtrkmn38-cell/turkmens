/**
 * ════════════════════════════════════════════════════════════════════
 *  nadirturkmen.com — SİTE İÇERİĞİ
 * ════════════════════════════════════════════════════════════════════
 *  Sitedeki ve "Klasik CV" sayfasındaki bütün yazılar bu dosyadan gelir.
 *  Siteni güncellemek için yalnızca bu dosyayı düzenlemen yeterli.
 *
 *  • Çevrilebilir alanlar  { tr: '…', en: '…' }  şeklindedir.
 *  • Başlıklarda *yıldız* içine aldığın kelimeler italik/vurgulu görünür.
 *  • Boş bırakılan ('') alanlar ve bağlantılar sitede gösterilmez.
 * ════════════════════════════════════════════════════════════════════
 */

export const profile = {
  name: 'Nadir Türkmen',
  firstName: 'Nadir',
  lastName: 'Türkmen',
  initials: 'NT',
  url: 'https://nadirturkmen.com',
  email: 'turkmen.nadir@hotmail.com',
  // Telefon herkese açık sitede görünür; istersen '+90 5xx xxx xx xx' biçiminde ekle.
  phone: '',
  location: { tr: 'İzmit, Kocaeli', en: 'Izmit, Kocaeli' },
  country: 'TR',
  timeZone: 'Europe/Istanbul',
  available: true, // "Yeni fırsatlara açığım" rozeti (false → gizlenir)
  // Fotoğrafını public/images/ klasörüne koyup yolunu yaz: '/images/nadir.jpg'
  photo: '',
  role: { tr: 'Enerji Sistemleri Mühendisliği', en: 'Energy Systems Engineering' },
};

export const socials = [
  { label: 'LinkedIn', url: 'https://www.linkedin.com/in/nadir-turkmen/' },
  { label: 'NTherm', url: 'https://www.ntherm.site/' },
  { label: 'GitHub', url: '' }, // istersen ekle
  { label: 'Instagram', url: '' }, // istersen ekle
];

export const content = {
  meta: {
    description: {
      tr: 'Nadir Türkmen — Enerji Sistemleri Mühendisliği. Enerji verimliliği, atık ısı geri kazanımı (ORC), GES + batarya fizibilitesi, enerji etütleri ve enerji piyasaları.',
      en: 'Nadir Türkmen — Energy Systems Engineering. Energy efficiency, waste heat recovery (ORC), PV + battery feasibility, energy audits and energy markets.',
    },
  },

  hero: {
    status: { tr: 'Yeni fırsatlara açığım', en: 'Open to new opportunities' },
    lead: {
      tr: 'Enerji verimliliği, atık ısı geri kazanımı ve enerji etütleri üzerine çalışıyorum. Sahadan topladığım veriyi fizibiliteye, tasarrufa ve yatırım kararına dönüştürüyorum.',
      en: 'I work on energy efficiency, waste heat recovery and energy audits, turning field data into feasibility studies, savings and investment decisions.',
    },
  },

  about: {
    title: {
      tr: 'Sahadaki veriyi *ölçülebilir enerji tasarrufuna* dönüştürüyorum.',
      en: 'I turn field data into *measurable energy savings.*',
    },
    paragraphs: [
      {
        tr: 'Kocaeli Üniversitesi Enerji Sistemleri Mühendisliği son sınıf öğrencisiyim (mezuniyet: Haziran 2027). Üç endüstriyel stajımda atık ısıdan elektrik üretimi, GES + batarya depolama fizibilitesi ve 10 farklı tesiste enerji etütleri üzerinde çalıştım.',
        en: "I'm a final-year Energy Systems Engineering student at Kocaeli University (graduating June 2027). Across three industrial internships I've worked on waste-heat-to-power, PV + battery storage feasibility and energy audits at 10 plants.",
      },
      {
        tr: 'Mühendisliği yazılımla birleştirmeyi seviyorum: TS 825:2024 hesaplarını yapan NTherm’i kurdum ve Türkiye’nin gün öncesi elektrik fiyatını makine öğrenmesiyle tahmin eden bir platform geliştiriyorum.',
        en: "I love combining engineering with software: I founded NTherm, a SaaS for TS 825:2024 calculations, and I'm building a platform that forecasts Türkiye's day-ahead electricity price with machine learning.",
      },
    ],
    stats: [
      { value: '3', label: { tr: 'Endüstriyel staj', en: 'Industrial internships' } },
      { value: '10', label: { tr: 'Tesiste enerji etüdü', en: 'Plants audited' } },
      { value: '~20', unit: 'MWth', label: { tr: 'Hesaplanan geri kazanılabilir atık ısı', en: 'Recoverable waste heat calculated' } },
      { value: '4,3', unit: 'MWe', label: { tr: 'Modellenen ORC ünitesi (net)', en: 'ORC unit modeled (net)' } },
    ],
  },

  experience: {
    title: { tr: 'Enerji *yolculuğum*', en: 'My energy *journey*' },
    intro: {
      tr: 'Endüstriyel stajlar, saha etütleri ve takım projeleri; en yeniden en eskiye.',
      en: 'Industrial internships, field audits and team projects, newest first.',
    },
    jobs: [
      {
        start: '09/2026',
        end: null, // null → "Halen" / "Present"
        role: { tr: 'Uzun Dönem Stajyer – Enerji Verimliliği', en: 'Long-Term Intern – Energy Efficiency' },
        company: 'Enerjisa Müşteri Çözümleri',
        note: { tr: '2025 stajının ardından yeniden katıldım', en: 'Rejoined after the 2025 internship' },
        location: { tr: 'İstanbul', en: 'Istanbul' },
        bullets: [
          {
            tr: 'Demir-çelik tesislerinden (tav fırınları, elektrik ark ocakları) proses verisi toplayıp analiz ederek atık ısıdan Organik Rankine Çevrimi (ORC) ile elektrik üretim potansiyelini değerlendiriyor ve raporluyorum.',
            en: 'Collect and analyze process data from iron and steel plants (reheating furnaces, electric arc furnaces) to assess and report the potential for power generation from waste heat with Organic Rankine Cycle (ORC) units.',
          },
          {
            tr: 'Excel çıktılı, mühendislik kontrollü ve kullanım kılavuzlu standart bir veri toplama formu hazırladım; depolama entegreli ark ocağı ORC sistemleri için Microsoft Visio’da P&ID konseptleri çizdim.',
            en: 'Built a standardized data collection form with Excel output, engineering checks and a user guide; drew P&ID concepts for storage-integrated EAF ORC systems in Microsoft Visio.',
          },
        ],
      },
      {
        start: '06/2026',
        end: '08/2026',
        role: {
          tr: 'Mühendislik Stajyeri – Enerji Verimliliği ve Enerji Tedariği',
          en: 'Engineering Intern – Energy Efficiency and Energy Procurement',
        },
        company: 'Capex Enerji',
        note: { tr: 'Enerji verimliliği danışmanlığı', en: 'Energy efficiency consultancy' },
        location: { tr: 'Kocaeli', en: 'Kocaeli' },
        bullets: [
          {
            tr: '10 üretim tesisinde endüstriyel enerji etütleri için sahada veri toplanmasına destek verdim; teknik raporlar için elektrik ve doğal gaz tüketimlerini Excel’de analiz ettim.',
            en: 'Supported on-site data collection for industrial energy audits at 10 manufacturing plants; analyzed electricity and natural gas consumption in Excel for technical reports.',
          },
          {
            tr: 'Beş soğutma kulesi fanının (toplam 37,5 kW, ~281 MWh/yıl) yüksek verimli kompozit fanlarla değiştirilmesi için fizibilite raporu hazırladım: %20–30 enerji tasarrufu; karbon fiber seçeneği ek maliyetini ~1,8 yılda geri ödüyor.',
            en: 'Prepared a feasibility report on replacing five cooling-tower fans (37.5 kW in total, ~281 MWh/yr) with high-efficiency composite fans: 20–30% energy savings; the carbon-fiber option repays its extra cost in ~1.8 years.',
          },
          {
            tr: 'Elektrik ve doğal gaz tedarik tekliflerini karşılaştırdım; elektrik tekliflerini EPİAŞ gün öncesi (PTF), gün içi ve dengeleme piyasası fiyatlarıyla kıyasladım.',
            en: 'Compared electricity and natural gas supply offers; benchmarked electricity offers against EXIST (EPİAŞ) day-ahead (MCP), intraday and balancing market prices.',
          },
          {
            tr: 'Şirketin iki dilli web sitesini (capexenerji.com.tr), bir satış takip PWA’sını ve teklif takip modülünü geliştirdim (PHP, SQLite, JavaScript).',
            en: "Developed the company's bilingual website (capexenerji.com.tr), a sales tracking PWA and a quote tracking module (PHP, SQLite, JavaScript).",
          },
        ],
      },
      {
        start: '06/2025',
        end: '08/2025',
        role: { tr: 'Mühendislik Stajyeri – Enerji Sistemleri', en: 'Engineering Intern – Energy Systems' },
        company: 'Enerjisa Müşteri Çözümleri',
        note: { tr: 'Enerjisa Enerji’nin müşteri çözümleri şirketi', en: 'Customer solutions arm of Enerjisa Enerji' },
        location: { tr: 'İstanbul', en: 'Istanbul' },
        bullets: [
          {
            tr: 'Üç aşamalı bir fizibilite çalışmasında (atık ısı geri kazanımı, GES, depolama) iki fırından ~20 MWth geri kazanılabilir baca gazı ısısı hesapladım ve tek hat şemasıyla birlikte 4,3 MWe (net) bir ORC ünitesi modelledim.',
            en: 'In a three-phase feasibility study (waste heat recovery, PV, storage), calculated ~20 MWth of recoverable flue-gas heat from two furnaces and modeled a 4.3 MWe (net) ORC unit with its single-line diagram.',
          },
          {
            tr: 'HelioScope’ta GES eğim senaryolarını LCOE’ye göre karşılaştırdım (20° önerildi), C-rate/DoD analiziyle batarya depolamayı boyutlandırdım ve ~40 milyon USD’lik proje için Excel fizibilite modeli (CAPEX, OPEX, LCOE, geri ödeme) kurup yöneticilere sundum.',
            en: 'Compared PV tilt scenarios in HelioScope by LCOE (recommended 20°), sized battery storage with C-rate/DoD analysis and built an Excel feasibility model (CAPEX, OPEX, LCOE, payback) for a ~USD 40 million project, presented to managers.',
          },
        ],
      },
      {
        start: '12/2024',
        end: '08/2025',
        role: { tr: 'Batarya & Güç Aktarma Ekibi Üyesi', en: 'Battery & Powertrain Team Member' },
        company: { tr: 'Kocaeli Üniversitesi Formula Student Takımı', en: 'Kocaeli University Formula Student Team' },
        location: { tr: 'Kocaeli', en: 'Kocaeli' },
        bullets: [
          {
            tr: 'Formula SAE Italy 2025’te yarışan elektrikli araç için batarya kutusu sac parçalarını, baraları ve bağlantı elemanlarını 3D CAD’de modelledim, açınım çizimlerini hazırladım ve batarya taşıma arabasını tasarladım.',
            en: 'Modeled battery-case sheet-metal parts, busbars and mounts in 3D CAD, prepared flat-pattern drawings and designed the battery hand cart for the electric car that competed at Formula SAE Italy 2025.',
          },
        ],
      },
    ],

    educationTitle: { tr: 'Eğitim', en: 'Education' },
    education: [
      {
        start: '10/2023',
        end: '06/2027',
        endNote: { tr: 'beklenen', en: 'expected' },
        school: { tr: 'Kocaeli Üniversitesi', en: 'Kocaeli University' },
        degree: { tr: 'Enerji Sistemleri Mühendisliği, Lisans', en: 'B.Sc. in Energy Systems Engineering' },
        details: [
          { tr: 'Genel not ortalaması: 3,20 / 4,00', en: 'GPA: 3.20 / 4.00' },
          {
            tr: 'Bitirme projesi: Türkiye gün öncesi elektrik fiyatının (PTF) makine öğrenmesiyle tahmini',
            en: "Graduation project: machine-learning forecasting of Türkiye's day-ahead electricity price (MCP)",
          },
        ],
      },
    ],

    certificationsTitle: { tr: 'Sertifikalar', en: 'Certifications' },
    certifications: [
      {
        name: {
          tr: 'ISO 50001:2018 Enerji Yönetim Sistemi İç Denetçi Eğitimi',
          en: 'ISO 50001:2018 Energy Management System Internal Auditor Training',
        },
        issuer: 'Capex Enerji',
        date: '02/2026',
      },
      {
        name: { tr: 'Şirket Değerleme ve Yatırım Süreçleri', en: 'Company Valuation and Investment Processes' },
        issuer: 'BTK Akademi',
        date: '04/2025',
      },
      {
        name: { tr: 'Etkili İletişim Stratejileri', en: 'Effective Communication Strategies' },
        issuer: 'BTK Akademi',
        date: '03/2025',
      },
    ],
  },

  skills: {
    title: { tr: 'Mühendislik ve *yazılım* bir arada', en: 'Engineering meets *software*' },
    intro: {
      tr: 'Enerji mühendisliği bilgimi veri ve yazılımla birleştirdiğim araç kutum.',
      en: 'My toolbox, where energy engineering meets data and software.',
    },
    groups: [
      {
        name: { tr: 'Enerji mühendisliği', en: 'Energy engineering' },
        items: [
          { tr: 'Enerji etütleri', en: 'Energy audits' },
          'ISO 50001',
          { tr: 'Atık ısı geri kazanımı (ORC)', en: 'Waste heat recovery (ORC)' },
          { tr: 'GES + BESS fizibilitesi', en: 'PV + BESS feasibility' },
          'LCOE',
          'CAPEX / OPEX',
          'TS 825',
        ],
      },
      {
        name: { tr: 'Enerji piyasaları', en: 'Energy markets' },
        items: [
          { tr: 'EPİAŞ gün öncesi piyasası', en: 'EXIST day-ahead market' },
          { tr: 'Gün içi & dengeleme piyasaları', en: 'Intraday & balancing markets' },
          { tr: 'PTF analizi ve tahmini', en: 'MCP analysis & forecasting' },
          { tr: 'Enerji tedariği', en: 'Energy procurement' },
        ],
      },
      {
        name: { tr: 'Veri & yazılım', en: 'Data & software' },
        items: ['Python', 'pandas', 'scikit-learn', 'XGBoost', 'LightGBM', 'SQL', 'Django', 'Flask', 'JavaScript', 'PHP', 'Git'],
      },
      {
        name: { tr: 'Araçlar', en: 'Tools' },
        items: [
          { tr: 'Excel (ileri, VBA)', en: 'Excel (advanced, VBA)' },
          'PowerPoint',
          'Visio',
          'HelioScope',
          'PVsyst',
          'SolidWorks',
          'Autodesk Inventor',
        ],
      },
    ],
    languagesTitle: { tr: 'Diller', en: 'Languages' },
    languages: [
      { name: { tr: 'Türkçe', en: 'Turkish' }, level: { tr: 'Ana dil', en: 'Native' } },
      { name: { tr: 'İngilizce', en: 'English' }, level: { tr: 'B1 – Orta', en: 'B1 – Intermediate' } },
    ],
    // Sadece Klasik CV sayfasında görünür
    extras: [{ tr: 'B sınıfı sürücü belgesi', en: "Driver's license: Class B" }],
    // Bölümün altında kayan şerit
    marquee: ['ISO 50001', 'ORC', 'PV + BESS', 'LCOE', 'TS 825', 'EPİAŞ', 'Python', 'XGBoost', 'HelioScope', 'PVsyst', 'SolidWorks', 'Excel VBA'],
  },

  projects: {
    title: { tr: 'Kendi *projelerim*', en: "Things I've *built*" },
    intro: {
      tr: 'Mühendislik problemlerini yazılımla çözdüğüm projeler.',
      en: 'Projects where I solve engineering problems with software.',
    },
    items: [
      {
        title: 'NTherm',
        kind: { tr: 'TS 825:2024 bina yalıtım SaaS’ı · Kurucu & geliştirici', en: 'TS 825:2024 building insulation SaaS · Founder & developer' },
        start: '12/2025',
        end: null,
        description: {
          tr: 'TS 825:2024 (Nisan 2025’ten beri zorunlu) için freemium bir SaaS: 997 lokasyon (DG1–DG6) için U değerleri, ısı kayıp/kazançları, ısıtma ihtiyacı ve enerji sınıfı, PDF raporlarla. 3D eleman editörü, NASA POWER iklim verisi, yapay zekâ destekli ısı pompası seçimi ve yoğuşma kontrolleri; Shopier üzerinden Premium plan.',
          en: 'A freemium SaaS for TS 825:2024 (mandatory since 04/2025): U-values, heat losses/gains, heating demand and energy class for 997 locations (DG1–DG6), with PDF reports. 3D element editor, NASA POWER climate data, AI-assisted heat pump selection and condensation checks; Premium plan via Shopier.',
        },
        tags: ['Python / Flask', 'PostgreSQL', 'JavaScript', 'TS 825'],
        links: [{ label: 'ntherm.site', url: 'https://www.ntherm.site/' }],
        visual: 'ntherm', // 'ntherm' | 'chart' | 'web' | ya da görsel yolu: '/images/proje.jpg'
      },
      {
        title: { tr: 'PTF Tahmin Platformu', en: 'MCP Forecasting Platform' },
        kind: { tr: 'Gün öncesi elektrik fiyatı tahmini · Bitirme projesi', en: 'Day-ahead electricity price forecasting · Graduation project' },
        start: '12/2025',
        end: null,
        description: {
          tr: 'EPİAŞ verisiyle ertesi günün 24 saatlik Piyasa Takas Fiyatını (PTF) XGBoost + LightGBM topluluğu ve günlük yeniden eğitim hattıyla tahmin ediyor; başarımı mevsimsel-naif tahmine karşı MAE ile ölçülüyor.',
          en: 'Forecasts next-day hourly market clearing prices (MCP) from EXIST data with an XGBoost + LightGBM ensemble and a daily retraining pipeline, evaluated by MAE against a seasonal-naive baseline.',
        },
        tags: ['Python', 'XGBoost', 'LightGBM', 'Django', 'PostgreSQL'],
        links: [{ label: 'sarjkapisi.com', url: 'https://sarjkapisi.com/' }],
        visual: 'chart',
      },
      {
        title: { tr: 'Capex Enerji Dijital Araçları', en: 'Capex Enerji Digital Tools' },
        kind: { tr: 'Kurumsal web sitesi + satış araçları', en: 'Corporate website + sales tools' },
        start: '06/2026',
        end: '08/2026',
        description: {
          tr: 'Bir enerji verimliliği danışmanlık firması için iki dilli kurumsal web sitesi, sahada kullanılan satış takip PWA’sı ve teklif takip modülü.',
          en: 'A bilingual corporate website for an energy efficiency consultancy, a sales tracking PWA used in the field and a quote tracking module.',
        },
        tags: ['PHP', 'SQLite', 'JavaScript', 'PWA'],
        links: [{ label: 'capexenerji.com.tr', url: 'https://www.capexenerji.com.tr/' }],
        visual: 'web',
      },
    ],
    next: {
      title: { tr: 'Ekibinize *enerji* katmaya hazırım', en: 'Ready to bring *energy* to your team' },
      text: {
        tr: 'Staj, yarı zamanlı ve yeni mezun pozisyonları için konuşalım.',
        en: "Let's talk about internships, part-time and graduate roles.",
      },
    },
  },

  contact: {
    // Parçacıkların oluşturduğu dev kelime (kısa ve BÜYÜK harf olması en iyisi)
    word: { tr: 'MERHABA', en: 'HELLO' },
    title: {
      tr: 'Bir proje, staj ya da iş fırsatı mı var? *Konuşalım.*',
      en: "Have a project, internship or role in mind? *Let's talk.*",
    },
    text: {
      tr: 'Enerji verimliliği, atık ısı geri kazanımı, GES fizibilitesi ya da enerji piyasaları hakkında konuşmak için bana yazabilirsin.',
      en: 'Feel free to reach out about energy efficiency, waste heat recovery, PV feasibility or energy markets.',
    },
  },
};

/* Arayüz metinleri (menü, butonlar vb.) */
export const ui = {
  skip: { tr: 'İçeriğe geç', en: 'Skip to content' },
  home: { tr: 'Ana sayfa', en: 'Home' },
  nav: {
    about: { tr: 'Hakkımda', en: 'About' },
    experience: { tr: 'Deneyim', en: 'Experience' },
    skills: { tr: 'Yetkinlikler', en: 'Skills' },
    projects: { tr: 'Projeler', en: 'Projects' },
    contact: { tr: 'İletişim', en: 'Contact' },
  },
  mainMenu: { tr: 'Ana menü', en: 'Main menu' },
  sections: { tr: 'Bölümler', en: 'Sections' },
  menu: { tr: 'Menü', en: 'Menu' },
  cv: { tr: 'CV', en: 'CV' },
  cvLong: { tr: 'Klasik CV görünümü', en: 'Classic CV view' },
  langSwitch: { tr: 'Switch to English', en: 'Türkçeye geç' },
  viewWork: { tr: 'Deneyimimi gör', en: 'See my experience' },
  viewCv: { tr: 'CV’mi görüntüle', en: 'View my CV' },
  contactMe: { tr: 'İletişime geç', en: 'Get in touch' },
  scroll: { tr: 'Keşfetmek için kaydır', en: 'Scroll to explore' },
  playHint: { tr: 'Parçacıklara tıkla ya da basılı tut', en: 'Click or hold on the particles' },
  localTime: { tr: 'Yerel saat', en: 'Local time' },
  present: { tr: 'Halen', en: 'Present' },
  copy: { tr: 'Kopyala', en: 'Copy' },
  copied: { tr: 'E-posta adresi kopyalandı', en: 'Email address copied' },
  sendMail: { tr: 'E-posta gönder', en: 'Send an email' },
  backToTop: { tr: 'Başa dön', en: 'Back to top' },
  builtWith: { tr: 'Three.js ile tasarlandı ve kodlandı.', en: 'Designed & built with Three.js.' },
  langPrompt: { tr: 'Bu site Türkçe olarak da mevcut.', en: 'This site is also available in English.' },
  langPromptAction: { tr: 'Türkçeye geç', en: 'Switch to English' },
  dismiss: { tr: 'Kapat', en: 'Dismiss' },
  // CV sayfası
  print: { tr: 'PDF olarak kaydet', en: 'Save as PDF' },
  backToSite: { tr: 'Etkileşimli siteye dön', en: 'Back to the interactive site' },
  cvSections: {
    summary: { tr: 'Özet', en: 'Summary' },
    experience: { tr: 'Deneyim', en: 'Experience' },
    education: { tr: 'Eğitim', en: 'Education' },
    certifications: { tr: 'Sertifikalar', en: 'Certifications' },
    skills: { tr: 'Yetkinlikler', en: 'Skills' },
    languages: { tr: 'Diller ve ek bilgiler', en: 'Languages & more' },
    projects: { tr: 'Projeler', en: 'Projects' },
    contact: { tr: 'İletişim', en: 'Contact' },
    links: { tr: 'Bağlantılar', en: 'Links' },
    location: { tr: 'Konum', en: 'Location' },
    email: { tr: 'E-posta', en: 'Email' },
    phone: { tr: 'Telefon', en: 'Phone' },
    web: { tr: 'Web', en: 'Web' },
  },
};
