"""F/D handshake of the instruction decode unit (HIPV rtl/core/idu/idu.sv):
ReadyD = ~ValidDReg | ReadyE, EnFD = ValidF & ReadyD, the valid bit
ValidDReg, loaded with ValidF whenever ReadyD is high, and the flush
ValidD = ValidDReg & ~PCSrcE."""
from schemdraw import logic
from schemdraw import elements as elm
from schemdraw.backends import svg, svgtext
from _style import new_drawing, block, line, GREY

# schemdraw's text-size estimate parses labels as XML and fails on '&';
# measure with a same-width stand-in instead (the drawn text is unchanged).
_text_approx_size = svgtext.text_approx_size


def _text_size_amp(text, *args, **kw):
    return _text_approx_size(text.replace("&", "8"), *args, **kw)


svgtext.text_approx_size = svg.text_approx_size = _text_size_amp

XL, XR = 0.0, 21.5          # input / output columns


def arrow(d, a, b):
    d.add(elm.Arrow().at(a).to(b))


def dot(d, xy):
    d.add(elm.Dot().at(xy))


def label(d, xy, text, **kw):
    kw.setdefault("fontsize", 11)
    d.add(elm.Label().at(xy).label(text, **kw))


def port_out(d, y, name, frm):
    arrow(d, (frm, y), (XR + 0.1, y))
    label(d, (XR + 0.4, y), name, halign="left")


def flopenr(d, xy, name, width):
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

    # ---------------- valid bit: ValidDReg <= ValidF when ReadyD ----------------
    y_vd = 5.0
    V = flopenr(d, (12.0, y_vd), "validreg", 1)
    label(d, (XL - 0.4, y_vd), "ValidF", halign="right")
    arrow(d, (XL - 0.1, y_vd), V["D"])
    q = V["Q"]
    xq = 15.4
    line(d, q, (xq, q[1]))
    dot(d, (xq, q[1]))
    f = d.add(block(logic.And(inputs=2, inputnots=[1])).anchor("in2").at((17.0, q[1])))
    F = f.absanchors
    line(d, (xq, q[1]), F["in2"])
    xp = F["in1"][0] - 0.8
    label(d, (xp, 8.2), "PCSrcE  (flush)")
    line(d, (xp, 7.9), (xp, F["in1"][1]))
    arrow(d, (xp, F["in1"][1]), F["in1"])
    port_out(d, F["out"][1], "ValidD", F["out"][0])
    label(d, (q[0] + 0.3, q[1] + 0.35), "ValidDReg", halign="left", fontsize=10)

    # ---------------- ReadyD = ~ValidDReg | ReadyE ----------------
    o = d.add(block(logic.Or(inputs=2, inputnots=[1])).anchor("out").at((8.0, 0.0)))
    O = o.absanchors
    # ValidDReg feeds back into the inverted OR input
    yfb, xfb = 1.3, 4.4
    line(d, (xq, q[1]), (xq, yfb), (xfb, yfb), (xfb, O["in1"][1]))
    arrow(d, (xfb, O["in1"][1]), O["in1"])
    label(d, (XL - 0.4, O["in2"][1]), "ReadyE", halign="right")
    arrow(d, (XL - 0.1, O["in2"][1]), O["in2"])

    xr = 10.0
    line(d, O["out"], (xr, 0.0))
    dot(d, (xr, 0.0))
    line(d, (xr, 0.0), (xr, V["en"][1]))
    arrow(d, (xr, V["en"][1]), V["en"])
    port_out(d, 0.0, "ReadyD  (to Fetch)", xr)
    label(d, ((O["out"][0] + xr) / 2, 0.3), "ReadyD", fontsize=10)

    # ---------------- EnFD = ValidF & ReadyD ----------------
    a = d.add(block(logic.And(inputs=2)).anchor("out").at((16.6, -3.4)))
    A = a.absanchors
    line(d, (xr, 0.0), (xr, A["in1"][1]))
    arrow(d, (xr, A["in1"][1]), A["in1"])
    xv = 2.0
    dot(d, (xv, y_vd))
    line(d, (xv, y_vd), (xv, A["in2"][1]))
    arrow(d, (xv, A["in2"][1]), A["in2"])
    port_out(d, A["out"][1], "EnFD  (to the F/D registers)", A["out"][0])

    label(d, (XL - 1.6, -5.6),
          "ReadyD = ~ValidDReg | ReadyE: the stage is empty, or its instruction leaves this cycle\n"
          "ValidD = ValidDReg & ~PCSrcE: a valid instruction that is not on the wrong path\n"
          "EnFD = ValidF & ReadyD: an instruction moves from Fetch into Decode",
          halign="left", fontsize=10, color=GREY)
    return d
