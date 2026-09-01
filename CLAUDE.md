# CLAUDE.md

This file gives Claude Code the context it needs to work effectively in this
repository.

## Project overview

This is a Quarto project for the university course **DN** (redesigned around
RISC-V SoC design). It follows a "single source, multiple outputs" approach:
each week's teaching content is written **once**, in a single `.qmd` file,
and is rendered into two different outputs:

1. **Lecture slides** (reveal.js) — used in class.
2. **A book chapter** (HTML/PDF) — compiled together with all other chapters
   into a full textbook for the course.

Content that should only appear in one of the two outputs (e.g. a discussion
question for class, or a long derivation for the book) is wrapped in
Quarto `content-visible` divs — see "Content conventions" below.

## Directory structure

```
.
├── _quarto.yml              # book project config (html + pdf output)
├── index.qmd                # book preface/title page
├── chapters/                # one .qmd file per week/chapter
│   ├── 01-introduction.qmd
│   ├── 02-sv-basics.qmd
│   ├── 03-pipeline-structure.qmd
│   ├── 04-pipeline-hazards.qmd
│   ├── 05-memory.qmd
│   └── 06-cocotb-verification.qmd
├── images/                  # diagrams/images, shared between slides and book
├── code/                    # SystemVerilog / CocoTB code examples referenced from .qmd files
└── scripts/
    └── render.sh            # helper script for rendering slides / book
```

Chapter filenames are prefixed with a two-digit week number
(`NN-short-name.qmd`) so their order in `chapters/` matches the order they
appear in `_quarto.yml`'s `book.chapters` list. When adding a new week,
follow the same numbering convention and add the file to `_quarto.yml`.

## Content conventions

Every chapter file starts with YAML front matter that includes a
`revealjs` format block. This is what lets the file be rendered as
standalone slides:

```yaml
---
title: "Chapter title"
format:
  revealjs:
    slide-level: 2
---
```

When the file is rendered as part of the whole book (via `_quarto.yml`),
the book's `html`/`pdf` format settings are used instead.

To show content only in one output, use:

```markdown
::: {.content-visible when-format="revealjs"}
Slide-only content (e.g. a discussion question for the class).
:::

::: {.content-visible unless-format="revealjs"}
Book-only content (e.g. a detailed derivation or extended example).
:::
```

Content **outside** these divs appears in both outputs, so it should be
written to make sense in either context.

## Writing style

Confirmed as the target style for this project (based on
`chapters/03-pipeline-structure.qmd`):

- **Slides** (`when-format="revealjs"` content and top-level bullets): terse,
  telegraphic bullets — no full sentences, one idea per line.
- **Book prose** (`unless-format="revealjs"` content and shared prose):
  first-person plural ("we implement...", "we treat memory as..."), written
  as an engineer teaching engineers rather than a neutral/impersonal
  textbook voice.
- Explain the **why** behind a design choice, not just the what — often both
  a pedagogical reason (what the example is meant to teach) and a practical
  one (why it's done that way in real designs). See the pipeline-register
  justification in `03-pipeline-structure.qmd` for the pattern to match.
- Introduce terminology once, then reuse it consistently (e.g. DFF, jigsaw
  testing methodology) rather than re-explaining or varying the term.

## Working conventions for Claude Code

- Keep prose content in the language the user is writing in for that
  chapter, but keep `CLAUDE.md`, scripts, and code comments in English
  unless told otherwise.
- Diagrams belong in `images/` as SVG when possible (matches what has been
  used elsewhere in this project) and are referenced with a relative
  Markdown image link: `![caption](../images/name.svg)`.
- Code examples belong in `code/` and are pulled into chapters either as a
  fenced code block (for short inline snippets) or via
  `{{< include ../code/file.sv >}}` (for larger, reusable examples that
  should stay in sync with an actual source file).
- Don't remove or rename the `format: revealjs` block from a chapter's front
  matter — doing so breaks that chapter's ability to render standalone as
  slides.
- When adding a new chapter, mirror the structure of
  `chapters/03-pipeline-structure.qmd`, which is the reference example for
  how `content-visible` blocks, images, and code blocks are meant to be
  used together.

## Common commands

Render a single chapter as slides:
```bash
quarto render chapters/03-pipeline-structure.qmd --to revealjs
```

Live-preview a chapter's slides while editing:
```bash
quarto preview chapters/03-pipeline-structure.qmd --to revealjs
```

Render the whole book:
```bash
quarto render --to html
quarto render --to pdf   # requires a LaTeX engine, e.g. `quarto install tinytex`
```

Or use the helper script (see `scripts/render.sh`):
```bash
./scripts/render.sh slides chapters/03-pipeline-structure.qmd
./scripts/render.sh book pdf
./scripts/render.sh book html
```

## Non-goals

This repository does not contain the RTL/CocoTB codebase for the RISC-V
CPU itself (`cpu_top`, pipeline stages, etc.) — that lives in a separate
project. `code/` here only holds small illustrative snippets meant for
teaching, not the full verified implementation.
