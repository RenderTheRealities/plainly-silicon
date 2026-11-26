"""Short 31s1: GTA 6 runs at 30 fps on PS5 (vertical, sunset theme). Teases 31-can-your-pc-run-gta-6.

Design language: a neon "frame counter" HUD on a sunset gradient. Scene 1 smashes a 60 into a 30;
scene 2 is three stacked stat plates; scene 3 is a top-down city grid with dots for people and cars
streaming into a red-hot CPU chip while the GPU chip idles; scene 4 is two pairs of growth bars
(GPU vs CPU, PS5 -> PS5 Pro); scene 5 is a calendar page with a question mark; scene 6 is an end card.
"""
import math
from render import *  # noqa: F401,F403

SIZE = (1080, 1920)
CX = 540


def hud_number(x, cx, cy, s, size, c, a):
    if a <= 0:
        return
    x.text((cx, cy), s, "brand", size, c, a, anchor="mm")


# ---------- 1. the hook: 60 becomes 30 ----------
def s_hook(x):
    a = x.b(0)
    x.rect([170, 470, 910, 1090], WHITE, a, 6, r=40, fill=PANEL + (255,))
    x.text((CX, 540), "FPS", "semi", 46, MUTED, a, anchor="mm")
    p = ease(x.since(0) / 1.4)
    if p < 0.55:
        hud_number(x, CX, 790, "60", 330, GREEN, a)
    else:
        hud_number(x, CX, 790, "30", 330, AMBER, a)
    if 0.35 < p < 0.75:
        x.line([(230, 1000), (850, 560)], RED, a, 16)
    label_box(x, CX, 1180, "PS5 Pro", WHITE, a, 44)


# ---------- 2. Digital Foundry's numbers ----------
def s_numbers(x):
    rows = [("30 FPS cap", "both PS5 models", AMBER), ("~1440p", "internal resolution", CYAN), ("No 60 mode", "no performance mode", RED)]
    for i, (big, small, c) in enumerate(rows):
        a = x.b(0) * ease((x.since(0) - i * 1.6) / 0.4)
        y = 470 + i * 260
        x.rect([120, y, 960, y + 220], c, a, 5, r=30, fill=PANEL + (255,))
        x.text((170, y + 80), big, "brand", 84, c, a, anchor="lm")
        x.text((172, y + 165), small, "semi", 40, WHITE, a, anchor="lm")
    x.text((CX, 1250), "source: Digital Foundry, Nov 2026", "semi", 30, MUTED, x.b(0), anchor="mm")


# ---------- 3. the CPU is the wall ----------
def s_cpu(x):
    a0 = x.b(0)
    # top-down city grid
    for k in range(5):
        yy = 440 + k * 70
        x.line([(110, yy), (970, yy)], MUTED, a0 * 0.5, 3, glow=False)
    for k in range(7):
        xx = 140 + k * 135
        x.line([(xx, 440), (xx, 720)], MUTED, a0 * 0.5, 3, glow=False)
    a1 = x.b(1)
    for k in range(26):
        t = (x.since(1) * 0.45 + k / 26) % 1
        sx = 140 + (k * 97) % 810
        sy = 450 + (k * 53) % 260
        px = sx + (300 - sx) * t
        py = sy + (1010 - sy) * t
        x.circle(px, py, 9, AMBER if k % 3 else CYAN, a1 * (1 - t * 0.6), 0, fill=AMBER if k % 3 else CYAN)
    heat = 0.6 + 0.4 * math.sin(x.t * 6)
    chip_icon(x, 300, 1060, 230, RED, a1 * heat, 6, pins=5)
    x.text((300, 1060), "CPU", "brand", 64, RED, a1, anchor="mm")
    x.text((300, 1240), "8 Zen 2 cores", "semi", 38, WHITE, x.b(2), anchor="mm")
    chip_icon(x, 790, 1060, 200, GREEN, a1 * 0.8, 5, pins=5)
    x.text((790, 1060), "GPU", "brand", 56, GREEN, a1, anchor="mm")
    x.text((790, 1240), "waiting", "semi", 38, MUTED, x.b(2), anchor="mm")


# ---------- 4. PS5 vs PS5 Pro ----------
def s_pro(x):
    a0 = x.b(0)
    x.text((CX, 450), "PS5  ->  PS5 Pro", "brand", 64, WHITE, a0, anchor="mm")
    base, top = 1150, 560
    for k, (lbl, gain, c) in enumerate([("GPU", 0.95, GREEN), ("CPU", 0.10, RED)]):
        cx0 = 250 + k * 420
        h0 = 260
        h1 = h0 * (1 + gain * ease(x.since(0) / 1.5))
        x.d.rounded_rectangle([cx0 - 70, base - h0, cx0 + 10, base], radius=12, fill=col(MUTED, a0))
        x.d.rounded_rectangle([cx0 + 30, base - h1, cx0 + 110, base], radius=12, fill=col(c, a0))
        x.text((cx0 + 20, base + 50), lbl, "brand", 56, c, a0, anchor="mm")
    x.text((670, base - 330), "+10%", "brand", 64, RED, x.b(0), anchor="mm")
    x.text((290, top - 20), "much bigger", "semi", 36, GREEN, a0, anchor="mm")
    label_box(x, CX, 1300, "still 30 FPS", AMBER, x.b(1), 46)


# ---------- 5. the PC version ----------
def s_pc(x):
    a0 = x.b(0)
    x.rect([280, 450, 800, 930], WHITE, a0, 6, r=30, fill=PANEL + (255,))
    x.d.rounded_rectangle([280, 450, 800, 560], radius=30, fill=col(RED, a0))
    x.text((CX, 505), "PC RELEASE", "brand", 46, WHITE, a0, anchor="mm")
    x.text((CX, 690), "?", "brand", 220, AMBER, a0, anchor="mm")
    x.text((CX, 860), "not announced", "semi", 40, MUTED, a0, anchor="mm")
    label_box(x, CX, 1010, "report: early 2027", CYAN, x.b(1), 44)
    a2 = x.b(2)
    x.text((CX, 1140), "2x console speed", "brand", 60, WHITE, a2, anchor="mm")
    x.text((CX, 1215), "may still miss 60 in crowds", "semi", 40, RED, a2, anchor="mm")


# ---------- 6. end card ----------
def s_end(x):
    a0 = x.b(0)
    x.text((CX, 560), "Can your PC", "brand", 92, WHITE, a0, anchor="mm")
    x.text((CX, 670), "run GTA 6?", "brand", 92, AMBER, a0, anchor="mm")
    p = ease(x.since(1) / 0.6)
    x.rect([250, 800, 830, 960], CYAN, x.b(1), 6, r=40, fill=PANEL + (255,))
    x.text((CX, 880), "MONDAY", "brand", 96, CYAN, x.b(1) * p, anchor="mm")
    x.text((CX, 1050), "full breakdown", "semi", 44, MUTED, x.b(1), anchor="mm")


SCENES = [
    ("Even PS5 Pro: no 60", s_hook),
    ("Digital Foundry's numbers", s_numbers),
    ("The real bottleneck", s_cpu),
    ("PS5 Pro: GPU, not CPU", s_pro),
    ("And on PC?", s_pc),
    ("Full breakdown Monday", s_end),
]
