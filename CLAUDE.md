# Tessera — Project Memory

This file is read automatically at the start of every Claude session in this repo.
It is the standing brief for all Tessera work, mainly **Instagram posts**.

## The brand (from README.md)
- Tessera sells kaftans and suit sets with **natural dyes and botanical ecoprint** (real leaves pressed into fabric).
- Voice: calm, earthy, premium. Short sensory lines. Example: "Deep rust tones drawn from earth. Grounded, rich, and quietly powerful."
- Each ecoprint piece is one-of-a-kind. That is the core selling point.

## Image sources — ALWAYS use these, never stock or AI-invented products
1. `images/CONTACT_SHEET.jpg` — look at this FIRST to find the right photo. Do not open all 59 photos.
2. `images/library/` — 59 real product photos (JPEG, max 1400px).
3. Root `*.png.png` — 10 polished catalog shots used in README (names below).

## Rules for any post
- Photos are the source of truth. Never change colours, prints, motifs, borders, tassels or garment shape.
- Do not claim a fabric (silk, modal, cotton, chanderi) or a craft (block print, bandhani, ecoprint) unless it is listed in this file as confirmed, or the user says so in the request.
- Instagram sizes: feed 1080x1350 (4:5, preferred), square 1080x1080, story/reel cover 1080x1920.
- Save finished posts in `instagram/<YYYY-MM-DD>-<topic>/` with the image(s) and a `caption.txt` (caption + hashtags).
- Commit and push finished posts so they persist (the cloud container is wiped after the session).

## Confirmed product names (catalog PNGs in repo root)
| File | Name | Confirmed details |
|---|---|---|
| black-kaftan.png.png | Black Kaftan | naturally dyed black, botanical accents |
| green-chanderi-kaftan.png.png | Green Chanderi Kaftan | chanderi silk, leaf impressions |
| green-yellow-kaftan.png.png | Green Yellow Kaftan | natural dyes, leaf prints |
| kaftan.png.png | Classic Kaftan | — |
| mixed-design-ecoprint.png.png | Mixed Design Ecoprint | real botanicals |
| premium-ecoprint.png.png | Premium Ecoprint | layered ecoprint |
| red-yellow-kaftan.png.png | Red Yellow Kaftan | — |
| rust-coloured-kaftan.png.png | Rust Coloured Kaftan | — |
| yellow-kaftan-tessera.png.png | Yellow Kaftan Tessera | botanical prints |
| yellow-marigold-modal.png.png | Yellow Marigold Modal | modal fabric |

## Photo library inventory (`images/library/`) — visual only, NAMES/FABRICS UNCONFIRMED
Built from the contact sheet. Ask the user before naming a product publicly.

**Unstitched fabric on mannequin**
- 24A3E504-...jpg — olive green with small print
- 650B9D1B-...jpg — mustard/ochre with small print

**Kaftans with gold embroidered yoke (on hanger, styled room)**
- IMG_1578 — group: maroon, black, green
- IMG_1580 — maroon
- IMG_1584 — green
- IMG_1612, IMG_1632 — green kaftan with yellow leaf-print lower panel (1632 = group shot)
- IMG_1626 — group, wide shot (small/landscape)

**Leaf-print / ecoprint kaftans (on hanger)**
- IMG_1657 — cream with large grey-green leaves
- IMG_1661 — multicolour leaf print, yellow/blue
- IMG_1674 — rust/orange
- IMG_1691 — group with magenta dip-dye (landscape)
- IMG_1692 — pale yellow
- IMG_1707 — cream/green large leaves
- IMG_1728 — yellow
- IMG_1751 — white with magenta dip-dye hem

