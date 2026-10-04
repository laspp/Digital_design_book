#!/usr/bin/env python3
"""Render SystemVerilog modules (images/rtl/*.sv) to SVG and PDF schematics.

Pipeline: Yosys (read_verilog -sv; proc; opt; JSON netlist) -> netlistsvg
-> SVG -> PDF (cairosvg). The module drawn is the one named like the file.
Outputs next to the source are generated and git-ignored; stale-only unless
--force.

Requires: pip install yowasp-yosys cairosvg nodejs-wheel-binaries
          npm install --prefix .tools netlistsvg
"""
import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

import cairosvg
from nodejs_wheel.executable import ROOT_DIR as NODE_ROOT

ROOT = Path(__file__).resolve().parent.parent
RTL_DIR = ROOT / "images" / "rtl"
NETLISTSVG = ROOT / ".tools" / "node_modules" / "netlistsvg" / "bin" / "netlistsvg.js"
NODE = Path(NODE_ROOT) / "bin" / "node"
YOSYS = Path(sys.executable).parent / "yowasp-yosys"


def render(src: Path, force: bool) -> bool:
    svg, pdf = src.with_suffix(".svg"), src.with_suffix(".pdf")
    if not force and svg.exists() and pdf.exists() \
            and min(svg.stat().st_mtime, pdf.stat().st_mtime) >= src.stat().st_mtime:
        return False
    with tempfile.TemporaryDirectory() as tmp:
        netlist = Path(tmp) / "netlist.json"
        script = (f"read_verilog -sv {src}; hierarchy -top {src.stem}; "
                  f"proc; opt; write_json {netlist}")
        subprocess.run([str(YOSYS), "-q", "-p", script], check=True)
        subprocess.run([str(NODE), str(NETLISTSVG), str(netlist), "-o", str(svg)],
                       check=True)
    cairosvg.svg2pdf(url=str(svg), write_to=str(pdf))
    print(f"rendered {src.name}")
    return True


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--force", action="store_true", help="re-render everything")
    args = ap.parse_args()
    for src in sorted(RTL_DIR.glob("*.sv")):
        try:
            render(src, args.force)
        except Exception as e:
            print(f"error: {src.name}: {e}", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
