# nadirturkmen.com

Nadir Türkmen'in kişisel web sitesi ve etkileşimli CV'si.

Sitenin arkasında Three.js ile yapılmış, enerji temalı bir 3D parçacık sahnesi var. Sayfayı kaydırdıkça binlerce parçacık her bölümde başka bir şekle dönüşüyor:

| Bölüm | Şekil |
| --- | --- |
| Giriş | Güneş (kaynayan yüzey, korona, ışık halesi) |
| Hakkımda | Kanatları dönen rüzgar türbinleri |
| Deneyim | Kablolarında enerji akan nakil hattı |
| Yetkinlikler | Elektronları dönen atom |
| Projeler | Üzerinde ışık gezinen GES paneli tarlası |
| İletişim | Parçacıklardan "MERHABA" yazısı |

İmleç parçacıkları iter. Giriş ve iletişim bölümünde tıklamak şok dalgası oluşturur, basılı tutmak ise bir girdap oluşturur.

> Bu klasör Turkmen'S uygulamasından tamamen bağımsızdır, yalnızca aynı depoda durur.

## Bilgisayarında çalıştırma

Node.js 20 veya üstü gerekir.

```bash
cd website
npm install
npm run dev
```

Tarayıcıda `http://localhost:5173` adresini aç. Yayına hazır sürümü üretmek için `npm run build` kullan. Çıktı `dist/` klasörüne yazılır.

## İçeriği düzenleme

Sitedeki ve CV sayfasındaki bütün yazılar tek bir dosyada durur: **`src/content.js`**.

- Çevrilebilir alanlar `{ tr: '…', en: '…' }` biçimindedir.
- Başlıklarda `*yıldız*` içine alınan kelimeler italik ve renkli görünür.
- Boş bırakılan alanlar (`''`) sitede gösterilmez. Örnek: `phone`, sosyal medya bağlantıları.
- **Fotoğraf eklemek için:** fotoğrafı `public/images/nadir.jpg` olarak kaydet ve `profile.photo` alanına `'/images/nadir.jpg'` yaz.
- **Yeni proje eklemek için:** `projects.items` listesine bir öğe ekle. `visual` alanına `'/images/proje.jpg'` gibi bir görsel yolu yazabilirsin.
- **Mezun olduktan sonra:** `profile.role` ve Hakkımda paragrafını güncellemen yeterli.

Renkleri `src/styles/main.css` dosyasında bulabilirsin. Her bölümün parçacık renkleri `--c1` ve `--c2` ile ayarlanır. 3D şekillerin kodu `src/webgl/shapes.js` dosyasındadır.

## Klasik CV sayfası

`/cv.html` aynı içerikten üretilen, A4 düzeninde, yazdırılabilir bir CV'dir. "PDF olarak kaydet" butonu tarayıcının yazdırma penceresini açar.

## Yayına alma (nadirturkmen.com)

1. **Alan adını al.** `nadirturkmen.com` 10 Kasım 2026 itibarıyla kayıtlı değildi. Herhangi bir alan adı firmasından alabilirsin.
2. **Vercel'de yayınla** (önerilen, ücretsiz):
   - vercel.com'a GitHub hesabınla gir ve **Add New → Project** ile bu depoyu seç.
   - **Root Directory** olarak `website` seç. Framework (Vite) otomatik algılanır. Ardından **Deploy**'a bas.
   - Vercel varsayılan olarak `main` dalını yayınlar. Bu yüzden önce siteyi ekleyen PR'ı `main`'e birleştir.
3. **Alan adını bağla:** Vercel'de **Settings → Domains** bölümüne `nadirturkmen.com` ekle. Vercel'in gösterdiği DNS kayıtlarını (A ve CNAME) alan adı firmanın paneline gir. HTTPS sertifikası otomatik gelir.

Netlify kullanmak istersen ayarlar şöyle: Base directory `website`, Build command `npm run build`, Publish directory `website/dist`.

GitHub Pages gibi bir alt klasörde yayınlıyorsan build'i `BASE_PATH=/klasor-adi/ npm run build` ile al.

## Klasör yapısı

```
website/
├── index.html          ana sayfa (içerik build sırasında doldurulur)
├── cv.html             klasik CV sayfası
├── public/             ikonlar, paylaşım görseli, robots.txt, sitemap.xml
└── src/
    ├── content.js      ← bütün yazılar burada
    ├── render.js       içerikten HTML üretir (build ve dil değişimi için)
    ├── main.js         ana sayfa: yükleme ekranı, dil, etkileşimler
    ├── cv-page.js      CV sayfası
    ├── webgl/          3D sahne: World.js, shapes.js, shaders.js
    ├── ui/             menü, kayarak gelme animasyonları, kart efektleri
    └── styles/         main.css, cv.css
```

## Teknik notlar

- Sayfa build sırasında Türkçe olarak hazır HTML'e dönüştürülür. Bu sayede arama motorları içeriği doğrudan okur. İngilizce sürüm `?lang=en` ile açılır.
- Düşük performanslı cihazlarda parçacık sayısı ve çözünürlük otomatik düşer. WebGL desteklenmiyorsa sade bir arka plan gösterilir.
- "Hareketi azalt" ayarı açık olan kullanıcılarda animasyonlar kapanır.
