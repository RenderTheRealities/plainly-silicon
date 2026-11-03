"""Thumbnail for video 1: exploded line-art PC parts + big two-line text."""
import math, os
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "../.."))
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, K = 1280, 720, 2
NAVY = (11, 18, 32); CYAN = (34, 211, 238); AMBER = (245, 158, 11); WHITE = (240, 242, 245)
FD = "/usr/share/fonts/opentype/inter/"
w, h = W * K, H * K
img = Image.new("RGBA", (w, h), NAVY + (255,))
bg = Image.new("RGBA", (w, h), (0, 0, 0, 0))
ImageDraw.Draw(bg).ellipse([w * 0.45, -h * 0.2, w * 1.25, h * 1.1], fill=(22, 40, 66, 255))
img.alpha_composite(bg.filter(ImageFilter.GaussianBlur(160)))

layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
d = ImageDraw.Draw(layer)
lw = 7 * K


def iso(x, y, z, ox, oy, s):
    return (ox + (x - y) * s * 0.866, oy + (x + y) * s * 0.5 - z * s)


def box(ox, oy, s, x, y, z, a, b, c, color):
    P = lambda p, q, r: iso(p, q, r, ox, oy, s)
    top = [P(x, y, z + c), P(x + a, y, z + c), P(x + a, y + b, z + c), P(x, y + b, z + c)]
    d.line(top + [top[0]], fill=color, width=lw, joint="curve")
    for (p, q) in [(x + a, y), (x + a, y + b), (x, y + b)]:
        d.line([P(p, q, z), P(p, q, z + c)], fill=color, width=lw)
    d.line([P(x + a, y, z), P(x + a, y + b, z), P(x, y + b, z)], fill=color, width=lw, joint="curve")


ox, oy, s = 900 * K, 420 * K, 34 * K
c = CYAN + (255,)
box(ox, oy, s, -5, -5, 0, 10, 10, 0.5, c)                 # motherboard
box(ox, oy, s, -1.5, -1.5, 2.4, 3, 3, 0.8, c)             # CPU floating
for i in range(2):
    box(ox, oy, s, 2.4 + i * 1.0, -4, 3.4, 0.4, 4.4, 1.6, AMBER + (255,))  # RAM
box(ox, oy, s, -4.6, 1.8, 4.6, 7, 1.4, 0.6, c)            # GPU
# dashed guides
for (a, b, z0, z1) in [(0, 0, 0.5, 2.4), (2.6, -1.8, 0.5, 3.4), (-1, 2.5, 0.5, 4.6)]:
    p0, p1 = iso(a, b, z0, ox, oy, s), iso(a, b, z1, ox, oy, s)
    for i in range(0, 10, 2):
        t0, t1 = i / 10, (i + 1) / 10
        d.line([(p0[0] + (p1[0] - p0[0]) * t0, p0[1] + (p1[1] - p0[1]) * t0),
                (p0[0] + (p1[0] - p0[0]) * t1, p0[1] + (p1[1] - p0[1]) * t1)], fill=(34, 211, 238, 140), width=4 * K)
g = layer.filter(ImageFilter.GaussianBlur(14 * K))
img.alpha_composite(g); img.alpha_composite(g); img.alpha_composite(layer)

# cursor mid double-click on the CPU
mx, my = 905 * K, 300 * K
pts = [(mx, my), (mx, my + 70 * K), (mx + 19 * K, my + 54 * K), (mx + 35 * K, my + 86 * K),
       (mx + 49 * K, my + 79 * K), (mx + 33 * K, my + 48 * K), (mx + 57 * K, my + 48 * K)]
dd = ImageDraw.Draw(img)
dd.polygon(pts, fill=WHITE + (255,), outline=NAVY + (255,), width=3 * K)
for r in (40, 64):
    dd.ellipse([mx - r * K, my - r * K, mx + r * K, my + r * K], outline=(240, 242, 245, 150), width=4 * K)

# text
t1 = ImageFont.truetype(FD + "InterDisplay-Black.otf", 150 * K)
t2 = ImageFont.truetype(FD + "InterDisplay-Black.otf", 118 * K)
shadow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
sd = ImageDraw.Draw(shadow)
sd.text((64 * K, 120 * K), "EVERY", font=t1, fill=(0, 0, 0, 220))
sd.text((64 * K, 270 * K), "PART", font=t1, fill=(0, 0, 0, 220))
sd.text((64 * K, 440 * K), "EXPLAINED", font=t2, fill=(0, 0, 0, 220))
img.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(18 * K)))
dd = ImageDraw.Draw(img)
dd.text((60 * K, 112 * K), "EVERY", font=t1, fill=WHITE)
dd.text((60 * K, 262 * K), "PART", font=t1, fill=WHITE)
dd.text((60 * K, 432 * K), "EXPLAINED", font=t2, fill=AMBER)

# small logo mark bottom-left
logo = Image.open(os.path.join(ROOT, "brand/plainly-silicon-logo.png")).convert("RGBA").resize((88 * K, 88 * K))
img.alpha_composite(logo, (60 * K, 600 * K))

img.convert("RGB").resize((W, H), Image.LANCZOS).save(os.path.join(HERE, "thumbnail.jpg"), quality=92)
print("ok")
