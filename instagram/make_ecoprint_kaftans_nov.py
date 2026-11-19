# Builds 3 ecoprint kaftan carousels (20, 22, 24 Nov 2026) from images/ecoprint-kaftans-nov/.
# Photos are only resized/cropped — never recoloured or edited.
import sys, os; sys.path.insert(0,"instagram")
from tessera_style import *
SRC="images/ecoprint-kaftans-nov/"
def P(n): return Image.open(f"{SRC}IMG_{n}.jpg").convert("RGB")
def closing(photo,band_ay,head,lines,out):
    c=Image.new("RGB",(W,H),CREAM); c.paste(fit(photo,W,560,ay=band_ay),(0,0)); d=ImageDraw.Draw(c)
    d.rectangle([0,560,W,563],fill=GOLD); y=630
    ctext(d,y,head,f(CZ5,44),OLIVE); rule(d,W/2-60,y+72)
    for i,t in enumerate(lines): ctext(d,y+104+i*54,t,f(CG,38),OLIVE)
    cta(d,y+104+len(lines)*54+40); logo(c,W-56-110,H-56-118,118); c.save(out,quality=93)
posts={
 "2026-11-20-olive-leaf-kaftan":[
   ("hero",3080,"Olive, edged in leaves.","Modal silk ecoprint kaftan, lace seam","Swipe for the details  →",0.0),
   ("card",3088,"Where green meets gold",["Smooth olive modal silk flows into","a soft panel of real leaf prints."],0.5),
   ("card",3084,"A fine lace finish",["A fine lace trim marks the line","between the two colours."],0.5),
   ("close",3089,0.35,"NO TWO ARE THE SAME",["Every leaf leaves its own mark,","so this kaftan is one of a kind."])],
 "2026-11-22-red-fern-kaftan":[
   ("hero",3076,"Red, with ferns.","Modal silk, ecoprinted velvet yoke","Swipe for the details  →",0.4),
   ("card",3077,"Ferns, pressed in",["Real fern leaves, ecoprinted onto","a velvet yoke in gold and olive."],0.35),
   ("card",3075,"Deep red modal silk",["Soft sheen and an easy drape,","made for winter evenings."],0.55),
   ("close",3071,0.45,"ONE OF A KIND",["Every fern prints its own way,","so no two yokes are ever alike."])],
 "2026-11-24-marigold-leaf-kaftan":[
   ("hero",3024,"Sunlight, in leaves.","Modal silk ecoprint kaftan","Swipe for the details  →",0.6),
   ("card",3025,"Marigold and blush",["Golden leaf prints with soft","touches of pink and lilac."],0.5),
   ("card",3022,"Easy at the neck",["A clean V-neck in deep green,","and lace where the colours meet."],0.3),
   ("close",3026,0.55,"NO TWO ARE THE SAME",["Every leaf leaves its own colour,","so this kaftan is one of a kind."])],
}
for folder,slides in posts.items():
    out=f"instagram/{folder}/"; os.makedirs(out,exist_ok=True)
    for i,s in enumerate(slides,1):
        if s[0]=="hero": _,n,t,sub,hint,ay=s; hero(P(n),t,sub,hint,f"{out}{i}-hero-v2.jpg",ay=ay)
        elif s[0]=="card": _,n,head,lines,ay=s; card_on_photo(P(n),head,lines,f"{out}{i}-detail-v2.jpg",ay=ay)
        else: _,n,ay,head,lines=s; closing(P(n),ay,head,lines,f"{out}{i}-one-of-a-kind-v2.jpg")
print("ok")
