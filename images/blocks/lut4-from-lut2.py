"""A LUT4 built from four LUT2s and three 2:1 multiplexers."""
from schemdraw import elements as elm
from _style import new_drawing, block, GREY


def mux21(spacing, height):
    return block(elm.Multiplexer(
        pins=[elm.IcPin(name="", side="L", anchorname="a", slot="2/2"),
              elm.IcPin(name="", side="L", anchorname="b", slot="1/2"),
              elm.IcPin(name="", side="R", anchorname="y"),
              elm.IcPin(name="", side="T", anchorname="s")],
        size=(1.2, height), pinspacing=spacing))


def draw():
    d = new_drawing()
    d.add(elm.Line().at((-3.9, 0)).to((-3.9, 0)))   # reserve room for the left labels
    gap = 5.2                      # distance between the two LUT3 groups
    lut_x, mux_x, final_x = 0.0, 3.4, 7.6
    centers = [gap / 2, -gap / 2]
    group_outs = []

    for g, yc in enumerate(centers):
        luts = []
        for dy in (+0.6, -0.6):
            lut = elm.Ic(pins=[elm.IcPin(name="", side="R", anchorname="q"),
                               elm.IcPin(name="", side="L", anchorname="i")],
                         size=(1.8, 1.0))
            d.add(block(lut).at((lut_x, yc + dy - 0.5))
                  .label("LUT2", "center", fontsize=13))
            # shared inputs: every LUT2 sees in1 and in2
            ix, iy = lut.absanchors["i"]
            d.add(elm.Line().at((ix, iy)).to((ix - 0.7, iy)))
            d.add(elm.Label().at((lut_x - 1.15, yc + dy)).label("in1, in2", halign="right", fontsize=11))
            luts.append(lut)
        m = mux21(1.2, 2.2)
        d.add(m.anchor("a").at((mux_x, yc + 0.6)))
        for lut, pin in zip(luts, ("a", "b")):
            d.add(elm.Line().at(lut.absanchors["q"]).to(m.absanchors[pin]))
        sx, sy = m.absanchors["s"]
        d.add(elm.Arrow().at((sx, sy + 0.6)).to((sx, sy)))
        d.add(elm.Label().at((sx, sy + 0.85)).label("in3", fontsize=11))
        group_outs.append(m.absanchors["y"])
        d.add(elm.EncircleBox([*luts, m], padx=0.3, pady=0.1)
              .linestyle("--").linewidth(1.2).color(GREY))
        d.add(elm.Label().at((lut_x - 0.1, yc - 1.8)).label(f"LUT3 #{g + 1}", halign="left",
                                                           fontsize=11, color=GREY))

    final = mux21(gap, gap + 1.0)
    d.add(final.anchor("a").at((final_x, group_outs[0][1])))
    for pin, out in zip(("a", "b"), group_outs):
        d.add(elm.Line().at(out).to((final_x - 0.9, out[1])).to(final.absanchors[pin]))
    sx, sy = final.absanchors["s"]
    d.add(elm.Arrow().at((sx, sy + 0.6)).to((sx, sy)))
    d.add(elm.Label().at((sx, sy + 0.85)).label("in4", fontsize=11))
    y = final.absanchors["y"]
    d.add(elm.Line().at(y).to((y[0] + 1.4, y[1])))
    d.add(elm.Label().at((y[0] + 1.5, y[1])).label("out = LUT4(in1..in4)", halign="left"))
    return d
