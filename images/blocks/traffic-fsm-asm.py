"""ASM chart of the traffic-light FSM (traffic_fsm.sv): one column per state.

Each column: state box (name and Moore outputs), a Tick decision, a
MsCount decision, and the conditional updates of MsCount. The 0 branches
loop back to the state's entry; the 1 branch leads to the next state.
"""
from schemdraw import flow
from schemdraw import elements as elm

from _style import new_drawing, block, line

STATES = [("RED", "Red = 1", "RED_MS"),
          ("RED_YELLOW", "Red = 1\nYellow = 1", "RED_YELLOW_MS"),
          ("GREEN", "Green = 1", "GREEN_MS"),
          ("YELLOW", "Yellow = 1", "YELLOW_MS")]
DX = 9.0          # column spacing
ROUTE = 3.1       # x offset of the line that leaves a column
TOP = 0.6         # height of the routing line between columns
EXIT = -8.0       # height of the routing line below the columns


def arrow(d, a, b):
    d.add(elm.Arrow().at(a).to(b))


def draw():
    d = new_drawing(fontsize=11)
    for i, (name, outs, limit) in enumerate(STATES):
        cx = i * DX
        lx = cx - 4.1                      # x of the loop-back line
        st = d.add(block(flow.Box(w=2.8, h=1.3)).at((cx, -0.5)).anchor("N")
                   .label(f"$\\bf{{{name.replace('_', chr(92) + '_')}}}$\n{outs}"))
        arrow(d, (cx, TOP), st.N)
        d1 = d.add(block(flow.Decision(w=2.2, h=1.2, W="0", S="1"), fill="white")
                   .at((cx, st.S[1] - 0.6)).anchor("N").label("Tick"))
        arrow(d, st.S, d1.N)
        d2 = d.add(block(flow.Decision(w=4.6, h=1.8, W="0", S="1"), fill="white")
                   .at((cx, d1.S[1] - 0.6)).anchor("N")
                   .label(f"MsCount ==\n{limit} - 1"))
        arrow(d, d1.S, d2.N)
        inc = d.add(block(flow.RoundBox(w=2.4, h=0.7)).at((lx, d2.W[1])).anchor("center")
                    .label("MsCount++"))
        clr = d.add(block(flow.RoundBox(w=2.6, h=0.7)).at((cx, d2.S[1] - 0.6)).anchor("N")
                    .label("MsCount = 0"))
        arrow(d, d2.W, inc.E)
        arrow(d, d2.S, clr.N)
        # both 0 branches loop back to the entry of the state box
        line(d, d1.W, (lx, d1.W[1]))
        d.add(elm.Dot().at((lx, d1.W[1])))
        line(d, inc.N, (lx, -0.2))
        arrow(d, (lx, -0.2), (cx, -0.2))
        # leave towards the next state
        nx = cx + DX if i < len(STATES) - 1 else -6.0
        line(d, clr.S, (cx, EXIT))
        if i < len(STATES) - 1:
            line(d, (cx, EXIT), (cx + ROUTE, EXIT), (cx + ROUTE, TOP), (nx, TOP))
        else:
            line(d, (cx, EXIT), (cx + ROUTE, EXIT), (cx + ROUTE, EXIT - 0.6),
                 (nx, EXIT - 0.6), (nx, TOP), (0, TOP))
    # reset enters RED
    d.add(elm.Arrow().at((0, TOP + 1.2)).to((0, TOP)))
    d.add(elm.Label().at((0, TOP + 1.5)).label("reset"))
    d.add(elm.Dot().at((0, TOP)))
    return d
