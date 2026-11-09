# Editable project — Ajrakh Collection reel

The edit is code (FFmpeg + Python), not a timeline file. Change the shot list in `build.py` and re-run it.

## Files
- `build.py` — the edit: shot list (clip, in-point, length, speed, zoom, focus), crossfades, text timing, audio mix.
- `make_text.py` — renders the text overlays, end card and thumbnail.
- `make_music.py` — generates the original music (drone + flute-style line, Raag Bhairavi, E).
- `assets/text/` — the rendered overlays (`t1`–`t3`) and `endcard.png`.
- `assets/music.flac` — the music used.
- `assets/photos/` — the 3 photos used.
- `assets/fonts/` — Cinzel, Cormorant Garamond Italic and Jost, all under the SIL Open Font License.

## Shot list (final timeline, 29.2 s)
| # | Time | Source | Text |
|---|---|---|---|
| 0 | 0.0–3.6 | photo 154a875b, crop into the medallion field | Some stories never go out of style. |
| 1 | 3.1–6.1 | IMG_2574 8.5–11.5s — border + motif close | Rooted in heritage. Made for today. |
| 2 | 5.6–8.8 | photo e10e3a26, pan down | (same) |
| 3 | 8.3–11.3 | IMG_2579 0.2–3.2s — print + border band | (same) |
| 4 | 10.8–14.8 | IMG_2883 28–31s at 0.75x — fabric settling | — |
| 5 | 14.3–17.1 | IMG_2886 4.6–7.4s — worn as a drape | — |
| 6 | 16.6–19.6 | IMG_2876 3–6s — motif field + panel | Tradition, with a touch of individuality. |
| 7 | 19.1–22.5 | photo 7937e8cb — styled | (same) |
| 8 | 22.0–25.2 | photo 154a875b — both pieces | (same) |
| 9 | 24.7–29.2 | End card | TESSERA / Naturally Yours. / THE AJRAKH COLLECTION / DM to enquire. |

## Footage review (all 16 clips)
**Used:** IMG_2574, 2579, 2876, 2883, 2886.

**Not used:**
- IMG_2587, 2589, 2606 and 2610: wide styled shots of the same set-up. The sharper photo 7937e8cb replaces them.
- IMG_2607: hands folding the fabric in most frames.
- IMG_2878 and 2879: short folded shots that repeat 2876.
- IMG_2881, 2884 and 2885: flat lays and held-up shots that repeat 2876, often with hands in frame.
- IMG_2887: soft focus.

## Rebuild
```
python3 make_text.py <work> <fonts> <logo.png> assets/photos/154a875b-image.jpg
python3 make_music.py <work>/music.wav 31
python3 build.py <work> <folder with the photos>     # clips in <work>/src/
```
