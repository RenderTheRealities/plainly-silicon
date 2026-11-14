"""Short 06s1: CPU cache levels as distance rings around one core (vertical, ember theme)."""
import math
from render import *  # noqa: F401,F403

SIZE = (1080, 1920)
CX, CY = 540, 830
RINGS = [(120, "L1", "4"), (225, "L2", "14"), (340, "L3", "50")]


def core(x, a, pulse=0.0):
    """The CPU core at the center of the map."""
    if a <= 0:
        return
    r = 62 + 6 * math.sin(pulse)
    x.circle(CX, CY, r, CYAN, a, 6, fill=PANEL)
    x.text((CX, CY), "CORE", "title", 34, WHITE, a, anchor="mm")


def ring(x, i, c, a, dash=False, label=True):
    r, name, cyc = RINGS[i]
    if a <= 0:
        return
    if dash:
        n = 48
        for k in range(n):
            if k % 2:
                continue
            u0, u1 = 2 * math.pi * k / n, 2 * math.pi * (k + 1) / n
            x.d.arc([CX - r, CY - r, CX + r, CY + r], math.degrees(u0), math.degrees(u1), fill=col(c, a), width=5)
    else:
        x.circle(CX, CY, r, c, a, 7)
    if label:
        # tag sits on the ring at the upper-right
        u = -math.pi / 4
        tx, ty = CX + r * math.cos(u), CY + r * math.sin(u)
        x.rect([tx - 46, ty - 30, tx + 46, ty + 30], c, a, 4, r=14, fill=NAVY + (255,), glow=False)
        x.text((tx, ty), name, "title", 36, c, a, anchor="mm")


def packet(x, r, p, c, a, ang=math.pi * 0.75):
    """A data dot travelling from radius r in to the core, progress p 0..1."""
    if a <= 0 or p <= 0:
        return
    rr = r - (r - 70) * clamp(p)
    px, py = CX + rr * math.cos(ang), CY + rr * math.sin(ang)
    x.line([(CX + r * math.cos(ang), CY + r * math.sin(ang)), (px, py)], AMBER, a * 0.6, 5, glow=False)
    x.circle(px, py, 20, AMBER, a, 0, fill=AMBER)


def counter(x, y, value, c, a, unit="cycles"):
    x.text((CX, y), f"{int(value)}", "title", 120, c, a, anchor="mm")
    x.text((CX, y + 80), unit, "semi", 40, MUTED, a, anchor="mm")


# ---------- scene 1: the long wait ----------
def s_hook(x):
    a = x.b(0)
    # core at top, RAM stick far below, a long dotted road between
    x.circle(CX, 470, 60, CYAN, a, 6, fill=PANEL)
    x.text((CX, 470), "CORE", "title", 32, WHITE, a, anchor="mm")
    x.rect([300, 1130, 780, 1210], WHITE, a, 5, r=10, fill=PANEL + (255,), glow=False)
    for k in range(8):
        x.d.rectangle([325 + k * 57, 1148, 365 + k * 57, 1192], fill=col(MUTED, a))
    x.text((CX, 1240), "RAM", "title", 34, WHITE, a, anchor="mm")
    for yy in range(545, 1120, 34):
        x.circle(CX, yy, 5, MUTED, a, 0, fill=MUTED)
    p = clamp(x.since(0) / 3.2)
    if a > 0:
        # packet crawls up from the RAM, counter ticks
        py = 1110 - (1110 - 545) * ease(p)
        x.circle(CX, py, 22, AMBER, a, 0, fill=AMBER)
        x.text((850, 760), f"{int(365 * p)}", "title", 96, AMBER, a, anchor="mm")
        x.text((850, 830), "cycles", "semi", 38, MUTED, a, anchor="mm")
        x.text((230, 760), "waiting", "semi", 40, MUTED, a * (0.5 + 0.5 * math.sin(x.t * 5)), anchor="mm")
    a1 = x.b(1)
    if a1 > 0:
        # tiny memories appear around the core
        for k, rr in enumerate((90, 120, 150)):
            x.circle(CX, 470, rr, CYAN, a1 * (1 - k * 0.25), 4)


# ---------- scene 2: level one ----------
def s_l1(x):
    a = x.b(0)
    core(x, a, x.t * 3)
    x.text((CX, 430), "AMD Zen 4 core", "title", 56, WHITE, a, anchor="mm")
    a1 = x.b(1)
    ring(x, 0, CYAN, a1)
    a2 = x.b(2)
    if a2 > 0:
        cyc = (x.since(2) % 1.4) / 0.5
        packet(x, 120, cyc, CYAN, a2)
        x.text((CX, 1100), "32 KB", "title", 80, WHITE, a2, anchor="mm")
        x.text((CX, 1190), "about 4 cycles", "semi", 46, GREEN, a2, anchor="mm")


