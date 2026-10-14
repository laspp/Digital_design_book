"""One SLICEL lane: a LUT6 feeding a flip-flop.

Step 1: just the LUT6 box, with one bus-style input and two outputs (O6,
the six-input function, and O5, a five-input function sharing the same
LUT). Pin labels sit inside the block, like the D/Q/clock labels on the
dff() helper in _style.py.
"""
from schemdraw import elements as elm
from _style import new_drawing, GREY
from _slicel import lut6_lane


def draw(name="A"):
    """name: the lane letter (A, B, C, D for a real SLICEL), used to label
    the input bus as e.g. "A1:A6" so this can be reused for all four lanes.
    """
    d = new_drawing()
    d.add(elm.Line().at((-2.6, 0)).to((-2.6, 0)))  # reserve room for labels

    lut6_lane(d, name, -1.8)

    d.add(elm.Label().at((1.2, 2.2)).label(
        f"one SLICEL lane (step 1: LUT6 {name})", fontsize=11, color=GREY))
    return d
