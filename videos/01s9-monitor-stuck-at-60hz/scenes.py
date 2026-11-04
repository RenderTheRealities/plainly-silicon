"""Short 01s9: your 144 Hz monitor may be running at 60 (vertical)."""
from render import *  # noqa: F401,F403

SIZE = (1080, 1920)
CX = 540


def d_hook(x):
    a = x.b(0)
    x.rect([160, 480, 920, 920], WHITE, a, 6, r=16)
    x.line([(CX, 920), (CX, 1000)], WHITE, a, 8, glow=False)
    x.line([(400, 1000), (680, 1000)], WHITE, a, 8, glow=False)
    x.text((CX, 640), "144 Hz", "title", 120, CYAN, a, anchor="mm")
    s = ease(x.since(0) / 0.8 - 1)
    x.line([(250, 640), (250 + 580 * s, 640)], RED, a * (s > 0), 10)
    x.text((CX, 820), "running at 60 Hz?", "title", 60, RED, ease(x.since(0) / 0.6 - 1.5), anchor="mm")


def d_motion(x):
    a = x.b(0)
    for k, (hz, y, c) in enumerate([(60, 640, MUTED), (144, 960, CYAN)]):
        x.text((160, y - 120), f"{hz} Hz", "title", 52, c, a)
        x.line([(160, y), (920, y)], c, a * 0.4, 3, glow=False)
        steps = hz // 12
        p = (x.t * 0.45) % 1
        q = int(p * steps) / steps
        x.circle(160 + 760 * q, y, 34, c, a, 0, fill=c)
    x.text((CX, 1150), "higher = smoother", "semi", 44, WHITE, x.b(1), anchor="mm")


def dropdown(x, a, val, y=760):
    x.rect([200, y - 60, 880, y + 60], WHITE, a, 4, r=12, fill=PANEL + (255,))
    x.text((240, y), "Refresh rate", "semi", 38, MUTED, a, anchor="lm")
    x.text((840, y), val, "title", 48, CYAN if val != "60 Hz" else AMBER, a, anchor="rm")


def d_default(x):
    dropdown(x, x.b(0), "60 Hz")
    label_box(x, CX, 1000, "often the default", AMBER, x.b(1), 44)


def d_fix(x):
    path = ["Settings", "System", "Display", "Advanced display"]
    for i, p in enumerate(path):
        a = ease((x.since(0) - i * 0.5) / 0.4)
        label_box(x, CX, 460 + i * 105, p, WHITE, a, 40)
    dropdown(x, x.b(1), "144 Hz" if x.since(1) > 1.2 else "60 Hz", y=930)
    label_box(x, CX, 1150, "missing? try DisplayPort", AMBER, x.b(2), 38)


def d_end(x):
    x.text((CX, 700), "10 s", "title", 200, CYAN, x.b(0), anchor="mm")
    label_box(x, CX, 1150, "More on the channel", GREEN, x.b(1), 40)


SCENES = [("Stuck at 60 Hz?", d_hook), ("What refresh rate means", d_motion), ("Windows' default", d_default),
          ("The fix", d_fix), ("Worth 10 seconds", d_end)]
