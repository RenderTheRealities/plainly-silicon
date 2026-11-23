"""Thumbnail for video 12: a dusty fan held still while an air can blasts the dust away, mint palette."""
import math, os, random
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "../.."))
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, K = 1280, 720, 2
BG = (5, 38, 35); PANEL = (10, 56, 51); GRIDC = (14, 66, 60); TEAL = (45, 212, 191); AMBER = (253, 230, 138)
WHITE = (236, 253, 245); MUTED = (130, 180, 170); PINK = (251, 113, 133); LIME = (190, 242, 100)
GF = "/usr/share/fonts/truetype/google-fonts/"
w, h = W * K, H * K
img = Image.new("RGBA", (w, h), BG + (255,))
d = ImageDraw.Draw(img)
for k in range(-H, W, 48):
    d.line([(k * K, 0), ((k + H) * K, h)], fill=GRIDC, width=2 * K)


def S(*v):
    return [p * K for p in v]


def pop(size):
    return ImageFont.truetype(GF + "Poppins-Bold.ttf", size * K)


cx, cy, r = 930, 380, 210
gl = Image.new("RGBA", (w, h), (0, 0, 0, 0))
ImageDraw.Draw(gl).ellipse(S(cx - r - 20, cy - r - 20, cx + r + 20, cy + r + 20), outline=TEAL + (160,), width=34 * K)
img.alpha_composite(gl.filter(ImageFilter.GaussianBlur(24 * K)))
d = ImageDraw.Draw(img)
d.rounded_rectangle(S(cx - r * 1.12, cy - r * 1.12, cx + r * 1.12, cy + r * 1.12), radius=40 * K, fill=PANEL, outline=WHITE, width=8 * K)
d.ellipse(S(cx - r, cy - r, cx + r, cy + r), outline=TEAL, width=8 * K)
for k in range(7):
    th = 0.3 + k * 2 * math.pi / 7
    pts = [(cx + r * 0.25 * math.cos(th), cy + r * 0.25 * math.sin(th)),
           (cx + r * 0.9 * math.cos(th + 0.2), cy + r * 0.9 * math.sin(th + 0.2)),
           (cx + r * 0.9 * math.cos(th + 0.62), cy + r * 0.9 * math.sin(th + 0.62)),
           (cx + r * 0.25 * math.cos(th + 0.5), cy + r * 0.25 * math.sin(th + 0.5))]
    d.polygon([(p[0] * K, p[1] * K) for p in pts], fill=TEAL + (150,))
d.ellipse(S(cx - 50, cy - 50, cx + 50, cy + 50), fill=PANEL, outline=TEAL, width=8 * K)
# finger holding the fan still
d.rounded_rectangle(S(cx - 40, cy - 330, cx + 40, cy - 90), radius=40 * K, fill=AMBER, outline=BG, width=5 * K)
# dust: left side dusty, blown out to the left
rnd = random.Random(3)
for _ in range(260):
    px = rnd.uniform(cx - r, cx - 20); py = rnd.uniform(cy - r, cy + r)
    if (px - cx) ** 2 + (py - cy) ** 2 > r * r:
        continue
    s = rnd.uniform(3, 8)
    d.ellipse(S(px - s, py - s, px + s, py + s), fill=MUTED + (220,))
for _ in range(120):
    px = rnd.uniform(620, 700); py = rnd.uniform(200, 580); s = rnd.uniform(3, 9)
    d.ellipse(S(px - s, py - s, px + s, py + s), fill=MUTED + (200,))
# air blast lines from the right
for k in range(5):
    y = 230 + k * 70
    d.line(S(1250, y, 1170, y), fill=WHITE, width=6 * K)
# check badge
d.ellipse(S(1110, 110, 1210, 210), fill=LIME)
d.line(S(1132, 160, 1152, 182, 1190, 136), fill=BG, width=12 * K, joint="curve")

d.text((60 * K, 50 * K), "CLEAN IT", font=pop(132), fill=WHITE)
d.text((60 * K, 230 * K), "SAFELY", font=pop(132), fill=AMBER)
d.rounded_rectangle(S(60, 470, 590, 550), radius=40 * K, fill=PINK)
d.text((325 * K, 512 * K), "3 ways people break PCs", font=pop(34), fill=BG, anchor="mm")
logo = Image.open(os.path.join(ROOT, "brand/plainly-silicon-logo.png")).convert("RGBA").resize((80 * K, 80 * K))
img.alpha_composite(logo, (60 * K, 610 * K))
img.convert("RGB").resize((W, H), Image.LANCZOS).save(os.path.join(HERE, "thumbnail.jpg"), quality=92)
print("ok")
