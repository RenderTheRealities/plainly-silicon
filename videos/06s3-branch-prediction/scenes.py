"""Short 06s3: branch prediction, the CPU guessing past an if (vertical, tangerine theme).
Rail-yard look: instruction 'cars' on a track that forks at a switch; flat poster shapes, heavy type."""
import math
from render import *  # noqa: F401,F403

SIZE = (1080, 1920)
CX = 540


def car(x, cx, cy, c, a, ghost=False, s=44, mark=None):
    """One instruction as a rail car: solid when certain, hollow when speculative."""
    if a <= 0:
        return
    if ghost:
        x.rect([cx - s / 2, cy - s / 2, cx + s / 2, cy + s / 2], c, a, 5, r=8, glow=False)
    else:
        x.rect([cx - s / 2, cy - s / 2, cx + s / 2, cy + s / 2], c, a, 0, r=8, fill=c, glow=False)
    x.circle(cx - s * 0.25, cy + s / 2 + 6, 6, c, a, 0, fill=c)
    x.circle(cx + s * 0.25, cy + s / 2 + 6, 6, c, a, 0, fill=c)
    if mark == "x":
        x.line([(cx - 12, cy - 12), (cx + 12, cy + 12)], AMBER, a, 5, glow=False)
        x.line([(cx - 12, cy + 12), (cx + 12, cy - 12)], AMBER, a, 5, glow=False)


def track(x, pts, c, a, w=8):
    x.line(pts, c, a, w, glow=False)


def lerp(p0, p1, f):
    return (p0[0] + (p1[0] - p0[0]) * f, p0[1] + (p1[1] - p0[1]) * f)


def along(path, f):
    """Point at fraction f along a polyline."""
    segs = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
    L = [math.dist(a_, b_) for a_, b_ in segs]
    d = f * sum(L)
    for (p0, p1), l in zip(segs, L):
        if d <= l:
            return lerp(p0, p1, d / l if l else 0)
        d -= l
    return path[-1]


def fork(x, a, jx=430, y=820, up=600, down=1040, x1=980):
    """Track that splits at a junction: returns (stem, upper, lower) paths."""
    stem = [(90, y), (jx, y)]
    upper = [(jx, y), (jx + 140, up), (x1, up)]
    lower = [(jx, y), (jx + 140, down), (x1, down)]
    track(x, stem, CYAN, a)
    track(x, upper, CYAN, a)
    track(x, lower, CYAN, a)
    return stem, upper, lower


def checkmark(x, cx, cy, s, c, a, w=10):
    x.line([(cx - s, cy), (cx - s * 0.3, cy + s * 0.7), (cx + s, cy - s * 0.8)], c, a, w, glow=False)


# ---------- 1: the hook ----------
def s_hook(x):
    a = x.b(0)
    x.rect([110, 440, 970, 780], CYAN, a, 0, r=24, fill=CYAN, glow=False)
    lines = [("if", " score > best:"), ("", "    save()"), ("else", ":"), ("", "    keep_playing()")]
    for i, (kw, rest) in enumerate(lines):
        ai = ease((x.t - 0.3 - i * 0.25) / 0.4)
        y = 500 + i * 70
        f = font("monob", 46)
        x.text((160, y), kw, "monob", 46, AMBER, ai, anchor="lm")
        x.text((160 + x.d.textlength(kw, font=f), y), rest, "mono", 46, PANEL, ai, anchor="lm")
    # a car already rolling past the code before the answer is known
    k = (x.since(0) * 0.25) % 1
    track(x, [(90, 880), (990, 880)], CYAN, a)
    for j in range(4):
        px = 90 + ((k + j * 0.12) % 1) * 900
        car(x, px, 845, CYAN, a, ghost=j % 2 == 1)
    b = x.b(1)
    if b > 0:
        sc = 1 + 0.25 * (1 - ease(x.since(1) / 0.4))
        x.text((CX, 1090), "if", "title", int(260 * sc), CYAN, b, anchor="mm")
        # highlight 'if' in the code
        x.rect([145, 470, 215, 530], AMBER, b, 5, r=8, glow=False)


