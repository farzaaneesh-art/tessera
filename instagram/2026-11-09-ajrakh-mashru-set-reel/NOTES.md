# Ajrakh Mashru Top & Bottom Set — reel

Facts confirmed by user (2026-11-09): Ajrakh, mashru, hand block printed, natural dye; sold as a top & bottom set. Length/metreage not given, so none stated.

- Length 26.0 s, 1080x1920, 30 fps, H.264 High + AAC 192k, faststart.
- Colour: IMG_2891/2893/2895/2896 lifted (+10% saturation, +4% contrast) towards the daylight photos; IMG_2892 untouched.
- Music: original, synthesised (drone + santoor-style plucks, Raag Kafi, D). Different from the two winter reels on purpose. -15 LUFS.
- Shot list and rebuild steps: `project/README.md`.

Instagram export command (from the master):
```
ffmpeg -i master.mov -c:v libx264 -profile:v high -level 4.1 -preset slow -crf 19 -maxrate 8M -bufsize 16M \
  -pix_fmt yuv420p -r 30 -g 60 -c:a aac -b:a 192k -ar 48000 -movflags +faststart TESSERA_AJRAKH_MASHRU_REEL_FINAL.mp4
```
