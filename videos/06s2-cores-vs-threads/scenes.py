"""Short 06s2: cores vs threads and what Hyper-Threading really does (vertical, neon theme).
Conveyor-belt style: threads are lanes of instruction tiles feeding a core's execution units."""
import math
from render import *  # noqa: F401,F403

SIZE = (1080, 1920)
CX = 540


def tiles(x, y, c, a, speed=1.0, x0=60, x1=420, n=5, stop=False, t0=0.0):
    """A lane of instruction tiles sliding right toward a core."""
    step = (x1 - x0) / n
    off = 0 if stop else ((x.t - t0) * 110 * speed) % step
    for k in range(n):
        tx = x0 + k * step + off
        if tx + 50 > x1:
            continue
        x.rect([tx, y - 28, tx + 50, y + 28], c, a, 3, r=8, fill=c + (255,), glow=False)
    x.line([(x0, y + 40), (x1, y + 40)], GRID, a, 4, glow=False)


def core_box(x, a, box=(460, 520, 990, 1060), label="CORE"):
    x0, y0, x1, y1 = box
    x.rect([x0, y0, x1, y1], CYAN, a, 6, r=26, fill=PANEL + (255,))
    x.text(((x0 + x1) / 2, y0 + 46), label, "title", 44, CYAN, a, anchor="mm")


def units(x, a, busy, y0=700, x0=500):
    """Four execution units in a row; busy[i] is None (idle) or a color."""
    for i in range(4):
        ux = x0 + i * 120
        c = busy[i]
        x.rect([ux, y0, ux + 100, y0 + 100], c or MUTED, a, 4, r=12, fill=(c or NAVY) + (255,), glow=False)
        x.text((ux + 50, y0 + 50), ["+", "x", "ld", "br"][i], "title", 40, NAVY if c else MUTED, a, anchor="mm")


# ---------- scene 1: the spec label ----------
def s_hook(x):
    a = x.b(0)
    x.rect([240, 470, 840, 1000], CYAN, a, 6, r=24, fill=PANEL + (255,))
    chip_icon(x, CX, 650, 200, CYAN, a, 5, 5)
    p = ease(x.since(0) / 0.8)
    x.text((CX, 850), f"{int(8 * p)} cores", "title", 70, WHITE, a, anchor="mm")
    x.text((CX, 940), f"{int(16 * p)} threads", "title", 70, AMBER, a, anchor="mm")
    a1 = x.b(1)
    if a1 > 0:
        x.text((CX, 1150), "threads ≠ cores", "title", 64, AMBER, a1, anchor="mm")


# ---------- scene 2: what a thread and a core are ----------
def s_define(x):
    a = x.b(0)
    x.text((70, 600), "thread", "semi", 40, AMBER, a, anchor="lm")
    tiles(x, 680, AMBER, a)
    a1 = x.b(1)
    core_box(x, a1)
    if a1 > 0:
        k = int(x.t * 3) % 4
        units(x, a1, [AMBER if i == k else None for i in range(4)])
        # the "where it's up to" register
        x.rect([520, 870, 930, 970], AMBER, a1, 4, r=14, fill=NAVY + (255,), glow=False)
        x.text((725, 920), f"at step {int(x.t * 3) + 1}", "semi", 38, AMBER, a1, anchor="mm")
        x.text((CX, 1170), "math units + a bookmark", "semi", 44, WHITE, a1, anchor="mm")


