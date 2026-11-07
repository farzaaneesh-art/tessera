import sys; sys.path.insert(0,"instagram")
from tessera_style import *
OUT="instagram/2026-11-14-stitch-it-3-ways/"
P=Image.open("images/library/IMG_2655.jpg").convert("RGB")
hero(P,"One set. Three looks.","How to stitch your unstitched suit","Save this for your tailor  →",OUT+"1-cover.jpg")
ways=[("1","CLASSIC KURTA","Straight kurta, side slits, straight pants.","Easy for work, errands, and dinners.","Ask for: knee or calf length, 3/4 sleeves."),
      ("2","ANARKALI","Fitted top that flares from the waist.","Best for weddings, Eid, and parties.","Ask for: many panels, so it twirls."),
      ("3","CO-ORD SET","Short kurta or shirt with wide pants.","Modern and relaxed. Dupatta optional.","Ask for: a boxy cut and palazzo pants.")]
for i,(n,t,a,b,tip) in enumerate(ways):
    c=Image.new("RGB",(W,H),CREAM); d=ImageDraw.Draw(c)
    ctext(d,190,n,f(CZ5,200),GOLD_DK); ctext(d,470,t,f(CZ5,64),OLIVE); rule(d,W/2-60,566)
    ctext(d,610,a,f(CG,42),OLIVE); ctext(d,670,b,f(CG,42),OLIVE)
    bw=820; bx=(W-bw)//2; d.rectangle([bx,800,bx+bw,900],outline=GOLD_DK,width=2)
    ctext(d,828,tip,f(CG,38),RUST)
    if i==2: cta(d,1000)
    else: ctext(d,1010,"Swipe for the next look  →",f(CG,32),OLIVE)
    logo(c,W-56-110,H-56-118,118)
    c.save(OUT+f"{i+2}-way-{n}.jpg",quality=93)
print("ok")
