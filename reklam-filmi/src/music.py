# Bright Correct reklam filmi - özgün (telifsiz) müzik ve ses efektleri
#
# Tamamen sentezle üretilir: pad akorlar, FM "e-piano" arpej, çan sesleri, yumuşak davul,
# damla / geçiş (whoosh) / parıltı efektleri ve konvolüsyon yankı.
# Tempo 80 BPM (vuruş = 0.75 sn); sahne geçişleri ve yazı girişleri bu ızgaraya oturur.
#
# Kullanım: python3 music.py  -> cikti/ara/muzik.wav (48 kHz, stereo, 24 bit)
import os
import wave

import numpy as np
from scipy.signal import butter, fftconvolve, sosfilt

from prep import ROOT

SR = 48000
DUR = 34.5
N = int(round(DUR * SR))
BEAT = 0.75
EIGHTH = BEAT / 2
rng = np.random.default_rng(11)

# (başlangıç, bas notası, pad notaları) - MIDI numaraları, D majör
CHORDS = [
    (0.0, 38, [57, 61, 64, 66, 69]),     # Dmaj9     - damlalık
    (4.5, 35, [54, 57, 61, 62, 66]),     # Bm9       - "Bright Correct"
    (7.5, 31, [54, 57, 59, 62, 66]),     # Gmaj9     - faydalar
    (10.5, 40, [55, 59, 62, 66, 69]),    # Em9
    (13.5, 42, [57, 62, 64, 66, 69]),    # D/F#      - içerikler
    (16.5, 31, [54, 59, 62, 66, 71]),    # Gmaj7
    (19.5, 35, [54, 57, 61, 62, 66]),    # Bm9       - içermez listesi
    (22.5, 42, [57, 61, 64, 66, 69]),    # F#m7
    (24.0, 31, [54, 57, 59, 62, 66]),    # Gmaj9     - kişiselleştirme
    (25.5, 33, [57, 62, 64, 69, 71]),    # Asus4
    (27.0, 33, [57, 61, 64, 66, 69]),    # A6
    (28.5, 38, [57, 61, 64, 66, 69]),    # Dmaj9     - kapanış
    (31.5, 38, [55, 59, 62, 66, 71]),    # Gmaj9/D
    (33.0, 38, [54, 57, 61, 64, 69]),    # Dmaj9
]


def chord_at(t):
    cur = CHORDS[0]
    for c in CHORDS:
        if c[0] <= t + 1e-6:
            cur = c
    return cur


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12.0)


def bus():
    return np.zeros((2, N))


def pan2(x, pan):
    a = (pan + 1) * np.pi / 4
    return np.vstack([x * np.cos(a), x * np.sin(a)])


def add(b, sig, t0, pan=0.0, gain=1.0):
    if sig.ndim == 1:
        sig = pan2(sig, pan)
    i0 = int(round(t0 * SR))
    s0 = max(0, -i0)
    i0 = max(0, i0)
    n = min(sig.shape[1] - s0, N - i0)
    if n > 0:
        b[:, i0:i0 + n] += sig[:, s0:s0 + n] * gain


def lp(x, fc, order=2):
    return sosfilt(butter(order, fc / (SR / 2), output='sos'), x, axis=-1)


def hp(x, fc, order=2):
    return sosfilt(butter(order, fc / (SR / 2), btype='high', output='sos'), x, axis=-1)


def bp(x, lo, hi, order=2):
    return sosfilt(butter(order, [lo / (SR / 2), hi / (SR / 2)], btype='band', output='sos'), x, axis=-1)


def fade_env(n, att, rel, hold):
    t = np.arange(n) / SR
    a = np.clip(t / att, 0, 1) if att > 0 else np.ones(n)
    a = 0.5 - 0.5 * np.cos(np.pi * a)
    r = np.clip((t - hold) / rel, 0, 1)
    return a * (0.5 + 0.5 * np.cos(np.pi * r))


# --- Enstrümanlar ---
TABLE = 4096


