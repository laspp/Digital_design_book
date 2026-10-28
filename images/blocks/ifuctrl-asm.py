"""ASM chart of the IFU control FSM (HIPV rtl/core/ifu/ifuctrl.sv).

Transitions and the DiscardF register: one column per state, decisions, the
DiscardF updates (rounded boxes) and the paths to the next state. The outputs
are shown in a separate diagram. Where no box is shown, DiscardF keeps its
value; ObiRvalidF only arrives in WAIT_RESP, so the clear is shown there.
"""
from schemdraw import flow
from schemdraw import elements as elm
from schemdraw.backends import svg, svgtext
from _style import new_drawing, block, line

# schemdraw's text-size estimate parses labels as XML and fails on '&';
# measure with a same-width stand-in instead (the drawn text is unchanged).
_text_approx_size = svgtext.text_approx_size


def _text_size_amp(text, *args, **kw):
    return _text_approx_size(text.replace("&", "8"), *args, **kw)


svgtext.text_approx_size = svg.text_approx_size = _text_size_amp

DX = 10.0         # column spacing
ENTRY = 0.5       # height where loop-backs join the entry of a state box
TOP1 = 1.4        # routing line into WAIT_RESP and DONE
TOP2 = 2.2        # routing line into REQUEST
BOT = -9.2        # routing line back to REQUEST


def arrow(d, *pts):
    """Polyline through pts with an arrowhead on the last segment."""
    if len(pts) > 2:
        line(d, *pts[:-1])
    d.add(elm.Arrow().at(pts[-2]).to(pts[-1]))


def state(d, x, name, top):
    st = d.add(block(flow.Box(w=3.0, h=1.2)).at((x, 0)).anchor("N")
               .label(f"$\\bf{{{name.replace('_', chr(92) + '_')}}}$"))
    arrow(d, (x, top), st.N)
    return st


def dec(d, xy, text, w=2.8, **exits):
    return d.add(block(flow.Decision(w=w, h=1.4, **exits), fill="white")
                 .at(xy).anchor("center").label(text))


def cond(d, xy, text):
    return d.add(block(flow.RoundBox(w=2.6, h=0.75)).at(xy).anchor("center").label(text))


def loop_back(d, frm, x_col):
    """0 exit on the left of a decision, back to the entry of its state box."""
    lx = x_col - 2.8
    line(d, frm, (lx, frm[1]), (lx, ENTRY))
    arrow(d, (lx, ENTRY), (x_col, ENTRY))


def draw():
    d = new_drawing(fontsize=11)
    xr, xw, xd = 0.0, DX, DX + 7.5

    # REQUEST: a redirect in the cycle of the grant makes the response stale
    st = state(d, xr, "REQUEST", TOP2)
    gnt = dec(d, (xr, -2.4), "ObiGntF", W="0", S="1")
    arrow(d, st.S, gnt.N)
    loop_back(d, gnt.W, xr)
    p = dec(d, (xr, -4.6), "PCSrcE", w=2.6, S="1", E="0")
    arrow(d, gnt.S, p.N)
    c = cond(d, (xr, -6.6), "DiscardF = 1")
    arrow(d, p.S, c.N)
    y_j = -7.8
    line(d, p.E, (xr + 2.0, p.E[1]), (xr + 2.0, y_j))
    d.add(elm.Dot().at((xr + 2.0, y_j)))
    line(d, c.S, (xr, y_j), (xr + 3.0, y_j), (xr + 3.0, TOP1), (xw, TOP1))

    # WAIT_RESP
    st = state(d, xw, "WAIT_RESP", TOP1)
    rv = dec(d, (xw, -2.4), "ObiRvalidF", w=3.2, W="0", S="1")
    arrow(d, st.S, rv.N)
    # no response yet: a redirect makes the outstanding response stale
    xq = xw - 3.6
    arrow(d, rv.W, (xq, rv.W[1]), (xq, -3.9))
    q = dec(d, (xq, -4.6), "PCSrcE", w=2.6, W="0", S="1")
    c = cond(d, (xq, -6.6), "DiscardF = 1")
    arrow(d, q.S, c.N)
    lx = xq - 2.0
    line(d, q.W, (lx, q.W[1]), (lx, ENTRY))
    arrow(d, (lx, ENTRY), (xw, ENTRY))
    line(d, c.S, (xq, -7.6), (lx, -7.6), (lx, q.W[1]))
    d.add(elm.Dot().at((lx, q.W[1])))
    # response: drop it if stale or redirected, else hand it to Decode
    ds = dec(d, (xw, -4.8), "DiscardF |\nPCSrcE", w=3.2, S="1", E="0")
    arrow(d, rv.S, ds.N)
    c = cond(d, (xw, -6.9), "DiscardF = 0")
    arrow(d, ds.S, c.N)
    x_up = xw + 3.0
    line(d, ds.E, (x_up, ds.E[1]), (x_up, TOP1), (xd, TOP1))
    x_back = xr - 3.8
    line(d, c.S, (xw, BOT), (x_back, BOT), (x_back, TOP2), (xr, TOP2))

    # DONE
    st = state(d, xd, "DONE", TOP1)
    rd = dec(d, (xd, -2.4), "ReadyD |\nPCSrcE", w=3.0, W="0", S="1")
    arrow(d, st.S, rd.N)
    loop_back(d, rd.W, xd)
    line(d, rd.S, (xd, BOT), (xw, BOT))
    d.add(elm.Dot().at((xw, BOT)))

    # reset enters REQUEST
    d.add(elm.Arrow().at((xr, TOP2 + 1.2)).to((xr, TOP2)))
    d.add(elm.Label().at((xr, TOP2 + 1.5)).label("reset"))
    d.add(elm.Dot().at((xr, TOP2)))
    return d
