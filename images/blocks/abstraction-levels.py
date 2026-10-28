"""Levels of abstraction, each with what it looks like for the HIPV SoC.
RTL, the level this course designs at, is highlighted."""
from schemdraw import flow
from schemdraw import elements as elm
from _style import new_drawing, block, ACCENT, FILL, GREY

LEVELS = [
    ("System", "HIPV SoC: core, OBI crossbar, RAM, UART, timer, GPIO"),
    ("Algorithmic", "RV32I: fetch, decode, execute, access memory, write back"),
    ("RTL", "hipv_core.sv: IFU, IDU, IEU, LSU, WBU built from flopenr, mux2, adder"),
    ("Gate", "netlist of LUT6, FDRE, CARRY4 and RAMB36E1 cells for the xc7a100t"),
    ("Transistor", "CMOS: SRAM cells, pass transistors, inverters"),
    ("Material", "doped silicon in a 28 nm process"),
]
BW, BH, GAP = 13.0, 1.1, 0.35
STEPS = {2: "synthesis", 3: "FPGA vendor", 4: "foundry"}   # step below level i


def draw():
    d = new_drawing()
    ys = []
    for i, (name, text) in enumerate(LEVELS):
        y = -i * (BH + GAP)
        ys.append(y)
        rtl = name == "RTL"
        d.add(block(flow.Box(w=BW, h=BH), fill=ACCENT if rtl else FILL)
              .at((0, y)).anchor("W")
              .label(text, fontsize=11, color="white" if rtl else ACCENT))
        d.add(elm.Label().at((-0.3, y - 0.12)).label(f"$\\bf{{{name}}}$", halign="right",
                                               fontsize=12))
    d.add(elm.Label().at((BW + 0.3, ys[2])).label("this course", halign="left",
                                                   fontsize=11, color=ACCENT))

    # left: abstraction grows upwards
    x_up = -3.6
    d.add(elm.Arrow().at((x_up, ys[-1] - 0.3)).to((x_up, ys[0] + 0.3)).color(GREY))
    d.add(elm.Label().at((x_up - 0.3, (ys[0] + ys[-1]) / 2))
          .label("more abstract,\nfewer details", halign="right", fontsize=10, color=GREY))

    # right: who turns one level into the next, below RTL
    x_dn = BW + 3.4
    for i, text in STEPS.items():
        d.add(elm.Arrow().at((x_dn, ys[i] - 0.2)).to((x_dn, ys[i + 1] + 0.2)).color(GREY))
        d.add(elm.Label().at((x_dn + 0.3, (ys[i] + ys[i + 1]) / 2))
              .label(text, halign="left", fontsize=10, color=GREY))
    return d
