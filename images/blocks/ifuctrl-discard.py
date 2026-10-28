"""Generation of NextDiscardF in the IFU control FSM (HIPV ifuctrl.sv).

Priority as in the code: an arriving response (ObiRvalidF) clears the flag,
otherwise a redirect (PCSrcE) while a transaction is outstanding sets it,
otherwise it holds. Reset clears the register.
"""
from schemdraw import flow, logic
from schemdraw import elements as elm
from _style import new_drawing, block, line, dff, GREY


def arrow(d, *pts):
    if len(pts) > 2:
        line(d, *pts[:-1])
    d.add(elm.Arrow().at(pts[-2]).to(pts[-1]))


def label(d, xy, text, **kw):
    kw.setdefault("fontsize", 11)
    d.add(elm.Label().at(xy).label(text, **kw))


def mux2():
    return block(elm.Multiplexer(
        pins=[elm.IcPin(name="0", side="L", anchorname="in0", slot="2/2"),
              elm.IcPin(name="1", side="L", anchorname="in1", slot="1/2"),
              elm.IcPin(name="", side="R", anchorname="y"),
              elm.IcPin(name="", side="B", anchorname="sel")],
        size=(1.2, 2.2), pinspacing=1.2, leadlen=0))


def draw():
    d = new_drawing()

    # state decoding
    label(d, (-0.2, 3.0), "State", halign="right")
    line(d, (0, 3.0), (0.6, 3.0))
    d.add(elm.Dot().at((0.6, 3.0)))
    eq_req = d.add(block(flow.Box(w=2.6, h=0.8)).at((1.4, 4.0)).anchor("W")
                   .label("== REQUEST", fontsize=10))
    eq_wait = d.add(block(flow.Box(w=2.6, h=0.8)).at((1.4, 2.0)).anchor("W")
                    .label("== WAIT_RESP", fontsize=10))
    arrow(d, (0.6, 3.0), (0.6, 4.0), eq_req.W)
    arrow(d, (0.6, 3.0), (0.6, 2.0), eq_wait.W)

    # outstanding = (State == REQUEST & ObiGntF) | State == WAIT_RESP
    and1 = d.add(block(logic.And(inputs=2)).anchor("in2").at((5.0, 4.0)))
    line(d, eq_req.E, and1.in2)
    # ObiGntF runs above the REQUEST comparator to the AND gate
    label(d, (-0.2, 5.0), "ObiGntF", halign="right")
    line(d, (0, 5.0), (4.6, 5.0), (4.6, and1.in1[1]), and1.in1)
    or1 = d.add(block(logic.Or(inputs=2)).anchor("in1").at((7.4, and1.out[1] - 0.6)))
    line(d, and1.out, (6.9, and1.out[1]), (6.9, or1.in1[1]), or1.in1)
    line(d, eq_wait.E, (6.9 - 0.4, eq_wait.E[1]), (6.9 - 0.4, or1.in2[1]), or1.in2)
    label(d, (or1.out[0] + 0.1, or1.out[1] + 0.3), "outstanding", halign="left",
          fontsize=9, color=GREY)

    # set = PCSrcE & outstanding
    and2 = d.add(block(logic.And(inputs=2)).anchor("in1").at((10.6, or1.out[1])))
    line(d, or1.out, and2.in1)
    label(d, (-0.2, 0.6), "PCSrcE", halign="right")
    line(d, (0, 0.6), (10.0, 0.6), (10.0, and2.in2[1]), and2.in2)

    # priority muxes: set -> 1, then ObiRvalidF -> 0
    m1 = mux2()
    d.add(m1.anchor("in1").at((14.2, 4.6)))
    M1 = m1.absanchors
    label(d, (M1["in1"][0] - 0.5, M1["in1"][1]), "1", halign="right")
    line(d, (M1["in1"][0] - 0.4, M1["in1"][1]), M1["in1"])
    line(d, and2.out, (M1["sel"][0], and2.out[1]), M1["sel"])

    m2 = mux2()
    d.add(m2.anchor("in0").at((17.0, M1["y"][1])))
    M2 = m2.absanchors
    line(d, M1["y"], M2["in0"])
    label(d, (M2["in1"][0] - 0.5, M2["in1"][1]), "0", halign="right")
    line(d, (M2["in1"][0] - 0.4, M2["in1"][1]), M2["in1"])
    label(d, (-0.2, -0.4), "ObiRvalidF", halign="right")
    line(d, (0, -0.4), (M2["sel"][0], -0.4), M2["sel"])

    # DiscardF register
    ff = dff()
    d.add(ff.anchor("D").at((20.2, M2["y"][1])))
    F = ff.absanchors
    arrow(d, M2["y"], F["D"])
    label(d, ((M2["y"][0] + F["D"][0]) / 2, M2["y"][1] + 0.35), "NextDiscardF",
          fontsize=10)
    c = F["CLK"]
    line(d, (c[0] - 0.6, c[1]), c)
    label(d, (c[0] - 0.7, c[1]), "clk", halign="right", fontsize=10, color=GREY)
    label(d, ((F["D"][0] + F["Q"][0]) / 2, c[1] - 0.8), "reset: DiscardF <= 0",
          fontsize=9, color=GREY)

    # DiscardF output, fed back to the hold input of the first mux
    q = F["Q"]
    xq = q[0] + 0.8
    line(d, q, (xq, q[1]))
    d.add(elm.Dot().at((xq, q[1])))
    arrow(d, (xq, q[1]), (xq + 1.0, q[1]))
    label(d, (xq + 1.1, q[1]), "DiscardF", halign="left")
    y_fb = M1["in0"][1] + 1.4
    line(d, (xq, q[1]), (xq, y_fb), (M1["in0"][0] - 0.8, y_fb),
         (M1["in0"][0] - 0.8, M1["in0"][1]))
    arrow(d, (M1["in0"][0] - 0.8, M1["in0"][1]), M1["in0"])
    return d
