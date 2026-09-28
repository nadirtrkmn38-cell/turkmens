"""Enerji Tedariği reklam filmi için müzik + ses efekti sentezi.

Tamamen kod ile üretilir (telif sorunu yoktur). 120 BPM, Si minör -> Re majör,
sahne geçişleri (4, 9, 14, 20, 24.5, 28. sn) vuruşlara oturur.

Kullanım:  python3 music.py   ->  music.wav (48 kHz, stereo, 16-bit)
Gerekenler: numpy, scipy, (opsiyonel) pyloudnorm
"""
import numpy as np
from scipy import signal
from scipy.io import wavfile

SR = 48000
DUR = 33.0
N = int(SR * DUR)
rng = np.random.default_rng(7)
BEAT = 0.5  # 120 BPM


def mtof(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def bus():
    return np.zeros((2, N))


def add(b, start, sig, pan=0.0, gain=1.0):
    i = int(round(start * SR))
    if i >= N:
        return
    if sig.ndim == 1:
        a = (pan + 1) * np.pi / 4
        sig = np.vstack([sig * np.cos(a), sig * np.sin(a)])
    n = min(sig.shape[1], N - i)
    b[:, i:i + n] += gain * sig[:, :n]


def lp(x, fc, order=2):
    bb, aa = signal.butter(order, fc / (SR / 2))
    return signal.lfilter(bb, aa, x, axis=-1)


def hp(x, fc, order=2):
    bb, aa = signal.butter(order, fc / (SR / 2), 'high')
    return signal.lfilter(bb, aa, x, axis=-1)


def bp(x, lo, hi, order=2):
    bb, aa = signal.butter(order, [lo / (SR / 2), hi / (SR / 2)], 'band')
    return signal.lfilter(bb, aa, x, axis=-1)


def svf_sweep(x, fcs, q=1.2):
    """Zamanla değişen band-pass (state variable filter)."""
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


# ------------------------------------------------------------------ buses
PAD, BASS, KICK, PERC, PLUCK, CHIME, SFX, FX = (bus() for _ in range(8))

# ------------------------------------------------------------------ harmony
CHORDS = [  # (başlangıç, süre, pad notaları, bas kökü)
    (0.0, 4.0, [59, 62, 66, 69], 47),    # Bm7
    (4.0, 4.0, [55, 59, 62, 66], 43),    # Gmaj7
    (8.0, 4.0, [57, 62, 66, 76], 50),    # Dadd9
    (12.0, 4.0, [57, 61, 64, 71], 45),   # Aadd9
    (16.0, 4.0, [59, 62, 66, 69], 47),   # Bm7
    (20.0, 4.0, [55, 59, 62, 66], 43),   # Gmaj7
    (24.0, 4.0, [57, 61, 64, 69, 71], 45),  # A (yükseliş)
    (28.0, 5.0, [50, 57, 62, 66, 69, 76], 38),  # D (final)
]


def saw(f, n):
    ph = (rng.random() + f * np.arange(n) / SR) % 1.0
    return 2 * ph - 1


# pad
for ci, (st, du, notes, _) in enumerate(CHORDS):
    rel = 1.6 if ci < 7 else 2.5
    n = int((du + rel) * SR)
    tt = np.arange(n) / SR
    att = 1.2 if ci == 0 else 0.35
    env = np.clip(tt / att, 0, 1) * np.where(tt > du, np.exp(-(tt - du) / (rel / 4)), 1.0)
    L = np.zeros(n)
    R = np.zeros(n)
    for m in notes:
        f = mtof(m)
        for cents, (gl, gr) in zip((-9, 0, 9), ((1.0, .45), (.75, .75), (.45, 1.0))):
            s = saw(f * 2 ** (cents / 1200), n)
            L += s * gl
            R += s * gr
    cutoff = 900 + ci * 170
    sig = lp(np.vstack([L, R]), cutoff) * env / len(notes)
    add(PAD, st, sig, gain=1.35 if ci == 7 else 1.0)

# bas: 4-9 uzun sub, 9-27.5 sekizlik pompalayan bas
for st, du, _, root in CHORDS:
    f = mtof(root)
    if st < 8:
        if st >= 4:
            n = int((du + .6) * SR)
            tt = np.arange(n) / SR
            env = np.clip(tt / .6, 0, 1) * np.where(tt > du, np.exp(-(tt - du) / .15), 1)
            s = np.sin(2 * np.pi * f * tt) + .25 * np.sin(4 * np.pi * f * tt)
            add(BASS, st, s * env * .8)
    if st >= 8 and st < 28:
        steps = int(du / .25)
        for k in range(steps):
            t0 = st + k * .25
            if t0 < 9.0 or t0 >= 27.5:
                continue
            n = int(.25 * SR)
            tt = np.arange(n) / SR
            acc = 1.0 if k % 2 else .55  # ara vuruş vurgusu
            env = (1 - np.exp(-tt / .004)) * np.exp(-tt / .11)
            s = np.sin(2 * np.pi * f * tt) + .35 * np.sin(4 * np.pi * f * tt) + .12 * np.sin(6 * np.pi * f * tt)
            add(BASS, t0, s * env * acc)
# final kök
n = int(4.8 * SR)
tt = np.arange(n) / SR
add(BASS, 28.0, (np.sin(2 * np.pi * mtof(38) * tt) + .3 * np.sin(4 * np.pi * mtof(38) * tt)) * np.exp(-tt / 1.6) * .9)


# ------------------------------------------------------------------ drums
def kick():
    n = int(.45 * SR)
    tt = np.arange(n) / SR
    fr = 45 + 95 * np.exp(-tt / .035)
    ph = 2 * np.pi * np.cumsum(fr) / SR
    s = np.sin(ph) * np.exp(-tt / .16)
    s[:int(.002 * SR)] += rng.standard_normal(int(.002 * SR)) * .3
    return np.tanh(s * 1.6)


def hat(open_=False):
    n = int((.18 if open_ else .06) * SR)
    tt = np.arange(n) / SR
    s = hp(rng.standard_normal(n), 7500) * np.exp(-tt / (.05 if open_ else .015))
    return s


def clap():
    n = int(.3 * SR)
    tt = np.arange(n) / SR
    s = bp(rng.standard_normal(n), 900, 3200) * (np.exp(-tt / .09))
    for d in (.008, .016):  # çoklu el çırpma
        k = int(d * SR)
        s[k:] += bp(rng.standard_normal(n - k), 900, 3200) * np.exp(-tt[:n - k] / .02) * .6
    return s


K = kick()
t0 = 4.0
while t0 < 27.4:
    step = 1.0 if t0 < 14 else .5
    add(KICK, t0, K, gain=1.0)
    t0 += step
t0 = 9.25
while t0 < 27.5:
    add(PERC, t0, hat(), pan=.25, gain=.55)
    t0 += .5
t0 = 20.125
while t0 < 27.5:
    add(PERC, t0, hat(), pan=-.3, gain=.18)
    t0 += .25
t0 = 14.5
while t0 < 27.5:
    add(PERC, t0, clap(), pan=-.05, gain=.55)
    t0 += 1.0


# ------------------------------------------------------------------ pluck arp
def pluck(f, dur=.5):
    n = int(dur * SR)
    tt = np.arange(n) / SR
    env = 1 - np.exp(-tt / .003)
    s = (np.sin(2 * np.pi * f * tt) * np.exp(-tt / .22)
         + .45 * np.sin(4 * np.pi * f * tt) * np.exp(-tt / .1)
         + .18 * np.sin(6 * np.pi * f * tt) * np.exp(-tt / .05))
    return s * env


PAT = [0, 2, 1, 3, 2, 1, 3, 2]
for st, du, notes, _ in CHORDS:
    if st < 4 or st >= 28:
        continue
    ns = sorted(notes)[:4]
    for k in range(int(du / .25)):
        tk = st + k * .25
        m = ns[PAT[k % 8] % len(ns)] + 12
        vel = .9 if k % 2 == 0 else .6
        add(PLUCK, tk, pluck(mtof(m)), pan=(.3 if k % 2 else -.3), gain=vel)
# final: yavaş arp
for k, m in enumerate([74, 78, 81, 86, 81, 78]):
    add(PLUCK, 28.0 + k * .5, pluck(mtof(m), .9), pan=(-.25 if k % 2 else .25), gain=.75 * (1 - k * .1))


# ------------------------------------------------------------------ chimes (açılış kelimeleri)
def bell(f, dur=2.0):
    n = int(dur * SR)
    tt = np.arange(n) / SR
    s = (np.sin(2 * np.pi * f * tt) * np.exp(-tt / .7)
         + .35 * np.sin(2 * np.pi * f * 2.76 * tt) * np.exp(-tt / .18)
         + .15 * np.sin(2 * np.pi * f * 5.4 * tt) * np.exp(-tt / .07))
    return s * (1 - np.exp(-tt / .002))


for tk, m in ((.3, 74), (.68, 78), (1.06, 83)):
    add(CHIME, tk, bell(mtof(m)), pan=(m - 78) / 12, gain=.8)
# bildirim sesi (S5)
add(CHIME, 22.3, bell(mtof(88), 1.2), pan=.3, gain=.55)
add(CHIME, 22.42, bell(mtof(95), 1.2), pan=.3, gain=.45)
# onay (S2)
add(CHIME, 7.88, bell(mtof(86), 1.0), pan=.35, gain=.35)
add(CHIME, 7.98, bell(mtof(90), 1.0), pan=.35, gain=.3)


# ------------------------------------------------------------------ UI SFX
def pop(f=900, dur=.08):
    n = int(dur * SR)
    tt = np.arange(n) / SR
    fr = f * (1 + .6 * np.exp(-tt / .01))
    s = np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-tt / .018)
    return s


