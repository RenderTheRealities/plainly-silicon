"""Short 01s1: every PC part in under a minute (vertical)."""
import math
from render import *  # noqa: F401,F403

SIZE = (1080, 1920)
CX = 540


def p_intro(x):
    parts = ["PSU", "Board", "CPU", "GPU", "SSD", "RAM", "Cooler"]
    for i, nm in enumerate(parts):
        a = ease((x.t - 0.25 * i) / 0.4)
        ang = -math.pi / 2 + i * 2 * math.pi / len(parts) + x.t * 0.15
        px, py = CX + 300 * math.cos(ang), 820 + 300 * math.sin(ang)
        label_box(x, px, py, nm, CYAN, a, 40)
    chip_icon(x, CX, 820, 170, AMBER, x.b(0), 5)
    x.text((CX, 820), "PC", "title", 60, AMBER, x.b(0), anchor="mm")


def p_power(x):
    a = x.b(0)
    x.rect([CX - 220, 450, CX + 220, 700], CYAN, a, 5, r=20, fill=(17, 27, 46, 255))
    x.text((CX, 545), "POWER", "title", 56, CYAN, a, anchor="mm")
    x.text((CX, 615), "SUPPLY", "title", 56, CYAN, a, anchor="mm")
    for j, v in enumerate(["12 V", "5 V", "3.3 V"]):
        aa = a * ease((x.since(0) - 0.8 - j * 0.3) / 0.4)
        y = 760 + j * 60
        x.line([(CX - 180, y), (CX + 120, y)], CYAN, aa, 5)
        x.text((CX + 150, y), v, "monob", 38, CYAN, aa, anchor="lm")
    b = x.b(1)
    x.rect([CX - 300, 980, CX + 300, 1250], WHITE, b, 4, r=14)
    for k, (p0, p1) in enumerate([((CX - 200, 1050), (CX + 200, 1050)), ((CX - 100, 1050), (CX - 100, 1200)), ((CX + 150, 1050), (CX + 150, 1200))]):
        x.line([p0, p1], CYAN, b, 5)
        pp = (x.t * 0.7 + k * 0.33) % 1
        x.circle(p0[0] + (p1[0] - p0[0]) * pp, p0[1] + (p1[1] - p0[1]) * pp, 10, CYAN, b, 0, fill=CYAN)
    x.text((CX, 1285), "motherboard = the roads", "semi", 38, WHITE, b, anchor="mt")


def p_cpu_gpu(x):
    a = x.b(0)
    chip_icon(x, 290, 640, 260, CYAN, a, 5, pins=4)
    for i in range(8):
        r_, c_ = divmod(i, 4)
        lit = 0.4 + 0.6 * (0.5 + 0.5 * math.sin(x.t * 5 + i))
        x.rect([200 + c_ * 48, 570 + r_ * 75, 236 + c_ * 48, 630 + r_ * 75], CYAN, a * lit, 3, r=4,
               fill=(34, 211, 238, int(80 * lit)), glow=False)
    x.text((290, 820), "CPU · 8 cores", "semi", 38, WHITE, a, anchor="mm")
    x.text((800, 600), "billions", "title", 58, AMBER, x.b(1), anchor="mm")
    x.text((800, 665), "of steps / second", "semi", 34, WHITE, x.b(1), anchor="mm")
    g = x.b(2)
    fill = clamp(x.since(2) / 1.5)
    for r_ in range(10):
        for c_ in range(24):
            lit = ((r_ * 7 + c_ * 13) % 100) / 100 < fill
            x.d.rectangle([150 + c_ * 32, 940 + r_ * 30, 175 + c_ * 32, 963 + r_ * 30], fill=col(CYAN, g * (0.9 if lit else 0.18)))
    x.text((CX, 1270), "GPU · thousands of cores", "semi", 38, CYAN, g, anchor="mt")


def p_mem(x):
    a = x.b(0)
    x.rect([140, 460, 500, 880], CYAN, a, 5, r=12)
    for i in range(3):
        x.rect([165, 485 + i * 128, 475, 590 + i * 128], CYAN, a, 3, r=6, glow=False)
    x.text((320, 930), "Storage", "title", 50, CYAN, a, anchor="mm")
    x.text((320, 985), "keeps files", "semi", 34, WHITE, a, anchor="mm")
    b = x.b(2)
    x.rect([600, 640, 960, 690], AMBER, b, 5, r=8)
    x.line([(630, 690), (630, 880)], AMBER, b, 5)
    x.line([(930, 690), (930, 880)], AMBER, b, 5)
    x.text((780, 930), "RAM", "title", 50, AMBER, b, anchor="mm")
    x.text((780, 985), "fast, forgets", "semi", 34, WHITE, b, anchor="mm")
    wipe = x.b(3)
    for i in range(3):
        p = ease((x.since(2) - i * 0.3) / 0.8)
        fx = 330 + (640 + i * 100 - 330) * p
        fy = 520 + i * 128 + (585 - 520 - i * 128) * p - 120 * math.sin(math.pi * p)
        x.rect([fx, fy, fx + 80, fy + 50], WHITE, b * (1 - 0.85 * wipe), 3, r=6, fill=(17, 27, 46, 255), glow=False)
    label_box(x, CX, 1150, "power off → RAM wiped", RED, wipe, 40)


def p_cool(x):
    a = x.b(0)
    cx, cy = CX, 900
    chip_icon(x, cx, cy, 220, CYAN, a, 5)
    for k in range(3):
        ph = (x.t * 0.7 + k / 3) % 1.0
        y = cy - 150 - ph * 220
        pts = [(cx - 100 + i * 8, y + 12 * math.sin(i * 0.5 + x.t * 4)) for i in range(26)]
        x.line(pts, AMBER, a * (1 - ph), 4)
    fcx, fcy = cx, 520
    x.circle(fcx, fcy, 100, CYAN, a, 5)
    for k in range(4):
        ang = x.t * 10 + k * math.pi / 2
        x.line([(fcx, fcy), (fcx + 88 * math.cos(ang), fcy + 88 * math.sin(ang))], CYAN, a, 5, glow=False)
    label_box(x, CX, 1180, "Full video on the channel", GREEN, x.b(2), 42)


SCENES = [("Every PC part, fast", p_intro), ("Power + motherboard", p_power), ("CPU + GPU", p_cpu_gpu),
          ("Storage + RAM", p_mem), ("Cooling", p_cool)]
