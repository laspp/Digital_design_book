"""Four SLICEL lanes (A-D), LUT6 only, stacked vertically, plus the first
level of 2:1 muxes combining pairs of O6 outputs into a wider O7 function.

D is drawn at the top and A at the bottom, matching the lane order used in
Xilinx's own SLICEL documentation. One mux sits between D and C (its O7
comes from D's and C's O6), the other between A and B (its O7 comes from
B's and A's O6). Flip-flops come in a later step.
"""
from schemdraw import elements as elm
from _style import new_drawing, block, line, GREY
from _slicel import lut6_lane, HEIGHT

GAP = 0.2
STEP = HEIGHT + GAP
BOTTOM = -1.8
MUX_X = 4.0
MUX_W = 1.1          # a small trapezoid (like mux2.py), not stretched to
MUX_H = 2.0          # span the full gap between the two lanes it connects


def add_mux_at(d, x, top_pt, bot_pt, w, h, label=""):
    """A small 2:1 mux (elm.Multiplexer, as in mux2.py), centered between
    top_pt and bot_pt and connected to each via a bent wire (the mux is
    smaller than the gap between its two inputs, so each wire bends to
    meet it). pinspacing=h keeps the two input pins flush to the box's
    top/bottom edges (the default margin otherwise ignores box height).
    """
    cy = (top_pt[1] + bot_pt[1]) / 2
    mux = block(elm.Multiplexer(
        pins=[elm.IcPin(name="", side="L", anchorname="a", slot="2/2"),
              elm.IcPin(name="", side="L", anchorname="b", slot="1/2"),
              elm.IcPin(name=label, side="R", anchorname="y")],
        size=(w, h), pinspacing=h))
    d.add(mux.at((x, cy - h / 2)))
    ax, ay = mux.absanchors["a"]
    bx, by = mux.absanchors["b"]
    line(d, top_pt, (ax, top_pt[1]), (ax, ay))
    line(d, bot_pt, (bx, bot_pt[1]), (bx, by))
    return mux


def add_mux(d, top_lut, bot_lut):
    """First mux level: combines two lanes' O6 outputs into one O7."""
    return add_mux_at(d, MUX_X, top_lut.absanchors["o6"], bot_lut.absanchors["o6"],
                       MUX_W / 4, MUX_H / 2)


def draw():
    d = new_drawing()
    d.add(elm.Line().at((-2.6, 0)).to((-2.6, 0)))  # reserve room for labels

    luts = {}
    for i, name in enumerate("ABCD"):   # i=0 -> A (bottom) ... i=3 -> D (top)
        luts[name] = lut6_lane(d, name, BOTTOM + i * STEP)

    mux_dc = add_mux(d, luts["D"], luts["C"])
    mux_ab = add_mux(d, luts["B"], luts["A"])

    # second mux level: combines the two O7 outputs above into one O8
    add_mux_at(d, MUX_X + 2.0, mux_dc.absanchors["y"], mux_ab.absanchors["y"],
               MUX_W / 4, MUX_H / 2, label="")

    top = BOTTOM + 3 * STEP + HEIGHT
    d.add(elm.Label().at((1.2, top + 0.6)).label(
        "four SLICEL lanes + two mux levels (O6 -> O7 -> O8)", fontsize=11, color=GREY))
    return d
