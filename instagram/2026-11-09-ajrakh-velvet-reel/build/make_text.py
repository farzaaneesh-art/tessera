"""Render text overlay PNGs (1080x1920, transparent) and the end card."""
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

S = sys.argv[1]          # scratchpad
LOGO = sys.argv[2]
OUT = f"{S}/text"
import os; os.makedirs(OUT, exist_ok=True)
W, H = 1080, 1920
F = f"{S}/fonts"
CREAM = (250, 246, 234)
GOLD = (231, 198, 152)
OLIVE = (65, 68, 46)
BROWN = (74, 61, 43)

def font(name, size):
    return ImageFont.truetype(f"{F}/{name}", size)

def spaced(draw, xy_center_y, text, fnt, fill, tracking=0, center_x=W // 2):
    # draw text with letter spacing, centred
    widths = [draw.textlength(c, font=fnt) for c in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = center_x - total / 2
    for c, w in zip(text, widths):
        draw.text((x, xy_center_y), c, font=fnt, fill=fill, anchor="ls")
        x += w + tracking
    return total

def overlay(name, lines, y0, rule=True):
    """lines: list of (text, fontfile, size, tracking, gap_after)"""
    txt = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(txt)
    y = y0
    for text, ff, size, tr, gap in lines:
        spaced(d, y, text, font(ff, size), CREAM + (255,), tr)
        y += gap
    if rule:
        d.line([(W / 2 - 60, y0 - 115), (W / 2 + 60, y0 - 115)], fill=GOLD + (255,), width=2)
    # soft shadow for legibility on bright fabric
    alpha = txt.split()[3]
    sh = Image.new("RGBA", (W, H), (30, 22, 12, 0))
    sh.putalpha(alpha.filter(ImageFilter.GaussianBlur(14)).point(lambda a: int(a * 0.85)))
    sh2 = Image.new("RGBA", (W, H), (30, 22, 12, 0))
    sh2.putalpha(alpha.filter(ImageFilter.GaussianBlur(3)).point(lambda a: int(a * 0.6)))
    # soft warm-dark scrim band behind the text block (feathered, no hard edges)
    band = Image.new("L", (W, H), 0)
    bd = ImageDraw.Draw(band)
    bd.rectangle([0, y0 - 230, W, y + 90], fill=120)
    band = band.filter(ImageFilter.GaussianBlur(110))
    scrim = Image.new("RGBA", (W, H), (34, 26, 16, 0)); scrim.putalpha(band)
    out = Image.alpha_composite(Image.alpha_composite(Image.alpha_composite(scrim, sh), sh2), txt)
    out.save(f"{OUT}/{name}.png")

IT = "Cormorant-400-italic.ttf"
RG = "Cormorant-500-normal.ttf"
CZ = "Cinzel-500.ttf"

overlay("t1", [("Some textures", IT, 84, 1, 92), ("speak without words.", IT, 84, 1, 0)], 1180)
overlay("t2", [("AJRAKH", CZ, 70, 14, 86), ("An expression of", IT, 64, 1, 72),
               ("timeless textile artistry.", IT, 64, 1, 0)], 1150)
overlay("t3", [("Rich in texture.", IT, 80, 1, 92), ("Beautiful in character.", IT, 80, 1, 0)], 1180)
overlay("t4", [("2.5 METRES", CZ, 76, 12, 86), ("of possibilities.", IT, 72, 1, 0)], 1180)
overlay("t5", [("Yours to tailor into", IT, 72, 1, 82), ("a top of quiet elegance.", IT, 72, 1, 0)], 1180)

# ---- End card (opaque, warm beige) ----
BEIGE = (241, 233, 218)
card = Image.new("RGBA", (W, H), BEIGE + (255,))
# subtle radial lightening at centre for depth
glow = Image.new("L", (W, H), 0)
gd = ImageDraw.Draw(glow)
gd.ellipse([W / 2 - 700, 520 - 700, W / 2 + 700, 520 + 900], fill=60)
glow = glow.filter(ImageFilter.GaussianBlur(220))
card = Image.composite(Image.new("RGBA", (W, H), (252, 249, 241, 255)), card, glow)
logo = Image.open(LOGO).convert("RGBA")
lw = 470
logo = logo.resize((lw, int(logo.height * lw / logo.width)), Image.LANCZOS)
card.alpha_composite(logo, ((W - lw) // 2, 330))
d = ImageDraw.Draw(card)
y = 330 + logo.height + 120
spaced(d, y, "Naturally Yours.", font(IT, 78), OLIVE, 1); y += 80
d.line([(W / 2 - 70, y), (W / 2 + 70, y)], fill=(201, 160, 105), width=2); y += 95
spaced(d, y, "AJRAKH VELVET  |  2.5 METRES", font(CZ, 40), BROWN, 6); y += 90
spaced(d, y, "Discover the Collection.", font(IT, 52), OLIVE, 1); y += 150
spaced(d, y, "DM us  ·  WhatsApp +971 50 525 2491", font(RG, 36), BROWN, 2)
card.save(f"{OUT}/endcard.png")
print("ok")
