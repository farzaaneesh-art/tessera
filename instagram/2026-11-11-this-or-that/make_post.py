import sys; sys.path.insert(0,"instagram")
from tessera_style import *
OUT="instagram/2026-11-11-this-or-that/"
A=Image.open("images/library/IMG_3442.jpg").convert("RGB"); B=Image.open("images/library/IMG_3504.jpg").convert("RGB")
# Slide 1: split A | B
c=Image.new("RGB",(W,H),CREAM); top=250; ph=H-top-150; half=(W-12)//2
c.paste(fit(A,half,ph),(0,top)); c.paste(fit(B,half,ph),(half+12,top)); d=ImageDraw.Draw(c)
ctext(d,70,"THIS  OR  THAT?",f(CZ5,64),OLIVE); rule(d,W/2-60,160)
ctext(d,176,"Pick one. Tell us in the comments.",f(CG,36),RUST)
for x,l in [(half/2,"A"),(half+12+half/2,"B")]:
    d.ellipse([x-46,top+30,x+46,top+122],fill=CREAM); ctext(d,top+42,l,f(CZ7,58),OLIVE,cx=x)
ctext(d,H-118,"Swipe to see each one up close  →",f(CG,32),OLIVE)
logo(c,W-56-90,H-56-96+20,96)
c.save(OUT+"1-this-or-that.jpg",quality=93)
# Slides 2 and 3: each option full size
for img,l,txt,name in [(A,"A","Pink, with a rich border","2-option-a.jpg"),(B,"B","Olive green, with tassels","3-option-b.jpg")]:
    c=Image.new("RGB",(W,H),CREAM); c.paste(fit(img,W,H),(0,0)); d=ImageDraw.Draw(c)
    d.rectangle([48,48,48+150,48+150],fill=CREAM); ctext(d,68,l,f(CZ7,96),OLIVE,cx=48+75)
    d.rectangle([48,H-48-120,48+640,H-48],fill=CREAM)
    d.text((88,H-48-120+22),"OPTION "+l,font=f(CZ5,34),fill=RUST)
    d.text((88,H-48-120+66),txt,font=f(CG,34),fill=OLIVE)
    c.save(OUT+name,quality=93)
print("ok")
