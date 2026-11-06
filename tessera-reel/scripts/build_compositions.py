"""Writes index.html and compositions/*.html for the Tessera reel from one shot table.

Edit the tables below and re-run:  python3 scripts/build_compositions.py
(Hand edits to the generated HTML are fine too; re-running overwrites them.)
"""
import json
import os

W, H = 1080, 1920

FONT_FACES = """
@font-face { font-family: 'Cormorant Garamond'; font-weight: 400; font-style: normal; src: url('assets/fonts/cormorant-garamond-latin-400-normal.woff2') format('woff2'); }
@font-face { font-family: 'Cormorant Garamond'; font-weight: 400; font-style: italic; src: url('assets/fonts/cormorant-garamond-latin-400-italic.woff2') format('woff2'); }
@font-face { font-family: 'Cormorant Garamond'; font-weight: 500; font-style: normal; src: url('assets/fonts/cormorant-garamond-latin-500-normal.woff2') format('woff2'); }
@font-face { font-family: 'Cormorant Garamond'; font-weight: 300; font-style: italic; src: url('assets/fonts/cormorant-garamond-latin-300-italic.woff2') format('woff2'); }
@font-face { font-family: 'Jost'; font-weight: 300; font-style: normal; src: url('assets/fonts/jost-latin-300-normal.woff2') format('woff2'); }
@font-face { font-family: 'Jost'; font-weight: 400; font-style: normal; src: url('assets/fonts/jost-latin-400-normal.woff2') format('woff2'); }
@font-face { font-family: 'Jost'; font-weight: 500; font-style: normal; src: url('assets/fonts/jost-latin-500-normal.woff2') format('woff2'); }
"""

# Scenes: id, global start, duration, entry ("wipe" | "dissolve"), shots, headline blocks
# shot: (src, local start, duration)
# headline block: (id, local start, duration, top px, [ (line html, local reveal time) ... ], size)
SCENES = [
    dict(id="hook", start=0.0, dur=4.6, entry=None,
         shots=[("h1", 0.0, 2.8), ("h2", 2.6, 1.933)],
         heads=[]),  # hook text is hand-built below (centred, larger)
    dict(id="craft", start=4.3, dur=10.0, entry="dissolve",
         shots=[("s2a", 0.0, 2.65), ("s3a", 2.45, 2.65), ("s2b", 4.9, 2.65), ("s2c", 7.35, 2.65)],
         heads=[]),
    # styling (AI-generated visuals) is hand-built in styling_file(), 14.2 -> 20.2
    dict(id="beauty", start=20.0, dur=6.2, entry="dissolve",
         shots=[("s4a", 0.0, 2.4), ("s4c", 2.2, 2.4), ("s5b", 4.2, 2.0)],
         heads=[]),
]
STYLING = dict(start=14.2, dur=6.0)
OUTRO = dict(start=26.0, dur=5.6)
TOTAL = 31.6

# Caption groups: (VO id, [groups])  — times spread over the sentence by character count
CAPTIONS = [
    ("n02", ["But their beauty", "doesn’t have to."]),
    ("n03", ["In every leaf, every petal,", "nature leaves an impression."]),
    ("n04", ["Through botanical printing,", "we preserve these fleeting details", "on beautiful fabric."]),
    ("n05", ["Each impression is different."]),
    ("n06", ["Each piece tells its own story."]),
]

BASE_CSS = """
#root { position: absolute; inset: 0; overflow: hidden; }
.shot { position: absolute; inset: 0; will-change: transform, opacity; }
.shot video { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; }
.scrim-top { position: absolute; left: 0; top: 0; width: 1080px; height: 820px; z-index: 50;
  background: linear-gradient(to bottom, rgba(45,32,23,0.66) 0%, rgba(45,32,23,0.46) 45%, rgba(45,32,23,0) 100%); }
.scrim-bot { position: absolute; left: 0; top: 1000px; width: 1080px; height: 920px; z-index: 50;
  background: linear-gradient(to top, rgba(45,32,23,0.70) 0%, rgba(45,32,23,0.52) 45%, rgba(45,32,23,0) 100%); }
.hl { position: absolute; left: 90px; width: 900px; z-index: 60; text-align: center;
  font-family: 'Cormorant Garamond', serif; font-weight: 400; color: #F4EEE3; line-height: 1.08;
  letter-spacing: -0.005em; text-shadow: 0 2px 24px rgba(30,20,12,0.35); }
.hl .line { display: block; }
.hl em { font-style: italic; color: #EFE2C6; }
.rule { display: block; width: 72px; height: 1px; margin: 34px auto 0; background: #C9C3A8; }
"""


