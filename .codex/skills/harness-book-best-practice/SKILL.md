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

- Store the stable public-facing field `release_date` in `book.json`.
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

## Diagrams (PUML)

`.puml` is the source of truth in `diagrams/`. The committed `.png` next to it is the artifact embedded in the book. Regenerate `.png` with `python3 tools/book-kit/export_pdf.py <book> --clean-generated` (this calls `plantuml -tpng`); never hand-edit a `.png`.

### Pick The Diagram Type By What You Want To Show

These books are about runtime behavior, so default to diagrams that surface behavior, not static structure:

- State diagram (`state`, `[*]`, `<<choice>>`) — for lifecycles, "where state lives," and stateful loops (query loop, thread, budget thresholds).
- Activity diagram (`start`/`stop`, `if/then/else`, `fork`/`fork again`) — for decision ladders and governance flows (recovery paths, compact rebuild, tool batch ordering).
- Sequence diagram (`actor`, `participant`, `->`) — for temporal interactions between distinct actors (coordinator/worker, user/runtime/worker).
- Component / box-and-arrow — only when structure itself is the point. Do not use it as a default layout for behavioral content.

If a diagram does not show a loop, a decision branch, a transition, or a temporal exchange, reconsider whether it is earning its page.

### Comparison Diagrams (book2)

When contrasting Claude Code vs Codex on a single dimension:

- Use `top to bottom direction` and stack the two sides vertically. Do not lay them out side-by-side with `left to right direction`; that invites parallel component lists and makes the contrast hard to read at book width.
- Wrap each side in a bold composite state: `state "<b>Claude Code - assemble then loop</b>" as CC { ... }` and `state "<b>Codex - structure then turn</b>" as CX { ... }`.
- Separate the two composites with a `[hidden]` edge: `CC -[hidden]-> CX`.
- Contrast exactly one behavioral dimension per diagram (control plane, continuity, governance, ...). Use a closing note on each side to name the design lever, not to restate the boxes.

### Titles And Notes

- Title: name the behavior, not the chapter. Use the form `Topic - Behavior Statement`, e.g. `Query Loop Core - One Iteration Of The While Loop`, `Recovery Decision Paths - Cheapest Fix First`, `Tool Batch Ordering - Concurrency Without Context Reordering`. Avoid `Chapter N · Topic` phrasing.
- Notes should explain the invariant, the design lever, or the principle a designer can copy ("concurrency speeds up I/O; contextual cause-and-effect is always replayed in original block order"). Notes that just restate the adjacent boxes are noise.

### Rendering For Book Pages

Target render dimensions of roughly 700-1500 px on each axis so the diagram fits a printed page without forced scaling.

Standard skinparam baseline (default Harness palette):

```
skinparam backgroundColor #FEFEFE      # transparent for book2 comparisons
skinparam shadowing false
skinparam dpi 120                       # 120 for comparison diagrams, 130 for single-book
skinparam defaultFontName Georgia
skinparam defaultFontSize 14
skinparam TitleFontSize 19
skinparam TitleFontColor #161616
skinparam NoteFontSize 12
skinparam ArrowFontSize 12
skinparam ArrowColor #5E5A53
```

Then add only the semantic blocks the diagram actually uses (`skinparam state { ... }`, `skinparam activity { ... }`, `skinparam sequence { ... }`, `skinparam note { ... }`) using the palette below.

Default Harness palette (book1 and Claude-Code-side of book2):

- shape background `#F2E9D9`, border `#1D1D1D`, font `#161616`, arrow `#5E5A53`, start `#8C2721`, end `#161616`
- note background `#F5EBDD`, border `#8C2721`, font `#7B1E1E`
- accent fills for distinguishing roles inside one diagram: `#E8DDD0` (input / source), `#EFE6D8` (runtime / loop), `#F5EBDD` (decision / warning / error)

Codex palette (Codex-side of book2 only, when contrast with the Harness palette is the point):

- shape background `#F8FAFC`, border `#334155`, font `#0F172A`, arrow `#475569`
- note background `#FFF7ED`, border `#C2410C`, font `#7C2D12`

Do not reintroduce these settings, which were removed from the redesigned diagrams because they fight auto-layout or print badly:

- `linetype ortho` and `packageStyle rectangle`
- explicit `ranksep` / `nodesep` overrides
- per-shape `RectangleFontSize`, `PackageFontSize`, etc. (use `defaultFontSize` plus the semantic blocks above)
- DPI above 130 (renders that overflow the page)

### Validation After Diagram Changes

When changing a `.puml`:

1. Regenerate with `--clean-generated` so the embedded `.png` matches the source.
2. Eyeball the rendered `.png`: does it fit roughly 700-1500 px on each axis, and does the contrast read at book width?
3. Rebuild the affected book PDF and confirm the diagram is not clipped at the page boundary.
4. For book2 comparison diagrams, also confirm the two composite states stack vertically and the `[hidden]` separator is keeping them apart.

## Output Naming

Keep final exports per book under `exported/` with stable names:

- `book1-claude-code/exported/book1-claude-code.pdf`
- `book1-claude-code/exported/book1-claude-code-print.html`
- `book2-comparing/exported/book2-comparing.pdf`
- `book2-comparing/exported/book2-comparing-print.html`

If a new output is added, put it in `book.json` under `outputs`.
Do not encode the primary release version only in the output filename. The canonical source of version truth should remain `book.json`.

## PDF Link Colors

All hyperlink colors in the PDF are set to **Maroon** for a uniform appearance. This is configured via Pandoc `-V` variables in `export_book_pdf.py`:

- `linkcolor=Maroon` (internal cross-references)
- `urlcolor=Maroon` (external URLs)
- `citecolor=Maroon` (citations)
- `filecolor=Maroon` (file links)
- `toccolor=Maroon` (TOC entries)

When adding new link-related Pandoc variables, keep the Maroon convention. Do not leave individual color variables at their Pandoc defaults (Blue, Green, Cyan) as this produces a distracting multi-color link style.

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
- The current robust fix is to guard chapter TOC entries with a page-remaining-space check before rendering the chapter line. In `tools/book-kit/export_book_pdf.py`, `\tocchapterneedspace` measures `\pagegoal - \pagetotal` and forces a page break when the remaining height is too small. This prevents chapter headings from landing at the bottom of a TOC page and avoids losing the following section entries around the break.
- Apply the same page-remaining-space protection to TOC section entries when single section rows disappear near a break. In this repo, section-level protection was needed because `book1` could still lose `3.4` even after chapter-level protection was added.

## TOC Failure Modes

- A TOC entry can exist in `.toc` but still disappear from the rendered PDF near a page break. Treat this as a LaTeX pagination problem, not a Pandoc generation problem.
- Fixing one break point is not enough. A change that restores `第 4 章` in one book can still regress `第 5 章` or a mid-chapter section block in the other book.
- Long titles and titles with extra punctuation are more fragile near page boundaries. If a single heading keeps disappearing after structural fixes, a small title shortening is acceptable.

## TOC Validation Protocol

- Always validate TOC fixes against both books, not only the book that first exposed the issue.
- Use `pdftotext -f 3 -l 6 -layout ...` or an equivalent page-scoped extraction to inspect only the TOC pages. Whole-document text extraction can hide TOC regressions because the same heading still exists later in body text.
- A TOC fix is not complete unless these breakpoints are all checked:
- `book1-claude-code`: `第 3 章` section block around `3.3` to `3.7`
- `book1-claude-code`: `第 4 章` to `第 5 章`
- `book2-comparing`: `第 3 章` to `第 4 章`
- `book2-comparing`: `第 4 章` to `第 5 章`
- If any one breakpoint regresses, keep iterating. Do not record the attempt as a stable solution.

## Preferred Fix Order

- First inspect the generated `.toc` file. If the missing headings are present there, debug LaTeX pagination and TOC macros rather than markdown generation.
- Prefer shared fixes in `tools/book-kit/export_book_pdf.py` over per-book hacks.
- Prefer page-break control around TOC entries over line-spacing or font-size tweaks.
- Only after the shared TOC logic is stable should you shorten an individual heading, and only when one specific title remains an outlier.

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
- Current reference material includes:
  - `references/harness-engineering-book-proposal.md` (book1 proposal)
  - `references/comparative-book-proposal.md` (book2 proposal)

## Editing Strategy

- Prefer updating shared code in `tools/book-kit/` for behavior changes.
- Prefer updating `book.json` for per-book output naming.
- Prefer updating `book.json` for per-book release metadata such as `release_date`.
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
- If diagrams changed and `.puml` is the source, use `--clean-generated`, then run the diagram validation steps in the **Diagrams (PUML)** section

## Decision Heuristics

- If the question is "source asset or output artifact?", default to `assets/` for source and `exported/` for output.
- If the question is "per-book patch or shared tool change?", default to shared tool change.
- If the question is "quick layout tweak or root-cause fix?", default to root-cause analysis first, especially for TOC and PDF issues.
