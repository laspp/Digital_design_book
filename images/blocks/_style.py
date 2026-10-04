"""Shared look for the book's schemdraw figures: blue accent, light fill."""
import schemdraw

ACCENT = "#1A5276"     # same blue as the book's headings and links
FILL = "#E8F0F7"
RED = "#C0392B"        # configuration memory
RED_FILL = "#FDEDEC"
GREY = "#5D6D7E"


def new_drawing(**kw):
    schemdraw.theme("default")
    d = schemdraw.Drawing(**kw)
    d.config(unit=2.5, fontsize=12, lw=1.6, color="#2C3E50")
    return d


def block(el, fill=FILL, edge=ACCENT):
    """Style an element as a filled, accent-coloured block.

    theta(0) keeps blocks upright even after a line was drawn in another
    direction (schemdraw carries the last direction forward).
    """
    return el.fill(fill).color(edge).theta(0)


def line(d, *pts):
    """Draw a polyline through explicit points (avoids schemdraw's direction state)."""
    from schemdraw import elements as elm
    for a, b in zip(pts, pts[1:]):
        d.add(elm.Line().at(a).to(b))


def dff(mirror=False, size=(2.0, 2.2)):
    """A plain D flip-flop box with D, Q and a clock wedge (no inverted output).

    D and Q share the top pin row; the clock is the bottom pin on the D side.
    mirror=True puts D and clock on the right, Q on the left (data flows right to left).
    """
    from schemdraw import elements as elm
    din, qout = ("R", "L") if mirror else ("L", "R")
    return block(elm.Ic(
        pins=[elm.IcPin(name="D", side=din, anchorname="D", slot="2/2"),
              elm.IcPin(name=">", side=din, anchorname="CLK", slot="1/2"),
              elm.IcPin(name="Q", side=qout, anchorname="Q", slot="2/2")],
        size=size, pinspacing=1.2))
