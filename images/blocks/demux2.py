"""1-to-2 demultiplexer: the input goes to y0 when sel = 0, to y1 when sel = 1."""
from schemdraw import elements as elm
from _style import new_drawing, block, line, GREY


def demux12(mirror=False):
    """A 1:2 demux. mirror=True flips it so data flows right to left."""
    din, dout = ("R", "L") if mirror else ("L", "R")
    return block(elm.Multiplexer(
        demux=True,
        pins=[elm.IcPin(name="", side=din, anchorname="a"),
              elm.IcPin(name="0", side=dout, anchorname="y0", slot="2/2"),
              elm.IcPin(name="1", side=dout, anchorname="y1", slot="1/2"),
              elm.IcPin(name="", side="B", anchorname="sel")],
        size=(1.4, 2.8), pinspacing=1.5))


def draw():
    d = new_drawing()
    dm = demux12()
    d.add(dm)
    a, y0, y1, sel = (dm.absanchors[k] for k in ("a", "y0", "y1", "sel"))

    line(d, (a[0] - 1.4, a[1]), a)
    d.add(elm.Label().at((a[0] - 1.5, a[1])).label("in", halign="right"))
    for name, pt in (("y0", y0), ("y1", y1)):
        line(d, pt, (pt[0] + 1.4, pt[1]))
        d.add(elm.Label().at((pt[0] + 1.5, pt[1])).label(name, halign="left"))
    line(d, sel, (sel[0], sel[1] - 1.0))
    d.add(elm.Label().at((sel[0], sel[1] - 1.3)).label("sel", fontsize=12))
    d.add(elm.Label().at((sel[0] + 0.3, sel[1] - 0.5))
          .label("sel = 0 → y0\nsel = 1 → y1", fontsize=10, color=GREY, halign="left"))
    return d
