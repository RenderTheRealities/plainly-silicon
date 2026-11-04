"""Short 01s10: why two RAM sticks beat one (vertical)."""
from render import *  # noqa: F401,F403

SIZE = (1080, 1920)
CX = 540


def stick(x, cx, y, a, label, c):
    x.rect([cx - 50, y, cx + 50, y + 380], c, a, 5, r=8, fill=PANEL + (255,))
    for k in range(4):
        x.rect([cx - 30, y + 30 + k * 85, cx + 30, y + 90 + k * 85], c, a, 3, r=4, glow=False)
    x.text((cx, y + 430), label, "monob", 34, c, a, anchor="mm")


def e_hook(x):
    stick(x, 200, 520, x.b(0), "8 GB", CYAN)
    stick(x, 360, 520, x.b(0), "8 GB", CYAN)
    x.text((540, 710), "vs", "title", 60, WHITE, x.b(0), anchor="mm")
    stick(x, 800, 520, x.b(0), "16 GB", AMBER)
    x.text((CX, 1140), "same total. why faster?", "title", 48, WHITE, x.b(1), anchor="mm")


def lanes(x, a, active):
    chip_icon(x, CX, 520, 160, WHITE, a, 5)
    x.text((CX, 520), "CPU", "title", 48, WHITE, a, anchor="mm")
    for k, lx in enumerate((400, 680)):
        on = k < active
        x.line([(lx, 640), (lx, 1180)], CYAN if on else MUTED, a, 10 if on else 4, glow=on)
        if on:
            for j in range(4):
                y = 650 + ((x.t * 260 + j * 135) % 520)
                x.rect([lx - 22, y, lx + 22, y + 34], AMBER, a, 0, r=6, fill=AMBER + (255,), glow=False)
        x.text((lx, 1220), f"channel {k + 1}", "semi", 34, CYAN if on else MUTED, a, anchor="mm")


def e_lanes(x):
    lanes(x, x.b(0), 2)


def e_one_two(x):
    lanes(x, x.b(0), 2 if x.b(1) > 0.5 else 1)


def e_bw(x):
    a = x.b(0)
    bar(x, 140, 680, 800, 0.5, MUTED, a, 50, "1 stick", "1× peak")
    bar(x, 140, 880, 800, ease(x.since(0) / 1.5), CYAN, a, 50, "2 sticks", "~2× peak")
    label_box(x, CX, 1120, "games + built-in graphics", AMBER, x.b(1), 40)


def e_slots(x):
    a = x.b(0)
    x.rect([200, 450, 880, 1100], WHITE, a, 4, r=14)
    for i in range(4):
        on = i in (1, 3)
        x.rect([300 + i * 135, 500, 360 + i * 135, 1000], GREEN if on else MUTED, a, 5 if on else 3, r=6, glow=on)
        x.text((330 + i * 135, 1012), str(i + 1), "monob", 40, GREEN if on else MUTED, a, anchor="mt")
    label_box(x, CX, 1190, "check your manual", GREEN, x.b(1), 40)


SCENES = [("2 × 8 GB vs 1 × 16 GB", e_hook), ("Memory channels", e_lanes), ("One stick vs two", e_one_two),
          ("Double the bandwidth", e_bw), ("Which slots?", e_slots)]
