# Enerji Tedariği — Motion Reel

[enerjitedarigi.com](https://enerjitedarigi.com) için 45 saniyelik hareketli grafik gösterim videosu (showreel).
Sitenin kendi renkleri (#0e1b2c lacivert, #2356c7 vurgu mavisi, logonun üç açık mavi tonu),
yazı tipleri (Plus Jakarta Sans, Geist, Geist Mono), logosu ve sitedeki metinler kullanıldı.
Örnek şirket **Türkmen A.Ş.**; müzik ve tüm ses efektleri kod ile sentezlendi (telif sorunu yok).

| Dosya | Format |
| --- | --- |
| `cikti/enerjitedarigi_motion_reel.mp4` | 16:9 — 1920×1080, 60 fps, H.264 + AAC 256 kbps, −14 LUFS, 45 sn |
| `cikti/enerjitedarigi_motion_reel_9x16.mp4` | 9:16 dikey (Reels / Shorts / TikTok / hikâye) — 1080×1920, 60 fps, aynı müzik, 45 sn |
| `cikti/kapak.jpg`, `cikti/kapak_9x16.jpg` | Kapak görselleri |

## Konsept: "Akım"

Müzik 120 BPM; bir ölçü 2 saniye, her kesme ve geçiş bir vuruşa oturur. Metinler okunabilsin diye
her kelime/başlık ekranda en az bir saniye kalır. Logonun üç çubuğu filmin görsel dilidir:
açılışta üç fazlı elektrik dalgalarına (L1/L2/L3), geçişlerde paralelkenar maskelere ve
sözleşme kontrol kapısına, final öncesinde ekolayzer şehrine dönüşür.

| Süre | Bölüm | Ne anlatıyor / teknik |
| --- | --- | --- |
| 0–4 sn | Akım | Kıvılcım → osiloskop çizgisi → üç fazlı sinüs → şerit morph ile logo → çubuğun içine zoom |
| 4–10 sn | Soru | "Elektrik tedarikçinizi en son ne zaman karşılaştırdınız?" — her kelime 1 sn, her biri başka bir kinetik tipografi tekniğiyle |
| 10–16 sn | Fatura → Profil | Çizgiyle açılan fatura, 3D eğim, alan tespiti, kartın dönüp enerji profiline dönüşmesi |
| 16–22 sn | Talep | Türkmen A.Ş. unvanı glitch ile "UNVAN GİZLİ" olur; lisanslı tedarikçilere radar/ağ, geri dönen teklifler |
| 22–28 sn | Karşılaştırma | Farklı fiyat modelleri tarayıcı çizgiyle aynı ölçeğe "düzleşir", sıralama |
| **28–36 sn** | **Sözleşme + Fatura takibi** | Seçilen teklif satırı sözleşmeye dönüşür, imza ve "İMZALANDI" damgası; ardından her ayın faturası sözleşme kontrol kapısından geçer, Ağustos'ta %7,4 fark yakalanır ve bildirim gelir |
| 36–40 sn | Değerler | Ekolayzer şehri üzerinden uçuş: ÜCRETSİZ · ANONİM · LİSANSLI · **FATURA TAKİBİ** |
| 40–45 sn | Marka | Şok dalgası, yaylı logo, kelime markası kilidi, "Sözleşme sonrası fatura takibi" vurgusu, adres |

Kamera sarsıntısı, kromatik sapma, yönlü hareket bulanıklığı ve alt kare örneklemeli
hareket bulanıklığı (240 fps render → 60 fps, 4 örnek) kullanılır. Tutarlar ve teklifler temsilî örnektir; videoda da belirtilir.

### 9:16 dikey sürüm

Aynı animasyon ve aynı zamanlama; yerleşim dikey kadraja göre yeniden kuruldu. Başlıklar iki satıra bölünür,
fatura/profil, talep ve tedarikçi kartları, aylık fatura bandı ve bildirim telefonda okunabilsin diye büyütülür
(`zoom` ile, metin gerçek boyutunda çizilir). Final kartında logo üstte, kelime markası altta durur;
"Sözleşme sonrası fatura takibi" etiketi kendi satırında öne çıkar.

## Düzenleme ve yeniden üretme

Tüm animasyon `index.html` içindedir; her kare `renderFrame(t)` ile saf bir zaman fonksiyonu olarak çizilir.
Tarayıcıda `index.html?t=12.5` (dikey için `index.html?format=9x16&t=12.5`) açılarak herhangi bir an görüntülenebilir.
Sahne sınırları `SC`, fatura takibi zamanları `T6`, biçime göre değişen konum ve ölçüler `G` nesnesindedir;
müzikteki karşılıkları `music.py` içinde aynı saniyelerdir.

```bash
pip install numpy scipy pyloudnorm imageio-ffmpeg   # müzik + ffmpeg
python3 music.py                                    # music.wav üretir
node render.mjs --sub 4                             # 16:9, 60 fps, 4 alt kare hareket bulanıklığı (~16 dk)
node render.mjs --format 9x16 --sub 4               # 9:16 dikey sürüm (~13 dk)
node render.mjs --stills 3,10,44.9                  # sadece kontrol kareleri (PNG); --format 9x16 ile dikey
node render.mjs --sheet 0:45:0.5                    # kontrol paftası
```

`ffmpeg` PATH'te değilse `imageio-ffmpeg` içindeki ikili kullanılır ya da yolu `FFMPEG=/yol/ffmpeg` ile verilebilir.
Render, CPU sayısı kadar (en fazla 4) paralel Chromium ile yapılır.
