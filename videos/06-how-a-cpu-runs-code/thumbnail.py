"""Thumbnail for video 06: a CPU core with instructions riding the clock wave + big text (sunset theme)."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "../.."))
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, K = 1280, 720, 2
# sunset theme colors (THEMES["sunset"] in render.py)
NAVY = (30, 14, 48); PANEL = (48, 24, 72); PINK = (244, 114, 182); ORANGE = (251, 146, 60)
WHITE = (253, 242, 248); GREEN = (110, 231, 183)
GF = "/usr/share/fonts/truetype/google-fonts/"
w, h = W * K, H * K
img = Image.new("RGBA", (w, h), NAVY + (255,))
bgd = ImageDraw.Draw(img)
for y in range(h):
    f = y / h
    bgd.line([(0, y), (w, y)], fill=tuple(int(NAVY[i] + (PANEL[i] - NAVY[i]) * f) for i in range(3)) + (255,))
glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
ImageDraw.Draw(glow).ellipse([w * 0.5, h * 0.05, w * 1.1, h * 0.95], fill=(120, 40, 110, 200))
img.alpha_composite(glow.filter(ImageFilter.GaussianBlur(170)))

layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
d = ImageDraw.Draw(layer)
lw = 8 * K
# chip outline with pins
cx, cy, s = 930 * K, 300 * K, 400 * K
x0, y0, x1, y1 = cx - s / 2, cy - s / 2, cx + s / 2, cy + s / 2
d.rounded_rectangle([x0, y0, x1, y1], radius=34 * K, outline=PINK + (255,), width=lw)
for i in range(1, 6):
    o = s / 6 * i
    for seg in [(x0 + o, y0, x0 + o, y0 - 40 * K), (x0 + o, y1, x0 + o, y1 + 40 * K),
                (x0, y0 + o, x0 - 40 * K, y0 + o), (x1, y0 + o, x1 + 40 * K, y0 + o)]:
        d.line(seg, fill=PINK + (255,), width=6 * K)
# pipeline lanes inside the chip: capsules stepping diagonally
cols = [PINK, ORANGE, GREEN]
for r in range(3):
    for c in range(3):
        if c > r + 1:
            continue
        bx = x0 + 40 * K + c * 112 * K
        by = y0 + 60 * K + r * 100 * K
        d.rounded_rectangle([bx, by, bx + 96 * K, by + 64 * K], radius=32 * K, outline=cols[(c - r) % 3] + (255,),
                            width=6 * K, fill=(PANEL + (255,)))
# clock wave along the bottom
yw, amp, per = 640 * K, 40 * K, 120 * K
pts = []
xs = 600 * K
while xs < w + per:
    pts += [(xs, yw + amp), (xs, yw - amp), (xs + per / 2, yw - amp), (xs + per / 2, yw + amp)]
    xs += per
d.line(pts, fill=ORANGE + (255,), width=7 * K, joint="curve")
g = layer.filter(ImageFilter.GaussianBlur(16 * K))
img.alpha_composite(g); img.alpha_composite(g); img.alpha_composite(layer)
# one highlighted tick
dd = ImageDraw.Draw(img)
dd.rounded_rectangle([840 * K, 584 * K, 900 * K, 696 * K], radius=14 * K, outline=WHITE + (255,), width=5 * K)

# text
t1 = ImageFont.truetype(GF + "Poppins-Bold.ttf", 190 * K)
t2 = ImageFont.truetype(GF + "Poppins-Bold.ttf", 150 * K)
lines = [((56, 40), "ONE", t1, WHITE), ((56, 230), "TICK", t1, WHITE), ((60, 450), "0.2 ns", t2, ORANGE)]
shadow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
sd = ImageDraw.Draw(shadow)
for (px, py), s_, f_, c_ in lines:
    sd.text((px * K + 6 * K, py * K + 8 * K), s_, font=f_, fill=(0, 0, 0, 230))
img.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(16 * K)))
dd = ImageDraw.Draw(img)
for (px, py), s_, f_, c_ in lines:
    dd.text((px * K, py * K), s_, font=f_, fill=c_)

logo = Image.open(os.path.join(ROOT, "brand/plainly-silicon-logo.png")).convert("RGBA").resize((80 * K, 80 * K))
img.alpha_composite(logo, ((W - 110) * K, 24 * K))

img.convert("RGB").resize((W, H), Image.LANCZOS).save(os.path.join(HERE, "thumbnail.jpg"), quality=92)
print("ok")
