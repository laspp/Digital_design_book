"""Integer execution unit (HIPV rtl/core/ieu/ieu.sv): the D/E handshake and
valid bit, the D/E pipeline registers, the forwarding muxes (fwdamux,
fwdbmux), the ALU source muxes (srcamux, srcbmux), the ALU, the branch
comparator (branchcmp), the target adder and mux, and the redirect logic."""
from schemdraw import flow
from schemdraw import elements as elm
from schemdraw.backends import svg, svgtext
from _style import new_drawing, block, line, GREY

# schemdraw's text-size estimate parses labels as XML and fails on '&';
# measure with a same-width stand-in instead (the drawn text is unchanged).
_text_approx_size = svgtext.text_approx_size


def _text_size_amp(text, *args, **kw):
    return _text_approx_size(text.replace("&", "8"), *args, **kw)


svgtext.text_approx_size = svg.text_approx_size = _text_size_amp

XL, XR = 0.0, 31.0          # module boundary (left / right)
YT, YB = 16.4, -15.0


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


def stub_in(d, pin, name):
    """Short input arrow from the left into pin, labelled with its source."""
    x, y = pin
    arrow(d, (x - 1.2, y), pin)
    label(d, (x - 1.3, y), name, halign="right", fontsize=9)


def stub_sel(d, pin, name, up=True):
    """Short select arrow into a mux from above (up=True) or below."""
    x, y = pin
    s = 0.9 if up else -0.9
    arrow(d, (x, y + s), pin)
    label(d, (x, y + s + (0.3 if up else -0.3)), name, fontsize=9)


def mux(d, out, n, name, sel="T"):
    """n-input mux with the output at out; returns the absolute anchors."""
    pins = [elm.IcPin(name=str(i), side="L", anchorname=f"in{i}", slot=f"{n - i}/{n}")
            for i in range(n)]
    pins += [elm.IcPin(name="", side="R", anchorname="y"),
             elm.IcPin(name="", side=sel, anchorname="sel")]
    m = block(elm.Multiplexer(pins=pins, size=(1.4, 1.2 * n + 0.4),
                              pinspacing=1.2, leadlen=0))
    d.add(m.anchor("y").at(out))
    A = m.absanchors
    yl = (A["in0"][1] + 1.7) if sel == "B" else (A[f"in{n - 1}"][1] - 1.7)
    label(d, ((A["in0"][0] + A["y"][0]) / 2, yl),
          f"{name}\nmux{n} #(32)", fontsize=9)
    return A


