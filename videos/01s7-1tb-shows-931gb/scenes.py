"""Short 01s7: why a 1 TB drive shows 931 GB (vertical)."""
from render import *  # noqa: F401,F403

SIZE = (1080, 1920)
CX = 540


def b_hook(x):
    a = x.b(0)
    x.rect([140, 470, 500, 760], CYAN, a, 6, r=16, fill=PANEL + (255,))
    x.text((320, 615), "1 TB", "title", 90, CYAN, a, anchor="mm")
    x.text((320, 800), "on the box", "semi", 36, MUTED, a, anchor="mm")
    b = x.b(1)
    x.rect([580, 470, 940, 760], WHITE, b, 4, r=10)
    x.d.rectangle([580, 470, 940, 520], fill=col(MUTED, b * 0.5))
    x.text((760, 640), "931 GB", "title", 80, AMBER, b, anchor="mm")
    x.text((760, 800), "in Windows", "semi", 36, MUTED, b, anchor="mm")
    x.text((CX, 1050), "−69 GB ?", "title", 110, RED, x.b(2), anchor="mm")


def b_safe(x):
    a = x.b(0)
    x.circle(CX, 760, 200, GREEN, a, 10)
    x.line([(CX - 90, 760), (CX - 20, 840), (CX + 110, 670)], GREEN, a, 16)
    label_box(x, CX, 1100, "two ways of counting", WHITE, x.b(1), 46)


def ruler(x, y, ticks, c, a, label):
    x.line([(140, y), (940, y)], c, a, 5)
    for i in range(ticks + 1):
        tx = 140 + 800 * i / ticks
        x.line([(tx, y), (tx, y - (40 if i % 5 == 0 else 20))], c, a, 3, glow=False)
    x.text((140, y + 50), label, "semi", 34, c, a, anchor="lm")


def b_decimal(x):
    a = x.b(0)
    ruler(x, 700, 10, CYAN, a, "steps of 1,000")
    x.text((CX, 900), "1 TB =", "title", 60, WHITE, x.b(1), anchor="mm")
    x.text((CX, 1000), "1,000,000,000,000 bytes", "monob", 50, CYAN, x.b(1), anchor="mm")


def b_binary(x):
    a = x.b(0)
    x.text((CX, 520), "Windows' gigabyte", "semi", 40, MUTED, a, anchor="mm")
    x.text((CX, 610), "1,024 × 1,024 × 1,024", "monob", 52, AMBER, a, anchor="mm")
    x.text((CX, 690), "= 1,073,741,824 bytes", "monob", 40, WHITE, a, anchor="mm")
    b = x.b(1)
    x.text((CX, 870), "1,000,000,000,000", "monob", 46, CYAN, b, anchor="mm")
    x.line([(200, 920), (880, 920)], WHITE, b, 4, glow=False)
    x.text((CX, 970), "1,073,741,824", "monob", 46, AMBER, b, anchor="mm")
    x.text((CX, 1110), "≈ 931", "title", 110, GREEN, b * ease((x.since(1) - 0.8) / 0.5), anchor="mm")


def b_end(x):
    a = x.b(0)
    ruler(x, 640, 10, CYAN, a, "drive makers")
    ruler(x, 860, 8, AMBER, a, "Windows")
    label_box(x, CX, 1150, "your drive is the size on the box", GREEN, x.b(1), 40)


SCENES = [("Where did 69 GB go?", b_hook), ("Nothing is missing", b_safe), ("Counting in thousands", b_decimal),
          ("Counting in 1,024s", b_binary), ("Same bytes, different ruler", b_end)]
