"""Cut a 1080x1920 Instagram Reel from real phone clips of a kaftan.

Usage: python3 reel/make_real_reel.py CLIP1.mov CLIP2.mov ...  ->  reel/tessera-real-reel.mp4
Clips are used in the order given. Needs Pillow and ffmpeg.
"""
import os
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "reel", "tessera-real-reel.mp4")
W, H, FPS = 1080, 1920, 30
XFADE = 0.3

SERIF = "/usr/share/fonts/truetype/crosextra/Caladea-Regular.ttf"
SERIF_I = "/usr/share/fonts/truetype/crosextra/Caladea-Italic.ttf"
SANS_M = "/usr/share/fonts/opentype/inter/Inter-Medium.otf"

INK = (52, 36, 22)  # deep brown: the clips have a light cream wall behind the text


def duration(path):
    out = subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path])
    return float(out)


def card(path, lines):
    """lines: [(text, font_path, size, y, tracking)] centred, dark ink on a soft light band."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    ys = [y for _, _, _, y, _ in lines]
    top, bottom = min(ys) - 40, max(ys) + max(s for _, _, s, _, _ in lines) + 50
    # A translucent cream band keeps text legible when it crosses the hanger or decor.
    band = Image.new("RGBA", (W, bottom - top), (250, 245, 235, 175))
    img.alpha_composite(band, (0, top))
    for text, fp, size, y, tracking in lines:
        f = ImageFont.truetype(fp, size)
        text = (" " * tracking).join(text) if tracking else text
        x = (W - d.textlength(text, font=f)) / 2
        d.text((x, y), text, font=f, fill=INK + (255,))
    img.save(path)


def main(clips):
    durs = [duration(c) for c in clips]
    offsets, t = [], 0.0
    for dur in durs[:-1]:
        t += dur - XFADE
        offsets.append(t)
    total = sum(durs) - XFADE * (len(durs) - 1)

    tmp = tempfile.mkdtemp()
    hook = os.path.join(tmp, "hook.png")
    mid = os.path.join(tmp, "mid.png")
    end = os.path.join(tmp, "end.png")
    card(hook, [("Printed with real leaves.", SERIF_I, 88, 300, 0)])
    card(mid, [("Every mark you see", SERIF_I, 72, 280, 0),
               ("was once a leaf or a flower.", SERIF_I, 72, 370, 0)])
    card(end, [("TESSERA", SERIF, 104, 250, 2),
               ("DM  “KAFTAN”  TO ORDER", SANS_M, 40, 400, 0)])

    # (png, start, end) — the hook is on screen from frame 0 so it can stop the scroll.
    texts = [(hook, 0.0, offsets[0] + 0.1),
             (mid, offsets[0] + 0.4, offsets[1] + 0.6),
             (end, total - 3.2, total)]

    cmd = ["ffmpeg", "-y", "-loglevel", "error"]
    for c in clips:
        cmd += ["-i", c]
    for png, _, _ in texts:
        cmd += ["-loop", "1", "-framerate", str(FPS), "-i", png]
    cmd += ["-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo"]

    n = len(clips)
    f = []
    for i in range(n):
        # Phone clips arrive rotated; ffmpeg auto-rotates to portrait before this chain.
        f.append(f"[{i}:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
                 f"fps={FPS},format=yuv420p,setsar=1,"
                 # gentle warm grade to sit closer to the brand's earthy palette
                 f"eq=saturation=1.08:contrast=1.03,colorbalance=rs=0.03:bs=-0.03[v{i}]")
    last = "v0"
    for i in range(1, n):
        f.append(f"[{last}][v{i}]xfade=transition=fade:duration={XFADE}:offset={offsets[i-1]:.3f}[x{i}]")
        last = f"x{i}"
    for k, (_, s, e) in enumerate(texts):
        src = n + k
        fade_in = "" if s == 0 else f"fade=in:st={s:.3f}:d=0.35:alpha=1,"
        f.append(f"[{src}:v]format=rgba,trim=duration={total:.3f},{fade_in}"
                 f"fade=out:st={e - 0.35:.3f}:d=0.35:alpha=1[t{k}]")
        f.append(f"[{last}][t{k}]overlay=0:0:enable='between(t,{s:.3f},{e:.3f})'[o{k}]")
        last = f"o{k}"

    cmd += ["-filter_complex", ";".join(f), "-map", f"[{last}]", "-map", f"{n + len(texts)}:a",
            "-t", f"{total:.3f}", "-c:v", "libx264", "-preset", "slow", "-crf", "19",
            "-pix_fmt", "yuv420p", "-profile:v", "high", "-movflags", "+faststart",
            "-c:a", "aac", "-b:a", "128k", OUT]
    subprocess.run(cmd, check=True)
    print(f"wrote {OUT} ({total:.1f}s)")


if __name__ == "__main__":
    main(sys.argv[1:])
