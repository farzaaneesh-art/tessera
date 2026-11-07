# 3-slide carousel from images/mixed-design-ecoprint-real.jpg (real photo, = IMG_1657). Photo only resized/cropped (true colours).
from PIL import Image, ImageDraw, ImageFont
F="/root/.claude/plugins/synced/5b983104-35b1-44ad-9650-6be25a8f60b3_bf3cb9d3-a57e-4e68-9be6-86d008990efc/82436e8d-b5bb-4da5-b372-0309f771299f/skills/animation-studio/examples/wedding-invite/assets/fonts/"
OUT="instagram/2026-11-09-mixed-design-ecoprint/"
OLIVE=(0x41,0x44,0x2E); CREAM=(0xFA,0xF6,0xEA); GOLD=(0xE7,0xC6,0x98); GOLD_DK=(0xB0,0x8A,0x52); RUST=(0x9A,0x4E,0x32); SAGE=(0x7A,0x8A,0x5A)
W,H=1080,1350
src=Image.open("images/mixed-design-ecoprint-real.jpg").convert("RGB")
logo=Image.open("images/tessera-logo-transparent.png").convert("RGBA")
def f(n,s): return ImageFont.truetype(F+n,s)
CZ5,CZ7,CG="Cinzel-500.ttf","Cinzel-700.ttf","CormorantGaramond-600.ttf"
def fit(img,w,h,ay=0.5):
    s=max(w/img.width,h/img.height); im=img.resize((round(img.width*s),round(img.height*s)),Image.LANCZOS)
    l=(im.width-w)//2; t=int((im.height-h)*ay); return im.crop((l,t,l+w,t+h))
def put_logo(c,x,y,h):
    lg=logo.resize((round(logo.width*h/logo.height),h),Image.LANCZOS); c.paste(lg,(x,y),lg)
def ctext(d,y,txt,font,fill):
    w=d.textlength(txt,font=font); d.text(((W-w)/2,y),txt,font=font,fill=fill)

# Slide 1: hero
c=Image.new("RGB",(W,H),CREAM); STRIP=300; ph_h=H-STRIP
c.paste(fit(src.crop((150,0,1470,1300)),W,ph_h,0.0),(0,0)); d=ImageDraw.Draw(c)
d.rectangle([0,ph_h,W,ph_h+3],fill=GOLD)
y=ph_h+46
d.text((72,y),"It began as a leaf.",font=f(CZ5,56),fill=OLIVE)
d.line([(74,y+88),(194,y+88)],fill=GOLD_DK,width=2)
d.text((72,y+104),"Mixed Design Ecoprint kaftan",font=f(CG,38),fill=OLIVE)
d.text((72,y+154),"Swipe to see the leaves  →",font=f(CG,30),fill=RUST)
put_logo(c,W-56-172,ph_h+(STRIP-184)//2+4,184)
c.save(OUT+"1-hero-v2.jpg",quality=93)

# Slide 2: fabric close-up
c=Image.new("RGB",(W,H),CREAM)
c.paste(fit(src.crop((560,450,1240,1300)),W,H),(0,0)); d=ImageDraw.Draw(c)
cx,cy,cw,ch=48,H-48-250,700,250
d.rectangle([cx,cy,cx+cw,cy+ch],fill=CREAM)
d.text((cx+40,cy+34),"Real leaves. Real colour.",font=f(CZ5,40),fill=OLIVE)
d.line([(cx+42,cy+98),(cx+162,cy+98)],fill=GOLD_DK,width=2)
d.text((cx+40,cy+116),"Each leaf is pressed into the fabric",font=f(CG,34),fill=OLIVE)
d.text((cx+40,cy+160),"and leaves its own print behind.",font=f(CG,34),fill=OLIVE)
c.save(OUT+"2-leaves-v2.jpg",quality=93)

# Slide 3: story + CTA (text slide)
c=Image.new("RGB",(W,H),CREAM); d=ImageDraw.Draw(c)
# small photo band at top
c.paste(fit(src.crop((460,1180,1260,1580)),W,540),(0,0)); d.rectangle([0,540,W,543],fill=GOLD)
y=618
ctext(d,y,"NO TWO ARE THE SAME",f(CZ5,46),OLIVE)
d.line([(W/2-60,y+78),(W/2+60,y+78)],fill=GOLD_DK,width=2)
lines=["Every leaf falls differently.","Every print comes out its own way.","So this kaftan is the only one",
       "exactly like it, anywhere."]
ly=y+112
for i,t in enumerate(lines):
    ctext(d,ly,t,f(CG,40),OLIVE); ly+=56
by=ly+50; bw,bh=760,92; bx=(W-bw)//2
d.rectangle([bx,by,bx+bw,by+bh],fill=OLIVE)
ctext(d,by+24,"DM  or  WhatsApp +971 50 525 2491",f(CZ5,32),CREAM)
put_logo(c,W-56-110,H-56-118,118)
c.save(OUT+"3-one-of-a-kind-v2.jpg",quality=93)
print("ok")
