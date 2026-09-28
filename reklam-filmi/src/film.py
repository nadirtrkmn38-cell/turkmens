# Bright Correct reklam filmini baştan sona üretir:
#   görüntü (render.py) + müzik (music.py) -> ses normalizasyonu -> birleştirme -> kapak
#
# Kullanım: python3 film.py
#   Çıktı: cikti/bright-correct-reklam.mp4  (1080x1920, 30 fps, H.264 + AAC)
#          cikti/kapak.jpg                  (Reels/TikTok kapak görseli)
import json
import os
import subprocess
import sys

import cv2

import music
import render

OUT = render.OUT_DIR
TMP = os.path.join(OUT, 'ara')
COVER_T = 33.4


def run(cmd):
    return subprocess.run(cmd, check=True, capture_output=True, text=True)


def loudnorm(src, dst, target=-14.0, tp=-1.5):
    ff = render.ffmpeg_exe()
    flt = f'loudnorm=I={target}:TP={tp}:LRA=11'
    r = run([ff, '-hide_banner', '-i', src, '-af', flt + ':print_format=json', '-f', 'null', '-'])
    m = json.loads(r.stderr[r.stderr.rindex('{'):r.stderr.rindex('}') + 1])
    flt += (f":measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}"
            f":measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
    run([ff, '-hide_banner', '-y', '-i', src, '-af', flt, '-ar', '48000', '-c:a', 'pcm_s24le', dst])
    print('ses:', m['input_i'], 'LUFS ->', target, 'LUFS')


def main():
    os.makedirs(TMP, exist_ok=True)
    if '--ses' not in sys.argv:
        render.main()
    else:
        render.init()
    mix = music.build()
    music.write_wav(os.path.join(TMP, 'muzik.wav'), mix)
    loudnorm(os.path.join(TMP, 'muzik.wav'), os.path.join(TMP, 'muzik_norm.wav'))
    final = os.path.join(OUT, 'bright-correct-reklam.mp4')
    run([render.ffmpeg_exe(), '-hide_banner', '-y', '-i', os.path.join(TMP, 'video.mp4'),
         '-i', os.path.join(TMP, 'muzik_norm.wav'), '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
         '-c:a', 'aac', '-b:a', '256k', '-ar', '48000', '-shortest', '-movflags', '+faststart', final])
    img = render.post(render.compose(COVER_T, render.SCENES), COVER_T)
    cv2.imwrite(os.path.join(OUT, 'kapak.jpg'), cv2.cvtColor(img, cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 95])
    print('hazır:', final)


if __name__ == '__main__':
    main()