# ---------- 2: assembly line, then a fork ----------
def s_line(x):
    a = x.b(0)
    st = ["FETCH", "DECODE", "EXECUTE"]
    for i, nm in enumerate(st):
        cx = 220 + i * 320
        x.rect([cx - 140, 440, cx + 140, 540], CYAN, a, 0, r=16, fill=CYAN, glow=False)
        x.text((cx, 490), nm, "title", 40, AMBER, a, anchor="mm")
    track(x, [(60, 640), (1020, 640)], CYAN, a)
    # cars advance one station per 'tick', all stations busy at once
    tick = x.since(0) * 1.4
    for j in range(6):
        pos = (tick - j) % 6
        st_i = int(pos)
        f = ease(clamp((pos - st_i) * 2.2))
        cx = -100 + (st_i + f) * 320
        if 60 < cx < 1020:
            car(x, cx, 600, CYAN, a, s=50)
    b = x.b(1)
    if b > 0:
        stem, up, dn = fork(x, b, y=900, up=760, down=1120)
        x.circle(430, 900, 46, AMBER, b, 0, fill=AMBER)
        x.text((430, 902), "?", "title", 64, CYAN, b, anchor="mm")
        x.text((990, 715), "score > best", "semi", 36, CYAN, b, anchor="rm")
        x.text((990, 1075), "not higher", "semi", 36, CYAN, b, anchor="rm")
        # a car waiting at the junction, the comparison still 'running'
        car(x, 330, 868, CYAN, b, s=50)
        sp = x.since(1) * 4
        for k in range(8):
            ang = sp + k * math.pi / 4
            al = b * (0.25 + 0.75 * ((k / 8 + x.t * 0.8) % 1))
            x.circle(430 + 70 * math.cos(ang), 900 + 70 * math.sin(ang), 6, CYAN, al, 0, fill=CYAN)


# ---------- 3: the predictor guesses ----------
def s_guess(x):
    a = x.b(0)
    x.text((CX, 450), "last times this branch ran", "semi", 38, CYAN, a, anchor="mm")
    hist = [1, 1, 0, 1, 1, 1, 1]
    for i, h in enumerate(hist):
        ai = ease((x.since(0) - i * 0.15) / 0.3)
        cx = 180 + i * 120
        x.rect([cx - 46, 490, cx + 46, 582], CYAN, ai, 0 if h else 5, r=12, fill=CYAN if h else None, glow=False)
        # little arrow: up = took the 'if' path, down = the 'else' path
        d = -1 if h else 1
        col_ = AMBER if h else CYAN
        x.line([(cx, 536 - 20 * d), (cx, 536 + 22 * d)], col_, ai, 6, glow=False)
        x.line([(cx - 16, 536 + 4 * d), (cx, 536 + 22 * d), (cx + 16, 536 + 4 * d)], col_, ai, 6, glow=False)
    stem, up, dn = fork(x, a, y=920, up=760, down=1120)
    # switch lever pointing up
    lv = ease((x.since(0) - 1.6) / 0.5)
    ang = -math.pi / 2 - 0.6 * lv + (1 - lv) * 0.6
    # the switch: the guessed branch lights up
    if lv > 0:
        seg = [up[0], along(up, 0.25 * lv)] if lv < 1 else up
        x.line(seg if lv < 1 else up, AMBER, a, 14, glow=False)
    x.circle(430, 920, 26, CYAN, a, 0, fill=CYAN)
    x.line([(430, 920), (430 + 80 * math.cos(ang), 920 + 80 * math.sin(ang))], CYAN, a, 12, glow=False)
    g = ease((x.since(0) - 2.0) / 0.4)
    x.rect([250, 1185, 830, 1265], CYAN, g, 0, r=40, fill=CYAN, glow=False)
    x.text((CX, 1225), "GUESS: TAKE THE IF", "title", 44, AMBER, g, anchor="mm")
    # speculative cars racing down the upper branch
    go = clamp((x.since(0) - 2.2) / 3.5)
    for j in range(4):
        f = go - j * 0.12
        if f > 0:
            px, py = along(up, min(f, 1) * 0.95)
            car(x, px, py - 32, CYAN, a, ghost=True, s=44)


# ---------- 4: right vs wrong ----------
def mini_fork(x, oy, a):
    stem = [(90, oy), (330, oy)]
    up = [(330, oy), (420, oy - 110), (980, oy - 110)]
    dn = [(330, oy), (420, oy + 110), (980, oy + 110)]
    for p in (stem, up, dn):
        track(x, p, CYAN, a, 7)
    return up, dn


