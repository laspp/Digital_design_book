"""Hazard unit (HIPV rtl/core/hazard/hazard.sv): for each Execute operand,
compare the source register with RdM and RdW, qualify with RegWrite and
rs != x0, and select M over W (the newest value) over the register file."""
from schemdraw import flow, logic
from schemdraw import elements as elm
from _style import new_drawing, block, line, GREY


def arrow(d, a, b):
    d.add(elm.Arrow().at(a).to(b))


def dot(d, xy):
    d.add(elm.Dot().at(xy))


def label(d, xy, text, **kw):
    kw.setdefault("fontsize", 11)
    d.add(elm.Label().at(xy).label(text, **kw))


def box(d, l, r, t, b, text, **kw):
    kw.setdefault("fontsize", 11)
    d.add(block(flow.Box(w=r - l, h=t - b)).at(((l + r) / 2, (t + b) / 2))
          .anchor("center").label(text, **kw))


def operand(d, y0, rs, fwd, title):
    """Forwarding logic for one operand, centred on y0."""
    label(d, (-1.8, y0 + 4.9), title, halign="left", color=GREY)

    # comparators
    bl, br = 3.0, 5.0
    box(d, bl, br, y0 + 3.6, y0 + 2.2, "=", fontsize=14)
    box(d, bl, br, y0 + 0.7, y0 - 0.7, "≠ 0", fontsize=12)
    box(d, bl, br, y0 - 2.2, y0 - 3.6, "=", fontsize=14)

    # rs fans out to all three
    xb = 1.6
    label(d, (-0.4, y0), rs, halign="right")
    line(d, (-0.1, y0), (xb, y0))
    line(d, (xb, y0 + 3.3), (xb, y0 - 2.5))
    dot(d, (xb, y0))
    for y in (y0 + 3.3, y0, y0 - 2.5):
        if y != y0:
            dot(d, (xb, y))
        arrow(d, (xb, y), (bl, y))
    for y, name in ((y0 + 2.5, "RdM"), (y0 - 3.3, "RdW")):
        label(d, (-0.4, y), name, halign="right")
        arrow(d, (-0.1, y), (bl, y))

    # AND gates: MatchM = RegWriteM & (rs == RdM) & (rs != 0), same for W
    gm = d.add(block(logic.And(inputs=3)).anchor("out").at((10.4, y0 + 2.4)))
    gw = d.add(block(logic.And(inputs=3)).anchor("out").at((10.4, y0 - 2.4)))
    M, W = gm.absanchors, gw.absanchors

    xe = 6.9
    line(d, (br, y0 + 2.9), (xe, y0 + 2.9), (xe, M["in2"][1]))
    arrow(d, (xe, M["in2"][1]), M["in2"])
    line(d, (br, y0 - 2.9), (xe, y0 - 2.9), (xe, W["in2"][1]))
    arrow(d, (xe, W["in2"][1]), W["in2"])

    xn = 6.2
    line(d, (br, y0), (xn, y0))
    dot(d, (xn, y0))
    line(d, (xn, y0), (xn, M["in3"][1]))
    arrow(d, (xn, M["in3"][1]), M["in3"])
    line(d, (xn, y0), (xn, W["in1"][1]))
    arrow(d, (xn, W["in1"][1]), W["in1"])

    xr = 7.6
    line(d, (xr, y0 + 4.3), (xr, M["in1"][1]))
    arrow(d, (xr, M["in1"][1]), M["in1"])
    label(d, (xr, y0 + 4.6), "RegWriteM")
    line(d, (xr, y0 - 4.3), (xr, W["in3"][1]))
    arrow(d, (xr, W["in3"][1]), W["in3"])
    label(d, (xr, y0 - 4.6), "RegWriteW")

    # priority select: M (newest) before W before the register file
    pl, pr = 12.6, 18.4
    box(d, pl, pr, y0 + 3.2, y0 - 3.2,
        "priority select\n\nMatchM → 10  FWD_MEM\nMatchW → 01  FWD_WB\nelse      → 00  FWD_RF",
        fontsize=10)
    arrow(d, M["out"], (pl, M["out"][1]))
    arrow(d, W["out"], (pl, W["out"][1]))
    label(d, ((M["out"][0] + pl) / 2, M["out"][1] + 0.3), "MatchM", fontsize=10)
    label(d, ((W["out"][0] + pl) / 2, W["out"][1] + 0.3), "MatchW", fontsize=10)
    arrow(d, (pr, y0), (pr + 1.6, y0))
    label(d, (pr + 1.7, y0), fwd, halign="left")


def draw():
    d = new_drawing()
    operand(d, 5.6, "Rs1E", "ForwardAE", "operand A")
    operand(d, -6.4, "Rs2E", "ForwardBE", "operand B")
    label(d, (-1.8, -12.6),
          "RegWriteM and RegWriteW are already qualified with the stage valid bits (LSU, WBU)",
          halign="left", fontsize=10, color=GREY)
    return d
