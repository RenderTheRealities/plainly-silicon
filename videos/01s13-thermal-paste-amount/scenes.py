"""Short 01s13: how much thermal paste (vertical)."""
import math
from render import *  # noqa: F401,F403

SIZE = (1080, 1920)
CX = 540


def h_hook(x):
    a = x.b(0)
    x.rect([200, 640, 760, 780], WHITE, a, 5, r=40)
    x.d.polygon([(760, 660), (880, 690), (880, 730), (760, 760)], outline=col(WHITE, a), width=5)
    x.text((480, 710), "PASTE", "title", 54, WHITE, a, anchor="mm")
    x.text((CX, 1000), "how much?", "title", 72, AMBER, x.b(1), anchor="mm")


def h_gaps(x):
    a = x.b(0)
    top = [(160 + i * 40, 640 + (14 if i % 2 else 0)) for i in range(20)]
    bot = [(160 + i * 40, 760 - (14 if i % 3 == 0 else 0)) for i in range(20)]
    x.line(top, WHITE, a, 5, glow=False)
    x.line(bot, WHITE, a, 5, glow=False)
    x.text((CX, 560), "cooler", "semi", 38, MUTED, a, anchor="mm")
    x.text((CX, 850), "CPU", "semi", 38, MUTED, a, anchor="mm")
    f = x.b(1)
    if f > 0:
        x.d.polygon(top + bot[::-1], fill=col(AMBER, f * 0.6))
    label_box(x, CX, 1050, "paste pushes out the air", AMBER, f, 40)


def h_pea(x):
    a = x.b(0)
    x.rect([270, 560, 810, 1100], WHITE, a, 5, r=14)
    spread = ease(x.since(1) / 1.5) if x.b(1) > 0 else 0
    r = 26 + 210 * spread
    x.circle(CX, 830, r, AMBER, a, 0, fill=AMBER)
    if x.b(1) > 0:
        x.rect([250, 540 - 120 * (1 - spread), 830, 580 - 120 * (1 - spread)], CYAN, x.b(1), 5, r=8)
    x.text((CX, 1180), "pea-sized dot", "title", 52, AMBER, a, anchor="mm")


def h_compare(x):
    for k, (cx, rr, ok, nm) in enumerate([(300, 110, False, "too little"), (780, 260, False, "too much")]):
        a = ease((x.since(0 if k == 0 else 1)) / 0.5)
        x.rect([cx - 170, 630, cx + 170, 970], WHITE, a, 4, r=10)
        if k == 0:
            for j in range(3):
                x.circle(cx - 80 + j * 80, 800, 30, AMBER, a, 0, fill=AMBER)
        else:
            x.circle(cx, 800, 205, AMBER, a, 0, fill=AMBER)
        x.text((cx, 1050), nm, "semi", 40, RED, a, anchor="mm")
    x.text((300, 560), "air gaps", "semi", 32, MUTED, ease(x.since(0) / 0.5), anchor="mm")
    x.text((780, 560), "mess, no gain", "semi", 32, MUTED, ease(x.since(1) / 0.5), anchor="mm")


def h_pre(x):
    a = x.b(0)
    x.rect([270, 560, 810, 1000], CYAN, a, 5, r=14)
    for i in range(3):
        for j in range(3):
            x.rect([340 + i * 150, 630 + j * 120, 440 + i * 150, 700 + j * 120], AMBER, a, 0, r=4, fill=AMBER + (200,), glow=False)
    label_box(x, CX, 1080, "often pre-applied", GREEN, a, 42)
    label_box(x, CX, 1200, "More on the channel", GREEN, x.b(1), 36)


SCENES = [("Thermal paste: how much?", h_hook), ("What paste does", h_gaps), ("The pea method", h_pea),
          ("Too little vs too much", h_compare), ("Check your cooler", h_pre)]
