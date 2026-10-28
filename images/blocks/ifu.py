"""Instruction fetch unit (HIPV rtl/core/ifu/ifu.sv): the ifuctrl FSM, the PC
loop (pcmux, pcreg, pcadd4) and the instruction register (instrreg)."""
from schemdraw import flow
from schemdraw import elements as elm
from _style import new_drawing, block, line, GREY

XL, XR = 0.0, 20.0          # module boundary (left / right)
YT, YB = 8.0, -9.6


def arrow(d, a, b):
    d.add(elm.Arrow().at(a).to(b))


def dot(d, xy):
    d.add(elm.Dot().at(xy))


def label(d, xy, text, **kw):
    kw.setdefault("fontsize", 11)
    d.add(elm.Label().at(xy).label(text, **kw))


def port_in(d, y, name, to):
    label(d, (XL - 0.4, y), name, halign="right")
    arrow(d, (XL - 0.1, y), (to, y))


def port_out(d, y, name, frm):
    arrow(d, (frm, y), (XR + 0.1, y))
    label(d, (XR + 0.4, y), name, halign="left")


def flopenr(d, xy, name):
    """flopenr with D, en and clock on the left, Q on the right; xy is the D pin."""
    r = block(elm.Ic(
        pins=[elm.IcPin(name="D", side="L", anchorname="D", slot="3/3"),
              elm.IcPin(name="en", side="L", anchorname="en", slot="2/3"),
              elm.IcPin(name=">", side="L", anchorname="clk", slot="1/3"),
              elm.IcPin(name="Q", side="R", anchorname="Q", slot="3/3")],
        size=(2.2, 2.8), pinspacing=0.9, leadlen=0))
    d.add(r.anchor("D").at(xy))
    A = r.absanchors
    label(d, ((A["D"][0] + A["Q"][0]) / 2, A["clk"][1] - 0.95),
          f"{name}\nflopenr #(32)", fontsize=10)
    c = A["clk"]
    line(d, (c[0] - 0.6, c[1]), c)
    label(d, (c[0] - 0.7, c[1]), "clk", halign="right", fontsize=10, color=GREY)
    return A


def draw():
    d = new_drawing()

    # ---------------- control FSM ----------------
    cl, cr, ct, cb = 4.6, 9.6, 6.9, 2.9
    d.add(block(flow.Box(w=cr - cl, h=ct - cb)).at(((cl + cr) / 2, (ct + cb) / 2))
          .anchor("center")
          .label("ifuctrl\n(FSM)\n\nREQUEST\nWAIT_RESP\nDONE", fontsize=11))
    y_gnt, y_rv, y_rdy, y_src = 6.3, 5.5, 4.7, 3.5
    port_in(d, y_gnt, "ObiGntF", cl)
    port_in(d, y_rv, "ObiRvalidF", cl)
    port_in(d, y_rdy, "ReadyD", cl)
    port_in(d, y_src, "PCSrcE", cl)
    y_req, y_val, y_pcen, y_ien = 6.3, 5.5, 4.5, 3.3
    port_out(d, y_req, "ObiReqF", cr)
    port_out(d, y_val, "ValidF", cr)

    # ---------------- PC loop ----------------
    mux = block(elm.Multiplexer(
        pins=[elm.IcPin(name="0", side="L", anchorname="in0", slot="1/2"),
              elm.IcPin(name="1", side="L", anchorname="in1", slot="2/2"),
              elm.IcPin(name="", side="R", anchorname="y"),
              elm.IcPin(name="", side="T", anchorname="sel")],
        size=(1.4, 2.8), pinspacing=1.4, leadlen=0))
    d.add(mux.anchor("y").at((4.4, 0.0)))
    M = mux.absanchors
    label(d, (M["y"][0] - 0.7, M["in0"][1] - 1.9), "pcmux\nmux2 #(32)", fontsize=10)
    dot(d, (M["sel"][0], y_src))
    arrow(d, (M["sel"][0], y_src), M["sel"])
    port_in(d, M["in1"][1], "PCTargetE", M["in1"][0])

    P = flopenr(d, (11.4, 0.0), "pcreg")
    arrow(d, M["y"], P["D"])
    label(d, (7.2, 0.3), "PCNextF")

    # PCEnF from the FSM to the PC register enable
    x_pcen = 10.4
    line(d, (cr, y_pcen), (x_pcen, y_pcen), (x_pcen, P["en"][1]))
    arrow(d, (x_pcen, P["en"][1]), P["en"])
    label(d, (cr + 0.1, y_pcen + 0.3), "PCEnF", halign="left", fontsize=10)

    # PCF to ObiAddrF, the PCF output and the adder
    q = P["Q"]
    jx = 14.6
    line(d, q, (jx, q[1]))
    dot(d, (jx, q[1]))
    port_out(d, q[1], "PCF", jx)
    line(d, (jx, q[1]), (jx, 1.4))
    port_out(d, 1.4, "ObiAddrF", jx)

    al, ar, ay = 15.8, 17.4, -2.6
    d.add(block(flow.Box(w=ar - al, h=2.0)).at(((al + ar) / 2, ay)).anchor("center")
          .label("+", fontsize=16))
    label(d, ((al + ar) / 2, ay - 1.4), "pcadd4\nadder #(32)", fontsize=10)
    line(d, (jx, q[1]), (jx, ay + 0.5))
    arrow(d, (jx, ay + 0.5), (al, ay + 0.5))
    label(d, (al - 1.1, ay - 0.5), "4", halign="right")
    arrow(d, (al - 1.0, ay - 0.5), (al, ay - 0.5))
    yx = 18.4
    line(d, (ar, ay), (yx, ay))
    dot(d, (yx, ay))
    port_out(d, ay, "PCPlus4F", yx)
    # PCPlus4F feedback to mux input 0
    yfb = -4.9
    fx = M["in0"][0] - 1.0
    line(d, (yx, ay), (yx, yfb), (fx, yfb), (fx, M["in0"][1]))
    arrow(d, (fx, M["in0"][1]), M["in0"])
    label(d, (7.2, yfb + 0.3), "PCPlus4F", fontsize=10)

    # ---------------- instruction register ----------------
    I = flopenr(d, (11.4, -6.4), "instrreg")
    port_in(d, I["D"][1], "ObiRdataF", I["D"][0])
    x_ien = 9.9
    line(d, (cr, y_ien), (x_ien, y_ien), (x_ien, I["en"][1]))
    arrow(d, (x_ien, I["en"][1]), I["en"])
    label(d, (cr + 0.1, y_ien + 0.3), "InstrEnF", halign="left", fontsize=10)
    port_out(d, I["Q"][1], "InstrF", I["Q"][0])

    # module boundary
    for a, b in (((XL, YT), (XR, YT)), ((XR, YT), (XR, YB)),
                 ((XR, YB), (XL, YB)), ((XL, YB), (XL, YT))):
        d.add(elm.Line().at(a).to(b).linestyle("--").color(GREY))
    label(d, (XL + 0.2, YT - 0.4), "ifu", halign="left", color=GREY)
    label(d, (XL + 0.2, YB + 0.4), "clk and reset (synchronous) go to ifuctrl and both registers",
          halign="left", fontsize=10, color=GREY)
    return d
