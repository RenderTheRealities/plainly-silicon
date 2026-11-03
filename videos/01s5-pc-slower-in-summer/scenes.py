"""Short 01s5: why your PC gets slower in summer (vertical)."""
import math
from render import *  # noqa: F401,F403

SIZE = (1080, 1920)
CX = 540


def sun(x, cx, cy, a):
    x.circle(cx, cy, 90, AMBER, a, 6)
    for k in range(12):
        ang = k * math.pi / 6 + x.t * 0.5
        x.line([(cx + 115 * math.cos(ang), cy + 115 * math.sin(ang)), (cx + 160 * math.cos(ang), cy + 160 * math.sin(ang))], AMBER, a, 6)


def h_hook(x):
    sun(x, CX, 700, x.b(0))
    x.text((CX, 1040), "slower on hot days?", "title", 56, WHITE, x.b(0), anchor="mm")
    x.text((CX, 1120), "you're not imagining it", "semi", 40, AMBER, x.b(1), anchor="mm")


def heat_chip(x, cy, a):
    chip_icon(x, CX, cy, 240, CYAN, a, 5)
    for k in range(3):
        ph = (x.t * 0.7 + k / 3) % 1.0
        y = cy - 160 - ph * 220
        pts = [(CX - 100 + i * 8, y + 12 * math.sin(i * 0.5 + x.t * 4)) for i in range(26)]
        x.line(pts, AMBER, a * (1 - ph), 5)


def h_heat(x):
    heat_chip(x, 860, x.b(0))
    x.text((CX, 1120), "100+ W of heat", "title", 60, AMBER, x.b(0), anchor="mm")
    x.text((CX, 1190), "in a chip smaller than a cracker", "semi", 38, WHITE, x.b(0), anchor="mm")


def h_cool(x):
    a = x.b(0)
    cy = 950
    chip_icon(x, CX, cy, 200, CYAN, a, 5)
    x.rect([CX - 120, cy - 135, CX + 120, cy - 120], WHITE, x.b(1), 3, r=3, glow=False, fill=WHITE + (255,))
    for i in range(9):
        fx = CX - 120 + i * 30
        x.line([(fx, cy - 150), (fx, cy - 320)], CYAN, x.b(1), 5, glow=False)
    fcx, fcy = CX, 480
    x.circle(fcx, fcy, 90, CYAN, x.b(1), 5)
    for k in range(4):
        ang = x.t * 10 + k * math.pi / 2
        x.line([(fcx, fcy), (fcx + 80 * math.cos(ang), fcy + 80 * math.sin(ang))], CYAN, x.b(1), 5, glow=False)
    x.text((CX, 1150), "paste → fins → fans", "title", 50, WHITE, x.b(1), anchor="mm")


def h_throttle(x):
    a = x.b(0)
    th = ease(x.since(1) / 2.5) if x.b(1) > 0 else 0
    temp = 0.5 + 0.48 * th
    bar(x, 140, 620, 800, temp, RED if temp > 0.85 else AMBER, a, 44, "Temperature", f"{int(60 + 40 * th)}°C")
    bar(x, 140, 820, 800, 1 - 0.35 * th, CYAN, a, 44, "Clock speed", f"{4.8 - 1.6 * th:0.1f} GHz")
    label_box(x, CX, 1050, "thermal throttling", RED, x.b(2), 52)


def h_end(x):
    label_box(x, CX, 620, "clean dusty fans", GREEN, x.b(0), 50)
    label_box(x, CX, 780, "give the case room", GREEN, ease((x.since(0) - 0.6) / 0.4), 50)
    label_box(x, CX, 1180, "Full video on the channel", GREEN, x.b(1), 42)


SCENES = [("Hot day, slow PC", h_hook), ("Where the heat comes from", h_heat), ("How cooling works", h_cool),
          ("Thermal throttling", h_throttle), ("The fix", h_end)]
