"""2-to-1 multiplexer: y = sel ? in1 : in0"""
import schemdraw
from schemdraw import elements as elm


def draw():
    d = schemdraw.Drawing()
    mux = d.add(elm.Multiplexer(
        pins=[elm.IcPin(name="0", side="L", anchorname="in0", slot="1/2"),
              elm.IcPin(name="1", side="L", anchorname="in1", slot="2/2"),
              elm.IcPin(name="", side="R", anchorname="y"),
              elm.IcPin(name="", side="B", anchorname="sel")],
        size=(2.2, 3)))
    d.add(elm.Line().at(mux.in0).left(1.5).label("in0", "left"))
    d.add(elm.Line().at(mux.in1).left(1.5).label("in1", "left"))
    d.add(elm.Line().at(mux.y).right(1.5).label("y", "right"))
    d.add(elm.Line().at(mux.sel).down(1).label("sel", "bottom"))
    return d
