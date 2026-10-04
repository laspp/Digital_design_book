#!/usr/bin/env python3
"""Render WaveDrom sources (images/waves/*.json) to SVG and PDF.

The .json files (WaveJSON, https://wavedrom.com/tutorial.html) are the
source of truth; the .svg/.pdf next to them are generated and git-ignored.
Only sources newer than their output are re-rendered, unless --force.

Requires: pip install wavedrom cairosvg
"""
import argparse
import json
import sys
from pathlib import Path

import cairosvg
import wavedrom

WAVES_DIR = Path(__file__).resolve().parent.parent / "images" / "waves"


def render(src: Path, force: bool) -> bool:
    svg, pdf = src.with_suffix(".svg"), src.with_suffix(".pdf")
    if not force and svg.exists() and pdf.exists() \
            and min(svg.stat().st_mtime, pdf.stat().st_mtime) >= src.stat().st_mtime:
        return False
    drawing = wavedrom.render(json.dumps(json.loads(src.read_text())))
    drawing.saveas(str(svg))
    cairosvg.svg2pdf(url=str(svg), write_to=str(pdf))
    print(f"rendered {src.name}")
    return True


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--force", action="store_true", help="re-render everything")
    args = ap.parse_args()
    sources = sorted(WAVES_DIR.glob("*.json"))
    if not sources:
        print(f"no sources in {WAVES_DIR}")
    for src in sources:
        try:
            render(src, args.force)
        except Exception as e:
            print(f"error: {src.name}: {e}", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