def shot_html(scene_id, idx, src, st, dur, z):
    vid = f"{scene_id}-v{idx}"
    return (f'    <div class="shot" id="{vid}-wrap" data-layout-allow-overflow style="z-index:{z}">\n'
            f'      <video id="{vid}" class="clip" src="assets/footage/{src}.mp4" data-start="{st}" '
            f'data-duration="{dur}" data-track-index="{idx}" muted playsinline></video>\n'
            f'    </div>')


def scene_file(sc):
    sid = sc["id"]
    parts, js = [], []
    for i, (src, st, dur) in enumerate(sc["shots"]):
        parts.append(shot_html(sid, i, src, st, dur, i + 1))
        w = f"#{sid}-v{i}-wrap"
        # gentle push through each shot
        js.append(f'tl.fromTo("{w}", {{scale: 1.0}}, {{scale: 1.05, duration: {dur}, ease: "none"}}, {st});')
        if i == 0:
            if sc["entry"] == "wipe":
                js.append(f'tl.fromTo("{w}", {{"--wipe": "-25%"}}, {{"--wipe": "125%", duration: 0.9, ease: "power2.inOut"}}, 0);')
            elif sc["entry"] == "dissolve":
                js.append(f'tl.fromTo("{w}", {{opacity: 0}}, {{opacity: 1, duration: 0.45, ease: "power1.inOut"}}, 0);')
        else:
            js.append(f'tl.fromTo("{w}", {{opacity: 0}}, {{opacity: 1, duration: 0.4, ease: "power1.inOut"}}, {st});')
    wipe_css = ""
    if sc["entry"] == "wipe":
        wipe_css = (f"#{sid}-v0-wrap {{ --wipe: -25%; -webkit-mask-image: linear-gradient(to top, #000 calc(var(--wipe) - 25%), transparent var(--wipe));"
                    f" mask-image: linear-gradient(to top, #000 calc(var(--wipe) - 25%), transparent var(--wipe)); }}")
    for (hid, hst, hdur, top, lines, size) in sc["heads"]:
        spans = "\n".join(f'        <span class="line" id="{hid}-l{j}">{txt}</span>' for j, (txt, _) in enumerate(lines))
        parts.append(f'    <div class="hl clip" id="{hid}" data-start="{hst}" data-duration="{hdur}" data-track-index="9" '
                     f'style="top:{top}px; font-size:{size}px">\n{spans}\n        <span class="rule" id="{hid}-rule"></span>\n    </div>')
        for j, (_, rt) in enumerate(lines):
            t0 = round(hst + rt + 0.05, 3)
            js.append(f'tl.fromTo("#{hid}-l{j}", {{opacity: 0, filter: "blur(8px)", y: 10}}, '
                      f'{{opacity: 1, filter: "blur(0px)", y: 0, duration: 0.9, ease: "power3.out"}}, {t0});')
        js.append(f'tl.fromTo("#{hid}-rule", {{scaleX: 0, opacity: 0}}, {{scaleX: 1, opacity: 0.9, duration: 0.8, ease: "power2.out"}}, {round(hst + 0.4, 3)});')
        out = round(hst + hdur - 0.4, 3)
        js.append(f'tl.to("#{hid}", {{opacity: 0, filter: "blur(6px)", duration: 0.35, ease: "power2.in"}}, {out});')
    # last shot of the payoff melts to ivory before the brand card
    if sid == "beauty":
        last = len(sc["shots"]) - 1
        js.append(f'tl.to("#{sid}-v{last}-wrap", {{opacity: 0, duration: 0.8, ease: "power1.in"}}, 5.4);')
        js.append('tl.to("#beauty-scrim-b", {opacity: 0, duration: 0.8, ease: "power1.in"}, 5.4);')
    scr = '    <div class="scrim-bot" id="%s-scrim-b"></div>' % sid
    if sid == "hook":
        scr = '    <div class="scrim-top" id="hook-scrim-t"></div>\n    <div class="scrim-bot" id="hook-scrim-b"></div>' 
    body = "\n".join(parts)
    jsb = "\n    ".join(js)
    return f"""<template>
  <style>
{FONT_FACES}
{BASE_CSS}
{wipe_css}
  </style>
  <div id="root" data-composition-id="{sid}" data-width="{W}" data-height="{H}" data-duration="{sc['dur']}">
{body}
{scr}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    {jsb}
    window.__timelines["{sid}"] = tl;
  </script>
</template>
"""


