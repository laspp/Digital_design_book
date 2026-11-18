"""A load waiting for the data memory stalls the pipeline: ReadyM falls first
and forces ReadyE and ReadyD low in the same cycle, so Fetch holds its output.
Writeback sees ValidM = 0, a bubble."""
from _style import GREY
from _valid_ready import new, stage_box, handshake, text, box_xy, BW


def draw():
    d = new()
    stage_box(d, 0, "Fetch", "or x5, x4, x2", hot=True)
    stage_box(d, 1, "Decode", "sub x4, x3, x2", hot=True)
    stage_box(d, 2, "Execute", "add x3, x2, x1", hot=True)
    stage_box(d, 3, "Memory", "lw x1, 0x400(x0)", hot=True)
    stage_box(d, 4, "Writeback", "bubble")
    handshake(d, 0, 1, 0)   # F -> D: ValidF = 1, ReadyD = 0
    handshake(d, 1, 1, 0)   # D -> E: ValidD = 1, ReadyE = 0
    handshake(d, 2, 1, 0)   # E -> M: ValidE = 1, ReadyM = 0
    handshake(d, 3, 0, 1)   # M -> W: ValidM = 0, ReadyW = 1
    text(d, (box_xy(3) + BW / 2, -2.0), "waits for ObiRvalidM", fontsize=10, color=GREY)
    text(d, (box_xy(1) + BW / 2 + 3.0, -2.0), "ReadyM falls first, the chain follows in the same cycle",
         fontsize=10, color=GREY)
    return d
