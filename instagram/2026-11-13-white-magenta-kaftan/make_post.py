import sys; sys.path.insert(0,"instagram")
from tessera_style import *
OUT="instagram/2026-11-13-white-magenta-kaftan/"
P=Image.open("images/library/IMG_1751.jpg").convert("RGB")
hero(P.crop((0,300,760,1330)),"White, then magenta.","Premium Ecoprint kaftan","Swipe for the details  →",OUT+"1-hero-v2.jpg",ay=0.0)
card_on_photo(P.crop((110,520,560,1120)),"Every leaf, its own mark",["Real leaves, layered and pressed in,","melting into rich magenta at the hem."],OUT+"2-detail-v2.jpg")
# Slide 3: real photo note + CTA
c=Image.new("RGB",(W,H),CREAM); c.paste(fit(P.crop((60,560,620,1300)),W,560),(0,0)); d=ImageDraw.Draw(c)
d.rectangle([0,560,W,563],fill=GOLD); y=640
ctext(d,y,"WHAT YOU SEE IS WHAT YOU GET",f(CZ5,40),OLIVE); rule(d,W/2-60,y+70)
for i,t in enumerate(["This is the real kaftan,","photographed just as it is.","Every ecoprint is one of a kind."]):
    ctext(d,y+100+i*54,t,f(CG,38),OLIVE)
cta(d,y+300); logo(c,W-56-110,H-56-118,118)
c.save(OUT+"3-real-photo-v2.jpg",quality=93)
print("ok")
