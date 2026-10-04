"""I/O block: optional registers on the output and input paths, tri-state driver."""
from schemdraw import elements as elm
from schemdraw import logic
from _style import new_drawing, block, dff, line, RED, RED_FILL, GREY


def mux21(mirror=False):
    din, dout = ("R", "L") if mirror else ("L", "R")
    return block(elm.Multiplexer(
        pins=[elm.IcPin(name="", side=din, anchorname="a", slot="2/2"),
              elm.IcPin(name="", side=din, anchorname="b", slot="1/2"),
              elm.IcPin(name="", side=dout, anchorname="y")],
        size=(1.2, 2.6), pinspacing=1.5))


def label(d, xy, text, **kw):
    d.add(elm.Label().at(xy).label(text, **kw))


def draw():
    d = new_drawing()
    out_y, in_y, clk_y = 0.0, -6.0, -9.0
    label(d, (-3.2, 1.9), "output path", halign="left", fontsize=13)
    label(d, (-3.2, in_y + 2.2), "input path", halign="left", fontsize=13)
    label(d, (6.8, -3.0), "registers and OE control are optional, configured per pin",
          fontsize=11, color=GREY)

    # ------------- output path, data flows left to right -------------
    label(d, (-1.8, out_y), "from FPGA fabric", halign="right", fontsize=11)
    line(d, (-1.6, out_y), (0.0, out_y))
    d.add(elm.Dot().at((0.0, out_y)))
    ff = dff()
    d.add(ff.anchor("D").at((0.8, out_y)))
    line(d, (0.0, out_y), ff.absanchors["D"])
    mux = mux21()
    d.add(mux.anchor("a").at((5.0, out_y + 1.0)))
    line(d, (0.0, out_y), (0.0, out_y + 1.0), mux.absanchors["a"])       # bypass
    q = ff.absanchors["Q"]
    line(d, q, (q[0] + 0.5, q[1]), (q[0] + 0.5, out_y - 0.5), mux.absanchors["b"])

    tri = block(logic.Tristate(outputnot=False))
    my = mux.absanchors["y"]
    d.add(tri.anchor("start").at((my[0] + 0.2, my[1])))
    line(d, my, tri.absanchors["start"])
    cx, cy = tri.absanchors["c"]
    line(d, (cx, cy), (cx, cy + 0.9))
    label(d, (cx, cy + 1.2), "OE", fontsize=12, color=RED)

    pad = elm.Ic(size=(2.2, 1.0))
    pad_x = tri.absanchors["end"][0] + 0.6
    d.add(block(pad, RED_FILL, RED).at((pad_x, my[1] - 0.5))
          .label("I/O pad", "center", fontsize=12, color=RED))
    line(d, tri.absanchors["end"], (pad_x, my[1]))
    pad_right = pad_x + 2.2

    # ------------- input path, data flows right to left -------------
    wire_x = pad_right + 0.6
    line(d, (pad_right, my[1]), (wire_x, my[1]), (wire_x, in_y), (wire_x - 0.8, in_y))
    jx = wire_x - 0.8
    d.add(elm.Dot().at((jx, in_y)))
    ffi = dff(mirror=True)
    d.add(ffi.anchor("D").at((jx - 0.8, in_y)))
    line(d, (jx, in_y), ffi.absanchors["D"])
    mi = mux21(mirror=True)
    d.add(mi.anchor("a").at((jx - 4.8, in_y + 1.0)))
    line(d, (jx, in_y), (jx, in_y + 1.0), mi.absanchors["a"])             # bypass
    q = ffi.absanchors["Q"]
    line(d, q, (q[0] - 0.5, q[1]), (q[0] - 0.5, in_y - 0.5), mi.absanchors["b"])
    y = mi.absanchors["y"]
    line(d, y, (y[0] - 1.4, y[1]))
    label(d, (y[0] - 1.5, y[1]), "to FPGA fabric", halign="right", fontsize=11)

    # ------------- shared clock -------------
    x_out = ff.absanchors["CLK"][0] - 0.4
    x_in = ffi.absanchors["CLK"][0] + 0.4
    line(d, ff.absanchors["CLK"], (x_out, ff.absanchors["CLK"][1]), (x_out, clk_y), (x_in, clk_y),
         (x_in, ffi.absanchors["CLK"][1]), ffi.absanchors["CLK"])
    d.add(elm.Dot().at((x_out, clk_y)))
    line(d, (x_out, clk_y), (x_out - 0.8, clk_y))
    label(d, (x_out - 0.9, clk_y), "clk", halign="right")
    return d
