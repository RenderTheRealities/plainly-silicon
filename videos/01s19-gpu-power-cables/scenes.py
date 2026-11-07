"""Short 01s19: why a graphics card needs extra PCIe power cables (vertical, graphite)."""
import math
from render import *  # noqa: F401,F403

SIZE = (1080, 1920)
CX = 540


def gpu(x, a, x0, y0, w=760, h=300, sockets=2, plugged=(False, False)):
    """Side view of a graphics card: shroud, two fans, gold slot fingers below, power sockets on top."""
    if a <= 0:
        return
    x.d.rounded_rectangle([x0, y0, x0 + w, y0 + h], radius=22, fill=col(PANEL, a), outline=col(WHITE, a), width=5)
    for k in range(2):
        fx, fy, r = x0 + w * (0.28 + 0.44 * k), y0 + h / 2, h * 0.36
        x.circle(fx, fy, r, MUTED, a, 4)
        for j in range(5):
            ang = x.t * 4 + j * 2 * math.pi / 5
            x.line([(fx, fy), (fx + r * 0.85 * math.cos(ang), fy + r * 0.85 * math.sin(ang))], MUTED, a, 5, glow=False)
        x.circle(fx, fy, 16, WHITE, a, 0, fill=WHITE)
    # slot fingers
    for k in range(0, int(w * 0.55), 16):
        x.d.rectangle([x0 + 60 + k, y0 + h, x0 + 70 + k, y0 + h + 34], fill=col(AMBER if False else MUTED, a))
    # power sockets on top edge
    out = []
    for k in range(sockets):
        sx = x0 + w - 260 + k * 130
        ok = plugged[k] if k < len(plugged) else False
        x.d.rectangle([sx, y0 - 40, sx + 100, y0], fill=col(GREEN if ok else NAVY, a), outline=col(WHITE, a), width=4)
        out.append((sx + 50, y0 - 40))
    return out


def pins(x, cx, cy, n, a, c, cell=44):
    """A connector face: a 2-row grid of square pins."""
    cols = n // 2
    w = cols * cell
    x.d.rounded_rectangle([cx - w / 2 - 18, cy - cell - 18, cx + w / 2 + 18, cy + cell + 18], radius=12,
                          fill=col(PANEL, a), outline=col(c, a), width=5)
    for r in range(2):
        for k in range(cols):
            px = cx - w / 2 + k * cell + cell / 2
            py = cy - cell / 2 + r * cell
            x.d.rectangle([px - 14, py - 14, px + 14, py + 14], fill=col(c, a * 0.9))


def g_hook(x):
    a = x.b(0)
    gpu(x, a, 160, 560, sockets=2)
    # motherboard slot under the card
    x.d.rectangle([200, 900, 720, 940], fill=col(GRID, a), outline=col(MUTED, a), width=3)
    x.text((460, 990), "PCIe slot", "semi", 38, MUTED, a, anchor="mm")
    # dangling cables swing toward the sockets
    s = x.since(0)
    for k in range(2):
        sx = 160 + 760 - 260 + k * 130 + 50
        sw = 30 * math.sin(s * 2 + k)
        ax = a * ease((s - 1.5) / 0.5)
        x.line([(sx + sw, 410), (sx + sw * 0.5, 450)], CYAN, ax, 20, glow=False)
        x.d.rectangle([sx + sw * 0.5 - 50, 450, sx + sw * 0.5 + 50, 490], fill=col(CYAN, ax))
    x.text((300, 470), "why these?", "title", 52, AMBER, a * ease((s - 2.2) / 0.5), anchor="mm")


def g_slot(x):
    a = x.b(0)
    # a tall watt scale 0..300, the slot fills only the bottom quarter
    x0, x1, top, base = 380, 700, 470, 1170
    x.d.rounded_rectangle([x0, top, x1, base], radius=20, outline=col(MUTED, a), width=4)
    for wv in (75, 150, 225, 300):
        y = base - (base - top) * wv / 300
        x.line([(x1 + 10, y), (x1 + 40, y)], MUTED, a, 3, glow=False)
        x.text((x1 + 56, y), f"{wv} W", "semi", 34, MUTED, a, anchor="lm")
    p = ease(x.since(0) / 1.4)
    hy = base - (base - top) * 0.25 * p
    if base - 8 - hy > 30:
        x.d.rounded_rectangle([x0 + 8, hy, x1 - 8, base - 8], radius=14, fill=col(CYAN, a))
    x.text((CX, hy - 50), f"{int(75 * p)} W", "title", 72, CYAN, a, anchor="mm")
    x.text((x0 - 30, base - 90), "slot", "title", 48, WHITE, a, anchor="rm")
    label_box(x, 230, 700, "small cards: OK", GREEN, x.b(1), 34)


