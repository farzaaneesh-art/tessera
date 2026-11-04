"""Build the TESSERA 30s 9:16 reel (photo cut) from the product images in this repo.

Usage: python3 reel/build_reel.py <fonts_dir> <out_dir>
Needs: Pillow, numpy, ffmpeg on PATH. Fonts: Cormorant Garamond TTFs named
CG-normal-400.ttf, CG-normal-500.ttf, CG-italic-400.ttf, CG-normal-300.ttf.
"""
import os
import subprocess
import sys
import wave

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)

W, H, FPS, DUR = 1080, 1920, 30, 30.0
XF = 0.35  # crossfade length (s)


def load(name, sharpen=True):
    im = Image.open(os.path.join(ROOT, name + ".png.png")).convert("RGB")
    return im.filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2)) if sharpen else im


IMG = {n: load(n) for n in [
    "mixed-design-ecoprint", "green-chanderi-kaftan", "premium-ecoprint",
    "rust-coloured-kaftan", "green-yellow-kaftan", "yellow-marigold-modal",
    "red-yellow-kaftan", "yellow-kaftan-tessera"]}


def box(cx, cy, w):
    """9:16 crop box centred on (cx, cy) with width w (source px)."""
    h = w * 16 / 9
    return np.array([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2])


FULL = lambda cx=543: box(cx, 724, 814)  # widest 9:16 crop of a 1086x1448 photo

# (start, end, image, box_from, box_to, transition_in)
SHOTS = [
    (0.0, 1.4, "mixed-design-ecoprint", box(600, 700, 400), box(600, 690, 360), "cut"),
    (1.4, 5.2, "green-chanderi-kaftan", box(640, 760, 440), box(640, 880, 420), "fade"),
    (5.2, 8.8, "rust-coloured-kaftan", box(500, 820, 420), box(520, 760, 400), "fade"),
    (8.8, 11.2, "green-yellow-kaftan", box(540, 1040, 300), box(560, 1060, 280), "fade"),
    (11.2, 13.6, "yellow-marigold-modal", box(520, 900, 460), box(540, 860, 430), "fade"),
    (13.6, 18.2, "premium-ecoprint", box(560, 640, 300), FULL(543), "fade"),  # reveal pull-back
    (18.2, 20.07, "green-yellow-kaftan", FULL(543), box(543, 724, 770), "cut"),
    (20.07, 21.93, "red-yellow-kaftan", FULL(543), box(543, 724, 770), "cut"),
    (21.93, 23.8, "yellow-kaftan-tessera", FULL(560), box(560, 724, 770), "cut"),
    (23.8, 26.4, "mixed-design-ecoprint", FULL(543), box(543, 700, 740), "fade"),
]
END_START = 26.4

CAPTIONS = [
    (0.5, 2.4, "Flowers bloom. Leaves grow."),
    (2.6, 5.0, "And eventually,\nnature lets them go."),
    (5.4, 8.6, "What if we could keep\na little of that beauty?"),
    (8.9, 11.1, "Silver oak leaves,\nmarigold and cosmos —"),
    (11.2, 13.4, "pressed into\nsoft modal."),
    (13.8, 18.0, "Through eco-printing,\nnature leaves something\nunexpected."),
    (18.4, 20.0, "Earthy tones."),
    (20.2, 21.8, "Delicate impressions."),
    (22.0, 23.6, "Never exactly repeated."),
]

f_cap = ImageFont.truetype(os.path.join(FONTS, "CG-normal-500.ttf"), 80)
f_logo = ImageFont.truetype(os.path.join(FONTS, "CG-normal-400.ttf"), 132)
f_tag = ImageFont.truetype(os.path.join(FONTS, "CG-italic-400.ttf"), 64)
f_cta = ImageFont.truetype(os.path.join(FONTS, "CG-normal-500.ttf"), 48)
CREAM = (246, 240, 228)

ease = lambda x: x * x * (3 - 2 * x)


def render_shot(s, t):
    t0, t1, name, b0, b1, _ = s
    p = ease(min(max((t - t0) / (t1 - t0), 0), 1))
    b = b0 + (b1 - b0) * p
    return IMG[name].transform((W, H), Image.Transform.EXTENT, tuple(b), Image.Resampling.BICUBIC)


# Scrim: soft dark gradient behind captions for legibility (kept out of the Reels UI zone).
scrim = Image.new("L", (W, H), 0)
sd = ImageDraw.Draw(scrim)
for y in range(1000, H):
    sd.line([(0, y), (W, y)], fill=int(205 * min(1, (y - 1000) / 380)))
SCRIM = Image.composite(Image.new("RGB", (W, H), (20, 14, 8)), Image.new("RGB", (W, H)), scrim)


def text_block(draw, txt, font, cy, alpha, fill=CREAM, spacing=10):
    lines = txt.split("\n")
    hs = [draw.textbbox((0, 0), ln, font=font) for ln in lines]
    total = sum(b[3] - b[1] for b in hs) + spacing * (len(lines) - 1)
    y = cy - total / 2
    for ln, b in zip(lines, hs):
        w = b[2] - b[0]
        x = (W - w) / 2 - b[0] - 40  # nudge left of centre: keeps clear of the Reels button column
        draw.text((x, y - b[1]), ln, font=font, fill=fill + (int(255 * alpha),))
        y += b[3] - b[1] + spacing


def fade(t, a, b, d=0.25):
    return max(0.0, min(1.0, (t - a) / d, (b - t) / d))


