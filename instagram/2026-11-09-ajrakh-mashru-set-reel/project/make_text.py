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

overlay("t1", [("An ode to", IT, 84, 1, 96), ("timeless heritage.", IT, 84, 1, 0)], 1180)
overlay("t2", [("AJRAKH  ·  MASHRU", CZ, 60, 10, 88), ("A story woven", IT, 70, 1, 80), ("in tradition.", IT, 70, 1, 0)], 1150)
overlay("t3", [("Two pieces.", IT, 80, 1, 92), ("One beautiful expression.", IT, 80, 1, 0)], 1180)
overlay("t4", [("HAND BLOCK PRINTED", JO, 36, 9, 58), ("NATURALLY DYED", JO, 36, 9, 0)], 1220)

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
spaced(d, y, "AJRAKH MASHRU", font(CZ, 54), BROWN, 10); y += 66
spaced(d, y, "TOP & BOTTOM SET  ·  HAND BLOCK PRINTED  ·  NATURALLY DYED", font(JO, 23), BROWN, 3); y += 115
spaced(d, y, "DM to enquire", font(IT, 58), OLIVE, 1); y += 70
spaced(d, y, "WhatsApp +971 50 525 2491", font(JOL, 30), BROWN, 2)
card.save(f"{OUT}/endcard.png")

# ---------- Cover: cream title band + real photo ----------
src = Image.open(COVER_SRC).convert("RGB")
BAND = 560
ph_h = H - BAND
sw, sh_ = src.size
scale = W / sw
ph = src.resize((W, int(sh_ * scale)), Image.LANCZOS)
top = max(0, (ph.height - ph_h) // 2)
ph = ph.crop((0, top, W, top + ph_h))
cov = Image.new("RGB", (W, H), (250, 246, 234)); cov.paste(ph, (0, BAND))
d = ImageDraw.Draw(cov)
spaced(d, 330, "TESSERA", font(CZ, 40), OLIVE, 16)
d.line([(W / 2 - 50, 366), (W / 2 + 50, 366)], fill=(201, 160, 105), width=2)
spaced(d, 452, "Ajrakh Mashru Set", font(IT, 92), OLIVE, 1)
spaced(d, 512, "TOP & BOTTOM  ·  HAND BLOCK PRINTED  ·  NATURALLY DYED", font(JO, 23), BROWN, 3)
cov.save(f"{OUT}/cover.jpg", quality=95)
print("ok")
