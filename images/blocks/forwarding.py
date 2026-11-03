"""Forwarding for operand A (HIPV rtl/core/hazard, rtl/core/ieu/ieu.sv): the
hazard unit compares register numbers and drives the 2-bit select ForwardAE;
fwdamux in the IEU picks the 32-bit operand FwdAE."""
from schemdraw import flow
from schemdraw import elements as elm
from _style import new_drawing, block, line, GREY


def arrow(d, a, b):
    d.add(elm.Arrow().at(a).to(b))


def dot(d, xy):
    d.add(elm.Dot().at(xy))


def label(d, xy, text, **kw):
    kw.setdefault("fontsize", 11)
    d.add(elm.Label().at(xy).label(text, **kw))


def dashed_box(d, l, r, t, b, name):
    for a, c in (((l, t), (r, t)), ((r, t), (r, b)), ((r, b), (l, b)), ((l, b), (l, t))):
        d.add(elm.Line().at(a).to(c).linestyle("--").color(GREY))
    label(d, (l + 0.2, t - 0.4), name, halign="left", color=GREY)


def draw():
    d = new_drawing()

    # ---------------- hazard unit ----------------
    hl, hr, ht, hb = 3.0, 8.0, 9.6, 5.8
    d.add(block(flow.Box(w=hr - hl, h=ht - hb)).at(((hl + hr) / 2, (ht + hb) / 2))
          .anchor("center").label("hazard unit\n\ncompares register\nnumbers only", fontsize=11))
    for y, name in ((9.0, "Rs1E"), (8.2, "RdM"), (7.4, "RegWriteM"),
                    (6.6, "RdW"), (5.8, "RegWriteW")):
        arrow(d, (hl - 2.0, y), (hl, y))
        label(d, (hl - 2.3, y), name, halign="right")

    # ---------------- fwdamux (inside the IEU) ----------------
    m = block(elm.Multiplexer(
        pins=[elm.IcPin(name="0", side="L", anchorname="in0", slot="3/3"),
              elm.IcPin(name="1", side="L", anchorname="in1", slot="2/3"),
              elm.IcPin(name="2", side="L", anchorname="in2", slot="1/3"),
              elm.IcPin(name="", side="R", anchorname="y"),
              elm.IcPin(name="", side="T", anchorname="sel")],
        size=(1.4, 4.0), pinspacing=1.2, leadlen=0))
    d.add(m.anchor("y").at((14.0, 0.0)))
    M = m.absanchors
    label(d, ((M["in0"][0] + M["y"][0]) / 2, M["in2"][1] - 2.1),
          "fwdamux\nmux3 #(32)", fontsize=9)
    for k, name in (("in0", "RD1E   (D/E register)"),
                    ("in1", "ResultW   (from W)"),
                    ("in2", "ForwardDataM   (from M)")):
        y = M[k][1]
        arrow(d, (8.6, y), M[k])
        label(d, (8.3, y), name, halign="right")

    # ForwardAE: hazard unit -> mux select
    ys = (ht + hb) / 2
    line(d, (hr, ys), (M["sel"][0], ys))
    arrow(d, (M["sel"][0], ys), M["sel"])
    label(d, ((hr + M["sel"][0]) / 2, ys + 0.35), "ForwardAE  (2 bits)", fontsize=10)
    label(d, (M["sel"][0] + 0.15, (ys + M["sel"][1]) / 2),
          "00  FWD_RF\n01  FWD_WB\n10  FWD_MEM", halign="left", fontsize=9, color=GREY)

    # FwdAE: to the three consumers
    xo = 16.4
    line(d, M["y"], (xo, M["y"][1]))
    label(d, ((M["y"][0] + xo) / 2 + 0.2, M["y"][1] + 0.35), "FwdAE  (32 bits)", fontsize=10)
    for y, name in ((1.6, "srcamux  (ALU operand A)"),
                    (0.0, "branchcmp  (operand A)"),
                    (-1.6, "rd1mux  (refresh while stalled)")):
        if y != 0.0:
            line(d, (xo, M["y"][1]), (xo, y))
        arrow(d, (xo, y), (xo + 1.6, y))
        label(d, (xo + 1.7, y), name, halign="left")
    dot(d, (xo, M["y"][1]))

    dashed_box(d, 9.6, 24.6, 3.6, -4.0, "ieu")
    return d
