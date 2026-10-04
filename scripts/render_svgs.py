#!/usr/bin/env python3
"""Convert hand-drawn SVGs (images/*.svg) to PDF for the LaTeX/PDF build.

Quarto would otherwise need rsvg-convert for every SVG in a PDF build;
filters/wave-pdf.lua swaps each images/**/*.svg for the .pdf made here and
by the other render_*.py scripts. Outputs are generated and git-ignored;
only stale PDFs are rebuilt unless --force.

Requires: pip install cairosvg
"""
import argparse
import sys
from pathlib import Path

import cairosvg

IMAGES_DIR = Path(__file__).resolve().parent.parent / "images"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--force", action="store_true", help="re-render everything")
    args = ap.parse_args()
    for svg in sorted(IMAGES_DIR.glob("*.svg")):
        pdf = svg.with_suffix(".pdf")
        if not args.force and pdf.exists() and pdf.stat().st_mtime >= svg.stat().st_mtime:
            continue
        try:
            cairosvg.svg2pdf(url=str(svg), write_to=str(pdf))
        except Exception as e:
            print(f"error: {svg.name}: {e}", file=sys.stderr)
            return 1
        print(f"rendered {svg.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
