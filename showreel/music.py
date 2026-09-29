"""Enerji Tedariği — Motion Reel müziği ve ses tasarımı.

Tamamen kod ile sentezlenir (telif sorunu yoktur). 120 BPM, 1 ölçü = 2 sn, toplam 45 sn.
Si minör: Bm-G | Bm-G-A | D-A-Bm | G-D-A | Bm-G-D | A-Bm-Em-F# | G-A | D (final).
Tüm ses efektleri index.html'deki görsel olaylarla aynı zamanlara oturur.

Kullanım:  python3 music.py   ->  music.wav (48 kHz, stereo, 16-bit, -14 LUFS)
Gerekenler: numpy, scipy, (opsiyonel) pyloudnorm
"""
import numpy as np
from scipy import signal
from scipy.io import wavfile

SR = 48000
DUR = 45.0
N = int(SR * DUR)
BPM = 120
BT = 60 / BPM
rng = np.random.default_rng(26)


def b(n):
    return n * BT


def mtof(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def tt(dur):
    return np.arange(int(dur * SR)) / SR


def bus():
    return np.zeros((2, N))


def add(bu, start, sig, pan=0.0, gain=1.0):
    i = int(round(start * SR))
    if sig.ndim == 1:
        a = (np.clip(pan, -1, 1) + 1) * np.pi / 4
        sig = np.vstack([sig * np.cos(a), sig * np.sin(a)]) * np.sqrt(2)
    if i < 0:
        sig = sig[:, -i:]
        i = 0
    if i >= N:
        return
    n = min(sig.shape[1], N - i)
    bu[:, i:i + n] += gain * sig[:, :n]


def butter(x, fc, kind='low', order=2):
    fc = np.clip(fc, 20, SR / 2 - 100)
    sos = signal.butter(order, np.array(fc) / (SR / 2), kind, output='sos')
    return signal.sosfilt(sos, x, axis=-1)


def bp(x, lo, hi, order=2):
    sos = signal.butter(order, [lo / (SR / 2), hi / (SR / 2)], 'band', output='sos')
    return signal.sosfilt(sos, x, axis=-1)


def lp_sweep(x, fcs, block=256, q=.707):
    """Zamanla değişen 2. derece alçak geçiren (blok blok, durum korunur)."""
    x = np.atleast_2d(x)
    y = np.zeros_like(x)
    zi = np.zeros((x.shape[0], 1, 2))
    for s in range(0, x.shape[1], block):
        fc = float(np.clip(fcs[min(s, len(fcs) - 1)], 30, SR / 2.2))
        sos = signal.butter(2, fc / (SR / 2), 'low', output='sos')
        for c in range(x.shape[0]):
            y[c, s:s + block], zi[c] = signal.sosfilt(sos, x[c, s:s + block], zi=zi[c])
    return y if y.shape[0] > 1 else y[0]


def svf_bp(x, fcs, q=1.2):
    """Zamanla değişen band geçiren (state variable filter)."""
    y = np.zeros_like(x)
    low = band = 0.0
    damp = 1.0 / q
    for i in range(len(x)):
        f = 2 * np.sin(np.pi * min(fcs[i], SR / 6) / SR)
        high = x[i] - low - damp * band
        band += f * high
        low += f * band
        y[i] = band
    return y


def saw(f, n, ph0=None):
    """PolyBLEP testere dişi (aliasing'i azaltılmış)."""
    dt = f / SR
    ph = ((rng.random() if ph0 is None else ph0) + dt * np.arange(n)) % 1.0
    s = 2 * ph - 1
    m = ph < dt
    x = ph[m] / dt
    s[m] -= x + x - x * x - 1
    m = ph > 1 - dt
    x = (ph[m] - 1) / dt
    s[m] -= x * x + x + x + 1
    return s


def supersaw(notes, dur, voices=7, cents=16, width=.9):
    n = int(dur * SR)
    L = np.zeros(n)
    R = np.zeros(n)
    for m in notes:
        f = mtof(m)
        for v in range(voices):
            d = (v - (voices - 1) / 2) / ((voices - 1) / 2)
            s = saw(f * 2 ** (d * cents / 1200), n)
            a = (d * width + 1) * np.pi / 4
            L += s * np.cos(a)
            R += s * np.sin(a)
    return np.vstack([L, R]) / (len(notes) * np.sqrt(voices))


def env_adsr(n, a=.005, d=.1, s=.6, r=.2, hold=None):
    t = np.arange(n) / SR
    hold = (n / SR - r) if hold is None else hold
    e = np.where(t < a, t / max(a, 1e-6), s + (1 - s) * np.exp(-(t - a) / max(d, 1e-6)))
    rel = np.clip(1 - (t - hold) / max(r, 1e-6), 0, 1)
    return e * np.where(t > hold, rel, 1)


# ================================================================== buses
KICK, SNARE, HATS, BASS, PAD, STAB, ARP, FX, UI, CHIME = (bus() for _ in range(10))

# ================================================================== harmony
BM, G_, D_, A_ = [59, 62, 66, 69], [55, 59, 62, 66], [57, 62, 66, 69], [57, 61, 64, 69]
EM, FS = [55, 59, 64, 67], [54, 58, 61, 66]
ROOT = {'Bm': 47, 'G': 43, 'D': 50, 'A': 45, 'Em': 40, 'F#': 42}
VOX = {'Bm': BM, 'G': G_, 'D': D_, 'A': A_, 'Em': EM, 'F#': FS}
PROG = ['Bm', 'G',                    # 0-4    akım
        'Bm', 'G', 'A',               # 4-10   soru
        'D', 'A', 'Bm',               # 10-16  fatura
        'G', 'D', 'A',                # 16-22  talep
        'Bm', 'G', 'D',               # 22-28  karşılaştırma
        'A', 'Bm', 'Em', 'F#',        # 28-36  sözleşme + fatura takibi
        'G', 'A',                     # 36-40  değerler
        'D', 'D', 'D']                # 40-46  marka


def chord_at(beat):
    return PROG[min(len(PROG) - 1, int(beat // 4))]


# ================================================================== drums
def kick(dur=.42, punch=1.0):
    t = tt(dur)
    f = 44 + 120 * np.exp(-t / .028) + 60 * np.exp(-t / .004)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / .22)
    click = butter(rng.standard_normal(len(t)), 2500, 'high') * np.exp(-t / .002) * .35
    return np.tanh((s + click) * 1.9 * punch) * .95


def clap(dur=.35):
    t = tt(dur)
    n = len(t)
    s = np.zeros(n)
    for d in (0, .009, .018, .026):
        k = int(d * SR)
        s[k:] += bp(rng.standard_normal(n - k), 900, 4200) * np.exp(-t[:n - k] / (.012 if d < .02 else .13))
    return s * .9


def hat(open_=False):
    t = tt(.2 if open_ else .06)
    return butter(rng.standard_normal(len(t)), 7800, 'high') * np.exp(-t / (.06 if open_ else .014))


def snare(dur=.22, tone=190):
    t = tt(dur)
    nz = bp(rng.standard_normal(len(t)), 1400, 9000) * np.exp(-t / .07)
    tn = np.sin(2 * np.pi * tone * t) * np.exp(-t / .05)
    return nz * .8 + tn * .5


KT = []                                    # vuruş zamanları (sidechain için)
KT += [b(n) for n in range(8, 19)]         # soru (b18.5'te çöküş -> davul susar)
KT += [b(n) for n in range(20, 56)]        # fatura, talep, karşılaştırma
KT += [b(56)]                              # sözleşme: tek vuruş, nefes
KT += [b(n) for n in range(60, 71)]        # fatura takibi
KT += [b(n) for n in range(72, 76)]        # değerler
KT += [b(n / 2) for n in range(152, 157)]  # yükseliş: sekizlikler (38.0-39.0)
for T in KT:
    add(KICK, T, kick(punch=1.15 if T in (b(8), b(60)) else 1.0))

CLAPS = list(range(21, 56, 2)) + list(range(61, 70, 2)) + [73, 75]
for n in CLAPS:
    add(SNARE, b(n), clap(), pan=.04, gain=.8)
for lo, hi in ((20, 56), (60, 71), (72, 78.5)):  # sekizlik arası (offbeat) hi-hat
    n2 = int(lo * 2)
    while n2 / 2 < hi:
        if n2 % 2 == 1:
            add(HATS, b(n2 / 2), hat(open_=(n2 % 4 == 3)), pan=.22, gain=.5)
        n2 += 1
for n4 in range(16 * 4, int(18.5 * 4)):          # tipografi duvarı: onaltılıklar
    add(HATS, b(n4 / 4), hat(), pan=-.2 + .4 * (n4 % 2), gain=.32 + .18 * (n4 % 4 == 2))
# yükseliş rulosu: sekizlik -> onaltılık -> otuzikilik, tizleşerek
roll = [b(76 + k / 2) for k in range(2)] + [b(77 + k / 4) for k in range(4)] + [b(78 + k / 8) for k in range(4)]
for i, T in enumerate(roll):
    add(SNARE, T, snare(tone=180 + i * 12), pan=(-.15 if i % 2 else .15), gain=.35 + .45 * i / len(roll))

# ================================================================== bass
def bass_note(f, dur, drive=1.4):
    t = tt(dur)
    s = np.sin(2 * np.pi * f * t) + .45 * np.sin(4 * np.pi * f * t) + .2 * saw(f * 2, len(t)) * .5
    e = (1 - np.exp(-t / .004)) * np.exp(-t / (dur * .55))
    return np.tanh(s * drive) * e


# soru: her kelimede uzun sub (stab ile birlikte)
for n in (8, 10, 12, 14, 16):
    add(BASS, b(n), bass_note(mtof(ROOT[chord_at(n)] - 12), BT * 1.9, 1.2), gain=1.0)
# gövde: house tarzı offbeat bas + kök vurgusu
for lo, hi in ((20, 56), (60, 71), (72, 78.5)):
    n2 = int(lo * 2)
    while n2 / 2 < hi:
        beat = n2 / 2
        r = ROOT[chord_at(beat)]
        if n2 % 2 == 1:
            add(BASS, b(beat), bass_note(mtof(r - 12), BT * .45), gain=.95)
        elif n2 % 8 == 0:
            add(BASS, b(beat), bass_note(mtof(r - 24), BT * .9, 1.0), gain=.7)
        n2 += 1
# sözleşme anı: tek uzun kök notası
add(BASS, b(56), bass_note(mtof(ROOT['A'] - 12), 2.0, 1.0), gain=.8)

# ================================================================== pad
def pad(notes, dur, att=.4, rel=1.2, cut0=500, cut1=2600):
    n = int((dur + rel) * SR)
    x = supersaw(notes, dur + rel, voices=5, cents=11)
    t = np.arange(n) / SR
    e = np.clip(t / att, 0, 1) * np.where(t > dur, np.exp(-(t - dur) / (rel / 3)), 1)
    fcs = cut0 + (cut1 - cut0) * np.clip(t / max(dur, 1e-3), 0, 1) ** 1.5
    return lp_sweep(x, fcs) * e


# giriş: Bm pad dalgalarla birlikte açılır
add(PAD, 0.8, pad(BM, 2.2, att=1.0, rel=.6, cut0=250, cut1=1800), gain=.9)
add(PAD, 3.0, pad(G_, 1.0, att=.05, rel=.3, cut0=1800, cut1=5000), gain=.5)
# gövde: her ölçüde akor (soru .. fatura takibi); sözleşme ölçüsü sıcak ve açık
for bar in range(2, 18):
    add(PAD, bar * 2.0, pad(VOX[PROG[bar]], 2.0, att=.25, rel=.5, cut0=900, cut1=2600 if bar == 14 else 1500), gain=.75 if bar == 14 else .5)
# değerler: filtre açılır
add(PAD, 36.0, pad([55, 59, 62, 67], 2.0, att=.2, rel=.2, cut0=700, cut1=3000), gain=.7)
add(PAD, 38.0, pad([57, 61, 64, 69, 73], 1.25, att=.1, rel=.15, cut0=1500, cut1=7000), gain=.75)
# final: büyük D akoru
add(PAD, 40.0, pad([38, 50, 57, 62, 66, 69, 74, 76], DUR - 40.0 - 1.4, att=.02, rel=1.4, cut0=5000, cut1=1400), gain=1.35)


# ================================================================== stabs
def stab(notes, dur=.34, cut=4200, bright=1.0):
    x = supersaw(notes, dur, voices=7, cents=22)
    t = np.arange(x.shape[1]) / SR
    e = (1 - np.exp(-t / .003)) * np.exp(-t / (dur * .38))
    fcs = 400 + cut * bright * np.exp(-t / .09)
    return lp_sweep(x, fcs) * e


for n in (8, 10, 12, 14, 16):                               # soru: her kelime
    add(STAB, b(n), stab([m + 12 for m in VOX[chord_at(n)]], .5, 5200), gain=1.0)
add(STAB, 33.0, stab([64, 65, 71, 76], .6, 4500), gain=.8)  # faturada fark: gerilimli akor
for i, T in enumerate((36.0, 36.75, 37.5, 38.25)):          # değer kelimeleri
    add(STAB, T, stab([m + 12 for m in VOX[chord_at(T / BT)]], .3 if i < 3 else .55, 3000 + i * 1200), gain=.75 if i < 3 else .95)


# ================================================================== arp (S3-S5, S8)
def pluck(f, dur=.32, bright=1.0):
    t = tt(dur)
    s = (np.sin(2 * np.pi * f * t) * np.exp(-t / .16)
         + .5 * np.sin(4 * np.pi * f * t) * np.exp(-t / .07) * bright
         + .22 * np.sin(6 * np.pi * f * t) * np.exp(-t / .035) * bright)
    return s * (1 - np.exp(-t / .002))


PAT = [0, 2, 1, 3, 2, 1, 3, 2, 0, 3, 1, 2, 3, 1, 2, 1]
for lo, hi, g in ((20, 56, 1.0), (60, 71, .7)):
    for n4 in range(lo * 4, hi * 4):
        beat = n4 / 4
        ns = sorted(VOX[chord_at(beat)])
        m = ns[PAT[n4 % 16]] + 12
        vel = (.9 if n4 % 2 == 0 else .55) * g
        add(ARP, b(beat), pluck(mtof(m), bright=.6 + .4 * ((n4 % 4) == 0)), pan=(.35 if n4 % 2 else -.35), gain=vel)
# final: yavaş arp
for k, m in enumerate([74, 78, 81, 86, 81, 78, 74, 78, 81, 86]):
    add(ARP, 40.5 + k * .375, pluck(mtof(m), .9), pan=(-.3 if k % 2 else .3), gain=.6 * (1 - k * .06))


# ================================================================== SFX kütüphanesi
def whoosh(dur=.6, f0=300, f1=4200, q=1.1, shape=1.5):
    t = tt(dur)
    u = t / dur
    fcs = f0 + (f1 - f0) * np.sin(np.pi * u) ** shape
    s = svf_bp(rng.standard_normal(len(t)), fcs, q)
    return butter(s * np.sin(np.pi * u) ** 2, 9000)


def whip(T, dur=.5, pan_from=-.8, pan_to=.8, gain=1.0):
    """Stereo'da süpürülen whoosh; T = en yoğun an."""
    w = whoosh(dur, 250, 5200, 1.3, 1.2)
    n = len(w)
    p = np.linspace(pan_from, pan_to, n)
    a = (p + 1) * np.pi / 4
    add(FX, T - dur / 2, np.vstack([w * np.cos(a), w * np.sin(a)]) * np.sqrt(2), gain=gain)


def riser(dur, f0=300, f1=9000, tone0=180, tone1=1400):
    t = tt(dur)
    u = t / dur
    fcs = f0 * (f1 / f0) ** (u ** 1.5)
    nz = svf_bp(rng.standard_normal(len(t)), fcs, 1.6)
    fr = tone0 * (tone1 / tone0) ** (u ** 1.3)
    tone = np.sin(2 * np.pi * np.cumsum(fr) / SR) + .3 * np.sin(4 * np.pi * np.cumsum(fr) / SR)
    return (nz + tone * .22) * u ** 2


def reverse_cym(dur=.8):
    t = tt(dur)
    s = butter(rng.standard_normal(len(t)), 3000, 'high') * np.exp(-(dur - t) / .25)
    return s * np.clip((dur - t) / .01, 0, 1)


def impact(size=1.0):
    t = tt(3.2)
    boom = np.sin(2 * np.pi * np.cumsum(36 + 70 * np.exp(-t / .09)) / SR) * np.exp(-t / (.7 * size))
    crash = butter(butter(rng.standard_normal(len(t)), 2200, 'high'), 12000) * np.exp(-t / (.9 * size)) * .4
    thump = butter(rng.standard_normal(len(t)), 300) * np.exp(-t / .03) * 2
    return np.tanh(boom * 1.7) * .95 + crash + thump * .5


def pop(f=900, dur=.09):
    t = tt(dur)
    fr = f * (1 + .7 * np.exp(-t / .008))
    return np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t / .02)


def tick(f=5200):
    t = tt(.03)
    return np.sin(2 * np.pi * f * t) * np.exp(-t / .003) + butter(rng.standard_normal(len(t)), 6000, 'high') * np.exp(-t / .002) * .5


def click(dur=.012):
    t = tt(dur)
    return butter(rng.standard_normal(len(t)), 2000, 'high') * np.exp(-t / .0025)


def bell(f, dur=1.6, bright=1.0):
    t = tt(dur)
    mod = np.sin(2 * np.pi * f * 3.5 * t) * 2.2 * np.exp(-t / .25) * bright
    s = np.sin(2 * np.pi * f * t + mod) * np.exp(-t / .6)
    s += .3 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t / .2)
    return s * (1 - np.exp(-t / .002))


def sonar(f=1150, dur=1.2):
    t = tt(dur)
    s = np.sin(2 * np.pi * f * t) * np.exp(-t / .22) * (1 - np.exp(-t / .004))
    return s


def glitch(dur=.42):
    t = tt(dur)
    n = len(t)
    s = rng.standard_normal(n)
    # örnek-tut (bitcrush) + kesik kesik kapı
    hold = np.repeat(s[::24], 24)[:n]
    gate = (np.floor(t * 34) % 3 != 1).astype(float) * (rng.random(int(np.ceil(t[-1] * 34)) + 1)[np.floor(t * 34).astype(int)] > .25)
    tone = np.sign(np.sin(2 * np.pi * (320 + 900 * (np.floor(t * 34) % 5)) * t))
    return butter(hold * .6 + tone * .25, 7000) * gate


def zap(dur=.5, f0=1800, f1=90):
    t = tt(dur)
    fr = f0 * (f1 / f0) ** (t / dur)
    return np.sin(2 * np.pi * np.cumsum(fr) / SR) * (1 - t / dur) ** 1.2


def crackle(dur=.35, dens=160):
    t = tt(dur)
    s = np.zeros(len(t))
    k = rng.integers(0, len(t), int(dens * dur))
    s[k] = rng.standard_normal(len(k))
    s = butter(s, 1800, 'high')
    return s * np.exp(-t / (dur * .5)) * 3


# ================================================================== S1 · AKIM (0-4)
add(FX, 0.03, crackle(.5), gain=.55)
add(FX, 0.03, np.sin(2 * np.pi * 52 * tt(1.2)) * np.exp(-tt(1.2) / .5) * (1 - np.exp(-tt(1.2) / .01)), gain=.6)
zing_t = tt(1.1)
zing = np.sin(2 * np.pi * np.cumsum(500 + 2600 * (1 - np.exp(-zing_t / .25))) / SR) * np.exp(-zing_t / .35) * .5
zing += whoosh(1.1, 800, 7000, 1.4, .8) * .8
add(FX, 0.18, np.vstack([zing, np.roll(zing, 180)]), gain=.55)
for k in range(22):                                   # harf karıştırma tıkırtıları
    add(UI, .35 + k * .03 + (k % 3) * .004, tick(4000 + (k * 373) % 2500), pan=(k % 5 - 2) * .2, gain=.12)
for k, pn in enumerate((-.4, 0, .4)):                 # L1 L2 L3
    add(UI, 1.32 + k * .05, pop(1300 + k * 180, .07), pan=pn, gain=.22)
hum_t = tt(1.5)                                       # 50 Hz uğultu (üç faz)
hum = sum(np.sin(2 * np.pi * 100 * hum_t + k * 2.094) * (.5 + .5 * np.sin(2 * np.pi * .85 * hum_t + k * 2.094)) for k in range(3))
add(FX, .9, butter(np.tanh(hum * 1.5), 900) * np.clip(hum_t / .5, 0, 1) * np.clip((1.5 - hum_t) / .4, 0, 1), gain=.18)
add(FX, 1.75, riser(1.25, 400, 6000, 200, 900), gain=.35)
add(FX, 3.0, impact(.55), gain=.7)                    # logo çubukları iner
for k, m in enumerate((74, 78, 81, 86)):
    add(CHIME, 3.0 + k * .012, bell(mtof(m), 2.0), pan=(k - 1.5) * .3, gain=.28)
add(CHIME, 3.08, bell(mtof(93), .8, .5), pan=.35, gain=.12)   # ışık süpürmesi
add(CHIME, 3.2, bell(mtof(98), .8, .5), pan=.5, gain=.08)
add(FX, 3.4, riser(.6, 600, 12000, 300, 2400), gain=.65)       # dalış -> drop
add(FX, 4.0 - .8, reverse_cym(.8), gain=.5)

# ================================================================== S2 · SORU (4-10)
add(FX, 4.0, impact(.9), gain=.85)
whip(5.0 + .1, .45, .9, -.9, .7)                       # TEDARİKÇİNİZİ (sağdan)
add(FX, 6.0, np.vstack([whoosh(.3, 2500, 9000, 2, 1), whoosh(.3, 2500, 9000, 2, 1)]), gain=.55)   # kesit
for i in range(8):                                     # split-flap
    add(UI, 7.0 + i * .03 + .05, click(.01), pan=(i - 3.5) * .15, gain=.35)
for i in range(17):                                    # duvar harfleri
    add(UI, 8.0 + i * .02 + .04, tick(3000 + i * 90), pan=(i - 8) * .05, gain=.13)
whip(8.8, .55, -.5, .5, .35)                           # kamera geri çekilir
add(FX, 9.25, zap(.75, 1400, 60), gain=.38)            # çöküş: güç kesilmesi
add(FX, 9.25, whoosh(.6, 3000, 300, 1.2, 1), gain=.35)
beam_t = tt(.6)
beam = (np.sin(2 * np.pi * 880 * beam_t) * .4 + np.sin(2 * np.pi * 1320.5 * beam_t) * .2) * np.clip(beam_t / .15, 0, 1) * np.clip((.6 - beam_t) / .08, 0, 1)
add(FX, 9.6, beam * (1 + .3 * np.sin(2 * np.pi * 9 * beam_t)), gain=.07)
add(FX, 9.5, riser(.5, 800, 8000, 400, 1600), gain=.3)

# ================================================================== S3 · FATURA (10-16)
add(FX, 10.0, np.vstack([whoosh(.6, 200, 3000, 1, 1.4), whoosh(.6, 200, 3000, 1, 1.4)]), gain=.4)
add(UI, 10.6, click(), gain=.3)
scan_t = tt(.75)
scan = svf_bp(rng.standard_normal(len(scan_t)), 1500 + 2500 * scan_t / .75, 5) * np.sin(np.pi * scan_t / .75) ** 2
add(FX, 11.0, np.vstack([scan, scan]) * np.array([[1], [.7]]), gain=.35)
for i, T in enumerate((11.2, 11.25, 11.32, 11.37)):
    add(UI, T + .02, pop(1500 + i * 220, .07), pan=(-.3 if i % 2 == 0 else .3), gain=.4)
whip(13.15, .8, .6, -.6, .5)                           # kart döner
for i in range(12):                                    # profil çubukları yükselir
    add(UI, 13.48 + i * .035, pop(700 * 2 ** ([0, 2, 4, 7, 9, 12, 14, 16, 19, 21, 24, 26][i] / 12), .06), pan=-.4 + i * .07, gain=.22)
add(CHIME, 13.8, bell(mtof(86), 1.2, .6), pan=.3, gain=.14)
whip(16.0, .7, .9, -.9, .9)                            # whip pan -> talep

# ================================================================== S4 · TALEP (16-22)
add(FX, 16.75, glitch(.44), pan=-.1, gain=.34)          # unvan bozulur
add(FX, 16.9, glitch(.2), pan=.3, gain=.22)
add(FX, 17.1, whoosh(.34, 3000, 800, 1.5, 1), pan=.2, gain=.3)
add(UI, 17.4, click(.02), gain=.5)                     # kilit
add(UI, 17.41, pop(420, .1), gain=.35)
for i in range(3):
    add(CHIME, 18.95 + i * .14, sonar(1150 - i * 60), pan=.1 + i * .15, gain=.28 * (1 - i * .25))
for i in range(5):
    add(UI, 19.3 + i * .07, pop(900 + i * 120), pan=.4 + i * .08, gain=.35)
    add(UI, 19.65 + i * .08, tick(5200 + i * 300), pan=.5, gain=.15)
for i in range(5):                                     # teklifler geri döner
    add(UI, 20.7 + i * .16, pop(1100 * 2 ** ([0, 4, 7, 11, 12][i] / 12), .09), pan=-.3, gain=.42)
    add(CHIME, 20.7 + i * .16, bell(mtof(81 + [0, 4, 7, 11, 12][i]), .5, .3), pan=-.3, gain=.07)
add(FX, 21.4, riser(.6, 500, 9000, 300, 1200), gain=.35)
add(FX, 21.4, whoosh(.6, 400, 6000, 1.2, 1.3), gain=.3)

# ================================================================== S5 · KARŞILAŞTIRMA (22-28)
for i in range(3):
    add(FX, 22.15 + i * .15, whoosh(.9, 1500, 5000, 3, 1) * .6, pan=-.4 + i * .4, gain=.18)
sc_t = tt(.95)
sc = svf_bp(rng.standard_normal(len(sc_t)), 900 + 3000 * sc_t / .95, 4) * np.sin(np.pi * sc_t / .95)
pp = np.linspace(-.8, .8, len(sc))
a_ = (pp + 1) * np.pi / 4
add(FX, 24.05, np.vstack([sc * np.cos(a_), sc * np.sin(a_)]) * 1.4, gain=.35)   # tarayıcı soldan sağa
for k in range(14):
    add(UI, 24.85 + k * .045, tick(4500), pan=.6, gain=.09)
whip(26.1, .55, -.3, .3, .3)                           # sıralama
add(CHIME, 26.3, bell(mtof(86), 1.2), pan=.5, gain=.18)
add(CHIME, 26.4, bell(mtof(93), 1.2), pan=.5, gain=.14)
add(FX, 27.2, whoosh(.8, 300, 2500, 1.1, 1.2), pan=.3, gain=.3)   # satır sözleşmeye dönüşür

# ================================================================== S6 · SÖZLEŞME (28-30)
for i in range(6):
    add(UI, 27.95 + i * .06, tick(3800 + i * 200), pan=.4, gain=.1)
pen_t = tt(.62)                                        # imza: kağıt üzerinde kalem
pen = bp(rng.standard_normal(len(pen_t)), 2500, 7000) * (.35 + .65 * np.abs(np.sin(2 * np.pi * 7.5 * pen_t))) * np.clip(pen_t / .03, 0, 1) * np.clip((.62 - pen_t) / .05, 0, 1)
add(FX, 28.45, pen, pan=.35, gain=.32)
add(FX, 29.15, impact(.25), gain=.45)                  # damga
add(UI, 29.15, click(.02), gain=.6)
add(UI, 29.16, pop(300, .12), gain=.5)
add(CHIME, 29.2, bell(mtof(88), 1.2, .6), pan=.35, gain=.14)
for i in range(3):                                     # logo şeritleri
    whip(29.8 + i * .07, .45, .9, -.9, .4)
add(FX, 30.0 - .6, reverse_cym(.6), gain=.3)

# ================================================================== S6 · FATURA TAKİBİ (30-36)
T6 = [30.5, 31.0, 31.5, 32.0, 32.5, 33.0]
add(FX, 30.0, impact(.4), gain=.4)
for s_ in range(1, 6):                                 # yürüyen bant adımları
    add(FX, T6[s_] - .3, whoosh(.3, 600, 2500, 1.4, 1), pan=.4, gain=.16)
for i, T in enumerate(T6):
    add(UI, T, click(.015), pan=0, gain=.4)            # kapıya varış
    if i < 5:                                          # sözleşmeye uygun
        add(CHIME, T + .08, bell(mtof(81 + [0, 2, 4, 5, 7][i]), .7, .35), pan=-.2, gain=.12)
        add(UI, T + .08, pop(1400 + i * 80, .07), pan=-.2, gain=.22)
al_t = tt(.9)                                          # fark: alarm tonu (iki kez)
alarm = sum(np.sin(2 * np.pi * f * al_t) * ((al_t >= s0) & (al_t < s0 + .14)) for f, s0 in ((880, 0), (660, .16), (880, .42), (660, .58)))
add(FX, 33.02, butter(alarm * np.exp(-al_t / .6), 5000), gain=.16)
add(FX, 33.0, impact(.35), gain=.45)
add(CHIME, 33.45, bell(mtof(88), 1.4), pan=.5, gain=.2)       # bildirim
add(CHIME, 33.57, bell(mtof(95), 1.4), pan=.5, gain=.16)
add(FX, 34.0, whoosh(.5, 800, 3000, 1.2, 1), pan=-.4, gain=.18)
add(FX, 35.2, whoosh(.6, 3000, 250, 1.1, 1), gain=.35)        # kartlar düşer, çizgi ufka çıkar

# ================================================================== S7 · DEĞERLER (36-40)
add(FX, 35.6, riser(39.25 - 35.6, 250, 11000, 110, 1800), gain=.55)
for T in (36.0, 36.75, 37.5, 38.25):
    add(UI, T, tick(3500), gain=.25)
add(FX, 39.0, reverse_cym(.85), gain=.35)

# ================================================================== S8 · MARKA (40-45)
add(FX, 40.0, impact(1.3), gain=1.25)
air = butter(rng.standard_normal((2, int(3.2 * SR))), 3000, 'high') * np.exp(-tt(3.2) / 1.2) * .25
add(FX, 40.0, air, gain=.5)
for k, m in enumerate((62, 69, 74, 78, 81, 86)):
    add(CHIME, 40.02 + k * .018, bell(mtof(m), 2.8, .8), pan=(k - 2.5) * .25, gain=.2)
for i in range(3):
    add(UI, 40.05 + i * .045, pop(500 + i * 200, .1), pan=(i - 1) * .4, gain=.3)
add(FX, 40.72, whoosh(.7, 400, 3000, 1.2, 1.2), pan=.3, gain=.25)     # kelime markası
for i in range(3):                                                    # hizmet etiketleri
    add(UI, 41.6 + i * .12, pop(900 + i * 150, .08), pan=(i - 1) * .4, gain=.3)
add(UI, 42.05, pop(1000, .08), gain=.35)                               # URL
add(CHIME, 42.6, bell(mtof(98), 1.5, .4), pan=.4, gain=.12)            # parıltı
add(CHIME, 42.72, bell(mtof(105), 1.5, .3), pan=.5, gain=.08)

# ================================================================== sidechain
duck = np.ones(N)
for T in KT:
    i = int(T * SR)
    n = min(int(.42 * SR), N - i)
    t = np.arange(n) / SR
    duck[i:i + n] = np.minimum(duck[i:i + n], 1 - .55 * np.exp(-t / .1))
PAD *= duck
BASS *= duck
STAB *= (1 - (1 - duck) * .35)
ARP *= (1 - (1 - duck) * .5)

# ================================================================== efektler (reverb, delay)
def make_ir(sec=2.8, decay=.6, pre=.018):
    n = int(sec * SR)
    t = np.arange(n) / SR
    ir = rng.standard_normal((2, n)) * np.exp(-t / decay)
    ir = butter(ir, 7000)
    ir[:, :int(pre * SR)] = 0
    return ir / np.sqrt((ir ** 2).sum(axis=1, keepdims=True))


def delay(x, sec, fb=.35, mix=.3, taps=5):
    d = int(sec * SR)
    out = np.zeros_like(x)
    tap = x.copy()
    g = mix
    for k in range(taps):
        tap = np.pad(tap, ((0, 0), (d, 0)))[:, :x.shape[1]]
        tap = butter(tap, 4500, order=1)
        out += (tap[::-1] if k % 2 == 0 else tap) * g
        g *= fb
    return x + out


ARP = delay(ARP, BT * .75, .38, .32)
CHIME = delay(CHIME, BT * .5, .3, .22)
IR = make_ir()
send = PAD * .3 + STAB * .35 + ARP * .4 + CHIME * .6 + UI * .25 + FX * .3 + SNARE * .18
wet = np.vstack([signal.fftconvolve(send[c], IR[c])[:N] for c in range(2)])

# drop öncesi ve implozyon sessizlikleri (kısa boşluk = daha sert vuruş)
def gap(bu, t0, t1, fade=.01):
    i0, i1, f = int(t0 * SR), int(t1 * SR), int(fade * SR)
    g = np.ones(N)
    g[i0:i1] = 0
    g[i0 - f:i0] = np.linspace(1, 0, f)
    return bu * g


mix = (KICK * .85 + SNARE * .45 + HATS * .3 + BASS * .55 + PAD * .36 + STAB * 1.5 + ARP * .15
       + FX * .5 + UI * .7 + CHIME * .5 + wet * .32)
import os
if os.environ.get('MUSIC_DEBUG'):
    ref = np.sqrt(np.mean(mix ** 2))
    for nm, x, gn in (('KICK', KICK, .85), ('SNARE', SNARE, .45), ('HATS', HATS, .3), ('BASS', BASS, .55), ('PAD', PAD, .36), ('STAB', STAB, 1.5),
                      ('ARP', ARP, .15), ('FX', FX, .5), ('UI', UI, .7), ('CHIME', CHIME, .5), ('WET', wet, .32)):
        print(f'{nm:6s} {20 * np.log10(np.sqrt(np.mean((x * gn) ** 2)) / ref + 1e-12):6.1f} dB (rel), peak {20 * np.log10(np.abs(x * gn).max() / ref + 1e-12):5.1f}')
mix = gap(mix, 4.0 - .045, 4.0)
mix = gap(mix, 39.85, 40.0)

# master: yüksek geçiren, hafif glue kompresyon, loudness, limiter
mix = butter(mix, 25, 'high')
t = np.arange(N) / SR
fade = np.clip(t / .02, 0, 1) * np.clip((DUR - t) / 1.6, 0, 1)
mix *= fade

mix /= np.sqrt(np.mean(mix ** 2)) / 10 ** (-20 / 20)          # referans: -20 dBFS RMS
env = np.sqrt(butter(np.mean(mix ** 2, axis=0), 6, order=1).clip(1e-12))
thr = 10 ** (-17 / 20)
gain = np.where(env > thr, (env / thr) ** (1 / 2.0 - 1), 1.0)   # 2:1 glue
mix *= gain

# loudness (-14 LUFS) + ileri bakışlı tepe sınırlayıcı (-1 dBFS), birkaç tur
from scipy.ndimage import minimum_filter1d
ceil = 10 ** (-1.2 / 20)


def limit(x):
    pk = np.max(np.abs(x), axis=0)
    g = np.minimum(1.0, ceil / np.maximum(pk, 1e-9))
    g = minimum_filter1d(g, size=int(.04 * SR))
    win = np.hanning(int(.02 * SR))
    return x * np.convolve(g, win / win.sum(), mode='same')


try:
    import pyloudnorm as pyln
    meter = pyln.Meter(SR)
    for it in range(4):
        lufs = meter.integrated_loudness(mix.T)
        mix *= 10 ** ((-14.0 - lufs) / 20)
        mix = limit(mix)
    print(f'loudness {meter.integrated_loudness(mix.T):.2f} LUFS')
except ImportError:
    mix /= np.abs(mix).max() / ceil
mix = np.clip(mix, -ceil, ceil)
print('peak dBFS', round(20 * np.log10(np.abs(mix).max()), 2))
wavfile.write('music.wav', SR, (np.clip(mix, -1, 1).T * 32767).astype(np.int16))
print('music.wav yazıldı')
