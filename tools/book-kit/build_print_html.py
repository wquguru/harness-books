from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path

from book_meta import chapter_paths, load_meta, release_display_items, resolve_book_dir


SECTION_RE = re.compile(
    r'<section class="normal markdown-section">(.*?)</section>',
    re.DOTALL,
)
PAGE_RE = re.compile(r"gitbook\.page\.hasChanged\((\{.*?\})\);", re.DOTALL)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build print HTML for a book.")
    parser.add_argument("book_dir", nargs="?", help="Book directory path")
    parser.add_argument(
        "--draft",
        action="store_true",
        help="Render draft release metadata using today's date and the current git revision.",
    )
    return parser.parse_args(argv)


def load_page(book_dir: Path, md_path: str) -> tuple[str, str]:
    book_output_dir = book_dir / "_book"
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


def build_html(book_dir: Path, meta: dict, *, draft: bool = False) -> str:
    articles: list[str] = []
    release_bits = release_display_items(book_dir, meta, draft=draft)

    for index, md_path in enumerate(chapter_paths(book_dir)):
        title, body = load_page(book_dir, md_path)
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
                    f'<article class="{chapter_class}" data-source="{html.escape(md_path)}">',
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
  <link rel="stylesheet" href="../_book/gitbook/style.css" />
  <link rel="stylesheet" href="../styles/website.css" />
  <link rel="stylesheet" href="../styles/pdf.css" />
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
      font-family: "Noto Serif SC", "Songti SC", "STSong", serif;
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
    meta = load_meta(book_dir)
    book_output_dir = book_dir / "_book"
    if not book_output_dir.exists():
        raise SystemExit(f"Missing built book directory: {book_output_dir}")

    output = book_dir / meta["outputs"]["print_html"]
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(build_html(book_dir, meta, draft=args.draft), encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
