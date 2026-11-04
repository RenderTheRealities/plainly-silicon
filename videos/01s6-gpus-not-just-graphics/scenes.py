"""Short 01s6: GPUs aren't just for graphics (vertical)."""
import math
from render import *  # noqa: F401,F403

SIZE = (1080, 1920)
CX = 540


def card(x, a, y=560):
    x.rect([140, y, 940, y + 260], CYAN, a, 6, r=18, fill=PANEL + (255,))
    for k, fx in enumerate((330, 640)):
        x.circle(fx, y + 130, 90, CYAN, a, 5)
        for j in range(5):
            ang = x.t * 6 + j * 2 * math.pi / 5 + k
            x.line([(fx, y + 130), (fx + 80 * math.cos(ang), y + 130 + 80 * math.sin(ang))], CYAN, a, 4, glow=False)
    x.rect([780, y + 40, 900, y + 220], AMBER, a, 4, r=8, glow=False)


def a_hook(x):
    card(x, x.b(0))
    x.text((CX, 900), "GRAPHICS card", "title", 64, WHITE, x.b(0), anchor="mm")
    stamp(x, CX, 1080, "NOT JUST GAMES", RED, x.b(1), angle=-6)


def a_split(x):
    a = x.b(0)
    n = int(1 + 11 * ease(x.since(1) / 1.8)) if x.b(1) > 0 else 1
    size = 720 / n
    for r_ in range(n):
        for c_ in range(n):
            x0, y0 = 180 + c_ * size, 470 + r_ * size
            x.d.rectangle([x0 + 3, y0 + 3, x0 + size - 3, y0 + size - 3], outline=col(CYAN, a), width=3,
                          fill=col(CYAN, a * (0.15 + 0.25 * ((r_ + c_) % 2))))
    label_box(x, CX, 1240, "small, independent pieces", AMBER, x.b(1), 40)


def a_ai(x):
    a = x.b(0)
    layers = [(220, 4), (440, 6), (660, 6), (880, 3)]
    pts = [[(lx, 560 + (i + 0.5) * 560 / n) for i in range(n)] for lx, n in layers]
    for L in range(3):
        for p in pts[L]:
            for q in pts[L + 1]:
                x.line([p, q], MUTED, a * 0.5, 2, glow=False)
    for L, layer in enumerate(pts):
        for i, (px, py) in enumerate(layer):
            lit = 0.5 + 0.5 * math.sin(x.t * 4 - L * 1.2 + i)
            x.circle(px, py, 26, CYAN, a, 4, fill=CYAN if lit > 0.75 else None)
    x.text((CX, 480), "AI", "title", 90, AMBER, a, anchor="mm")
    x.text((CX, 1210), "× × ×  millions of multiplications  × × ×", "semi", 32, WHITE, x.b(1), anchor="mm")


def a_science(x):
    items = [(270, 640, "weather"), (810, 640, "molecules"), (CX, 1000, "video editing")]
    for i, (cx, cy, nm) in enumerate(items):
        a = x.b(0 if i < 2 else 1) * ease((x.since(0 if i < 2 else 1) - (i % 2) * 0.3) / 0.5)
        if i == 0:
            for k in range(3):
                x.circle(cx - 50 + k * 50, cy - 20 + (k % 2) * -30, 60, WHITE, a, 4)
            for k in range(4):
                y0 = cy + 70 + ((x.t * 80 + k * 30) % 90)
                x.line([(cx - 60 + k * 40, y0), (cx - 70 + k * 40, y0 + 25)], CYAN, a, 4, glow=False)
        elif i == 1:
            nodes = [(cx, cy - 80), (cx - 80, cy + 20), (cx + 80, cy + 20), (cx, cy + 110)]
            for p in nodes[1:]:
                x.line([nodes[0], p], WHITE, a, 4, glow=False)
            for k, p in enumerate(nodes):
                x.circle(p[0], p[1], 30, AMBER if k == 0 else CYAN, a, 5)
        else:
            x.rect([cx - 260, cy - 70, cx + 260, cy + 70], WHITE, a, 4, r=6)
            for k in range(6):
                ox = cx - 240 + ((k * 90 + x.t * 60) % 480)
                x.rect([ox, cy - 45, ox + 60, cy + 45], CYAN, a, 3, r=4, glow=False)
        x.text((cx, cy + 170 if i < 2 else cy + 120), nm, "semi", 38, WHITE, a, anchor="mm")


def a_end(x):
    card(x, x.b(0) * 0.5, y=480)
    label_box(x, CX, 880, "a parallel math machine", AMBER, x.b(1), 52)
    label_box(x, CX, 1180, "More on the channel", GREEN, x.b(2), 40)


SCENES = [("GPUs: not just graphics", a_hook), ("Thousands of cores", a_split), ("AI runs on GPUs", a_ai),
          ("Science and video", a_science), ("What a GPU really is", a_end)]
