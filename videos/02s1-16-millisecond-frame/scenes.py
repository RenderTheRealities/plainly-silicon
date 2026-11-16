"""Short 02s1: the frame-time budget (vertical, blueprint theme).
Drafting-table style: a stopwatch dial, ruler strips of one second, a budget bar with a moving
playhead, a pixel grid filling in and a frame-time graph with one spike."""
import math
from render import *  # noqa: F401,F403

SIZE = (1080, 1920)
CX = 540


def dim_line(x, x0, x1, y, label, c, a):
    """Engineering dimension line with end ticks and a centered label."""
    x.line([(x0, y), (x1, y)], c, a, 3, glow=False)
    for xx in (x0, x1):
        x.line([(xx, y - 16), (xx, y + 16)], c, a, 3, glow=False)
    x.text(((x0 + x1) / 2, y - 22), label, "semi", 38, c, a, anchor="md")


# ---------- scene 1: a stopwatch that only runs to 16.7 ms ----------
def s_dial(x):
    a = x.b(0)
    cy, r = 760, 300
    x.circle(CX, cy, r, CYAN, a, 6, fill=PANEL)
    x.rect([CX - 40, cy - r - 60, CX + 40, cy - r - 10], CYAN, a, 5, r=8, fill=PANEL + (255,))
    for k in range(60):
        ang = math.radians(k * 6 - 90)
        r0 = r - (34 if k % 5 == 0 else 18)
        x.line([(CX + r0 * math.cos(ang), cy + r0 * math.sin(ang)),
                (CX + (r - 8) * math.cos(ang), cy + (r - 8) * math.sin(ang))], MUTED if k % 5 else WHITE, a, 3, glow=False)
    # hand sweeps one 16.7 ms lap per second of screen time, repeatedly
    lap = (x.since(0) * 1.0) % 1.0
    ms = 16.7 * lap
    ang = math.radians(360 * lap - 90)
    x.line([(CX, cy), (CX + (r - 50) * math.cos(ang), cy + (r - 50) * math.sin(ang))], AMBER, a, 8)
    x.circle(CX, cy, 16, AMBER, a, 4, fill=AMBER)
    x.text((CX, cy + 110), f"{ms:4.1f} ms", "title", 76, WHITE, a, anchor="mm")
    x.text((CX, 1150), "one frame at 60 fps", "semi", 46, CYAN, a, anchor="mm")
    a1 = x.b(1)
    if a1 > 0:
        x.rect([270, 1190, 810, 1260], RED, a1, 4, r=34, fill=NAVY + (255,), glow=False)
        x.text((CX, 1225), "miss it = late frame", "semi", 40, RED, a1, anchor="mm")


# ---------- scene 2: one second, sliced 60 ways and 144 ways ----------
def strip(x, y, n, c, a, prog, label, value):
    x0, x1 = 90, 990
    x.text((x0, y - 70), label, "title", 46, WHITE, a, anchor="ls")
    x.text((x1, y - 70), value, "title", 46, c, a, anchor="rs")
    x.rect([x0, y - 40, x1, y + 40], c, a, 4, r=6, fill=PANEL + (255,), glow=False)
    shown = int(n * prog)
    for k in range(1, shown):
        xx = x0 + (x1 - x0) * k / n
        x.line([(xx, y - 40), (xx, y + 40)], c, a * 0.8, 2, glow=False)
    # highlight one slice
    if prog >= 1:
        w = (x1 - x0) / n
        x.d.rectangle([x0, y - 40, x0 + w, y + 40], fill=col(c, a * 0.9))


