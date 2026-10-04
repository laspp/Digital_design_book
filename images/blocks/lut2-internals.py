"""LUT2 internals: four SRAM cells addressed through a 4-to-1 multiplexer."""
from schemdraw import elements as elm
from _style import new_drawing, block, RED, RED_FILL, GREY

CELLS = [("00", "1"), ("01", "1"), ("10", "1"), ("11", "0")]   # NAND truth table


def draw():
    d = new_drawing()
    n = len(CELLS)
    mux = d.add(block(elm.Multiplexer(
        pins=[elm.IcPin(name=a, side="L", anchorname=f"d{i}", slot=f"{n - i}/{n}")
              for i, (a, _) in enumerate(CELLS)]
        + [elm.IcPin(name="", side="R", anchorname="y"),
           elm.IcPin(name="", side="B", anchorname="s0", slot="1/2"),
           elm.IcPin(name="", side="B", anchorname="s1", slot="2/2")],
        size=(2.2, 4.6), pinspacing=1.1)))
    ax = mux.absanchors

    cell_x = -3.8
    for i, (_, bit) in enumerate(CELLS):
        y = ax[f"d{i}"][1]
        cell = elm.Ic(pins=[elm.IcPin(name="", side="R", anchorname="q")],
                      size=(2.4, 0.8))
        d.add(block(cell, RED_FILL, RED).at((cell_x, y - 0.4))
              .label(f"stores {bit}", "center", fontsize=12, color=RED))
        d.add(elm.Line().at((cell_x + 2.4, y)).to(ax[f"d{i}"]))
    d.add(elm.Label().at((cell_x + 1.2, ax["d0"][1] + 0.75))
          .label("SRAM cells (configuration)", fontsize=11, color=RED))

    d.add(elm.Line().at(ax["y"]).to((ax["y"][0] + 1.6, ax["y"][1])))
    d.add(elm.Label().at((ax["y"][0] + 1.9, ax["y"][1])).label("out", halign="left"))

    left = cell_x - 0.4
    base = min(ax["s0"][1], ax["s1"][1]) - 0.8      # y of the first address wire
    for name, anchor, y_wire in (("in1", "s0", base), ("in2", "s1", base - 0.6)):
        x, y = ax[anchor]
        d.add(elm.Line().at((x, y)).to((x, y_wire)))
        d.add(elm.Line().at((x, y_wire)).to((left, y_wire)))
        d.add(elm.Label().at((left - 0.1, y_wire)).label(name, halign="right"))
    d.add(elm.Label().at((ax["s1"][0] + 0.4, base - 0.3))
          .label("address = (in2, in1)", fontsize=11, color=GREY, halign="left"))
    return d
