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
- Display: **Bodoni Moda** 400/500 (headlines, TESSERA). Script: **Great Vibes** (accent words, "Naturally Yours."). Headlines 88–118 px.
- Support: **Josefin Sans** 500/600. Captions 42 px; labels, disclosure and CTA 28–40 px.
- Max ~5 words per headline line. Captions 3–6 words per group.
- Files in `assets/fonts/` (OFL licences included).

## Motion rules
- Arrivals: blur 8 px → 0 + opacity, 0.7–1.0 s, `power3.out`. Word stagger 0.08–0.12 s.
- Exits are ~half the entrance: blur-out 0.35 s, `power2.in`.
- Landed titles stay still. Movement lives in the footage: slow push 1.00 → 1.05 per shot.
- Transitions (only three kinds):
  1. **Fabric wipe** — soft-edged vertical mask (v1 only; v2 uses dissolves so no bare ground shows).
  2. **Organic dissolve** — 0.3–0.5 s crossfade between shots.
  3. **Dip to ivory** — final product shot melts into the brand card.
- No zoom > 1.4× on 512 px-wide sources; no flashes, shakes, stickers, particles.

## Sound (v2)
- Narration: Kokoro `bf_emma` (British female) at 0.84× speed, chosen because it measured the steadiest
  pitch of five local voices. Each line is then pitch-smoothed in Praat: about 1 semitone lower and
  a 20 % narrower pitch range, so it sounds calmer and more even. Lines are placed with long pauses.
- Soft piano + pad bed at 64 BPM in D major, ducked under the voice; it comes forward only in the
  wordless styling section and resolves on one chord under the brand card.

## Product accuracy (v2)
- Real Tessera footage carries the film: hook, craft close-ups, product movement and the rack.
- Three AI-generated styling images (brown, lilac-marigold, yellow) appear only in the 14.2–20.2 s
  "Styling inspiration" section. They are shown whole, unedited, as framed plates on ivory, so they
  read as illustrations, not footage. Each carries the label "AI-generated styling visual".
- No narration or caption about real fabric or real prints plays over the AI images.
