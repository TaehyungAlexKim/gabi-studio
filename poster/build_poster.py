#!/usr/bin/env python3
"""Gabi Studio QR mini-poster — 6x8" @ 300dpi (1800x2400).
Matches the site look: ivory, soft ink, dusty-blue accent, Sempé logo.
Background: CC0 grand piano + oil-paint canvas, rendered as a soft blue-grey
duotone band fading up into ivory. QR sits on a clean card above the band.
"""
import os, glob
from PIL import Image, ImageDraw, ImageFont, ImageOps
import segno

HERE = os.path.dirname(os.path.abspath(__file__))
A = os.path.join(HERE, "assets")
LOGO = os.path.join(HERE, "..", "assets", "logo.png")
URL = "https://www.gabistudio.ca/"
W, H = 1800, 2400

# palette (from the site)
BG        = (251, 250, 247)
INK       = (51, 50, 46)
INK_SOFT  = (111, 109, 102)
MUTED     = (154, 151, 142)
LINE      = (228, 224, 216)
ACCENT    = (127, 151, 166)
ACCENT_DP = (95, 119, 137)
CARD      = (255, 255, 255)
DUO_DARK  = (74, 92, 106)     # muted blue-grey (echoes accent)
DUO_LIGHT = (247, 244, 237)

# fonts (macOS)
BASK = "/System/Library/Fonts/Supplemental/Baskerville.ttc"
def bask(sz, italic=False):
    idx = 0
    try:
        for i in range(8):
            n = ImageFont.truetype(BASK, sz, index=i).getname()
            if italic and 'Italic' in n[1] and 'Semi' not in n[1] and 'Bold' not in n[1]:
                idx = i; break
            if not italic and n[1] == 'Regular':
                idx = i; break
    except Exception:
        idx = 0
    return ImageFont.truetype(BASK, sz, index=idx)
SANS_CANDS = ["/System/Library/Fonts/Avenir Next.ttc",
              "/System/Library/Fonts/Helvetica.ttc",
              "/System/Library/Fonts/Supplemental/Arial.ttf"]
def sans(sz):
    for p in SANS_CANDS:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, sz)
            except Exception: continue
    return ImageFont.load_default()

# helpers
def crop_aspect(im, w, h, ox=0.5, oy=0.5):
    im = ImageOps.exif_transpose(im).convert("RGB")
    iw, ih = im.size; tar = w/h; ar = iw/ih
    if ar > tar:
        nw = int(ih*tar); x = int((iw-nw)*ox); im = im.crop((x,0,x+nw,ih))
    else:
        nh = int(iw/tar); y = int((ih-nh)*oy); im = im.crop((0,y,iw,y+nh))
    return im.resize((w,h), Image.LANCZOS)

def duotone(im, dark, light):
    g = ImageOps.autocontrast(im.convert("L"), cutoff=1)
    ch = [g.point([int(dark[i]+(light[i]-dark[i])*v/255) for v in range(256)]) for i in range(3)]
    return Image.merge("RGB", ch)

def tracked(draw, cx, cy, text, font, fill, tracking, anchor_mid=True):
    ws = [draw.textlength(c, font=font) for c in text]
    total = sum(ws) + tracking*(len(text)-1)
    x = cx - total/2 if anchor_mid else cx
    for c, w in zip(text, ws):
        draw.text((x, cy), c, font=font, fill=fill, anchor="lm"); x += w + tracking

# ---- canvas ----
img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)
cx = W//2

# ---- background band: piano | oil-paint canvas, duotone, faded up ----
band_h = 660
piano = crop_aspect(Image.open(os.path.join(A, "piano_a.jpg")), 900, band_h, ox=0.5, oy=0.42)
canv  = crop_aspect(Image.open(os.path.join(A, "palette.jpg")), 900, band_h, ox=0.5, oy=0.5)
band = Image.new("RGB", (W, band_h))
band.paste(piano, (0,0)); band.paste(canv, (900,0))
band = duotone(band, DUO_DARK, DUO_LIGHT)
# vertical alpha: transparent at top -> soft at bottom
mask = Image.new("L", (W, band_h))
mp = mask.load()
for y in range(band_h):
    a = int(120 * (y/(band_h-1)))      # 0 -> ~47%
    for x in range(W): mp[x,y] = a
img.paste(band, (0, H-band_h), mask)

# ---- logo ----
logo = Image.open(LOGO).convert("RGBA")
lw = 820; lh = int(logo.height * lw/logo.width)
logo = logo.resize((lw, lh), Image.LANCZOS)
img.paste(logo, (cx - lw//2, 96), logo)

# ---- tagline (serif) ----
ty = 96 + lh + 12
d.text((cx, ty), "Where children's deep sensibility", font=bask(46, italic=True), fill=INK_SOFT, anchor="mm")
d.text((cx, ty+58), "and boundless creativity blossom.", font=bask(46, italic=True), fill=INK_SOFT, anchor="mm")

# ---- subtitle caps ----
sy = ty + 130
tracked(d, cx, sy, "PIANO · ART · LANGLEY, BC", sans(27), ACCENT_DP, 8)
# thin accent line
d.line([(cx-40, sy+42), (cx+40, sy+42)], fill=ACCENT, width=2)

# ---- QR card ----
qr_png = os.path.join(HERE, "_qr.png")
segno.make(URL, error="h").save(qr_png, scale=10, border=3, dark="#33322e", light="#ffffff")
qr = Image.open(qr_png).convert("RGB")
QS = qr.size[0]
pad_top, cap_h = 56, 150
cardw = QS + 2*70
cardh = pad_top + QS + cap_h
card_x = cx - cardw//2
card_y = sy + 96
d.rounded_rectangle([card_x, card_y, card_x+cardw, card_y+cardh], radius=26,
                    fill=CARD, outline=LINE, width=2)
img.paste(qr, (cx - QS//2, card_y + pad_top))
qy = card_y + pad_top + QS + 20
tracked(d, cx, qy+14, "SCAN TO EXPLORE", sans(29), ACCENT_DP, 6)
d.text((cx, qy+62), "www.gabistudio.ca", font=bask(34), fill=INK, anchor="mm")

out = os.path.join(HERE, "gabi-qr-poster.png")
img.save(out, dpi=(300,300))
os.remove(qr_png)
print("saved:", out, img.size)
