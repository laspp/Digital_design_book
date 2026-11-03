"""Writeback unit (HIPV rtl/core/wbu/wbu.sv): the M/W valid bit (ReadyW is
constant 1), the M/W pipeline registers (alureg, rdatareg, pcplus4reg,
ctrlreg), the result mux and the valid-qualified RegWriteW."""
from schemdraw import flow, logic
from schemdraw import elements as elm
from _style import new_drawing, block, line, GREY

XL, XR = 0.0, 23.0          # module boundary (left / right)
YT, YB = 12.6, -12.0


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


def flopenr(d, xy, name, width=32):
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
          f"{name}\nflopenr #({width})", fontsize=10)
    c = A["clk"]
    line(d, (c[0] - 0.6, c[1]), c)
    label(d, (c[0] - 0.7, c[1]), "clk", halign="right", fontsize=10, color=GREY)
    return A


def draw():
    d = new_drawing()

    # ---------------- handshake: ReadyW = 1, valid bit ----------------
    y_rw = 11.4
    label(d, (3.2, y_rw), "1", fontsize=12)
    port_out(d, y_rw, "ReadyW", 3.6)
    label(d, (8.0, y_rw + 0.35), "Writeback never stalls", fontsize=10, color=GREY)

    hl, hr, ht, hb = 3.0, 7.4, 10.2, 7.8
    d.add(block(flow.Box(w=hr - hl, h=ht - hb)).at(((hl + hr) / 2, (ht + hb) / 2))
          .anchor("center").label("valid bit\nValidW <= EnMW", fontsize=10))
    y_vm, y_vw, y_en = 9.0, 9.6, 8.4
    port_in(d, y_vm, "ValidM", hl)
    xv = 18.6
    line(d, (hr, y_vw), (xv, y_vw))
    dot(d, (xv, y_vw))
    port_out(d, y_vw, "ValidW", xv)

    # EnMW = ValidM & ReadyW = ValidM loads all four registers
    xen = 8.6
    line(d, (hr, y_en), (xen, y_en))
    label(d, (hr + 0.1, y_en - 0.3), "EnMW", halign="left", fontsize=10)

    # ---------------- M/W pipeline registers ----------------
    xd = 10.6
    A = flopenr(d, (xd, 5.6), "alureg")
    R = flopenr(d, (xd, 1.6), "rdatareg")
    P = flopenr(d, (xd, -2.4), "pcplus4reg")
    C = flopenr(d, (xd, -6.4), "ctrlreg", 8)
    port_in(d, A["D"][1], "ALUResultM", A["D"][0])
    port_in(d, R["D"][1], "ReadDataM", R["D"][0])
    port_in(d, P["D"][1], "PCPlus4M", P["D"][0])
    port_in(d, C["D"][1], "RegWriteM, RdM,\nResultSrcM", C["D"][0])
    line(d, (xen, y_en), (xen, C["en"][1]))
    for Q in (A, R, P, C):
        if Q is not C:
            dot(d, (xen, Q["en"][1]))
        arrow(d, (xen, Q["en"][1]), Q["en"])

    # ---------------- result mux ----------------
    m = block(elm.Multiplexer(
        pins=[elm.IcPin(name="0", side="L", anchorname="in0", slot="3/3"),
              elm.IcPin(name="1", side="L", anchorname="in1", slot="2/3"),
              elm.IcPin(name="2", side="L", anchorname="in2", slot="1/3"),
              elm.IcPin(name="", side="R", anchorname="y"),
              elm.IcPin(name="", side="B", anchorname="sel")],
        size=(1.4, 4.0), pinspacing=1.2, leadlen=0))
    d.add(m.anchor("in1").at((16.0, R["Q"][1])))
    M = m.absanchors
    label(d, ((M["in0"][0] + M["y"][0]) / 2, M["in0"][1] + 1.7),
          "resultmux\nmux3 #(32)", fontsize=9)
    xr = 14.6
    line(d, A["Q"], (xr, A["Q"][1]), (xr, M["in0"][1]))
    arrow(d, (xr, M["in0"][1]), M["in0"])
    arrow(d, R["Q"], M["in1"])
    line(d, P["Q"], (xr, P["Q"][1]), (xr, M["in2"][1]))
    arrow(d, (xr, M["in2"][1]), M["in2"])
    label(d, (A["Q"][0] + 0.2, A["Q"][1] + 0.3), "ALUResultW", halign="left", fontsize=10)
    label(d, (R["Q"][0] + 0.2, R["Q"][1] + 0.3), "ReadDataW", halign="left", fontsize=10)
    label(d, (P["Q"][0] + 0.2, P["Q"][1] + 0.3), "PCPlus4W", halign="left", fontsize=10)
    port_out(d, M["y"][1], "ResultW", M["y"][0])

    # ---------------- control fields ----------------
    q = C["Q"]
    xs = 13.4
    line(d, q, (xs, q[1]))
    dot(d, (xs, q[1]))
    # ResultSrcW: mux select
    s = M["sel"]
    line(d, (xs, q[1]), (s[0], q[1]))
    arrow(d, (s[0], q[1]), s)
    label(d, (s[0] + 0.15, (q[1] + s[1]) / 2), "ResultSrcW", halign="left", fontsize=10)
    # RdW
    y_rd = -8.4
    line(d, (xs, q[1]), (xs, y_rd))
    dot(d, (xs, y_rd))
    port_out(d, y_rd, "RdW", xs)

    # RegWriteW = RegWriteWReg & ValidW
    g = d.add(block(logic.And(inputs=2)).anchor("out").at((21.4, -10.4)))
    G = g.absanchors
    line(d, (xs, y_rd), (xs, G["in2"][1]))
    arrow(d, (xs, G["in2"][1]), G["in2"])
    label(d, (xs + 0.2, G["in2"][1] - 0.35), "RegWriteWReg", halign="left", fontsize=10)
    line(d, (xv, y_vw), (xv, G["in1"][1]))
    arrow(d, (xv, G["in1"][1]), G["in1"])
    port_out(d, G["out"][1], "RegWriteW", G["out"][0])

    # module boundary
    for a, b in (((XL, YT), (XR, YT)), ((XR, YT), (XR, YB)),
                 ((XR, YB), (XL, YB)), ((XL, YB), (XL, YT))):
        d.add(elm.Line().at(a).to(b).linestyle("--").color(GREY))
    label(d, (XL + 0.2, YT - 0.4), "wbu", halign="left", color=GREY)
    label(d, (XL + 0.2, YB + 0.4),
          "RegWriteW, RdW, ResultW drive the register file write port (Decode) and the hazard unit",
          halign="left", fontsize=10, color=GREY)
    return d
