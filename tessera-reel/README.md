# TESSERA — Botanical Eco-Print reel (HyperFrames project)

v2: 31.6 s · 1080×1920 · 30 fps. Scenes: hook → craft (real close-ups) → styling (AI visuals, labelled) → beauty (real movement) → outro. Brand rules: `DESIGN.md`.

## Rebuild
```bash
python3 scripts/build_audio.py          # voiceover + music bed (needs: pip install kokoro-onnx soundfile; voice parts in assets/vo/parts)
python3 scripts/build_compositions.py   # writes index.html + compositions/*.html from the shot/caption tables
npx hyperframes check
npx hyperframes preview                 # live Studio preview
npx hyperframes render --output TESSERA_Ecoprint_Reel.mp4 --fps 30 --quality high
```
Note: re-running `build_compositions.py` overwrites hand edits to the HTML.

## Layout
- `compositions/hook|craft|styling|beauty|outro.html`: one scene each. `captions.html` holds the narration captions.
- `assets/footage/`: shots cut from the original phone clips (crop + lanczos scale + light sharpen; colour unchanged).
- `assets/vo2/raw/`: Kokoro `bf_emma` lines. `assets/vo2/parts/`: the same lines pitch-smoothed (used). `assets/vo2/timing.json`: placement.
- `assets/styling/`: the three AI-generated styling images (unaltered).
- `assets/vo/`: v1 narration, kept for reference.
- `assets/audio/voiceover.wav` (−16.5 LUFS), `music_bed.wav` (procedural, about −27 LUFS, ducked under the voice).
- `assets/fonts/`: Cormorant Garamond + Jost (OFL).

## v3 (final) notes
- AI styling images fill the frame (1080 × 1440, full width) over a blurred extension of the same image, with
  "AI-generated styling visual" at the top. Images themselves are unaltered.
- Footage re-cut from the original uploads at near-lossless quality (CRF 10). The 1440×1920 macro clips and the
  1080×1920 rack clip are used 1:1 with no scaling. The five hanger clips only exist as 512×910 uploads; they are
  scaled once (lanczos) with at most 1.12× zoom and very light sharpening.
- Render: `npx hyperframes render --fps 30 --quality high --crf 14 --video-frame-format png`, then `-c copy` faststart remux.
