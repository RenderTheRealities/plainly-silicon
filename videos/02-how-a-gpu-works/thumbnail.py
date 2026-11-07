"""Thumbnail for video 02 (neon theme): a wireframe triangle dissolving into lit pixels + '16 ms / ONE FRAME'."""
import math, os
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "../.."))
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, K = 1280, 720, 2
BG = (4, 4, 10); MAG = (217, 70, 239); CY = (34, 211, 238); WHITE = (245, 240, 255)
GF = "/usr/share/fonts/truetype/google-fonts/"
w, h = W * K, H * K
img = Image.new("RGBA", (w, h), BG + (255,))
glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
ImageDraw.Draw(glow).ellipse([w * 0.42, -h * 0.1, w * 1.15, h * 1.05], fill=(60, 16, 90, 255))
img.alpha_composite(glow.filter(ImageFilter.GaussianBlur(170)))

layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
d = ImageDraw.Draw(layer)
# pixel grid filling the big triangle
tri = [(700 * K, 640 * K), (960 * K, 70 * K), (1240 * K, 620 * K)]
def inside(px, py):
    def s(a, b, c): return (a[0] - c[0]) * (b[1] - c[1]) - (b[0] - c[0]) * (a[1] - c[1])
    d1, d2, d3 = s((px, py), tri[0], tri[1]), s((px, py), tri[1], tri[2]), s((px, py), tri[2], tri[0])
    return not ((d1 < 0 or d2 < 0 or d3 < 0) and (d1 > 0 or d2 > 0 or d3 > 0))
c = 40 * K
for gy in range(60 * K, 660 * K, c):
    for gx in range(680 * K, 1260 * K, c):
        cx, cy = gx + c / 2, gy + c / 2
        if inside(cx, cy) and cx > 900 * K:   # right part of triangle already "pixelated"
            hue = (math.sin(gx / 90 + gy / 140) + 1) / 2
            col = tuple(int(MAG[i] * hue + CY[i] * (1 - hue)) for i in range(3))
            d.rectangle([gx + 4 * K, gy + 4 * K, gx + c - 4 * K, gy + c - 4 * K], fill=col + (255,))
d.line(tri + [tri[0]], fill=WHITE + (255,), width=6 * K, joint="curve")
for p in tri:
    d.ellipse([p[0] - 16 * K, p[1] - 16 * K, p[0] + 16 * K, p[1] + 16 * K], fill=CY + (255,))
g = layer.filter(ImageFilter.GaussianBlur(14 * K))
img.alpha_composite(g); img.alpha_composite(layer)

t1 = ImageFont.truetype(GF + "Poppins-Bold.ttf", 210 * K)
t2 = ImageFont.truetype(GF + "Poppins-Bold.ttf", 112 * K)
shadow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
sd = ImageDraw.Draw(shadow)
sd.text((64 * K, 120 * K), "16 ms", font=t1, fill=(0, 0, 0, 230))
sd.text((64 * K, 400 * K), "1 FRAME", font=t2, fill=(0, 0, 0, 230))
img.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(18 * K)))
dd = ImageDraw.Draw(img)
dd.text((58 * K, 110 * K), "16 ms", font=t1, fill=WHITE)
dd.text((60 * K, 392 * K), "1 FRAME", font=t2, fill=CY)
logo = Image.open(os.path.join(ROOT, "brand/plainly-silicon-logo.png")).convert("RGBA").resize((88 * K, 88 * K))
img.alpha_composite(logo, (60 * K, 600 * K))
img.convert("RGB").resize((W, H), Image.LANCZOS).save(os.path.join(HERE, "thumbnail.jpg"), quality=92)
print("ok")
