"""The traffic-light system: a 1 ms tick generator enabling the traffic-light FSM."""
from schemdraw import flow
from schemdraw import elements as elm
from _style import new_drawing, block, line, GREY


def arrow(d, a, b):
    d.add(elm.Arrow().at(a).to(b))


def lamp(d, xy, color):
    d.add(flow.Circle(r=0.35).at(xy).anchor("center").fill(color).color("#2C3E50"))


def draw():
    d = new_drawing()
    tick = d.add(block(flow.Box(w=4.4, h=2.6)).at((0, 0)).anchor("center")
                 .label("tick_gen\n\ncounter 0 ... 99 999\nTICK_CYCLES = 100 000",
                        fontsize=11))
    fsm = d.add(block(flow.Box(w=4.4, h=3.4)).at((8.4, 0)).anchor("center")
                .label("traffic_fsm\n\nState\nMsCount\nRED_MS ... YELLOW_MS",
                       fontsize=11))
    arrow(d, tick.E, (fsm.W[0], 0))
    d.add(elm.Label().at((4.2, 0.4)).label("Tick", fontsize=11))
    d.add(elm.Label().at((4.2, -0.4)).label("1 pulse / ms", fontsize=10, color=GREY))

    # clk and reset go to both modules
    bot = -2.6
    for x0, box in ((tick.S[0], tick), (fsm.S[0], fsm)):
        arrow(d, (x0 - 0.4, bot - 0.6), (x0 - 0.4, box.S[1]))
        arrow(d, (x0 + 0.4, bot - 1.2), (x0 + 0.4, box.S[1]))
    line(d, (-3.6, bot - 0.6), (fsm.S[0] - 0.4, bot - 0.6))
    line(d, (-3.6, bot - 1.2), (fsm.S[0] + 0.4, bot - 1.2))
    d.add(elm.Dot().at((tick.S[0] - 0.4, bot - 0.6)))
    d.add(elm.Dot().at((tick.S[0] + 0.4, bot - 1.2)))
    d.add(elm.Label().at((-3.7, bot - 0.6)).label("clk", halign="right", fontsize=11))
    d.add(elm.Label().at((-3.7, bot - 1.2)).label("reset", halign="right", fontsize=11))

    # outputs to the lamps
    ex = fsm.E[0]
    for y, name, color in ((1.0, "Red", "#E74C3C"), (0.0, "Yellow", "#F4D03F"),
                           (-1.0, "Green", "#2ECC71")):
        arrow(d, (ex, y), (ex + 2.2, y))
        d.add(elm.Label().at((ex + 1.0, y + 0.3)).label(name, fontsize=11))
        lamp(d, (ex + 2.6, y), color)

    # module boundary of the top level
    d.add(elm.Line().at((-2.9, 2.6)).to((11.1, 2.6)).linestyle("--").color(GREY))
    d.add(elm.Line().at((11.1, 2.6)).to((11.1, -4.3)).linestyle("--").color(GREY))
    d.add(elm.Line().at((11.1, -4.3)).to((-2.9, -4.3)).linestyle("--").color(GREY))
    d.add(elm.Line().at((-2.9, -4.3)).to((-2.9, 2.6)).linestyle("--").color(GREY))
    d.add(elm.Label().at((-2.7, 2.3)).label("traffic_light", halign="left", fontsize=11,
                                            color=GREY))
    return d
