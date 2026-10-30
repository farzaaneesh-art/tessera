"""Build a 1080x1920 Instagram Reel from the product photos in the repo root.

Usage: python3 reel/make_reel.py  ->  writes reel/tessera-reel.mp4
Needs Pillow and ffmpeg.
"""
import os
import subprocess

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "reel", "tessera-reel.mp4")
W, H, FPS = 1080, 1920, 30
FADE = 0.25  # crossfade between shots, seconds

SERIF = "/usr/share/fonts/truetype/crosextra/Caladea-Regular.ttf"
SERIF_I = "/usr/share/fonts/truetype/crosextra/Caladea-Italic.ttf"
SANS = "/usr/share/fonts/opentype/inter/Inter-Light.otf"
SANS_R = "/usr/share/fonts/opentype/inter/Inter-Regular.otf"
SANS_M = "/usr/share/fonts/opentype/inter/Inter-Medium.otf"

CREAM = (250, 244, 232)

# (file, name, line) — copy taken from README.md, trimmed to one short line.
PRODUCTS = [
    ("green-chanderi-kaftan.png.png", "Green Chanderi Kaftan", "Feather-light chanderi silk, leaf impressions."),
    ("black-kaftan.png.png", "Black Kaftan", "Naturally dyed black, botanical accents."),
    ("yellow-marigold-modal.png.png", "Yellow Marigold Modal", "Soft modal drape in marigold tones."),
    ("rust-coloured-kaftan.png.png", "Rust Coloured Kaftan", "Deep rust tones drawn from earth."),
    ("green-yellow-kaftan.png.png", "Green Yellow Kaftan", "A palette shaped by leaves and natural dyes."),
    ("premium-ecoprint.png.png", "Premium Ecoprint", "Crafted through time, pressure and precision."),
    ("red-yellow-kaftan.png.png", "Red Yellow Kaftan", "Bold warmth with organic flow."),
    ("mixed-design-ecoprint.png.png", "Mixed Design Ecoprint", "Each piece carries real botanicals."),
    ("yellow-kaftan-tessera.png.png", "Yellow Kaftan Tessera", "Radiant botanical prints on soft fabric."),
    ("kaftan.png.png", "Classic Kaftan", "Breathable, relaxed, endlessly wearable."),
]

HOOK_DUR, SHOT_DUR, OUTRO_DUR = 3.2, 1.6, 2.8


def font(path, size):
    return ImageFont.truetype(path, size)


def cover(img, scale):
    """Resize so the image covers W x H times `scale`."""
    s = max(W / img.width, H / img.height) * scale
    return img.resize((round(img.width * s), round(img.height * s)), Image.LANCZOS)


def ease(t):
    t = min(max(t, 0.0), 1.0)
    return t * t * (3 - 2 * t)


def ken_burns(base, t, zoom_in, drift):
    """Crop a W x H window from `base` at progress t (0..1), sub-pixel smooth."""
    t = ease(t)
    z = 1.06 + 0.08 * (t if zoom_in else 1 - t)  # 1.06 -> 1.14 or reverse
    k = min(base.width / W, base.height / H)  # base pixels per output pixel at full cover
    cw = W * k / z
    ch = cw * H / W
    cx = base.width / 2 + drift * (t - 0.5) * (base.width - cw) * 0.6
    cy = base.height * 0.46
    x0, y0 = cx - cw / 2, cy - ch / 2
    x0 = min(max(x0, 0), base.width - cw)
    y0 = min(max(y0, 0), base.height - ch)
    a = cw / W
    return base.transform((W, H), Image.AFFINE, (a, 0, x0, 0, a, y0), resample=Image.BICUBIC)


def bottom_shade(strength=235):
    """Dark gradient so text stays readable over any photo."""
    g = Image.new("L", (1, H))
    for y in range(H):
        f = max(0.0, (y - H * 0.5) / (H * 0.5))
        g.putpixel((0, y), int(strength * f ** 1.4))
    g = g.resize((W, H))
    layer = Image.new("RGBA", (W, H), (20, 14, 8, 0))
    layer.putalpha(g)
    return layer


SHADE = bottom_shade()


