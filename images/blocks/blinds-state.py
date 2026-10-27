"""State diagram of the window-blinds controller (a Mealy machine).

Each arrow is labelled condition / outputs that are 1 on that transition.
"""
from schemdraw import flow
from schemdraw import elements as elm
from _style import new_drawing, FILL, ACCENT


def draw():
    d = new_drawing()
    up = d.add(flow.State(r=1.1).at((0, 0)).anchor("center").label("UP")
               .fill(FILL).color(ACCENT))
    down = d.add(flow.State(r=1.1).at((8, 0)).anchor("center").label("DOWN")
                 .fill(FILL).color(ACCENT))
    d.add(flow.Arc2(k=0.35, arrow="->").at(up.NE).to(down.NW)
          .label("Button = 1 / Push = 1", "top", ofst=0.2))
    d.add(flow.Arc2(k=0.35, arrow="->").at(down.SW).to(up.SE)
          .label("Button = 1 / Pull = 1", "bottom", ofst=0.2))
    d.add(flow.ArcLoop(radius=0.9, arrow="->").at(up.SW).to(up.NW)
          .label("Button = 0 / –", "left", ofst=0.2))
    d.add(flow.ArcLoop(radius=0.9, arrow="->").at(down.NE).to(down.SE)
          .label("Button = 0 / –", "right", ofst=0.2))
    d.add(elm.Arrow().at((0, 2.6)).to(up.N).label("reset", "start"))
    return d
