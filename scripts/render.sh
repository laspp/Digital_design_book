#!/usr/bin/env bash
#
# render.sh — helper script to render this Quarto project either as
# per-chapter lecture slides (reveal.js) or as the full book (html/pdf).
#
# Usage:
#   ./scripts/render.sh slides <path-to-chapter.qmd>   Render one chapter as slides
#   ./scripts/render.sh preview <path-to-chapter.qmd>  Live-preview one chapter as slides
#   ./scripts/render.sh book <html|pdf>                Render the whole book
#   ./scripts/render.sh book-preview                   Live-preview the whole book
#   ./scripts/render.sh all                            Render slides for every chapter + the book (html)
#
# Requires: quarto (https://quarto.org/docs/get-started/)
# Wave diagrams (images/waves/*.json) are rendered first: pip install wavedrom cairosvg schemdraw
# and block diagrams (images/blocks/*.py)
# For PDF book output: a LaTeX engine, e.g. `quarto install tinytex`

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
CHAPTERS_DIR="$PROJECT_ROOT/chapters"

usage() {
  echo "Usage:"
  echo "  $0 slides <path-to-chapter.qmd>   Render one chapter as slides"
  echo "  $0 preview <path-to-chapter.qmd>  Live-preview one chapter as slides"
  echo "  $0 book <html|pdf>                Render the whole book"
  echo "  $0 book-preview                   Live-preview the whole book"
  echo "  $0 all                            Render slides for every chapter + the book (html)"
  exit 1
}

check_quarto() {
  if ! command -v quarto &> /dev/null; then
    echo "Error: quarto is not installed or not on PATH." >&2
    echo "See https://quarto.org/docs/get-started/ for installation instructions." >&2
    exit 1
  fi
}

render_waves() {
  python3 "$SCRIPT_DIR/render_waves.py"
  python3 "$SCRIPT_DIR/render_blocks.py"
}

render_slides() {
  local chapter="$1"
  if [[ ! -f "$chapter" ]]; then
    echo "Error: chapter file not found: $chapter" >&2
    exit 1
  fi
  echo "Rendering slides: $chapter"
  quarto render "$chapter" --to revealjs --profile slides
}

preview_slides() {
  local chapter="$1"
  if [[ ! -f "$chapter" ]]; then
    echo "Error: chapter file not found: $chapter" >&2
    exit 1
  fi
  echo "Previewing slides: $chapter"
  quarto preview "$chapter" --to revealjs --profile slides
}

render_book() {
  local fmt="$1"
  case "$fmt" in
    html|pdf)
      echo "Rendering book (${fmt}) from: $PROJECT_ROOT"
      (cd "$PROJECT_ROOT" && quarto render --to "$fmt")
      ;;
    *)
      echo "Error: unknown book format '$fmt' (expected 'html' or 'pdf')" >&2
      usage
      ;;
  esac
}

preview_book() {
  echo "Previewing book from: $PROJECT_ROOT"
  (cd "$PROJECT_ROOT" && quarto preview)
}

render_all() {
  echo "Rendering slides for every chapter in $CHAPTERS_DIR ..."
  for chapter in "$CHAPTERS_DIR"/*.qmd; do
    render_slides "$chapter"
  done
  echo ""
  render_book "html"
}

main() {
  check_quarto

  if [[ $# -lt 1 ]]; then
    usage
  fi

  render_waves

  case "$1" in
    slides)
      [[ $# -eq 2 ]] || usage
      render_slides "$2"
      ;;
    preview)
      [[ $# -eq 2 ]] || usage
      preview_slides "$2"
      ;;
    book)
      [[ $# -eq 2 ]] || usage
      render_book "$2"
      ;;
    book-preview)
      [[ $# -eq 1 ]] || usage
      preview_book
      ;;
    all)
      render_all
      ;;
    *)
      usage
      ;;
  esac
}

main "$@"
