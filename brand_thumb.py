"""Stamp the Plainly Silicon logo on a thumbnail (same size and spot on every thumbnail).

Usage: python3 brand_thumb.py IN.jpg OUT.jpg [--no-logo]   (16:9 long-video or 9:16 Shorts thumbnail;
9:16 ones are fitted into the 2:3 area YouTube actually shows)
Canva makes the design; this adds the brand mark so it never depends on the generated layout:
the logo tile in the top-right corner (bottom-right is covered by YouTube's duration badge), 9% of the thumbnail height from the edges.
"""
import os, sys
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))


def shorts_safe(im):
    """YouTube crops Shorts thumbnails to about 2:3 (Studio grid, Shorts shelves), cutting ~8% off
    the top and bottom of a 9:16 image. Fit the whole design inside the centre 2:3 area and fill
    the rest of the 1080x1920 frame with a blurred copy, so nothing important is ever cropped."""
    W, H = 1080, 1920
    safe_h = int(W * 3 / 2)                      # 1620: the part every surface shows
    s = safe_h / im.height
    fg = im.resize((int(im.width * s), safe_h), Image.LANCZOS)
    bg = im.resize((W, H), Image.LANCZOS).filter(ImageFilter.GaussianBlur(40))
    bg = Image.blend(bg, Image.new("RGB", (W, H), (0, 0, 0)), 0.35)
    bg.paste(fg, ((W - fg.width) // 2, (H - safe_h) // 2))
    return bg


def stamp(src, dst, logo_too=True):
    im = Image.open(src).convert("RGB")
    # long videos: 1280x720 (16:9); Shorts: 1080x1920 (9:16, vertical like the Short itself)
    target = (1280, 720) if im.width > im.height else (1080, 1920)
    if im.size != target:
        im = im.resize(target, Image.LANCZOS)
    if target == (1080, 1920):
        im = shorts_safe(im)
    if not logo_too:
        im.save(dst, quality=92)
        return
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
    # --no-logo: the design already has the logo (e.g. the owner's own Canva covers)
    stamp(sys.argv[1], sys.argv[2], logo_too="--no-logo" not in sys.argv)
    print("ok", sys.argv[2])