# End-card background: last frame of the mixed-design shot, blurred and warmed down.
end_bg = render_shot(SHOTS[-1], 26.4).filter(ImageFilter.GaussianBlur(28))
end_bg = Image.blend(end_bg, Image.new("RGB", (W, H), (58, 44, 30)), 0.55)


def frame(t):
    if t >= END_START:
        base = end_bg.copy()
        prev = render_shot(SHOTS[-1], t)
        k = min(1, (t - END_START) / 0.6)
        base = Image.blend(prev, base, ease(k))
    else:
        cur = [s for s in SHOTS if s[0] <= t < s[1]][0]
        base = render_shot(cur, t)
        i = SHOTS.index(cur)
        if cur[5] == "fade" and t - cur[0] < XF and i > 0:
            base = Image.blend(render_shot(SHOTS[i - 1], t), base, ease((t - cur[0]) / XF))
        base = Image.blend(base, Image.composite(SCRIM, base, scrim), 1.0)

    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    for a, b, txt in CAPTIONS:
        al = fade(t, a, b)
        if al > 0:
            # soft shadow then text
            sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            text_block(ImageDraw.Draw(sh), txt, f_cap, 1290, al * 0.85, fill=(0, 0, 0))
            ov = Image.alpha_composite(ov, sh.filter(ImageFilter.GaussianBlur(9)))
            d = ImageDraw.Draw(ov)
            text_block(d, txt, f_cap, 1290, al)
    if t >= END_START:
        def tb(txt, font, cy, a, sp=10):
            text_block(d, txt, font, cy, a, spacing=sp)
        # end card sits in the vertical centre — well inside the safe zone
        tb("T E S S E R A", f_logo, 760, fade(t, 26.7, 99, 0.7))
        tb("Not inspired by nature.\nMade by it.", f_tag, 960, fade(t, 27.4, 99, 0.6), 14)
        tb("Each piece one of a kind  ·  Link in bio", f_cta, 1150, fade(t, 28.2, 99, 0.5))
    return Image.alpha_composite(base.convert("RGBA"), ov).convert("RGB")


# ---------- temp music bed (synthesised; replace with licensed track) ----------
SR = 48000
n = int(SR * DUR)
tt = np.arange(n) / SR
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
CH = [(0, 7, [50, 57, 62, 66, 73]), (7, 13.6, [47, 54, 62, 66, 69]),
      (13.6, 18.2, [43, 50, 59, 62, 66]), (18.2, 23.8, [45, 52, 59, 64, 69]),
      (23.8, 26.4, [43, 50, 59, 62, 66]), (26.4, 30, [50, 57, 62, 66, 69])]
pad = np.zeros(n)
for a, b, notes in CH:
    env = np.clip(np.minimum((tt - a + 0.8) / 1.6, (b + 0.8 - tt) / 1.6), 0, 1)
    for m in notes:
        f = nt(m)
        v = 0.5 * np.sin(2 * np.pi * f * tt) + 0.5 * np.sin(2 * np.pi * f * 1.003 * tt + 1)
        pad += env * v * (0.6 if m < 55 else 0.35)
plk = np.zeros(n)
for at, m in [(0.0, 81), (1.4, 78), (5.2, 76), (8.8, 74), (11.2, 78), (13.6, 81), (16.0, 83),
              (18.2, 83), (20.07, 81), (21.93, 78), (23.8, 76), (26.6, 74), (26.6, 81), (28.0, 78)]:
    i0 = int(at * SR)
    L = min(n - i0, int(3.5 * SR))
    x = np.arange(L) / SR
    f = nt(m)
    tone = sum(np.sin(2 * np.pi * f * k * x) / k ** 2.2 for k in (1, 2, 3, 4))
    plk[i0:i0 + L] += tone * np.exp(-x * 2.2) * np.minimum(1, x / 0.004)
rng = np.random.default_rng(7)
air = np.convolve(rng.standard_normal(n), np.ones(400) / 400, "same") * 0.8
ir_len = int(2.2 * SR)
ir = rng.standard_normal(ir_len) * np.exp(-np.arange(ir_len) / SR * 3.0)
wet = np.fft.irfft(np.fft.rfft(plk, 2 * n) * np.fft.rfft(ir, 2 * n))[:n] * 0.02
mix = pad / 6 + plk * 0.22 + wet + air * 0.15
mix *= np.minimum(1, tt / 0.4) * np.clip((DUR - tt) / 1.8, 0, 1)
mix = mix / np.abs(mix).max() * 0.5  # ~ -6 dBFS peak; sits low enough for a VO on top
with wave.open(os.path.join(OUT, "music_temp.wav"), "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((mix * 32767).astype(np.int16).tobytes())

# ---------- render ----------
outmp4 = os.path.join(OUT, "tessera_reel_v1.mp4")
cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
       "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", os.path.join(OUT, "music_temp.wav"),
       "-vf", "eq=saturation=0.86:contrast=1.02,colorbalance=rm=0.03:bm=-0.03:rh=0.02:bh=-0.02",
       "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-pix_fmt", "yuv420p",
       "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest", outmp4]
p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
for k in range(int(DUR * FPS)):
    t = k / FPS
    fr = frame(t)
    p.stdin.write(fr.tobytes())
    if k in (15, 90, 200, 300, 350, 400, 470, 560, 620, 885):
        fr.resize((540, 960)).save(os.path.join(OUT, f"check_{k:03d}.jpg"), quality=85)
p.stdin.close()
p.wait()
print("done", outmp4)