def draw():
    d = new_drawing()

    # ---------------- handshake logic and valid bit ----------------
    hl, hr, ht, hb = 2.2, 7.2, 15.2, 12.4
    box(d, hl, hr, ht, hb, "handshake\n+ valid bit\n(ValidEReg)")
    y_vd, y_rm = 14.4, 13.2
    port_in(d, y_vd, "ValidD", hl)
    port_in(d, y_rm, "ReadyM", hl)
    port_out(d, y_vd, "ValidE", hr)
    port_out(d, y_rm, "ReadyE", hr)

    # ---------------- D/E pipeline registers ----------------
    gl, gr, gt, gb = 3.0, 6.4, 11.0, -14.0
    box(d, gl, gr, gt, gb, "D/E\nregisters\n\nflopenr\n× 8")
    xen = (gl + gr) / 2
    arrow(d, (xen, hb), (xen, gt))
    label(d, (xen + 0.15, (hb + gt) / 2), "EnDE", halign="left", fontsize=10)
    port_in(d, -6.0, "from IDU:\nRD1D, RD2D,\nImmExtD,\nPCD, PCPlus4D,\nRs1D, Rs2D, RdD,\n"
                     "Funct3D,\ncontrols", gl)

    # ---------------- forwarding muxes ----------------
    FA = mux(d, (13.0, 8.0), 3, "fwdamux")
    FB = mux(d, (13.0, 1.0), 3, "fwdbmux", sel="B")
    arrow(d, (gr, FA["in0"][1]), FA["in0"])
    arrow(d, (gr, FB["in0"][1]), FB["in0"])
    label(d, (gr + 0.2, FA["in0"][1] + 0.3), "RD1E", halign="left", fontsize=10)
    label(d, (gr + 0.2, FB["in0"][1] + 0.3), "RD2E", halign="left", fontsize=10)
    for A in (FA, FB):
        stub_in(d, A["in1"], "ResultW")
        stub_in(d, A["in2"], "ForwardDataM")
    stub_sel(d, FA["sel"], "ForwardAE")
    stub_sel(d, FB["sel"], "ForwardBE", up=False)

    # ---------------- ALU source muxes ----------------
    SA = mux(d, (18.2, 7.0), 3, "srcamux")
    SB = mux(d, (18.2, 0.4), 2, "srcbmux")
    stub_sel(d, SA["sel"], "ALUSrcAE")
    stub_sel(d, SB["sel"], "ALUSrcBE")
    stub_in(d, SA["in2"], "0")

    # FwdAE: to srcamux and down to the branch comparator
    xfa = 14.5
    line(d, FA["y"], (xfa, FA["y"][1]), (xfa, SA["in0"][1]))
    arrow(d, (xfa, SA["in0"][1]), SA["in0"])
    label(d, (xfa - 0.75, FA["y"][1] + 0.3), "FwdAE", fontsize=10)

    # WriteDataE: to srcbmux, the branch comparator and the Memory stage
    xwd = 15.5
    line(d, FB["y"], (xwd, FB["y"][1]), (xwd, SB["in0"][1]))
    arrow(d, (xwd, SB["in0"][1]), SB["in0"])
    label(d, (xwd - 0.9, FB["y"][1] + 0.3), "WriteDataE", fontsize=10)

    # PCE and ImmExtE: to the source muxes and down to the target adder
    xpc, xim, xs = 7.2, 7.8, 16.0
    y_pc, y_im = 4.6, -1.2
    line(d, (gr, y_pc), (xs, y_pc), (xs, SA["in1"][1]))
    arrow(d, (xs, SA["in1"][1]), SA["in1"])
    label(d, (gr + 0.2, y_pc + 0.3), "PCE", halign="left", fontsize=10)
    line(d, (gr, y_im), (xs, y_im), (xs, SB["in1"][1]))
    arrow(d, (xs, SB["in1"][1]), SB["in1"])
    label(d, (xim + 0.3, y_im - 0.3), "ImmExtE", halign="left", fontsize=10)
    dot(d, (xpc, y_pc))
    dot(d, (xim, y_im))

    # ---------------- ALU ----------------
    al, ar, at, ab = 20.2, 22.2, 8.6, -1.2
    box(d, al, ar, at, ab, "alu")
    arrow(d, SA["y"], (al, SA["y"][1]))
    arrow(d, SB["y"], (al, SB["y"][1]))
    label(d, ((SA["y"][0] + al) / 2, SA["y"][1] + 0.3), "SrcAE", fontsize=10)
    label(d, ((SB["y"][0] + al) / 2, SB["y"][1] + 0.3), "SrcBE", fontsize=10)
    xac = (al + ar) / 2
    arrow(d, (xac, at + 0.9), (xac, at))
    label(d, (xac, at + 1.2), "ALUControlE", fontsize=9)
    y_res, xres = 3.6, 23.2
    line(d, (ar, y_res), (xres, y_res))
    dot(d, (xres, y_res))
    port_out(d, y_res, "ALUResultE", xres)

    # WriteDataE also leaves the stage as the store data
    y_wdo = -2.4
    line(d, (xwd, SB["in0"][1]), (xwd, y_wdo))
    dot(d, (xwd, SB["in0"][1]))
    dot(d, (xwd, y_wdo))
    port_out(d, y_wdo, "WriteDataE", xwd)

    # ---------------- branch comparator ----------------
    bl, br, bt, bb = 17.6, 21.0, -3.4, -6.2
    box(d, bl, br, bt, bb, "branchcmp", fontsize=10)
    y_ba, y_bb = -4.0, -5.4
    line(d, (xfa, SA["in0"][1]), (xfa, y_ba))
    dot(d, (xfa, SA["in0"][1]))
    arrow(d, (xfa, y_ba), (bl, y_ba))
    line(d, (xwd, y_wdo), (xwd, y_bb))
    arrow(d, (xwd, y_bb), (bl, y_bb))
    xf3 = (bl + br) / 2
    arrow(d, (xf3, bb - 0.9), (xf3, bb))
    label(d, (xf3, bb - 1.2), "Funct3E", fontsize=9)

    # ---------------- redirect ----------------
    rl, rr, rt, rb = 24.0, 29.6, -3.0, -6.6
    box(d, rl, rr, rt, rb, "PCSrcE =\nValidE & ReadyM &\n(JumpE | JalrE |\nBranchE & TakenE)",
        fontsize=10)
    y_tk = (bt + bb) / 2
    arrow(d, (br, y_tk), (rl, y_tk))
    label(d, ((br + rl) / 2 - 0.6, y_tk + 0.3), "TakenE", fontsize=10)
    port_out(d, y_tk, "PCSrcE", rr)

    # ---------------- branch/jump target ----------------
    tl, tr, tt, tb = 17.4, 19.4, -8.6, -11.4
    box(d, tl, tr, tt, tb, "+", fontsize=16)
    label(d, ((tl + tr) / 2, tb - 0.7), "targetadd\nadder #(32)", fontsize=9)
    y_ta, y_tb = -9.2, -10.8
    line(d, (xpc, y_pc), (xpc, y_ta))
    arrow(d, (xpc, y_ta), (tl, y_ta))
    line(d, (xim, y_im), (xim, y_tb))
    arrow(d, (xim, y_tb), (tl, y_tb))
    label(d, (tl - 1.0, y_ta + 0.3), "PCE", fontsize=9)
    label(d, (tl - 1.2, y_tb + 0.3), "ImmExtE", fontsize=9)

    TM = mux(d, (26.4, -10.4), 2, "targetmux", sel="T")
    line(d, (tr, (tt + tb) / 2), (tr + 1.0, (tt + tb) / 2), (tr + 1.0, TM["in0"][1]))
    arrow(d, (tr + 1.0, TM["in0"][1]), TM["in0"])
    line(d, (xres, y_res), (xres, TM["in1"][1]))
    arrow(d, (xres, TM["in1"][1]), TM["in1"])
    label(d, (xres + 0.1, TM["in1"][1] + 0.35), "{[31:1], 0}", halign="left", fontsize=9)
    stub_sel(d, TM["sel"], "JalrE")
    port_out(d, TM["y"][1], "PCTargetE", TM["y"][0])

    # ---------------- pass-through to the Memory stage ----------------
    port_out(d, -13.2, "PCPlus4E, RdE, Rs1E, Rs2E, Funct3E,\nRegWriteE, MemWriteE, ResultSrcE", gr)

    # module boundary
    for a, b in (((XL, YT), (XR, YT)), ((XR, YT), (XR, YB)),
                 ((XR, YB), (XL, YB)), ((XL, YB), (XL, YT))):
        d.add(elm.Line().at(a).to(b).linestyle("--").color(GREY))
    label(d, (XL + 0.2, YT - 0.4), "ieu", halign="left", color=GREY)
    label(d, (XL + 0.2, YB + 0.4), "clk and reset (synchronous) go to the valid bit and the registers",
          halign="left", fontsize=10, color=GREY)
    return d