def swipe(dur=.35, lo=600, hi=5000):
    n = int(dur * SR)
    tt = np.arange(n) / SR
    fcs = lo * (hi / lo) ** (tt / dur)
    s = svf_sweep(rng.standard_normal(n), fcs, q=2.0)
    env = np.sin(np.pi * tt / dur) ** 2
    return s * env


for tk, f, pn in ((4.95, 520, .3), (6.2, 700, .3), (11.3, 880, .5), (11.42, 990, .5), (11.54, 1100, .5),
                  (11.66, 1240, .5), (18.1, 1000, .4), (25.1, 700, -.4), (25.24, 800, 0), (25.38, 900, .4),
                  (28.2, 600, 0), (28.3, 750, 0), (28.4, 900, 0), (29.4, 800, 0)):
    add(SFX, tk, pop(f), pan=pn, gain=.9)
add(SFX, 10.15, swipe(.55, 400, 3500), pan=.3, gain=.35)
add(SFX, 16.1, swipe(.85, 500, 6000), pan=.2, gain=.3)


# ------------------------------------------------------------------ transitions / riser / impact
def whoosh(dur=.8):
    n = int(dur * SR)
    tt = np.arange(n) / SR
    u = tt / dur
    fcs = 300 + 3200 * np.sin(np.pi * u) ** 1.5
    s = svf_sweep(rng.standard_normal(n), fcs, q=1.1)
    env = np.sin(np.pi * u) ** 2
    return lp(s * env, 6500)


