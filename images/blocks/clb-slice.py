"""One CLB slice: a LUT2 and a flip-flop, an output mux picks LUT or register."""
from schemdraw import elements as elm
from _style import new_drawing, block, dff, line, RED, RED_FILL, GREY


def draw():
    d = new_drawing()
    d.add(elm.Line().at((-2.6, 0)).to((-2.6, 0)))          # reserve room for labels

    lut = elm.Ic(pins=[elm.IcPin(name="", side="L", anchorname="i1", slot="2/2"),
                       elm.IcPin(name="", side="L", anchorname="i2", slot="1/2"),
                       elm.IcPin(name="", side="R", anchorname="q")],
                 size=(2.4, 2.4), pinspacing=1.2)
    d.add(block(lut).at((0, -1.2)).label("LUT2", "center", fontsize=14))
    for pin, name in (("i1", "in1"), ("i2", "in2")):
        x, y = lut.absanchors[pin]
        line(d, (x, y), (x - 0.9, y))
        d.add(elm.Label().at((x - 1.0, y)).label(name, halign="right"))
    d.add(elm.Label().at((1.2, 1.6)).label("one CLB slice", fontsize=11, color=GREY))

    qx, qy = lut.absanchors["q"]
    ff = dff()
    d.add(ff.anchor("D").at((qx + 1.8, -1.6)))
    line(d, (qx, qy), (qx + 0.9, qy))
    d.add(elm.Dot().at((qx + 0.9, qy)))
    line(d, (qx + 0.9, qy), (qx + 0.9, -1.6), ff.absanchors["D"])

    mux = block(elm.Multiplexer(
        pins=[elm.IcPin(name="", side="L", anchorname="a", slot="2/2"),
              elm.IcPin(name="", side="L", anchorname="b", slot="1/2"),
              elm.IcPin(name="", side="R", anchorname="y"),
              elm.IcPin(name="", side="B", anchorname="s")],
        size=(1.4, 3.6), pinspacing=2.4))
    mx = ff.absanchors["Q"][0] + 2.0
    d.add(mux.anchor("a").at((mx, 1.2)))
    # LUT output -> mux "a" (combinational), flip-flop Q -> mux "b" (registered)
    line(d, (qx + 0.9, qy), (qx + 0.9, 1.2), mux.absanchors["a"])
    line(d, ff.absanchors["Q"], (mx - 0.5, ff.absanchors["Q"][1]), (mx - 0.5, -1.2), mux.absanchors["b"])
    y = mux.absanchors["y"]
    line(d, y, (y[0] + 1.6, y[1]))
    d.add(elm.Label().at((y[0] + 1.7, y[1])).label("out", halign="left"))

    cx, cy = ff.absanchors["CLK"]
    line(d, (cx, cy), (cx - 0.6, cy), (cx - 0.6, -4.2), (-2.4, -4.2))
    d.add(elm.Label().at((-2.5, -4.2)).label("clk", halign="right"))

    sx, sy = mux.absanchors["s"]
    cfg = elm.Ic(size=(4.2, 0.9))
    d.add(block(cfg, RED_FILL, RED).at((sx - 2.1, sy - 2.4))
          .label("config memory (SRAM)", "center", fontsize=11, color=RED))
    d.add(elm.Line().at((sx, sy - 1.5)).to((sx, sy)).color(RED))
    return d