def s_result(x):
    a = x.b(0)
    x.text((90, 455), "RIGHT GUESS", "title", 46, CYAN, a, anchor="lm")
    up, dn = mini_fork(x, 640, a)
    for j in range(4):
        f = clamp(x.since(0) / 2.0) * 0.9 - j * 0.12
        if f > 0:
            px, py = along(up, f)
            car(x, px, py - 28, CYAN, a, s=40)
    checkmark(x, 520, 455, 26, GREEN, ease((x.since(0) - 1.0) / 0.4), 10)
    x.text((960, 800), "no time lost", "semi", 36, CYAN, ease((x.since(0) - 1.2) / 0.4), anchor="rm")
    b = x.b(1)
    if b <= 0:
        return
    x.text((90, 900), "WRONG GUESS", "title", 46, RED, b, anchor="lm")
    up2, dn2 = mini_fork(x, 1090, b)
    t1 = x.since(1)
    flush = ease((t1 - 1.6) / 0.8)
    for j in range(4):
        f = 0.9 - j * 0.12
        px, py = along(up2, f)
        # cars marked wrong, then flushed off the track
        car(x, px + flush * 300, py - 28 - flush * 60, RED, b * (1 - flush), s=40, mark="x" if t1 > 0.8 else None)
    x.text((960, 900), "FLUSH", "title", 46, RED, ease((t1 - 1.6) / 0.3) * (1 - ease((t1 - 4.5) / 0.5)), anchor="rm")
    re = clamp((t1 - 3.0) / 3.0)
    for j in range(3):
        f = re * 0.9 - j * 0.14
        if f > 0:
            px, py = along([(90, 1090)] + dn2, f)
            car(x, px, py - 28, CYAN, b, s=40)


# ---------- 5: the cost ----------
def s_cost(x):
    a = x.b(0)
    cx, cy, R = CX, 660, 230
    x.circle(cx, cy, R + 20, CYAN, a, 0, fill=CYAN)
    lost = int(20 * ease((x.since(0) - 0.3) / 3.0))
    for k in range(20):
        ang = -math.pi / 2 + k * 2 * math.pi / 20
        on = k < lost
        px, py = cx + R * 0.86 * math.cos(ang), cy + R * 0.86 * math.sin(ang)
        x.circle(px, py, 18, AMBER, a, 0 if on else 4, fill=AMBER if on else None)
    x.text((cx, cy - 10), "15-20", "title", 92, AMBER, a, anchor="mm")
    x.text((cx, cy + 58), "cycles", "semi", 36, PANEL, a, anchor="mm")
    x.text((cx, 955), "wasted per wrong guess", "title", 46, CYAN, a, anchor="mm")
    b = x.b(1)
    if b <= 0:
        return
    for i, (frac, nm) in enumerate(((1.0, "fewer wrong guesses"), (0.78, "more wrong guesses"))):
        y = 1080 + i * 110
        x.text((90, y - 30), f"5 GHz  ·  {nm}", "semi", 34, CYAN, b, anchor="lm")
        bar(x, 90, y, 900, frac * ease(x.since(1) / 1.2), CYAN if i == 0 else RED, b, h=44)


# ---------- 6: the full video ----------
def s_end(x):
    a = x.b(0)
    x.rect([120, 500, 960, 940], CYAN, a, 0, r=28, fill=CYAN, glow=False)
    x.text((CX, 580), "FULL VIDEO", "semi", 36, PANEL, a, anchor="mm")
    x.text((CX, 680), "How a CPU Runs", "title", 76, AMBER, a, anchor="mm")
    x.text((CX, 770), "Your Code", "title", 76, AMBER, a, anchor="mm")
    track(x, [(200, 880), (880, 880)], PANEL, a, 6)
    for j in range(5):
        px = 200 + ((x.t * 0.18 + j * 0.2) % 1) * 680
        car(x, px, 850, AMBER, a, s=36)


SCENES = [
    ("It runs code early", s_hook),
    ("The line forks at an if", s_line),
    ("Make a guess", s_guess),
    ("Right or wrong", s_result),
    ("The price of a wrong guess", s_cost),
    ("The full assembly line", s_end),
]
