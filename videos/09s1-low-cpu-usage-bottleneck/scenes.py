"""Short 09s1: low total CPU usage can still be a CPU bottleneck (vertical, arctic theme).
Visual language: a big semicircle usage dial, a 4x4 grid of thread tiles that fill like
liquid, a relay-race lane where one runner sets the pace, and a two-zone GPU gauge."""
import math
from render import *  # noqa: F401,F403

SIZE = (1080, 1920)
CX = 540


def dial(x, cx, cy, r, frac, c, a, label="", big=""):
    """Semicircle gauge from 180 to 360 degrees, filled to frac."""
    if a <= 0:
        return
    box = [cx - r, cy - r, cx + r, cy + r]
    x.d.arc(box, 180, 360, fill=col(GRID, a), width=46)
    if frac > 0.005:
        x.d.arc(box, 180, 180 + 180 * clamp(frac), fill=col(c, a), width=46)
    ang = math.pi + math.pi * clamp(frac)
    x.line([(cx, cy), (cx + (r - 70) * math.cos(ang), cy + (r - 70) * math.sin(ang))], WHITE, a, 8, glow=False)
    x.circle(cx, cy, 18, WHITE, a, 4, fill=WHITE)
    if big:
        x.text((cx, cy + 90), big, "title", 110, c, a, anchor="mm")
    if label:
        x.text((cx, cy - r - 40), label, "semi", 40, MUTED, a, anchor="md")


def tile(x, cx, cy, s, frac, c, a, hot=False):
    """A thread tile that fills from the bottom."""
    if a <= 0:
        return
    x0, y0, x1, y1 = cx - s / 2, cy - s / 2, cx + s / 2, cy + s / 2
    x.rect([x0, y0, x1, y1], MUTED, a, 3, r=12, fill=PANEL + (255,), glow=False)
    if frac > 0.01:
        x.d.rounded_rectangle([x0 + 6, y1 - 6 - (s - 12) * frac, x1 - 6, y1 - 6], radius=8, fill=col(c, a))
    if hot:
        x.rect([x0 - 8, y0 - 8, x1 + 8, y1 + 8], RED, a, 5, r=16, glow=False)