for T in (4.0, 9.0, 14.0, 20.0, 24.5):
    w = whoosh(.8)
    add(FX, T - .45, w, pan=-.2, gain=.4)
    add(FX, T - .43, whoosh(.8), pan=.2, gain=.4)

# riser 25.8 -> 28
dur = 2.2
n = int(dur * SR)
tt = np.arange(n) / SR
u = tt / dur
fcs = 300 * (9000 / 300) ** (u ** 1.4)
nz = svf_sweep(rng.standard_normal(n), fcs, q=1.6)
tone = np.sin(2 * np.pi * np.cumsum(220 * 2 ** (2 * u ** 1.3)) / SR) * .25
riser = (nz + tone) * (u ** 2.2) * (1 - np.exp(-(1 - u + 1e-4) / .01))
add(FX, 25.8, riser, gain=.7)

# impact 28.0
n = int(3.0 * SR)
tt = np.arange(n) / SR
boom = np.sin(2 * np.pi * np.cumsum(38 + 40 * np.exp(-tt / .12)) / SR) * np.exp(-tt / .9)
crash = lp(hp(rng.standard_normal(n), 2500), 11000) * np.exp(-tt / .7) * .35
add(FX, 28.0, np.tanh(boom * 1.5) * .9 + crash, gain=1.25)
add(FX, 28.0, crash, pan=.6, gain=.25)
add(FX, 28.0, crash, pan=-.6, gain=.25)

