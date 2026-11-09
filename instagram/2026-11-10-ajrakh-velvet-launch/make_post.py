# Ajrakh Velvet launch carousel. Real photos from images/ajrakh-velvet/ — only resized/cropped, never recoloured or redrawn.
import sys; sys.path.insert(0,"instagram")
from tessera_style import *
OUT="instagram/2026-11-10-ajrakh-velvet-launch/"
def P(n): return Image.open(f"images/ajrakh-velvet/ajrakh_velvet_{n:02d}.jpg").convert("RGB")
# 1 cover: all three
hero(P(1),"Ajrakh Velvet","Three designs for the cooler months","Swipe to meet all three  →",OUT+"1-cover.jpg",ay=0.35)
# 2-4 each design
hero(P(2),"Design 1","Charcoal velvet with ivory medallions","2.5 metres  ·  swipe  →",OUT+"2-design-1.jpg",ay=0.6)
hero(P(5),"Design 2","Ivory velvet, indigo stripes, rust border","2.5 metres  ·  swipe  →",OUT+"3-design-2.jpg",ay=0.55)
hero(P(8),"Design 3","Red and indigo Ajrakh, all-over print","2.5 metres  ·  swipe  →",OUT+"4-design-3.jpg",ay=0.5)
# 5 details + CTA
c=Image.new("RGB",(W,H),CREAM); c.paste(fit(P(7),W,520,ay=0.25),(0,0)); d=ImageDraw.Draw(c)
d.rectangle([0,520,W,523],fill=GOLD); y=590
ctext(d,y,"THE DETAILS",f(CZ5,48),OLIVE); rule(d,W/2-60,y+76)
rows=[("Designs","3, each one different"),("Length","2.5 metres of fabric each"),("Feel","soft velvet with a rich sheen"),("Season","made for winter evenings")]
ry=y+110; lf=f(CZ7,30); vf=f(CG,38)
for k,v in rows:
    kw=d.textlength(k.upper(),font=lf); vw=d.textlength(v,font=vf); x=(W-(kw+28+vw))/2
    d.text((x,ry+6),k.upper(),font=lf,fill=RUST); d.text((x+kw+28,ry),v,font=vf,fill=OLIVE); ry+=62
cta(d,ry+40); logo(c,W-56-110,H-56-118,118)
c.save(OUT+"5-details.jpg",quality=93)
print("ok")
