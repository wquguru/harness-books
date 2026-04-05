from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

from book_meta import (
    chapter_paths,
    load_meta,
    release_display_items,
    resolve_book_dir,
    resolve_build_dir,
    resolve_source_dir,
)


SECTION_RE = re.compile(
    r'<section class="normal markdown-section">(.*?)</section>',
    re.DOTALL,
)
PAGE_RE = re.compile(r"gitbook\.page\.hasChanged\((\{.*?\})\);", re.DOTALL)
HTML_ATTR_RE = re.compile(r'(?P<attr>href|src)="(?P<url>[^"]+)"')


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build print HTML for a book.")
    parser.add_argument("book_dir", nargs="?", help="Book directory path")
    parser.add_argument("--locale", help="Locale to build, for example en or zh-Hans")
    parser.add_argument(
        "--draft",
        action="store_true",
        help="Render draft release metadata using today's date and the current git revision.",
    )
    return parser.parse_args(argv)


def load_page(book_output_dir: Path, md_path: str) -> tuple[str, str]:
    html_name = "index.html" if md_path == "README.md" else md_path.replace(".md", ".html")
    page_path = book_output_dir / html_name
    content = page_path.read_text(encoding="utf-8")

    section_match = SECTION_RE.search(content)
    if not section_match:
        raise SystemExit(f"Cannot find markdown section in {page_path}")

    meta_match = PAGE_RE.search(content)
    if not meta_match:
        raise SystemExit(f"Cannot find page metadata in {page_path}")

    page_meta = json.loads(meta_match.group(1))
    title = page_meta["page"]["title"]
    return title, section_match.group(1).strip()


def html_name_for_md_path(md_path: str) -> str:
    return "index.html" if md_path == "README.md" else md_path.replace(".md", ".html")


def anchor_for_md_path(md_path: str, index: int) -> str:
    stem = Path(md_path).stem
    if md_path == "README.md":
        stem = "readme"
    return f"article-{index + 1}-{stem}"


def is_external_url(url: str) -> bool:
    return url.startswith(("http://", "https://", "mailto:", "tel:", "data:", "javascript:", "#"))


def rebase_local_url(url: str, *, book_dir: Path, output_parent: Path) -> str:
    parts = urlsplit(url)
    if not parts.path:
        return url
    rebased = os.path.relpath(book_dir / parts.path, output_parent)
    return urlunsplit(("", "", rebased, parts.query, parts.fragment))


def rewrite_section_html(
    section_html: str,
    *,
    md_path: str,
    anchor_map: dict[str, str],
    book_dir: Path,
    output_parent: Path,
    cover_image: str | None = None,
    cover_alt: str | None = None,
) -> str:
    if cover_image and cover_alt:
        section_html = re.sub(
            rf'(<img\b[^>]*\balt="{re.escape(html.escape(cover_alt))}"[^>]*\bsrc=")([^"]+)(")',
            rf"\1{cover_image}\3",
            section_html,
            count=1,
        )

    def replace_attr(match: re.Match[str]) -> str:
        attr = match.group("attr")
        url = match.group("url")
        if is_external_url(url):
            return match.group(0)

        parts = urlsplit(url)
        target = parts.path
        if attr == "href" and target.endswith(".html"):
            anchor = anchor_map.get(target)
            if anchor:
                fragment = f"#{anchor}"
                if parts.fragment:
                    fragment = f"{fragment}-{parts.fragment}"
                return f'{attr}="{fragment}"'

        rebased = rebase_local_url(url, book_dir=book_dir, output_parent=output_parent)
        return f'{attr}="{html.escape(rebased, quote=True)}"'

    return HTML_ATTR_RE.sub(replace_attr, section_html)


def default_print_font_stack(language: str) -> str:
    if language.startswith("zh"):
        return '"Noto Serif SC", "Songti SC", "STSong", serif'
    return '"Iowan Old Style", "Palatino Linotype", "Book Antiqua", "Georgia", serif'


