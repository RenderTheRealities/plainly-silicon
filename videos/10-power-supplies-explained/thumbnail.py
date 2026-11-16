"""Thumbnail for video 10: a power supply with a swollen capacitor and heat rising, ember palette."""
import math, os
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "../.."))
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, K = 1280, 720, 2
BG = (22, 20, 19); PANEL = (40, 35, 32); ORANGE = (251, 146, 60); YELLOW = (250, 204, 21)
WHITE = (245, 240, 235); RED = (239, 68, 68); MUTED = (160, 150, 140)
FD = "/usr/share/fonts/opentype/inter/"
w, h = W * K, H * K
img = Image.new("RGBA", (w, h), BG + (255,))
d = ImageDraw.Draw(img)
for gy in range(0, h, 2):
    f = gy / h
    d.line([(0, gy), (w, gy + 1)], fill=(int(22 + 18 * f), int(20 + 8 * f), 19, 255), width=2)


def S(*v):
    return [p * K for p in v]


gl = Image.new("RGBA", (w, h), (0, 0, 0, 0))
g = ImageDraw.Draw(gl)
g.rectangle(S(700, 170, 1210, 500), outline=ORANGE + (170,), width=26 * K)
g.ellipse(S(1020, 210, 1150, 340), fill=RED + (120,))
img.alpha_composite(gl.filter(ImageFilter.GaussianBlur(18 * K)))
d = ImageDraw.Draw(img)
# PSU box
d.rectangle(S(700, 170, 1210, 500), fill=PANEL, outline=ORANGE, width=8 * K)
fx, fy, fr = 850, 335, 115
d.ellipse(S(fx - fr, fy - fr, fx + fr, fy + fr), outline=MUTED, width=6 * K)
for k in range(5):
    a = k * 2 * math.pi / 5 + 0.3
    d.line(S(fx, fy, fx + fr * 0.85 * math.cos(a), fy + fr * 0.85 * math.sin(a)), fill=MUTED, width=6 * K)
# swollen capacitor
cx = 1085
d.rounded_rectangle(S(cx - 50, 250, cx + 50, 450), radius=18 * K, fill=(70, 50, 40), outline=YELLOW, width=6 * K)
d.ellipse(S(cx - 56, 222, cx + 56, 282), fill=(70, 50, 40), outline=RED, width=7 * K)  # bulging top
d.line(S(cx - 24, 252, cx + 24, 252), fill=RED, width=6 * K)
d.line(S(cx, 232, cx, 272), fill=RED, width=6 * K)
# heat lines
for i, ox in enumerate((1030, 1085, 1140)):
    pts = [S(ox + 12 * math.sin(j / 2 + i), 205 - j * 9)[:2] for j in range(14)]
    d.line(pts, fill=RED, width=7 * K, joint="curve")
# 12 V trace going bad
pts = []
for j in range(120):
    x = 710 + j * 4.2
    n = 0 if j < 50 else (j - 50) / 70 * 26 * math.sin(j * 1.9)
    pts.append((x * K, (560 + n) * K))
d.line(pts, fill=YELLOW, width=6 * K)
d.text((705 * K, 600 * K), "12 V", font=ImageFont.truetype(FD + "Inter-Bold.otf", 34 * K), fill=YELLOW)

big = ImageFont.truetype(FD + "InterDisplay-Black.otf", 170 * K)
d.text((50 * K, 40 * K), "CHEAP", font=big, fill=WHITE)
d.text((50 * K, 240 * K), "PSU?", font=big, fill=ORANGE)
d.rounded_rectangle(S(60, 500, 620, 580), radius=40 * K, fill=WHITE)
d.text((340 * K, 540 * K), "Watts and 80 Plus, explained", font=ImageFont.truetype(FD + "Inter-Bold.otf", 36 * K), fill=BG, anchor="mm")
logo = Image.open(os.path.join(ROOT, "brand/plainly-silicon-logo.png")).convert("RGBA").resize((80 * K, 80 * K))
img.alpha_composite(logo, (1170 * K, 620 * K))
img.convert("RGB").resize((W, H), Image.LANCZOS).save(os.path.join(HERE, "thumbnail.jpg"), quality=92)
print("ok")
