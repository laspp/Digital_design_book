"""Instruction decode unit (HIPV rtl/core/idu/idu.sv): the F/D handshake and
valid bit, the F/D pipeline registers (instrreg, pcreg, pcplus4reg), the
control decoder (idudec), the immediate extension (extend) and the register
file (regfile)."""
from schemdraw import flow
from schemdraw import elements as elm
from _style import new_drawing, block, line, GREY

XL, XR = 0.0, 24.0          # module boundary (left / right)
YT, YB = 10.4, -15.0


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


def box(d, l, r, t, b, text, **kw):
    kw.setdefault("fontsize", 11)
    d.add(block(flow.Box(w=r - l, h=t - b)).at(((l + r) / 2, (t + b) / 2))
          .anchor("center").label(text, **kw))


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

    # ---------------- handshake logic and valid bit ----------------
    hl, hr, ht, hb = 2.6, 7.6, 9.6, 6.4
    box(d, hl, hr, ht, hb, "handshake\n+ valid bit\n(ValidDReg)")
    y_vf, y_src, y_re = 9.0, 8.0, 7.0
    port_in(d, y_vf, "ValidF", hl)
    port_in(d, y_src, "PCSrcE", hl)
    port_in(d, y_re, "ReadyE", hl)
    port_out(d, y_vf, "ValidD", hr)
    port_out(d, y_src, "ReadyD", hr)

    # ---------------- F/D pipeline registers ----------------
    xreg = 10.6
    I = flopenr(d, (xreg, 4.0), "instrreg")
    P = flopenr(d, (xreg, -8.0), "pcreg")
    P4 = flopenr(d, (xreg, -11.6), "pcplus4reg")
    port_in(d, I["D"][1], "InstrF", I["D"][0])
    port_in(d, P["D"][1], "PCF", P["D"][0])
    port_in(d, P4["D"][1], "PCPlus4F", P4["D"][0])
    port_out(d, P["Q"][1], "PCD", P["Q"][0])
    port_out(d, P4["Q"][1], "PCPlus4D", P4["Q"][0])

    # EnFD = ValidF & ReadyD loads all three registers
    xen = 9.0
    line(d, (hr, y_re), (xen, y_re), (xen, P4["en"][1]))
    label(d, (hr + 0.1, y_re + 0.3), "EnFD", halign="left", fontsize=10)
    for A in (I, P, P4):
        if A is not P4:
            dot(d, (xen, A["en"][1]))
        arrow(d, (xen, A["en"][1]), A["en"])

    # ---------------- InstrD bus ----------------
    xb = 14.2
    q = I["Q"]
    line(d, q, (xb, q[1]))
    dot(d, (xb, q[1]))
    label(d, (xb - 0.7, q[1] + 0.3), "InstrD", fontsize=10)
    y_dec, y_ext, y_fld, y_a1, y_a2 = 5.6, 1.0, -1.0, -2.6, -3.4
    line(d, (xb, y_dec), (xb, y_a2))
    for y in (y_ext, y_fld, y_a1):
        dot(d, (xb, y))

    # ---------------- control decoder ----------------
    cl, cr, ct, cb = 16.4, 21.0, 7.0, 3.6
    box(d, cl, cr, ct, cb, "idudec\n\nmain decoder\n+ ALU decoder")
    arrow(d, (xb, y_dec), (cl, y_dec))
    label(d, ((xb + cl) / 2, y_dec + 0.55), "op, funct3,\nfunct7[5]", fontsize=9)
    port_out(d, 5.3, "RegWriteD, MemWriteD, ResultSrcD,\n"
                     "BranchD, JumpD, JalrD,\n"
                     "ALUSrcAD, ALUSrcBD, ALUControlD", cr)

    # ---------------- immediate extension ----------------
    el, er, et, eb = 16.4, 21.0, 2.0, 0.0
    box(d, el, er, et, eb, "extend")
    xis = (el + er) / 2
    arrow(d, (xis, cb), (xis, et))
    label(d, (xis + 0.15, (cb + et) / 2), "ImmSrcD", halign="left", fontsize=10)
    arrow(d, (xb, y_ext), (el, y_ext))
    label(d, ((xb + el) / 2, y_ext + 0.3), "[31:7]", fontsize=9)
    port_out(d, y_ext, "ImmExtD", er)

    # ---------------- instruction fields ----------------
    port_out(d, y_fld, "Rs1D, Rs2D, RdD, Funct3D", xb)

    # ---------------- register file ----------------
    rl, rr, rt, rb = 16.4, 21.0, -1.8, -6.6
    box(d, rl, rr, rt, rb, "regfile\n32 × 32", fontsize=11)
    y_we, y_a3, y_wd = -4.4, -5.1, -5.8
    for y, pin in ((y_a1, "A1"), (y_a2, "A2"), (y_we, "WE3"), (y_a3, "A3"), (y_wd, "WD3")):
        label(d, (rl + 0.15, y), pin, halign="left", fontsize=9)
    for y, pin in ((y_a1, "RD1"), (y_a2, "RD2")):
        label(d, (rr - 0.15, y), pin, halign="right", fontsize=9)
    arrow(d, (xb, y_a1), (rl, y_a1))
    arrow(d, (xb, y_a2), (rl, y_a2))
    label(d, ((xb + rl) / 2, y_a1 + 0.3), "[19:15]", fontsize=9)
    label(d, ((xb + rl) / 2, y_a2 - 0.3), "[24:20]", fontsize=9)
    port_out(d, y_a1, "RD1D", rr)
    port_out(d, y_a2, "RD2D", rr)
    port_in(d, y_we, "RegWriteW", rl)
    port_in(d, y_a3, "RdW", rl)
    port_in(d, y_wd, "ResultW", rl)
    label(d, ((rl + rr) / 2 - 1.35, rb - 0.45), "from Writeback", fontsize=9, color=GREY)
    xc = (rl + rr) / 2 + 1.2
    line(d, (xc, rb - 0.6), (xc, rb))
    label(d, (xc, rb - 0.85), "clk", fontsize=10, color=GREY)

    # module boundary
    for a, b in (((XL, YT), (XR, YT)), ((XR, YT), (XR, YB)),
                 ((XR, YB), (XL, YB)), ((XL, YB), (XL, YT))):
        d.add(elm.Line().at(a).to(b).linestyle("--").color(GREY))
    label(d, (XL + 0.2, YT - 0.4), "idu", halign="left", color=GREY)
    label(d, (XL + 0.2, YB + 0.4), "clk and reset (synchronous) go to the valid bit and the registers",
          halign="left", fontsize=10, color=GREY)
    return d
