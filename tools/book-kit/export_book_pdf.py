from __future__ import annotations

import argparse
import os
import subprocess
import sys
import shutil
from pathlib import Path

from book_meta import (
    escape_latex,
    load_meta,
    release_display_items,
    resolve_book_dir,
    resolve_source_dir,
)
from build_pandoc_book import build_book


def run(args: list[str], *, cwd: Path | None = None) -> None:
    subprocess.run(args, cwd=cwd, check=True)


def default_fonts(language: str) -> tuple[str, str | None, str]:
    if language.startswith("zh"):
        if sys.platform == "darwin":
            return ("Songti SC", "Songti SC", "Menlo")
        return ("Noto Serif CJK SC", "Noto Serif CJK SC", "Noto Sans Mono")
    if sys.platform == "darwin":
        return ("Palatino", "Songti SC", "Menlo")
    return ("TeX Gyre Pagella", "Noto Serif CJK SC", "Noto Sans Mono")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export a book PDF.")
    parser.add_argument("book_dir", nargs="?", help="Book directory path")
    parser.add_argument("--locale", help="Locale to export, for example en or zh-Hans")
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Remove build caches and previous exported files before rebuilding.",
    )
    parser.add_argument(
        "--clean-generated",
        action="store_true",
        help="Also regenerate PNG diagrams from .puml sources before exporting.",
    )
    parser.add_argument(
        "--draft",
        action="store_true",
        help="Render draft release metadata using today's date and the current git revision.",
    )
    return parser.parse_args(argv)


def remove_path(path: Path) -> None:
    if not path.exists():
        return
    if path.is_dir():
        shutil.rmtree(path)
    else:
        path.unlink()


def clean_book_outputs(book_dir: Path, meta: dict) -> None:
    for rel_path in meta.get("outputs", {}).values():
        remove_path(book_dir / rel_path)

    for rel_dir in ("_book", "_debug", "_texdebug"):
        remove_path(book_dir / rel_dir)


def regenerate_diagrams(book_dir: Path) -> None:
    diagram_dir = book_dir / "diagrams"
    puml_files = sorted(diagram_dir.glob("*.puml"))
    if not puml_files:
        return

    for puml_path in puml_files:
        png_path = puml_path.with_suffix(".png")
        remove_path(png_path)

    try:
        run(["plantuml", "-tpng", *[str(path.name) for path in puml_files]], cwd=diagram_dir)
    except FileNotFoundError as exc:
        raise SystemExit("Missing required command for --clean-generated: plantuml") from exc


def render_title_page(meta: dict, cover_pdf_rel: str | None, release_items: list[str]) -> str:
    pages: list[str] = []

    if cover_pdf_rel:
        pages.append(
            "\n".join(
                [
                    r"\begin{titlepage}",
                    r"\thispagestyle{empty}",
                    r"\newgeometry{margin=0mm}",
                    rf"\noindent\includegraphics[width=\paperwidth,height=\paperheight]{{{cover_pdf_rel}}}",
                    r"\restoregeometry",
                    r"\end{titlepage}",
                    r"\clearpage",
                ]
            )
        )

    title_page_lines = meta.get("title_page_lines", [])
    if title_page_lines or release_items:
        body = [r"\begin{titlepage}", r"\thispagestyle{empty}", r"\newgeometry{top=0mm,bottom=0mm,left=0mm,right=0mm}"]
        if title_page_lines:
            first = True
            for line in title_page_lines:
                line = escape_latex(str(line).strip())
                if first:
                    body.append(r"\vspace*{0.62\textheight}")
                    body.append(r"\begin{center}")
                    body.append(rf"{{\fontsize{{18pt}}{{30pt}}\selectfont\itshape {line}\par}}")
                    first = False
                else:
                    body.append(r"\vspace{8mm}")
                    body.append(rf"{{\fontsize{{16pt}}{{24pt}}\selectfont\color[HTML]{{7B1E1E}} {line}\par}}")
            body.append(r"\end{center}")
        if release_items:
            escaped_items = [escape_latex(item) for item in release_items]
            release_line = r" \textbullet{} ".join(escaped_items)
            body.extend(
                [
                    r"\vspace*{\fill}",
                    r"\begin{center}",
                    rf"{{\fontsize{{10.5pt}}{{15pt}}\selectfont\color[HTML]{{666666}} {release_line}\par}}",
                    r"\end{center}",
                ]
            )
        body.extend(
            [
                r"\restoregeometry",
                r"\end{titlepage}",
                r"\clearpage",
            ]
        )
        pages.append("\n".join(body))

    return "\n\n".join(pages) + ("\n" if pages else "")