def s_divide(x):
    a = x.b(0)
    dim_line(x, 90, 990, 470, "1 second = 1000 ms", WHITE, a)
    strip(x, 680, 60, CYAN, a, clamp(x.since(0) / 2.0), "60 Hz", "1000 / 60 = 16.7 ms")
    a1 = x.b(1)
    if a1 > 0:
        strip(x, 960, 144, AMBER, a1, clamp(x.since(1) / 2.0), "144 Hz", "1000 / 144 = 6.9 ms")
        # zoomed comparison of one slice each
        p = ease((x.since(1) - 2.2) / 0.6)
        if p > 0:
            x.rect([150, 1100, 150 + 600 * p, 1150], CYAN, a1, 3, r=6, fill=CYAN + (255,), glow=False)
            x.rect([150, 1180, 150 + 249 * p, 1230], AMBER, a1, 3, r=6, fill=AMBER + (255,), glow=False)
            x.text((780, 1125), "16.7", "title", 44, CYAN, a1 * p, anchor="lm")
            x.text((430, 1205), "6.9", "title", 44, AMBER, a1 * p, anchor="lm")


# ---------- scene 3: what fits inside the budget ----------
STAGES = [("CPU: draw calls", 0.0, 0.22, "CYAN"), ("vertices", 0.22, 0.42, "AMBER"),
          ("which pixels?", 0.42, 0.60, "GREEN"), ("color pixels", 0.60, 0.95, "WHITE")]


def s_budget(x):
    a = x.b(0)
    top, bot, bx0, bx1 = 430, 1230, 640, 820
    x.rect([bx0, top, bx1, bot], CYAN, a, 5, r=10, fill=PANEL + (255,), glow=False)
    x.text((bx1 + 30, top + 10), "0 ms", "semi", 34, MUTED, a, anchor="lm")
    x.text((bx1 + 30, bot - 10), "16.7 ms", "semi", 34, MUTED, a, anchor="lm")
    for i, (name, f0, f1, cn) in enumerate(STAGES):
        beat = 0 if i == 0 else 1
        ai = ease((x.since(beat) - (0 if i == 0 else (i - 1) * 0.9)) / 0.5) * a
        if ai <= 0:
            continue
        c = globals()[cn]
        y0, y1 = top + (bot - top) * f0, top + (bot - top) * f1
        x.d.rectangle([bx0 + 6, y0 + 4, bx1 - 6, y1 - 4], fill=col(c, ai * 0.85))
        x.line([(bx0 - 40, (y0 + y1) / 2), (bx0 - 8, (y0 + y1) / 2)], c, ai, 4, glow=False)
        x.text((bx0 - 54, (y0 + y1) / 2), name, "semi", 44, c, ai, anchor="rm")
    # playhead runs down the bar, looping
    ph = top + (bot - top) * ((x.t * 0.35) % 1.0)
    x.line([(bx0 - 14, ph), (bx1 + 14, ph)], RED, a, 4, glow=False)
    x.text((bx0 - 54, top + (bot - top) * 0.975), "spare", "semi", 36, MUTED, a, anchor="rm")
    x.text((CX, bot + 24), "share of time varies by game", "reg", 32, MUTED, a, anchor="ma")


# ---------- scene 4: two million pixels, then out to the screen ----------
def s_pixels(x):
    a = x.b(0)
    cols, rows = 16, 9
    gx0, gy0, cell = 110, 440, 54
    p = clamp(x.since(0) / 3.5)
    filled = int(cols * rows * p)
    for k in range(cols * rows):
        r_, c_ = divmod(k, cols)
        bx, by = gx0 + c_ * cell, gy0 + r_ * cell
        if k < filled:
            shade = [CYAN, AMBER, GREEN, WHITE][(r_ * 3 + c_) % 4]
            x.d.rectangle([bx + 3, by + 3, bx + cell - 3, by + cell - 3], fill=col(shade, a * 0.9))
        else:
            x.d.rectangle([bx + 3, by + 3, bx + cell - 3, by + cell - 3], outline=col(GRID, a), width=2)
    x.text((CX, 1000), f"{int(2073600 * p):,}", "title", 90, WHITE, a, anchor="mm")
    x.text((CX, 1075), "pixels per frame (1920 x 1080)", "semi", 40, CYAN, a, anchor="mm")
    a1 = x.b(1)
    if a1 > 0:
        # finished frame slides into a monitor outline
        s = ease(x.since(1) / 0.8)
        x.rect([300, 1130, 780, 1250], WHITE, a1, 5, r=8, fill=PANEL + (255,), glow=False)
        x.d.rectangle([310, 1140, 310 + 460 * s, 1240], fill=col(CYAN, a1 * 0.8))
        x.text((CX, 1190), "sent to screen", "semi", 38, NAVY if s > 0.6 else WHITE, a1, anchor="mm")