def saw_table(f0, fc):
    K = max(1, int(min(9000.0, SR * 0.45) / f0))
    ph = np.arange(TABLE) / TABLE
    tab = np.zeros(TABLE)
    for k in range(1, K + 1):
        tab += (1.0 / k) / (1.0 + (k * f0 / fc) ** 2) * np.sin(2 * np.pi * k * ph)
    return tab / np.abs(tab).max()


def osc(tab, freq, n, phase0):
    ph = (phase0 + np.cumsum(np.broadcast_to(freq, (n,)) / SR)) % 1.0
    idx = ph * TABLE
    i = idx.astype(np.int64)
    fr = idx - i
    return tab[i % TABLE] * (1 - fr) + tab[(i + 1) % TABLE] * fr


def pad_note(m, hold, att=0.8, rel=1.8, fc=1500.0):
    f = hz(m)
    n = int((hold + rel) * SR)
    t = np.arange(n) / SR
    tab = saw_table(f, fc)
    out = np.zeros((2, n))
    for v, (det, pan) in enumerate(((-7.0, -0.65), (0.0, 0.0), (7.0, 0.65))):
        drift = 2.5 * np.sin(2 * np.pi * rng.uniform(0.08, 0.2) * t + rng.uniform(0, 6.3))
        fv = f * 2 ** ((det + drift) / 1200)
        out += pan2(osc(tab, fv, n, rng.uniform()), pan)
    return out * fade_env(n, att, rel, hold) / 3


def air_note(m, hold, att=1.2, rel=2.0):
    n = int((hold + rel) * SR)
    t = np.arange(n) / SR
    s = np.sin(2 * np.pi * hz(m) * t + 0.4 * np.sin(2 * np.pi * 5.1 * t)) * (0.8 + 0.2 * np.sin(2 * np.pi * 0.23 * t))
    return s * fade_env(n, att, rel, hold)


def bass_note(m, hold, rel=0.7):
    f = hz(m)
    n = int((hold + rel) * SR)
    t = np.arange(n) / SR
    s = np.sin(2 * np.pi * f * t) + 0.3 * np.sin(4 * np.pi * f * t) + 0.08 * np.sin(6 * np.pi * f * t)
    s = np.tanh(1.4 * s) / 1.4
    return s * fade_env(n, 0.12, rel, hold)


def pluck(m, vel):
    f = hz(m)
    n = int(2.2 * SR)
    t = np.arange(n) / SR
    I = 1.5 * np.exp(-t / 0.16) + 0.22
    car = np.sin(2 * np.pi * f * t + I * np.sin(2 * np.pi * f * t))
    tine = 0.16 * np.sin(2 * np.pi * 4.0 * f * t) * np.exp(-t / 0.045)
    amp = (0.72 * np.exp(-t / 0.6) + 0.28 * np.exp(-t / 0.1)) * (1 - np.exp(-t / 0.003))
    return (car + tine) * amp * vel


def bell(m, vel, decay=1.0):
    f = hz(m)
    n = int(3.5 * SR)
    t = np.arange(n) / SR
    s = np.zeros(n)
    for r, a, d in ((1.0, 1.0, 1.4), (2.0, 0.42, 0.8), (3.0, 0.22, 0.55), (4.16, 0.18, 0.3),
                    (5.43, 0.1, 0.22), (6.79, 0.05, 0.15)):
        if f * r < SR * 0.45:
            s += a * np.sin(2 * np.pi * f * r * t + rng.uniform(0, 6.3)) * np.exp(-t / (d * decay))
    return s * (1 - np.exp(-t / 0.0015)) * vel


def kick(vel):
    n = int(0.7 * SR)
    t = np.arange(n) / SR
    f = 46 + 62 * np.exp(-t / 0.04)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.3) * (1 - np.exp(-t / 0.002))
    click = hp(rng.standard_normal(n), 1500) * np.exp(-t / 0.004) * 0.08
    return (s + click) * vel


def shaker(vel):
    n = int(0.09 * SR)
    t = np.arange(n) / SR
    s = bp(rng.standard_normal(n), 5000, 11000)
    return s * (1 - np.exp(-t / 0.004)) * np.exp(-t / 0.02) * vel


