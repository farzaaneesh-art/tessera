"""Builds the (v2, 31 s) voiceover track and a soft ambient music bed for the Tessera reel.

- assets/audio/voiceover.wav : the narration sentences placed on the film's clock
- assets/audio/music_bed.wav : a quiet procedural piano/pad bed, ducked under the voice

Everything is deterministic (seeded), so re-running gives identical files.
Run from the project root:  python3 scripts/build_audio.py
"""
import json
import numpy as np
import soundfile as sf

SR = 48000
LEN = 31.6
N = int(SR * LEN)

# ---------------------------------------------------------------- voiceover
# (file, start second on the film clock)
VO = [
    ("n01", 0.40),            # Flowers fade.
    ("n02", 3.30),            # But their beauty doesn't have to.
    ("n03", 5.30),            # In every leaf, every petal...
    ("n04", 8.90),            # Through botanical printing...
    ("n05", 20.50),           # Each impression is different.
    ("n06", 23.20),           # Each piece tells its own story.
    ("n07", 26.60),           # Tessera.
    ("n08", 28.10),           # Naturally Yours.
]

def load_resampled(path):
    x, sr = sf.read(path, dtype="float64")
    if x.ndim > 1:
        x = x.mean(axis=1)
    if sr != SR:
        t_old = np.arange(len(x)) / sr
        t_new = np.arange(int(len(x) * SR / sr)) / SR
        x = np.interp(t_new, t_old, x)
    return x

vo = np.zeros(N)
timing = []
for name, start in VO:
    x = load_resampled(f"assets/vo2/parts/{name}.wav")
    i = int(start * SR)
    vo[i:i + len(x)] += x[: N - i]
    timing.append({"id": name, "start": start, "end": round(start + len(x) / SR, 3)})
json.dump(timing, open("assets/vo2/timing.json", "w"), indent=2)
sf.write("assets/audio/voiceover_raw.wav", vo, SR, subtype="PCM_24")

# ---------------------------------------------------------------- music bed
rng = np.random.default_rng(7)
t = np.arange(N) / SR

def midi(m):
    return 440.0 * 2 ** ((m - 69) / 12)

BPM = 64
BEAT = 60 / BPM
BAR = 4 * BEAT
# D major colour: Dmaj9, Bm7(11), Gmaj7(9), Asus4 -> A   (2 bars each)
CHORDS = [
    [50, 57, 62, 66, 69, 76],   # D  A  D  F# A  E
    [47, 54, 62, 66, 69, 76],   # B  F# D  F# A  E
    [43, 50, 59, 62, 66, 69],   # G  D  B  D  F# A
    [45, 52, 61, 62, 64, 69],   # A  E  C# D  E  A
]
CHORD_LEN = 2 * BAR

