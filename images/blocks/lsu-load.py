"""Load data path of the LSU (HIPV rtl/core/lsu/lsu.sv) for two loads from the
same memory word 0x400 = 0xA1B2C3D4: `lw x1, 0x400(x0)` and
`lb x1, 0x402(x0)`. Each row shows the word from memory (ObiRdataM, the
lanes selected by ObiBeM highlighted), the word after the right shift by
8 * AddrLsbM (ReadShiftM), and the register value after extension
(ReadDataM, sign copies highlighted)."""
from schemdraw import elements as elm, flow
from _style import new_drawing, block, GREY, INK, RED, RED_FILL, FILL

W, H = 1.25, 0.95            # one byte cell
COLS = [3.6, 11.2, 18.8]     # x of the left edge of the three 4-byte words
ROWS = [3.4, 0.0]            # y of the centre line of the lw and lb rows


def cell(d, x, y, text, mark=False, copy=False):
    """One byte lane. mark: selected by ObiBeM / holds the loaded byte.
    copy: bits copied from the sign (or zero fill)."""
    el = flow.Box(w=W, h=H).at((x + W / 2, y)).anchor("center")
    if mark:
        el = block(el, fill=RED_FILL, edge=RED)
    elif copy:
        el = block(el, fill="#FFFFFF", edge=GREY).linestyle("--")
    else:
        el = block(el)
    d.add(el.label(text, loc="center", fontsize=11))


def word(d, x, y, bytes_, marks=(), copies=()):
    """bytes_ is written byte 3 first, as in a hexadecimal number."""
    for i, b in enumerate(bytes_):
        lane = 3 - i
        cell(d, x + i * W, y, b, mark=lane in marks, copy=lane in copies)


def text(d, xy, s, **kw):
    kw.setdefault("fontsize", 11)
    d.add(elm.Label().at(xy).label(s, **kw))


def arrow(d, a, b, label=None):
    d.add(elm.Arrow().at(a).to(b).color(INK))
    if label:
        text(d, ((a[0] + b[0]) / 2, a[1] + 0.85), label, color=GREY)


def draw():
    d = new_drawing()
    d.config(unit=2.5, fontsize=11)

    # column headers
    heads = ["memory word\n(ObiRdataM)", "after shift\n(ReadShiftM)",
             "register value\n(ReadDataM)"]
    for x, h in zip(COLS, heads):
        text(d, (x + 2 * W, ROWS[0] + 1.6), h, color=GREY)
    for x in COLS:
        for i, lane in enumerate("3210"):
            text(d, (x + i * W + W / 2, ROWS[0] + 0.78), lane, fontsize=9, color=GREY)

    # row 1: lw x1, 0x400(x0)
    y = ROWS[0]
    text(d, (0.0, y + 0.25), "lw x1, 0x400(x0)", halign="left", fontsize=12)
    text(d, (0.0, y - 0.35), "AddrLsbM = 0", halign="left", color=GREY)
    word(d, COLS[0], y, ["A1", "B2", "C3", "D4"], marks=(3, 2, 1, 0))
    word(d, COLS[1], y, ["A1", "B2", "C3", "D4"], marks=(3, 2, 1, 0))
    word(d, COLS[2], y, ["A1", "B2", "C3", "D4"], marks=(3, 2, 1, 0))
    arrow(d, (COLS[0] + 4 * W + 0.15, y), (COLS[1] - 0.15, y), ">> 0")
    arrow(d, (COLS[1] + 4 * W + 0.15, y), (COLS[2] - 0.15, y), "lw: keep all")
    text(d, (COLS[0] + 2 * W, y - 1.0), "ObiBeM = 1111", color=RED)

    # row 2: lb x1, 0x402(x0)
    y = ROWS[1]
    text(d, (0.0, y + 0.25), "lb x1, 0x402(x0)", halign="left", fontsize=12)
    text(d, (0.0, y - 0.35), "AddrLsbM = 2", halign="left", color=GREY)
    word(d, COLS[0], y, ["A1", "B2", "C3", "D4"], marks=(2,))
    word(d, COLS[1], y, ["00", "00", "A1", "B2"], marks=(0,))
    word(d, COLS[2], y, ["FF", "FF", "FF", "B2"], marks=(0,), copies=(3, 2, 1))
    arrow(d, (COLS[0] + 4 * W + 0.15, y), (COLS[1] - 0.15, y), ">> 16")
    arrow(d, (COLS[1] + 4 * W + 0.15, y), (COLS[2] - 0.15, y), "lb: sign-extend")
    text(d, (COLS[0] + 2 * W, y - 1.0), "ObiBeM = 0100", color=RED)
    text(d, (COLS[2] + 2 * W, y - 1.0), "bit 7 of 0xB2 is 1", color=GREY)
    return d