def text_layer(lines, alpha_fn, t):
    """lines: [(text, font, y, x_or_None, appear_at)]; centred when x is None."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for text, f, y, x, at in lines:
        a = alpha_fn(t - at)
        if a <= 0:
            continue
        rise = int((1 - a) * 24)
        if x is None:
            x_pos = (W - d.textlength(text, font=f)) / 2
        else:
            x_pos = x
        # soft shadow
        sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(sh).text((x_pos, y + rise + 3), text, font=f, fill=(0, 0, 0, int(200 * a)))
        layer = Image.alpha_composite(layer, sh.filter(ImageFilter.GaussianBlur(6)))
        d = ImageDraw.Draw(layer)
        d.text((x_pos, y + rise), text, font=f, fill=CREAM + (int(255 * a),))
    return layer


def fade_in(dt, dur=0.35):
    return ease(dt / dur) if dt > 0 else 0.0


def spaced(text, n=1):
    return (" " * n).join(text)


def build_shots():
    shots = []
    imgs = [Image.open(os.path.join(ROOT, f)).convert("RGB") for f, _, _ in PRODUCTS]
    bases = [cover(im, 1.1) for im in imgs]

    f_name = font(SERIF, 76)
    f_line = font(SANS_R, 42)
    f_idx = font(SANS_M, 30)
    n = len(PRODUCTS)

    # 1. Hook: first frame must already carry text so the reel stops the scroll.
    hook_base = bases[0]
    hook_name, hook_line = PRODUCTS[0][1], PRODUCTS[0][2]
    f_big = font(SERIF_I, 112)
    f_small = font(SANS, 40)

    def hook(t):
        frame = ken_burns(hook_base, t / HOOK_DUR, True, 0).convert("RGBA")
        dim = Image.new("RGBA", (W, H), (15, 10, 5, 90))
        frame = Image.alpha_composite(frame, dim)
        frame = Image.alpha_composite(frame, SHADE)
        lines = [
            ("Dyed by leaves.", f_big, 300, None, -1),  # visible from frame 0
            ("Not machines.", f_big, 430, None, 0.7),
            (spaced("TESSERA  ECOPRINT", 1).upper(), f_small, 620, None, 1.2),
            (f"01 / {n:02d}", f_idx, 1180, 80, 1.3),
            (hook_name, f_name, 1225, 80, 1.4),
            (hook_line, f_line, 1325, 80, 1.55),
        ]
        return Image.alpha_composite(frame, text_layer(lines, fade_in, t))

    shots.append((HOOK_DUR, hook))

    # 2. One quick shot per product.
    # The hook already shows product 01, so the run starts at 02.
    for i, ((_, name, line), base) in list(enumerate(zip(PRODUCTS, bases)))[1:]:
        def shot(t, base=base, name=name, line=line, i=i):
            frame = ken_burns(base, t / SHOT_DUR, i % 2 == 0, 1 if i % 2 else -1).convert("RGBA")
            frame = Image.alpha_composite(frame, SHADE)
            lines = [
                (f"{i + 1:02d} / {n:02d}", f_idx, 1180, 80, 0.05),
                (name, f_name, 1225, 80, 0.12),
                (line, f_line, 1325, 80, 0.25),
            ]
            return Image.alpha_composite(frame, text_layer(lines, fade_in, t))

        shots.append((SHOT_DUR, shot))

    # 3. Outro / call to action over a blurred collage colour.
    outro_base = cover(imgs[4], 1.1).filter(ImageFilter.GaussianBlur(28))
    f_brand = font(SERIF, 120)
    f_cta = font(SANS_M, 44)

    def outro(t):
        frame = ken_burns(outro_base, t / OUTRO_DUR, False, 0).convert("RGBA")
        frame = Image.alpha_composite(frame, Image.new("RGBA", (W, H), (20, 14, 8, 150)))
        lines = [
            (spaced("TESSERA", 2), f_brand, 640, None, 0.1),
            ("Shaped by real botanicals.", font(SERIF_I, 56), 830, None, 0.5),
            ("No two pieces alike.", font(SERIF_I, 56), 905, None, 0.8),
            ("DM  “KAFTAN”  TO ORDER", f_cta, 1110, None, 1.3),
        ]
        return Image.alpha_composite(frame, text_layer(lines, fade_in, t))

    shots.append((OUTRO_DUR, outro))
    return shots


def main():
    shots = build_shots()
    # Shot k starts at sum(previous durations) - k*FADE so neighbours overlap.
    starts, t0 = [], 0.0
    for dur, _ in shots:
        starts.append(t0)
        t0 += dur - FADE
    total = t0 + FADE
    frames = int(round(total * FPS))

    cmd = [
        "ffmpeg", "-y", "-loglevel", "error",
        "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
        "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
        "-shortest", "-c:v", "libx264", "-preset", "slow", "-crf", "19",
        "-pix_fmt", "yuv420p", "-profile:v", "high", "-movflags", "+faststart",
        "-c:a", "aac", "-b:a", "128k", OUT,
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for k in range(frames):
        t = k / FPS
        active = [(i, t - s) for i, s in enumerate(starts) if s <= t < s + shots[i][0]]
        img = None
        for i, lt in active:
            fr = shots[i][1](lt).convert("RGB")
            if img is None:
                img = fr
            else:  # crossfade into the incoming shot
                img = Image.blend(img, fr, ease(lt / FADE))
        proc.stdin.write(img.tobytes())
    proc.stdin.close()
    proc.wait()
    print(f"wrote {OUT} ({total:.1f}s, {frames} frames)")


if __name__ == "__main__":
    main()
