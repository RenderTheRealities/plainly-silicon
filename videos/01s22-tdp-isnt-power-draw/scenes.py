"""Short 01s22: TDP is a cooling guideline, not the CPU's real power draw (vertical, paper theme)."""
import math
from render import *  # noqa: F401,F403

SIZE = (1080, 1920)
CX = 540


def fan(x, cx, cy, r, c, a, spin=0.0):
    """A simple cooler fan: frame ring, hub and five blades."""
    if a <= 0:
        return
    x.circle(cx, cy, r, c, a, 6, fill=PANEL)
    for k in range(5):
        ang = spin + k * 2 * math.pi / 5
        pts = [(cx, cy)]
        for j in range(7):
            u = ang + j * 0.13
            rr = r * (0.3 + 0.6 * j / 6)
            pts.append((cx + rr * math.cos(u), cy + rr * math.sin(u)))
        for j in range(6, -1, -1):
            u = ang + 0.55 + j * 0.05
            rr = r * (0.3 + 0.55 * j / 6)
            pts.append((cx + rr * math.cos(u), cy + rr * math.sin(u)))
        x.d.polygon(pts, fill=col(c, a * 0.85))
    x.circle(cx, cy, r * 0.22, c, a, 0, fill=c)


def plug(x, cx, cy, c, a):
    """A wall plug: body, two prongs and a cable going down."""
    if a <= 0:
        return
    x.rect([cx - 70, cy - 60, cx + 70, cy + 60], c, a, 6, r=22, fill=PANEL + (255,), glow=False)
    for dx in (-30, 30):
        x.d.rectangle([cx + dx - 9, cy - 120, cx + dx + 9, cy - 60], fill=col(c, a))
    x.line([(cx, cy + 60), (cx, cy + 120), (cx - 60, cy + 170)], c, a, 8, glow=False)


def heat_wave(x, x0, y_bot, y_top, c, a, phase):
    pts = [(x0 + 16 * math.sin(phase + j * 0.7), y_bot - (y_bot - y_top) * j / 12) for j in range(13)]
    x.line(pts, c, a, 7, glow=False)


# ---------- scene 1: the sticker ----------
def s_hook(x):
    a = x.b(0)
    # CPU box with a spec sticker
    x.rect([170, 430, 640, 980], WHITE, a, 6, r=18, fill=PANEL + (255,), glow=False)
    x.d.polygon([(170, 430), (260, 360), (730, 360), (640, 430)], fill=col(GRID, a), outline=col(WHITE, a))
    x.d.polygon([(640, 430), (730, 360), (730, 910), (640, 980)], fill=col(GRID, a), outline=col(WHITE, a))
    chip_icon(x, 405, 590, 120, WHITE, a, 5, pins=5)
    x.rect([220, 760, 590, 930], AMBER, a, 5, r=14, fill=NAVY + (255,), glow=False)
    x.text((405, 810), "TDP", "title", 54, AMBER, a, anchor="mm")
    x.text((405, 885), "125 W", "title", 64, WHITE, a, anchor="mm")
    # a plug with a question: is that the draw?
    plug(x, 870, 640, MUTED, a)
    x.text((870, 470), "?", "title", 110, MUTED, a * (1 - x.b(1)), anchor="mm")
    a1 = x.b(1)
    if a1 > 0:
        fan(x, 860, 1110, 120, CYAN, a1, spin=x.since(1) * 4)
        x.line([(590, 845), (720, 1020)], CYAN, a1, 5, glow=False)
        label_box(x, 405, 1150, "a cooling number", CYAN, a1, 46)


