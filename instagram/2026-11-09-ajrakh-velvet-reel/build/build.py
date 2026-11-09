"""Assemble the TESSERA Ajrakh reel with ffmpeg."""
import subprocess, sys, os

S = sys.argv[1]
SRC = f"{S}/src"
SH = f"{S}/shots"; os.makedirs(SH, exist_ok=True)
X = 0.5  # crossfade length

# (clip, src_start, src_len, speed, zoom_from, zoom_to)
shots = [
    ("2852", 4.9, 3.4, 0.85, 1.00, 1.07),  # A hook: sheen + border in low sun
    ("2871", 3.2, 4.4, 1.0, 1.04, 1.00),   # B ajrakh floral band, slow pan
    ("2862", 13.8, 2.2, 1.0, 1.00, 1.04),  # C floral band close
    ("2865", 0.8, 3.5, 1.0, 1.00, 1.05),   # D hanging in light, movement
    ("2862", 15.8, 3.5, 1.0, 1.03, 1.00),  # E crushed surface close
    ("2860", 9.6, 2.95, 1.0, 1.00, 1.03),  # F complete layout, flat
    ("2862", 21.4, 4.0, 1.0, 1.00, 1.03),  # G complete panel, hanging
    ("2862", 6.0, 3.0, 1.0, 1.04, 1.00),   # H hanging panel, garment-like
    ("2852", 14.0, 2.0, 1.0, 1.02, 1.06),  # I return to texture
]
END_LEN = 4.5

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        print(r.stderr[-3000:]); sys.exit(1)

durs = []
for i, (c, ss, ln, sp, z0, z1) in enumerate(shots):
    out_len = ln / sp
    nfr = round(out_len * 30)
    durs.append(nfr / 30)
    vf = (
        f"setpts=(PTS-STARTPTS)/{sp},fps=30,"
        "hqdn3d=1.2:1.2:2.5:2.5,"
        "scale=2160:3840:flags=lanczos,setsar=1,"
        f"zoompan=z='{z0}+({z1}-{z0})*on/{nfr}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
        f":d=1:s=1080x1920:fps=30,"
        "eq=contrast=1.04:saturation=1.02:gamma=1.01,"
        "unsharp=5:5:0.45:5:5:0,"
        "vignette=angle=0.32,format=yuv420p"
    )
    run(["ffmpeg", "-v", "error", "-y", "-ss", str(ss), "-t", str(ln + 0.2),
         "-i", f"{SRC}/IMG_{c}_compressed.mp4", "-vf", vf, "-frames:v", str(nfr),
         "-an", "-c:v", "libx264", "-crf", "12", "-preset", "medium", f"{SH}/s{i}.mp4"])
    print("shot", i, durs[-1])

# end card as video
nfr = round(END_LEN * 30)
run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", f"{S}/text/endcard.png",
     "-vf", f"zoompan=z='1.0+0.02*on/{nfr}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30,format=yuv420p",
     "-frames:v", str(nfr), "-c:v", "libx264", "-crf", "12", f"{SH}/end.mp4"])
durs.append(nfr / 30)
files = [f"{SH}/s{i}.mp4" for i in range(len(shots))] + [f"{SH}/end.mp4"]

starts = []; acc = 0
for i, d in enumerate(durs):
    starts.append(acc); acc += d - X
total = starts[-1] + durs[-1]
print("starts", [round(s, 2) for s in starts], "total", round(total, 2))

# text windows (seconds on final timeline), relative to shot starts
texts = [
    ("t1", 0.35, starts[1] - 0.15),
    ("t2", starts[1] + 0.45, starts[3] - 0.2),
    ("t3", starts[3] + 0.45, starts[5] - 0.2),
    ("t4", starts[5] + 0.4, starts[7] - 0.2),
    ("t5", starts[7] + 0.35, starts[9] - 0.15),
]

inputs = []
for f in files:
    inputs += ["-i", f]
for name, a, b in texts:
    inputs += ["-loop", "1", "-t", f"{total:.3f}", "-i", f"{S}/text/{name}.png"]
inputs += ["-i", f"{S}/music.wav"]

fc = []
prev = "[0:v]"
for i in range(1, len(files)):
    off = starts[i]
    tr = "fade"
    fc.append(f"{prev}[{i}:v]xfade=transition={tr}:duration={X}:offset={off:.3f}[v{i}]")
    prev = f"[v{i}]"
base = len(files)
for k, (name, a, b) in enumerate(texts):
    idx = base + k
    fc.append(f"[{idx}:v]format=rgba,fade=in:st={a:.2f}:d=0.7:alpha=1,fade=out:st={b - 0.6:.2f}:d=0.6:alpha=1[tx{k}]")
    fc.append(f"{prev}[tx{k}]overlay=0:0:shortest=1[o{k}]")
    prev = f"[o{k}]"
fc.append(f"{prev}format=yuv420p[vout]")
aidx = base + len(texts)
fc.append(f"[{aidx}:a]atrim=0:{total:.3f},afade=t=out:st={total - 2.5:.3f}:d=2.5,loudnorm=I=-15:TP=-1.5:LRA=9[aout]")

master = f"{S}/out/master.mov"; os.makedirs(f"{S}/out", exist_ok=True)
run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(fc),
     "-map", "[vout]", "-map", "[aout]", "-t", f"{total:.3f}", "-r", "30",
     "-c:v", "libx264", "-preset", "slow", "-crf", "10", "-pix_fmt", "yuv420p",
     "-c:a", "pcm_s16le", "-ar", "48000", master])
print("master done", total)
