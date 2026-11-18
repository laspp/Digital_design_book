"""Propagation of valid and ready through the HIPV pipeline: valid forward
through one register per stage, ready backward through logic only, and the
redirect PCSrcE from Execute that clears valid in Fetch and Decode."""
from schemdraw import elements as elm
from _style import GREY, INK, RED
from _valid_ready import (new, stage_box, handshake, text, box_xy, STAGES, BW, BH)


def draw():
    d = new()
    for i, name in enumerate(STAGES):
        stage_box(d, i, name)
    for i in range(4):
        handshake(d, i, None, None)

    # notes under the stages
    notes = ["ValidF = DONE & ~PCSrcE", "ValidD = ValidDReg & ~PCSrcE", "ValidE = ValidEReg",
             "ValidM = ValidMReg & (~MemOpM | DoneM)", "ReadyW = 1"]
    for i, n in enumerate(notes):
        text(d, (box_xy(i) + BW / 2, -2.0), n, fontsize=9, color=GREY)

    # redirect from Execute back to Fetch and Decode, above the boxes
    ye = BH / 2
    xe = box_xy(2) + BW / 2
    ytop = ye + 1.9
    pts = [(xe, ye), (xe, ytop)]
    d.add(elm.Line().at(pts[0]).to(pts[1]).color(RED))
    d.add(elm.Line().at((xe, ytop)).to((box_xy(0) + BW / 2, ytop)).color(RED))
    for i in (0, 1):
        x = box_xy(i) + BW / 2
        if i == 1:
            d.add(elm.Dot().at((x, ytop)).color(RED))
        d.add(elm.Arrow().at((x, ytop)).to((x, ye + 0.1)).color(RED))
    text(d, (box_xy(1) + BW / 2 + 3.0, ytop + 0.5), "PCSrcE: redirect clears valid in Fetch and Decode",
         color=RED, fontsize=10)

    # direction hints
    text(d, (box_xy(4) + BW + 0.2, 0.55), "valid, forward", halign="left", color=GREY, fontsize=10)
    text(d, (box_xy(4) + BW + 0.2, -0.55), "ready, backward", halign="left", color=GREY, fontsize=10)
    return d
