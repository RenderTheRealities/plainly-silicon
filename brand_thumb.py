"""Stamp the Plainly Silicon logo on a thumbnail (same size and spot on every thumbnail).

Usage: python3 brand_thumb.py IN.jpg OUT.jpg
Canva makes the design; this adds the brand mark so it never depends on the generated layout:
the logo tile in the top-right corner (bottom-right is covered by YouTube's duration badge), 9% of the thumbnail height from the edges.
"""
import os, sys
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))


def stamp(src, dst):
    im = Image.open(src).convert("RGB")
    if im.size != (1280, 720) and im.width > im.height:
        im = im.resize((1280, 720), Image.LANCZOS)
    w, h = im.size
    s = int(min(w, h) * 0.13)          # logo size (94 px on 1280x720)
    m = int(min(w, h) * 0.035)         # margin from the edges
    logo = Image.open(os.path.join(HERE, "brand/plainly-silicon-logo.png")).convert("RGBA").resize((s, s), Image.LANCZOS)
    x, y = w - s - m, m
    # soft dark plate so the logo reads on any background
    plate = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(plate).rounded_rectangle([x - 6, y - 6, x + s + 6, y + s + 6], radius=int(s * 0.22), fill=(11, 18, 32, 170))
    out = Image.alpha_composite(im.convert("RGBA"), plate)
    out.alpha_composite(logo, (x, y))
    out.convert("RGB").save(dst, quality=92)


if __name__ == "__main__":
    stamp(sys.argv[1], sys.argv[2])
    print("ok", sys.argv[2])
