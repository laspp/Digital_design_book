"""Variant of the brutalist cover with students building and learning the SoC.

Outputs images/cover/cover-students.svg, .pdf and .png.
Run:  python3 scripts/make_cover_students.py
"""
import random
from pathlib import Path

import cairosvg

OUT = Path(__file__).resolve().parent.parent / "images" / "cover"
W, H = 210, 297  # mm

# palette
CONCRETE = "#bdb6aa"
LIGHT = "#d9d3c7"
MID = "#9c958a"
SHADOW = "#57534d"
DARK = "#1e1d1b"
RED = "#c3262c"
RED_DARK = "#8e1a1f"

# oblique projection offset for side/top faces
DX, DY = 12, -8

random.seed(7)
el = []


def rect(x, y, w, h, fill, extra=""):
    el.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" fill="{fill}" {extra}/>')


def poly(pts, fill, extra=""):
    p = " ".join(f"{x:.2f},{y:.2f}" for x, y in pts)
    el.append(f'<polygon points="{p}" fill="{fill}" {extra}/>')


def text(x, y, s, size, fill, family="DIN Condensed", weight="bold", anchor="start", spacing=0, extra=""):
    el.append(
        f'<text x="{x}" y="{y}" font-family="{family}" font-weight="{weight}" font-size="{size}" '
        f'fill="{fill}" text-anchor="{anchor}" letter-spacing="{spacing}" {extra}>{s}</text>'
    )


def block(x, y, w, h, front=LIGHT, side=SHADOW, top=MID, dx=DX, dy=DY):
    """Oblique concrete box: front face at (x,y,w,h), side to the right, top above."""
    poly([(x, y), (x + w, y), (x + w + dx, y + dy), (x + dx, y + dy)], top)
    poly([(x + w, y), (x + w + dx, y + dy), (x + w + dx, y + h + dy), (x + w, y + h)], side)
    rect(x, y, w, h, front)


# ---------------------------------------------------------------- background
rect(0, 0, W, H, CONCRETE)
# board-formed concrete: plank seams with varying tone
y = 0.0
while y < 205:
    h = random.uniform(3.2, 4.4)
    rect(0, y, W, h, "#000", f'opacity="{random.uniform(0.0, 0.05):.3f}"')
    rect(0, y + h - 0.25, W, 0.25, "#000", 'opacity="0.10"')
    y += h

# ---------------------------------------------------------------- red sun
cx, cy, r = 128, 92, 58
el.append(f'<clipPath id="sun"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath>')
el.append('<g clip-path="url(#sun)">')
rect(cx - r, cy - r, 2 * r, 2 * r, RED)
# sunset slits in the lower half, getting wider toward the horizon
yy, gap = cy + 6, 1.0
while yy < cy + r:
    rect(cx - r, yy, 2 * r, gap, CONCRETE)
    yy += gap + 6.5 - gap * 1.2
    gap += 0.9
el.append("</g>")


def line(pts, color, width, extra=""):
    p = " ".join(f"{x:.2f},{y:.2f}" for x, y in pts)
    el.append(f'<polyline points="{p}" fill="none" stroke="{color}" stroke-width="{width}" {extra}/>')