HOOK_EXTRA_CSS = """
.hook-txt { position: absolute; left: 90px; width: 900px; top: 700px; z-index: 60; text-align: center;
  font-family: 'Cormorant Garamond', serif; color: #F7F1E6; font-size: 108px; line-height: 1.04;
  text-shadow: 0 2px 30px rgba(30,20,12,0.45); }
.hook-txt .line { display: block; }
.hook-txt em { font-style: italic; }
#hook-q { top: 690px; font-size: 96px; }
.hook-vig { position: absolute; inset: 0; z-index: 50;
  background: radial-gradient(ellipse 80% 42% at 50% 47%, rgba(40,28,18,0.52) 0%, rgba(40,28,18,0.22) 60%, rgba(40,28,18,0.05) 100%); }
"""


def hook_file():
    sc = SCENES[0]
    s = scene_file(sc)
    # replace generic scrims with a centred vignette + the hook lines
    s = s.replace('    <div class="scrim-top" id="hook-scrim-t"></div>\n    <div class="scrim-bot" id="hook-scrim-b"></div>',
                  """    <div class="hook-vig" id="hook-vig"></div>
    <div class="hook-txt clip" id="hook-a" data-start="0" data-duration="1.95" data-track-index="9">
      <span class="line" id="hook-a1">Flowers fade.</span>
    </div>
    <div class="hook-txt clip" id="hook-q" data-start="1.95" data-duration="2.65" data-track-index="10">
      <span class="line" id="hook-q1">But what if</span>
      <span class="line" id="hook-q2">their beauty</span>
      <span class="line" id="hook-q3"><em>could stay?</em></span>
    </div>""")
    s = s.replace(BASE_CSS, BASE_CSS + HOOK_EXTRA_CSS)
    hook_js = """tl.to("#hook-a", {opacity: 0, filter: "blur(8px)", duration: 0.3, ease: "power2.in"}, 1.62);
    tl.fromTo("#hook-q1", {opacity: 0, filter: "blur(10px)"}, {opacity: 1, filter: "blur(0px)", duration: 0.7, ease: "power3.out"}, 2.0);
    tl.fromTo("#hook-q2", {opacity: 0, filter: "blur(10px)"}, {opacity: 1, filter: "blur(0px)", duration: 0.7, ease: "power3.out"}, 2.16);
    tl.fromTo("#hook-q3", {opacity: 0, filter: "blur(10px)"}, {opacity: 1, filter: "blur(0px)", duration: 0.8, ease: "power3.out"}, 2.36);
    tl.to("#hook-q", {opacity: 0, filter: "blur(8px)", duration: 0.3, ease: "power2.in"}, 4.25);
    window.__timelines["hook"]"""
    s = s.replace('window.__timelines["hook"]', hook_js, 1)
    return s


STYLING_IMAGES = [  # (file, local start, duration, push from, push to, y drift)
    ("ai-styling-brown.png", 0.0, 2.4, 1.0, 1.05, -10),
    ("ai-styling-lilac-marigold.png", 2.0, 2.2, 1.05, 1.0, 10),
    ("ai-styling-yellow.png", 3.8, 2.2, 1.0, 1.05, -10),
]


