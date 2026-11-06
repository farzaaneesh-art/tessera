# TESSERA — "The Stories We Wear" (HyperFrames project)

40 s · 1080×1920 · 30 fps. Brand rules: `DESIGN.md`.

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
- `compositions/hook|idea|craft|desire|payoff|outro.html`: one scene each. `captions.html` holds the narration captions.
- `assets/footage/`: shots cut from the original phone clips (crop + lanczos scale + light sharpen; colour unchanged).
- `assets/vo/parts/`: one Kokoro `af_heart` file per sentence. `assets/vo/timing.json`: where each sentence sits.
- `assets/audio/voiceover.wav` (−16.5 LUFS), `music_bed.wav` (procedural, −29.5 LUFS, ducked under the voice).
- `assets/fonts/`: Cormorant Garamond + Jost (OFL).
