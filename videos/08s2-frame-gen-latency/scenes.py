"""Short 08s2: frame generation raises the FPS counter, not responsiveness (vertical, terminal theme).
Visual language: a console-style FPS readout, a film strip of real vs generated frames on a time axis,
input pulses that only land on real frames, and a base-frame-rate ruler."""
from render import *  # noqa: F401,F403

SIZE = (1080, 1920)
CX = 540


def frame_card(x, cx, cy, real, a, w=120, h=170, hit=0.0):
    """A frame: real = solid; generated = dashed outline with '?'."""
    if a <= 0:
        return
    x0, y0, x1, y1 = cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2
    if real:
        x.rect([x0, y0, x1, y1], CYAN, a, 5, r=10, fill=PANEL + (255,))
        x.text((cx, cy), "R", "monob", 64, CYAN, a, anchor="mm")
        if hit > 0:
            x.rect([x0 - 10, y0 - 10, x1 + 10, y1 + 10], AMBER, a * hit, 4, r=14)
    else:
        step = 18
        for k in range(int((x1 - x0) / step)):
            if k % 2 == 0:
                xx = x0 + k * step
                x.line([(xx, y0), (min(xx + step, x1), y0)], MUTED, a, 4, glow=False)
                x.line([(xx, y1), (min(xx + step, x1), y1)], MUTED, a, 4, glow=False)
        for k in range(int((y1 - y0) / step)):
            if k % 2 == 0:
                yy = y0 + k * step
                x.line([(x0, yy), (x0, min(yy + step, y1))], MUTED, a, 4, glow=False)
                x.line([(x1, yy), (x1, min(yy + step, y1))], MUTED, a, 4, glow=False)
        x.text((cx, cy), "?", "monob", 64, MUTED, a, anchor="mm")


# ---------- scene 1: the counter doubles ----------
def s_hook(x):
    a = x.b(0)
    p = ease(x.since(0) / 1.4)
    x.rect([150, 480, 930, 820], CYAN, a, 4, r=8, fill=PANEL + (255,))
    x.text((190, 520), "> fps_overlay", "mono", 36, MUTED, a)
    x.text((CX, 690), f"{int(60 + 60 * p)} FPS", "monob", 130, CYAN, a, anchor="mm")
    a1 = x.b(1)
    if a1 > 0:
        x.text((CX, 960), "feels like:", "mono", 46, MUTED, a1, anchor="mm")
        x.text((CX, 1060), "60", "monob", 120, AMBER, a1, anchor="mm")


# ---------- scene 2: real, guess, real ----------
def s_strip(x):
    a = x.b(0)
    y = 720
    x.line([(80, y + 150), (1000, y + 150)], MUTED, a, 3, glow=False)
    x.text((1000, y + 190), "time ->", "mono", 32, MUTED, a, anchor="ra")
    xs = [170, 370, 570, 770, 970]
    for k, cx in enumerate(xs):
        if k % 2 == 0:
            frame_card(x, cx - 30 if k == 4 else cx, y, True, x.b(0))
    a1 = x.b(1)
    for k, cx in enumerate(xs):
        if k % 2 == 1:
            frame_card(x, cx, y, False, a1)
    if a1 > 0:
        x.text((CX, 1030), "2 real + 1 guessed between", "mono", 40, WHITE, a1, anchor="mm")
        x.text((CX, 1110), "pictures on screen: x2", "monob", 48, CYAN, a1, anchor="mm")