def g_need(x):
    a = x.b(0)
    x0, x1, top, base = 380, 700, 470, 1170
    x.d.rounded_rectangle([x0, top, x1, base], radius=20, outline=col(MUTED, a), width=4)
    slot_y = base - (base - top) * 0.25
    x.d.rounded_rectangle([x0 + 8, slot_y, x1 - 8, base - 8], radius=14, fill=col(CYAN, a))
    x.text((CX, (slot_y + base) / 2), "75 W slot", "title", 44, NAVY, a, anchor="mm")
    # demand line rises to 300
    p = ease(x.since(0) / 2.0)
    dy = base - (base - top) * (0.25 + 0.75 * p)
    for k in range(x0 - 60, x1 + 30, 36):
        x.line([(k, dy), (k + 20, dy)], WHITE, a, 5, glow=False)
    x.text((x1 + 70, dy), f"{int(75 + 225 * p)} W", "title", 52, WHITE, a, anchor="lm")
    x.text((x1 + 70, dy + 56), "gaming", "semi", 32, MUTED, a, anchor="lm")
    # missing gap hatched in red
    a1 = x.b(1)
    if a1 > 0 and slot_y - dy > 30:
        x.rect([x0 + 8, dy, x1 - 8, slot_y], AMBER, a1, 5, r=10, glow=False)
        for k in range(int(dy), int(slot_y), 40):
            x.line([(x0 + 14, k + 30), (x0 + 50, k)], AMBER, a1 * 0.6, 3, glow=False)
        x.text((CX, (dy + slot_y) / 2 - 30), "from", "title", 46, AMBER, a1, anchor="mm")
        x.text((CX, (dy + slot_y) / 2 + 30), "the PSU", "title", 46, AMBER, a1, anchor="mm")


def g_conn(x):
    rows = [(1, 6, "6-pin", "75 W"), (2, 8, "8-pin", "150 W"), (3, 16, "12V-2x6", "600 W")]
    x.text((CX, 450), "rated power per connector", "semi", 38, MUTED, x.b(0), anchor="mm")
    for k, (beat, n, name, watts) in enumerate(rows):
        ab = x.b(beat)
        if ab <= 0:
            continue
        y = 600 + k * 230
        cell = 44 if n <= 8 else 30
        pins(x, 330, y, n if n <= 8 else 12, ab, WHITE if k < 2 else AMBER, cell)
        if n > 8:  # the four small sense pins above the 12V-2x6 power pins
            for j in range(4):
                x.d.rectangle([330 - 54 + j * 30, y - 76, 330 - 38 + j * 30, y - 64], fill=col(AMBER, ab))
        x.text((330, y + 90), name, "semi", 36, MUTED, ab, anchor="mm")
        x.text((960, y), watts, "title", 84, AMBER if k == 2 else WHITE, ab, anchor="rm")


def g_sum(x):
    a = x.b(0)
    blocks = [("slot", 75, CYAN), ("8-pin", 150, WHITE), ("8-pin", 150, WHITE)]
    base, scale, x0, x1 = 1200, 2.0, 300, 640
    y = base
    s = x.since(1)
    for k, (name, w, c) in enumerate(blocks):
        ab = a * x.b(1) * ease((s - k * 0.9) / 0.5) if k else a
        h = w * scale
        if ab > 0 and h * ease(ab) > 30:
            yy = y - h * ease(ab)
            x.d.rounded_rectangle([x0, yy + 4, x1, y - 4], radius=12, fill=col(c, ab))
            x.text(((x0 + x1) / 2, y - 45), f"{name}  {w} W", "title", 42, NAVY, ab, anchor="mm")
        y -= h
    # 300 W card line
    ly = base - 300 * scale
    for k in range(200, 900, 36):
        x.line([(k, ly), (k + 20, ly)], AMBER, a, 5, glow=False)
    x.text((880, ly - 34), "300 W card", "semi", 36, AMBER, a, anchor="rm")
    tot = 75 + 150 * ease(s / 0.6) + 150 * ease((s - 0.9) / 0.6) if x.b(1) > 0 else 75
    x.text((800, 1080), f"{int(tot)} W", "title", 90, GREEN if tot >= 300 else WHITE, a, anchor="mm")
    x.text((800, 1160), "total", "semi", 34, MUTED, a, anchor="mm")


def g_plug(x):
    a = x.b(0)
    s = x.since(0)
    p1 = ease(s / 0.8)
    plugged = (True, x.b(1) <= 0)  # second socket empty while the warning plays
    gpu(x, a, 160, 600, sockets=2, plugged=(p1 > 0.95, x.b(1) <= 0 and p1 > 0.95))
    # cables dropping into the sockets
    for k in range(2):
        sx = 160 + 760 - 260 + k * 130 + 50
        if k == 1 and x.b(1) > 0:
            continue
        cy = 440 + 120 * p1
        x.line([(sx, 420), (sx, cy)], CYAN, a, 14, glow=False)
        x.d.rectangle([sx - 46, cy, sx + 46, cy + 40], fill=col(CYAN, a))
    a1 = x.b(1) * (1 - x.b(2))
    if x.b(2) > 0:
        sx = 160 + 760 - 260 + 130 + 50
        x.line([(sx, 420), (sx, 560)], CYAN, x.b(2), 14, glow=False)
        x.d.rectangle([sx - 46, 560, sx + 46, 600], fill=col(CYAN, x.b(2)))
        label_box(x, CX, 1100, "every socket filled", GREEN, x.b(2), 42)
    if a1 > 0:
        sx = 160 + 760 - 260 + 130 + 50
        x.circle(sx, 480, 56, AMBER, a1, 6)
        x.text((sx, 480), "!", "title", 70, AMBER, a1, anchor="mm")
        label_box(x, CX, 1100, "crash  /  black screen", AMBER, a1, 42)
    if x.b(0) > 0 and x.b(1) <= 0:
        label_box(x, CX, 1100, "click!", GREEN, a * ease((s - 0.8) / 0.3), 48)
    label_box(x, CX, 1220, "More PC hardware on the channel", CYAN, x.b(2), 34)


SCENES = [("Why the extra cables?", g_hook), ("The slot: 75 W", g_slot), ("A card wants more", g_need),
          ("What each plug carries", g_conn), ("Add it up", g_sum), ("Plug in every one", g_plug)]