# ---------- scene 3: level two ----------
def s_l2(x):
    a = x.b(0)
    core(x, a, x.t * 3)
    ring(x, 0, MUTED, a, label=True)
    ring(x, 1, CYAN, a)
    # a red X on L1: the miss
    u = math.pi * 0.25
    mx, my = CX + 120 * math.cos(u), CY + 120 * math.sin(u)
    x.line([(mx - 22, my - 22), (mx + 22, my + 22)], RED, a, 8, glow=False)
    x.line([(mx - 22, my + 22), (mx + 22, my - 22)], RED, a, 8, glow=False)
    x.text((CX, 430), "miss L1? check L2", "title", 52, WHITE, a, anchor="mm")
    a1 = x.b(1)
    if a1 > 0:
        packet(x, 225, (x.since(1) % 2.0) / 1.2, CYAN, a1)
        x.text((240, 1215), "1 MB", "title", 64, WHITE, a1, anchor="mm")
        x.text((800, 1215), "~14 cycles", "title", 58, AMBER, a1, anchor="mm")


# ---------- scene 4: level three, shared ----------
def s_l3(x):
    a = x.b(0)
    for i in (0, 1):
        ring(x, i, MUTED, a)
    ring(x, 2, CYAN, a)
    core(x, a, x.t * 3)
    # neighbour cores sitting on the shared L3
    for k in range(6):
        u = k * math.pi / 3 + math.pi / 6
        nx, ny = CX + 410 * math.cos(u), CY + 410 * math.sin(u) * 0.95
        if abs(math.sin(u)) < 0.9:
            chip_icon(x, nx, ny, 54, MUTED, a * ease(x.since(0) / 0.8 - k * 0.1), 3, pins=3)
    x.text((CX, 405), "shared by the cores", "semi", 44, WHITE, a, anchor="mm")
    a1 = x.b(1)
    if a1 > 0:
        packet(x, 340, (x.since(1) % 2.4) / 1.8, CYAN, a1, ang=math.pi * 0.5)
        label_box(x, CX, 1235, "roughly 50 cycles", AMBER, a1, 46)


# ---------- scene 5: RAM, a hundred times further ----------
def s_ram(x):
    a = x.b(0)
    x.text((CX, 440), "time to get one value", "semi", 44, MUTED, a, anchor="mm")
    rows = [("L1", 4, GREEN), ("L2", 14, CYAN), ("L3", 50, AMBER), ("RAM", 365, RED)]
    x0, wmax, vmax = 230, 760, 365.0
    for k, (lab, v, c) in enumerate(rows):
        y = 560 + k * 150
        ab = a * ease((x.since(0) - k * 0.35) / 0.5)
        if ab <= 0:
            continue
        grow = ease((x.since(0) - k * 0.35) / (1.6 if lab == "RAM" else 0.6))
        x.text((x0 - 30, y + 30), lab, "title", 50, WHITE, ab, anchor="rm")
        w_ = max(30, wmax * v / vmax * grow)
        x.d.rounded_rectangle([x0, y, x0 + w_, y + 60], radius=30, fill=col(c, ab))
        if lab == "RAM":
            x.text((x0 + w_ - 30, y + 30), f"{int(v * grow)}", "title", 44, NAVY, ab, anchor="rm")
        else:
            x.text((x0 + w_ + 20, y + 30), f"{v}", "title", 44, c, ab, anchor="lm")
    a1 = x.b(1)
    if a1 > 0:
        x.text((CX, 1125), "73 ns = 365 cycles at 5 GHz", "semi", 44, WHITE, a1, anchor="mm")
        stamp(x, CX, 1230, "~100x slower", RED, a1, angle=-5)


# ---------- scene 6: outro ----------
def s_end(x):
    a = x.b(0)
    # big L3 ring catching packets before they reach RAM
    x.circle(CX, 760, 300, CYAN, a, 9)
    core(x, a, x.t * 3)
    for k in range(5):
        ph = (x.t * 0.8 + k / 5) % 1
        u = k * 2 * math.pi / 5 + 0.3
        rr = 300 - 220 * ph
        x.circle(540 + rr * math.cos(u), 760 + rr * math.sin(u), 16, AMBER, a, 0, fill=AMBER)
    x.text((CX, 760 - 330 - 10), "bigger cache = fewer trips to RAM", "semi", 40, WHITE, a, anchor="md")
    a1 = x.b(1)
    if a1 > 0:
        label_box(x, CX, 1170, "How a CPU Runs Your Code", AMBER, a1, 44)


SCENES = [("The 350-cycle wait", s_hook), ("Level 1: 4 cycles", s_l1), ("Level 2: 14 cycles", s_l2),
          ("Level 3: shared", s_l3), ("RAM: ~100x slower", s_ram), ("Why cache matters", s_end)]
