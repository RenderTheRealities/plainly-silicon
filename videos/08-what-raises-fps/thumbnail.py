"""Thumbnail for video 08: a monitor whose FPS counter jumps from 48 to 85, arctic palette (light ice)."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "../.."))
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, K = 1280, 720, 2
ICE = (232, 241, 250); GRIDC = (205, 222, 240); PANEL = (250, 252, 255); INK = (15, 32, 54)
TEAL = (14, 116, 144); ORANGE = (234, 88, 12); GREEN = (4, 120, 87); RED = (200, 30, 50); MUTED = (90, 110, 135)
FD = "/usr/share/fonts/opentype/inter/"
DV = "/usr/share/fonts/truetype/dejavu/"
w, h = W * K, H * K
img = Image.new("RGBA", (w, h), ICE + (255,))
d = ImageDraw.Draw(img)
for i, gx in enumerate(range(0, w, 30 * K)):
    d.line([(gx, 0), (gx, h)], fill=GRIDC + (255 if i % 5 == 0 else 120,), width=(2 if i % 5 == 0 else 1) * K)
for i, gy in enumerate(range(0, h, 30 * K)):
    d.line([(0, gy), (w, gy)], fill=GRIDC + (255 if i % 5 == 0 else 120,), width=(2 if i % 5 == 0 else 1) * K)

# monitor with shadow
mx0, my0, mx1, my1 = 640 * K, 90 * K, 1220 * K, 500 * K
sh = Image.new("RGBA", (w, h), (0, 0, 0, 0))
ImageDraw.Draw(sh).rounded_rectangle([mx0 + 14 * K, my0 + 20 * K, mx1 + 14 * K, my1 + 20 * K], radius=26 * K, fill=(15, 32, 54, 90))
img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(18 * K)))
d = ImageDraw.Draw(img)
d.rounded_rectangle([mx0, my0, mx1, my1], radius=26 * K, fill=INK)
d.rounded_rectangle([mx0 + 22 * K, my0 + 22 * K, mx1 - 22 * K, my1 - 22 * K], radius=12 * K, fill=PANEL)
d.rectangle([900 * K, my1, 960 * K, 570 * K], fill=INK)
d.rounded_rectangle([820 * K, 565 * K, 1040 * K, 590 * K], radius=10 * K, fill=INK)

mono = ImageFont.truetype(DV + "DejaVuSansMono-Bold.ttf", 120 * K)
monos = ImageFont.truetype(DV + "DejaVuSansMono-Bold.ttf", 34 * K)
d.text((790 * K, 230 * K), "48", font=mono, fill=MUTED, anchor="mm")
d.line([(700 * K, 262 * K), (880 * K, 200 * K)], fill=RED, width=12 * K)
d.text((1075 * K, 230 * K), "85", font=mono, fill=GREEN, anchor="mm")
# arrow between
d.line([(888 * K, 232 * K), (945 * K, 232 * K)], fill=INK, width=10 * K)
d.polygon([(965 * K, 232 * K), (940 * K, 212 * K), (940 * K, 252 * K)], fill=INK)
d.text((930 * K, 345 * K), "FPS", font=monos, fill=MUTED, anchor="mm")
# frame-time bars
d.rounded_rectangle([700 * K, 395 * K, 1160 * K, 425 * K], radius=12 * K, fill=GRIDC)
d.rounded_rectangle([700 * K, 395 * K, 700 * K + 460 * K * 0.56, 425 * K], radius=12 * K, fill=TEAL)

t1 = ImageFont.truetype(FD + "InterDisplay-Bold.otf", 176 * K)
t2 = ImageFont.truetype(FD + "InterDisplay-Bold.otf", 176 * K)
d.text((54 * K, 70 * K), "FREE", font=t1, fill=INK)
d.text((54 * K, 270 * K), "FPS", font=t2, fill=ORANGE)
d.rounded_rectangle([60 * K, 520 * K, 560 * K, 600 * K], radius=40 * K, fill=INK)
d.text((310 * K, 560 * K), "+ 5 MYTHS BUSTED", font=ImageFont.truetype(FD + "Inter-SemiBold.otf", 42 * K), fill=PANEL, anchor="mm")
logo = Image.open(os.path.join(ROOT, "brand/plainly-silicon-logo.png")).convert("RGBA").resize((80 * K, 80 * K))
img.alpha_composite(logo, (1170 * K, 620 * K))
img.convert("RGB").resize((W, H), Image.LANCZOS).save(os.path.join(HERE, "thumbnail.jpg"), quality=92)
print("ok")
