#!/usr/bin/env python3
"""Render schemdraw block diagrams (images/blocks/*.py) to SVG and PDF.

Each source defines draw() -> schemdraw.Drawing (files starting with
_ are shared helpers, e.g. _style.py). The .svg/.pdf next to it
are generated and git-ignored; only stale outputs are re-rendered unless
--force.

Requires: pip install schemdraw
"""
import argparse
import importlib.util
import sys
from pathlib import Path

BLOCKS_DIR = Path(__file__).resolve().parent.parent / "images" / "blocks"


def render(src: Path, force: bool) -> bool:
    svg, pdf = src.with_suffix(".svg"), src.with_suffix(".pdf")
    if not force and svg.exists() and pdf.exists() \
            and min(svg.stat().st_mtime, pdf.stat().st_mtime) >= src.stat().st_mtime:
        return False
    sys.path.insert(0, str(BLOCKS_DIR))   # lets sources import _style.py
    spec = importlib.util.spec_from_file_location(src.stem, src)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    drawing = mod.draw()
    drawing.save(str(svg))
    drawing.save(str(pdf))
    print(f"rendered {src.name}")
    return True


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--force", action="store_true", help="re-render everything")
    args = ap.parse_args()
    for src in sorted(BLOCKS_DIR.glob("*.py")):
        if src.name.startswith("_"):   # shared helpers, not diagrams
            continue
        try:
            render(src, args.force)
        except Exception as e:
            print(f"error: {src.name}: {e}", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