# ---------------------------------------------------------------- crane (behind the building)
mx, mw, mtop = 178, 6, 18
line([(mx, 206), (mx, mtop)], DARK, 1.0)
line([(mx + mw, 206), (mx + mw, mtop)], DARK, 1.0)
zz = [(mx if i % 2 == 0 else mx + mw, 206 - i * 6) for i in range(int((206 - mtop) / 6) + 1)]
line(zz, DARK, 0.6)
# jib and counter-jib
jl, jr, jy = 118, 206, mtop
line([(jl, jy), (jr, jy)], DARK, 1.0)
line([(jl + 6, jy + 4), (jr, jy + 4)], DARK, 1.0)
line([(jl + 6 + i * 5, jy + (4 if i % 2 == 0 else 0)) for i in range(int((jr - jl - 6) / 5) + 1)], DARK, 0.5)
# A-frame and stays
apex = (mx + mw / 2, 11.5)
line([(mx, mtop), apex, (mx + mw, mtop)], DARK, 0.9)
line([(jl, jy), apex, (jr - 2, jy)], DARK, 0.4)
rect(jr - 12, jy + 4, 10, 7, SHADOW)  # counterweight
# trolley, cable and the block being lowered
hx = 150
rect(hx - 2.5, jy + 4, 5, 2, DARK)
line([(hx - 1, jy + 6), (hx - 1, 29)], DARK, 0.3)
line([(hx + 1, jy + 6), (hx + 1, 29)], DARK, 0.3)
line([(hx - 7, 33), (hx, 29), (hx + 7, 33)], DARK, 0.3)
block(hx - 9, 33, 18, 7, front=LIGHT, side=SHADOW, top=MID, dx=4, dy=-3)
text(hx, 38.6, "RV32M", 3.6, SHADOW, anchor="middle", spacing=0.3)

# ---------------------------------------------------------------- monument
GROUND = 206

# chip body raised on pilotis (the pins)
cx0, cw, ctop, ch = 28, 142, 150, 34
for i in range(14):
    px = cx0 + 4 + i * 10
    block(px, ctop + ch, 4, GROUND - ctop - ch, front=MID, side=DARK, top=MID, dx=4, dy=-3)
for i in range(3):  # pins along the receding side
    px = cx0 + cw + 3 + i * 3.4
    py = ctop + ch + DY * (3 + i * 3.4) / DX
    rect(px, py, 1.8, GROUND - py, SHADOW)
block(cx0, ctop, cw, ch)
# deep window slots on the chip face
for row in range(3):
    for col in range(11):
        sx = cx0 + 6 + col * 12
        sy = ctop + 5 + row * 10
        rect(sx, sy, 8.5, 5.2, DARK)
        rect(sx, sy, 8.5, 1.1, "#000", 'opacity="0.5"')
# pin-1 marker, cast into the top slab
el.append(f'<ellipse cx="{cx0 + 14}" cy="{ctop - 2.6}" rx="3.2" ry="1.6" fill="{SHADOW}"/>')

# central tower (the core)
tx, tw, ttop = 84, 26, 34
block(tx, ttop, tw, ctop - ttop - 4, front=LIGHT, side=SHADOW, top=MID)
# vertical ribs on the tower
for i in range(1, 4):
    rect(tx + i * tw / 4 - 0.5, ttop + 10, 1.0, ctop - ttop - 14, MID)

# five cantilevered pipeline stages, alternating left / right
stages = ["IF", "ID", "EX", "MEM", "WB"]
for i, name in enumerate(stages):
    sy = 44 + i * 20
    sh = 13
    if i % 2 == 0:
        sx, sw = tx - 30, tw + 30
    else:
        sx, sw = tx, tw + 34
    block(sx, sy, sw, sh)
    # ribbon window
    rect(sx + 3, sy + 3.5, sw - 6, 4.2, DARK)
    # stage label cast below the window
    lx = sx + 4 if i % 2 == 0 else sx + sw - 4
    text(lx, sy + sh - 1.3, name, 4.2, SHADOW, anchor="start" if i % 2 == 0 else "end", spacing=0.6)

# antenna / mast
block(tx + tw / 2 - 2, 14, 4, ttop - 14, front=MID, side=DARK, top=MID, dx=4, dy=-3)
block(tx + tw / 2 - 2.5, 12, 5, 4, front=RED, side=RED_DARK, top=RED, dx=4, dy=-3)

# ---------------------------------------------------------------- students
# Figures are drawn in a local frame: feet at (0, 0), head top near y = -100.
# Each shape is drawn twice: a light outline pass, then the fill pass.


