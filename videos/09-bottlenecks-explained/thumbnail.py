"""Thumbnail for video 09: a small CPU chip choking a big graphics card through a narrow pipe, ocean palette."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "../.."))
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, K = 1280, 720, 2
TOP = (8, 24, 44); BOT = (14, 38, 66); PANEL = (20, 50, 86); BLUE = (96, 165, 250); EMER = (52, 211, 153)
WHITE = (240, 246, 252); RED = (248, 113, 113); MUTED = (130, 150, 180)
GF = "/usr/share/fonts/truetype/google-fonts/"
w, h = W * K, H * K
img = Image.new("RGBA", (w, h), TOP + (255,))
d = ImageDraw.Draw(img)
for gy in range(h):
    f = gy / h
    d.line([(0, gy), (w, gy)], fill=tuple(int(TOP[i] + (BOT[i] - TOP[i]) * f) for i in range(3)) + (255,))

def S(*v):
    return [p * K for p in v]

# glow layer
gl = Image.new("RGBA", (w, h), (0, 0, 0, 0))
g = ImageDraw.Draw(gl)
g.rounded_rectangle(S(840, 170, 1240, 470), radius=30 * K, outline=BLUE + (160,), width=24 * K)
g.ellipse(S(660, 240, 810, 400), outline=RED + (200,), width=22 * K)
img.alpha_composite(gl.filter(ImageFilter.GaussianBlur(16 * K)))
d = ImageDraw.Draw(img)

# GPU card
d.rounded_rectangle(S(840, 170, 1240, 470), radius=30 * K, fill=PANEL, outline=BLUE, width=8 * K)
for cx in (950, 1130):
    d.ellipse(S(cx - 80, 240, cx + 80, 400), outline=BLUE, width=7 * K)
    d.ellipse(S(cx - 22, 298, cx + 22, 342), fill=BLUE)
d.text((1040 * K, 520 * K), "GPU", font=ImageFont.truetype(GF + "Poppins-Bold.ttf", 44 * K), fill=BLUE, anchor="mm")
# narrow pipe into the card
d.rounded_rectangle(S(620, 296, 845, 344), radius=12 * K, fill=PANEL, outline=EMER, width=6 * K)
for px in (660, 710, 760, 810):
    d.ellipse(S(px - 9, 311, px + 9, 329), fill=WHITE)
d.ellipse(S(660, 230, 810, 410), outline=RED, width=9 * K)
# small CPU chip
d.rounded_rectangle(S(530, 270, 630, 370), radius=12 * K, fill=PANEL, outline=EMER, width=6 * K)
for i in range(2):
    for j in range(2):
        d.rounded_rectangle(S(548 + i * 42, 288 + j * 42, 572 + i * 42, 312 + j * 42), radius=4 * K, fill=EMER)
d.text((580 * K, 240 * K), "CPU", font=ImageFont.truetype(GF + "Poppins-Bold.ttf", 34 * K), fill=EMER, anchor="mm")

big = ImageFont.truetype(GF + "Poppins-Bold.ttf", 168 * K)
d.text((50 * K, 30 * K), "CPU", font=big, fill=WHITE)
d.text((60 * K, 230 * K), "or", font=ImageFont.truetype(GF + "Poppins-Bold.ttf", 80 * K), fill=MUTED)
d.text((50 * K, 300 * K), "GPU?", font=big, fill=EMER)
d.rounded_rectangle(S(60, 560, 640, 640), radius=40 * K, fill=WHITE)
d.text((350 * K, 600 * K), "102 vs 186 FPS, same GPU", font=ImageFont.truetype(GF + "Poppins-Bold.ttf", 38 * K), fill=TOP, anchor="mm")
logo = Image.open(os.path.join(ROOT, "brand/plainly-silicon-logo.png")).convert("RGBA").resize((80 * K, 80 * K))
img.alpha_composite(logo, (1170 * K, 620 * K))
img.convert("RGB").resize((W, H), Image.LANCZOS).save(os.path.join(HERE, "thumbnail.jpg"), quality=92)
print("ok")
