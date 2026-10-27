"""General structure of an FSM: next-state logic, state register, output logic.

The Moore output logic sees only the state; the Mealy output logic also sees
the inputs.
"""
from schemdraw import flow
from schemdraw import elements as elm
from _style import new_drawing, block, dff, line


def arrow(d, a, b):
    d.add(elm.Arrow().at(a).to(b))


def draw():
    d = new_drawing()
    nsl = d.add(block(flow.Box(w=2.8, h=3.2)).at((0, 0)).anchor("center")
                .label("next-state\nlogic\n(comb.)"))
    reg = dff(size=(2.0, 2.4))
    d.add(reg.anchor("D").at((3.6, 0)))
    d.add(elm.Label().at((4.6, -2.3)).label("state register", fontsize=11))
    arrow(d, (1.4, 0), reg.absanchors["D"])
    d.add(elm.Label().at((2.5, 0.35)).label("NextState", fontsize=11))
    clk = reg.absanchors["CLK"]
    line(d, (clk[0] - 0.8, clk[1]), clk)
    d.add(elm.Label().at((clk[0] - 1.0, clk[1])).label("clk", halign="right", fontsize=11))

    q = reg.absanchors["Q"]
    jx = q[0] + 0.9
    line(d, q, (jx, q[1]))
    d.add(elm.Dot().at((jx, 0)))
    d.add(elm.Label().at((jx + 0.1, 0.35)).label("State", halign="left", fontsize=11))
    # feedback of the state to the next-state logic
    line(d, (jx, 0), (jx, 2.6), (-2.2, 2.6), (-2.2, 0.8))
    arrow(d, (-2.2, 0.8), (-1.4, 0.8))
    # input
    line(d, (-4.0, -0.8), (-2.8, -0.8))
    d.add(elm.Dot().at((-2.8, -0.8)))
    arrow(d, (-2.8, -0.8), (-1.4, -0.8))
    d.add(elm.Label().at((-4.1, -0.8)).label("Inputs", halign="right"))

    bx = jx + 2.6
    moore = d.add(block(flow.Box(w=2.8, h=1.6)).at((bx, 1.8)).anchor("W")
                  .label("output logic\n(Moore)"))
    mealy = d.add(block(flow.Box(w=2.8, h=1.6)).at((bx, -2.2)).anchor("W")
                  .label("output logic\n(Mealy)"))
    d.add(elm.Dot().at((jx, 1.8)))
    arrow(d, (jx, 1.8), moore.W)
    line(d, (jx, 0), (jx, -1.8))
    arrow(d, (jx, -1.8), (bx, -1.8))
    line(d, (-2.8, -0.8), (-2.8, -3.8), (bx - 0.8, -3.8), (bx - 0.8, -2.6))
    arrow(d, (bx - 0.8, -2.6), (bx, -2.6))
    for box, txt in ((moore, "Outputs"), (mealy, "Outputs")):
        arrow(d, box.E, (box.E[0] + 1.4, box.E[1]))
        d.add(elm.Label().at((box.E[0] + 1.5, box.E[1])).label(txt, halign="left"))
    return d