def figure(x, y, s, shapes, outline=4.0, flip=False):
    el.append(f'<g transform="translate({x},{y}) scale({-s if flip else s},{s})">')
    for o in (True, False):
        for kind, *a in shapes:
            if kind == "poly":
                pts, col = a
                st = f'stroke="{LIGHT}" stroke-width="{outline}" stroke-linejoin="round"' if o else ""
                poly(pts, LIGHT if o else col, st)
            elif kind == "limb":
                pts, w, col = a
                line(pts, LIGHT if o else col, w + (outline if o else 0), 'stroke-linejoin="round" stroke-linecap="round"')
            elif kind == "circle":
                cx_, cy_, r_, col = a
                el.append(f'<circle cx="{cx_}" cy="{cy_}" r="{r_ + (outline / 2 if o else 0)}" fill="{LIGHT if o else col}"/>')
            elif kind == "rect":
                rx, ry, rw, rh, col = a
                st = f'stroke="{LIGHT}" stroke-width="{outline}"' if o else ""
                rect(rx, ry, rw, rh, LIGHT if o else col, st)
            elif kind == "text" and not o:
                tx_, ty_, s_, size, col = a
                text(tx_, ty_, s_, size, col, anchor="middle", spacing=0.5)
    el.append("</g>")


# Monument figures in the manner of partisan memorial sculpture: greatcoats,
# side caps with a star, broad strides, faceted two-tone "bronze" planes.
BRONZE = "#2a2723"
LIT = "#4a453e"
STRAP = "#161513"


def head(hx, hy):
    """Head in profile facing right with a titovka cap; hy is the chin line."""
    return [
        ("poly", [(hx - 3, hy - 1), (hx + 3, hy - 1), (hx + 4, hy + 4), (hx - 4, hy + 4)], BRONZE),
        ("poly", [(hx - 6, hy - 13), (hx + 5, hy - 14), (hx + 7, hy - 9), (hx + 9, hy - 6), (hx + 7, hy - 5),
                  (hx + 7, hy - 1), (hx + 3, hy), (hx - 4, hy - 1), (hx - 7, hy - 7)], BRONZE),
        ("poly", [(hx + 2, hy - 13), (hx + 5, hy - 14), (hx + 7, hy - 9), (hx + 9, hy - 6), (hx + 7, hy - 5),
                  (hx + 7, hy - 1), (hx + 3, hy)], LIT),
        ("poly", [(hx - 8, hy - 11), (hx + 7, hy - 13), (hx + 8, hy - 18), (hx - 5, hy - 20)], BRONZE),
        *chip(hx + 3, hy - 15.5, 3.4),
    ]


def chip(cx_, cy_, size):
    """Cap badge: a tiny IC with pins on all four sides."""
    b, p, n = size / 2, size * 0.28, 3
    shapes = [("rect", cx_ - b, cy_ - b, size, size, RED)]
    for i in range(n):
        o = -b + size * (i + 0.5) / n - 0.3
        shapes += [
            ("rect", cx_ + o, cy_ - b - p, 0.6, p, RED),
            ("rect", cx_ + o, cy_ + b, 0.6, p, RED),
            ("rect", cx_ - b - p, cy_ + o, p, 0.6, RED),
            ("rect", cx_ + b, cy_ + o, p, 0.6, RED),
        ]
    shapes.append(("rect", cx_ - b * 0.45, cy_ - b * 0.45, b * 0.9, b * 0.9, RED_DARK))
    return shapes


