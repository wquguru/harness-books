from __future__ import annotations

import datetime as dt
import json
import re
import subprocess
from pathlib import Path


LINK_RE = re.compile(r"\(([^)#]+\.md)\)")
MARKDOWN_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
TEXT_LINK_RE = re.compile(r"(?<!!)\[([^\]]+)\]\(([^)]+)\)")
TOP_HEADING_RE = re.compile(r"^#\s+(.+)$", re.MULTILINE)
CHAPTER_PREFIX_RE = re.compile(r"^(第\s*[0-9A-Za-z一二三四五六七八九十百千]+\s*章)\s*(.+)$")
APPENDIX_PREFIX_RE = re.compile(r"^(附录\s*[A-Za-z一二三四五六七八九十]+)\s*(.+)$")


def resolve_book_dir(raw_path: str | None) -> Path:
    if raw_path:
        return Path(raw_path).resolve()
    return Path.cwd().resolve()


def load_meta(book_dir: Path) -> dict:
    meta_path = book_dir / "book.meta.json"
    if not meta_path.exists():
        raise SystemExit(f"Missing book metadata: {meta_path}")
    return json.loads(meta_path.read_text(encoding="utf-8"))


def git_revision(book_dir: Path) -> str | None:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short=6", "HEAD"],
            cwd=book_dir,
            check=True,
            capture_output=True,
            text=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None
    revision = result.stdout.strip()
    return revision or None


def release_display_items(book_dir: Path, meta: dict, *, draft: bool = False) -> list[str]:
    items: list[str] = []
    if draft:
        items.append("Draft")
        items.append(dt.date.today().isoformat())
    else:
        release_date = str(meta.get("release_date", "")).strip()
        if release_date:
            items.append(release_date)

    revision = str(meta.get("revision", "")).strip() or git_revision(book_dir) or ""
    if revision:
        items.append(f"rev {revision}")

    return items


def chapter_paths(book_dir: Path) -> list[str]:
    summary_path = book_dir / "SUMMARY.md"
    if not summary_path.exists():
        raise SystemExit(f"Missing SUMMARY.md: {summary_path}")

    paths: list[str] = []
    for line in summary_path.read_text(encoding="utf-8").splitlines():
        match = LINK_RE.search(line)
        if match:
            paths.append(match.group(1))
    return paths


def strip_markdown_links(text: str) -> str:
    return TEXT_LINK_RE.sub(r"\1", text)


def strip_local_file_links(text: str) -> str:
    def repl(match: re.Match[str]) -> str:
        label, target = match.groups()
        if target.startswith(("http://", "https://", "mailto:", "#")):
            return match.group(0)
        return label

    return TEXT_LINK_RE.sub(repl, text)


def strip_markdown_formatting(text: str) -> str:
    text = strip_markdown_links(text)
    text = text.replace("`", "")
    text = re.sub(r"[*_~]+", "", text)
    return text


def top_heading(text: str) -> str | None:
    match = TOP_HEADING_RE.search(text)
    if not match:
        return None
    return strip_markdown_formatting(match.group(1).strip())


def escape_latex(text: str) -> str:
    replacements = {
        "\\": r"\textbackslash{}",
        "{": r"\{",
        "}": r"\}",
        "$": r"\$",
        "&": r"\&",
        "%": r"\%",
        "#": r"\#",
        "_": r"\_",
        "^": r"\^{}",
        "~": r"\~{}",
    }
    return "".join(replacements.get(ch, ch) for ch in text)


def derive_short_title(title: str) -> str:
    title = strip_markdown_formatting(title).strip()

    for separator in ("：", ":"):
        if separator in title:
            return title.split(separator, 1)[0].strip()

    for pattern in (CHAPTER_PREFIX_RE, APPENDIX_PREFIX_RE):
        match = pattern.match(title)
        if match:
            prefix, rest = match.groups()
            for separator in ("：", ":", "，", ",", "、"):
                if separator in rest:
                    return f"{prefix} {rest.split(separator, 1)[0].strip()}".strip()
            return title

    for prefix in ("前言", "序言", "导读"):
        if title.startswith(prefix):
            rest = title[len(prefix) :].strip()
            for separator in ("，", ",", "、", "：", ":", " "):
                if separator in rest:
                    return f"{prefix} {rest.split(separator, 1)[0].strip()}".strip()
            return title

    return title


def short_title_for_path(md_path: str, text: str) -> str | None:
    if md_path == "README.md":
        return None

    heading = top_heading(text)
    if not heading:
        return None
    return derive_short_title(heading)


def replace_top_heading_with_latex(text: str, *, short_title: str) -> str:
    match = TOP_HEADING_RE.search(text)
    if not match:
        return text

    long_title = escape_latex(strip_markdown_formatting(match.group(1).strip()))
    short_title = escape_latex(strip_markdown_formatting(short_title.strip()))
    replacement = f"\\chapter[{short_title}]{{{long_title}}}"
    return text[: match.start()] + replacement + text[match.end() :]


def normalize_readme(text: str, *, title: str, cover_alt: str | None) -> str:
    lines = text.splitlines()
    filtered: list[str] = []
    for line in lines:
        stripped = line.strip()
        if stripped == f"# {title}":
            continue
        if cover_alt and stripped.startswith(f"![{cover_alt}]("):
            continue
        filtered.append(line)

    body = strip_markdown_links("\n".join(filtered).strip())
    return "# 导读\n\n" + body + "\n"
