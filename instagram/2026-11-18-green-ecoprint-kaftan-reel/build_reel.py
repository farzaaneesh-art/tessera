import subprocess, os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

S = "/tmp/claude-0/-home-user-tessera/e7dd8a54-55fb-55b5-9b3e-057707d50fae/scratchpad"
U = "/root/.claude/uploads/e7dd8a54-55fb-55b5-9b3e-057707d50fae"
FD = "/root/.claude/plugins/synced/5b983104-35b1-44ad-9650-6be25a8f60b3_bf3cb9d3-a57e-4e68-9be6-86d008990efc/82436e8d-b5bb-4da5-b372-0309f771299f/skills/animation-studio/examples/wedding-invite/assets/fonts"
LOGO = "/home/user/tessera/images/tessera-logo.jpg"
OUT = sys.argv[1]
W, H, FPS = 1080, 1920, 30
T = os.path.join(S, "build", "tmp"); os.makedirs(T, exist_ok=True)

DRAFT = f"{U}/74ef76c0-tessera_reel_draft.mp4"
M1618 = f"{U}/7590ed52-IMG_1618.mov"
M1620 = f"{U}/0bc02ee3-IMG_1620.mov"

CREAM = (250, 246, 234); OLIVE = (65, 68, 46); GOLD = (231, 198, 152)
GRADE = ("eq=contrast=1.04:saturation=1.03:gamma=1.01,"
         "colorbalance=rs=0.02:bs=-0.03:rm=0.025:bm=-0.035:rh=0.015:bh=-0.03,"
         "vignette=angle=PI/6")

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: print(" ".join(cmd)); print(r.stderr[-3000:]); sys.exit(1)

def font(name, size): return ImageFont.truetype(f"{FD}/{name}", size)

def text_png(path, lines, y_center=1560):
    """Cream serif lines on a soft lower gradient, with a thin gold rule."""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    grad = Image.new("L", (1, H))
    for y in range(H):
        a = 0 if y < 1150 else int(min(1, (y - 1150) / 600) * 120)
        grad.putpixel((0, y), a)
    shade = Image.new("RGBA", (W, H), (40, 30, 20, 255)); shade.putalpha(grad.resize((W, H)))
    im = Image.alpha_composite(im, shade)
    d = ImageDraw.Draw(im)
    y = y_center
    for txt, f, col, sp in lines:
        bw = d.textlength(txt, font=f) + sp * (len(txt) - 1)
        x = (W - bw) / 2
        for ch in txt:
            d.text((x, y), ch, font=f, fill=col, anchor="ls"); x += d.textlength(ch, font=f) + sp
        y += f.size * 1.5
    d.line([(W/2 - 60, y_center - f.size - 40), (W/2 + 60, y_center - f.size - 40)], fill=GOLD + (255,), width=2)
    im.save(path)

