"""Short 01s15: '3 nm' is a name, not a measurement (vertical)."""
from render import *  # noqa: F401,F403

SIZE = (1080, 1920)
CX = 540


def j_hook(x):
    a = x.b(0)
    chip_icon(x, CX, 700, 300, CYAN, a, 6, pins=5)
    x.text((CX, 700), "3 nm", "title", 96, WHITE, a, anchor="mm")
    x.line([(200, 1000), (880, 1000)], AMBER, a, 5, glow=False)
    for i in range(11):
        x.line([(200 + i * 68, 1000), (200 + i * 68, 970)], AMBER, a, 3, glow=False)
    x.text((CX, 1100), "measuring… what?", "semi", 44, AMBER, a * ease(x.since(0) / 0.6 - 1), anchor="mm")


def j_past(x):
    a = x.b(0)
    x.text((CX, 500), "decades ago", "semi", 40, MUTED, a, anchor="mm")
    for k, (lab, w) in enumerate([("name", 600), ("real gate", 600)]):
        bar(x, 160, 700 + k * 200, 760, w / 760, CYAN if k == 0 else GREEN, a, 50, lab, "")
    label_box(x, CX, 1150, "number = real size", GREEN, x.b(0), 42)


def j_now(x):
    a = x.b(0)
    x.text((CX, 500), "today", "semi", 40, MUTED, a, anchor="mm")
    grow = ease(x.since(1) / 1.5) if x.b(1) > 0 else 0
    bar(x, 160, 700, 760, 0.05, CYAN, a, 50, "name: 3", "")
    bar(x, 160, 900, 760, 0.05 + 0.9 * grow, AMBER, a, 50, "real parts", "many times bigger")
    label_box(x, CX, 1150, "the link broke", RED, x.b(1), 42)


def j_label(x):
    a = x.b(0)
    label_box(x, CX, 500, "a generation label", CYAN, a, 46)
    for k, (nm, w) in enumerate([("company A · 3 nm", 0.8), ("company B · 3 nm", 0.6)]):
        bar(x, 160, 700 + k * 150, 760, w * ease(x.since(2) / 1.2) if x.b(2) > 0 else 0.02, CYAN if k == 0 else AMBER, x.b(2), 44, nm, "")
    b = x.b(3)
    x.text((CX, 1090), "10 nm became Intel 7", "title", 58, WHITE, b, anchor="mm")
    x.text((CX, 1170), "same process, new name", "semi", 36, MUTED, b, anchor="mm")


def j_end(x):
    label_box(x, CX, 700, "compare real performance", GREEN, x.b(0), 46)
    x.text((CX, 860), "not the number in the name", "semi", 40, WHITE, x.b(0), anchor="mm")
    label_box(x, CX, 1150, "More on the channel", GREEN, x.b(1), 40)


SCENES = [("What does 3 nm mean?", j_hook), ("Back then", j_past), ("Today", j_now),
          ("Just a label", j_label), ("What to compare", j_end)]
