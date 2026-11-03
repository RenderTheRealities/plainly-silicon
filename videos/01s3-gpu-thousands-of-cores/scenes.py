"""Short 01s3: why a GPU has thousands of cores (vertical)."""
import math
from render import *  # noqa: F401,F403

SIZE = (1080, 1920)
CX = 540


def g_hook(x):
    a = x.b(0)
    x.text((300, 620), "8", "title", 200, WHITE, a, anchor="mm")
    x.text((300, 760), "CPU cores", "semi", 40, WHITE, a, anchor="mm")
    b = x.b(1)
    x.text((780, 620), "1000s", "title", 150, CYAN, b, anchor="mm")
    x.text((780, 760), "GPU cores", "semi", 40, CYAN, b, anchor="mm")
    x.text((CX, 1050), "so who's in charge?", "title", 54, AMBER, x.b(2), anchor="mm")


def g_cpu(x):
    a = x.b(0)
    for i in range(8):
        r_, c_ = divmod(i, 4)
        x0, y0 = 170 + c_ * 190, 520 + r_ * 220
        lit = 0.5 + 0.5 * math.sin(x.t * 3 + i)
        x.rect([x0, y0, x0 + 160, y0 + 180], WHITE, a, 4, r=14, fill=(229, 231, 235, int(40 * lit)))
    x.text((CX, 1020), "a few expert workers", "title", 52, WHITE, x.b(1), anchor="mm")
    x.text((CX, 1090), "fast · clever · step by step", "semi", 36, MUTED, x.b(1), anchor="mm")


def g_crowd(x):
    a = x.b(0)
    for r_ in range(16):
        for c_ in range(24):
            x.d.rectangle([150 + c_ * 32, 480 + r_ * 32, 175 + c_ * 32, 505 + r_ * 32], fill=col(CYAN, a * 0.35))
    x.text((CX, 1080), "a huge crowd of simple workers", "title", 46, CYAN, x.b(1), anchor="mm")


def g_fill(x):
    a = x.b(0)
    fill = clamp(x.since(1) / 1.6) if x.b(1) > 0 else 0
    for r_ in range(16):
        for c_ in range(24):
            lit = ((r_ * 7 + c_ * 13) % 100) / 100 < fill
            x.d.rectangle([150 + c_ * 32, 480 + r_ * 32, 175 + c_ * 32, 505 + r_ * 32],
                          fill=col(CYAN if lit else MUTED, a * (0.95 if lit else 0.25)))
    x.text((CX, 1080), "every pixel at the same time", "title", 46, WHITE, x.b(1), anchor="mm")


def g_end(x):
    a = x.b(0)
    label_box(x, CX, 640, "GPU → frame rate", CYAN, a, 54)
    label_box(x, CX, 800, "CPU → everything else", WHITE, ease((x.since(0) - 0.6) / 0.4), 54)
    label_box(x, CX, 1180, "Full video on the channel", GREEN, x.b(1), 42)


SCENES = [("CPU vs GPU cores", g_hook), ("CPU: the experts", g_cpu), ("GPU: the crowd", g_crowd),
          ("Drawing a frame", g_fill), ("Who does what", g_end)]
