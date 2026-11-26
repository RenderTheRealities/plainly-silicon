"""Short 23s1: why Intel Arc needs Resizable BAR (vertical, blueprint theme). Teases 23-best-budget-gpu.
Visual language: an engineering drawing: a VRAM block drawn as a stack of 48 cells with dimension
lines, a small "aperture" frame that slides over the cells, the aperture snapping open to the full
block with data packets dropping in, a two-column performance gauge, a BIOS toggle switch, and a
plain end card."""
import math
from render import *  # noqa: F401,F403

SIZE = (1080, 1920)
CX = 540
COLS, ROWS = 6, 8          # 48 cells = 12 GB, each cell 256 MB
CW, CH = 100, 62
GX0, GY0 = CX - COLS * CW // 2, 640


def cell_box(i):
    r, c = divmod(i, COLS)
    return [GX0 + c * CW + 6, GY0 + r * CH + 6, GX0 + (c + 1) * CW - 6, GY0 + (r + 1) * CH - 6]


def vram(x, a, lit=None, fillc=None):
    """The VRAM block: 48 cells with a dimension line down the right side."""
    x.rect([GX0 - 14, GY0 - 14, GX0 + COLS * CW + 14, GY0 + ROWS * CH + 14], WHITE, a, 4, r=6, glow=False)
    for i in range(COLS * ROWS):
        on = lit(i) if lit else 0
        b = cell_box(i)
        x.d.rectangle(b, fill=col(fillc or CYAN, a * (0.18 + 0.72 * on)), outline=col(MUTED, a * 0.6))
    # dimension line (blueprint style)
    dx = GX0 + COLS * CW + 50
    x.line([(dx, GY0), (dx, GY0 + ROWS * CH)], MUTED, a, 3, glow=False)
    for yy in (GY0, GY0 + ROWS * CH):
        x.line([(dx - 16, yy), (dx + 16, yy)], MUTED, a, 3, glow=False)


def cpu(x, cx, cy, a, s=120):
    chip_icon(x, cx, cy, s, WHITE, a, 4, pins=4)
    x.text((cx, cy), "CPU", "title", int(s * 0.32), WHITE, a, anchor="mm")


def aperture(x, box, c, a, w=8):
    """Corner-bracket frame, like a camera viewfinder."""
    if a <= 0:
        return
    x0, y0, x1, y1 = box
    L = min(34, (x1 - x0) / 3)
    for (px, py, sx, sy) in ((x0, y0, 1, 1), (x1, y0, -1, 1), (x0, y1, 1, -1), (x1, y1, -1, -1)):
        x.line([(px + sx * L, py), (px, py), (px, py + sy * L)], c, a, w, glow=False)


# ---------- scene 1: 12 GB, but only 256 MB reachable ----------
def s_hook(x):
    a = x.b(0)
    cpu(x, CX, 470, a)
    vram(x, a, lit=lambda i: 1.0 if i == 0 else 0.0)
    x.text((GX0 + COLS * CW + 70, GY0 + ROWS * CH / 2), "12 GB", "title", 46, WHITE, a, anchor="lm")
    a1 = x.b(1)
    b = cell_box(0)
    x.line([(CX, 540), (CX, 590), ((b[0] + b[2]) / 2, 590), ((b[0] + b[2]) / 2, b[1] - 6)], AMBER, a1, 6, glow=False)
    aperture(x, [b[0] - 12, b[1] - 12, b[2] + 12, b[3] + 12], AMBER, a1)
    if a1 > 0:
        label_box(x, CX, 1225, "CPU reaches 256 MB at a time", AMBER, a1, 44)


# ---------- scene 2: the sliding window ----------
def s_slide(x):
    a = x.b(0)
    cpu(x, CX, 470, a)
    tt = x.since(0)
    pos = int(tt / 0.22) % (COLS * ROWS)
    vram(x, a, lit=lambda i: 1.0 if i == pos else (0.35 if i < pos else 0.0))
    b = cell_box(pos)
    aperture(x, [b[0] - 12, b[1] - 12, b[2] + 12, b[3] + 12], AMBER, a)
    x.line([(CX, 540), ((b[0] + b[2]) / 2, b[1] - 14)], AMBER, a * 0.8, 4, glow=False)
    x.text((GX0 + COLS * CW + 70, GY0 + ROWS * CH / 2), "12 GB", "title", 46, WHITE, a, anchor="lm")
    x.text((90, 470), "since 32-bit", "semi", 36, MUTED, a, anchor="lm")
    a1 = x.b(1)
    if a1 > 0:
        label_box(x, CX, 1225, "slide, read, slide, read...", AMBER, a1, 44)


