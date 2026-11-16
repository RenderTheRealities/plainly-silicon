"""Short 07s1: the inflated "was" price and checking price history (vertical, crimson theme).
Visual language: a swinging paper price tag on a string, a dot field of 175 products,
a 12-month timeline with a Black Friday pin, and a hand-drawn price-history line."""
import math
from render import *  # noqa: F401,F403

SIZE = (1080, 1920)
CX = 540


def tag(x, cx, cy, w, h, ang, a, was="$399", now="$299", strike=1.0):
    """A hanging price tag: string from (cx, cy - h/2 - 120), body rotated by ang (radians)."""
    if a <= 0:
        return
    top = (cx, cy - h / 2 - 140)
    ca, sa = math.cos(ang), math.sin(ang)

    def rot(px, py):  # rotate around the string's top point
        dx, dy = px - top[0], py - top[1]
        return (top[0] + dx * ca - dy * sa, top[1] + dx * sa + dy * ca)

    notch = 70
    body = [(-w / 2 + notch, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2 + notch, h / 2), (-w / 2, 0)]
    body = [(cx + bx, cy + by) for bx, by in body]
    # tag points left: make it hang from its notch end
    pts = [rot(*p) for p in body]
    hole = rot(cx - w / 2 + 55, cy)
    x.line([top, hole], MUTED, a, 3, glow=False)
    x.d.polygon(pts, fill=col(PANEL, a), outline=col(CYAN, a))
    x.d.line(pts + [pts[0]], fill=col(CYAN, a), width=5)
    x.circle(hole[0], hole[1], 12, CYAN, a, 4, fill=NAVY)
    # text (not rotated, small angles only)
    wx, wy = rot(cx + 40, cy - 55)
    nx, ny = rot(cx + 40, cy + 50)
    x.text((wx, wy), "was " + was, "reg", 48, MUTED, a, anchor="mm")
    if strike > 0:
        tw = x.d.textlength("was " + was, font=font("reg", 48))
        x.line([(wx - tw / 2 - 6, wy), (wx - tw / 2 - 6 + (tw + 12) * strike, wy)], AMBER, a, 6, glow=False)
    x.text((nx, ny), now, "title", 92, CYAN, a, anchor="mm")


# ---------- 1: the hook ----------
def s_hook(x):
    a = x.b(0)
    ang = 0.12 * math.sin(x.t * 2.2) * math.exp(-x.t * 0.25)
    tag(x, CX + 40, 800, 560, 300, ang, a, strike=ease((x.t - 1.2) / 0.8))
    q = ease((x.t - 3.0) / 0.5)
    if q > 0:
        rr = 8 * math.sin(x.t * 5)
        x.d.ellipse([CX + 70 - 200 - rr, 745 - 70 - rr, CX + 70 + 200 + rr, 745 + 70 + rr], outline=col(AMBER, q * a), width=6)
        x.text((CX + 70, 1130), "this number?", "title", 60, AMBER, q * a, anchor="mm")


# ---------- 2: why it feels good ----------
def s_feel(x):
    a = x.b(0)
    tag(x, CX - 60, 760, 480, 260, -0.05, a)
    s = ease((x.t - 1.5) / 0.6)
    if s > 0:
        r = 125 * (0.6 + 0.4 * s)
        bx, by = CX + 250, 1000
        pts = [(bx + (r if k % 2 == 0 else r * 0.78) * math.cos(k * math.pi / 12 + x.t * 0.4),
                by + (r if k % 2 == 0 else r * 0.78) * math.sin(k * math.pi / 12 + x.t * 0.4)) for k in range(24)]
        x.d.polygon(pts, fill=col(AMBER, s))
        x.text((bx, by - 18), "-$100", "title", 60, NAVY, s, anchor="mm")
        x.text((bx, by + 38), "OFF!", "title", 40, NAVY, s, anchor="mm")
    f = ease((x.t - 4.0) / 0.6)
    x.text((CX - 120, 1180), "feels like a deal...", "semi", 50, WHITE, f, anchor="mm")


