"""Short 08s1: Ultra vs High presets (vertical, sunset theme).
Design language: a settings-menu look (dropdowns, toggles, sliders) next to a tiny drawn skyline
"screenshot" and round FPS dials. No conveyor belts or chips."""
import math
from render import *  # noqa: F401,F403

SIZE = (1080, 1920)
CX = 540


def dropdown(x, cx, cy, w, label, value, c, a, open_=0.0):
    x.rect([cx - w / 2, cy - 50, cx + w / 2, cy + 50], c, a, 4, r=50, fill=PANEL + (255,))
    x.text((cx - w / 2 + 40, cy), label, "semi", 38, MUTED, a, anchor="lm")
    x.text((cx + w / 2 - 90, cy), value, "title", 46, c, a, anchor="rm")
    # chevron
    x.line([(cx + w / 2 - 66, cy - 10), (cx + w / 2 - 50, cy + 8), (cx + w / 2 - 34, cy - 10)], c, a, 5, glow=False)


def dial(x, cx, cy, r, val, vmax, c, a, label=""):
    """Half-ring FPS gauge."""
    if a <= 0:
        return
    box = [cx - r, cy - r, cx + r, cy + r]
    x.d.arc(box, 180, 360, fill=col(GRID, a), width=26)
    frac = clamp(val / vmax)
    if frac > 0:
        x.d.arc(box, 180, 180 + 180 * frac, fill=col(c, a), width=26)
    x.text((cx, cy - 20), f"{val:.0f}", "title", int(r * 0.55), WHITE, a, anchor="mb")
    if label:
        x.text((cx, cy + 20), label, "semi", 34, MUTED, a, anchor="mt")


def skyline(x, x0, y0, w, h, a, detail=1.0, fog=0.0, people=6):
    """Tiny stylized city 'screenshot'."""
    if a <= 0:
        return
    x.rect([x0, y0, x0 + w, y0 + h], WHITE, a, 4, r=16, fill=NAVY + (255,), glow=False)
    # sky gradient band
    x.d.rectangle([x0 + 4, y0 + 4, x0 + w - 4, y0 + h * 0.55], fill=col(PANEL, a))
    x.circle(x0 + w * 0.78, y0 + h * 0.22, h * 0.09, AMBER, a, 0, fill=AMBER)
    bw = w / 7
    for i in range(7):
        bh = h * (0.28 + 0.32 * ((i * 37) % 10) / 10)
        bx = x0 + 10 + i * bw
        x.d.rectangle([bx, y0 + h * 0.8 - bh, bx + bw - 12, y0 + h * 0.8], fill=col(CYAN, a * 0.85))
        for wy in range(int(y0 + h * 0.8 - bh + 14), int(y0 + h * 0.8 - 10), 26):
            x.d.rectangle([bx + 10, wy, bx + 22, wy + 10], fill=col(AMBER, a * 0.7))
    # street with reflections
    x.d.rectangle([x0 + 4, y0 + h * 0.8, x0 + w - 4, y0 + h - 4], fill=col(GRID, a))
    if detail > 0:
        for i in range(7):
            bx = x0 + 10 + i * bw
            x.d.rectangle([bx + 6, y0 + h * 0.83, bx + bw - 18, y0 + h * 0.86], fill=col(CYAN, a * 0.35 * detail))
    for k in range(people):
        px = x0 + 30 + k * (w - 60) / max(1, people - 1)
        x.circle(px, y0 + h * 0.9, 7, WHITE, a, 0, fill=WHITE)
    if fog > 0:
        x.d.rectangle([x0 + 4, y0 + h * 0.45, x0 + w - 4, y0 + h * 0.8], fill=col(MUTED, a * fog))


# 1. hook: the preset dropdown flips and the dial jumps
def s_hook(x):
    a = x.b(0)
    flip = ease((x.since(0) - 2.0) / 0.6)
    dropdown(x, CX, 520, 820, "Preset", "ULTRA" if flip < 0.5 else "HIGH", AMBER if flip < 0.5 else CYAN, a)
    fps = 100 + 24 * flip
    dial(x, CX, 960, 250, fps, 140, CYAN, a, "relative FPS")
    if flip > 0:
        label_box(x, CX, 1150, "+24%", GREEN, flip, 56)


# 2. the test: two bars, then two near-identical screenshots
def s_test(x):
    a = x.b(0)
    x.text((CX, 440), "Cyberpunk 2077 · TechSpot", "semi", 40, MUTED, a, anchor="mm")
    g = ease(x.since(1) / 1.0) if x.b(1) > 0 else 0
    for i, (nm, v, c) in enumerate([("Ultra", 100, AMBER), ("High", 124, CYAN)]):
        bx = 300 + i * 300
        hh = 300 * (v / 124) * g
        x.d.rounded_rectangle([bx - 70, 820 - hh, bx + 70, 820], radius=14, fill=col(c, a))
        x.text((bx, 850), nm, "title", 44, WHITE, a, anchor="mt")
        if g > 0.9:
            x.text((bx, 800 - hh), f"{v}", "title", 44, c, a, anchor="mb")
    b = x.b(2)
    skyline(x, 70, 960, 440, 280, b, detail=1.0, fog=0.0, people=7)
    skyline(x, 570, 960, 440, 280, b, detail=0.6, fog=0.08, people=5)
    x.text((540, 1100), "≈", "title", 80, WHITE, b, anchor="mm")


