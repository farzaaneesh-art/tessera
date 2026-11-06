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
