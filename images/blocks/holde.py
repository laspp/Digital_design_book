"""Operand refresh while Execute stalls (HIPV rtl/core/ieu/ieu.sv): rd1mux
and rd1reg load RD1D from Decode on EnDE, and reload the forwarded value
FwdAE on HoldE = ValidEReg & ~ReadyM. The loop closes through fwdamux."""
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


def arrow(d, a, b):
    d.add(elm.Arrow().at(a).to(b))


def dot(d, xy):
    d.add(elm.Dot().at(xy))


def label(d, xy, text, **kw):
    kw.setdefault("fontsize", 11)
    d.add(elm.Label().at(xy).label(text, **kw))


def mux(d, out, n, name, sel="T"):
    """n-input mux with the output at out; input 0 on top. Returns the anchors."""
    pins = [elm.IcPin(name=str(i), side="L", anchorname=f"in{i}", slot=f"{n - i}/{n}")
            for i in range(n)]
    pins += [elm.IcPin(name="", side="R", anchorname="y"),
             elm.IcPin(name="", side=sel, anchorname="sel")]
    m = block(elm.Multiplexer(pins=pins, size=(1.4, 1.2 * n + 0.4),
                              pinspacing=1.2, leadlen=0))
    d.add(m.anchor("y").at(out))
    A = m.absanchors
    yl = (A["in0"][1] + 1.7) if sel == "B" else (A[f"in{n - 1}"][1] - 2.0)
    label(d, ((A["in0"][0] + A["y"][0]) / 2, yl), f"{name}\nmux{n} #(32)", fontsize=9)
    return A


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

    # ---------------- rd1mux -> rd1reg ----------------
    X = mux(d, (5.5, 1.0), 2, "rd1mux", sel="B")
    R = flopenr(d, (9.0, 1.0), "rd1reg")
    arrow(d, X["y"], R["D"])
    label(d, ((X["y"][0] + R["D"][0]) / 2, 1.3), "RD1NextE", fontsize=10)
    arrow(d, (1.0, X["in1"][1]), X["in1"])
    label(d, (0.9, X["in1"][1]), "RD1D  (from Decode)", halign="right")

    # ---------------- fwdamux ----------------
    q = R["Q"]
    F = mux(d, (16.6, q[1] - 1.2), 3, "fwdamux", sel="B")
    arrow(d, q, F["in0"])
    label(d, ((q[0] + F["in0"][0]) / 2, q[1] + 0.3), "RD1E", fontsize=10)
    for k, name in (("in1", "ResultW"), ("in2", "ForwardDataM")):
        x, y = F[k]
        arrow(d, (x - 1.2, y), F[k])
        label(d, (x - 1.3, y), name, halign="right", fontsize=9)
    s = F["sel"]
    arrow(d, (s[0], s[1] - 0.9), s)
    label(d, (s[0], s[1] - 1.2), "ForwardAE", fontsize=9)

    # FwdAE: to the ALU/branch path and back into rd1mux (the refresh loop)
    o = F["y"]
    xo, ytop, xl = 18.4, 4.8, X["in0"][0] - 1.0
    line(d, o, (xo, o[1]))
    dot(d, (xo, o[1]))
    arrow(d, (xo, o[1]), (xo + 1.6, o[1]))
    label(d, (xo + 1.7, o[1]), "srcamux,\nbranchcmp", halign="left", fontsize=10)
    label(d, ((o[0] + xo) / 2, o[1] + 0.3), "FwdAE", fontsize=10)
    line(d, (xo, o[1]), (xo, ytop), (xl, ytop), (xl, X["in0"][1]))
    arrow(d, (xl, X["in0"][1]), X["in0"])
    label(d, ((xl + xo) / 2, ytop + 0.35),
          "forwarded value back into the register (refresh)", fontsize=10, color=GREY)

    # ---------------- enable: EnDE | HoldE ----------------
    ory = -3.6
    g = d.add(block(logic.Or(inputs=2)).anchor("out").at((6.9, ory)))
    xe = 7.3
    line(d, g.absanchors["out"], (xe, ory), (xe, R["en"][1]))
    arrow(d, (xe, R["en"][1]), R["en"])

    # EnDE: rd1mux select and one OR input
    y1 = g.absanchors["in1"][1]
    xs = X["sel"][0]
    line(d, (1.0, y1), g.absanchors["in1"])
    dot(d, (xs, y1))
    arrow(d, (xs, y1), X["sel"])
    label(d, (0.9, y1), "EnDE = ValidD & ReadyE", halign="right")
    label(d, (xs + 0.15, (y1 + X["sel"][1]) / 2), "1 = new instruction\n0 = refresh",
          halign="left", fontsize=9, color=GREY)

    # HoldE = ValidEReg & ~ReadyM
    y2 = g.absanchors["in2"][1]
    ya, xh = y2 - 1.8, 5.0
    a = d.add(block(logic.And(inputs=2, inputnots=[2])).anchor("out").at((3.6, ya)))
    line(d, a.absanchors["out"], (xh, ya), (xh, y2), g.absanchors["in2"])
    label(d, ((a.absanchors["out"][0] + xh) / 2, ya + 0.35), "HoldE", fontsize=10)
    for k, name in (("in1", "ValidEReg"), ("in2", "ReadyM")):
        p = a.absanchors[k]
        line(d, (1.0, p[1]), p)
        label(d, (0.9, p[1]), name, halign="right")
    label(d, (a.absanchors["out"][0] - 1.0, ya - 1.6),
          "HoldE = ValidEReg & ~ReadyM\n(valid instruction, Memory not ready)",
          fontsize=10, color=GREY)
    return d
