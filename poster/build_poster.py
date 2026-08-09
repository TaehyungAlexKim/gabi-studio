#!/usr/bin/env python3
"""Gabi Studio QR mini-poster — 6x8" @ 300dpi (1800x2400).
Site look: ivory, soft ink, dusty-blue accent, large Sempé logo.
Background: cropped piano KEYBOARD blended with an oil-paint canvas (horizontal
feather, no seam), soft blue-grey duotone, fading up into ivory under the logo.
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageOps
import segno

HERE = os.path.dirname(os.path.abspath(__file__))
A = os.path.join(HERE, "assets")
LOGO = os.path.join(HERE, "..", "assets", "logo.png")
URL = "https://www.gabistudio.ca/"
W, H = 1800, 2400

BG=(251,250,247); INK=(51,50,46); INK_SOFT=(111,109,102); MUTED=(154,151,142)
LINE=(228,224,216); ACCENT=(127,151,166); ACCENT_DP=(95,119,137); CARD=(255,255,255)
DUO_DARK=(74,92,106); DUO_LIGHT=(248,245,239)

BASK="/System/Library/Fonts/Supplemental/Baskerville.ttc"
def bask(sz, italic=False):
    idx=0
    try:
        for i in range(8):
            n=ImageFont.truetype(BASK,sz,index=i).getname()
            if italic and 'Italic' in n[1] and 'Bold' not in n[1] and 'Semi' not in n[1]: idx=i; break
            if not italic and n[1]=='Regular': idx=i; break
    except Exception: idx=0
    return ImageFont.truetype(BASK,sz,index=idx)
def sans(sz):
    for p in ["/System/Library/Fonts/Avenir Next.ttc","/System/Library/Fonts/Helvetica.ttc",
              "/System/Library/Fonts/Supplemental/Arial.ttf"]:
        if os.path.exists(p):
            try: return ImageFont.truetype(p,sz)
            except Exception: continue
    return ImageFont.load_default()

def crop_aspect(im,w,h,ox=0.5,oy=0.5):
    im=ImageOps.exif_transpose(im).convert("RGB"); iw,ih=im.size; tar=w/h; ar=iw/ih
    if ar>tar: nw=int(ih*tar); x=int((iw-nw)*ox); im=im.crop((x,0,x+nw,ih))
    else: nh=int(iw/tar); y=int((ih-nh)*oy); im=im.crop((0,y,iw,y+nh))
    return im.resize((w,h),Image.LANCZOS)
def duotone(im,dark,light):
    g=ImageOps.autocontrast(im.convert("L"),cutoff=1)
    return Image.merge("RGB",[g.point([int(dark[i]+(light[i]-dark[i])*v/255) for v in range(256)]) for i in range(3)])
def tracked(draw,cx,cy,text,font,fill,tr):
    ws=[draw.textlength(c,font=font) for c in text]; x=cx-(sum(ws)+tr*(len(text)-1))/2
    for c,w in zip(text,ws): draw.text((x,cy),c,font=font,fill=fill,anchor="lm"); x+=w+tr

img=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(img); cx=W//2

# ---- big logo (trim transparent margins first) ----
logo=Image.open(LOGO).convert("RGBA")
bb=logo.split()[3].getbbox()
if bb: logo=logo.crop(bb)
LW=1200; LH=int(logo.height*LW/logo.width)
logo=logo.resize((LW,LH),Image.LANCZOS)
logo_y=190
img.paste(logo,(cx-LW//2,logo_y),logo)

# ---- background: keyboard blended with oil canvas, duotone, fade up ----
band_top=logo_y+LH+46
band_h=H-band_top
keys=duotone(crop_aspect(Image.open(os.path.join(A,"keys_a.jpg")),W,band_h,oy=0.55),DUO_DARK,DUO_LIGHT)
oil =duotone(crop_aspect(Image.open(os.path.join(A,"palette.jpg")),W,band_h),DUO_DARK,DUO_LIGHT)
# horizontal feather: oil opacity 12% (left) -> 58% (right) — smooth, no seam
hmask=Image.new("L",(W,band_h)); hp=hmask.load()
for x in range(W):
    v=int(30+118*(x/(W-1)))
    for y in range(band_h): hp[x,y]=v
blend=Image.composite(oil,keys,hmask)
# vertical alpha fade into ivory
vmask=Image.new("L",(W,band_h)); vp=vmask.load()
for y in range(band_h):
    a=int(178*(y/(band_h-1)))
    for x in range(W): vp[x,y]=a
img.paste(blend,(0,band_top),vmask)

# ---- tagline (over faded top of band) ----
ty=band_top+64
d.text((cx,ty),"Where children's deep sensibility",font=bask(48,italic=True),fill=INK,anchor="mm")
d.text((cx,ty+60),"and boundless creativity blossom.",font=bask(48,italic=True),fill=INK,anchor="mm")
sy=ty+134
tracked(d,cx,sy,"PIANO · ART · LANGLEY, BC",sans(28),ACCENT_DP,8)
d.line([(cx-40,sy+44),(cx+40,sy+44)],fill=ACCENT,width=2)

# ---- QR card ----
qr_png=os.path.join(HERE,"_qr.png")
segno.make(URL,error="h").save(qr_png,scale=12,border=3,dark="#33322e",light="#ffffff")
qr=Image.open(qr_png).convert("RGB"); QS=qr.size[0]
pad_top,cap_h=56,150; cardw=QS+2*72; cardh=pad_top+QS+cap_h
card_x=cx-cardw//2; card_y=sy+92
d.rounded_rectangle([card_x,card_y,card_x+cardw,card_y+cardh],radius=26,fill=CARD,outline=LINE,width=2)
img.paste(qr,(cx-QS//2,card_y+pad_top))
qy=card_y+pad_top+QS+20
tracked(d,cx,qy+14,"SCAN TO EXPLORE",sans(29),ACCENT_DP,6)
d.text((cx,qy+62),"www.gabistudio.ca",font=bask(34),fill=INK,anchor="mm")

out=os.path.join(HERE,"gabi-qr-poster.png")
img.save(out,dpi=(300,300)); os.remove(qr_png)
print("saved:",out,img.size,"| logo",LW,"x",LH,"| band_top",band_top)
