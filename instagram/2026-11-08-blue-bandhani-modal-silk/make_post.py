# Builds the 3-slide carousel from images/library/IMG_3296.jpg. Photo is only resized/cropped (true colours).
from PIL import Image, ImageDraw, ImageFont, ImageFilter
F="/root/.claude/plugins/synced/5b983104-35b1-44ad-9650-6be25a8f60b3_bf3cb9d3-a57e-4e68-9be6-86d008990efc/82436e8d-b5bb-4da5-b372-0309f771299f/skills/animation-studio/examples/wedding-invite/assets/fonts/"
OUT="instagram/2026-11-08-blue-bandhani-modal-silk/"
OLIVE=(0x41,0x44,0x2E); CREAM=(0xFA,0xF6,0xEA); GOLD=(0xE7,0xC6,0x98); GOLD_DK=(0xB0,0x8A,0x52); RUST=(0x9A,0x4E,0x32)
W,H=1080,1350
src=Image.open("images/library/IMG_3296.jpg").convert("RGB")
logo=Image.open("images/tessera-logo-transparent.png").convert("RGBA")
def f(n,s): return ImageFont.truetype(F+n,s)
CZ5,CZ7,CG="Cinzel-500.ttf","Cinzel-700.ttf","CormorantGaramond-600.ttf"
def fit(img,w,h):
    s=max(w/img.width,h/img.height); im=img.resize((round(img.width*s),round(img.height*s)),Image.LANCZOS)
    l=(im.width-w)//2; t=(im.height-h)//2; return im.crop((l,t,l+w,t+h))
def put_logo(c,x,y,h):
    lg=logo.resize((round(logo.width*h/logo.height),h),Image.LANCZOS); c.paste(lg,(x,y),lg); return lg.width
def ctext(d,y,txt,font,fill,W=W):
    w=d.textlength(txt,font=font); d.text(((W-w)/2,y),txt,font=font,fill=fill)
def spaced(d,x,y,txt,font,fill,sp):
    for ch in txt:
        d.text((x,y),ch,font=font,fill=fill); x+=d.textlength(ch,font=font)+sp
    return x
def spaced_w(d,txt,font,sp): return sum(d.textlength(c,font=font)+sp for c in txt)-sp

# ---------- Slide 1: hero ----------
c=Image.new("RGB",(W,H),CREAM); STRIP=300; ph_h=H-STRIP
c.paste(fit(src,W,ph_h),(0,0)); d=ImageDraw.Draw(c)
d.rectangle([0,ph_h,W,ph_h+3],fill=GOLD)
# small cream tag on photo, top-left
tag="MODAL SILK"; tf=f(CZ5,26); tw=spaced_w(d,tag,tf,4)
d.rectangle([48,48,48+tw+44,48+58],fill=CREAM); spaced(d,70,60,tag,tf,RUST,4)
y=ph_h+46
d.text((72,y),"Blue Bandhani",font=f(CZ5,62),fill=OLIVE)
d.line([(74,y+92),(194,y+92)],fill=GOLD_DK,width=2)
d.text((72,y+108),"Unstitched 3-piece set",font=f(CG,36),fill=OLIVE)
d.text((72,y+156),"Swipe to see the details  →",font=f(CG,30),fill=RUST)
put_logo(c,W-56-172,ph_h+(STRIP-184)//2+4,184)
c.save(OUT+"1-hero.jpg",quality=93)

# ---------- Slide 2: detail ----------
c=Image.new("RGB",(W,H),CREAM)
c.paste(fit(src.crop((180,60,880,935)),W,H),(0,0)); d=ImageDraw.Draw(c)
# cream card bottom-left
cx,cy,cw,ch=48,H-48-250,640,250
d.rectangle([cx,cy,cx+cw,cy+ch],fill=CREAM)
d.text((cx+40,cy+34),"Every dot, tied by hand",font=f(CZ5,40),fill=OLIVE)
d.line([(cx+42,cy+98),(cx+162,cy+98)],fill=GOLD_DK,width=2)
d.text((cx+40,cy+116),"Real bandhani on soft modal silk,",font=f(CG,34),fill=OLIVE)
d.text((cx+40,cy+160),"framed by a wide gold border.",font=f(CG,34),fill=OLIVE)
c.save(OUT+"2-detail.jpg",quality=93)

# ---------- Slide 3: the set + CTA ----------
c=Image.new("RGB",(W,H),CREAM); PH=640
c.paste(fit(src.crop((0,560,1050,1260)),W,PH),(0,0)); d=ImageDraw.Draw(c)
d.rectangle([0,PH,W,PH+3],fill=GOLD)
y=PH+56
ctext(d,y,"WHAT'S IN THE SET",f(CZ5,44),OLIVE)
d.line([(W/2-60,y+74),(W/2+60,y+74)],fill=GOLD_DK,width=2)
rows=[("Top","unstitched"),("Dupatta","wide gold border"),("Bottom","unstitched")]
ry=y+104; lf=f(CZ7,30); vf=f(CG,36)
for k,v in rows:
    kw=d.textlength(k.upper(),font=lf); vw=d.textlength(v,font=vf); total=kw+28+vw
    x=(W-total)/2; d.text((x,ry+5),k.upper(),font=lf,fill=RUST); d.text((x+kw+28,ry),v,font=vf,fill=OLIVE); ry+=60
ctext(d,ry+8,"All three pieces in modal silk.",f(CG,34),OLIVE)
# CTA button
by=ry+80; bw,bh=720,92; bx=(W-bw)//2
d.rectangle([bx,by,bx+bw,by+bh],fill=OLIVE)
ctext(d,by+24,"DM  or  WhatsApp +971 50 525 2491",f(CZ5,32),CREAM)
put_logo(c,W-56-110,H-56-118,118)
c.save(OUT+"3-the-set.jpg",quality=93)
print("ok")
