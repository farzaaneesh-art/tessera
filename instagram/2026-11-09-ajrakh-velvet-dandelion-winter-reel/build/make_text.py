"""Text overlays, end card and cover for the Ajrakh Velvet winter reel."""
import sys, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W_DIR, FONTS, LOGO, COVER_SRC = sys.argv[1:5]
OUT = f"{W_DIR}/text"; os.makedirs(OUT, exist_ok=True)
W, H = 1080, 1920
CREAM = (250, 246, 234); GOLD = (231, 198, 152); OLIVE = (65, 68, 46); BROWN = (74, 61, 43)
IT, CZ, JO, JOL = "Cormorant-400-italic.ttf", "Cinzel-500.ttf", "Jost-400.ttf", "Jost-300.ttf"

def font(n, s): return ImageFont.truetype(f"{FONTS}/{n}", s)

def spaced(d, y, text, fnt, fill, tr=0, cx=W // 2):
    ws = [d.textlength(c, font=fnt) for c in text]
    x = cx - (sum(ws) + tr * (len(text) - 1)) / 2
    for c, w in zip(text, ws):
        d.text((x, y), c, font=fnt, fill=fill, anchor="ls"); x += w + tr

def overlay(name, lines, y0):
    """lines: (text, font, size, tracking, gap_after)."""
    txt = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(txt)
    y = y0
    for t, f, s, tr, gap in lines:
        spaced(d, y, t, font(f, s), CREAM + (255,), tr); y += gap
    d.line([(W / 2 - 60, y0 - 110), (W / 2 + 60, y0 - 110)], fill=GOLD + (255,), width=2)
    a = txt.split()[3]
    band = Image.new("L", (W, H), 0)
    ImageDraw.Draw(band).rectangle([0, y0 - 230, W, y + 90], fill=125)
    band = band.filter(ImageFilter.GaussianBlur(110))
    scrim = Image.new("RGBA", (W, H), (30, 22, 14, 0)); scrim.putalpha(band)
    sh = Image.new("RGBA", (W, H), (30, 22, 12, 0)); sh.putalpha(a.filter(ImageFilter.GaussianBlur(12)).point(lambda v: int(v * .8)))
    sh2 = Image.new("RGBA", (W, H), (30, 22, 12, 0)); sh2.putalpha(a.filter(ImageFilter.GaussianBlur(3)).point(lambda v: int(v * .55)))
    out = scrim
    for layer in (sh, sh2, txt): out = Image.alpha_composite(out, layer)
    out.save(f"{OUT}/{name}.png")

overlay("t1", [("Winter is approaching.", IT, 80, 1, 92), ("Let your wardrobe feel it.", IT, 80, 1, 0)], 1180)
overlay("t2", [("AJRAKH", CZ, 68, 14, 88), ("An age-old art of printing.", IT, 64, 1, 74),
               ("A beauty that never fades.", IT, 64, 1, 0)], 1150)
overlay("t3", [("Naturally dyed.", IT, 70, 1, 80), ("Hand block printed.", IT, 70, 1, 80),
               ("Rooted in tradition.", IT, 70, 1, 0)], 1140)
overlay("t4", [("Soft textures. Rich character.", IT, 64, 1, 78), ("WINTER-READY ELEGANCE", JO, 34, 8, 0)], 1190)
overlay("t5", [("2.5 METRES", CZ, 74, 12, 88), ("Your style. Your creation.", IT, 66, 1, 0)], 1180)

# ---------- End card ----------
BEIGE = (241, 233, 218)
def beige_bg():
    card = Image.new("RGBA", (W, H), BEIGE + (255,))
    g = Image.new("L", (W, H), 0)
    ImageDraw.Draw(g).ellipse([W / 2 - 700, -180, W / 2 + 700, 1420], fill=60)
    g = g.filter(ImageFilter.GaussianBlur(220))
    return Image.composite(Image.new("RGBA", (W, H), (252, 249, 241, 255)), card, g)

card = beige_bg()
logo = Image.open(LOGO).convert("RGBA"); lw = 440
logo = logo.resize((lw, int(logo.height * lw / logo.width)), Image.LANCZOS)
card.alpha_composite(logo, ((W - lw) // 2, 300))
d = ImageDraw.Draw(card)
y = 300 + logo.height + 115
spaced(d, y, "Naturally Yours.", font(IT, 76), OLIVE, 1); y += 78
d.line([(W / 2 - 70, y), (W / 2 + 70, y)], fill=(201, 160, 105), width=2); y += 100
spaced(d, y, "AJRAKH VELVET", font(CZ, 54), BROWN, 10); y += 70
spaced(d, y, "2.5 METRES  ·  NATURALLY DYED  ·  HAND BLOCK PRINTED", font(JO, 25), BROWN, 3); y += 95
spaced(d, y, "Discover the collection.", font(IT, 52), OLIVE, 1); y += 140
spaced(d, y, "DM us  ·  WhatsApp +971 50 525 2491", font(JOL, 30), BROWN, 2)
card.save(f"{OUT}/endcard.png")

# ---------- Cover (1080x1920; key info inside the centre 1080x1350 grid crop) ----------
src = Image.open(COVER_SRC).convert("RGB")
sw, sh_ = src.size; tw = int(sh_ * 9 / 16)
x0 = (sw - tw) // 2
cov = src.crop((x0, 0, x0 + tw, sh_)).resize((W, H), Image.LANCZOS).convert("RGBA")
grad = Image.new("L", (W, H), 0); gd = ImageDraw.Draw(grad)
for yy in range(H):  # darken top and bottom for type
    v = max(0, 1 - yy / 900) * 205 + max(0, (yy - 1500) / 420) * 120
    gd.line([(0, yy), (W, yy)], fill=int(min(v, 200)))
dark = Image.new("RGBA", (W, H), (28, 20, 12, 0)); dark.putalpha(grad)
cov = Image.alpha_composite(cov, dark)
txt = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(txt)
spaced(d, 225, "TESSERA", font(CZ, 40), CREAM, 16)
d.line([(W / 2 - 50, 262), (W / 2 + 50, 262)], fill=GOLD, width=2)
spaced(d, 372, "Ajrakh Velvet", font(IT, 112), CREAM, 1)
spaced(d, 432, "2.5 METRES  ·  NATURALLY DYED  ·  HAND BLOCK PRINTED", font(JO, 25), CREAM, 3)
a = txt.split()[3]
s1 = Image.new("RGBA", (W, H), (20, 14, 8, 0)); s1.putalpha(a.filter(ImageFilter.GaussianBlur(10)).point(lambda v: int(v * .7)))
cov = Image.alpha_composite(Image.alpha_composite(cov, s1), txt)
cov.convert("RGB").save(f"{OUT}/cover.jpg", quality=95)
print("ok")
