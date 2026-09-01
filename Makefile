# Makefile — convenience wrapper around scripts/render.sh.
#
# This does not duplicate quarto invocation logic (profiles, formats, etc.)
# — scripts/render.sh is the single place that knows how to call quarto.
# This file only adds one target per chapter (auto-discovered from
# chapters/*.qmd, so a new chapter needs no edit here) plus the book and
# housekeeping targets.
#
# Examples:
#   make slides-02-sv-basics       Render chapter 2's slides
#   make slides-02                 Same, via the short numeric alias
#   make preview-03                Live-preview chapter 3's slides
#   make book-pdf                  Render the whole book (PDF)
#   make all                       Slides for every chapter + book (HTML)

SHELL := bash
.DEFAULT_GOAL := help

CHAPTERS_DIR := chapters
RENDER := ./scripts/render.sh

CHAPTER_FILES := $(wildcard $(CHAPTERS_DIR)/*.qmd)
CHAPTER_NAMES := $(basename $(notdir $(CHAPTER_FILES)))
CHAPTER_NUMS  := $(sort $(foreach c,$(CHAPTER_NAMES),$(word 1,$(subst -, ,$(c)))))

SLIDES_TARGETS  := $(addprefix slides-,$(CHAPTER_NAMES))
PREVIEW_TARGETS := $(addprefix preview-,$(CHAPTER_NAMES))
SLIDES_ALIASES  := $(addprefix slides-,$(CHAPTER_NUMS))
PREVIEW_ALIASES := $(addprefix preview-,$(CHAPTER_NUMS))

.PHONY: help all book-html book-pdf clean \
        $(SLIDES_TARGETS) $(PREVIEW_TARGETS) $(SLIDES_ALIASES) $(PREVIEW_ALIASES)

help:
	@echo "Chapter targets (slides):"
	@$(foreach c,$(CHAPTER_NAMES),echo "  make slides-$(c)   (or: make slides-$(word 1,$(subst -, ,$(c))))";)
	@echo ""
	@echo "Same names with 'preview-' instead of 'slides-' live-preview a chapter."
	@echo ""
	@echo "Other targets:"
	@echo "  make book-html    Render the whole book (HTML)"
	@echo "  make book-pdf     Render the whole book (PDF)"
	@echo "  make all          Render slides for every chapter + the book (HTML)"
	@echo "  make clean        Remove rendered output"

# One real rule per chapter file: `make slides-<full-chapter-name>`.
$(SLIDES_TARGETS): slides-%: $(CHAPTERS_DIR)/%.qmd
	$(RENDER) slides $<

$(PREVIEW_TARGETS): preview-%: $(CHAPTERS_DIR)/%.qmd
	$(RENDER) preview $<

# Short numeric aliases: `make slides-02` -> `make slides-02-sv-basics`.
define chapter_alias
slides-$(word 1,$(subst -, ,$(1))): slides-$(1)
preview-$(word 1,$(subst -, ,$(1))): preview-$(1)
endef
$(foreach c,$(CHAPTER_NAMES),$(eval $(call chapter_alias,$(c))))

book-html:
	$(RENDER) book html

book-pdf:
	$(RENDER) book pdf

all:
	$(RENDER) all

clean:
	rm -rf _book .quarto
	rm -rf $(CHAPTERS_DIR)/*.html $(CHAPTERS_DIR)/*_files