FLAG_BEARER = [
    ("poly", [(-9, -34), (-1, -34), (-15, -5), (-23, -7)], BRONZE),
    ("poly", [(-29, -6), (-15, -6), (-14, 0), (-30, 0)], BRONZE),
    ("poly", [(1, -34), (10, -34), (22, -6), (14, -4)], BRONZE),
    ("poly", [(6, -34), (10, -34), (22, -6), (18, -5)], LIT),
    ("poly", [(13, -7), (25, -7), (28, 0), (13, 0)], BRONZE),
    ("poly", [(-11, -54), (11, -54), (20, -26), (4, -31), (-18, -24)], BRONZE),
    ("poly", [(3, -54), (11, -54), (20, -26), (8, -30)], LIT),
    ("poly", [(-13, -80), (12, -81), (11, -52), (-11, -52)], BRONZE),
    ("poly", [(3, -81), (12, -81), (11, -52), (4, -52)], LIT),
    ("rect", -11, -57, 22, 3, STRAP),
    ("limb", [(-10, -79), (10, -56)], 1.6, STRAP),
    ("limb", [(-11, -77), (-19, -62), (-22, -51)], 7, BRONZE),
    ("circle", -22, -49, 3.8, BRONZE),
    *head(1, -81),
    ("limb", [(23, -60), (14, -170)], 2.2, STRAP),
    ("limb", [(10, -78), (17, -96), (19, -113)], 7, BRONZE),
    ("limb", [(13, -80), (19, -96)], 2.5, LIT),
    ("circle", 19, -115, 3.8, BRONZE),
    ("poly", [(14, -170), (-10, -177), (-34, -168), (-58, -175), (-51, -150), (-28, -144), (-6, -151), (16, -143)], RED),
    ("poly", [(-10, -177), (-34, -168), (-28, -144), (-6, -151)], RED_DARK),
    ("limb", [(-46, -163), (-40, -163), (-40, -155), (-32, -155), (-32, -163), (-24, -163),
              (-24, -155), (-16, -155), (-16, -163), (-8, -163), (-8, -157)], 1.8, LIGHT),
]

BUILDER = [
    ("poly", [(-9, -34), (-1, -34), (-18, -6), (-26, -8)], BRONZE),
    ("poly", [(-33, -7), (-18, -7), (-17, 0), (-34, 0)], BRONZE),
    ("poly", [(2, -34), (11, -34), (16, -5), (8, -5)], BRONZE),
    ("poly", [(7, -34), (11, -34), (16, -5), (12, -5)], LIT),
    ("poly", [(6, -7), (20, -7), (22, 0), (6, 0)], BRONZE),
    ("poly", [(-11, -54), (12, -54), (17, -27), (-17, -25)], BRONZE),
    ("poly", [(4, -54), (12, -54), (17, -27), (8, -28)], LIT),
    ("poly", [(-11, -77), (13, -80), (12, -52), (-10, -52)], BRONZE),
    ("poly", [(4, -79), (13, -80), (12, -52), (5, -52)], LIT),
    ("rect", -10, -57, 22, 3, STRAP),
    ("limb", [(-10, -75), (-18, -60), (-20, -49)], 7, BRONZE),
    ("circle", -20, -47, 3.8, BRONZE),
    *head(0, -80),
    ("poly", [(9, -98), (41, -98), (46, -102), (14, -102)], "#d8545a"),
    ("poly", [(41, -98), (46, -102), (46, -88), (41, -84)], RED_DARK),
    ("rect", 9, -98, 32, 14, RED),
    ("rect", 12, -95, 26, 2.2, STRAP),
    ("text", 25, -86.5, "ALU", 7.5, LIGHT),
    ("limb", [(11, -77), (22, -70), (29, -83)], 7, BRONZE),
    ("limb", [(14, -78), (22, -72)], 2.5, LIT),
]