# 3. what Ultra adds: three sliders step down, then pause vs motion
def s_adds(x):
    a = x.b(0)
    rows = ["Reflections", "Fog", "Crowd size"]
    for i, nm in enumerate(rows):
        aa = ease((x.since(1) - i * 0.4) / 0.5) if x.b(1) > 0 else 0
        y = 470 + i * 130
        x.text((90, y), nm, "semi", 40, WHITE, a, anchor="lm")
        x.line([(520, y), (990, y)], GRID, a, 10, glow=False)
        pos = 990 - 130 * aa
        x.line([(520, y), (pos, y)], CYAN, a, 10, glow=False)
        x.circle(pos, y, 24, CYAN, a, 0, fill=WHITE)
        x.text((990, y - 44), "Ultra" if aa < 0.5 else "High", "semi", 30, AMBER if aa < 0.5 else CYAN, a, anchor="rm")
    b = x.b(2)
    # paused screenshot vs moving scene
    skyline(x, 70, 900, 430, 300, b, people=6)
    if b > 0:
        x.circle(285, 1050, 62, WHITE, b, 4, fill=NAVY)
        x.d.rectangle([260, 1020, 278, 1080], fill=col(WHITE, b))
        x.d.rectangle([292, 1020, 310, 1080], fill=col(WHITE, b))
    off = (x.t * 400) % 120
    skyline(x, 580, 900, 430, 300, b, people=6)
    for k in range(6):
        yy = 930 + k * 45
        x.line([(600 + off, yy), (680 + off, yy)], WHITE, b * 0.8, 6, glow=False)
    x.text((285, 1235), "paused: visible", "semi", 34, MUTED, b, anchor="mm")
    x.text((795, 1235), "mid fight: gone", "semi", 34, MUTED, b, anchor="mm")


# 4. the gain varies: three horizontal results
def s_varies(x):
    a = x.b(0)
    data = [("Cyberpunk, original", 0.24, "+24%", 0), ("Cyberpunk, newer version", 0.14, "+14%", 1),
            ("Presets that differ little", 0.02, "tiny", 2)]
    for i, (nm, v, s, beat) in enumerate(data):
        aa = x.b(beat)
        grow = ease(x.since(beat) / 0.8)
        y = 560 + i * 230
        x.text((90, y - 50), nm, "semi", 40, WHITE, aa, anchor="ls")
        x.d.rounded_rectangle([90, y, 990, y + 70], radius=35, fill=col(GRID, aa))
        x.d.rounded_rectangle([90, y, 90 + max(70, 900 * v / 0.3 * grow), y + 70], radius=35, fill=col(CYAN if i < 2 else MUTED, aa))
        x.text((990, y - 50), s, "title", 46, AMBER, aa, anchor="rs")


# 5. the recipe: two numbered cards and a memory meter
def s_recipe(x):
    a = x.b(0)
    x.rect([90, 450, 990, 680], CYAN, a, 5, r=30, fill=PANEL + (255,))
    x.circle(190, 565, 55, CYAN, a, 0, fill=CYAN)
    x.text((190, 565), "1", "title", 64, NAVY, a, anchor="mm")
    x.text((290, 565), "Preset: High", "title", 58, WHITE, a, anchor="lm")
    b = ease((x.since(0) - 1.6) / 0.5)
    x.rect([90, 740, 990, 970], AMBER, b, 5, r=30, fill=PANEL + (255,))
    x.circle(190, 855, 55, AMBER, b, 0, fill=AMBER)
    x.text((190, 855), "2", "title", 64, NAVY, b, anchor="mm")
    x.text((290, 855), "Textures: back up", "title", 54, WHITE, b, anchor="lm")
    m = ease((x.since(0) - 2.6) / 1.2)
    if b > 0:
        x.text((90, 1060), "graphics memory", "semi", 36, MUTED, b, anchor="ls")
        x.d.rounded_rectangle([90, 1080, 990, 1150], radius=20, outline=col(WHITE, b), width=4)
        x.d.rounded_rectangle([98, 1088, 98 + 600 * m, 1142], radius=14, fill=col(GREEN, b))
        x.text((990, 1200), "fits? keep it", "semi", 38, GREEN, m, anchor="rm")


# 6. outro: dial from 48 to mid 80s
def s_outro(x):
    a = x.b(0)
    v = 48 + 37 * ease(x.since(0) / 2.5)
    dial(x, CX, 840, 280, v, 120, CYAN, a, "FPS")
    x.text((CX, 1090), "What Actually Raises FPS", "title", 56, AMBER, a, anchor="mm")
    x.text((CX, 1170), "full video on the channel", "semi", 38, MUTED, a, anchor="mm")


SCENES = [
    ("Ultra -> High", s_hook),
    ("The Cyberpunk test", s_test),
    ("What Ultra adds", s_adds),
    ("It depends on the game", s_varies),
    ("The 2-step recipe", s_recipe),
    ("The full video", s_outro),
]
