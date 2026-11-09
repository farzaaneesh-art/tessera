"""Original ambient bed: tanpura-style drone + warm pad + sparse soft plucks (Bhupali notes).
Fully synthesised, so no licensing issues."""
import sys, wave
import numpy as np

OUT = sys.argv[1]
DUR = float(sys.argv[2])
SR = 48000
N = int(SR * DUR)
t = np.arange(N) / SR
rng = np.random.default_rng(7)
SA = 146.83  # D3

def env(n, a, d):
    x = np.arange(n) / SR
    return np.minimum(1, x / a) * np.exp(-x / d)

def tanpura_pluck(f, dur=4.5, amp=1.0):
    n = int(SR * dur); x = np.arange(n) / SR
    s = np.zeros(n)
    for h in range(1, 18):
        # jawari: upper partials bloom then fade, slight detune shimmer
        bloom = np.minimum(1, x / (0.15 + 0.05 * h)) * np.exp(-x / (2.8 / (1 + 0.12 * h)))
        s += (1 / h ** 0.9) * bloom * np.sin(2 * np.pi * f * h * (1 + 0.0004 * h) * x + rng.uniform(0, 6.28))
    return amp * s * env(n, 0.01, 3.0) / 3

def pluck(f, dur=3.0, amp=1.0):
    # soft santoor/harp-like: few partials, quick attack, long decay
    n = int(SR * dur); x = np.arange(n) / SR
    s = sum((0.6 ** (h - 1)) * np.sin(2 * np.pi * f * h * x) * np.exp(-x * (1.2 + 0.9 * h)) for h in range(1, 6))
    return amp * s * np.minimum(1, x / 0.004)

mix = np.zeros(N + SR * 6)
def add(sig, start):
    i = int(start * SR); mix[i:i + len(sig)] += sig

# tanpura cycle: Pa(low) Sa Sa Sa(low), ~1.1s per pluck
cycle = [SA * 0.75, SA, SA, SA * 0.5]
k = 0; tt = 0.0
while tt < DUR:
    add(tanpura_pluck(cycle[k % 4], amp=0.55 if k % 4 else 0.65), tt)
    tt += 1.15; k += 1

# warm pad: Sa + Pa + Sa', slow swell
pad = np.zeros(N)
for f, a in [(SA, 0.5), (SA * 1.5, 0.3), (SA * 2, 0.25)]:
    for det in (-0.6, 0.6):
        pad += a * np.sin(2 * np.pi * (f + det) * t)
pad *= 0.10 * (0.6 + 0.4 * np.sin(2 * np.pi * t / 12 - 1.5))
mix[:N] += pad

# santoor-like plucks in Raag Kafi (S R g m P D n): rolling figures with tremolo pairs
r = {"S":1,"R":9/8,"g":6/5,"m":4/3,"P":3/2,"D":5/3,"n":9/5,"S'":2,"R'":9/4}
phr = ["S","R","g","R","S","n.","S","R", "g","m","P","m","g","R","g","S",
       "P","D","n","S'","n","D","P","m", "g","m","P","g","R","S","R","S"]
r["n."] = 9/10
t0, step = 1.5, 0.42
for k, n in enumerate(phr * 3):
    st = t0 + k * step + (0.08 if k % 4 == 3 else 0)
    if st > DUR - 3.0: break
    amp = 0.16 if k % 8 == 0 else 0.10
    add(pluck(SA * 2 * r[n], amp=amp), st)
    if k % 8 == 0:
        add(pluck(SA * 2 * r[n] * 2, amp=0.05), st + 0.03)
add(pluck(SA * 2, dur=3.0, amp=0.18), DUR - 2.8)   # final resolving Sa
mix = mix[:N]
# simple reverb: convolve with decaying noise IR
ir_n = int(SR * 2.2)
ir = rng.standard_normal(ir_n) * np.exp(-np.arange(ir_n) / SR / 0.55)
ir /= np.sqrt((ir ** 2).sum())
from numpy.fft import rfft, irfft
L = 1 << int(np.ceil(np.log2(N + ir_n)))
wet = irfft(rfft(mix, L) * rfft(ir, L), L)[:N]
out = 0.75 * mix + 0.45 * wet
# low-pass-ish smoothing (one-pole) for warmth
a = 0.35
y = np.empty_like(out); acc = 0.0
for i in range(0, N, 1):
    pass
from scipy.signal import lfilter  # noqa
y = lfilter([1 - a], [1, -a], out)
# fades
fi, fo = int(SR * 1.2), int(SR * 2.5)
y[:fi] *= np.linspace(0, 1, fi); y[-fo:] *= np.linspace(1, 0, fo) ** 1.5
y /= np.abs(y).max() / 0.8
st = np.stack([y, np.roll(y, int(SR * 0.012))], 1)  # slight stereo width
pcm = (st * 32767).astype(np.int16)
with wave.open(OUT, "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print("ok")
