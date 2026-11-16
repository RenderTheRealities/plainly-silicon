"""Short 03s2: the RAM notch is a key (vertical, paper theme).
Design language: flat technical illustration of DIMM edges, slots with ridges, a ruler,
a spec-sheet card and socket 'keys'. Sticks are drawn horizontally, wide, to fill the phone screen."""
import math
from render import *  # noqa: F401,F403

SIZE = (1080, 1920)
CX = 540
GOLD = (196, 150, 40)


def stick(x, x0, y0, w, h, notch_f, a, label="", c=None, pins=True):
    """A DIMM: green-ish PCB in theme colors, black chips, gold contacts, notch at fraction notch_f."""
    if a <= 0:
        return
    c = c or CYAN
    nx = x0 + w * notch_f
    nw = 22
    pts = [(x0, y0), (x0 + w, y0), (x0 + w, y0 + h), (nx + nw / 2, y0 + h), (nx + nw / 2, y0 + h - 30),
           (nx - nw / 2, y0 + h - 30), (nx - nw / 2, y0 + h), (x0, y0 + h)]
    x.d.polygon(pts, fill=col(PANEL, a), outline=col(c, a))
    x.d.line(pts + [pts[0]], fill=col(c, a), width=4)
    # chips
    cw = (w - 80) / 8
    for i in range(8):
        cx0 = x0 + 40 + i * cw
        x.d.rectangle([cx0 + 6, y0 + 22, cx0 + cw - 6, y0 + h * 0.5], fill=col(WHITE, a * 0.85))
    if pins:
        for px in range(int(x0 + 14), int(x0 + w - 14), 9):
            if abs(px - nx) < nw / 2 + 6:
                continue
            x.d.rectangle([px, y0 + h - 26, px + 5, y0 + h - 4], fill=col(GOLD, a))
    if label:
        x.text((x0 + w / 2, y0 + h * 0.66), label, "title", 40, c, a, anchor="mm")


def slot(x, x0, y0, w, ridge_f, a, c=None):
    if a <= 0:
        return
    c = c or WHITE
    x.d.rounded_rectangle([x0, y0, x0 + w, y0 + 50], radius=8, fill=col(WHITE, a * 0.9))
    x.d.rectangle([x0 + 10, y0 + 6, x0 + w - 10, y0 + 22], fill=col(NAVY, a))
    rx = x0 + w * ridge_f
    x.d.rectangle([rx - 9, y0 - 4, rx + 9, y0 + 22], fill=col(AMBER, a))


# 1. hook: two sticks, same 288 pins, same length
def s_hook(x):
    a0, a1 = x.b(0), ease((x.since(0) - 0.8) / 0.5)
    stick(x, 90, 460, 900, 200, 0.50, a0, "DDR4", CYAN)
    stick(x, 90, 760, 900, 200, 0.44, a1, "DDR5", AMBER)
    cnt = int(288 * clamp(x.since(0) / 2.0))
    x.text((990, 690), f"{cnt} pins", "semi", 34, MUTED, a0, anchor="rm")
    x.text((990, 990), f"{cnt} pins", "semi", 34, MUTED, a1, anchor="rm")
    # equal-length ruler
    r = ease((x.since(0) - 2.5) / 0.6)
    x.line([(90, 1060), (990, 1060)], WHITE, r, 4, glow=False)
    for xx in (90, 990):
        x.line([(xx, 1040), (xx, 1080)], WHITE, r, 4, glow=False)
    x.text((CX, 1100), "same length", "semi", 38, WHITE, r, anchor="mt")
    q = x.b(1)
    x.text((CX, 1215), "so why won't it fit?", "title", 52, AMBER, q, anchor="mm")


# 2. zoom on the bottom edge: notch over slot ridge, DDR4 vs DDR5 positions
def s_notch(x):
    a = x.b(0)
    # magnified edge of a stick
    zoom_y = 470
    stick(x, 40, zoom_y, 1000, 230, 0.50, a, "", CYAN)
    b = x.b(1)
    drop = 1 - ease(x.since(1) / 1.0)
    slot(x, 40, 760 + 40 * drop, 1000, 0.50, b)
    x.text((CX, 860), "notch meets ridge", "semi", 40, WHITE, b, anchor="mm")
    c = x.b(2)
    # comparison strip: the two notch positions on one ruler
    x.line([(90, 1050), (990, 1050)], MUTED, c, 4, glow=False)
    for f, nm, cc, dy in [(0.50, "DDR4", CYAN, -1), (0.44, "DDR5", AMBER, 1)]:
        px = 90 + 900 * f
        x.d.polygon([(px, 1050), (px - 18, 1050 + 34 * dy), (px + 18, 1050 + 34 * dy)], fill=col(cc, c))
        x.text((px + (60 if dy < 0 else -60), 1050 + 70 * dy), nm, "title", 40, cc, c,
               anchor=("lm" if dy < 0 else "rm"))