# ---------- 3: the Which? study, a field of 175 products ----------
def s_study(x):
    a = x.b(0)
    x.text((CX, 440), "175 products  ·  8 retailers", "semi", 46, WHITE, a, anchor="mm")
    cols, r, gap = 15, 17, 46
    x0 = CX - (cols - 1) * gap / 2
    n_hit = round(175 * 0.83)  # 145
    turn = x.b(1)
    for i in range(175):
        cx, cy = x0 + (i % cols) * gap, 520 + (i // cols) * gap
        ai = a * ease((x.since(0) - i * 0.012) / 0.3)
        hit = i < n_hit and turn > 0 and (x.since(1) > i * 0.012)
        x.circle(cx, cy, r, CYAN if hit else MUTED, ai, 3, fill=CYAN if hit else None)
    if turn > 0:
        pct = int(83 * clamp(x.since(1) / 1.8))
        x.text((CX, 1195), f"{pct}%", "title", 110, CYAN, turn, anchor="mm")
        x.text((CX, 1095), "same price or cheaper outside the sale", "semi", 40, CYAN, turn, anchor="mm")


# ---------- 4: never cheapest only on the day ----------
def s_zero(x):
    a = x.b(0)
    months = ["J", "J", "A", "S", "O", "N", "D", "J", "F", "M", "A", "M"]
    y = 640
    x.line([(90, y), (990, y)], MUTED, a, 4, glow=False)
    for i, m in enumerate(months):
        mx = 120 + i * 76
        x.line([(mx, y - 14), (mx, y + 14)], MUTED, a, 3, glow=False)
        x.text((mx, y + 50), m, "semi", 34, MUTED, a, anchor="mm")
    # Black Friday pin, late November
    bf = 120 + 5 * 76 + 50
    p = ease((x.t - 0.3) / 0.5)
    x.line([(bf, y - 120 * p), (bf, y)], AMBER, a * p, 5, glow=False)
    x.circle(bf, y - 120 * p, 22, AMBER, a * p, 4, fill=AMBER)
    x.text((bf, y - 175), "Black Friday", "title", 40, AMBER, a * p, anchor="mm")
    # big zero box
    z = ease((x.t - 1.0) / 0.6)
    x.rect([CX - 230, 820, CX + 230, 1180], CYAN, z, 6, r=30, fill=PANEL + (255,), glow=False)
    x.text((CX, 960), "0", "title", 190, CYAN, z, anchor="mm")
    x.text((CX, 1110), "cheapest only that day", "semi", 38, WHITE, z, anchor="mm")


# ---------- 5: check the price history ----------
def s_history(x):
    a = x.b(0)
    gx0, gx1, gy0, gy1 = 160, 980, 560, 980
    x.rect([gx0 - 90, gy0 - 120, gx1 + 30, gy1 + 80], MUTED, a, 3, r=24, fill=PANEL + (255,), glow=False)
    x.text((gx0, gy0 - 70), "price history", "title", 46, WHITE, a, anchor="lm")

    def py(v):
        return gy1 - (v - 250) / (420 - 250) * (gy1 - gy0)
    for v in (299, 399):
        x.text((gx0 - 10, py(v)), f"${v}", "semi", 34, MUTED, a, anchor="rm")
    # price per week over ~26 weeks: 349 in spring, 299 from summer on, a 399 "was" spike just before the sale
    pts = []
    for k in range(27):
        v = 349 if k < 6 else 299
        if 20 <= k <= 21:
            v = 399
        pts.append((gx0 + 20 + k * (gx1 - gx0 - 40) / 26, py(v)))
    draw = clamp(x.since(1) / 2.5) if x.b(1) > 0 else 0
    n = max(2, int(len(pts) * draw))
    if draw > 0:
        x.line(pts[:n], CYAN, a, 6, glow=False)
    if draw >= 1:
        sx, sy = pts[20]
        x.text((sx + 40, sy - 45), "\"was\" $399", "semi", 34, AMBER, a, anchor="mm")
        x.text((pts[26][0] - 10, pts[26][1] + 45), "sale $299", "semi", 34, CYAN, a, anchor="rm")
    c = x.b(2)
    if c > 0:
        x.rect([CX - 300, 1115, CX + 300, 1225], GREEN, c, 5, r=20, fill=NAVY + (255,), glow=False)
        x.text((CX, 1170), "real saving: $0", "title", 60, GREEN, c, anchor="mm")


# ---------- 6: six more traps ----------
def s_more(x):
    a = x.b(0)
    for i in range(7):
        cx, cy = 150 + i * 130, 720
        ai = a * ease((x.since(0) - 0.15 * i) / 0.4)
        done = i == 0
        x.circle(cx, cy, 52, CYAN if done else AMBER, ai, 5, fill=CYAN if done else None)
        x.text((cx, cy), str(i + 1), "title", 52, NAVY if done else AMBER, ai, anchor="mm")
    x.text((CX, 900), "7 Black Friday", "title", 76, WHITE, a, anchor="mm")
    x.text((CX, 990), "PC Part Traps", "title", 76, WHITE, a, anchor="mm")
    x.text((CX, 1110), "full video on the channel", "semi", 40, MUTED, a, anchor="mm")


SCENES = [("The \"was\" price", s_hook), ("Why it feels like a deal", s_feel), ("Which? tracked 175 deals", s_study),
          ("Cheapest only on Black Friday?", s_zero), ("Check the price history", s_history), ("Six more traps", s_more)]
