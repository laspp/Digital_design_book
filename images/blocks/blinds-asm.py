"""ASM chart of the window-blinds controller: Mealy outputs in conditional boxes."""
from schemdraw import flow
from schemdraw import elements as elm
from _style import new_drawing, block, line

STATES = [("UP", "Push = 1"), ("DOWN", "Pull = 1")]
DX = 6.0
TOP = 0.6
EXIT = -5.2


def arrow(d, a, b):
    d.add(elm.Arrow().at(a).to(b))


def draw():
    d = new_drawing(fontsize=11)
    for i, (name, out) in enumerate(STATES):
        cx = i * DX
        lx = cx - 2.0
        st = d.add(block(flow.Box(w=2.4, h=1.0)).at((cx, -0.5)).anchor("N")
                   .label(f"$\\bf{{{name}}}$"))
        arrow(d, (cx, TOP), st.N)
        dec = d.add(block(flow.Decision(w=2.4, h=1.3, W="0", S="1"), fill="white")
                    .at((cx, st.S[1] - 0.6)).anchor("N").label("Button"))
        arrow(d, st.S, dec.N)
        cond = d.add(block(flow.RoundBox(w=2.2, h=0.7)).at((cx, dec.S[1] - 0.6))
                     .anchor("N").label(out))
        arrow(d, dec.S, cond.N)
        line(d, dec.W, (lx, dec.W[1]), (lx, -0.2))
        arrow(d, (lx, -0.2), (cx, -0.2))
        line(d, cond.S, (cx, EXIT))
        if i == 0:
            line(d, (cx, EXIT), (cx + 2.4, EXIT), (cx + 2.4, TOP), (cx + DX, TOP))
        else:
            line(d, (cx, EXIT), (cx + 2.4, EXIT), (cx + 2.4, EXIT - 0.6),
                 (-3.0, EXIT - 0.6), (-3.0, TOP), (0, TOP))
    d.add(elm.Arrow().at((0, TOP + 1.2)).to((0, TOP)))
    d.add(elm.Label().at((0, TOP + 1.5)).label("reset"))
    d.add(elm.Dot().at((0, TOP)))
    return d
