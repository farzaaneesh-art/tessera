# TESSERA — "The Stories We Wear" · Design system for the reel

## Idea
Quiet luxury. The garments are the hero; type and motion behave like a well-made label —
present, calm, never loud. Nothing on screen should look like an ad template.

## Canvas
- 1080 × 1920, 30 fps, 40 s.
- Instagram safe band: all words between y = 168 and y = 1330, x = 90–990.
  Nothing readable sits under the right-hand action rail (x > 960) or below 1330 px.

## Colour tokens
| Token | Hex | Use |
|---|---|---|
| `--ivory` | `#F4EEE3` | Type on footage, outro ground |
| `--beige` | `#E7DCC8` | Secondary type, accent word on footage |
| `--sage` | `#A9B29C` | Hairlines on footage |
| `--olive` | `#6E6C3F` | Outro hairline + small caps |
| `--terracotta` | `#B0654A` | Reserved accent (one word max per scene) |
| `--brown` | `#3D2D21` | Outro ink, scrims (as rgba) |

Footage is never re-coloured. The only thing laid over it is a warm-brown gradient scrim
(max 55 % opacity) behind type, so product colours stay true.

## Type
- Display: **Cormorant Garamond** 400 / 500, italic for the emotional word. Headlines 84–104 px.
- Support: **Jost** 300 / 400. Captions 40 px, small caps / labels 22–26 px tracked 0.28–0.34 em.
- Max ~5 words per headline line. Captions 3–6 words per group.
- Files in `assets/fonts/` (OFL licences included).

## Motion rules
- Arrivals: blur 8 px → 0 + opacity, 0.7–1.0 s, `power3.out`. Word stagger 0.08–0.12 s.
- Exits are ~half the entrance: blur-out 0.35 s, `power2.in`.
- Landed titles stay still. Movement lives in the footage: slow push 1.00 → 1.05 per shot.
- Transitions (only three kinds):
  1. **Fabric wipe** — soft-edged vertical mask rising like cloth being lifted (scene 1→2, 4→5).
  2. **Organic dissolve** — 0.3–0.5 s crossfade between shots.
  3. **Dip to ivory** — final product shot melts into the brand card.
- No zoom > 1.4× on 512 px-wide sources; no flashes, shakes, stickers, particles.

## Sound
- Warm female narration (Kokoro `af_heart`, 0.9× speed), placed sentence by sentence with
  natural pauses. Narration is the clock: headlines land on the words that say them.
- Soft piano + pad bed at 70 BPM in D major, ducked ~5 dB under the voice, building
  from pad only → single notes → gentle eighth notes in the desire section → one resolving chord.

## Product accuracy
Every frame of garment is original Tessera footage: cropped, scaled (lanczos) and lightly
sharpened only. No generated garments, no recolouring, no redrawn prints. AI-generated
model images supplied with the brief are **not** used in this film.
