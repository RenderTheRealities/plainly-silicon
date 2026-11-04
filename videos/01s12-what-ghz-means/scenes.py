"""Short 01s12: what GHz actually counts (vertical)."""
import math
from render import *  # noqa: F401,F403

SIZE = (1080, 1920)
CX = 540


def g_hook(x):
    chip_icon(x, CX, 760, 300, CYAN, x.b(0), 6, pins=5)
    x.text((CX, 760), "4 GHz", "title", 84, WHITE, x.b(0), anchor="mm")
    x.text((CX, 1110), "counting what?", "title", 56, AMBER, x.b(0) * ease(x.since(0) / 0.5 - 1.2), anchor="mm")


def metronome(x, a, speed=2.0):
    px, py = CX, 1050
    ang = -math.pi / 2 + 0.5 * math.sin(x.t * speed * math.pi)
    x.d.polygon([(px - 160, py), (px + 160, py), (px + 70, 520), (px - 70, 520)], outline=col(WHITE, a), width=5)
    x.line([(px, py - 40), (px + 420 * math.cos(ang), py - 40 + 420 * math.sin(ang))], CYAN, a, 7)
    return int(x.t * speed)


def g_tick(x):
    n = metronome(x, x.b(0))
    x.text((CX, 1160), f"tick {n}", "monob", 50, CYAN, x.b(1), anchor="mm")


def g_billions(x):
    a = x.b(0)
    x.text((CX, 600), "1 GHz = 1,000,000,000", "monob", 48, WHITE, a, anchor="mm")
    x.text((CX, 670), "ticks per second", "semi", 36, MUTED, a, anchor="mm")
    n = int(x.since(1) * 4_000_000_000) if x.b(1) > 0 else 0
    x.text((CX, 900), f"{n:,}", "monob", 56, AMBER, x.b(1), anchor="mm")
    x.text((CX, 980), "ticks so far", "semi", 36, MUTED, x.b(1), anchor="mm")


def work(x, y, ghz, per, c, a, label):
    x.text((140, y - 30), label, "semi", 38, c, a, anchor="ld")
    n = int(ghz * 3)
    for i in range(n):
        w = per * 24
        x.rect([140 + i * 50, y, 140 + i * 50 + 40, y + w], c, a, 3, r=4, glow=False, fill=c + (90,))


def g_ipc(x):
    a = x.b(1)
    work(x, 560, 5, 3, MUTED, a, "older chip · 5 GHz")
    work(x, 820, 4, 6, CYAN, a, "newer chip · 4 GHz")
    label_box(x, CX, 1180, "more work per tick", GREEN, x.b(2), 42)


def g_end(x):
    label_box(x, CX, 650, "GHz = how fast it ticks", CYAN, x.b(0), 46)
    label_box(x, CX, 800, "not work per tick", AMBER, ease((x.since(0) - 0.8) / 0.4), 46)
    label_box(x, CX, 1150, "More on the channel", GREEN, x.b(1), 40)


SCENES = [("What does 4 GHz mean?", g_hook), ("A clock that ticks", g_tick), ("Billions per second", g_billions),
          ("Faster ticks ≠ faster chip", g_ipc), ("The takeaway", g_end)]
