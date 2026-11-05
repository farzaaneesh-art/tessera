# Tessera reel — caption and posting notes

**Video:** `tessera-reel.mp4` (1080×1920, 30fps, 17.9s, H.264). The audio track is silent on purpose: add a trending sound inside the Instagram app before you post.

**Cover frame:** the opening frame ("Dyed by leaves.") works as the cover.

## Caption

Dyed by leaves. Not machines. 🍃

Every Tessera kaftan is ecoprinted with real botanicals: leaves pressed into silk, chanderi and modal, then steamed until their colour stays. No two pieces turn out the same.

Which one is yours? Tell us the number 👇

01 Green Chanderi · 02 Black · 03 Yellow Marigold Modal · 04 Rust · 05 Green Yellow · 06 Premium Ecoprint · 07 Red Yellow · 08 Mixed Design · 09 Yellow Tessera · 10 Classic

DM "KAFTAN" to order.

#ecoprint #naturaldye #botanicalprint #kaftan #slowfashion #handmadeinindia #chanderisilk #sustainablefashion #kaftandress #ecoprinting

---

# Real-footage reel — `tessera-real-reel.mp4`

10.5s, 1080×1920, cut from 4 phone clips (IMG_1712, 1713, 1715, 1716). Original audio dropped (room noise only), so add a sound in the app. The raw clips are not in the repo; rebuild with:

`python3 reel/make_real_reel.py IMG_1716.mov IMG_1713.mov IMG_1712.mov IMG_1715.mov`

## Caption

This is what real leaves leave behind. 🍃

The yellow, the purple, the little orange blooms: none of it was painted on. Each mark was pressed into the cloth straight from a leaf or a flower.

One piece. One print. DM "KAFTAN" to order.

#ecoprint #naturaldye #botanicalprint #kaftan #slowfashion #ecoprinting #sustainablefashion #kaftandress

---

# Viral cut — `tessera-viral-reel.mp4`

5.8s, loops seamlessly (last frame = first frame). Built from IMG_1715 + IMG_1716 only. Rebuild:

`python3 reel/make_viral_reel.py IMG_1715.mov IMG_1716.mov`

## Caption (keep it short — the video does the work)

Guess how many leaves are on this one 🍃👇

## Pinned comment (post it yourself, then pin)

Every print is a real leaf or flower pressed into the fabric. One piece only. DM "KAFTAN" to order.

## Posting checklist

- Add a trending sound in the app (volume low). A silent reel gets pushed less.
- Cover: frame 1 ("Nobody painted this."). Check it in the 4:5 grid preview.
- Post when your followers are most active (Insights → Total followers → Most active times).
- Reply to every comment in the first hour; reply with a question to keep threads going.
- Share to your Story with a poll sticker ("Would you wear this? Yes / Obviously").
- Hashtags (3–5 max): #ecoprint #naturaldye #botanicalprint #slowfashion #kaftan

---

# Drape reel — `tessera-drape-reel.mp4` (HyperFrames)

13.3s, 1080×1920. "1 dupatta, 3 ways": hook → 01 The wrap → 02 The cape → swirl → 03 Open & easy → comment prompt.
Built with HyperFrames in `hf-drape/` (edit text in `hf-drape/compositions/s*.html`, then `npx hyperframes render`).
The cut clips in `hf-drape/assets/` are not committed. Rebuild them from the WhatsApp videos with
`ffmpeg -ss START -to END -i SRC -an -vf "crop=…,scale=1080:1920" …` using these ranges:
s1 12.38.37 13.6–15.2 · s2 12.38.26 0.0–2.6 · s3 12.36.42 3.5–6.0 · s4 12.37.03 5.6–7.0 · s5 12.38.37 21.0–23.6 · s6 12.37.03 23.0–25.6

## Caption

1, 2 or 3? Tell us below 👇

One dupatta, three moods. Save this for your next "what do I wear" moment.

DM "DUPATTA" to order.

#dupattastyling #dupattadraping #kaftan #ethnicwear #howtostyle #slowfashion #blockprint

## Notes

- Save-and-comment bait is the whole point of this format: reply to every "1/2/3" comment.
- Add a trending sound in the app. Pick one with a clear beat and line the cuts up if you can.

---

# Flip reel — `tessera-flip-reel.mp4` (HyperFrames)

7.2s, 1080×1920, loops (last shot runs straight into the first). Cut from `Tessera_One_Reel.mov` (the sharpest source; frames after 2.5s, past its burned-in text).
Project: `hf-flip/`. Source ranges: f1 3.60–5.00 · f2 9.0–10.2 (crop 490×871+335+565) · f3 5.40–6.60 · f4 6.60–7.90 · f5 10.2–11.2 (crop 540×960+170+760) · f6 2.55–3.60.

## Caption

Every leaf on this is real 🍃 Would you wear it? Yes or no below 👇

## Pinned comment

Ecoprinted: real leaves and flowers pressed into the fabric and steamed until the colour stays. One piece. DM "KAFTAN" to order.

#ecoprint #naturaldye #botanicalprint #kaftan #slowfashion
