"""Shared drawing of the five HIPV stages with the valid/ready handshake
between neighbours: valid arrows run forward on top, ready arrows run
backward below. Used by valid-ready-chain.py and valid-ready-stall.py."""
from schemdraw import elements as elm, flow
from schemdraw.backends import svg, svgtext
from _style import new_drawing, block, GREY, INK, RED, RED_FILL

# schemdraw's text-size estimate parses labels as XML and fails on '&';
# measure with a same-width stand-in instead (the drawn text is unchanged).
_text_approx_size = svgtext.text_approx_size


def _text_size_amp(text, *args, **kw):
    return _text_approx_size(text.replace("&", "8"), *args, **kw)


svgtext.text_approx_size = svg.text_approx_size = _text_size_amp

STAGES = ["Fetch", "Decode", "Execute", "Memory", "Writeback"]
PITCH, BW, BH = 6.0, 3.0, 2.4


def text(d, xy, s, **kw):
    kw.setdefault("fontsize", 11)
    d.add(elm.Label().at(xy).label(s, **kw))


def box_xy(i):
    return i * PITCH


def stage_box(d, i, title, sub=None, hot=False):
    x = box_xy(i)
    el = flow.Box(w=BW, h=BH).at((x + BW / 2, 0)).anchor("center")
    el = block(el, fill=RED_FILL, edge=RED) if hot else block(el)
    d.add(el)
    text(d, (x + BW / 2, 0.45 if sub else 0), title, fontsize=12)
    if sub:
        text(d, (x + BW / 2, -0.5), sub, fontsize=11, color=RED if hot else GREY)


def handshake(d, i, valid, ready, vlabel="valid", rlabel="ready"):
    """Arrows between stage i and i+1. valid/ready: 0 or 1 or None (no value shown)."""
    x0, x1 = box_xy(i) + BW, box_xy(i + 1)
    for y, a, b, name, val in ((0.55, x0, x1, vlabel, valid), (-0.55, x1, x0, rlabel, ready)):
        low = val == 0
        d.add(elm.Arrow().at((a + (0.1 if a < b else -0.1), y)).to((b + (-0.1 if a < b else 0.1), y))
              .color(RED if low else INK))
        label = name if val is None else f"{name} = {val}"
        text(d, ((a + b) / 2, y + (0.5 if y > 0 else -0.5)), label, color=RED if low else GREY, fontsize=10)


def new():
    d = new_drawing()
    d.config(unit=2.5, fontsize=11)
    return d
