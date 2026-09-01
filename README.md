# Course material for DN — Quarto project

A structure that lets you write content **once** and generate both weekly
slide decks and book chapters from it.

## Installation

1. Install Quarto: <https://quarto.org/docs/get-started/>
2. (For PDF export of the book) install TinyTeX: `quarto install tinytex`

## Structure

```
course-material/
├── _quarto.yml               # book project configuration
├── index.qmd                 # book preface/title page
├── chapters/
│   ├── 01-introduction.qmd
│   ├── 02-sv-basics.qmd
│   ├── 03-pipeline-structure.qmd   # sample chapter with demo content
│   ├── 04-pipeline-hazards.qmd
│   ├── 05-memory.qmd
│   └── 06-cocotb-verification.qmd
├── images/                    # diagrams/images, shared between slides and book
├── code/                      # SV/CocoTB examples referenced from .qmd files
└── scripts/
    └── render.sh              # helper script for rendering slides / book
```

## How to write content

Each `.qmd` chapter has `format: revealjs` in its header, used when the
chapter is rendered **individually** as a lecture. When the chapter is
part of the whole book (see `_quarto.yml`), the format defined there
(html/pdf) is used instead.

For content meant to appear **only in lectures** or **only in the book**,
use these blocks:

```markdown
::: {.content-visible when-format="revealjs"}
Slide-only content (e.g. a discussion question for class).
:::

::: {.content-visible unless-format="revealjs"}
Book-only content (e.g. a detailed derivation).
:::
```

See `chapters/03-pipeline-structure.qmd` for a working example.

## Rendering

**One week's lecture (slides):**
```bash
quarto render chapters/03-pipeline-structure.qmd --to revealjs
```
This produces `chapters/03-pipeline-structure.html` — a reveal.js
presentation you can open in a browser or project directly.

**Live preview of slides while editing (auto-reload):**
```bash
quarto preview chapters/03-pipeline-structure.qmd --to revealjs
```

**Whole book (PDF):**
```bash
quarto render --to pdf
```

**Whole book (HTML, e.g. for web publishing):**
```bash
quarto render --to html
```

## Workflow through the semester

1. Before each week, write/extend the corresponding
   `chapters/NN-name.qmd`.
2. Add `content-visible` blocks along the way to separate slide-only from
   book-only content.
3. Store diagrams in `images/` (SVG recommended) and reference them with
   `![caption](../images/name.svg)` — draw once, use everywhere.
4. Put code (SV examples, CocoTB tests) in `code/`, then include it in a
   chapter with `{{< include ../code/example.sv >}}` or as a plain code
   block.
5. Commit to git after each week — you end up with both a history of the
   lectures and the incremental creation of the book material.

## Notes

- `images/pipeline-modules.svg` is currently a placeholder — replace it
  with the actual exported diagram (e.g. the one produced while
  discussing the pipeline's modular structure).
- Placeholder chapters (01, 02, 04, 05, 06) currently only contain a title
  and a short note — feel free to restructure them freely; the important
  part is keeping the `format: revealjs` YAML header if you also want
  those to render as standalone lectures.
