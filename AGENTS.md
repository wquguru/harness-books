# Repository Guidelines

## Project Structure & Module Organization

This repository contains two book projects: `book1-claude-code/` and `book2-comparing/`. Each book keeps its manuscript in root-level Markdown files such as `README.md`, `SUMMARY.md`, `preface.md`, and `chapter-*.md`.

Use these directories consistently:

- `assets/`: source assets only, such as `cover-wxb.svg`
- `diagrams/`: diagram sources (`.puml`) plus committed rendered images (`.png`)
- `styles/`: Honkit and print styling
- `exported/`: final deliverables such as `*.pdf` and `*-print.html`
- `tools/book-kit/`: shared Python build/export tooling for both books

Do not treat `_book/`, `_debug/`, or `_texdebug/` as source; they are generated and disposable.

## Build, Test, and Development Commands

Build the Honkit site for a book:

```bash
cd book1-claude-code && npx --yes honkit build . _book
cd book2-comparing && npx --yes honkit build . _book
```

Generate print HTML after `_book/` exists:

```bash
python3 tools/book-kit/build_print_html.py book1-claude-code
python3 tools/book-kit/build_print_html.py book2-comparing
```

Export the production PDF:

```bash
python3 tools/book-kit/export_pdf.py book1-claude-code
python3 tools/book-kit/export_pdf.py book2-comparing
```

Use `--clean` or `--clean-generated` when rebuild hygiene matters. Prefer shared scripts in `tools/book-kit/` over adding one-off per-book build logic.

## Book Metadata

Treat release metadata as first-class book configuration in each `book.meta.json`.

- Put the stable public field `release_date` in `book.meta.json`
- Let shared tooling derive `revision` from git automatically unless a manual `revision` override is truly needed
- Render release metadata through shared templates in `tools/book-kit/`, not by hardcoding values in Markdown chapters
- Prefer showing release metadata on the PDF/print title page or colophon area, not in running headers or chapter titles
- Prefer a stable release date over an auto-generated build timestamp so formal exports stay reproducible and diffs stay clean
- Use `--draft` only for internal draft exports that should show the current date plus git revision automatically

## Coding Style & Naming Conventions

Write Markdown with short sections, stable heading hierarchy, and descriptive filenames such as `chapter-06-errors-and-recovery.md`. Keep `SUMMARY.md` aligned with the actual reading order. Diagram sources should stay paired as `diagrams/name.puml` and `diagrams/name.png`.

For Python tooling, follow existing style: 4-space indentation, small functions, and standard-library-first scripts.

## Testing Guidelines

There is no automated test suite in this repo today. Validation is build-based:

- rebuild the affected book
- confirm outputs land under the book’s `exported/` directory
- visually inspect TOC, pagination, links, and updated diagrams

When changing shared export code, validate at least one full PDF export end to end.
When changing release metadata rendering, also confirm the generated `*-print.html` and inspect the title page in the exported PDF.

## Commit & Pull Request Guidelines

The visible history is minimal (`Initial commit`), so use short imperative commit messages, for example `Add AGENTS guide` or `Fix book2 PDF export path`. Keep commits scoped to one logical change.

PRs should state which book or shared tool changed, list validation commands run, and include screenshots only when layout, cover art, or PDF pagination changed.
