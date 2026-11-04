# TESSERA — 30s Reel production pack (v2, corrected)

9:16 · 1080×1920 · 30 fps · captions burned in · works with sound off

## What changed from v1, and why

| # | v1 problem | Fix |
|---|---|---|
| 1 | Fully AI footage, including a made-up print, for a brand that sells "real, can't be repeated" | Print and garment shots come from **your product photos**. Only garden and process shots may be generated. |
| 2 | 68-word VO + "unhurried" + pauses = 31–34s | VO trimmed to **52 words**. Fits 30s at a calm pace. |
| 3 | Ingredients named while they were hidden inside a rolled bundle | Each VO line now plays over a picture that shows what it says |
| 4 | "Silver oak **ferns**" — silver oak is a tree (*Grevillea robusta*), not a fern | "Silver oak **leaves**" in VO and all prompts |
| 5 | "Modal silk" — modal is not silk | Says "**modal**". ⚠ Check the fibre content of each piece you show. If a piece is silk or chanderi, don't call it modal. |
| 6 | Silent viewers never learned the product or the call to action | VO captions burned in. End card has a call to action. |
| 7 | Generic fern opening | Opens on a fern **print** close-up (your product) in the first second |
| 8 | Two taglines on the end card | "Naturally Yours." dropped. One tagline only. |
| 9 | Text in the lower third, under the Reels UI | Captions centred on y ≈ 1290, end card around y 760–1150, all above the bottom 420px, nudged away from the right-hand buttons |

## Voiceover (final, 52 words)

> Flowers bloom. Leaves grow. And eventually, nature lets them go.
> *(half-beat)*
> What if we could keep a little of that beauty?
> Silver oak leaves, marigold and cosmos — pressed into soft modal.
> Through eco-printing, nature leaves something unexpected.
> Earthy tones. Delicate impressions. Never exactly repeated.
> *(beat)*
> Tessera. Not inspired by nature. Made by it.

Direction: warm, unhurried, close-mic, slight smile. A quiet documentary, not a luxury ad. Record with a **human voice**. A phone in a wardrobe full of clothes is a good enough booth. Hit the cue times below.

## Timing map (built into `tessera_reel_v1.mp4`)

| Time | VO / caption | Picture (v1 photo cut) | Upgrade shot (v2, once you have footage) |
|---|---|---|---|
| 0.0–1.4 | — | Fern-print close-up, mixed-design ecoprint | keep |
| 1.4–5.2 | Flowers bloom… nature lets them go. | Leaf prints, green chanderi | 1.1 Garden: silver oak + marigold + cosmos |
| 5.2–8.8 | What if we could keep a little of that beauty? | Rust kaftan print | 2.1 Hands laying leaves on fabric |
| 8.8–11.2 | Silver oak leaves, marigold and cosmos — | Green-yellow hem print | 2.1 continued (name the ingredients while they're visible) |
| 11.2–13.6 | pressed into soft modal. | Yellow marigold modal | 3.1 / 3.2 Fold + roll + bind |
| 13.6–18.2 | Through eco-printing, nature leaves something unexpected. | **Reveal:** pull back from one leaf print to the full premium ecoprint kaftan | 4.1 Unwrap (**film this for real**) |
| 18.2–20.1 | Earthy tones. | Green-yellow kaftan | keep |
| 20.1–21.9 | Delicate impressions. | Red-yellow kaftan | keep |
| 21.9–23.8 | Never exactly repeated. | Yellow kaftan | keep. Three different pieces prove the line. |
| 23.8–26.4 | *(breath)* | Mixed-design kaftan, slow push | 5.1 Fabric moving (**film this for real**) |
| 26.4–30.0 | Tessera. Not inspired by nature. Made by it. | End card: **TESSERA** / *Not inspired by nature. Made by it.* / Each piece one of a kind · Link in bio | keep |

## Prompts for upgrade shots (corrected)

Add to every prompt's **negative** field: `text, logo, watermark, plastic flowers, shiny synthetic fabric, oversaturated, neon, fashion model pose, extra fingers, smooth waxy skin, repeated identical leaves`

**Hand continuity:** generate ONE reference still of the hands first (e.g. "adult South Asian woman's hands, medium-brown skin, short unpainted nails, thin silver ring on right ring finger, rolled cream cotton sleeve"). Then use image-to-video from that still for 2.1, 3.1, 3.2 and 4.1.

- **1.1 Garden** — Macro of silver oak (Grevillea robusta) leaves — narrow, fern-like, silvery underside — beside marigold blooms and pink cosmos in a quiet Indian garden, morning light through canopy, dew, gentle breeze, shallow depth of field, 85mm feel, warm muted grade, photoreal, no text
- **2.1 Laying** — Close-up of an artisan's adult hands (use reference) placing silver oak leaves, marigold petals and cosmos flowers on cream modal fabric on a wooden table, soft window light, visible weave and leaf veins, slow deliberate movement, documentary craft film, warm earthy grade, photoreal, no text
- **3.1 Fold** — Hands (use reference) folding cream modal fabric over fresh leaves and petals, edges aligning, petals pressed between layers, workshop daylight, tactile detail, photoreal, no text
- **3.2 Roll + bind** — Hands (use reference) rolling the leaf-filled fabric into a tight bundle and binding it with natural jute twine, bamboo steamer basket in soft focus, macro textures, warm grade, photoreal, no text
- **4.1 Unwrap** — ⚠ Film this on your real fabric. Don't generate it. If you must generate a placeholder, match the colours of the finished piece shown at 13.6s.
- **5.1 Flowing fabric** — ⚠ Film this: your real piece, a fan or open window, warm daylight, 60 fps slowed to 30.

## Audio

- `music_temp.wav` / the MP4's soundtrack is a **temporary synthesised bed** (soft pad + sparse piano-like notes). It holds the timing and mood only. Replace it with a licensed acoustic track before posting. Instagram's own music library is fine for organic posts. For paid ads, use a track you hold a commercial licence for.
- Keep music about 12–15 dB under the VO.
- SFX (subtle): leaf rustle under 1.4s, cloth under 13.6s (the reveal), distant birds 0–5s.

## Claims checklist (before posting)

- [ ] Fibre named in VO matches the pieces shown (modal vs silk vs chanderi)
- [ ] Prints shown match what customers receive. If your product photos are AI-styled, reshoot the close-ups on real fabric.
- [ ] No "chemical-free", "100% natural dye", "sustainable" claims anywhere — on screen, in the caption or in hashtags
- [ ] Music licensed for the use (organic vs paid)

## Rebuild

```
python3 reel/build_reel.py <fonts_dir> <out_dir>
```
Needs Pillow, numpy, ffmpeg and Cormorant Garamond TTFs (Google Fonts, OFL). To swap in footage later, edit the `SHOTS` list.
