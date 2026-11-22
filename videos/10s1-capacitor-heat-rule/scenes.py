"""Short 10s1: electrolytic capacitor life doubles for every 10 C cooler (vertical, retro theme).
Visual language: a chunky drawn capacitor can with a draining electrolyte level, a vertical
thermometer, a stack of hour-glass blocks that doubles/halves, and a warm heat-shimmer motif."""
import math
from render import *  # noqa: F401,F403

SIZE = (1080, 1920)
CX = 540


def cap_can(x, cx, cy, w, h, level, a, c=None, hot=0.0):
    """Electrolytic capacitor: can body, stripe, scored top, two legs, inner electrolyte level."""
    if a <= 0:
        return
    c = c or CYAN
    x0, y0, x1, y1 = cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2
    x.rect([x0, y0, x1, y1], WHITE, a, 6, r=w * 0.18, fill=PANEL + (255,), glow=False)
    # electrolyte level
    if level > 0.01:
        top = y1 - 10 - (h - 20) * clamp(level)
        x.d.rounded_rectangle([x0 + 10, top, x1 - 10, y1 - 10], radius=w * 0.12, fill=col(c, a * 0.85))
    # polarity stripe
    x.d.rectangle([x1 - w * 0.22, y0 + 14, x1 - w * 0.1, y1 - 14], fill=col(MUTED, a * 0.7))
    # scored vent on the top (a cross)
    x.line([(cx - w * 0.25, y0 + 2), (cx + w * 0.25, y0 + 2)], MUTED, a, 4, glow=False)
    # legs
    for dx in (-w * 0.2, w * 0.2):
        x.line([(cx + dx, y1), (cx + dx, y1 + h * 0.25)], WHITE, a, 6, glow=False)
    # heat shimmer
    if hot > 0:
        for k in range(3):
            xx = cx - w * 0.3 + k * w * 0.3
            pts = [(xx + 14 * math.sin(x.t * 3 + j * 0.8 + k), y0 - 30 - j * 22) for j in range(6)]
            x.line(pts, RED, a * hot, 5, glow=False)


def thermo(x, cx, top, bot, frac, a, temp_txt=""):
    if a <= 0:
        return
    x.rect([cx - 28, top, cx + 28, bot], WHITE, a, 5, r=28, fill=PANEL + (255,), glow=False)
    x.circle(cx, bot + 30, 50, WHITE, a, 5, fill=AMBER)
    y = bot - (bot - top - 20) * clamp(frac)
    x.d.rounded_rectangle([cx - 14, y, cx + 14, bot + 10], radius=14, fill=col(AMBER, a))
    if temp_txt:
        x.text((cx + 60, y), temp_txt, "title", 54, AMBER, a, anchor="lm")


# ---------- scene 1: the part that wears out ----------
def s_hook(x):
    a = x.b(0)
    # PSU box outline with the capacitor zoomed out of it
    x.rect([130, 440, 520, 700], MUTED, a, 5, r=18, fill=PANEL + (255,), glow=False)
    for k in range(6):
        x.line([(170 + k * 55, 480), (170 + k * 55, 660)], GRID, a, 6, glow=False)
    x.text((325, 740), "cheap PSU", "semi", 36, MUTED, a, anchor="mt")
    p = ease(x.since(0) / 1.2)
    cx = 325 + (750 - 325) * p
    cy = 570 + (840 - 570) * p
    s = 0.35 + 0.65 * p
    cap_can(x, cx, cy, 240 * s, 380 * s, 0.85, a)
    if p > 0.95:
        x.text((750, 1170), "electrolytic capacitor", "semi", 40, CYAN, a, anchor="mm")


# ---------- scene 2: what it does and how it's rated ----------
def s_rating(x):
    a = x.b(0)
    # bumpy line in, flat line out, through the capacitor
    pts = [(80 + k * 6, 560 + 50 * abs(math.sin((80 + k * 6) / 40 + x.t * 2))) for k in range(48)]
    x.line(pts, MUTED, a, 5, glow=False)
    cap_can(x, CX, 600, 150, 230, 0.85, a)
    x.line([(640, 600), (1000, 600)], CYAN, a, 6, glow=False)
    x.text((260, 470), "rough in", "semi", 34, MUTED, a, anchor="mm")
    x.text((820, 540), "smooth out", "semi", 34, CYAN, a, anchor="mm")
    a1 = x.b(1)
    if a1 > 0:
        x.rect([150, 870, 930, 1180], AMBER, a1, 5, r=20, fill=PANEL + (255,), glow=False)
        x.text((CX, 930), "DATASHEET", "semi", 34, MUTED, a1, anchor="mm")
        x.text((CX, 1020), "5,000 h", "title", 80, WHITE, a1, anchor="mm")
        x.text((CX, 1115), "@ 105 °C", "title", 64, AMBER, a1, anchor="mm")