def env_adsr(n, a, r):
    e = np.ones(n)
    na, nr = min(int(a * SR), n // 2), min(int(r * SR), n // 2)
    e[:na] = np.linspace(0, 1, na) ** 2
    if nr:
        e[-nr:] *= np.linspace(1, 0, nr) ** 2
    return e

pad = np.zeros(N)
k = 0
start = 0.0
while start < LEN:
    ch = CHORDS[k % 4]
    dur = CHORD_LEN + 1.6           # overlap for a soft crossfade
    i0 = int(start * SR)
    n = min(int(dur * SR), N - i0)
    tt = np.arange(n) / SR
    e = env_adsr(n, 1.4, 1.6)
    for m in ch[1:]:
        f = midi(m)
        v = (np.sin(2 * np.pi * f * tt) + 0.25 * np.sin(2 * np.pi * 2 * f * tt + 0.3)
             + 0.6 * np.sin(2 * np.pi * f * 1.003 * tt + 1.1))
        pad[i0:i0 + n] += v * e * 0.05
    start += CHORD_LEN
    k += 1

def piano_note(f, n, vel):
    tt = np.arange(n) / SR
    decay = np.exp(-tt * 1.6)
    body = (np.sin(2 * np.pi * f * tt) + 0.35 * np.sin(2 * np.pi * 2 * f * tt) * np.exp(-tt * 3)
            + 0.12 * np.sin(2 * np.pi * 3 * f * tt) * np.exp(-tt * 5))
    attack = np.minimum(1, tt / 0.006)
    return body * decay * attack * vel

keys = np.zeros(N)
bass = np.zeros(N)
beat_i = 0
while True:
    bt = beat_i * BEAT
    if bt >= 30.0:
        break
    ch = CHORDS[int(bt // CHORD_LEN) % 4]
    upper = [m + 12 for m in ch[2:]]
    # sparse in the opening, one note per beat from the idea, eighths in the desire section
    play = []
    if bt >= 4.4 and bt < 26.0:
        play.append((bt, upper[beat_i % len(upper)], 0.9 if beat_i % 4 == 0 else 0.6))
    if 14.2 <= bt < 25.6:
        play.append((bt + BEAT / 2, upper[(beat_i * 3 + 2) % len(upper)], 0.35))
    for (st, m, vel) in play:
        i0 = int(st * SR)
        n = min(int(3.5 * SR), N - i0)
        if n > 0:
            keys[i0:i0 + n] += piano_note(midi(m), n, vel * (0.85 + 0.15 * rng.random()))
    # bass on each chord change once the film opens up
    if beat_i % 8 == 0 and 8.0 <= bt < 26.0:
        i0 = int(bt * SR)
        n = min(int(CHORD_LEN * SR), N - i0)
        tt = np.arange(n) / SR
        f = midi(ch[0] - 12 if ch[0] > 45 else ch[0])
        bass[i0:i0 + n] += (np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(4 * np.pi * f * tt)) \
            * env_adsr(n, 0.3, 2.0) * 0.12
    beat_i += 1

# final resolving chord under the brand card
i0 = int(26.1 * SR)
for m in [62, 69, 74, 78, 81]:
    n = N - i0
    keys[i0:] += piano_note(midi(m), n, 0.45)

dry = pad * 0.9 + keys * 0.09 + bass

# simple stereo convolution reverb (seeded noise IR)
ir_len = int(2.8 * SR)
tt = np.arange(ir_len) / SR
irL = rng.standard_normal(ir_len) * np.exp(-tt * 2.3)
irR = rng.standard_normal(ir_len) * np.exp(-tt * 2.3)
for ir in (irL, irR):
    ir /= np.sqrt(np.sum(ir ** 2))

def conv(x, h):
    L = len(x) + len(h) - 1
    F = 1 << (L - 1).bit_length()
    return np.fft.irfft(np.fft.rfft(x, F) * np.fft.rfft(h, F), F)[: len(x)]

wetL, wetR = conv(dry, irL), conv(dry, irR)
music = np.stack([dry * 0.7 + wetL * 0.45, dry * 0.7 + wetR * 0.45], axis=1)

# master fades: gentle start, graceful end
fade = np.ones(N)
fi, fo = int(1.2 * SR), int(3.0 * SR)
fade[:fi] = np.linspace(0, 1, fi) ** 2
fade[-fo:] = np.linspace(1, 0, fo) ** 1.5
music *= fade[:, None]

# duck under the narration (smoothed envelope of the voice)
win = int(0.35 * SR)
venv = np.convolve(np.abs(vo), np.ones(win) / win, mode="same")
venv = venv / (venv.max() + 1e-9)
speaking = np.clip(venv * 8, 0, 1)
sm = int(0.5 * SR)
speaking = np.convolve(speaking, np.ones(sm) / sm, mode="same")
duck = 1 - 0.45 * np.clip(speaking, 0, 1)        # about -5 dB while she speaks
music *= duck[:, None]

music /= np.abs(music).max()
music *= 0.5
sf.write("assets/audio/music_bed_raw.wav", music, SR, subtype="PCM_24")
print("ok", timing[-1])