def build_html(book_dir: Path, meta: dict, source_dir: Path, book_output_dir: Path, *, draft: bool = False) -> str:
    articles: list[str] = []
    release_bits = release_display_items(book_dir, meta, draft=draft)
    output_rel = Path(meta["outputs"]["print_html"])
    output_parent = (book_dir / output_rel).parent
    gitbook_style_path = os.path.relpath(book_output_dir / "gitbook" / "style.css", output_parent)
    website_style_path = os.path.relpath(book_dir / "styles" / "website.css", output_parent)
    pdf_style_path = os.path.relpath(book_dir / "styles" / "pdf.css", output_parent)
    font_stack = meta.get("print_font_stack") or default_print_font_stack(str(meta.get("language", "")))
    chapter_list = chapter_paths(source_dir)
    anchor_map = {
        html_name_for_md_path(md_path): anchor_for_md_path(md_path, index)
        for index, md_path in enumerate(chapter_list)
    }

    for index, md_path in enumerate(chapter_list):
        title, body = load_page(book_output_dir, md_path)
        body = rewrite_section_html(
            body,
            md_path=md_path,
            anchor_map=anchor_map,
            book_dir=book_dir,
            output_parent=output_parent,
            cover_image=str(meta.get("cover_image", "")).strip() or None if index == 0 else None,
            cover_alt=str(meta.get("cover_alt", "")).strip() or None if index == 0 else None,
        )
        chapter_class = "book-cover" if index == 0 else "book-chapter"
        heading = "" if index == 0 else f"<header><h1>{html.escape(title)}</h1></header>"
        edition = ""
        if index == 0 and release_bits:
            edition = (
                '<div class="book-edition">'
                f"{html.escape(' · '.join(release_bits))}"
                "</div>"
            )
        articles.append(
            "\n".join(
                [
                    f'<article id="{anchor_for_md_path(md_path, index)}" class="{chapter_class}" data-source="{html.escape(md_path)}">',
                    heading,
                    body,
                    edition,
                    "</article>",
                ]
            )
        )

    return f"""<!DOCTYPE html>
<html lang="{html.escape(meta.get("language", "zh-Hans"))}">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{html.escape(meta["title"])}</title>
  <link rel="stylesheet" href="{html.escape(gitbook_style_path)}" />
  <link rel="stylesheet" href="{html.escape(website_style_path)}" />
  <link rel="stylesheet" href="{html.escape(pdf_style_path)}" />
  <style>
    :root {{
      --page-width: 840px;
      --ink: #161616;
      --muted: #5a5a5a;
      --rule: #d6d6d6;
      --accent: #7b1e1e;
      --paper: #fdfcf8;
    }}

    * {{
      box-sizing: border-box;
    }}

    html, body {{
      margin: 0;
      padding: 0;
      background: var(--paper);
      color: var(--ink);
    }}

    body {{
      font-family: {font_stack};
      line-height: 1.75;
    }}

    .print-book {{
      width: min(100%, var(--page-width));
      margin: 0 auto;
      padding: 0;
    }}

    .book-cover,
    .book-chapter {{
      padding: 20mm 0 16mm;
      page-break-after: always;
      break-after: page;
    }}

    .book-cover {{
      min-height: 250mm;
      display: flex;
      flex-direction: column;
      justify-content: center;
    }}

    .book-edition {{
      margin-top: auto;
      padding-top: 14mm;
      text-align: center;
      font-size: 12px;
      letter-spacing: 0.08em;
      color: var(--muted);
    }}

    .book-chapter > header {{
      margin-bottom: 10mm;
      padding-bottom: 4mm;
      border-bottom: 1px solid var(--rule);
    }}

    .book-chapter > header h1 {{
      margin: 0;
      font-size: 28px;
      line-height: 1.3;
    }}

    .markdown-section {{
      max-width: none;
    }}

    .markdown-section h1:first-child {{
      display: none;
    }}

    .markdown-section p,
    .markdown-section li,
    .markdown-section blockquote {{
      font-size: 15px;
    }}

    .markdown-section img {{
      display: block;
      margin: 1.5rem auto;
      max-width: 100%;
      height: auto;
      page-break-inside: avoid;
      break-inside: avoid;
    }}

    .markdown-section a {{
      color: inherit;
      text-decoration: none;
    }}

    .markdown-section blockquote {{
      color: var(--muted);
      border-left: 4px solid var(--accent);
      padding-left: 12px;
      margin-left: 0;
    }}

    @page {{
      size: A4;
      margin: 16mm 15mm 18mm;
    }}
  </style>
</head>
<body>
  <main class="print-book">
    {''.join(articles)}
  </main>
</body>
</html>
"""


def main() -> None:
    args = parse_args(sys.argv[1:])
    book_dir = resolve_book_dir(args.book_dir)
    meta = load_meta(book_dir, args.locale)
    source_dir = resolve_source_dir(book_dir, args.locale)
    book_output_dir = resolve_build_dir(book_dir, args.locale)
    if not book_output_dir.exists():
        raise SystemExit(f"Missing built book directory: {book_output_dir}")

    output = book_dir / meta["outputs"]["print_html"]
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        build_html(book_dir, meta, source_dir, book_output_dir, draft=args.draft),
        encoding="utf-8",
    )
    print(output)


if __name__ == "__main__":
    main()