def droplet():
    # su damlası: hızla yükselen kısa ton + gövde
    n = int(0.5 * SR)
    t = np.arange(n) / SR
    f1 = 900 + 1400 * (1 - np.exp(-t / 0.009))
    s = np.sin(2 * np.pi * np.cumsum(f1) / SR) * np.exp(-t / 0.035) * (1 - np.exp(-t / 0.0008))
    f2 = 320 + 260 * (1 - np.exp(-t / 0.02))
    s += 0.5 * np.sin(2 * np.pi * np.cumsum(f2) / SR) * np.exp(-t / 0.07) * (1 - np.exp(-t / 0.002))
    t3 = np.clip(t - 0.06, 0, None)
    f3 = 1500 + 900 * (1 - np.exp(-t3 / 0.008))
    s += 0.25 * np.sin(2 * np.pi * np.cumsum(f3) / SR) * np.exp(-t3 / 0.03) * (t > 0.06)
    return s


def sweep_noise(dur, lo0, hi0, lo1, hi1, shape, block=512):
    """Zamanla kayan bant geçiren gürültü (whoosh / riser)."""
    n = int(dur * SR)
    x = rng.standard_normal(n)
    out = np.zeros(n)
    zi = np.zeros((2, 2))
    for i in range(0, n, block):
        u = shape(i / n)
        lo = lo0 * (lo1 / lo0) ** u
        hi = hi0 * (hi1 / hi0) ** u
        sos = butter(2, [lo / (SR / 2), min(hi, SR * 0.45) / (SR / 2)], btype='band', output='sos')
        out[i:i + block], zi = sosfilt(sos, x[i:i + block], zi=zi)
    return out


def whoosh(dur=1.0, peak=0.5):
    n = int(dur * SR)
    u = np.arange(n) / n
    tri = lambda v: v / peak if v < peak else (1 - v) / (1 - peak)
    s = sweep_noise(dur, 250, 900, 1400, 7000, lambda v: tri(v))
    env = np.where(u < peak, (u / peak) ** 2.2, np.exp(-(u - peak) / (1 - peak) * 4.0))
    s = s * env
    p = np.linspace(-0.6, 0.6, n)
    a = (p + 1) * np.pi / 4
    return np.vstack([s * np.cos(a), s * np.sin(a)])


def riser(dur):
    n = int(dur * SR)
    u = np.arange(n) / n
    s = sweep_noise(dur, 300, 900, 3500, 12000, lambda v: v ** 1.5) * u ** 2.5
    t = np.arange(n) / SR
    f = hz(57) * 2 ** (u ** 1.8)
    s += 0.25 * np.sin(2 * np.pi * np.cumsum(f) / SR) * u ** 2 * (1 + 0.2 * np.sin(2 * np.pi * 6 * t))
    return s


def impact():
    n = int(2.4 * SR)
    t = np.arange(n) / SR
    f = 38 + 30 * np.exp(-t / 0.12)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.7) * (1 - np.exp(-t / 0.004))
    s += lp(rng.standard_normal(n), 900) * np.exp(-t / 0.12) * 0.35
    return s


def make_ir(dur=3.4, rt60=3.0, pre=0.022):
    n = int(dur * SR)
    t = np.arange(n) / SR
    ir = np.zeros((2, n))
    for c in range(2):
        x = rng.standard_normal(n)
        dark = lp(x, 2500)
        mix = np.exp(-t / 0.5)
        ir[c] = (x * mix + dark * (1 - mix) * 1.6) * np.exp(-6.9 * t / rt60) * (1 - np.exp(-t / 0.012))
        for _ in range(14):
            k = int(rng.uniform(0.004, 0.07) * SR)
            ir[c, k] += rng.uniform(-1.2, 1.2)
    ir = np.pad(ir, ((0, 0), (int(pre * SR), 0)))
    return ir / np.sqrt((ir ** 2).sum() / 2)


def reverb(x, ir):
    y = np.vstack([fftconvolve(x[0], ir[0])[:N], fftconvolve(x[1], ir[1])[:N]])
    return y


