from PIL import Image, ImageDraw, ImageFont
F="/root/.claude/plugins/synced/5b983104-35b1-44ad-9650-6be25a8f60b3_bf3cb9d3-a57e-4e68-9be6-86d008990efc/82436e8d-b5bb-4da5-b372-0309f771299f/skills/animation-studio/examples/wedding-invite/assets/fonts/"
OLIVE=(0x41,0x44,0x2E); CREAM=(0xFA,0xF6,0xEA); GOLD=(0xE7,0xC6,0x98); GOLD_DK=(0xB8,0x95,0x5E)
W,H=1080,1350; STRIP=260
canvas=Image.new("RGB",(W,H),CREAM)
# photo: resize + crop only (no colour change)
ph=Image.open("images/library/IMG_3296.jpg").convert("RGB")
s=W/ph.width; ph=ph.resize((W,round(ph.height*s)),Image.LANCZOS)
ph_h=H-STRIP; top=(ph.height-ph_h)//2
canvas.paste(ph.crop((0,top,W,top+ph_h)),(0,0))
d=ImageDraw.Draw(canvas)
d.rectangle([0,ph_h,W,ph_h+3],fill=GOLD)  # thin gold line between photo and strip
# text
h1=ImageFont.truetype(F+"Cinzel-500.ttf",58)
t2=ImageFont.truetype(F+"CormorantGaramond-600.ttf",34)
x=72; y=ph_h+52
d.text((x,y),"MODAL SILK",font=h1,fill=OLIVE)
y2=y+80
d.line([(x,y2),(x+120,y2)],fill=GOLD_DK,width=2)
d.text((x,y2+18),"A gentle sheen, a wide gold border, scattered white dots.",font=t2,fill=OLIVE)
# logo bottom-right on cream
lg=Image.open("images/tessera-logo-transparent.png").convert("RGBA")
lh=170; lg=lg.resize((round(lg.width*lh/lg.height),lh),Image.LANCZOS)
canvas.paste(lg,(W-lg.width-56,ph_h+(STRIP-lh)//2+2),lg)
canvas.save("instagram/2026-11-07-blue-modal-silk-set/post.jpg",quality=93)
print("ok")
