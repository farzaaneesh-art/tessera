"""Assemble TESSERA Ajrakh Velvet winter reel with ffmpeg.
usage: build.py <work_dir> <uploads_dir>"""
import subprocess, sys, os

WD, UP = sys.argv[1:3]
SRC = f"{WD}/src"; SH = f"{WD}/shots"; os.makedirs(SH, exist_ok=True)
X = 0.5
FINISH = "eq=contrast=1.03:saturation=1.0,unsharp=5:5:0.35:5:5:0,vignette=angle=0.30,format=yuv420p"
FIXC = "colorbalance=gm=0.03:bm=-0.02,eq=saturation=1.12,"   # compressed clips lean magenta
FIX60 = "eq=saturation=1.04,"
INDOOR = "colorbalance=rs=-0.03:rm=-0.04:bm=0.03:bs=0.02,"   # tame warm room-light cast
HLG = "eq=contrast=1.10:gamma=0.97,"                           # 4K iPhone HLG clip, see NOTES
LOWRES = "hqdn3d=1.2:1.2:2.5:2.5,"

def vid(name, ss, ln, speed=1.0, z=(1.0, 1.04), pre=""):
    return dict(kind="v", name=name, ss=ss, ln=ln, speed=speed, z=z, pre=pre)

def img(name, dur, cropx=0.5, z=(1.0, 1.05), pan=None):
    return dict(kind="i", name=name, dur=dur, cropx=cropx, z=z, pan=pan)

shots = [
    img("ac015040-image.jpg", 4.0, 0.5, (1.00, 1.08)),                           # 0 hook: dandelion motifs, velvet pile
    img("413d7038-image.jpg", 3.2, 0.5, (1.10, 1.10), pan="down"),               # 1 dense Ajrakh field, pan down
    img("cf95fc1e-image.jpg", 3.0, 0.5, (1.06, 1.00)),                           # 2 panel meets mandala field
    img("a63ebcab-image.jpg", 3.3, 0.5, (1.00, 1.05)),                           # 3 whole layout
    vid("IMG_5838_compressed.mp4", 4.0, 3.0, 1.0, (1.00, 1.04), LOWRES + FIXC),  # 4 hanging, panel detail
    vid("IMG_5836.mov", 0.3, 2.2, 0.5, (1.00, 1.05), FIX60),                     # 5 velvet wave, true slow motion
    vid("IMG_5842_compressed.mp4", 15.0, 2.0, 1.0, (1.03, 1.00), LOWRES + FIXC), # 6 lifting drape
    img("9d7ed1e6-image.jpg", 3.5, 0.5, (1.00, 1.05)),                           # 7 styled, folded
    img("fdb8557d-image.jpg", 3.0, 0.5, (1.06, 1.00)),                           # 8 panel, hanging
    vid("IMG_5838_compressed.mp4", 6.0, 2.5, 1.0, (1.00, 1.03), LOWRES + FIXC),  # 9 return: full hanging shot
]
END_LEN = 4.5

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: print(r.stderr[-3000:]); sys.exit(1)

def zp(z0, z1, nfr, x="iw/2-(iw/zoom/2)", y="ih/2-(ih/zoom/2)"):
    return (f"zoompan=z='{z0}+({z1}-{z0})*on/{nfr}':x='{x}':y='{y}':d=1:s=1080x1920:fps=30")

durs = []
for i, s in enumerate(shots):
    out = f"{SH}/s{i}.mp4"
    if s["kind"] == "v":
        nfr = round(s["ln"] / s["speed"] * 30)
        vf = (f"setpts=(PTS-STARTPTS)/{s['speed']},fps=30,{s['pre']}"
              "scale=2160:3840:flags=lanczos,setsar=1," + zp(*s["z"], nfr) + "," + FINISH)
        run(["ffmpeg", "-v", "error", "-y", "-ss", str(s["ss"]), "-t", str(s["ln"] + 0.2),
             "-i", f"{SRC}/{s['name']}", "-vf", vf, "-frames:v", str(nfr), "-an",
             "-c:v", "libx264", "-crf", "12", "-preset", "medium", out])
    else:
        nfr = round(s["dur"] * 30)
        # crop a 9:16 window from the 3:4 photo, then move slowly inside it
        crop = f"crop=ih*9/16:ih:(iw-ih*9/16)*{s['cropx']}:0,scale=2160:3840:flags=lanczos,setsar=1,"
        if s["pan"] == "down":
            z = zp(s["z"][0], s["z"][1], nfr, y=f"(ih-ih/zoom)*on/{nfr}")
        else:
            z = zp(*s["z"], nfr)
        run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", f"{UP}/{s['name']}",
             "-vf", crop + z + "," + FINISH, "-frames:v", str(nfr),
             "-c:v", "libx264", "-crf", "12", "-preset", "medium", out])
    durs.append(nfr / 30); print("shot", i, durs[-1], flush=True)

nfr = round(END_LEN * 30)
run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", f"{WD}/text/endcard.png",
     "-vf", zp(1.0, 1.02, nfr) + ",format=yuv420p", "-frames:v", str(nfr),
     "-c:v", "libx264", "-crf", "12", f"{SH}/end.mp4"])
durs.append(nfr / 30)
files = [f"{SH}/s{i}.mp4" for i in range(len(shots))] + [f"{SH}/end.mp4"]

st = []; acc = 0
for d in durs: st.append(acc); acc += d - X
total = st[-1] + durs[-1]
print("starts", [round(v, 2) for v in st], "total", round(total, 2))

texts = [("t1", 0.4, st[1] - 0.1), ("t2", st[1] + 0.45, st[3] - 0.15),
         ("t3", st[3] + 0.45, st[5] - 0.15), ("t4", st[5] + 0.45, st[7] - 0.15),
         ("t5", st[7] + 0.45, st[9] - 0.1)]

inp = []
for f in files: inp += ["-i", f]
for n, a, b in texts: inp += ["-loop", "1", "-t", f"{total:.3f}", "-i", f"{WD}/text/{n}.png"]
inp += ["-i", f"{WD}/music.wav"]
fc = []; prev = "[0:v]"
for i in range(1, len(files)):
    fc.append(f"{prev}[{i}:v]xfade=transition=fade:duration={X}:offset={st[i]:.3f}[v{i}]"); prev = f"[v{i}]"
b0 = len(files)
for k, (n, a, b) in enumerate(texts):
    fc.append(f"[{b0+k}:v]format=rgba,fade=in:st={a:.2f}:d=0.7:alpha=1,fade=out:st={b-0.6:.2f}:d=0.6:alpha=1[t{k}]")
    fc.append(f"{prev}[t{k}]overlay=0:0:shortest=1[o{k}]"); prev = f"[o{k}]"
fc.append(f"{prev}format=yuv420p[vout]")
fc.append(f"[{b0+len(texts)}:a]atrim=0:{total:.3f},afade=t=out:st={total-2.5:.3f}:d=2.5,loudnorm=I=-15:TP=-1.5:LRA=9[aout]")
os.makedirs(f"{WD}/out", exist_ok=True)
run(["ffmpeg", "-v", "error", "-y", *inp, "-filter_complex", ";".join(fc), "-map", "[vout]", "-map", "[aout]",
     "-t", f"{total:.3f}", "-r", "30", "-c:v", "libx264", "-preset", "slow", "-crf", "10",
     "-pix_fmt", "yuv420p", "-c:a", "pcm_s16le", "-ar", "48000", f"{WD}/out/master.mov"])
print("master done", round(total, 2))