def styling_file():
    imgs, js = [], []
    for i, (f, st, dur, s0, s1, dy) in enumerate(STYLING_IMAGES):
        imgs.append(f'      <div class="plate-in" id="sty-w{i}" data-layout-allow-overflow style="z-index:{i + 1}">\n'
                    f'        <img id="sty-i{i}" class="clip" src="assets/styling/{f}" data-start="{st}" data-duration="{dur}" '
                    f'data-track-index="{i}" alt="AI-generated styling visual">\n      </div>')
        js.append(f'tl.fromTo("#sty-w{i}", {{scale: {s0}, y: 0}}, {{scale: {s1}, y: {dy}, duration: {dur}, ease: "none"}}, {st});')
        if i:
            js.append(f'tl.fromTo("#sty-w{i}", {{opacity: 0}}, {{opacity: 1, duration: 0.45, ease: "power1.inOut"}}, {st});')
    body = "\n".join(imgs)
    jsb = "\n    ".join(js)
    return f"""<template>
  <style>
{FONT_FACES}
#root {{ position: absolute; inset: 0; overflow: hidden; }}
.sty-ground {{ position: absolute; inset: 0; background: radial-gradient(ellipse 75% 55% at 50% 45%, #FBF7F0 0%, #EFE6D6 100%); }}
#sty-label {{ position: absolute; left: 0; width: 1080px; top: 186px; text-align: center; font-family: 'Jost', sans-serif;
  font-weight: 400; font-size: 28px; letter-spacing: 0.32em; text-transform: uppercase; color: #6E6C3F; }}
#sty-plate {{ position: absolute; left: 150px; top: 240px; width: 780px; height: 1040px; overflow: hidden;
  box-shadow: 0 18px 50px rgba(61,45,33,0.18); background: #EFE6D6; }}
.plate-in {{ position: absolute; inset: 0; }}
.plate-in img {{ position: absolute; left: 0; top: 0; width: 780px; height: 1040px; object-fit: cover; }}
#sty-note {{ position: absolute; left: 0; width: 1080px; top: 1290px; text-align: center; font-family: 'Cormorant Garamond', serif;
  font-style: italic; font-size: 32px; color: #3D2D21; }}
  </style>
  <div id="root" data-composition-id="styling" data-width="{W}" data-height="{H}" data-duration="{STYLING['dur']}">
    <div class="sty-ground" id="sty-ground"></div>
    <div id="sty-label">Styling inspiration</div>
    <div id="sty-plate" data-layout-allow-overflow>
{body}
    </div>
    <div id="sty-note">AI-generated styling visual</div>
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    tl.fromTo("#sty-ground", {{opacity: 0}}, {{opacity: 1, duration: 0.5, ease: "power1.inOut"}}, 0);
    tl.fromTo("#sty-plate", {{opacity: 0, y: 14}}, {{opacity: 1, y: 0, duration: 0.8, ease: "power3.out"}}, 0.15);
    tl.fromTo("#sty-label", {{opacity: 0}}, {{opacity: 1, duration: 0.6, ease: "power2.out"}}, 0.35);
    tl.fromTo("#sty-note", {{opacity: 0}}, {{opacity: 1, duration: 0.6, ease: "power2.out"}}, 0.35);
    {jsb}
    window.__timelines["styling"] = tl;
  </script>
</template>
"""