KNEELER = [
    ("poly", [(-6, -40), (2, -40), (-4, -4), (-12, -6)], BRONZE),
    ("poly", [(-12, -7), (-3, -2), (-24, 0), (-27, -5)], BRONZE),
    ("poly", [(-10, -50), (8, -50), (10, -32), (-13, -28)], BRONZE),
    ("poly", [(-2, -43), (6, -35), (21, -33), (21, -43)], BRONZE),
    ("poly", [(13, -40), (21, -40), (21, -5), (13, -5)], BRONZE),
    ("poly", [(17, -40), (21, -40), (21, -5), (17, -5)], LIT),
    ("poly", [(12, -7), (26, -7), (28, 0), (12, 0)], BRONZE),
    ("poly", [(-11, -78), (10, -79), (8, -48), (-10, -48)], BRONZE),
    ("poly", [(2, -79), (10, -79), (8, -48), (3, -48)], LIT),
    ("rect", -10, -53, 19, 3, STRAP),
    *head(0, -80),
    ("limb", [(-9, -75), (-6, -58), (8, -52)], 6, BRONZE),
    ("limb", [(8, -76), (16, -60), (20, -51)], 6, BRONZE),
    ("poly", [(6, -55), (16, -51), (28, -57), (28, -48), (16, -43), (6, -47)], RED),
    ("limb", [(16, -51), (16, -43)], 0.8, RED_DARK),
]

POINTER = [
    ("poly", [(-8, -34), (0, -34), (-4, -5), (-12, -5)], BRONZE),
    ("poly", [(-17, -6), (-3, -6), (-2, 0), (-18, 0)], BRONZE),
    ("poly", [(1, -34), (9, -34), (12, -5), (4, -5)], BRONZE),
    ("poly", [(5, -34), (9, -34), (12, -5), (8, -5)], LIT),
    ("poly", [(3, -7), (16, -7), (18, 0), (3, 0)], BRONZE),
    ("poly", [(-11, -54), (11, -54), (14, -26), (-14, -26)], BRONZE),
    ("poly", [(3, -54), (11, -54), (14, -26), (7, -26)], LIT),
    ("poly", [(-12, -80), (12, -81), (11, -52), (-11, -52)], BRONZE),
    ("poly", [(3, -81), (12, -81), (11, -52), (4, -52)], LIT),
    ("rect", -11, -57, 22, 3, STRAP),
    ("limb", [(10, -79), (-9, -56)], 1.6, STRAP),
    ("limb", [(-10, -77), (-14, -61), (-11, -49)], 6.5, BRONZE),
    ("rect", -14, -58, 6, 16, LIGHT),
    ("rect", -14, -58, 6, 1.5, RED),
    *head(1, -81),
    ("limb", [(10, -78), (26, -92), (40, -105)], 6.5, BRONZE),
    ("limb", [(13, -80), (26, -91)], 2.2, LIT),
    ("limb", [(40, -105), (46, -110)], 2.2, BRONZE),
]

# studying an unrolled schematic
SCHOLAR = [
    ("poly", [(-8, -34), (0, -34), (-6, -5), (-14, -5)], BRONZE),
    ("poly", [(-19, -6), (-5, -6), (-4, 0), (-20, 0)], BRONZE),
    ("poly", [(1, -34), (9, -34), (14, -5), (6, -5)], BRONZE),
    ("poly", [(5, -34), (9, -34), (14, -5), (10, -5)], LIT),
    ("poly", [(5, -7), (18, -7), (20, 0), (5, 0)], BRONZE),
    ("poly", [(-11, -54), (11, -54), (15, -26), (-15, -26)], BRONZE),
    ("poly", [(3, -54), (11, -54), (15, -26), (7, -26)], LIT),
    ("poly", [(-12, -80), (12, -81), (11, -52), (-11, -52)], BRONZE),
    ("poly", [(3, -81), (12, -81), (11, -52), (4, -52)], LIT),
    ("rect", -11, -57, 22, 3, STRAP),
    *head(2, -81),
    ("limb", [(-10, -77), (-6, -62), (8, -62)], 6.5, BRONZE),
    ("limb", [(10, -78), (18, -66), (34, -66)], 6.5, BRONZE),
    ("poly", [(8, -76), (36, -78), (36, -56), (8, -54)], SHADOW),
    ("rect", 6, -76, 3, 22, MID),
    ("rect", 35, -78, 3, 22, MID),
    ("limb", [(11, -70), (16, -70)], 0.9, LIGHT),
    ("limb", [(11, -62), (16, -62)], 0.9, LIGHT),
    ("poly", [(16, -73), (22, -73), (25, -66), (22, -59), (16, -59)], RED),
    ("limb", [(25, -66), (33, -66), (33, -60)], 0.9, LIGHT),
    ("rect", 29, -62, 5, 5, LIGHT),
]

