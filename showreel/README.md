# Enerji Tedariği — Motion Reel

[enerjitedarigi.com](https://enerjitedarigi.com) için 30 saniyelik hareketli grafik gösterim videosu (showreel).
Sitenin kendi renkleri (#0e1b2c lacivert, #2356c7 vurgu mavisi, logonun üç açık mavi tonu),
yazı tipleri (Plus Jakarta Sans, Geist, Geist Mono), logosu ve sitedeki metinler kullanıldı.
Müzik ve tüm ses efektleri kod ile sentezlendi (telif sorunu yok).

| Dosya | Format |
| --- | --- |
| `cikti/enerjitedarigi_motion_reel.mp4` | 1920×1080, 60 fps, H.264 + AAC 256 kbps, −14 LUFS |
| `cikti/kapak.jpg` | 1920×1080 kapak görseli |

## Konsept: "Akım"

Müzik 128 BPM; 16 ölçü tam olarak 30,0 saniye eder, böylece her kesme ve geçiş bir vuruşa oturur.
Logonun üç çubuğu filmin görsel dilidir: açılışta üç fazlı elektrik dalgalarına (L1/L2/L3),
geçişlerde paralelkenar maskelere, tünelde ekolayzer şehrine dönüşür.

| Süre | Bölüm | Teknik |
| --- | --- | --- |
| 0–3,75 sn | 01 · Akım | Kıvılcım → osiloskop çizgisi → üç fazlı sinüs → şerit morph ile logo → çubuğun içine zoom |
| 3,75–7,5 sn | 02 · Soru | Her vuruşta başka bir kinetik tipografi: harf düşüşü + eko, whip + yönlü bulanıklık, zıt kesit, 3D split-flap, tipografi duvarı ve tek çizgiye çöküş |
| 7,5–11,25 sn | 03 · Fatura | Çizgiyle açılan fatura, 3D eğim, tarama ve alan tespiti, kartın dönüp "enerji profili"ne dönüşmesi, whip pan |
| 11,25–15 sn | 04 · Talep | Glitch ile unvan gizleme, radar dalgası, lisanslı tedarikçi ağı, geri dönen teklifler, logo biçimli iris geçişi |
| 15–18,75 sn | 05 · Karşılaştırma | Farklı fiyat modelleri tarayıcı çizgiyle aynı ölçeğe "düzleşir", sıralama animasyonu |
| 18,75–22,5 sn | 06 · İlkeler | Logo şeritleriyle silme, 2×2 ızgarada whip pan'ler, "Aynı ölçekte" harflerinin ölçeğe oturması, ızgaranın açığa çıkması |
| 22,5–26,25 sn | 07 · Süreç | Logo çubuklarından, vuruşla zıplayan ekolayzer şehrinin üzerinden uçuş; hızlanan süreç kelimeleri; implozyon |
| 26,25–30 sn | 08 · Marka | Şok dalgası ve kıvılcımlar, yaylı logo, kelime markası kilidi, slogan ve adres |

Her sahnede kamera sarsıntısı, kromatik sapma, yönlü hareket bulanıklığı ve alt kare örneklemeli
hareket bulanıklığı (240 fps render → 60 fps, 4 örnek) kullanılır. Tutarlar ve teklifler temsilî örnektir; videoda da belirtilir.

## Düzenleme ve yeniden üretme

Tüm animasyon `index.html` içindedir; her kare `renderFrame(t)` ile saf bir zaman fonksiyonu olarak çizilir.
Tarayıcıda `index.html?t=12.5` açılarak herhangi bir an görüntülenebilir. Zamanlama vuruş cinsindendir (`b(n)`).

```bash
pip install numpy scipy pyloudnorm imageio-ffmpeg   # müzik + ffmpeg
python3 music.py                                    # music.wav üretir
node render.mjs --sub 4                             # 60 fps video, 4 alt kare hareket bulanıklığı (~11 dk)
node render.mjs --stills 3,10,29.9                  # sadece kontrol kareleri (PNG)
node render.mjs --sheet 0:30:0.5                    # kontrol paftası
```

`ffmpeg` PATH'te değilse `imageio-ffmpeg` içindeki ikili kullanılır ya da yolu `FFMPEG=/yol/ffmpeg` ile verilebilir.
Render, CPU sayısı kadar (en fazla 4) paralel Chromium ile yapılır.