# ---------- scene 3: the window opens to the whole card ----------
def s_open(x):
    a = x.b(0)
    cpu(x, CX, 470, a)
    g = ease(x.since(0) / 0.9)
    b0 = cell_box(0)
    full = [GX0 - 26, GY0 - 26, GX0 + COLS * CW + 26, GY0 + ROWS * CH + 26]
    box = [b0[0] - 12 + (full[0] - b0[0] + 12) * g, b0[1] - 12 + (full[1] - b0[1] + 12) * g,
           b0[2] + 12 + (full[2] - b0[2] - 12) * g, b0[3] + 12 + (full[3] - b0[3] - 12) * g]
    a1 = x.b(1)
    tt = x.since(1)
    filled = int(tt / 0.04) if a1 > 0 else 0
    vram(x, a, lit=lambda i: 1.0 if i < filled else 0.0, fillc=GREEN)
    aperture(x, box, GREEN, a, 10)
    x.text((GX0 + COLS * CW + 70, GY0 + ROWS * CH / 2), "12 GB", "title", 46, WHITE, a, anchor="lm")
    if a1 > 0:
        # data packets falling from the CPU into the block, many lanes at once
        for k in range(COLS):
            px = GX0 + k * CW + CW / 2
            yy = 560 + ((tt * 420 + k * 37) % 90)
            x.d.rectangle([px - 14, yy, px + 14, yy + 22], fill=col(GREEN, a1))
    x.text((CX, 1235), "RESIZABLE BAR: ON", "title", 58, GREEN, a, anchor="mm")


# ---------- scene 4: who depends on it ----------
def s_gauge(x):
    a = x.b(0)
    x.text((CX, 430), "1080p performance, BAR on = 100", "semi", 36, MUTED, a, anchor="mm")
    # small chips: Nvidia / AMD gain a little
    for k, nm in enumerate(("Nvidia", "AMD")):
        cx = 300 + k * 480
        x.rect([cx - 170, 480, cx + 170, 580], WHITE, a, 3, r=10, fill=PANEL + (255,), glow=False)
        x.text((cx, 530), f"{nm}: small gain", "semi", 36, WHITE, a, anchor="mm")
    a1 = x.b(1)
    a2 = x.b(2)
    base = 1180
    hmax = 420
    for k, (lab, v, c, aa, beat) in enumerate((("BAR on", 100, GREEN, a1, 1), ("BAR off", 77, RED, a2, 2))):
        if aa <= 0:
            continue
        cx = 360 + k * 360
        h = hmax * v / 100 * ease(x.since(beat) / 0.8)
        x.d.rectangle([cx - 100, base - h, cx + 100, base], fill=col(c, aa * 0.85))
        x.rect([cx - 100, base - hmax * v / 100, cx + 100, base], WHITE, aa, 3, r=2, glow=False)
        x.text((cx, base - hmax * v / 100 - 40), str(v), "title", 64, WHITE, aa, anchor="mm")
        x.text((cx, base + 40), lab, "semi", 40, c, aa, anchor="mm")
    x.line([(200, base), (880, base)], WHITE, a1, 4, glow=False)
    if a1 > 0:
        x.text((CX, 650), "Intel Arc A770", "title", 52, WHITE, a1, anchor="mm")
    if a2 > 0:
        x.text((CX, base + 100), "source: TechPowerUp", "reg", 30, MUTED, a2, anchor="mm")


# ---------- scene 5: BIOS toggle ----------
def s_bios(x):
    a = x.b(0)
    x.rect([110, 480, 970, 900], WHITE, a, 4, r=4, fill=PANEL + (255,), glow=False)
    x.d.rectangle([110, 480, 970, 545], fill=col(WHITE, a * 0.9))
    x.text((140, 512), "BIOS  >  PCI Subsystem", "semi", 34, NAVY, a, anchor="lm")
    rows = ["Above 4G Decoding", "Re-Size BAR Support"]
    on = ease((x.since(0) - 0.6) / 0.4)
    for k, nm in enumerate(rows):
        y = 640 + k * 140
        x.text((150, y), nm, "semi", 42, WHITE, a, anchor="lm")
        # toggle
        tx = 790
        c = GREEN if on > 0.5 else MUTED
        x.rect([tx, y - 36, tx + 130, y + 36], c, a, 4, r=36, fill=(c[0], c[1], c[2], 90), glow=False)
        kx = tx + 36 + 58 * on
        x.circle(kx, y, 26, WHITE, a, 3, fill=WHITE)
    a1 = x.b(1)
    if a1 > 0:
        stamp(x, CX, 1080, "NO SWITCH? SKIP ARC", RED, a1, angle=-6)


# ---------- scene 6: the long video ----------
def s_end(x):
    a = x.b(0)
    x.rect([150, 520, 930, 1000], WHITE, a, 5, r=4, glow=False)
    aperture(x, [130, 500, 950, 1020], AMBER, a, 8)
    x.text((CX, 610), "FULL VIDEO", "semi", 38, MUTED, a, anchor="mm")
    x.text((CX, 740), "Best Budget", "title", 96, WHITE, a, anchor="mm")
    x.text((CX, 860), "GPUs, Ranked", "title", 96, AMBER, a, anchor="mm")
    x.text((CX, 950), "linked below", "semi", 40, MUTED, a, anchor="mm")


SCENES = [
    ("12 GB, but 256 MB at a time", s_hook),
    ("A 32-bit leftover", s_slide),
    ("Resizable BAR opens it", s_open),
    ("Arc is built around it", s_gauge),
    ("Check your BIOS", s_bios),
    ("Which budget GPU wins?", s_end),
]
