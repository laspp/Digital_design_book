"""Generate the book cover (A4) in a Yugoslav/Soviet brutalist poster style.

Outputs images/cover/cover.svg, cover.pdf and cover.png.
Run:  python3 scripts/make_cover.py
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
(OUT / "cover.svg").write_text(svg, encoding="utf-8")
cairosvg.svg2pdf(bytestring=svg.encode(), write_to=str(OUT / "cover.pdf"))
cairosvg.svg2png(bytestring=svg.encode(), write_to=str(OUT / "cover.png"), output_width=1654)
print("wrote", OUT)
