"""Thumbnail for video 07: line-art cart with a price tag whose 'was' price is slashed, retro palette."""
import math, os
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "../.."))
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, K = 1280, 720, 2
NAVY = (40, 28, 22); PANEL = (58, 42, 32); GOLD = (250, 180, 60); AMBER = (232, 93, 60)
WHITE = (250, 236, 214); RED = (232, 70, 60)
GF = "/usr/share/fonts/truetype/google-fonts/"
w, h = W * K, H * K
img = Image.new("RGBA", (w, h), NAVY + (255,))
bg = Image.new("RGBA", (w, h), (0, 0, 0, 0))
bd = ImageDraw.Draw(bg)
for k in range(-h, w, 48 * K):
    bd.line([(k, 0), (k + h, h)], fill=(70, 52, 40, 160), width=2 * K)
img.alpha_composite(bg)
glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
ImageDraw.Draw(glow).ellipse([w * 0.5, -h * 0.1, w * 1.15, h * 1.1], fill=(90, 60, 36, 255))
img.alpha_composite(glow.filter(ImageFilter.GaussianBlur(150)))

layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
d = ImageDraw.Draw(layer)
lw = 10 * K
# cart
cx, cy, s = 960 * K, 470 * K, 190 * K
P = lambda u, v: (cx + u * s, cy + v * s)
d.line([P(-1.35, -0.85), P(-1.05, -0.85), P(-0.8, 0.35), P(0.95, 0.35)], fill=GOLD, width=lw, joint="curve")
d.line([P(-0.97, -0.55), P(1.15, -0.55), P(0.95, 0.15), P(-0.84, 0.15), P(-0.97, -0.55)], fill=GOLD, width=lw, joint="curve")
for k in range(1, 5):
    u = -0.97 + k * 0.42
    d.line([P(u, -0.55), P(u - 0.04, 0.15)], fill=GOLD + (150,), width=5 * K)
for u in (-0.6, 0.75):
    x0, y0 = P(u, 0.6)
    r = s * 0.12
    d.ellipse([x0 - r, y0 - r, x0 + r, y0 + r], outline=GOLD, width=lw)
img.alpha_composite(layer.filter(ImageFilter.GaussianBlur(10 * K)))
img.alpha_composite(layer)

# price tag hanging over the cart, tilted
tagl = Image.new("RGBA", (520 * K, 260 * K), (0, 0, 0, 0))
td = ImageDraw.Draw(tagl)
tw_, th_ = 500 * K, 240 * K
n = th_ * 0.45
td.polygon([(n + 10 * K, 10 * K), (tw_, 10 * K), (tw_, th_), (n + 10 * K, th_), (10 * K, th_ / 2 + 5 * K)],
           fill=WHITE + (255,), outline=AMBER + (255,))
td.ellipse([n * 0.7 - 14 * K, th_ / 2 - 9 * K, n * 0.7 + 14 * K, th_ / 2 + 19 * K], fill=NAVY + (255,))
fp = ImageFont.truetype(GF + "Poppins-Bold.ttf", 80 * K)
fs = ImageFont.truetype(GF + "Poppins-Bold.ttf", 58 * K)
td.text((330 * K, 80 * K), "$399", font=fs, fill=(140, 120, 100, 255), anchor="mm")
td.line([(245 * K, 92 * K), (415 * K, 68 * K)], fill=RED + (255,), width=9 * K)
td.text((330 * K, 170 * K), "$279", font=fp, fill=NAVY + (255,), anchor="mm")
tagl = tagl.rotate(10, expand=True, resample=Image.BICUBIC)
img.alpha_composite(tagl, (690 * K, 70 * K))
# string
ImageDraw.Draw(img).line([(760 * K, 40 * K), (775 * K, 205 * K)], fill=WHITE + (200,), width=3 * K)

# text
t1 = ImageFont.truetype(GF + "Poppins-Bold.ttf", 190 * K)
t2 = ImageFont.truetype(GF + "Poppins-Bold.ttf", 150 * K)
shadow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
sd = ImageDraw.Draw(shadow)
sd.text((66 * K, 70 * K), "FAKE", font=t1, fill=(0, 0, 0, 230))
sd.text((66 * K, 300 * K), "DEALS", font=t2, fill=(0, 0, 0, 230))
img.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(16 * K)))
dd = ImageDraw.Draw(img)
dd.text((58 * K, 62 * K), "FAKE", font=t1, fill=WHITE)
dd.text((58 * K, 292 * K), "DEALS", font=t2, fill=AMBER)
dd.rounded_rectangle([62 * K, 520 * K, 520 * K, 600 * K], radius=40 * K, fill=GOLD)
dd.text((291 * K, 562 * K), "7 PC PART TRAPS", font=ImageFont.truetype(GF + "Poppins-Bold.ttf", 44 * K), fill=NAVY, anchor="mm")
logo = Image.open(os.path.join(ROOT, "brand/plainly-silicon-logo.png")).convert("RGBA").resize((80 * K, 80 * K))
img.alpha_composite(logo, (1170 * K, 620 * K))
img.convert("RGB").resize((W, H), Image.LANCZOS).save(os.path.join(HERE, "thumbnail.jpg"), quality=92)
print("ok")