def render_header(documentclass: str, cjk_mainfont: str | None) -> str:
    lines = [
            r"\usepackage{graphicx}",
            r"\usepackage{etoolbox}",
            r"\setkeys{Gin}{width=\linewidth,height=0.82\textheight,keepaspectratio}",
            r"% Keep paragraph spacing local instead of loading parskip.",
            r"% Pandoc's parskip path patches \@starttoc and caused TOC entries",
            r"% to disappear around page breaks in ctexbook-based PDFs.",
            r"\setlength{\parindent}{0pt}",
            r"\setlength{\parskip}{6pt plus 2pt minus 1pt}",
            r"% Tune TOC entry spacing and font without external packages.",
            r"\makeatletter",
            r"% Widen the reserved page-number box on the right side of TOC entries.",
            r"% This reduces collisions between long titles, dot leaders and page numbers.",
            r"\renewcommand{\@pnumwidth}{2.8em}",
            r"\renewcommand{\@tocrmarg}{3.8em}",
            r"% Avoid leaving a chapter TOC entry at the bottom of a page.",
            r"% If too little vertical space remains, force the chapter entry",
            r"% onto the next page before LaTeX starts measuring dotted lines.",
            r"\newcommand{\tocchapterneedspace}{%",
            r"  \ifdim\pagegoal<\maxdimen",
            r"    \dimen@=\pagegoal",
            r"    \advance\dimen@ by -\pagetotal",
            r"    \ifdim\dimen@<6\baselineskip",
            r"      \newpage",
            r"    \fi",
            r"  \fi",
            r"}",
            r"\newcommand{\tocsectionneedspace}{%",
            r"  \ifdim\pagegoal<\maxdimen",
            r"    \dimen@=\pagegoal",
            r"    \advance\dimen@ by -\pagetotal",
            r"    \ifdim\dimen@<6\baselineskip",
            r"      \newpage",
            r"    \fi",
            r"  \fi",
            r"}",
            r"% Use \AtBeginDocument so our TOC overrides win over ctexbook's",
            r"% own delayed hooks. Without this, long-title pagination fixes can",
            r"% be silently lost after class initialization.",
            r"\AtBeginDocument{%",
            r"  \renewcommand*\l@chapter[2]{%",
            r"    \ifnum \c@tocdepth >\m@ne",
            r"      \tocchapterneedspace%",
            r"      \addpenalty{-\@highpenalty}%",
            r"      \addvspace{8pt}%",
            r"      \begingroup",
            r"        \parindent \z@ \rightskip \@pnumwidth",
            r"        \parfillskip -\@pnumwidth",
            r"        \leavevmode \normalsize\bfseries #1\nobreak\hfill \nobreak\hb@xt@\@pnumwidth{\hss #2}\par",
            r"        \penalty\@highpenalty",
            r"      \endgroup",
            r"    \fi}%",
            r"  \renewcommand*\l@section[2]{%",
            r"    \ifnum \c@tocdepth >\z@",
            r"      \tocsectionneedspace%",
            r"      \addpenalty\@secpenalty",
            r"      \addvspace{1pt}%",
            r"      \@dottedtocline{1}{1.5em}{3.2em}{\normalsize #1}{\normalsize #2}%",
            r"    \fi}%",
            r"}",
            r"% Isolate TOC from global \parskip (6pt) which inflates entry spacing",
            r"% and causes page-break miscalculation in ctexbook.",
            r"% Keep the TOC pre-hook minimal. The most stable variant in repo",
            r"% debugging keeps page-style handling simple and avoids extra",
            r"% spacing changes that regress different chapter breakpoints.",
            r"\pretocmd{\tableofcontents}{\clearpage\begingroup\let\thispagestyle\@gobble\pagestyle{empty}}{}{}",
            r"\apptocmd{\tableofcontents}{\clearpage\endgroup}{}{}",
            r"\makeatother",
            "",
    ]
    if not documentclass.startswith("ctex") and cjk_mainfont:
        lines.extend(
            [
                r"\usepackage{xeCJK}",
                rf"\setCJKmainfont{{{escape_latex(cjk_mainfont)}}}",
                "",
            ]
        )
    return "\n".join(lines)