def outro_file():
    return f"""<template>
  <style>
{FONT_FACES}
#root {{ position: absolute; inset: 0; overflow: hidden; }}
.ground {{ position: absolute; inset: 0; background: #F4EEE3; }}
.grain {{ position: absolute; inset: 0; background: radial-gradient(ellipse 70% 55% at 50% 45%, rgba(255,252,245,0.9) 0%, rgba(231,220,200,0.55) 100%); }}
.card {{ position: absolute; left: 90px; width: 900px; top: 470px; text-align: center; color: #3D2D21; }}
#outro-brand {{ font-family: 'Cormorant Garamond', serif; font-weight: 500; font-size: 124px; letter-spacing: 0.30em;
  margin-right: -0.30em; line-height: 1; }}
#outro-brand span {{ display: inline-block; }}
#outro-tag {{ font-family: 'Cormorant Garamond', serif; font-style: italic; font-weight: 400; font-size: 60px; margin-top: 34px; color: #5A4434; }}
#outro-rule {{ width: 96px; height: 1px; background: #6E6C3F; margin: 56px auto 0; }}
#outro-craft {{ font-family: 'Jost', sans-serif; font-weight: 400; font-size: 28px; letter-spacing: 0.30em; text-transform: uppercase;
  margin-top: 52px; color: #6E6C3F; }}
#outro-disc {{ font-family: 'Cormorant Garamond', serif; font-style: italic; font-size: 46px; margin-top: 120px; color: #3D2D21; }}
#outro-ig {{ font-family: 'Jost', sans-serif; font-weight: 500; font-size: 30px; letter-spacing: 0.08em; margin-top: 30px; color: #3D2D21; }}
#outro-cta {{ font-family: 'Jost', sans-serif; font-weight: 400; font-size: 28px; letter-spacing: 0.12em; margin-top: 16px; color: #5A4434; }}
  </style>
  <div id="root" data-composition-id="outro" data-width="{W}" data-height="{H}" data-duration="{OUTRO['dur']}">
    <div class="ground" id="outro-ground"></div>
    <div class="grain" id="outro-glow"></div>
    <div class="card" id="outro-card">
      <div id="outro-brand"><span id="ob0">T</span><span id="ob1">E</span><span id="ob2">S</span><span id="ob3">S</span><span id="ob4">E</span><span id="ob5">R</span><span id="ob6">A</span></div>
      <div id="outro-tag">Naturally Yours.</div>
      <div id="outro-rule"></div>
      <div id="outro-craft">Where Nature Meets Craft</div>
      <div id="outro-disc">Discover our collection.</div>
      <div id="outro-ig">Instagram &nbsp;@weartessera</div>
      <div id="outro-cta">Enquiries via DM / WhatsApp</div>
    </div>
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    tl.fromTo("#outro-ground, #outro-glow", {{opacity: 0}}, {{opacity: 1, duration: 0.7, ease: "power1.inOut"}}, 0);
    for (let i = 0; i < 7; i++) {{
      tl.fromTo("#ob" + i, {{opacity: 0, filter: "blur(8px)"}}, {{opacity: 1, filter: "blur(0px)", duration: 0.9, ease: "power3.out"}}, 0.12 + i * 0.08);
    }}
    tl.fromTo("#outro-tag", {{opacity: 0, filter: "blur(8px)", y: 8}}, {{opacity: 1, filter: "blur(0px)", y: 0, duration: 1.0, ease: "power3.out"}}, 1.9);
    tl.fromTo("#outro-rule", {{scaleX: 0}}, {{scaleX: 1, duration: 0.9, ease: "power2.out"}}, 2.2);
    tl.fromTo("#outro-craft", {{opacity: 0}}, {{opacity: 1, duration: 0.8, ease: "power2.out"}}, 2.3);
    tl.fromTo("#outro-disc", {{opacity: 0, y: 8}}, {{opacity: 1, y: 0, duration: 0.9, ease: "power3.out"}}, 2.55);
    tl.fromTo("#outro-ig", {{opacity: 0}}, {{opacity: 1, duration: 0.8, ease: "power2.out"}}, 2.75);
    tl.fromTo("#outro-cta", {{opacity: 0}}, {{opacity: 1, duration: 0.8, ease: "power2.out"}}, 2.9);
    window.__timelines["outro"] = tl;
  </script>
</template>
"""