# ---------- scene 3: stall and fill ----------
def s_smt(x):
    a = x.b(0)
    core_box(x, a)
    stalled = (x.t % 3) > 1.4
    if x.b(1) <= 0:
        # one thread, stalling: units go dark
        tiles(x, 640, AMBER, a, stop=stalled)
        units(x, a, [None] * 4 if stalled else [AMBER, None, AMBER, None])
        if stalled:
            x.text((725, 900), "waiting on RAM...", "semi", 40, RED, a, anchor="mm")
        return
    a1 = x.b(1)
    tiles(x, 600, AMBER, a1, stop=stalled)
    tiles(x, 780, GREEN, a1, speed=1.3, stop=not stalled and x.b(2) > 0)
    x.text((70, 540), "thread A", "semi", 40, AMBER, a1, anchor="lm")
    x.text((70, 720), "thread B", "semi", 40, GREEN, a1, anchor="lm")
    if x.b(2) > 0:
        busy = [GREEN, GREEN, None, GREEN] if stalled else [AMBER, GREEN, AMBER, None]
    else:
        busy = [None] * 4 if stalled else [AMBER, None, AMBER, None]
    units(x, a1, busy)
    x.rect([500, 880, 700, 950], AMBER, a1, 3, r=10, fill=NAVY + (255,), glow=False)
    x.text((600, 915), "A", "title", 40, AMBER, a1, anchor="mm")
    x.rect([740, 880, 940, 950], GREEN, a1, 3, r=10, fill=NAVY + (255,), glow=False)
    x.text((840, 915), "B", "title", 40, GREEN, a1, anchor="mm")
    label_box(x, CX, 1170, "one core, two threads", AMBER, a1, 42)


# ---------- scene 4: shared units, not double ----------
def s_gain(x):
    a = x.b(0)
    units(x, a, [AMBER, GREEN, AMBER, GREEN], y0=480, x0=300)
    x.text((CX, 640), "same 4 units, shared", "semi", 40, WHITE, a, anchor="mm")
    a1 = x.b(1)
    if a1 > 0:
        p = ease(x.since(1) / 1.0)
        bar(x, 140, 800, 800, 0.5, MUTED, a1, 56)
        bar(x, 140, 960, 800, 0.5 + 0.15 * p, AMBER, a1, 56)
        x.text((140, 780), "1 thread", "semi", 42, WHITE, a1, anchor="ld")
        x.text((140, 940), "2 threads", "semi", 42, WHITE, a1, anchor="ld")
        x.text((140 + 800 * 0.65 + 20, 988), "up to +30%", "title", 40, AMBER, a1 * p, anchor="lm")
        # ghost "double" bar, crossed out
        x.d.rounded_rectangle([140, 1100, 940, 1156], radius=28, outline=col(MUTED, a1), width=3)
        x.text((CX, 1128), "2x", "title", 40, MUTED, a1, anchor="mm")
        x.line([(130, 1170), (950, 1086)], RED, a1 * p, 10, glow=False)


# ---------- scene 5: a chip without it ----------
def s_none(x):
    a = x.b(0)
    x.text((CX, 470), "Core Ultra 9 285K", "title", 56, WHITE, a, anchor="mm")
    a1 = x.b(1)
    # 8 big performance cores and 16 small efficient cores, one thread lane each
    for k in range(24):
        ab = a * ease((x.since(0) - k * 0.05) / 0.3)
        if k < 8:
            r_, c_ = divmod(k, 4)
            bx, by, s = 160 + c_ * 195, 560 + r_ * 175, 150
        else:
            r_, c_ = divmod(k - 8, 8)
            bx, by, s = 130 + c_ * 105, 940 + r_ * 105, 85
        x.rect([bx, by, bx + s, by + s], CYAN, ab, 4, r=10, fill=PANEL + (255,), glow=False)
        x.circle(bx + s / 2, by + s / 2, s * 0.16, AMBER, ab * (a1 if a1 > 0 else 0.0), 0, fill=AMBER)
    if a1 > 0:
        label_box(x, CX, 1200, "24 cores  ·  24 threads", AMBER, a1, 42)


# ---------- scene 6: outro ----------
def s_end(x):
    a = x.b(0)
    core_box(x, a, (240, 520, 840, 950), "1 CORE")
    tiles(x, 700, AMBER, a, x0=290, x1=790, n=6)
    tiles(x, 820, GREEN, a, speed=1.3, x0=290, x1=790, n=6)
    label_box(x, CX, 1120, "How a CPU Runs Your Code", CYAN, a * ease(x.since(0) / 0.6 - 0.3), 44)


SCENES = [("Cores vs threads", s_hook), ("A thread vs a core", s_define), ("Hyper-Threading fills the gaps", s_smt),
          ("Shared, not doubled", s_gain), ("Some CPUs dropped it", s_none), ("The short version", s_end)]