# ---------- scene 3: input only reaches real frames ----------
def s_input(x):
    a = x.b(0)
    y = 820
    xs = [170, 370, 570, 770, 940]
    # mouse at top
    x.rect([470, 430, 610, 600], WHITE, a, 5, r=60, fill=PANEL + (255,), glow=False)
    x.line([(540, 430), (540, 500)], WHITE, a, 4, glow=False)
    click = (x.t * 1.2) % 1
    for k, cx in enumerate(xs):
        real = k % 2 == 0
        if real:
            x.line([(540, 610), (cx, y - 95)], AMBER, a * (0.4 + 0.6 * (1 - click)), 4, glow=False)
        frame_card(x, cx, y, real, a, w=110, h=160, hit=(1 - click) if real else 0)
    x.text((CX, 980), "input read here: R only", "mono", 40, AMBER, a, anchor="mm")
    a1 = x.b(1)
    if a1 > 0:
        for cx in (370, 770):
            x.line([(cx - 40, y - 40), (cx + 40, y + 40)], RED, a1, 6, glow=False)
            x.line([(cx - 40, y + 40), (cx + 40, y - 40)], RED, a1, 6, glow=False)
        x.text((CX, 1080), "? = built from old frames", "mono", 40, RED, a1, anchor="mm")
        x.text((CX, 1150), "can't see your click", "mono", 40, RED, a1, anchor="mm")


# ---------- scene 4: 120 shown, 60 felt, plus a hold-back ----------
def s_feel(x):
    a = x.b(0)
    bar(x, 140, 520, 800, ease(x.since(0) / 0.8), CYAN, a, h=60, label="shown", value="120 fps")
    bar(x, 140, 680, 800, 0.5 * ease(x.since(0) / 0.8), AMBER, a, h=60, label="responds", value="60 fps")
    a1 = x.b(1)
    if a1 > 0:
        y = 1000
        x.text((140, 840), "newest real frame waits:", "mono", 36, WHITE, a1)
        frame_card(x, 260, y, True, a1, w=100, h=130)
        frame_card(x, 460, y, False, a1, w=100, h=130)
        # the held frame slides in late
        p = clamp(x.since(1) / 1.5)
        frame_card(x, 660 + 60 * (1 - p), y, True, a1 * (0.4 + 0.6 * p), w=100, h=130)
        x.text((860, y), "+ delay", "monob", 44, RED, a1, anchor="mm")
    a2 = x.b(2)
    if a2 > 0:
        label_box(x, CX, 1170, "paired with NVIDIA Reflex", GREEN, a2, 40)


# ---------- scene 5: AMD's base frame rate guidance ----------
def s_rule(x):
    a = x.b(0)
    x0, x1, y = 120, 960, 760
    span = 120.0

    def px(v):
        return x0 + (x1 - x0) * v / span
    zones = [(0, 30, RED, "avoid"), (30, 60, AMBER, "not ideal"), (60, 120, GREEN, "OK")]
    p = ease(x.since(0) / 1.2)
    for lo, hi, c, name in zones:
        if lo / span > p:
            continue
        hh = min(hi, span * p)
        x.d.rectangle([px(lo), y, px(hh), y + 90], fill=col(c, a * 0.85))
        x.text(((px(lo) + px(hi)) / 2, y + 150), name, "monob", 40, c, a, anchor="mm")
    for v in (0, 30, 60, 120):
        x.text((px(v), y - 30), str(v), "mono", 36, WHITE, a, anchor="md")
    x.text((CX, 560), "real fps BEFORE frame gen", "mono", 42, WHITE, a, anchor="mm")
    x.text((CX, 1100), "AMD: 60+ first, never < 30", "monob", 44, CYAN, a, anchor="mm")


# ---------- scene 6: smoothness, not speed ----------
def s_end(x):
    a = x.b(0)
    x.text((CX, 560), "smoothness", "monob", 90, CYAN, a, anchor="mm")
    x.text((CX, 680), "!= speed", "monob", 90, AMBER, a, anchor="mm")
    a1 = x.b(1)
    if a1 > 0:
        x.rect([160, 850, 920, 1150], CYAN, a1, 4, r=8, fill=PANEL + (255,))
        x.text((200, 890), "> next:", "mono", 36, MUTED, a1)
        x.text((CX, 990), "What Actually", "monob", 60, WHITE, a1, anchor="mm")
        x.text((CX, 1070), "Raises FPS", "monob", 60, WHITE, a1, anchor="mm")


SCENES = [
    ("Double the FPS?", s_hook),
    ("Real, guess, real", s_strip),
    ("Only real frames hear you", s_input),
    ("Looks like 120, feels like 60", s_feel),
    ("Start from 60 real FPS", s_rule),
    ("Smoothness, not speed", s_end),
]