# ---------- scene 3: every 10 degrees cooler doubles life ----------
def s_rule(x):
    a = x.b(0)
    rows = [(105, 5000), (95, 10000), (85, 20000)]
    x.text((CX, 450), "-10 °C  =  x2 life", "title", 64, CYAN, x.b(1), anchor="mm")
    for k, (t, hrs) in enumerate(rows):
        beat = (0, 2, 3)[k]
        aa = x.b(beat)
        y = 600 + k * 220
        x.text((120, y + 40), f"{t} °C", "title", 56, AMBER, aa, anchor="lm")
        blocks = hrs // 5000
        for j in range(blocks):
            bx = 420 + j * 130
            p = ease((x.since(beat) - j * 0.15) / 0.4)
            x.rect([bx, y, bx + 110, y + 80], CYAN, aa * p, 4, r=10, fill=CYAN, glow=False)
        x.text((420, y + 125), f"{hrs:,} h", "semi", 44, WHITE, aa, anchor="lm")


# ---------- scene 4: hotter halves it ----------
def s_hotter(x):
    a = x.b(0)
    p = 0.5 + 0.5 * math.sin(x.t * 1.3)
    t = 85 + 30 * p
    life = 20000 / (2 ** ((t - 85) / 10))
    thermo(x, 250, 470, 1050, (t - 70) / 50, a, f"{int(t)} °C")
    level = clamp(life / 20000)
    cap_can(x, 720, 760, 220, 380, level, a, hot=clamp((t - 95) / 15))
    x.text((720, 1080), f"~{int(round(life, -2)):,} h", "title", 60, WHITE, a, anchor="mm")
    a1 = x.b(1)
    if a1 > 0:
        label_box(x, CX, 1210, "+10 °C  =  half the life", RED, a1, 42)


# ---------- scene 5: why cheap units die early ----------
def s_cheap(x):
    a = x.b(0)
    # two PSUs side by side: good (big heatsink, fan) vs cheap (tiny sink, slow fan)
    for k, (cx, good) in enumerate(((290, True), (790, False))):
        c = GREEN if good else RED
        x.rect([cx - 200, 460, cx + 200, 920], c, a, 5, r=20, fill=PANEL + (255,), glow=False)
        fins = 7 if good else 3
        fh = 170 if good else 80
        for j in range(fins):
            fx = cx - 150 + j * (300 / max(1, fins - 1)) if fins > 1 else cx
            x.line([(fx, 880), (fx, 880 - fh)], MUTED, a, 8, glow=False)
        # fan
        spin = x.t * (5 if good else 1.2)
        fy = 590
        x.circle(cx, fy, 80, WHITE, a, 4)
        for b in range(4):
            ang = spin + b * math.pi / 2
            x.line([(cx, fy), (cx + 70 * math.cos(ang), fy + 70 * math.sin(ang))], WHITE, a, 8, glow=False)
        x.text((cx, 970), "cool" if good else "hot", "title", 54, c, a, anchor="mm")
    a1 = x.b(1)
    if a1 > 0:
        x.text((CX, 1100), "hotter caps", "title", 58, WHITE, a1, anchor="mm")
        x.text((CX, 1180), "wear out sooner", "title", 58, RED, a1, anchor="mm")


# ---------- scene 6: keep it cool + the long video ----------
def s_end(x):
    a = x.b(0)
    # airflow arrows through a dust filter grid
    x.rect([140, 450, 940, 650], MUTED, a, 4, r=14, glow=False)
    for k in range(1, 12):
        x.line([(140 + k * 67, 450), (140 + k * 67, 650)], GRID, a, 3, glow=False)
    for k in range(4):
        y = 490 + k * 45
        off = (x.t * 220 + k * 90) % 300
        x.line([(150 + off, y), (240 + off, y)], CYAN, a, 6, glow=False)
        x.d.polygon([(240 + off, y - 12), (262 + off, y), (240 + off, y + 12)], fill=col(CYAN, a))
    x.text((CX, 700), "clean filters, room to breathe", "semi", 40, WHITE, a, anchor="mm")
    a1 = x.b(1)
    if a1 > 0:
        x.rect([140, 820, 940, 1180], AMBER, a1, 5, r=24, fill=PANEL + (255,), glow=False)
        x.text((CX, 885), "FULL VIDEO", "semi", 36, MUTED, a1, anchor="mm")
        x.text((CX, 990), "Power Supplies", "title", 76, WHITE, a1, anchor="mm")
        x.text((CX, 1095), "Explained", "title", 76, AMBER, a1, anchor="mm")


SCENES = [
    ("The first part to wear out", s_hook),
    ("Rated in hours", s_rating),
    ("10 degrees cooler, double the life", s_rule),
    ("Hotter halves it", s_hotter),
    ("Why cheap units die early", s_cheap),
    ("Keep it cool", s_end),
]
