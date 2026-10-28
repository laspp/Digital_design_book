"""Overview of the HIPV core pipeline (rtl/core/hipv_core.sv): five stages with
valid/ready handshakes, the redirect and write-back feedback, the two OBI
ports as buses, and the hazard unit."""
from schemdraw import flow
from schemdraw import elements as elm
from _style import new_drawing, block, line, ACCENT, GREY, RED, RED_FILL

W, H, PITCH = 3.2, 4.0, 5.4          # stage box size and spacing
STAGES = [("IFU", "Fetch (F)"), ("IDU", "Decode (D)"), ("IEU", "Execute (E)"),
          ("LSU", "Memory (M)"), ("WBU", "Writeback (W)")]
TOP, BOT = H / 2, -H / 2


def arrow(d, *pts, **kw):
    if len(pts) > 2:
        line(d, *pts[:-1])
    d.add(elm.Arrow(**kw).at(pts[-2]).to(pts[-1]))


def label(d, xy, text, **kw):
    kw.setdefault("fontsize", 11)
    d.add(elm.Label().at(xy).label(text, **kw))


def bus(d, a, b, text):
    d.add(elm.Line(arrow="<|-|>", headwidth=0.45, headlength=0.4).at(a).to(b)
          .linewidth(5).color(ACCENT))
    label(d, (a[0] + 0.25, (a[1] + b[1]) / 2), text, halign="left", color=ACCENT)


def draw():
    d = new_drawing()
    xs = []
    for i, (name, stage) in enumerate(STAGES):
        x = i * PITCH
        xs.append(x)
        # the IDU label sits lower, to leave room for the register file
        ofst = (0, -0.6) if name == "IDU" else None
        d.add(block(flow.Box(w=W, h=H)).at((x, 0)).anchor("center")
              .label(f"$\\bf{{{name}}}$\n{stage}", ofst=ofst))
        if i:
            arrow(d, (xs[i - 1] + W / 2, 0), (x - W / 2, 0))
            label(d, ((xs[i - 1] + x) / 2, 0.35), "V/R", fontsize=9, color=GREY)
    xf, xd, xe, xm, xw = xs

    # register file inside the IDU
    rf = d.add(block(flow.Box(w=1.8, h=1.0), fill="white").at((xd + 0.5, TOP - 0.25))
               .anchor("N").label("regfile", fontsize=10))

    # redirect: branch / jal / jalr resolved in E -> IFU, and flush of the IDU
    y_j = TOP + 1.1
    arrow(d, (xe, TOP), (xe, y_j), (xf, y_j), (xf, TOP))
    d.add(elm.Dot().at((xd - 1.0, y_j)))
    arrow(d, (xd - 1.0, y_j), (xd - 1.0, TOP))
    label(d, ((xd + 0.5 + xe) / 2 + 0.2, y_j + 0.55), "PCSrcE, PCTargetE\n(branch, jump)",
          fontsize=10)

    # write-back into the register file
    y_w = TOP + 2.3
    arrow(d, (xw, TOP), (xw, y_w), (rf.N[0], y_w), rf.N)
    label(d, ((xd + xw) / 2 + 1.5, y_w + 0.35), "RegWriteW, RdW, ResultW", fontsize=10)

    # OBI buses to the memories
    y_mem = BOT - 3.0
    for x, name, text in ((xf, "instruction\nmemory", "OBI (instr.)"),
                          (xm + 0.6, "data\nmemory", "OBI (data)")):
        m = d.add(block(flow.Box(w=3.4, h=1.4), RED_FILL, RED).at((x, y_mem)).anchor("N")
                  .label(name, color=RED))
        bus(d, (x, BOT), m.N, text)

    # hazard unit
    hz = d.add(block(flow.Box(w=3.6, h=1.4)).at((xe, BOT - 3.0)).anchor("N")
               .label("hazard unit"))
    arrow(d, (xe - 0.8, BOT), (xe - 0.8, hz.N[1]))
    arrow(d, (xe + 0.2, hz.N[1]), (xe + 0.2, BOT))
    arrow(d, (xm - 0.8, BOT), (xm - 0.8, BOT - 1.5), (xe + 1.2, BOT - 1.5),
          (xe + 1.2, hz.N[1]))
    y_h = hz.S[1] - 0.8
    arrow(d, (xw, BOT), (xw, y_h), (xe + 0.6, y_h), (xe + 0.6, hz.S[1]))
    return d
