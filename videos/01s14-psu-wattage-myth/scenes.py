"""Short 01s14: what PSU wattage really means (vertical)."""
import math
from render import *  # noqa: F401,F403

SIZE = (1080, 1920)
CX = 540


def psu(x, a, y=500):
    x.rect([220, y, 860, y + 300], WHITE, a, 6, r=14, fill=PANEL + (255,))
    x.circle(400, y + 150, 100, WHITE, a, 4)
    x.text((690, y + 150), "850 W", "title", 70, CYAN, a, anchor="mm")


def i_hook(x):
    psu(x, x.b(0))
    x.text((CX, 1000), "≠ 850 W used", "title", 72, AMBER, x.b(1), anchor="mm")


def gauge(x, a, frac, label):
    cx, cy, r = CX, 950, 320
    pts = [(cx + r * math.cos(math.pi + math.pi * i / 40), cy + r * math.sin(math.pi + math.pi * i / 40)) for i in range(41)]
    x.line(pts, MUTED, a, 10, glow=False)
    k = int(40 * frac)
    if k:
        x.line(pts[:k + 1], CYAN, a, 14)
    ang = math.pi + math.pi * frac
    x.line([(cx, cy), (cx + (r - 50) * math.cos(ang), cy + (r - 50) * math.sin(ang))], AMBER, a, 8)
    x.text((cx, cy + 90), label, "monob", 56, WHITE, a, anchor="mm")


def i_max(x):
    gauge(x, x.b(0), 1.0, "850 W max")
    label_box(x, CX, 1180, "a limit, not a draw", AMBER, x.b(1), 40)


def i_draw(x):
    f = 300 / 850 * ease(x.since(1) / 1.5) if x.b(1) > 0 else 0.05
    gauge(x, x.b(0), f, f"{int(f * 850)} W")
    label_box(x, CX, 1180, "parts take what they need", GREEN, x.b(0), 38)


def i_eff(x):
    a = x.b(0)
    x0, y0, w, h = 160, 520, 760, 520
    x.line([(x0, y0), (x0, y0 + h), (x0 + w, y0 + h)], WHITE, a, 4, glow=False)
    pts = []
    for i in range(41):
        load = i / 40
        eff = 0.80 + 0.12 * math.exp(-((load - 0.5) / 0.35) ** 2) - (0.12 if load < 0.1 else 0) * (0.1 - load) * 10
        pts.append((x0 + w * load, y0 + h - (eff - 0.6) / 0.4 * h))
    k = max(2, int(41 * ease(x.since(0) / 1.5)))
    x.line(pts[:k], CYAN, a, 7)
    x.text((x0 + w / 2, y0 + h + 50), "load →", "semi", 34, MUTED, a, anchor="mm")
    x.text((x0 - 10, y0 + 20), "efficiency", "semi", 30, MUTED, a, anchor="lm")
    x.line([(x0 + w / 2, y0 + 40), (x0 + w / 2, y0 + h)], AMBER, x.b(0) * ease(x.since(0) / 0.5 - 2), 3, glow=False)
    label_box(x, CX, 1190, "best near half load", AMBER, x.b(1), 38)


def i_end(x):
    psu(x, x.b(0) * 0.6, y=480)
    label_box(x, CX, 930, "bill: barely changes", GREEN, x.b(0), 42)
    label_box(x, CX, 1060, "way too big: costs more up front", AMBER, x.b(1), 34)
    label_box(x, CX, 1190, "More on the channel", GREEN, x.b(2), 36)


SCENES = [("850 W isn't 850 W", i_hook), ("It's a maximum", i_max), ("Parts draw what they need", i_draw),
          ("The efficiency sweet spot", i_eff), ("So what to buy?", i_end)]
