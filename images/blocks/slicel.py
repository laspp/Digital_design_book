"""SLICEL (Xilinx Series-7), simplified: four LUT6 lanes, carry chain, F7/F8 muxes,
FF/latch + FF-only registers per lane. Ported from the hand-drawn SVG, so all
coordinates below are in that drawing's pixels; P() converts them to schemdraw units.
"""
from schemdraw import elements as elm
from _style import new_drawing, block, line, RED, RED_FILL, GREY

K = 1 / 80          # pixels -> schemdraw units
FS = 0.62           # original font px -> schemdraw pt, tuned so text fits the boxes
LW = 1.1
INK = "#1f2937"


def P(x, y):
    return (x * K, -y * K)


def text(d, x, y, s, size=10.5, color=INK, align="center"):
    dx = -6 if align == "center" else 0      # Label centring sits ~6 px right of the target
    d.add(elm.Label().at(P(x + dx, y)).label(s, fontsize=size * FS, color=color, halign=align).zorder(5))


def box(d, x, y, w, h, title, sub=None, size=11.5, fill=None, edge=None, color=INK):
    el = elm.Ic(size=(w * K, h * K))
    styled = block(el, fill, edge) if fill else block(el)
    d.add(styled.linewidth(1.2).zorder(3).at(P(x, y + h)))
    if sub:
        text(d, x + w / 2, y + h / 2 - 8, title, size, color)
        text(d, x + w / 2, y + h / 2 + 9, sub, size - 2, color)
    else:
        text(d, x + w / 2, y + h / 2, title, size, color)


def seg(d, *pts):
    line(d, *[P(*p) for p in pts])


def arrow(d, a, b):
    d.add(elm.Arrow(arrowwidth=0.07, arrowlength=0.12).at(P(*a)).to(P(*b)))


def draw():
    d = new_drawing()
    d.config(lw=LW)
    d.add(elm.Line().at(P(0, 100)).to(P(0, 100)))      # reserve the drawing's full extent
    d.add(elm.Line().at(P(1010, 920)).to(P(1010, 920)))

    # ---- carry chain, with COUT up and CIN in from below ----
    box(d, 180, 160, 50, 570, "")
    d.add(elm.Label().at(P(205, 445)).label("Carry chain", fontsize=12.5 * FS, color=INK, rotate=90).zorder(5))
    arrow(d, (205, 160), (205, 134))
    text(d, 205, 122, "COUT → (to slice above)", 10.5, GREY)
    arrow(d, (205, 752), (205, 730))
    text(d, 205, 770, "CIN ← (from slice below)", 10.5, GREY)

    # ---- F7A / F8 / F7B muxes ----
    seg(d, (325, 310), (325, 420))
    seg(d, (325, 580), (325, 470))
    seg(d, (400, 445), (750, 445))
    text(d, 660, 437, "O8 → wide-function output (to routing)", 10.5, GREY, "left")
    box(d, 250, 260, 150, 50, "F7AMUX", "LUT A + LUT B → O7A", 11.5)
    box(d, 250, 420, 150, 50, "F8MUX", "O7A + O7B → O8", 11.5)
    box(d, 250, 580, 150, 50, "F7BMUX", "LUT C + LUT D → O7B", 11.5)

    # ---- the four lanes ----
    for name, cy, to_mux in (("A", 205, +70), ("B", 365, -70), ("C", 525, +70), ("D", 685, -70)):
        seg(d, (10, cy), (40, cy))
        text(d, 14, cy - 9, "6", 11, INK, "left")
        box(d, 40, cy - 45, 110, 90, f"LUT6 {name}", None, 12.5)
        seg(d, (150, cy), (180, cy))
        seg(d, (230, cy), (430, cy))
        d.add(elm.Dot(radius=0.035).at(P(245, cy)))
        seg(d, (245, cy), (245, cy + to_mux), (250, cy + to_mux))
        # combinational output and the bypass source
        seg(d, (270, cy), (270, cy - 43), (750, cy - 43))
        text(d, 756, cy - 39, f"{name} (combinational)", 10.5, INK, "left")
        # FF/Latch, then FF only (drawn on top of the Q line, as in the original)
        box(d, 430, cy - 35, 100, 70, "FF/Latch", f"({name}FF)", 11.5)
        seg(d, (530, cy), (750, cy))
        text(d, 756, cy + 4, f"{name}Q (registered)", 10.5, INK, "left")
        text(d, 610, cy - 55, "direct input (bypass)", 10, GREY)
        arrow(d, (610, cy - 50), (610, cy - 37))
        box(d, 560, cy - 35, 100, 70, "FF only", f"({name}2)", 11.5)
        seg(d, (660, cy), (660, cy + 43), (750, cy + 43))
        text(d, 756, cy + 47, f"{name}Q2 (bypass-reg.)", 10.5, INK, "left")

    # ---- shared clock and clock-enable ----
    text(d, 270, 798, "CLK (common to all 8 flip-flops)", 10.8, GREY)
    seg(d, (40, 806), (660, 806))
    text(d, 270, 822, "CE (common to all 8 flip-flops)", 10.8, GREY)
    seg(d, (40, 830), (660, 830))
    arrow(d, (480, 835), (480, 743))
    arrow(d, (610, 835), (610, 743))

    # ---- INIT / SR callout ----
    d.add(elm.Line().at(P(530, 700)).to(P(560, 855)).linestyle("--").color(RED).linewidth(1.2))
    box(d, 150, 855, 700, 50, "each of the 8 flip-flops also has its own INIT (init value) "
        "+ SR (set/reset) config bits", None, 11.2, RED_FILL, RED, "#7a2a1c")
    return d
