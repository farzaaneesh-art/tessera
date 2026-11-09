# Editable project — Ajrakh Mashru Set reel

Everything needed to rebuild or change the reel. The edit is code (FFmpeg + Python), not a timeline file.

## Files
- `build.py` — the edit: shot list (clip, in-point, length, speed, zoom), colour fixes, crossfades, text timing, audio mix.
- `make_text.py` — renders the text overlays, end card and cover with Pillow.
- `make_music.py` — generates the original music (drone + santoor-style plucks, Raag Kafi).
- `assets/text/` — rendered overlays (`t1`–`t4`) and `endcard.png`.
- `assets/music.flac` — the music used.
- `assets/fonts/` — Cinzel, Cormorant Garamond Italic, Jost (all SIL Open Font License).

## Shot list (final timeline, 26.0 s)
| # | Time | Source | Text |
|---|---|---|---|
| 0 | 0.0–3.5 | IMG_2891 0.5–4.0s, slow push-in | An ode to timeless heritage. |
| 1 | 3.0–6.0 | photo bdf10091, pan down | AJRAKH · MASHRU / A story woven in tradition. |
| 2 | 5.5–8.5 | IMG_2892 8.0–11.0s | (same) |
| 3 | 8.0–11.5 | IMG_2893 1.0–4.5s — both pieces folded | Two pieces. One beautiful expression. |
| 4 | 11.0–14.5 | IMG_2895 2.5–6.0s — pan along both pieces | (same) |
| 5 | 14.0–17.5 | IMG_2892 0.5–4.0s — arched motifs | HAND BLOCK PRINTED / NATURALLY DYED |
| 6 | 17.0–20.0 | IMG_2896 32–35s — surface close-up | (same) |
| 7 | 19.5–22.5 | photo c592b88b — closing product shot | — |
| 8 | 22.0–26.0 | End card | TESSERA / Naturally Yours. / AJRAKH MASHRU / DM to enquire |

## Rebuild
1. Put the source clips in `<work>/src/` and the two photos in an uploads folder.
2. Fonts go in a fonts folder.
3. Run these commands:
   ```
   python3 make_text.py <work> <fonts> <logo.png> <cover-photo.jpg>
   python3 make_music.py <work>/music.wav 30
   python3 build.py <work> <uploads>
   ```
   The result is `<work>/out/master.mov`.
4. Export the Instagram version with the command in `../NOTES.md`.

## Not used, and why
- IMG_2890: dim and grey, with a hand and the room in frame.
- IMG_2897: 4K, but only 0.67 s long. Photo bdf10091 shows the same border sharper.
- Original clip audio: not used. Music only.