def ensure_cover_pdf(book_dir: Path, meta: dict, book_output_dir: Path) -> str | None:
    cover_image = meta.get("cover_image")
    if not cover_image:
        return None

    cover_path = book_dir / cover_image
    if cover_path.suffix.lower() == ".pdf":
        return cover_path.relative_to(book_dir).as_posix()

    if cover_path.suffix.lower() != ".svg":
        raise SystemExit(f"Unsupported cover format: {cover_path}")

    output_cover = book_output_dir / "cover.pdf"
    run(["rsvg-convert", "-f", "pdf", "-o", str(output_cover), str(cover_path)])
    return output_cover.relative_to(book_dir).as_posix()


def main() -> None:
    args = parse_args(sys.argv[1:])
    book_dir = resolve_book_dir(args.book_dir)
    meta = load_meta(book_dir, args.locale)
    source_dir = resolve_source_dir(book_dir, args.locale)
    release_items = release_display_items(book_dir, meta, draft=args.draft)
    pdf_meta = meta.get("pdf", {})
    documentclass = str(pdf_meta.get("documentclass", "ctexbook" if str(meta.get("language", "")).startswith("zh") else "book"))

    if args.clean or args.clean_generated:
        clean_book_outputs(book_dir, meta)
    if args.clean_generated:
        regenerate_diagrams(book_dir)

    book_output_dir = book_dir / "_book"
    output_name = meta["outputs"].get("pdf") or meta["outputs"]["book_pdf"]
    output = book_dir / output_name
    output.parent.mkdir(parents=True, exist_ok=True)
    book_md = book_output_dir / "book.md"
    titlepage_tex = book_output_dir / "titlepage.tex"
    header_tex = book_output_dir / "header.tex"

    book_output_dir.mkdir(parents=True, exist_ok=True)
    book_md.write_text(build_book(book_dir, meta, source_dir), encoding="utf-8")

    cover_pdf_rel = ensure_cover_pdf(book_dir, meta, book_output_dir)
    titlepage_tex.write_text(render_title_page(meta, cover_pdf_rel, release_items), encoding="utf-8")
    language = str(meta.get("language", ""))
    mainfont_default, cjk_mainfont_default, monofont_default = default_fonts(language)
    mainfont = str(pdf_meta.get("mainfont") or os.environ.get("PDF_MAINFONT") or mainfont_default)
    cjk_mainfont = str(pdf_meta.get("cjk_mainfont") or os.environ.get("PDF_CJK_MAINFONT") or (cjk_mainfont_default or "")).strip() or None
    monofont = str(pdf_meta.get("monofont") or os.environ.get("PDF_MONOFONT") or monofont_default)
    header_tex.write_text(render_header(documentclass, cjk_mainfont), encoding="utf-8")

    pandoc_args = [
        "pandoc",
        str(book_md),
        "--from",
        "markdown+raw_tex",
        "--resource-path",
        str(book_dir),
        "--toc",
        "--toc-depth=2",
        "--pdf-engine=xelatex",
        f"--include-before-body={titlepage_tex}",
        f"--include-in-header={header_tex}",
        "-V",
        f"documentclass={documentclass}",
        "-V",
        "classoption=oneside",
        "-V",
        "papersize=a4",
        "-V",
        "fontsize=12pt",
        "-V",
        "indent=true",
        "-V",
        "geometry:inner=28mm",
        "-V",
        "geometry:outer=22mm",
        "-V",
        "geometry:top=24mm",
        "-V",
        "geometry:bottom=26mm",
        "-V",
        "linestretch=1.32",
        "-V",
        "colorlinks=true",
        "-V",
        "linkcolor=Maroon",
        "-V",
        "urlcolor=Maroon",
        "-V",
        "citecolor=Maroon",
        "-V",
        "filecolor=Maroon",
        "-V",
        "toccolor=Maroon",
        "-V",
        f"mainfont={mainfont}",
        "-V",
        f"monofont={monofont}",
        "--highlight-style=tango",
        "-o",
        str(output),
    ]
    if documentclass.startswith("ctex") and cjk_mainfont:
        pandoc_args.extend(["-V", f"CJKmainfont={cjk_mainfont}"])

    run(
        pandoc_args,
        cwd=book_dir,
    )

    print(output)


if __name__ == "__main__":
    main()
