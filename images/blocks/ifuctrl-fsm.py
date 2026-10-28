"""State diagram of the IFU control FSM (HIPV rtl/core/ifu/ifuctrl.sv).

Transitions only: each arrow carries its condition. The outputs are shown
in a separate diagram.
"""
from schemdraw import flow
from schemdraw import elements as elm
from schemdraw.backends import svg, svgtext
from _style import new_drawing, FILL, ACCENT

# schemdraw's text-size estimate parses labels as XML and fails on '&';
# measure with a same-width stand-in instead (the drawn text is unchanged).
_text_approx_size = svgtext.text_approx_size


def _text_size_amp(text, *args, **kw):
    return _text_approx_size(text.replace("&", "8"), *args, **kw)


svgtext.text_approx_size = svg.text_approx_size = _text_size_amp


def state(d, xy, text):
    return d.add(flow.State(r=1.35).at(xy).anchor("center").label(text, fontsize=11)
                 .fill(FILL).color(ACCENT))


def label(d, xy, text, **kw):
    kw.setdefault("fontsize", 11)
    d.add(elm.Label().at(xy).label(text, **kw))


def draw():
    d = new_drawing()
    req = state(d, (0, 0), "$\\bf{REQUEST}$")
    wait = state(d, (9, 0), "$\\bf{WAIT\\_RESP}$")
    done = state(d, (4.5, -6.5), "$\\bf{DONE}$")

    # REQUEST
    d.add(flow.Arc2(k=0.3, arrow="->").at(req.NE).to(wait.NW))
    label(d, (4.5, 2.3), "ObiGntF")
    d.add(flow.ArcLoop(radius=1.1, arrow="->").at(req.SW).to(req.NW))
    label(d, (-3.1, 0), "~ObiGntF", halign="right")

    # WAIT_RESP
    d.add(flow.Arc2(k=0.15, arrow="->").at(wait.W).to(req.E))
    label(d, (4.5, -0.75), "ObiRvalidF & (DiscardF | PCSrcE)")
    d.add(flow.Arc2(k=0.25, arrow="->").at(wait.S).to(done.E))
    label(d, (8.6, -4.2), "ObiRvalidF &\n~(DiscardF | PCSrcE)", halign="left")
    d.add(flow.ArcLoop(radius=1.1, arrow="->").at(wait.NE).to(wait.SE))
    label(d, (12.1, 0), "~ObiRvalidF", halign="left")

    # DONE
    d.add(flow.Arc2(k=0.25, arrow="->").at(done.W).to(req.S))
    label(d, (0.4, -4.2), "ReadyD | PCSrcE", halign="right")
    d.add(flow.ArcLoop(radius=1.1, arrow="->").at(done.SE).to(done.SW))
    label(d, (4.5, -9.7), "~ReadyD & ~PCSrcE")

    d.add(elm.Arrow().at((-2.6, 2.6)).to(req.NW))
    label(d, (-2.8, 2.8), "reset", halign="right")
    return d
