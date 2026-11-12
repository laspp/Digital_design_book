"""Load/store unit (HIPV rtl/core/lsu/lsu.sv): the E/M handshake and valid
bit, the E/M pipeline registers, the OBI transaction control FSM
(lsuctrl), the address, byte-enable and store-data alignment, the read-data
register (rawreg) with shift and sign/zero extension, and the forwarding
mux that drives ForwardDataM."""
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

XL, XR = 0.0, 30.0          # module boundary (left / right)
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


def stub_in(d, pin, name, length=1.4):
    """Short input arrow from the left into pin, labelled with its source."""
    x, y = pin
    arrow(d, (x - length, y), pin)
    label(d, (x - length - 0.1, y), name, halign="right", fontsize=10)


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
    hl, hr, ht, hb = 2.2, 7.6, 15.4, 12.4
    box(d, hl, hr, ht, hb, "handshake + valid bit\n(ValidMReg)\n\nValidM waits for DoneM\non loads and stores",
        fontsize=10)
    y_ve, y_rw = 14.6, 13.2
    port_in(d, y_ve, "ValidE", hl)
    port_in(d, y_rw, "ReadyW", hl)
    port_out(d, y_ve, "ValidM", hr)
    port_out(d, y_rw, "ReadyM", hr)

    # ---------------- E/M pipeline registers ----------------
    gl, gr, gt, gb = 3.0, 6.4, 10.6, -14.0
    box(d, gl, gr, gt, gb, "E/M\nregisters\n\nflopenr\n× 6")
    xen = 4.0
    arrow(d, (xen, hb), (xen, gt))
    label(d, (xen + 0.15, (hb + gt) / 2), "EnEM", halign="left", fontsize=10)
    port_in(d, -4.0, "from IEU:\nALUResultE,\nWriteDataE,\nPCPlus4E, RdE,\nFunct3E,\n"
                     "RegWriteE,\nMemWriteE,\nResultSrcE", gl)

    # ---------------- OBI transaction control ----------------
    cl, cr, ct, cb = 11.6, 16.8, 11.6, 8.4
    box(d, cl, cr, ct, cb, "lsuctrl (FSM)\n\nIDLE\nWAIT_RESP\nDONE", fontsize=10)
    for y, name in ((11.2, "MemReqM = ValidMReg & MemOpM"), (10.4, "ObiGntM"),
                    (9.6, "ObiRvalidM"), (8.8, "ReadyW")):
        stub_in(d, (cl, y), name)
    port_out(d, 10.8, "ObiReqM", cr)
    # DoneM back to the handshake
    xd = 13.0
    line(d, (xd, ct), (xd, 11.9), (6.8, 11.9))
    arrow(d, (6.8, 11.9), (6.8, hb))
    label(d, (9.0, 12.2), "DoneM", fontsize=10)

    # ---------------- address, byte enables, store data ----------------
    xa, xo = 8.0, 9.0                      # ALUResultM bus, AddrLsbM bus
    y_al = 6.6
    line(d, (gr, y_al), (18.0, y_al))
    label(d, (gr + 0.2, y_al + 0.3), "ALUResultM", halign="left", fontsize=10)
    dot(d, (xa, y_al))
    dot(d, (xo, y_al))
    line(d, (xo, y_al), (xo, -0.2))
    box(d, 18.0, 21.0, 7.4, 5.8, "{[31:2], 00}", fontsize=10)
    port_out(d, y_al, "ObiAddrM", 21.0)

    y_be_o, y_be_f = 4.6, 3.6
    box(d, 18.0, 21.0, 4.9, 3.3, "byte\nenables", fontsize=10)
    arrow(d, (xo, y_be_o), (18.0, y_be_o))
    dot(d, (xo, y_be_o))
    label(d, (xo + 0.2, y_be_o + 0.3), "AddrLsbM = [1:0]", halign="left", fontsize=9)
    arrow(d, (gr, y_be_f), (18.0, y_be_f))
    label(d, (gr + 0.2, y_be_f - 0.3), "Funct3M", halign="left", fontsize=10)
    port_out(d, 4.1, "ObiBeM", 21.0)

    y_we = 2.2
    label(d, (gr + 0.2, y_we + 0.3), "MemWriteM", halign="left", fontsize=10)
    port_out(d, y_we, "ObiWeM", gr)

    y_wd, y_wo = 0.8, -0.2
    box(d, 18.0, 21.0, 1.2, -0.6, "<< 8·offset", fontsize=10)
    arrow(d, (gr, y_wd), (18.0, y_wd))
    label(d, (gr + 0.2, y_wd + 0.3), "WriteDataM", halign="left", fontsize=10)
    arrow(d, (xo, y_wo), (18.0, y_wo))
    dot(d, (xo, y_wo))
    port_out(d, 0.3, "ObiWdataM", 21.0)

    # ---------------- read data: rawreg -> shift -> extend ----------------
    R = flopenr(d, (13.0, -3.0), "rawreg")
    arrow(d, (10.0, -3.0), R["D"])
    label(d, (11.0, -2.7), "ObiRdataM", fontsize=10)
    # CaptureM = WaitRespM & ObiRvalidM loads rawreg
    xc = 12.0
    line(d, (xc, cb), (xc, R["en"][1]))
    arrow(d, (xc, R["en"][1]), R["en"])
    label(d, (xc + 0.15, cb - 0.4), "CaptureM", halign="left", fontsize=10)

    sl, sr, st, sb = 17.0, 19.8, -2.2, -3.8
    box(d, sl, sr, st, sb, ">> 8·offset", fontsize=10)
    arrow(d, R["Q"], (sl, -3.0))
    label(d, ((R["Q"][0] + sl) / 2, -2.7), "ReadRawM", fontsize=9)
    y_off = -7.0
    xs = (sl + sr) / 2
    line(d, (xo, y_wo), (xo, y_off), (xs, y_off))
    arrow(d, (xs, y_off), (xs, sb))

    el, er = 21.0, 24.0
    box(d, el, er, st, sb, "sign / zero\nextend", fontsize=10)
    arrow(d, (sr, -3.0), (el, -3.0))
    xf = (el + er) / 2
    arrow(d, (xf, st + 0.9), (xf, st))
    label(d, (xf, st + 1.2), "Funct3M", fontsize=9)
    xr = 25.0
    line(d, (er, -3.0), (xr, -3.0))
    dot(d, (xr, -3.0))
    port_out(d, -3.0, "ReadDataM", xr)

    # ---------------- forwarding data ----------------
    m = block(elm.Multiplexer(
        pins=[elm.IcPin(name="0", side="L", anchorname="in0", slot="2/2"),
              elm.IcPin(name="1", side="L", anchorname="in1", slot="1/2"),
              elm.IcPin(name="", side="R", anchorname="y"),
              elm.IcPin(name="", side="B", anchorname="sel")],
        size=(1.4, 2.8), pinspacing=1.2, leadlen=0))
    d.add(m.anchor("y").at((27.4, -8.4)))
    M = m.absanchors
    label(d, ((M["in0"][0] + M["y"][0]) / 2, M["in0"][1] + 1.3), "fwdmux", fontsize=9)
    line(d, (xa, y_al), (xa, M["in0"][1]))
    arrow(d, (xa, M["in0"][1]), M["in0"])
    line(d, (xr, -3.0), (xr, M["in1"][1]))
    arrow(d, (xr, M["in1"][1]), M["in1"])
    s = M["sel"]
    arrow(d, (s[0], s[1] - 0.9), s)
    label(d, (s[0], s[1] - 1.2), "ResultSrcM == MEM", fontsize=9)
    port_out(d, M["y"][1], "ForwardDataM", M["y"][0])

    # ALUResultM also goes on to Writeback
    y_alo = -11.0
    line(d, (xa, M["in0"][1]), (xa, y_alo))
    dot(d, (xa, M["in0"][1]))
    port_out(d, y_alo, "ALUResultM", xa)

    # ---------------- pass-through to Writeback ----------------
    port_out(d, -13.0, "PCPlus4M, RdM, ResultSrcM,\nRegWriteM = RegWriteMReg & ValidMReg", gr)

    # module boundary
    for a, b in (((XL, YT), (XR, YT)), ((XR, YT), (XR, YB)),
                 ((XR, YB), (XL, YB)), ((XL, YB), (XL, YT))):
        d.add(elm.Line().at(a).to(b).linestyle("--").color(GREY))
    label(d, (XL + 0.2, YT - 0.4), "lsu", halign="left", color=GREY)
    label(d, (XL + 0.2, YB + 0.4), "clk and reset (synchronous) go to the valid bit, the registers and lsuctrl",
          halign="left", fontsize=10, color=GREY)
    return d