# ------------------------------------------------------------------ sidechain ducking (kick)
duck = np.ones(N)
t0 = 4.0
while t0 < 27.4:
    step = 1.0 if t0 < 14 else .5
    i = int(t0 * SR)
    n = min(int(.4 * SR), N - i)
    tt = np.arange(n) / SR
    duck[i:i + n] = np.minimum(duck[i:i + n], 1 - .45 * np.exp(-tt / .12))
    t0 += step
PAD *= duck
BASS *= duck
PLUCK *= (1 - (1 - duck) * .5)


# ------------------------------------------------------------------ reverb
def make_ir(sec=2.6, decay=.55):
    n = int(sec * SR)
    tt = np.arange(n) / SR
    ir = rng.standard_normal((2, n)) * np.exp(-tt / decay)
    ir = lp(ir, 6000)
    ir[:, :int(.02 * SR)] = 0  # pre-delay
    return ir / np.sqrt((ir ** 2).sum(axis=1, keepdims=True))


IR = make_ir()
send = PAD * .35 + PLUCK * .45 + CHIME * .7 + SFX * .25 + FX * .35 + PERC * .12
wet = np.vstack([signal.fftconvolve(send[c], IR[c])[:N] for c in range(2)])


# pluck stereo delay (noktalı sekizlik)
def delay(x, sec, fb=.35, mix=.35):
    d = int(sec * SR)
    y = x.copy()
    out = np.zeros_like(x)
    tap = x.copy()
    g = mix
    for _ in range(4):
        tap = np.pad(tap, ((0, 0), (d, 0)))[:, :N]
        tap = lp(tap, 4000, 1)
        out += tap * g
        g *= fb
    out[[0, 1]] = out[[1, 0]]  # ping-pong hissi
    return y + out


PLUCK = delay(PLUCK, .375)

mix = (PAD * .30 + BASS * .42 + KICK * .78 + PERC * .20 + PLUCK * .16
       + CHIME * .22 + SFX * .16 + FX * .26 + wet * .30)

# master
mix = hp(mix, 28)
tt = np.arange(N) / SR
fade = np.clip(tt / .25, 0, 1) * np.clip((DUR - tt) / 1.6, 0, 1)
mix *= fade

try:
    import pyloudnorm as pyln
    meter = pyln.Meter(SR)
    lufs = meter.integrated_loudness(mix.T)
    target = -15.0
    mix *= 10 ** ((target - lufs) / 20)
    print(f'loudness {lufs:.1f} LUFS -> {target} LUFS')
except ImportError:
    mix /= np.abs(mix).max() / .7

# yumuşak limiter
ceil = 10 ** (-1.0 / 20)
mix = np.tanh(mix / ceil) * ceil
print('peak dBFS', 20 * np.log10(np.abs(mix).max()))
wavfile.write('music.wav', SR, (mix.T * 32767).astype(np.int16))
print('music.wav yazıldı')