def endcard(path):
    im = Image.new("RGB", (W, H), CREAM)
    logo = Image.open(LOGO).convert("RGB")
    # crop white margins
    import PIL.ImageOps as O
    bbox = O.invert(logo.convert("L")).point(lambda p: 255 if p > 18 else 0).getbbox()
    logo = logo.crop(bbox); logo.thumbnail((560, 560))
    # blend logo white -> cream so it sits on the card
    lw = logo.convert("RGBA"); px = lw.load()
    for yy in range(lw.height):
        for xx in range(lw.width):
            r, g, b, a = px[xx, yy]
            if r > 235 and g > 235 and b > 235: px[xx, yy] = CREAM + (255,)
    im.paste(lw.convert("RGB"), ((W - lw.width)//2, 430))
    d = ImageDraw.Draw(im)
    y = 430 + lw.height + 110
    d.line([(W/2-70, y), (W/2+70, y)], fill=GOLD, width=2)
    def c(txt, f, col, yy):
        d.text((W/2, yy), txt, font=f, fill=col, anchor="mm")
    c("Naturally Yours.", font("CormorantGaramond-600.ttf", 76), OLIVE, y + 90)
    c("CURATED INDIAN CRAFTSMANSHIP", font("Cinzel-500.ttf", 30), (154, 78, 50), y + 190)
    c("BOTANICAL ECOPRINT", font("Cinzel-500.ttf", 30), (154, 78, 50), y + 240)
    c("DM or WhatsApp +971 50 525 2491", font("CormorantGaramond-600.ttf", 44), OLIVE, y + 380)
    im.save(path)

# ---- shots: (name, src, start, src_dur, speed, crop, zoom_from, zoom_to, text)
cinzel = font("Cinzel-700.ttf", 116); corm = font("CormorantGaramond-600.ttf", 74); corm_s = font("CormorantGaramond-600.ttf", 50)
shots = [
    ("s1", M1618, 0.4, 2.1, 0.5, "780:1387:150:400", 1.00, 1.07,
        [("TESSERA", cinzel, CREAM, 14), ("Naturally Yours.", corm, CREAM, 2)]),
    ("s2", DRAFT, 14.3, 3.4, 1.0, None, 1.02, 1.12,
        [("Real leaves,", corm, CREAM, 2), ("pressed into cloth.", corm, CREAM, 2)]),
    ("s3", DRAFT, 4.0, 1.3, 0.8, None, 1.04, 1.10, None),
    ("s4", DRAFT, 8.0, 2.4, 0.75, None, 1.02, 1.06,
        [("Fluid. Light. Unhurried.", corm, CREAM, 2)]),
    ("s5", M1620, 0.0, 2.1, 0.5, "703:1250:110:380", 1.06, 1.00,
        [("No two pieces alike.", corm, CREAM, 2)]),
]
XF = 0.6
clips = []
for name, src, ss, sd, speed, crop, z0, z1, txt in shots:
    dur = sd / speed
    vf = []
    if crop: vf.append(f"crop={crop}")
    vf.append(f"scale={W}:{H}:flags=lanczos")
    if speed != 1.0:
        vf.append(f"setpts=PTS/{speed}")
        # 60fps sources at 0.5x are native 30fps slow-mo; 30fps sources get soft frame blending
        vf.append(f"framerate=fps={FPS}" if src == DRAFT else f"fps={FPS}")
    else:
        vf.append(f"fps={FPS}")
    # slow push: scale per frame then centre-crop
    vf.append(f"scale=w='trunc({W}*({z0}+({z1}-{z0})*t/{dur})/2)*2':h='trunc({H}*({z0}+({z1}-{z0})*t/{dur})/2)*2':eval=frame:flags=bicubic")
    vf.append(f"crop={W}:{H}")
    vf.append(GRADE)
    vf.append("format=yuv420p")
    out = f"{T}/{name}.mp4"
    inputs = ["-ss", str(ss), "-t", str(sd), "-i", src]
    if txt:
        p = f"{T}/{name}.png"; text_png(p, txt)
        fc = f"[0:v]{','.join(vf)}[v];[1:v]format=rgba,fade=in:st=0.5:d=0.7:alpha=1,fade=out:st={dur-1.1:.2f}:d=0.6:alpha=1[t];[v][t]overlay=format=auto,format=yuv420p[o]"
        cmd = ["ffmpeg", "-v", "error", "-y", *inputs, "-loop", "1", "-t", f"{dur:.3f}", "-i", p,
               "-filter_complex", fc, "-map", "[o]"]
    else:
        cmd = ["ffmpeg", "-v", "error", "-y", *inputs, "-vf", ",".join(vf)]
    run(cmd + ["-an", "-t", f"{dur:.3f}", "-c:v", "libx264", "-crf", "14", "-preset", "medium", out])
    clips.append((out, dur)); print(name, round(dur, 2))

ec = f"{T}/endcard.png"; endcard(ec)
ecv = f"{T}/endcard.mp4"; ED = 4.0
run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-t", str(ED), "-i", ec, "-vf",
     f"fps={FPS},scale=w='trunc({W}*(1+0.03*t/{ED})/2)*2':h='trunc({H}*(1+0.03*t/{ED})/2)*2':eval=frame,crop={W}:{H},format=yuv420p",
     "-c:v", "libx264", "-crf", "14", ecv])
clips.append((ecv, ED))

# ---- chain dissolves
args = []
for p, _ in clips: args += ["-i", p]
fc, prev, off = [], "[0:v]", 0.0
for i in range(1, len(clips)):
    off += clips[i-1][1] - XF
    lab = f"[x{i}]"
    fc.append(f"{prev}[{i}:v]xfade=transition=fade:duration={XF}:offset={off:.3f}{lab}")
    prev = lab
total = sum(d for _, d in clips) - XF * (len(clips) - 1)
fc.append(f"{prev}fade=in:st=0:d=0.5,format=yuv420p[v]")
run(["ffmpeg", "-v", "error", "-y", *args, "-f", "lavfi", "-t", f"{total:.3f}", "-i", "anullsrc=r=48000:cl=stereo",
     "-filter_complex", ";".join(fc), "-map", "[v]", "-map", f"{len(clips)}:a",
     "-c:v", "libx264", "-crf", "17", "-preset", "slow", "-profile:v", "high", "-pix_fmt", "yuv420p",
     "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", "-shortest", OUT])
print("total", round(total, 2))