# stone pedestals, as under a memorial group
PED = 197
block(3, PED, 86, GROUND - PED, front=LIGHT, side=SHADOW, top=MID, dx=4, dy=-3)
block(142, PED + 1, 64, GROUND - PED - 1, front=LIGHT, side=SHADOW, top=MID, dx=4, dy=-3)

figure(18, PED, 0.5, BUILDER)
figure(48, PED, 0.5, FLAG_BEARER)
figure(72, PED, 0.5, SCHOLAR)
figure(196, PED + 1, 0.5, POINTER, flip=True)
figure(160, PED + 1, 0.5, KNEELER, flip=True)

# small crews at work up on the structure
figure(148, 59.5, 0.07, FLAG_BEARER, outline=6)   # ID roof, signalling the crane
figure(128, 99.5, 0.07, BUILDER, outline=6)       # MEM roof
figure(66, 79.5, 0.07, KNEELER, outline=6)        # EX roof
figure(134, 146, 0.075, SCHOLAR, outline=6)       # chip roof
figure(158, 146, 0.075, POINTER, outline=6, flip=True)

# ---------------------------------------------------------------- plinth + type
rect(0, GROUND, W, H - GROUND, DARK)

# clock waveform engraved along the horizon
wave = []
x, hi = 0.0, True
y_hi, y_lo = GROUND + 4, GROUND + 10
wave.append(f"M 0 {y_lo}")
while x < W:
    wave.append(f"L {x:.1f} {y_hi if hi else y_lo}")
    x += 7
    wave.append(f"L {x:.1f} {y_hi if hi else y_lo}")
    hi = not hi
el.append(f'<path d="{" ".join(wave)}" fill="none" stroke="{RED}" stroke-width="1.3" stroke-linejoin="miter"/>')

text(16, 233, "DESIGNING A", 13, LIGHT, spacing=3.2)
text(14, 268, "RISC-V SoC", 49, RED, spacing=0.5)
rect(16, 274, 178, 0.6, LIGHT)
text(16, 283, "COURSE MATERIAL FOR THE SUBJECT DIGITAL DESIGN", 6.2, LIGHT, spacing=1.0)
# top band with the author / edition stamp
rect(0, 0, W, 11, DARK)
text(16, 7.6, "RATKO PILIPOVIĆ", 5.4, LIGHT, spacing=1.6)
text(194, 7.6, "RV32I · 5-STAGE PIPELINE", 5.4, RED, anchor="end", spacing=1.6)

# ---------------------------------------------------------------- grain
for _ in range(4500):
    gx, gy = random.uniform(0, W), random.uniform(0, H)
    gr = random.uniform(0.05, 0.28)
    col = "#000" if random.random() < 0.7 else "#fff"
    el.append(f'<circle cx="{gx:.2f}" cy="{gy:.2f}" r="{gr:.2f}" fill="{col}" opacity="{random.uniform(0.08, 0.3):.2f}"/>')

svg = (
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}">\n'
    + "\n".join(el)
    + "\n</svg>\n"
)

OUT.mkdir(parents=True, exist_ok=True)
(OUT / "cover-students.svg").write_text(svg, encoding="utf-8")
cairosvg.svg2pdf(bytestring=svg.encode(), write_to=str(OUT / "cover-students.pdf"))
cairosvg.svg2png(bytestring=svg.encode(), write_to=str(OUT / "cover-students.png"), output_width=1654)
print("wrote", OUT)