# ---------- scene 2: heat to the cooler, then boost ----------
def s_thermal(x):
    a = x.b(0)
    # chip at the bottom, heatsink fins on top
    x.rect([330, 1000, 750, 1120], WHITE, a, 6, r=14, fill=PANEL + (255,), glow=False)
    x.text((CX, 1060), "CPU", "title", 54, WHITE, a, anchor="mm")
    for k in range(9):
        fx = 330 + k * 52
        x.d.rectangle([fx, 560, fx + 22, 760], fill=col(MUTED, a))
    x.d.rectangle([330, 760, 752, 790], fill=col(MUTED, a))
    a1 = x.b(1)
    for k in range(4):
        heat_wave(x, 400 + k * 95, 990, 810, AMBER, a1, x.t * 6 + k)
    if a1 > 0:
        x.text((140, 900), "heat at", "semi", 36, MUTED, a1, anchor="lm")
        x.text((140, 950), "base speed", "title", 44, AMBER, a1, anchor="lm")
        label_box(x, CX, 480, "cooler sized for this", GREEN, a1, 40)
    a2 = x.b(2)
    if a2 > 0:
        p = ease(x.since(2) / 0.9)
        # boost arrow bursting past the cooler's rated zone
        y = 980 - 520 * p
        x.line([(880, 980), (880, y)], RED, a2, 14, glow=False)
        x.d.polygon([(850, y + 10), (910, y + 10), (880, y - 40)], fill=col(RED, a2))
        x.text((880, 1040), "BOOST", "title", 48, RED, a2, anchor="mm")


# ---------- scene 3: Intel's two figures ----------
def s_intel(x):
    a = x.b(0)
    x.text((CX, 440), "Core i9-14900K", "title", 64, WHITE, a, anchor="mm")
    base, scale = 1180, 2.1  # px per watt
    x.line([(130, base), (950, base)], WHITE, a, 4, glow=False)
    for w_ in (100, 200):
        yy = base - w_ * scale
        for k in range(130, 950, 30):
            x.line([(k, yy), (k + 14, yy)], GRID, a, 3, glow=False)
        x.text((130, yy - 10), f"{w_} W", "semi", 28, MUTED, a, anchor="ld")
    cols = [(1, 300, 125, "base power", CYAN), (1, 720, 253, "max turbo", AMBER)]
    for k, (beat, cx, wv, lab, c) in enumerate(cols):
        ab = x.b(beat)
        if ab <= 0:
            continue
        p = ease((x.since(beat) - k * 0.9) / 1.0)
        if p <= 0:
            continue
        h = wv * scale * p
        x.d.rounded_rectangle([cx - 110, base - h, cx + 110, base], radius=16, fill=col(c, ab))
        x.text((cx, base - h - 50), f"{int(round(wv * p))} W", "title", 66, c, ab, anchor="mm")
        x.text((cx, base + 46), lab, "semi", 38, WHITE, ab, anchor="mm")
    a2 = x.b(2)
    if a2 > 0:
        stamp(x, 510, 760, "2x", RED, a2, angle=-10)


# ---------- scene 4: AMD's dial ----------
def s_amd(x):
    a = x.b(0)
    x.text((CX, 440), "Ryzen 7 7700X", "title", 64, WHITE, a, anchor="mm")
    cx, cy, r = CX, 1000, 380
    vmax = 160.0

    def ang(v):
        return math.pi + math.pi * v / vmax

    # dial arc built from ticks
    for v in range(0, 161, 5):
        u = ang(v)
        r0 = r - (46 if v % 20 == 0 else 24)
        x.line([(cx + r0 * math.cos(u), cy + r0 * math.sin(u)), (cx + r * math.cos(u), cy + r * math.sin(u))],
               WHITE if v % 20 == 0 else MUTED, a, 5 if v % 20 == 0 else 3, glow=False)
    for v in (0, 40, 80, 120, 160):
        u = ang(v)
        x.text((cx + (r + 50) * math.cos(u), cy + (r + 50) * math.sin(u)), str(v), "semi", 30, MUTED, a, anchor="mm")
    x.text((cx, cy - 130), "watts", "semi", 36, MUTED, a, anchor="mm")
    a1 = x.b(1)
    if a1 > 0:
        p1 = ease(x.since(1) / 1.0)
        u = ang(105 * p1)
        x.line([(cx, cy), (cx + (r - 70) * math.cos(u), cy + (r - 70) * math.sin(u))], CYAN, a1, 12, glow=False)
        x.text((cx - 240, cy + 80), "TDP 105", "title", 50, CYAN, a1, anchor="mm")
        # second needle: the real socket limit
        p2 = ease(x.since(2) / 1.0) if x.b(2) > 0 else 0.0
        if p2 > 0:
            u2 = ang(105 + 37 * p2)
            x.line([(cx, cy), (cx + (r - 30) * math.cos(u2), cy + (r - 30) * math.sin(u2))], AMBER, a1, 12, glow=False)
            x.text((cx + 240, cy + 80), "PPT 142", "title", 50, AMBER, a1 * p2, anchor="mm")
    x.circle(cx, cy, 26, WHITE, a, 0, fill=WHITE)


