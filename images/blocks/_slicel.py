"""Shared SLICEL pieces, reused across the tutorial examples in this folder."""
from schemdraw import elements as elm
from _style import block

WIDTH = 2.4
HEIGHT = 3.6


def lut6_lane(d, name, y0):
    """Add one LUT6 lane box to drawing `d`.

    Bus input labeled "{name}1:{name}6" (e.g. "A1:A6"), O6/O5 outputs.
    The box is WIDTH x HEIGHT units, with its bottom edge at y0. Returns
    the Ic element so callers can read its absanchors for wiring.
    """
    lut = elm.Ic(
        pins=[elm.IcPin(name=f"{name}1:{name}6", side="L", anchorname="i", slot="5/6"),
              elm.IcPin(name="O6", side="R", anchorname="o6", slot="6/6"),
              elm.IcPin(name="O5", side="R", anchorname="o5", slot="5/6")],
        size=(WIDTH, HEIGHT), pinspacing=0.6)
    d.add(block(lut).at((0, y0)).label(f"LUT6 {name}", "center", fontsize=14))
    return lut
