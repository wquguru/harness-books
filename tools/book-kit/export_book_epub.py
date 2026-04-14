from __future__ import annotations

import argparse
import os
import subprocess
import sys
import shutil
import uuid
from pathlib import Path

from book_meta import (
    load_meta,
    release_display_items,
    resolve_book_dir,
    resolve_source_dir,
)
from build_pandoc_book import build_book


def run(args: list[str], *, cwd: Path | None = None) -> None:
    subprocess.run(args, cwd=cwd, check=True)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export a book EPUB.")
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
    parser.add_argument(
        "--no-embed-fonts",
        action="store_true",
        help="Disable font embedding even if configured in book.json",
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


def ensure_epub_cover(book_dir: Path, meta: dict, book_output_dir: Path) -> str | None:
    """Convert cover image to JPEG/PNG for EPUB, return relative path or None."""
    epub_config = meta.get("epub", {})
    cover_image = epub_config.get("cover_image") or meta.get("cover_image")
    if not cover_image:
        print("Warning: No cover_image defined in epub config or root metadata", file=sys.stderr)
        return None

    cover_path = book_dir / cover_image
    if cover_path.suffix.lower() in (".jpg", ".jpeg", ".png"):
        return cover_path.relative_to(book_dir).as_posix()

    # Convert SVG/PDF to PNG
    if cover_path.suffix.lower() == ".svg":
        output_cover = book_output_dir / "cover.png"
        try:
            run(["rsvg-convert", "-f", "png", "-o", str(output_cover), str(cover_path)])
        except FileNotFoundError:
            print("Warning: rsvg-convert not found, skipping EPUB cover", file=sys.stderr)
            return None
        return output_cover.relative_to(book_dir).as_posix()
    elif cover_path.suffix.lower() == ".pdf":
        # Convert PDF to PNG (first page)
        output_cover = book_output_dir / "cover.png"
        try:
            run(["pdftoppm", "-png", "-singlefile", str(cover_path), str(output_cover.with_suffix(""))])
        except FileNotFoundError:
            print("Warning: pdftoppm not found, skipping EPUB cover", file=sys.stderr)
            return None
        return output_cover.relative_to(book_dir).as_posix()
    else:
        print(f"Warning: Unsupported cover format for EPUB: {cover_path}, skipping", file=sys.stderr)
        return None


def render_epub_metadata(book_dir: Path, meta: dict, book_output_dir: Path, draft: bool = False) -> Path:
    """Generate EPUB metadata XML file."""
    epub_config = meta.get("epub", {})
    identifier = epub_config.get("identifier", "urn:uuid:generated")
    if identifier == "urn:uuid:generated":
        # Generate deterministic UUID from title and language
        base = f"{meta.get('title', '')}/{meta.get('language', '')}"
        identifier = f"urn:uuid:{uuid.uuid5(uuid.NAMESPACE_DNS, base)}"

    rights = epub_config.get("rights", "CC BY-NC-SA 4.0")
    language = meta.get("language", "en")
    title = meta.get("title", "")
    author = meta.get("author", "")

    release_items = release_display_items(book_dir, meta, draft=draft)
    if release_items:
        description = f"{title}. {', '.join(release_items)}"
    else:
        description = title

    metadata = f"""<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="uid">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="uid">{identifier}</dc:identifier>
    <dc:title>{escape_xml(title)}</dc:title>
    <dc:language>{language}</dc:language>
    <dc:creator>{escape_xml(author)}</dc:creator>
    <dc:rights>{escape_xml(rights)}</dc:rights>
    <dc:description>{escape_xml(description)}</dc:description>
  </metadata>
</package>"""

    metadata_path = book_output_dir / "metadata.xml"
    metadata_path.write_text(metadata, encoding="utf-8")
    return metadata_path


def escape_xml(text: str) -> str:
    """Basic XML escaping."""
    return (text.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace('"', "&quot;")
                .replace("'", "&apos;"))


def main() -> None:
    args = parse_args(sys.argv[1:])
    book_dir = resolve_book_dir(args.book_dir)
    meta = load_meta(book_dir, args.locale)
    source_dir = resolve_source_dir(book_dir, args.locale)
    epub_config = meta.get("epub", {})

    if args.clean or args.clean_generated:
        clean_book_outputs(book_dir, meta)
    if args.clean_generated:
        regenerate_diagrams(book_dir)

    book_output_dir = book_dir / "_book"
    output_name = meta["outputs"].get("epub")
    if not output_name:
        raise SystemExit("Missing epub output path in book.json outputs")
    output = book_dir / output_name
    output.parent.mkdir(parents=True, exist_ok=True)
    book_md = book_output_dir / "book.md"

    book_output_dir.mkdir(parents=True, exist_ok=True)
    book_md.write_text(build_book(book_dir, meta, source_dir, format="epub"), encoding="utf-8")

    cover_image_rel = ensure_epub_cover(book_dir, meta, book_output_dir)
    metadata_xml_path = render_epub_metadata(book_dir, meta, book_output_dir, draft=args.draft)

    # Determine CSS path
    css_path = epub_config.get("css") or meta.get("styles", {}).get("epub")
    if not css_path:
        raise SystemExit("Missing epub CSS path in book.json styles.epub or epub.css")
    epub_css_path = book_dir / css_path

    pandoc_args = [
        "pandoc",
        str(book_md),
        "--from", "markdown",
        "--to", "epub3",
        "--resource-path", str(book_dir),
        "--toc",
        "--toc-depth=2",
        "--css", str(epub_css_path),
        "--epub-metadata", str(metadata_xml_path),
        "-V", f"title={meta['title']}",
        "-V", f"author={meta['author']}",
        "-V", f"language={meta['language']}",
        "-o", str(output),
    ]
    if cover_image_rel:
        pandoc_args.extend(["--epub-cover-image", str(book_dir / cover_image_rel)])

    # Conditionally embed fonts
    embed_fonts = not args.no_embed_fonts and epub_config.get("embed_fonts", True)
    if embed_fonts:
        for font_path in epub_config.get("fonts", []):
            pandoc_args.extend(["--epub-embed-font", str(book_dir / font_path)])

    run(pandoc_args, cwd=book_dir)
    print(output)


if __name__ == "__main__":
    main()