# 3. the key at work: wrong stick stops on the ridge
def s_key(x):
    a = x.b(0)
    t = x.since(0)
    # stick comes down, stops at the ridge, small bounce
    y = 480 + min(t, 1.2) / 1.2 * 260
    if t > 1.2:
        y -= 18 * abs(math.sin((t - 1.2) * 6)) * math.exp(-(t - 1.2) * 2)
    stick(x, 90, y, 900, 200, 0.44, a, "DDR5", AMBER)
    slot(x, 90, 960, 900, 0.50, a)
    x.text((CX, 1050), "DDR4 slot", "semi", 38, MUTED, a, anchor="mm")
    if t > 1.3:
        st = ease((t - 1.3) / 0.4)
        x.line([(450, 920), (500, 970)], RED, st * a, 10, glow=False)
        x.line([(500, 920), (450, 970)], RED, st * a, 10, glow=False)
    b = x.b(1)
    label_box(x, 300, 1170, "DDR4  1.2 V", CYAN, b, 40)
    label_box(x, 780, 1170, "DDR5  1.1 V", AMBER, b, 40)


# 4. how to check: spec-sheet card, then a CPU-Z style readout
def s_check(x):
    a = x.b(0)
    x.rect([110, 440, 970, 820], WHITE, a, 4, r=18, fill=PANEL + (255,), glow=False)
    x.text((150, 490), "Your board  ·  Specifications", "title", 40, WHITE, a, anchor="lm")
    rows = [("Socket", "..."), ("Chipset", "..."), ("Memory", "4 x DDR5 DIMM"), ("Storage", "...")]
    hl = ease((x.since(0) - 1.0) / 0.5)
    for i, (k, v) in enumerate(rows):
        y = 570 + i * 60
        if k == "Memory" and hl > 0:
            x.d.rounded_rectangle([130, y - 26, 950, y + 26], radius=10, fill=col(AMBER, hl * 0.25))
        x.text((150, y), k, "semi", 36, MUTED, a, anchor="lm")
        x.text((930, y), v, "semi", 36, AMBER if k == "Memory" else WHITE, a, anchor="rm")
    b = x.b(1)
    # CPU-Z like window
    x.rect([190, 900, 890, 1230], WHITE, b, 4, r=10, fill=NAVY + (255,), glow=False)
    x.d.rectangle([194, 904, 886, 950], fill=col(CYAN, b))
    x.text((214, 927), "CPU-Z", "semi", 30, NAVY, b, anchor="lm")
    for i, tab in enumerate(["CPU", "Memory", "SPD"]):
        tx = 214 + i * 170
        x.rect([tx, 970, tx + 150, 1020], CYAN if tab == "Memory" else MUTED, b, 3, r=6, glow=False)
        x.text((tx + 75, 995), tab, "semi", 28, WHITE, b, anchor="mm")
    x.text((240, 1110), "Type", "semi", 40, MUTED, b, anchor="lm")
    x.rect([440, 1075, 840, 1145], AMBER, b, 4, r=8, glow=False)
    x.text((640, 1110), "DDR5", "title", 46, AMBER, b, anchor="mm")
    x.text((CX, 1190), "what's installed now", "semi", 30, MUTED, b, anchor="mm")


# 5. the shortcut: socket key cards
def s_shortcut(x):
    data = [("AM5", "DDR5 only", AMBER, 0.0), ("AM4", "DDR4 only", CYAN, 0.6),
            ("Intel 12th-14th gen", "DDR4 or DDR5 board", GREEN, None)]
    for i, (sock, mem, c, delay) in enumerate(data):
        if delay is None:
            aa = x.b(1)
        else:
            aa = ease((x.since(0) - delay) / 0.5)
        y = 440 + i * 235
        x.rect([90, y, 990, y + 200], c, aa, 5, r=24, fill=PANEL + (255,), glow=False)
        # little socket square
        x.rect([130, y + 30, 270, y + 170], c, aa, 4, r=8, glow=False)
        for gx in range(150, 260, 22):
            for gy in range(int(y + 50), int(y + 160), 22):
                x.d.ellipse([gx - 3, gy - 3, gx + 3, gy + 3], fill=col(c, aa))
        x.text((310, y + 70), sock, "title", 48, WHITE, aa, anchor="lm")
        x.text((310, y + 140), mem, "semi", 40, c, aa, anchor="lm")
    st = ease((x.since(1) - 1.5) / 0.5)
    if st > 0:
        stamp(x, CX, 1185, "CHECK THE BOARD", RED, st, angle=-4)


# 6. outro: three generations, three notch spots
def s_outro(x):
    a = x.b(0)
    for i, (nm, f, c) in enumerate([("DDR3", 0.56, MUTED), ("DDR4", 0.50, CYAN), ("DDR5", 0.44, AMBER)]):
        aa = ease((x.since(0) - i * 0.3) / 0.5)
        stick(x, 140, 450 + i * 210, 800, 160, f, aa, nm, c)
    x.text((CX, 1150), "Every Type of RAM Explained", "title", 52, WHITE, a, anchor="mm")
    x.text((CX, 1215), "full video on the channel", "semi", 36, MUTED, a, anchor="mm")


SCENES = [
    ("Same pins, won't fit", s_hook),
    ("The notch", s_notch),
    ("A key, on purpose", s_key),
    ("Which one does your board take?", s_check),
    ("The shortcut", s_shortcut),
    ("Every generation", s_outro),
]
