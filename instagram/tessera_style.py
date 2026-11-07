"""Shared Tessera post style (colours, fonts, helpers). Photos are only resized/cropped, never recoloured."""
import glob
from PIL import Image, ImageDraw, ImageFont
_F = glob.glob("/root/.claude/plugins/**/assets/fonts/Cinzel-500.ttf", recursive=True)
FONT_DIR = _F[0].rsplit("/", 1)[0] + "/" if _F else "fonts/"
OLIVE=(0x41,0x44,0x2E); CREAM=(0xFA,0xF6,0xEA); GOLD=(0xE7,0xC6,0x98); GOLD_DK=(0xB0,0x8A,0x52); RUST=(0x9A,0x4E,0x32)
W,H=1080,1350
CZ5,CZ7,CG="Cinzel-500.ttf","Cinzel-700.ttf","CormorantGaramond-600.ttf"
LOGO=Image.open("images/tessera-logo-transparent.png").convert("RGBA")
def f(name,size): return ImageFont.truetype(FONT_DIR+name,size)
def fit(img,w,h,ax=0.5,ay=0.5):
    s=max(w/img.width,h/img.height); im=img.resize((round(img.width*s),round(img.height*s)),Image.LANCZOS)
    l=int((im.width-w)*ax); t=int((im.height-h)*ay); return im.crop((l,t,l+w,t+h))
def logo(c,x,y,h):
    lg=LOGO.resize((round(LOGO.width*h/LOGO.height),h),Image.LANCZOS); c.paste(lg,(x,y),lg)
def ctext(d,y,txt,font,fill,cx=W/2):
    w=d.textlength(txt,font=font); d.text((cx-w/2,y),txt,font=font,fill=fill)
def rule(d,x,y,w=120): d.line([(x,y),(x+w,y)],fill=GOLD_DK,width=2)
def cta(d,y,bw=760):
    bx=(W-bw)//2; d.rectangle([bx,y,bx+bw,y+92],fill=OLIVE)
    ctext(d,y+24,"DM  or  WhatsApp +971 50 525 2491",f(CZ5,32),CREAM)
def hero(photo,title,sub,hint,out,ay=0.5,ax=0.5,strip=300):
    c=Image.new("RGB",(W,H),CREAM); ph_h=H-strip
    c.paste(fit(photo,W,ph_h,ax,ay),(0,0)); d=ImageDraw.Draw(c)
    d.rectangle([0,ph_h,W,ph_h+3],fill=GOLD); y=ph_h+46
    d.text((72,y),title,font=f(CZ5,56),fill=OLIVE); rule(d,74,y+88)
    d.text((72,y+104),sub,font=f(CG,38),fill=OLIVE)
    if hint: d.text((72,y+154),hint,font=f(CG,30),fill=RUST)
    logo(c,W-56-172,ph_h+(strip-184)//2+4,184); c.save(out,quality=93)
def card_on_photo(photo,head,lines,out,ay=0.5):
    c=Image.new("RGB",(W,H),CREAM); c.paste(fit(photo,W,H,ay=ay),(0,0)); d=ImageDraw.Draw(c)
    ch=130+44*len(lines); cx,cy,cw=48,H-48-ch,700
    d.rectangle([cx,cy,cx+cw,cy+ch],fill=CREAM)
    d.text((cx+40,cy+34),head,font=f(CZ5,40),fill=OLIVE); rule(d,cx+42,cy+98)
    for i,t in enumerate(lines): d.text((cx+40,cy+116+44*i),t,font=f(CG,34),fill=OLIVE)
    c.save(out,quality=93)
