---
name: harness-book-best-practice
description: >
  Best practices for working on the Harness books repo. Use this skill when editing, restructuring, building,
  or exporting the books under `book1-claude-code/` and `book2-comparing/`, especially for Honkit, print HTML,
  Pandoc/XeLaTeX PDF export, build cleanup, TOC issues, naming conventions, and keeping source assets separate
  from generated outputs.
---

# Harness Book Best Practice

Use this skill for changes inside this repository's book system.

## Scope

This repo has two books:

- `book1-claude-code/`
- `book2-comparing/`

Shared build logic lives in:

- `tools/book-kit/book_meta.py`
- `tools/book-kit/build_pandoc_book.py`
- `tools/book-kit/build_print_html.py`
- `tools/book-kit/export_book_pdf.py`
- `tools/book-kit/export_pdf.py`

Prefer changing shared behavior in `tools/book-kit/` rather than reintroducing per-book one-off scripts.

## Release Metadata

Treat book release metadata as structured config, not manuscript text.

- Store the stable public-facing field `release_date` in `book.meta.json`.
- Prefer deriving `revision` automatically from git in shared tooling instead of maintaining a manual version string.
- Render release metadata through shared export templates, not by manually inserting it into `README.md`, chapter files, or cover artwork.
- Preferred placement is the title page / colophon area for PDF and the cover section for print HTML.
- Do not default to volatile build timestamps in final deliverables. Prefer a stable release date so regenerated exports remain reproducible.
- Use `--draft` for internal draft exports when you explicitly want today's date plus git revision in the rendered output.

## Directory Rules

- `assets/` is for source assets only: cover SVG/PDF, hand-maintained source files, reusable static inputs.
- `diagrams/` is for diagram sources and committed generated images used by the books. In this repo, `.puml` is the source of truth and `.png` is the embedded artifact.
- `exported/` is for final deliverables only: `*.pdf`, `*-print.html`.
- `_book/` is a build/cache directory and may be deleted.
- `_debug/` and `_texdebug/` are disposable debug directories and may be deleted.

Do not move exported PDFs into `assets/`. That mixes source inputs with build outputs and makes cleanup/error analysis harder.

## Output Naming

Keep final exports per book under `exported/` with stable names:

- `book1-claude-code/exported/book1-claude-code.pdf`
- `book1-claude-code/exported/book1-claude-code-print.html`
- `book2-comparing/exported/book2-comparing.pdf`
- `book2-comparing/exported/book2-comparing-print.html`

If a new output is added, put it in `book.meta.json` under `outputs`.
Do not encode the primary release version only in the output filename. The canonical source of version truth should remain `book.meta.json`.

## Build Policy

Current PDF export is intentionally:

- `Pandoc`
- `XeLaTeX`
- `ctexbook`

Do not switch PDF generation to Playwright unless the user explicitly asks to change the production path.

Use:

```bash
python3 tools/book-kit/export_pdf.py book1-claude-code
python3 tools/book-kit/export_pdf.py book2-comparing
```

Available cleanup options:

```bash
python3 tools/book-kit/export_pdf.py book1-claude-code --clean
python3 tools/book-kit/export_pdf.py book2-comparing --clean-generated
```

Meaning:

- `--clean`: remove `_book/`, `_debug/`, `_texdebug/`, and old exported outputs before rebuilding
- `--clean-generated`: includes `--clean` behavior and also regenerates `diagrams/*.png` from `diagrams/*.puml`

Never let cleanup delete `assets/`.

## TOC And PDF Pitfalls

Important: PDF TOC layout is owned by LaTeX, not by Pandoc.

Known repo-specific pitfalls:

- Do not reintroduce Pandoc's default `parskip` path for PDF export in this repo.
- In this repo's `ctexbook` setup, `parskip` patched `\@starttoc` and caused TOC entries to disappear around page breaks.
- Keep paragraph spacing local in the LaTeX header instead.
- If TOC overrides are implemented via `\renewcommand{\l@chapter}` / `\renewcommand{\l@section}`, place them inside `\AtBeginDocument`. In this repo, `ctexbook` applies delayed hooks that can silently override preamble-time TOC customizations.
- Do NOT combine `\setstretch{1.0}` with `\setlength{\parskip}{0pt}` in the TOC `\pretocmd` group. This specific pair triggers a TeX page-break bug where TOC entries near the first page break silently disappear. `\setstretch{1.08}` or higher does not trigger it — the issue is specific to exactly `1.0` which creates zero-tolerance vertical spacing. The safe approach is to omit `\setstretch` entirely in the TOC group and only use `\parskip=0pt`.
- The currently stable shared fix is narrower: keep TOC macro overrides in `\AtBeginDocument`, and keep the `\tableofcontents` pre-hook minimal. In practice, `\let\thispagestyle\@gobble\pagestyle{empty}` has been more stable than adding extra TOC line-spacing tweaks.
- Do not treat `\setstretch{1.08}` as a universal TOC fix. It fixed one page break in `book2-comparing`, but regressed later chapter breaks in both books by causing subsequent chapter titles to disappear even though the entries were present in `.toc`.

When debugging TOC issues:

1. Confirm visually with rendered TOC pages, not only `pdftotext`.
2. Check whether entries are missing from rendering or missing from `.aux`/`.toc` generation.
3. Avoid "fixes" that only shrink fonts unless the root cause is confirmed.

If TOC entries disappear near page breaks, inspect `tools/book-kit/export_book_pdf.py` first.

## Markdown Content Rules

- Book-facing text must not leak repo implementation details like `book1-claude-code/` or `book2-comparing/` unless the chapter is explicitly about repo structure.
- Prefer public-facing wording like "第一本书" / "这本比较书" when discussing the series from inside the books.
- Use `Harness` consistently as the preferred term.
- Fix broken markdown links that produce bad book/PDF navigation; preserve external links, strip or rewrite local file links when needed for final merged output.
- Keep build, export, GitBook/Honkit, GitHub Pages, PDF pipeline, and local publishing instructions out of book-facing markdown. Put those details in repo docs or this skill instead.
- Avoid editorial-process language inside the books, such as "后续扩写", "继续修图", "换版式", "导出印刷稿", naming-convention notes for source assets, or other maintenance instructions for the manuscript itself.

## Editorial References

- Writing proposals, outlines, positioning notes, and other non-reader-facing editorial documents should live under `references/` in this skill, not inside `book1-claude-code/` or `book2-comparing/`.
- Use `references/` for background material that helps future editing decisions but should not be treated as buildable manuscript content.
- Current reference material includes `references/harness-engineering-book-proposal.md`.

## Editing Strategy

- Prefer updating shared code in `tools/book-kit/` for behavior changes.
- Prefer updating `book.meta.json` for per-book output naming.
- Prefer updating `book.meta.json` for per-book release metadata such as `release_date`.
- Keep `SUMMARY.md` aligned with the actual reading structure when the book uses Honkit navigation.
- Avoid adding extra build scripts under individual books unless there is a clear book-specific requirement that cannot live in shared tooling.

## Validation Checklist

After substantial book or pipeline changes, run enough of this checklist to cover the touched area:

- Export the affected book PDF
- If HTML-print behavior changed, regenerate the `*-print.html`
- If release metadata changed, confirm the version/date block appears in both print HTML and the exported PDF title page
- Confirm files land in `exported/`
- Check TOC pages visually if headings, spacing, or chapter titles changed
- Confirm no local `.md` links leak into the merged PDF text
- If diagrams changed and `.puml` is the source, use `--clean-generated`

## Decision Heuristics

- If the question is "source asset or output artifact?", default to `assets/` for source and `exported/` for output.
- If the question is "per-book patch or shared tool change?", default to shared tool change.
- If the question is "quick layout tweak or root-cause fix?", default to root-cause analysis first, especially for TOC and PDF issues.
