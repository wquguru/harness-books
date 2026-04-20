from __future__ import annotations

import sys
from pathlib import Path

from book_meta import (
    chapter_paths,
    load_meta,
    normalize_readme,
    replace_top_heading_with_latex,
    resolve_book_dir,
    resolve_source_dir,
    short_title_for_path,
    strip_local_file_links,
)


def build_book(book_dir: Path, meta: dict, source_dir: Path, format: str = "pdf") -> str:
    readme_path = meta.get("readme_path", "README.md")
    chunks: list[str] = []
    for md_path in chapter_paths(source_dir):
        path = source_dir / md_path
        text = path.read_text(encoding="utf-8").strip()
        if md_path == readme_path:
            text = normalize_readme(
                text,
                title=meta["title"],
                cover_alt=meta.get("cover_alt"),
                front_page_heading=str(meta.get("front_page_heading", "导读")),
            )
        elif format == "pdf":
            # Only apply LaTeX conversion for PDF
            short_title = short_title_for_path(md_path, text)
            if short_title:
                text = replace_top_heading_with_latex(
                    text,
                    short_title=short_title,
                )
        # Always strip local file links
        text = strip_local_file_links(text)
        chunks.append(text)

    if format == "pdf":
        return "\n\n\\clearpage\n\n".join(chunks) + "\n"
    else:
        # For EPUB, join with blank lines
        return "\n\n".join(chunks) + "\n"


def main() -> None:
    book_dir = resolve_book_dir(sys.argv[1] if len(sys.argv) > 1 else None)
    locale = sys.argv[2] if len(sys.argv) > 2 else None
    meta = load_meta(book_dir, locale)
    source_dir = resolve_source_dir(book_dir, locale)
    output = book_dir / "_book" / "book.md"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(build_book(book_dir, meta, source_dir), encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
