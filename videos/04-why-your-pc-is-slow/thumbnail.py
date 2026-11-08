"""Thumbnail for video 4: Task Manager-style meters with Disk pinned at 100% + big text."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "../.."))
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, K = 1280, 720, 2
NAVY = (11, 18, 32); PANEL = (17, 27, 46); GRID = (20, 31, 52)
CYAN = (34, 211, 238); AMBER = (245, 158, 11); WHITE = (240, 242, 245); RED = (239, 68, 68)
FD = "/usr/share/fonts/opentype/inter/"
DV = "/usr/share/fonts/truetype/dejavu/"
w, h = W * K, H * K
img = Image.new("RGBA", (w, h), NAVY + (255,))
gd = ImageDraw.Draw(img)
for gx in range(0, w, 60 * K):
    gd.line([(gx, 0), (gx, h)], fill=GRID + (255,), width=K)
for gy in range(0, h, 60 * K):
    gd.line([(0, gy), (w, gy)], fill=GRID + (255,), width=K)
bg = Image.new("RGBA", (w, h), (0, 0, 0, 0))
ImageDraw.Draw(bg).ellipse([w * 0.55, h * 0.05, w * 1.1, h * 1.0], fill=(90, 20, 30, 200))
img.alpha_composite(bg.filter(ImageFilter.GaussianBlur(150)))

# meter panel on the right
layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
d = ImageDraw.Draw(layer)
px0, py0, px1, py1 = 700 * K, 70 * K, 1230 * K, 650 * K
d.rectangle([px0, py0, px1, py1], fill=PANEL + (255,), outline=CYAN + (180,), width=3 * K)
d.rectangle([px0, py0, px1, py0 + 40 * K], fill=GRID + (255,))
d.rectangle([px0, py0, px0 + 8 * K, py0 + 40 * K], fill=CYAN + (255,))
lab = ImageFont.truetype(FD + "Inter-SemiBold.otf", 30 * K)
num = ImageFont.truetype(DV + "DejaVuSansMono-Bold.ttf", 34 * K)
meters = [("CPU", 0.15, CYAN), ("RAM", 0.68, AMBER), ("DISK", 1.0, RED)]
top, bot = 170 * K, 560 * K
for i, (nm, f, c) in enumerate(meters):
    cx = (820 + i * 150) * K
    bw = (70 if nm != "DISK" else 96) * K
    d.rectangle([cx - bw / 2, top, cx + bw / 2, bot], fill=GRID + (255,))
    d.rectangle([cx - bw / 2, bot - (bot - top) * f, cx + bw / 2, bot], fill=c + (255,))
    d.text((cx, bot + 14 * K), nm, font=lab, fill=WHITE + (255,), anchor="mt")
    if nm == "DISK":
        d.text((cx, top - 14 * K), "100%", font=num, fill=c + (255,), anchor="md")
        d.rectangle([cx - bw / 2 - 12 * K, top - 8 * K, cx + bw / 2 + 12 * K, bot + 8 * K], outline=RED + (255,), width=5 * K)
g = layer.filter(ImageFilter.GaussianBlur(12 * K))
img.alpha_composite(g)
img.alpha_composite(layer)

# text
t1 = ImageFont.truetype(FD + "InterDisplay-Black.otf", 150 * K)
t2 = ImageFont.truetype(FD + "InterDisplay-Black.otf", 150 * K)
lines = [((60, 110), "NOT", WHITE, t1), ((60, 260), "THE", WHITE, t1), ((60, 410), "RAM", AMBER, t2)]
shadow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
sd = ImageDraw.Draw(shadow)
for (x, y), s, c, f in lines:
    sd.text(((x + 4) * K, (y + 8) * K), s, font=f, fill=(0, 0, 0, 230))
img.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(16 * K)))
dd = ImageDraw.Draw(img)
for (x, y), s, c, f in lines:
    dd.text((x * K, y * K), s, font=f, fill=c + (255,))

logo = Image.open(os.path.join(ROOT, "brand/plainly-silicon-logo.png")).convert("RGBA").resize((72 * K, 72 * K))
img.alpha_composite(logo, (1180 * K - 72 * K + 40 * K, 40 * K) if False else (60 * K, 615 * K))

img.convert("RGB").resize((W, H), Image.LANCZOS).save(os.path.join(HERE, "thumbnail.jpg"), quality=92)
print("ok")