def captions_file():
    timing = {t["id"]: t for t in json.load(open("assets/vo2/timing.json"))}
    groups = []
    for vid, gs in CAPTIONS:
        t0, t1 = timing[vid]["start"], timing[vid]["end"]
        total = sum(len(g) for g in gs)
        acc = t0
        for g in gs:
            d = (t1 - t0) * len(g) / total
            groups.append([round(acc, 3), round(acc + d, 3), g])
            acc += d
    # each group holds until the next one starts, or 0.35 s after its sentence ends
    els, js = [], []
    for i, (s, e, g) in enumerate(groups):
        nxt = groups[i + 1][0] if i + 1 < len(groups) else 999
        nxt_st = nxt - 0.05
        end = min(nxt_st, e + 0.35) if nxt_st - e > 0.5 else nxt_st
        if e <= STYLING['start'] + 0.3:
            end = min(end, STYLING['start'] - 0.1)  # never let a fabric claim sit over the AI visuals
        st = round(s - 0.05, 3)
        dur = round(end - st, 3)
        els.append(f'    <div class="cap clip" id="cap{i}" data-start="{st}" data-duration="{dur}" data-track-index="0">'
                   f'<span class="cap-t" id="cap{i}-t">{g}</span></div>')
        js.append(f'tl.fromTo("#cap{i}-t", {{opacity: 0}}, {{opacity: 1, duration: 0.18, ease: "power1.out"}}, {st});')
        js.append(f'tl.to("#cap{i}-t", {{opacity: 0, duration: 0.12, ease: "power1.in"}}, {round(st + dur - 0.12, 3)});')
    body = "\n".join(els)
    jsb = "\n    ".join(js)
    return f"""<template>
  <style>
{FONT_FACES}
#root {{ position: absolute; inset: 0; overflow: hidden; }}
.cap {{ position: absolute; left: 0; width: 1080px; top: 1196px; text-align: center; z-index: 70; overflow: visible; }}
.cap-t {{ display: inline-block; max-width: 860px; font-family: 'Jost', sans-serif; font-weight: 400; font-size: 40px;
  line-height: 1.3; letter-spacing: 0.01em; color: #F7F1E6; text-shadow: 0 1px 14px rgba(25,16,10,0.55); }}
  </style>
  <div id="root" data-composition-id="captions" data-width="{W}" data-height="{H}" data-duration="{TOTAL}">
{body}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    {jsb}
    window.__timelines["captions"] = tl;
  </script>
</template>
"""


def index_file():
    hosts = []
    zmap = {"hook": 1, "craft": 2, "beauty": 4}
    for sc in SCENES:
        z = zmap[sc["id"]]
        hosts.append(f'      <div id="{sc["id"]}" data-composition-id="{sc["id"]}" data-composition-src="compositions/{sc["id"]}.html" '
                     f'data-start="{sc["start"]}" data-duration="{sc["dur"]}" data-track-index="{z}" data-track-kind="graphics" '
                     f'data-width="{W}" data-height="{H}" style="z-index:{z}"></div>')
    hosts.append(f'      <div id="styling" data-composition-id="styling" data-composition-src="compositions/styling.html" '
                 f'data-start="{STYLING["start"]}" data-duration="{STYLING["dur"]}" data-track-index="4" data-track-kind="graphics" '
                 f'data-width="{W}" data-height="{H}" style="z-index:3"></div>')
    hosts.append(f'      <div id="outro" data-composition-id="outro" data-composition-src="compositions/outro.html" '
                 f'data-start="{OUTRO["start"]}" data-duration="{OUTRO["dur"]}" data-track-index="6" data-track-kind="graphics" '
                 f'data-width="{W}" data-height="{H}" style="z-index:6"></div>')
    hosts.append(f'      <div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" '
                 f'data-start="0" data-duration="{TOTAL}" data-track-index="7" data-track-kind="captions" '
                 f'data-width="{W}" data-height="{H}" style="z-index:20"></div>')
    h = "\n".join(hosts)
    return f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>TESSERA — Botanical Eco-Print Collection</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: #F4EEE3; }}
      #main {{ position: relative; width: 1080px; height: 1920px; }}
      #ground {{ position: absolute; inset: 0; background: #F4EEE3; }}
    </style>
  </head>
  <body>
    <div id="main" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
      <div id="ground"></div>
{h}
      <audio id="voiceover" class="clip" src="assets/audio/voiceover.wav" data-start="0" data-duration="{TOTAL}" data-track-index="8" data-volume="1"></audio>
      <audio id="music" class="clip" src="assets/audio/music_bed.wav" data-start="0" data-duration="{TOTAL}" data-track-index="9" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""


if __name__ == "__main__":
    os.makedirs("compositions", exist_ok=True)
    open("compositions/hook.html", "w").write(hook_file())
    for sc in SCENES[1:]:
        open(f"compositions/{sc['id']}.html", "w").write(scene_file(sc))
    open("compositions/styling.html", "w").write(styling_file())
    open("compositions/outro.html", "w").write(outro_file())
    open("compositions/captions.html", "w").write(captions_file())
    open("index.html", "w").write(index_file())
    print("written")
