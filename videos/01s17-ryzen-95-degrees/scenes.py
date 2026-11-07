"""Short 01s17: why a Ryzen 7000 CPU sitting at 95 C is by design (vertical)."""
import math
from render import *  # noqa: F401,F403

SIZE = (1080, 1920)
CX = 540


def thermo(x, a, cx, top, bot, frac, c):
    """A tall thermometer: tube plus bulb, filled to frac."""
    r = 70
    x.d.rounded_rectangle([cx - 38, top, cx + 38, bot], radius=38, fill=col(PANEL, a), outline=col(WHITE, a), width=5)
    x.circle(cx, bot + r - 20, r, WHITE, a, 5, fill=PANEL)
    x.circle(cx, bot + r - 20, r - 14, c, a, 0, fill=c)
    fy = bot - (bot - top - 30) * clamp(frac)
    x.d.rounded_rectangle([cx - 22, fy, cx + 22, bot + 30], radius=22, fill=col(c, a))


def heat_c(frac):
    """Blend from AMBER (warm) to RED (hot) as the reading climbs."""
    return tuple(int(AMBER[i] + (RED[i] - AMBER[i]) * clamp(frac)) for i in range(3))


def t_hook(x):
    a = x.b(0)
    p = ease(x.since(0) / 2.4)
    temp = 40 + 55 * p
    thermo(x, a, 330, 440, 1060, (temp - 20) / 85, heat_c(p))
    x.text((760, 700), f"{int(round(temp))}°C", "title", 150, heat_c(p), a, anchor="mm")
    x.text((760, 820), "Ryzen under load", "semi", 38, MUTED, a, anchor="mm")
    a1 = x.b(1)
    # wavy heat lines rising off the reading
    for k in range(3):
        xs = 640 + k * 120
        pts = [(xs + 14 * math.sin(x.t * 6 + j * 0.8 + k), 560 - j * 14) for j in range(9)]
        x.line(pts, RED, a1 * 0.8, 5, glow=True)
    label_box(x, 760, 960, "too hot?", AMBER, a1, 56)


def t_design(x):
    a = x.b(0)
    stamp(x, CX, 520, "BY DESIGN", GREEN, a, angle=-6)
    # temperature over time: climbs, then flattens at the limit
    a2 = x.b(2)
    x0, y0, w, h = 150, 700, 780, 420
    x.line([(x0, y0), (x0, y0 + h), (x0 + w, y0 + h)], WHITE, a2, 4, glow=False)
    ly = y0 + 70
    for k in range(0, w, 34):
        x.line([(x0 + k, ly), (x0 + k + 18, ly)], RED, a2, 3, glow=False)
    x.text((x0 + w, ly - 22), "limit ~95°C", "semi", 34, RED, a2, anchor="rs")
    pts = []
    for i in range(61):
        u = i / 60
        yv = y0 + h - (h - 70) * min(1.0, 1 - (1 - min(u / 0.45, 1)) ** 2)
        pts.append((x0 + w * u, yv))
    k = max(2, int(61 * ease(x.since(2) / 2.5)))
    x.line(pts[:k], AMBER, a2, 8)
    x.text((x0 + w / 2, y0 + h + 44), "time under heavy load", "semi", 32, MUTED, a2, anchor="mm")


def t_brake(x):
    a = x.b(0)
    # clock speed column grows while the "thermal room" column drains
    s = x.since(1)
    p = ease(s / 3.0) if x.b(1) > 0 else 0.0
    held = x.b(2) > 0
    base, top = 1120, 520
    hmax = base - top
    # clock
    hc = hmax * (0.35 + 0.6 * p)
    x.d.rounded_rectangle([210, base - hc, 450, base], radius=20, fill=col(AMBER, a))
    x.text((330, base + 50), "clock speed", "semi", 36, WHITE, a, anchor="mm")
    x.text((330, base - hc - 40), "up" if not held else "holds", "title", 48, AMBER, a, anchor="mm")
    # thermal room
    hr = hmax * (0.9 - 0.9 * p)
    x.d.rounded_rectangle([630, top, 870, base], radius=20, outline=col(MUTED, a), width=4)
    if hr > 8:
        x.d.rounded_rectangle([630, base - hr, 870, base], radius=20, fill=col(CYAN, a))
    x.text((750, base + 50), "thermal room", "semi", 36, WHITE, a, anchor="mm")
    if held:
        label_box(x, 750, (top + base) / 2, "at limit", RED, x.b(2), 40)


def t_247(x):
    a = x.b(0)
    cx, cy, r = CX, 780, 270
    x.circle(cx, cy, r, WHITE, a, 6, fill=PANEL)
    for h_ in range(12):
        ang = h_ / 12 * 2 * math.pi
        x.line([(cx + (r - 30) * math.sin(ang), cy - (r - 30) * math.cos(ang)),
                (cx + (r - 6) * math.sin(ang), cy - (r - 6) * math.cos(ang))], MUTED, a, 5, glow=False)
    # hand sweeps around: hours pass, temperature stays at the limit
    ang = x.since(0) * 1.4
    x.line([(cx, cy), (cx + (r - 60) * math.sin(ang), cy - (r - 60) * math.cos(ang))], AMBER, a, 10)
    x.circle(cx, cy, 14, AMBER, a, 0, fill=AMBER)
    x.text((cx, cy + 120), "95°C", "title", 70, RED, a, anchor="mm")
    label_box(x, CX, 1150, "no damage, per AMD", GREEN, x.b(0) * ease(x.since(0) / 0.6 - 3), 44)


def t_end(x):
    rows = [(0, "Hot under load", "fine", GREEN), (1, "Hot while idle", "check", RED), (1, "Sudden slowdown", "check", RED)]
    for k, (beat, left, right, c) in enumerate(rows):
        delay = 0.0 if k == 0 else (k - 1) * 0.7
        ab = x.b(beat) * ease((x.since(beat) - delay) / 0.5)
        y = 520 + k * 210
        x.rect([120, y, 960, y + 150], c, ab, 5, r=24, fill=PANEL + (255,))
        x.text((170, y + 75), left, "title", 50, WHITE, ab, anchor="lm")
        x.text((910, y + 75), right, "title", 50, c, ab, anchor="rm")
    label_box(x, CX, 1200, "More PC hardware on the channel", CYAN, x.b(2), 36)


SCENES = [("95°C. Is that bad?", t_hook), ("Built to run hot", t_design), ("Heat is the brake", t_brake),
          ("All day, every day", t_247), ("When to worry", t_end)]