**Flat-lay suit sets (kurta + dupatta, on white rug)**
- Indigo / navy: IMG_2150, IMG_2162, IMG_2611, IMG_2638
- Red / maroon: IMG_2168, IMG_2604, IMG_2671, IMG_2747, IMG_2767, IMG_3190, IMG_3293
- Cream with black tassels: IMG_2655, IMG_3252, IMG_3257
- Coral: IMG_2847
- Purple dotted (tie-dye look): IMG_2864, IMG_3492
- Brown with gold border: IMG_2879, IMG_3480
- Yellow/black: IMG_2885
- Pink with maroon dupatta: IMG_2910, IMG_2921, IMG_2930
- Grey/sage: IMG_3220, IMG_3222
- Magenta: IMG_3277
- Blue with gold border, dotted: IMG_3296
- Yellow solid + printed dupatta: IMG_3426
- Pink dotted: IMG_3442
- Brown/cream geometric print: IMG_3444
- Black print: IMG_3468
- Olive green dotted: IMG_3504
- Olive with maroon border: IMG_3513
- Mustard with maroon border: IMG_5374
- IMG_2776 — mirror shot of a red/blue set (lifestyle)

**Shirts / tops & dupattas on hanger**
- IMG_3311 — beige shirt, dark leaf print at hem
- IMG_3339 — green ombre dupatta with leaf print
- IMG_3350 — olive printed shirt
- IMG_3359, IMG_3377, IMG_3409 — cream shirts, small dark print
- IMG_3391 — white shirt, pink floral
- IMG_3415 — ombre to magenta dupatta

## Account & ordering (confirmed by user)
- Instagram handle: **@weartessera** (confirmed 2026-11-07 via Metricool — no dot/underscore)
- **Which tool for what (decided by user 2026-11-07):**
  - **Scheduling → Metricool** (brand "weartessera", blogId 7805847, timezone Asia/Dubai). All planned/future posts go here.
  - **Comments + quick "post now" → direct Instagram API** (Instagram API with Instagram Login, `graph.instagram.com`).
  - Never post the same content through both tools — check Metricool's schedule before a quick post to avoid duplicates.
- Direct API setup:
  - Cloud environment **"tessera"** allows `graph.instagram.com` and `graph.facebook.com`.
  - Access token is stored as a network secret on that environment (never in the repo or chat). Status: pending — user is creating the Meta app.
  - Token lasts **60 days**. Refresh before expiry (`GET https://graph.instagram.com/refresh_access_token?grant_type=ig_refresh_token`), then re-save the new token in the environment's secrets.
  - The `instagram` plugin connector (comments-only webhook) is NOT used — it needs a public webhook and does not fit cloud sessions.
- Image hosting for posting: repo is **public**, so images can be passed as
  `https://raw.githubusercontent.com/farzaaneesh-art/tessera/<branch>/<path>` (push first; Instagram needs JPEG for feed images).
- How to order: **Instagram DM** or **WhatsApp +971 50 525 2491**
- Default caption CTA: "DM us or WhatsApp +971 50 525 2491 to order."
- WhatsApp link (for stories/bio): https://wa.me/971505252491
- Market: UAE (+971 number) — write prices in AED if prices are ever shown.

## Logo & brand look (confirmed by user)
- `images/tessera-logo.jpg` — original logo on white (1536x1536).
- `images/tessera-logo-transparent.png` — cropped, white removed.
  WARNING: the face inside the scarf is white, so it also became transparent.
  Use it only on white/cream areas. On top of a photo, put it on a cream (#FAF6EA) badge or strip.
- Logo = woman's profile in a scarf made of autumn leaves + "TESSERA" in a classic serif with a gold shadow.
- Colours sampled from the logo:
  - Olive ink (text): #41442E — headlines, body text
  - Cream: #FAF6EA — backgrounds, badges
  - Gold (text shadow): #E7C698 — thin lines, accents
  - Rust: #9A4E32
  - Burnt orange: #D7824C
  - Marigold: #E2B973
  - Sage leaf green: #7A8A5A (approx.)
  - Deep brown: #4A3D2B
- Fonts: logo is a Trajan-style serif. Use **Cinzel** (free, Google Fonts) for short headlines in caps,
  and a soft serif like **Cormorant Garamond** for lines/taglines. No modern sans-serif headlines.
- Post style: cream background or full-bleed photo, olive text, thin gold rule, small logo bottom corner. Calm, lots of space.

## Open questions for the user (fill in as answered)
- Price display (yes/no)?
- Fabric and craft for library photos (block print? bandhani? ecoprint?).
