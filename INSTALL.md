# Environment setup

This project has two tiers of requirements, depending on what you need to do.

- **Writing/editing chapters, rendering slides or the book**: just Quarto
  (and TinyTeX for PDF output).
- **Regenerating the diagrams** (`scripts/render_*.py`, wired together by
  `scripts/render.sh` / the Makefile): Quarto, plus a handful of Python
  packages and a local Node.js toolchain, documented below.

If you only edit `.qmd` prose and the diagrams already have up-to-date
`.svg`/`.pdf`/`.png` outputs checked out, you can skip straight to
"Core requirements".

## Core requirements

1. **Quarto**: <https://quarto.org/docs/get-started/>
2. **TinyTeX** (for the PDF book build, `xelatex`):
   ```bash
   quarto install tinytex
   ```
3. **Liberation fonts** (used as the PDF's main/sans/mono fonts, see
   `_quarto.yml`):
   - Arch: `sudo pacman -S ttf-liberation`
   - Debian/Ubuntu: `sudo apt-get install fonts-liberation`
   - macOS (Homebrew): `brew install --cask font-liberation`
4. **`rsvg-convert`**: Quarto's own LaTeX filter falls back to this for any
   `.svg` image that does not already have a pre-rendered `.pdf` sibling
   (see "How the PDF pipeline avoids rsvg-convert" below for why that
   matters here specifically).
   - Arch: `sudo pacman -S librsvg` (provides `rsvg-convert`)
   - Debian/Ubuntu: `sudo apt-get install librsvg2-bin`
   - macOS (Homebrew): `brew install librsvg`

At this point `quarto render` (HTML or PDF) and `quarto preview` work for
any chapter that already has its generated image files checked out.

## Diagram-generation toolchain

Four scripts regenerate the project's diagrams from source
(`images/waves/*.json`, `images/blocks/*.py`, `images/rtl/*.sv`, and
hand-drawn `images/*.svg`). Their outputs (`.svg`/`.pdf`/`.png` next to
each source) are git-ignored and only rebuilt when the source is newer —
most contributors will never need to run them.

### 1. Python packages available via your OS package manager

These install cleanly as system packages (recommended over `pip` for them
specifically, since they're plain Python libraries with no project-local
state):

- Arch: `sudo pacman -S python-cairosvg python-wavedrom python-schemdraw python-matplotlib`
- Debian/Ubuntu: `sudo apt-get install python3-cairosvg python3-wavedrom python3-schemdraw python3-matplotlib`
  (package names may vary/be missing on older releases; fall back to pip
  in a venv if so)

`python-matplotlib` is required because `schemdraw` silently falls back to
an SVG-only backend without it, and `scripts/render_blocks.py` needs to
save both `.svg` and `.pdf`.

### 2. A project-local virtualenv for the rest

`yowasp-yosys` (a WASM-packaged Yosys, used to synthesize the RTL
schematics) and `nodejs-wheel-binaries` (a pip-installable, bundled
Node.js, used to run `netlistsvg`) are not packaged for most Linux
distros. Install them into a venv that inherits the system packages from
step 1, instead of fighting `pip`'s externally-managed-environment error
or installing them system-wide:

```bash
python3 -m venv --system-site-packages .venv
.venv/bin/pip install yowasp-yosys nodejs-wheel-binaries
```

### 3. `netlistsvg`, via the venv's bundled Node

`nodejs-wheel-binaries` bundles `node`/`npm` but does not put them on your
`PATH`; drive `npm` through its Python API instead (its `bin/npm` shim
script is broken in at least the current release):

```bash
mkdir -p .tools
.venv/bin/python3 -c "
import nodejs_wheel
nodejs_wheel.npm(['install', '--prefix', '.tools', 'netlistsvg'])
"
```

### Running the render scripts

Once the venv is set up, use its interpreter (not your system `python3`)
for anything that touches these scripts:

```bash
.venv/bin/python3 scripts/render_waves.py   # images/waves/*.json  -> .svg/.pdf
.venv/bin/python3 scripts/render_blocks.py  # images/blocks/*.py   -> .svg/.pdf
.venv/bin/python3 scripts/render_rtl.py     # images/rtl/*.sv      -> .svg/.pdf
.venv/bin/python3 scripts/render_svgs.py    # images/*.svg         -> .pdf
```

`scripts/render.sh` (and the Makefile targets that wrap it) call these
with plain `python3`, so either put `.venv/bin` first on your `PATH` or
`source .venv/bin/activate` before using `make`/`render.sh`.

### How the PDF pipeline avoids rsvg-convert

`filters/wave-pdf.lua` rewrites every `images/**/*.svg` reference to its
`.pdf` sibling when rendering to LaTeX, so Quarto never has to convert
those SVGs itself. That only works once the four scripts above have been
run at least once (or you've checked out their outputs); on a fresh
clone with no generated `.pdf` files yet, Quarto's LaTeX filter falls back
to calling `rsvg-convert` directly, which is why it is listed under
"Core requirements" even though the project's own pipeline tries to avoid
it.

## Troubleshooting

- **`ModuleNotFoundError` for any of `cairosvg`, `wavedrom`, `schemdraw`,
  `nodejs_wheel`, or `externally-managed-environment` from `pip`**: see
  the two install steps above — system packages for the first group, the
  project venv for the rest.
- **`yowasp-yosys` fails with `Can't open output file ... /tmp/....: No
  such file or directory`**: it runs sandboxed (WASM/wasmtime) and can
  only see paths under the current working directory, not the system
  `/tmp`. `scripts/render_rtl.py` already works around this
  (`tempfile.TemporaryDirectory(dir=ROOT)`); if you see this again in a
  modified script, that is the cause.
- **CI (`.github/workflows/publish.yml`) fails on
  `Could not convert a SVG to a PDF ... rsvg-convert`**: the workflow
  renders the book straight from a fresh checkout, so none of the
  `render_*.py` outputs exist yet and Quarto needs `rsvg-convert` as a
  fallback. The workflow installs `librsvg2-bin` for this; if the error
  comes back, that step was removed or the Ubuntu package name changed.