# ---------- scene 5: a frame-time graph with one spike ----------
def s_spike(x):
    a = x.b(0)
    gx0, gx1, gy0, gy1 = 130, 990, 470, 1050
    x.line([(gx0, gy0), (gx0, gy1), (gx1, gy1)], WHITE, a, 4, glow=False)
    x.text((gx0 - 14, gy0), "ms", "semi", 34, MUTED, a, anchor="rm")

    def yv(ms):
        return gy1 - (gy1 - gy0) * ms / 45

    by = yv(16.7)
    for xx in range(gx0, gx1, 30):
        x.line([(xx, by), (xx + 15, by)], CYAN, a, 3, glow=False)
    x.text((gx1, by - 14), "16.7 ms budget", "semi", 34, CYAN, a, anchor="rd")
    n = 40
    prog = clamp(x.since(0) / 3.0)
    pts = []
    for k in range(int(n * prog) + 1):
        ms = 15.5 + 1.2 * math.sin(k * 1.7) if k != 26 else 40
        pts.append((gx0 + 10 + (gx1 - gx0 - 20) * k / n, yv(ms)))
    if len(pts) > 1:
        x.line(pts, AMBER, a, 5, glow=False)
    a1 = x.b(1)
    if a1 > 0 and prog >= 1:
        sx = gx0 + 10 + (gx1 - gx0 - 20) * 26 / n
        x.circle(sx, yv(40), 26, RED, a1, 5)
        x.text((sx + 40, yv(40)), "40 ms = hitch", "title", 44, RED, a1, anchor="lm")
        x.rect([200, 1110, 880, 1220], WHITE, a1, 4, r=14, fill=PANEL + (255,), glow=False)
        x.text((CX, 1165), "average still looks fine", "semi", 44, WHITE, a1, anchor="mm")


# ---------- scene 6: pointer to the long video ----------
def s_next(x):
    a = x.b(0)
    # a graphics card outline with a frame passing through it
    x.rect([170, 560, 910, 900], CYAN, a, 6, r=18, fill=PANEL + (255,))
    for k in range(2):
        cx = 360 + k * 360
        x.circle(cx, 730, 120, WHITE, a, 4)
        for j in range(7):
            ang = math.radians(j * 51 + x.t * 200)
            x.line([(cx, 730), (cx + 110 * math.cos(ang), 730 + 110 * math.sin(ang))], MUTED, a, 3, glow=False)
    for k in range(8):
        x.rect([210 + k * 84, 900, 260 + k * 84, 940], AMBER, a, 3, r=4, fill=AMBER + (255,), glow=False)
    fx = 170 + ((x.t * 260) % 900) - 100
    x.rect([fx, 1000, fx + 120, 1070], AMBER, a, 4, r=6, fill=NAVY + (255,), glow=False)
    x.text((fx + 60, 1035), "frame", "semi", 30, AMBER, a, anchor="mm")
    x.text((CX, 1160), "How a GPU Actually Works", "title", 54, WHITE, a, anchor="mm")
    x.text((CX, 1230), "full video on the channel", "semi", 38, CYAN, a, anchor="mm")


SCENES = [
    ("16.7 ms per frame", s_dial),
    ("1 second / frames", s_divide),
    ("What fits inside", s_budget),
    ("2 million pixels", s_pixels),
    ("Averages hide misses", s_spike),
    ("One frame, start to finish", s_next),
]