# ---------- scene 5: size for the big number ----------
def s_size(x):
    a = x.b(0)
    # cooler (left) and power supply (right), each with a check
    fan(x, 300, 700, 170, CYAN, a, spin=x.t * 3)
    x.text((300, 920), "cooler", "title", 50, WHITE, a, anchor="mm")
    x.rect([600, 560, 960, 840], WHITE, a, 6, r=18, fill=PANEL + (255,), glow=False)
    x.circle(780, 700, 90, MUTED, a, 5)
    for k in range(6):
        u = k * math.pi / 3 + x.t
        x.line([(780, 700), (780 + 80 * math.cos(u), 700 + 80 * math.sin(u))], MUTED, a, 4, glow=False)
    x.text((780, 920), "power supply", "title", 50, WHITE, a, anchor="mm")
    p = ease(x.since(0) / 1.2)
    rows = [("TDP / base", False, 1050), ("max turbo / PPT", True, 1170)]
    for k, (lab, ok, y) in enumerate(rows):
        ab = a * ease((x.since(0) - 0.6 - k * 0.8) / 0.5)
        if ab <= 0:
            continue
        c = GREEN if ok else RED
        x.rect([150, y - 50, 930, y + 50], c, ab, 5, r=20, fill=PANEL + (255,), glow=False)
        x.text((200, y), lab, "title", 46, WHITE if ok else MUTED, ab, anchor="lm")
        if ok:
            x.line([(840, y), (865, y + 25), (905, y - 25)], GREEN, ab, 9, glow=False)
        else:
            x.line([(845, y - 22), (895, y + 22)], RED, ab, 8, glow=False)
            x.line([(845, y + 22), (895, y - 22)], RED, ab, 8, glow=False)
            x.line([(200, y), (200 + x.d.textlength(safe(lab, "title"), font=font("title", 46)), y)], RED, ab, 5, glow=False)
    _ = p


# ---------- scene 6: outro ----------
def s_end(x):
    a = x.b(0)
    x.rect([140, 520, 940, 1000], WHITE, a, 6, r=26, fill=PANEL + (255,), glow=False)
    x.text((CX, 620), "TDP", "title", 90, CYAN, a, anchor="mm")
    x.text((CX, 710), "= heat to plan for", "semi", 42, MUTED, a, anchor="mm")
    x.line([(220, 770), (860, 770)], GRID, a, 4, glow=False)
    x.text((CX, 850), "Max turbo / PPT", "title", 64, AMBER, a, anchor="mm")
    x.text((CX, 930), "= real peak draw", "semi", 42, MUTED, a, anchor="mm")
    label_box(x, CX, 1150, "More PC hardware on the channel", CYAN, a * ease(x.since(0) / 0.6 - 0.5), 40)


SCENES = [("TDP isn't power draw", s_hook), ("A heat budget", s_thermal), ("Intel: 125 vs 253", s_intel),
          ("AMD: TDP vs PPT", s_amd), ("Buy for the peak", s_size), ("Remember this", s_end)]
