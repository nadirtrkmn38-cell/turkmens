# Enerji Tedariği — Reklam Filmi

[enerjitedarigi.com](https://enerjitedarigi.com) için 33 saniyelik tanıtım videosu.
Sitenin kendi renkleri (#0e1b2c lacivert, #2356c7 vurgu mavisi), yazı tipleri (Plus Jakarta Sans, Geist),
logosu ve sitedeki metinler/örnek değerler kullanıldı. Müzik ve efektler kod ile sentezlendi (telif sorunu yok).

| Dosya | Format | Kullanım |
| --- | --- | --- |
| `cikti/enerjitedarigi_reklam_16x9.mp4` | 1920×1080, 30 fps, H.264 + AAC | YouTube, web sitesi, LinkedIn |
| `cikti/enerjitedarigi_reklam_9x16.mp4` | 1080×1920, 30 fps, H.264 + AAC | Instagram Reels/Story, TikTok, YouTube Shorts |

Ses seviyesi −15 LUFS. Sessiz izlemede de anlaşılır olsun diye tüm mesajlar ekranda yazılı.

## Senaryo

| Süre | Sahne | Ekrandaki mesaj |
| --- | --- | --- |
| 0–4 sn | Açılış | "Elektrik tedarikçinizi en son ne zaman karşılaştırdınız?" |
| 4–9 sn | 01 · Fatura | Fatura yüklenir, tüketim profili (203.460 kWh, 2,4 GWh/yıl) otomatik çıkar |
| 9–14 sn | 02 · Anonim talep | Firma unvanı gizlenir, talep lisansı doğrulanmış tedarikçilere gider |
| 14–20 sn | 03 · Karşılaştırma | PTF endeksli / tarife indirimli / sabit teklifler aynı ölçeğe çevrilip sıralanır |
| 20–24,5 sn | 04 · Takip | Fatura sözleşmeyle karşılaştırılır, %7,4 fark bildirimi gelir |
| 24,5–28 sn | Güven | Ücretsiz · Anonim talep · Lisanslı tedarikçiler |
| 28–33 sn | Kapanış | Logo, "Ücretsiz teklif almaya başlayın", enerjitedarigi.com, yasal not |

Tutarlar sitedeki "temsilî örnek" değerlerdir; videoda da temsilî/tahmini olduğu belirtilir.

## Düzenleme ve yeniden üretme

Metinler, renkler ve zamanlama `index.html` içindedir (her sahnenin süresi `S` nesnesinde).
Tarayıcıda `index.html` açılıp konsolda `renderFrame(12.5)` ile herhangi bir an görüntülenebilir.

```bash
pip install numpy scipy pyloudnorm   # müzik için
python3 music.py                     # music.wav üretir
node render.mjs                      # 16:9 video  (Playwright + ffmpeg gerekir)
node render.mjs --format 9x16        # dikey video
node render.mjs --stills 3,10,30     # sadece kontrol kareleri (PNG)
```

`ffmpeg` PATH'te değilse yolunu `FFMPEG=/yol/ffmpeg` ile verin.
