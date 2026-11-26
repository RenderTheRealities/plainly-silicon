"""Crisp art for the GTA 6 PS5-vs-PC face-off thumbnails (assembled in Canva).
- num_30fps.png / num_60fps.png: GTA-VI-style number with "FPS" under it, one piece so they stay aligned.
  Hard drop shadow instead of a soft glow, so edges stay sharp at thumbnail size.
- shade_16x9.png / shade_9x16.png: transparent overlays that darken the photos where text sits
  and draw a clean seam between the PS5 half and the PC half."""
import os, sys
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.abspath(os.path.join(HERE, "../..")))
from render import BRAND_TITLE_FONT
from make_art import grad, palm

PURPLE, PINK = (46, 8, 72, 255), (255, 70, 160)

def mask(W, H, org, text, f, stroke):
    m = Image.new("L", (W, H), 0)
    ImageDraw.Draw(m).text(org, text, font=f, fill=255, stroke_width=stroke, stroke_fill=255)
    return m

def number_fps(num, out, size=900):
    f = ImageFont.truetype(BRAND_TITLE_FONT, size)
    sf = ImageFont.truetype(BRAND_TITLE_FONT, int(size * 0.30))
    d = ImageDraw.Draw(Image.new("L", (1, 1)))
    l, t, r, b = d.textbbox((0, 0), num, font=f)
    sl, st, sr, sb = d.textbbox((0, 0), "FPS", font=sf, stroke_width=int(size * 0.035))
    pad = int(size * 0.12); gap = int(size * 0.02); sh = int(size * 0.035)
    W = max(r - l, sr - sl) + 2 * pad + sh
    H = (b - t) + gap + (sb - st) + 2 * pad + sh
    org = ((W - sh - (r - l)) // 2 - l, pad - t)
    sorg = ((W - sh - (sr - sl)) // 2 - sl, pad + (b - t) + gap - st)
    outer = mask(W, H, org, num, f, int(size * 0.075))
    white = mask(W, H, org, num, f, int(size * 0.045))
    inner = mask(W, H, org, num, f, 0)
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    # hard drop shadow (sharp, offset down-right) for both the number and FPS
    shadow = Image.new("L", (W, H), 0)
    shadow.paste(outer, (sh, sh))
    fps_outer = mask(W, H, sorg, "FPS", sf, int(size * 0.035))
    sh2 = Image.new("L", (W, H), 0); sh2.paste(fps_outer, (sh, sh))
    shadow = Image.composite(Image.new("L", (W, H), 255), shadow, sh2)
    blk = Image.new("RGBA", (W, H), (0, 0, 0, 255)); blk.putalpha(shadow.point(lambda v: v * 200 // 255))
    img = Image.alpha_composite(img, blk)
    for m, c in ((outer, PURPLE), (white, (255, 255, 255, 255))):
        layer = Image.new("RGBA", (W, H), c); layer.putalpha(m); img = Image.alpha_composite(img, layer)
    fill = grad(W, H).convert("RGBA")
    pl = Image.new("RGBA", (W, H), (0, 0, 0, 0)); pd = ImageDraw.Draw(pl)
    palm(pd, W * 0.10, H * 0.78, H * 0.7, size / 900, (255, 255, 255, 46), 1.4)
    fill = Image.alpha_composite(fill, pl); fill.putalpha(inner)
    img = Image.alpha_composite(img, fill)
    # FPS: white letters, purple outline
    layer = Image.new("RGBA", (W, H), PURPLE); layer.putalpha(fps_outer); img = Image.alpha_composite(img, layer)
    layer = Image.new("RGBA", (W, H), (255, 255, 255, 255)); layer.putalpha(mask(W, H, sorg, "FPS", sf, 0))
    img = Image.alpha_composite(img, layer)
    img.save(os.path.join(HERE, out)); print(out, img.size)

def vgrad(d, box, a0, a1):
    x0, y0, x1, y1 = box
    for y in range(y0, y1):
        a = int(a0 + (a1 - a0) * (y - y0) / max(1, y1 - y0 - 1))
        d.line([(x0, y), (x1, y)], fill=(8, 2, 18, a))

def shade_16x9():
    W, H = 1280, 720
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    vgrad(d, (0, 0, W, 170), 150, 0)          # top: GTA logo + labels
    vgrad(d, (0, 300, W, H), 0, 215)          # bottom: the numbers
    d.rectangle([637, 0, 643, H], fill=(255, 255, 255, 255))        # seam
    d.rectangle([631, 0, 636, H], fill=PINK + (255,)); d.rectangle([644, 0, 649, H], fill=PINK + (255,))
    im.save(os.path.join(HERE, "shade_16x9.png")); print("shade_16x9.png")

def shade_9x16():
    W, H = 1080, 1920
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    vgrad(d, (0, 0, W, 560), 190, 40)         # top: GTA logo
    vgrad(d, (0, 560, W, 957), 40, 200)       # PS5 half, darker toward its number
    vgrad(d, (0, 963, W, 1400), 120, 60)      # PC half
    vgrad(d, (0, 1400, W, H), 60, 230)        # bottom: PC number + label
    d.rectangle([0, 957, W, 963], fill=(255, 255, 255, 255))
    d.rectangle([0, 951, W, 956], fill=PINK + (255,)); d.rectangle([0, 964, W, 969], fill=PINK + (255,))
    im.save(os.path.join(HERE, "shade_9x16.png")); print("shade_9x16.png")

if __name__ == "__main__":
    number_fps("30", "num_30fps.png")
    number_fps("60?", "num_60fps.png")
    shade_16x9(); shade_9x16()
