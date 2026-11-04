"""Short 01s8: plug your monitor into the graphics card (vertical)."""
from render import *  # noqa: F401,F403

SIZE = (1080, 1920)
CX = 540
MB = (300, 470, 780, 640)   # motherboard I/O area
GP = (300, 960, 780, 1060)  # graphics card ports


def case_back(x, a):
    x.rect([240, 420, 840, 1250], WHITE, a, 5, r=18)
    x.rect(MB, CYAN, a, 3, r=8, glow=False)
    for i in range(4):
        x.rect([330 + i * 70, 500, 380 + i * 70, 530], MUTED, a, 2, r=3, glow=False)
    x.rect([620, 560, 700, 610], CYAN, a, 3, r=4, glow=False)
    x.rect(GP, AMBER, a, 3, r=8, glow=False)
    for i in range(3):
        x.rect([340 + i * 120, 990, 430 + i * 120, 1030], AMBER, a, 3, r=4, glow=False)


def c_hook(x):
    case_back(x, x.b(0))
    x.text((CX, 820), "which port?", "title", 64, WHITE, x.b(1), anchor="mm")


def c_two(x):
    case_back(x, x.b(0))
    label_box(x, CX, 700, "motherboard ports", CYAN, x.b(1), 38)
    label_box(x, CX, 1120, "graphics card ports", AMBER, x.b(2), 38)


def c_cpu(x):
    a = x.b(0)
    chip_icon(x, 300, 760, 220, CYAN, a, 5)
    x.text((300, 760), "CPU", "title", 54, CYAN, a, anchor="mm")
    x.text((300, 940), "built-in graphics", "semi", 34, WHITE, a, anchor="mm")
    x.rect([640, 650, 900, 870], CYAN, a, 4, r=10)
    x.text((770, 760), "ports", "semi", 40, CYAN, a, anchor="mm")
    x.line([(420, 760), (630, 760)], CYAN, a, 5)
    stamp(x, CX, 1130, "MAYBE NO SIGNAL", RED, x.b(1), angle=-5)


def c_wrong(x):
    case_back(x, x.b(0))
    x.line([(940, 1300), (940, 585), (705, 585)], RED, x.b(0), 8)
    x.text((CX, 1120), "z z z", "title", 46, MUTED, x.b(0), anchor="mm")
    label_box(x, CX, 820, "graphics card idle", RED, x.b(0), 40)


def c_right(x):
    case_back(x, x.b(0))
    x.line([(CX, 1250), (CX, 1180), (385, 1180), (385, 1030)], GREEN, x.b(0), 8)
    x.circle(CX, 780, 90, GREEN, x.b(1), 8)
    x.line([(CX - 40, 780), (CX - 10, 815), (CX + 50, 745)], GREEN, x.b(1), 10)


SCENES = [("Check your monitor cable", c_hook), ("Two sets of ports", c_two), ("Motherboard ports = CPU graphics", c_cpu),
          ("Plugged in wrong", c_wrong), ("Plug into the GPU", c_right)]
