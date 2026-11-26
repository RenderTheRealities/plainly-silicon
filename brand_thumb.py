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
    """YouTube crops Shorts thumbnails to about 2:3 (Studio grid, Shorts shelves): roughly the middle
    1080x1620 of a 1080x1920 image. Fit the whole design into that area, then fill the strips beside
    and above/below it by stretching the design's outermost pixels, so the background colour simply
    continues to the frame edge (no blur, no mirrored copies)."""
    W, H = 1080, 1920
    safe_h = int(W * 3 / 2)                      # 1620: the part every surface shows
    s = safe_h / im.height
    fg = im.resize((int(im.width * s), safe_h), Image.LANCZOS)
    x0, y0 = (W - fg.width) // 2, (H - safe_h) // 2
    out = Image.new("RGB", (W, H))
    out.paste(fg, (x0, y0))
    # sides: stretch the design's outermost pixel columns outward (continues the background colour only)
    if x0 > 0:
        left = fg.crop((0, 0, 3, safe_h)).resize((x0, safe_h), Image.BILINEAR)
        rw = W - x0 - fg.width
        right = fg.crop((fg.width - 3, 0, fg.width, safe_h)).resize((rw, safe_h), Image.BILINEAR)
        out.paste(left, (0, y0)); out.paste(right, (x0 + fg.width, y0))
    # top and bottom (outside the shown area): stretch the outermost rows the same way
    out.paste(out.crop((0, y0, W, y0 + 3)).resize((W, y0), Image.BILINEAR), (0, 0))
    hb = H - y0 - safe_h
    out.paste(out.crop((0, y0 + safe_h - 3, W, y0 + safe_h)).resize((W, hb), Image.BILINEAR), (0, y0 + safe_h))
    return out


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
