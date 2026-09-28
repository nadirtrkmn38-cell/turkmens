# Persona Lab – Bright Correct reklam filmi

Dikey (9:16) sosyal medya reklam filmi: Instagram Reels / Story, TikTok, YouTube Shorts.

- **Çıktı:** `cikti/bright-correct-reklam.mp4` (1080×1920, 30 fps, H.264 + AAC, 34,5 sn)
- **Kapak:** `cikti/kapak.jpg`
- **Müzik:** Tamamen sentezle üretilmiş özgün müzik ve ses efektleri, telif sorunu yok (-14 LUFS)

## Senaryo

| Süre | Sahne | Görsel | Sonraki geçiş |
|---|---|---|---|
| 0:00 – 0:04.5 | Açılış: "Bilimin gücü leke karşıtı bakımda." | `kaynak/3.jpg` | Damla dalgası |
| 0:04.5 – 0:07.5 | Ürün adı: "Bright Correct – Leke karşıtı aydınlatıcı serum" | `kaynak/7.jpg` | Damlanın içine bulanık zoom |
| 0:07.5 – 0:13.5 | Çok yönlü aktif sistem + 3 fayda | `kaynak/1.jpg` | Işık patlaması |
| 0:13.5 – 0:19.5 | Aktif içerikler: Niasinamid, Alpha Arbutin, Tranexamic Acid | `kaynak/2.jpg` | Bulanık zoom |
| 0:19.5 – 0:24 | Paraben, alkol, parfüm, renklendirici, sülfat içermez | `kaynak/6.jpg` | Işık patlaması |
| 0:24 – 0:28.5 | Kişiye özel aktif seviyeleri | `kaynak/5.jpg` | Damla dalgası |
| 0:28.5 – 0:34.5 | Kapanış: ürün, logo, slogan | `kaynak/4.jpg` | Kararma |

Görsellerdeki yazılar arka plandan ayrılır (`src/prep.py`). Böylece her satır ayrı ayrı canlanır:
başlıklar bulanıktan netleşerek yükselir, logolar harf aralığı kapanarak gelir, çizgiler
çizilir, ikonlar büyüyerek belirir. Müzik 80 BPM'dir; sahne geçişleri ve yazı girişleri
vuruşlara denk gelir.

## Yeniden üretme

```bash
pip install numpy scipy opencv-python-headless imageio-ffmpeg
cd reklam-filmi/src
python3 film.py                          # görüntü + müzik + birleştirme (~5 dk)
python3 render.py --stills 3,6.5,32 out  # belirli saniyelerden önizleme kareleri
```

| Dosya | Görevi |
|---|---|
| `src/blocks.py` | Görsellerdeki yazı bloklarının koordinatları |
| `src/prep.py` | Yazıyı silip arka planı tamamlama, yazı katmanını ayırma |
| `src/render.py` | Sahneler, kamera hareketleri, yazı animasyonları, geçişler, efektler |
| `src/music.py` | Müzik ve ses efektleri |
| `src/film.py` | Hepsini birleştirip nihai MP4'ü ve kapağı üretir |