def grid_pos(i):
    return 240 + (i % 4) * 200, 560 + (i // 4) * 150


# ---------- scene 1: 40 percent, yet the limit ----------
def s_hook(x):
    a = x.b(0)
    p = ease(x.since(0) / 1.2)
    dial(x, CX, 800, 300, 0.4 * p, CYAN, a, label="CPU usage", big=f"{int(40 * p)}%")
    a1 = x.b(1)
    if a1 > 0:
        stamp(x, CX, 1130, "STILL THE LIMIT?", RED, a1, angle=-5)


# ---------- scene 2: an average of every thread ----------
def s_average(x):
    a = x.b(0)
    loads = [1.0, 0.7, 0.55, 0.4, 0.3, 0.6, 0.2, 0.35, 0.25, 0.5, 0.15, 0.3, 0.2, 0.45, 0.1, 0.3]
    for i, f in enumerate(loads):
        cx, cy = grid_pos(i)
        aa = a * ease((x.since(0) - i * 0.06) / 0.4)
        wob = 0.06 * math.sin(x.t * 2 + i) if i else 0
        tile(x, cx, cy, 128, clamp(f + wob), CYAN, aa)
    x.text((CX, 440), "16 threads, averaged", "semi", 44, WHITE, a, anchor="mm")
    a1 = x.b(1)
    if a1 > 0:
        label_box(x, CX, 1230, "uneven work, one number", AMBER, a1, 40)


# ---------- scene 3: one thread flat out = about 6 percent ----------
def s_main(x):
    a = x.b(0)
    for i in range(16):
        cx, cy = grid_pos(i)
        main = i == 0
        f = 1.0 if main else 0.0
        tile(x, cx, cy, 128, f * ease(x.since(0) / 0.8), RED if main else CYAN, a, hot=main and x.b(0) > 0.5)
    tx, ty = grid_pos(0)
    x.text((tx, ty - 110), "main thread", "semi", 34, RED, a, anchor="mm")
    a1 = x.b(1)
    if a1 > 0:
        x.text((CX, 1185), "1 / 16 = ", "title", 70, WHITE, a1, anchor="rm")
        x.text((CX + 10, 1185), "~6%", "title", 90, RED, a1, anchor="lm")


# ---------- scene 4: the slowest runner sets the pace ----------
def s_pace(x):
    a = x.b(0)
    lanes = 4
    for k in range(lanes):
        y = 520 + k * 170
        x.line([(110, y + 50), (970, y + 50)], MUTED, a * 0.6, 3, glow=False)
        main = k == 0
        speed = 0.35 if main else 1.0
        if main:
            pos = (x.since(0) * speed * 0.3) % 1
        else:
            # helpers dash ahead, then wait at the finish
            pos = min(1.0, x.since(0) * 0.9)
        px = 140 + 780 * pos
        c = RED if main else CYAN
        x.circle(px, y, 34, c, a, 5, fill=c)
        if main:
            x.text((px, y - 62), "main thread", "semi", 30, RED, a, anchor="mm")
        if not main and pos >= 1.0:
            x.text((px - 60, y), "waiting", "semi", 30, MUTED, a, anchor="rm")
    x.line([(950, 470), (950, 1080)], WHITE, a, 6, glow=False)
    x.text((950, 450), "frame done", "semi", 34, WHITE, a, anchor="md")
    label_box(x, CX, 1190, "slowest thread = your FPS", RED, a, 40)


# ---------- scene 5: read the GPU gauge ----------
def s_gpu(x):
    a = x.b(0)
    x.text((CX, 440), "GPU usage", "semi", 46, MUTED, a, anchor="mm")
    x0, x1, y = 120, 960, 620

    def px(v):
        return x0 + (x1 - x0) * (v - 50) / 50
    x.d.rounded_rectangle([x0, y, x1, y + 80], radius=40, fill=col(GRID, a))
    a2 = x.b(2)
    if a2 > 0:
        x.d.rounded_rectangle([x0, y, px(90), y + 80], radius=40, fill=col(AMBER, a2 * 0.85))
    a1 = x.b(1)
    if a1 > 0:
        x.d.rounded_rectangle([px(95), y, x1, y + 80], radius=16, fill=col(GREEN, a1 * 0.9))
    for v, up in ((50, False), (90, False), (95, True), (100, False)):
        if up:
            x.text((px(v), y - 20), f"{v}%", "semi", 34, WHITE, a, anchor="md")
        else:
            x.text((px(v), y + 100), f"{v}%", "semi", 34, WHITE, a, anchor="mt")
    if a1 > 0:
        x.text((CX, 860), "95%+  ->  GPU is the limit", "title", 48, GREEN, a1, anchor="mm")
    if a2 > 0:
        x.text((CX, 960), "under 90%  ->  likely the CPU", "title", 48, AMBER, a2, anchor="mm")
        x.text((CX, 1040), "(no frame cap, no V-Sync)", "reg", 36, MUTED, a2, anchor="mm")
        # needle sweeping in the low zone
        v = 68 + 10 * math.sin(x.t * 1.6)
        x.line([(px(v), y - 30), (px(v), y + 110)], WHITE, a2, 6, glow=False)


# ---------- scene 6: point to the long video ----------
def s_end(x):
    a = x.b(0)
    x.rect([140, 560, 940, 1060], CYAN, a, 5, r=28, fill=PANEL + (255,), glow=False)
    x.text((CX, 660), "FULL GUIDE", "semi", 40, MUTED, a, anchor="mm")
    x.text((CX, 790), "Bottlenecks", "title", 90, WHITE, a, anchor="mm")
    x.text((CX, 900), "Explained", "title", 90, CYAN, a, anchor="mm")
    # a tiny pipe narrowing as a motif
    p = ease(x.since(0) / 1.0)
    x.d.polygon([(260, 980), (480, 990), (480, 1010), (260, 1020)], fill=col(CYAN, a * p))
    x.d.polygon([(600, 990), (820, 980), (820, 1020), (600, 1010)], fill=col(CYAN, a * p))
    x.d.rectangle([480, 994, 600, 1006], fill=col(RED, a * p))


SCENES = [
    ("Only 40% busy?", s_hook),
    ("One number, 16 threads", s_average),
    ("The main thread", s_main),
    ("The slowest thread sets the pace", s_pace),
    ("Check the GPU instead", s_gpu),
    ("Bottlenecks Explained", s_end),
]
