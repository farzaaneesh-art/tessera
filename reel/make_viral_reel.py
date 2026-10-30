"""Short, loopable cut built for watch-through and replays.

Usage: python3 reel/make_viral_reel.py IMG_1715.mov IMG_1716.mov  ->  reel/tessera-viral-reel.mp4

Edit choices:
- Text is on screen from frame 0 and opens a question the video answers.
- Hard cuts every ~1.2s, mostly tight detail shots of the prints.
- The last shot ends on the exact frame the first shot starts on, so the loop is invisible.
- No end card: end cards tell people the video is over. The CTA lives in the caption.
- Clips 1712/1713 are left out: the mirror in them shows a tripod and a cluttered room.
"""
import os
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "reel", "tessera-viral-reel.mp4")
W, H, FPS = 1080, 1920, 30
BOLD = "/usr/share/fonts/opentype/inter/Inter-Bold.otf"
LOOP_POINT = 0.8  # seconds into the 1716 clip where the video starts and ends


def pill(path, lines, y=360, size=78):
    """Black text on white rounded boxes, centred. y sits inside the 4:5 feed crop."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    f = ImageFont.truetype(BOLD, size)
    pad_x, pad_y, gap = 34, 18, 10
    for text in lines:
        l, t, r, b = d.textbbox((0, 0), text, font=f)
        tw, th = r - l, b - t
        x = (W - tw) / 2
        d.rounded_rectangle((x - pad_x, y, x + tw + pad_x, y + th + 2 * pad_y), 22, fill=(255, 255, 255, 245))
        d.text((x - l, y + pad_y - t), text, font=f, fill=(20, 20, 20, 255))
        y += th + 2 * pad_y + gap
    img.save(path)


def main(clip_1715, clip_1716):
    # (source, start, end, crop as (w, h, x, y) in 1080x1920 portrait pixels or None, caption lines)
    shots = [
        (clip_1716, LOOP_POINT, 2.33, None, ["Nobody painted this."]),
        (clip_1715, 0.3, 1.5, (600, 1067, 340, 90), ["No brush. No stamp."]),
        (clip_1715, 1.5, 2.6, (490, 871, 355, 515), ["Every mark is", "a real leaf"]),
        (clip_1715, 2.6, 3.8, (600, 1067, 220, 853), ["pressed into", "the fabric."]),
        (clip_1716, 0.0, LOOP_POINT, None, ["Real leaves.", "Real fabric."]),
    ]

    tmp = tempfile.mkdtemp()
    cmd = ["ffmpeg", "-y", "-loglevel", "error"]
    for src, s, e, _, _ in shots:
        cmd += ["-ss", f"{s}", "-t", f"{e - s:.3f}", "-i", src]
    for k, (_, _, _, _, lines) in enumerate(shots):
        p = os.path.join(tmp, f"t{k}.png")
        pill(p, lines)
        cmd += ["-loop", "1", "-framerate", str(FPS), "-i", p]
    cmd += ["-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo"]

    n = len(shots)
    f = []
    for i, (_, _, _, crop, _) in enumerate(shots):
        c = f"crop={crop[0]}:{crop[1]}:{crop[2]}:{crop[3]}," if crop else ""
        f.append(f"[{i}:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},{c}"
                 f"scale={W}:{H}:flags=lanczos,fps={FPS},setsar=1,format=yuv420p,setpts=PTS-STARTPTS,"
                 f"eq=saturation=1.1:contrast=1.04,colorbalance=rs=0.03:bs=-0.03,unsharp=5:5:0.6[s{i}]")
        f.append(f"[s{i}][{n + i}:v]overlay=0:0:shortest=1[v{i}]")
    f.append("".join(f"[v{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0[out]")
    total = sum(e - s for _, s, e, _, _ in shots)

    cmd += ["-filter_complex", ";".join(f), "-map", "[out]", "-map", f"{2 * n}:a",
            "-t", f"{total:.3f}", "-c:v", "libx264", "-preset", "slow", "-crf", "18",
            "-pix_fmt", "yuv420p", "-profile:v", "high", "-movflags", "+faststart",
            "-c:a", "aac", "-b:a", "128k", OUT]
    subprocess.run(cmd, check=True)
    print(f"wrote {OUT} ({total:.1f}s)")


if __name__ == "__main__":
    main(*sys.argv[1:3])