def pingpong(x, d=EIGHTH * 1.5, fb=0.4, taps=6):
    mono = x.mean(axis=0)
    out = np.zeros_like(x)
    k = int(round(d * SR))
    for i in range(1, taps + 1):
        g = fb ** (i - 1)
        sh = k * i
        out[i % 2, sh:] += mono[:-sh] * g
    return lp(out, 3500)


def build():
    pad, air, bass, keys, bells, drums, sfx = (bus() for _ in range(7))

    # Pad + bas: akor değişimleri sahne geçişlerine oturur
    for i, (t0, b, notes) in enumerate(CHORDS):
        t1 = CHORDS[i + 1][0] if i + 1 < len(CHORDS) else DUR
        hold = t1 - t0 + 0.15
        lvl = 0.75 if t0 < 4.5 else (1.15 if t0 >= 28.5 else 1.0)
        for j, m in enumerate(notes):
            add(pad, pad_note(m, hold, att=0.9 if i == 0 else 0.7, fc=1300 if t0 < 4.5 else 1700), t0 - 0.12,
                gain=lvl * (0.9 if j == 0 else 1.0))
        add(air, air_note(notes[-1] + 12, hold), t0 - 0.1, pan=0.3 if i % 2 else -0.3, gain=lvl)
        if t0 >= 4.5:
            add(bass, bass_note(b, hold - 0.1), t0)

    # Arpej (sekizlik) - 4.5 ile 28.5 arası
    pattern = [0, 2, 4, 1, 3, 4, 2, 1]
    vels = [0.95, 0.55, 0.75, 0.5, 0.85, 0.55, 0.7, 0.5]
    accents = {round(20.25 + 0.375 * i, 3) for i in range(6)}
    k = 0
    t = 4.5
    while t < 28.5 - 1e-6:
        _, _, notes = chord_at(t)
        up = sorted(m + 12 for m in notes)
        m = up[pattern[k % 8] % len(up)]
        v = vels[k % 8] * rng.uniform(0.92, 1.05)
        if round(t, 3) in accents:
            v *= 1.25
        build_up = 0.75 + 0.25 * min(1.0, (t - 4.5) / 12.0)
        add(keys, pluck(m, v * build_up), t, pan=0.25 if k % 2 else -0.25)
        if t >= 13.5 and k % 4 == 2:
            add(keys, pluck(m + 12, 0.28 * v), t + 0.004, pan=0.5)
        k += 1
        t += EIGHTH

    # Yazı girişlerine denk gelen çan notaları (sahne tipografisi ile senkron)
    for (tb, m, v) in [(0.375, 81, 0.35), (1.125, 78, 0.55), (1.5, 81, 0.5), (1.875, 76, 0.5), (2.4375, 74, 0.3),
                       (5.25, 86, 0.6), (5.625, 81, 0.5), (6.0, 78, 0.3),
                       (8.25, 83, 0.35), (8.625, 79, 0.4), (9.75, 83, 0.45), (10.5, 86, 0.45), (11.25, 88, 0.45),
                       (13.875, 81, 0.45), (15.375, 85, 0.45), (16.875, 88, 0.45),
                       (24.75, 83, 0.45), (25.875, 86, 0.35), (26.25, 88, 0.35), (26.625, 90, 0.35),
                       (29.625, 86, 0.6), (29.8125, 81, 0.45), (30.375, 78, 0.35), (31.125, 76, 0.4),
                       (33.0, 74, 0.55), (33.0, 86, 0.3)]:
        add(bells, bell(m, v), tb, pan=rng.uniform(-0.4, 0.4))

    # Parıltı "ting"leri (görseldeki yıldız parlamaları)
    for tg in (2.8125, 3.375, 4.125, 6.5625, 22.5, 32.25, 32.625, 33.0):
        add(bells, bell(93 + int(rng.integers(0, 3)) * 2, 0.16, decay=0.4), tg - 0.02, pan=rng.uniform(-0.6, 0.6))

    # Işık süpürmesi: yükselen parıltı glissandosu
    penta = [74, 76, 78, 81, 83]
    for tb0, cnt in ((5.25, 10), (31.875, 16)):
        for i in range(cnt):
            m = penta[i % 5] + 12 * (1 + i // 5)
            add(bells, bell(m, 0.12 + 0.1 * (i / cnt), decay=0.5), tb0 + i * 0.065, pan=-0.7 + 1.4 * i / cnt)

    # Davul: yumuşak kick (7.5 - 28.5), shaker (13.5 - 28.5)
    t = 7.5
    while t < 28.5 - 1e-6:
        beat = int(round((t - 1.5) / BEAT)) % 4
        if beat in (0, 2):
            add(drums, kick(0.95 if beat == 0 else 0.75), t)
        if t >= 13.5:
            add(drums, shaker(0.5), t + EIGHTH, pan=0.35)
            add(drums, shaker(0.28), t, pan=-0.35)
        t += BEAT

    # Efektler
    add(sfx, droplet(), 4.5, pan=0.05, gain=1.0)
    add(sfx, droplet(), 28.5, pan=0.0, gain=1.1)
    for tc in (7.5, 19.5):
        add(sfx, whoosh(1.2, 0.55), tc - 0.66, gain=0.8)
    for tc in (13.5, 24.0):
        add(sfx, whoosh(1.4, 0.6), tc - 0.84, gain=0.45)
        for i in range(14):
            add(bells, bell(int(rng.choice([86, 88, 90, 93, 95, 98])), 0.07, decay=0.45),
                tc - 0.5 + rng.uniform(0, 1.2), pan=rng.uniform(-0.8, 0.8))
    add(sfx, whoosh(1.1, 0.25), 4.52, gain=0.35)
    add(sfx, whoosh(1.1, 0.25), 28.52, gain=0.35)
    add(sfx, impact(), 5.25, gain=0.45)
    add(sfx, impact(), 28.5, gain=0.8)
    r = riser(2.25)
    add(sfx, r, 28.5 - 2.25, pan=0.0, gain=0.55)

    # Karışım
    pad = hp(lp(pad, 3200), 110)
    keys = lp(keys, 6000)
    ir = make_ir()
    mix = (pad * 0.20 + air * 0.035 + bass * 0.17 + keys * 0.12 + bells * 0.09 + drums * 0.26 + sfx * 0.22)
    send = pad * 0.07 + keys * 0.06 + bells * 0.10 + sfx * 0.08 + air * 0.02
    mix = mix + reverb(send, ir) * 0.55 + pingpong(keys) * 0.035
    mix = hp(mix, 28)

    # Giriş ve çıkış
    t = np.arange(N) / SR
    fade = np.clip(t / 0.25, 0, 1) * np.clip((DUR - t) / 1.6, 0, 1) ** 1.5
    mix *= fade
    mix /= np.abs(mix).max()
    mix = np.tanh(mix * 1.3) / np.tanh(1.3) * 0.89
    return mix


def write_wav(path, x):
    x = np.clip(x, -1, 1)
    pcm = (x.T * (2 ** 23 - 1)).astype(np.int32)
    b = np.zeros((pcm.shape[0], 2, 3), np.uint8)
    for c in range(2):
        v = pcm[:, c]
        b[:, c, 0] = v & 0xFF
        b[:, c, 1] = (v >> 8) & 0xFF
        b[:, c, 2] = (v >> 16) & 0xFF
    with wave.open(path, 'wb') as w:
        w.setnchannels(2)
        w.setsampwidth(3)
        w.setframerate(SR)
        w.writeframes(b.tobytes())


if __name__ == '__main__':
    out = os.path.join(ROOT, 'cikti', 'ara')
    os.makedirs(out, exist_ok=True)
    mix = build()
    write_wav(os.path.join(out, 'muzik.wav'), mix)
    rms = np.sqrt((mix ** 2).mean())
    print('muzik.wav yazıldı; tepe', round(float(np.abs(mix).max()), 3), 'rms dBFS', round(float(20 * np.log10(rms)), 1))
