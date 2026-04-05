#!/usr/bin/env python3
"""Assemble a unified GitHub Pages site for both Honkit books."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
from html import escape, unescape as html_unescape
from pathlib import Path
from urllib.parse import quote

from book_meta import load_meta


REPO_ROOT = Path(__file__).resolve().parents[2]
BOOK_DIRS = ("book1-claude-code", "book2-comparing")
DIST_DIR = REPO_ROOT / "dist"
OG_DIRNAME = "og"
DEFAULT_SITE_URL = "https://harness-books.agentway.dev"
DEFAULT_CUSTOM_DOMAIN = "harness-books.agentway.dev"
DEFAULT_REPOSITORY_URL = "https://github.com/wquguru/harness-books"
SITE_LOCALES = (
    {"code": "zh-Hans", "prefix": "", "name": "中文"},
    {"code": "en", "prefix": "en", "name": "English"},
)
LOCALE_STORAGE_KEY = "harness-books-locale"


def locale_config(locale: str) -> dict[str, str]:
    if locale == "en":
        return {
            "home_label": "Home",
            "download_pdf_label": "Download PDF",
            "github_label": "GitHub",
            "site_label": "Harness Books",
            "switcher_aria": "Book switcher",
            "further_reading_label": "Further Reading",
            "prev_label": "Previous chapter",
            "next_label": "Next chapter",
            "cta_title": "This book stands on its own. AgentWay is a separate practice platform.",
            "cta_body_default": "Harness Books already contains the full public text. Its goal is to explain the control structures and judgments behind harness design. AgentWay is related, but it is not the next chapter of this book. If you want to apply these methods in training, drills, and ongoing practice, you can explore it separately.",
            "cta_body_book2": "This comparative book already lays out the key divergences between Claude Code and Codex. AgentWay is related, but it is not the next chapter of this book. If you want to apply these judgments in training, drills, and ongoing practice, you can explore it separately.",
            "cta_primary": "Explore AgentWay",
            "cta_secondary": "See Where It Fits",
            "root_lang": "en",
            "root_title": "Harness Books",
            "root_description": "Two books on harness engineering: one on the runtime discipline behind Claude Code, and one comparing the harness philosophies of Claude Code and Codex.",
            "hero_eyebrow": "Source-guided analysis of Claude Code and Codex",
            "hero_title": "A two-book series on harness engineering for coding agents",
            "repo_button": "View the GitHub repository",
            "seo_what": "What Is Harness Engineering",
            "seo_what_body": "Harness engineering is about control structure. It asks how the control plane, query loop, permissions, recovery, verification, state, and local governance work together to keep an agent system bounded and accountable.",
            "seo_learn": "What You Will Learn",
            "seo_learn_body": "These books cover the Claude Code runtime, Claude Code vs Codex, coding-agent architecture, recovery paths, verification discipline, approval policy, and context governance.",
            "seo_agentway": "What Is AgentWay",
            "seo_agentway_body": "Harness Books is the public home of these two books. AgentWay is a related but separate practice platform, not the hidden continuation of this site.",
            "footer_note": "This site provides the full public text of both books. On desktop you can switch between books directly inside the reader. On mobile the navigation adapts to touch-friendly vertical layouts.",
            "read_online_label": "Read Online",
            "toc_label": "View Contents",
            "book_cover_alt_suffix": "cover",
            "og_footer_home": "HARNESS BOOKS / HOME",
            "og_footer_book": "HARNESS BOOKS / EN EDITION",
        }
    return {
        "home_label": "首页",
        "download_pdf_label": "下载 PDF",
        "github_label": "GitHub",
        "site_label": "Harness Books",
        "switcher_aria": "Book switcher",
        "further_reading_label": "延伸阅读",
        "prev_label": "回到上一章",
        "next_label": "继续阅读下一章",
        "cta_title": "这本书可以独立阅读，AgentWay 是一个独立的实践平台。",
        "cta_body_default": "Harness Books 提供的是完整公开内容，重点是把 Harness 的控制结构与判断讲清楚。AgentWay 和这些主题相关，但它不是本书的后续章节；如果你想把这些方法继续用于训练、项目演练和持续实践，可以再单独了解它。",
        "cta_body_book2": "这本比较书已经把 Claude Code 与 Codex 的关键分歧完整展开。AgentWay 和这些主题相关，但它不是这本书的下一章；如果你想把这些判断继续用于训练、项目演练和持续实践，可以再单独了解它。",
        "cta_primary": "了解 AgentWay",
        "cta_secondary": "了解适用场景",
        "root_lang": "zh-Hans",
        "root_title": "Harness Books",
        "root_description": "两本围绕 Harness Engineering 的中文书稿：一本文档化 Claude Code 的工程约束，一本比较 Claude Code 与 Codex 的 harness 路线。",
        "hero_eyebrow": "Claude Code 和 Codex 的源码和设计哲学",
        "hero_title": "全网最值得读的Harness工程实践系列书籍（共两本）",
        "repo_button": "查看 GitHub 仓库",
        "seo_what": "What Is Harness Engineering",
        "seo_what_body": "Harness Engineering 讨论的是控制结构。它关心 control plane、query loop、permissions、recovery、verification、state 和 local governance 怎样一起维持 agent system 的边界与后果控制。",
        "seo_learn": "What You Will Learn",
        "seo_learn_body": "这两本书覆盖 Claude Code guide、Claude Code vs Codex、AI coding agent architecture、agent recovery、agent verification、approval policy 和 context governance 等核心主题。",
        "seo_agentway": "AgentWay 是什么",
        "seo_agentway_body": "Harness Books 是这两本书的官网，本身就提供完整公开内容。AgentWay 是相关但独立的实践平台，不是本网站的后续章节；如果你想把书里的方法继续用于训练、项目演练和持续实践，可以再单独了解它。",
        "footer_note": "这是这两本 Harness 工程书的官网，不需要注册也可以完整阅读。桌面端可以在书内直接切换，移动端会自动调整为更适合触屏阅读的纵向导航。",
        "read_online_label": "在线阅读",
        "toc_label": "查看目录",
        "book_cover_alt_suffix": "封面",
        "og_footer_home": "HARNESS BOOKS / HOME",
        "og_footer_book": "HARNESS BOOKS / ZH EDITION",
    }


def locale_prefix(locale: str) -> str:
    for item in SITE_LOCALES:
        if item["code"] == locale:
            return item["prefix"]
    return ""


def locale_name(locale: str) -> str:
    for item in SITE_LOCALES:
        if item["code"] == locale:
            return item["name"]
    return locale


def locale_code_to_prefix(locale: str) -> str:
    for item in SITE_LOCALES:
        if item["code"] == locale:
            return item["prefix"]
    return ""


def detect_locale_from_path(path: str) -> str:
    normalized = path.strip("/")
    if normalized == "en" or normalized.startswith("en/"):
        return "en"
    return "zh-Hans"


def localized_book_target(current_slug: str, current_page: str, target_locale: str) -> str:
    target_prefix = locale_code_to_prefix(target_locale)
    book_root = Path(target_prefix) / current_slug if target_prefix else Path(current_slug)
    normalized_page = current_page.strip()
    if not normalized_page or normalized_page == ".":
        normalized_page = "index.html"
    return str(book_root / normalized_page)


LOCALE_SWITCH_SCRIPT = f"""
<script>
(function () {{
  var storageKey = {json.dumps(LOCALE_STORAGE_KEY)};

  function safeLocalStorage() {{
    try {{
      return window.localStorage;
    }} catch (error) {{
      return null;
    }}
  }}

  function readStoredLocale() {{
    var storage = safeLocalStorage();
    if (!storage) return "";
    try {{
      return storage.getItem(storageKey) || "";
    }} catch (error) {{
      return "";
    }}
  }}

  function writeStoredLocale(locale) {{
    var storage = safeLocalStorage();
    if (!storage) return;
    try {{
      storage.setItem(storageKey, locale);
    }} catch (error) {{
      return;
    }}
  }}

  function detectBrowserLocale() {{
    var languages = navigator.languages && navigator.languages.length
      ? navigator.languages
      : [navigator.language || navigator.userLanguage || ""];
    for (var index = 0; index < languages.length; index += 1) {{
      var value = String(languages[index] || "").toLowerCase();
      if (!value) continue;
      if (value.indexOf("zh") === 0) return "zh-Hans";
      if (value.indexOf("en") === 0) return "en";
    }}
    return "zh-Hans";
  }}

  document.addEventListener("click", function (event) {{
    var target = event.target.closest("[data-hb-locale]");
    if (!target) return;
    writeStoredLocale(target.getAttribute("data-hb-locale") || "");
  }});

  if (!document.documentElement.hasAttribute("data-hb-autodetect")) return;

  var currentLocale = document.documentElement.getAttribute("data-locale") || "zh-Hans";
  var preferredLocale = readStoredLocale() || detectBrowserLocale();
  if (!preferredLocale || preferredLocale === currentLocale) {{
    writeStoredLocale(currentLocale);
    return;
  }}

  var targetPrefix = preferredLocale === "en" ? "/en/" : "/";
  var currentPath = window.location.pathname || "/";
  if (currentPath !== "/" && currentPath !== "/index.html") return;
  window.location.replace(targetPrefix);
}})();
</script>
""".strip()


def relative_href(from_dir: str, to_path: str) -> str:
    return os.path.relpath(to_path, start=from_dir).replace(os.sep, "/")
BOOK_SWITCHER_CSS = """
<style>
:root {
  --hb-page-bg: #f7f2e8;
  --hb-page-bg-soft: #efe8d9;
  --hb-panel-bg: rgba(252, 248, 239, 0.86);
  --hb-panel-strong: rgba(247, 241, 230, 0.96);
  --hb-summary-width: 320px;
  --hb-nav-bg: rgba(249, 245, 237, 0.82);
  --hb-nav-border: rgba(53, 41, 27, 0.12);
  --hb-nav-text: #2d2418;
  --hb-nav-muted: #756756;
  --hb-nav-pill: rgba(255, 252, 245, 0.82);
  --hb-nav-pill-active: #2d2418;
  --hb-nav-pill-active-text: #f8f4ea;
  --hb-shadow: 0 20px 46px rgba(53, 41, 27, 0.10);
  --hb-shadow-soft: 0 10px 24px rgba(53, 41, 27, 0.08);
}

.book.with-site-switcher {
  font-family: "Iowan Old Style", "Palatino Linotype", "Noto Serif SC", "Source Han Serif SC", serif;
  background:
    radial-gradient(circle at top left, rgba(187, 145, 94, 0.12), transparent 24%),
    radial-gradient(circle at right 12% top 10%, rgba(135, 89, 50, 0.10), transparent 18%),
    linear-gradient(180deg, var(--hb-page-bg) 0%, var(--hb-page-bg-soft) 100%);
}

.book.with-site-switcher .book-summary {
  left: calc(-1 * var(--hb-summary-width));
  width: var(--hb-summary-width);
  background: rgba(242, 235, 223, 0.72);
  border-right: 1px solid rgba(53, 41, 27, 0.08);
  box-shadow: inset -1px 0 0 rgba(255, 255, 255, 0.35);
}

.book.with-site-switcher.with-summary .book-summary {
  left: 0;
}

.book.with-site-switcher .book-summary {
  padding-top: 76px;
}

.book.with-site-switcher .book-body {
  padding-top: 76px;
  background: transparent;
}

.book.with-site-switcher .book-body .body-inner {
  background: transparent;
}

.book.with-site-switcher .book-body .page-wrapper {
  background: transparent;
}

.book.with-site-switcher .book-body .page-wrapper .page-inner {
  max-width: 940px;
  margin: 22px auto 36px;
  padding: 38px 44px 42px;
  border: 1px solid rgba(53, 41, 27, 0.10);
  border-radius: 28px;
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.42), transparent 100%),
    var(--hb-panel-bg);
  box-shadow: var(--hb-shadow);
}

.book.with-site-switcher .book-body .page-wrapper .page-inner section.normal {
  color: #33291d;
  font-size: 17px;
  line-height: 1.92;
}

.book.with-site-switcher .book-body .page-wrapper .page-inner section.normal h1,
.book.with-site-switcher .book-body .page-wrapper .page-inner section.normal h2,
.book.with-site-switcher .book-body .page-wrapper .page-inner section.normal h3 {
  color: #211912;
  font-weight: 700;
  letter-spacing: 0.01em;
}

.book.with-site-switcher .book-body .page-wrapper .page-inner section.normal h1 {
  margin-top: 0.2em;
  margin-bottom: 0.7em;
  font-size: 2.15em;
  line-height: 1.15;
}

.book.with-site-switcher .book-body .page-wrapper .page-inner section.normal h2 {
  margin-top: 1.7em;
  font-size: 1.5em;
}

.book.with-site-switcher .book-body .page-wrapper .page-inner section.normal p,
.book.with-site-switcher .book-body .page-wrapper .page-inner section.normal li,
.book.with-site-switcher .book-body .page-wrapper .page-inner section.normal blockquote {
  max-width: 38em;
}

.book.with-site-switcher .book-body .page-wrapper .page-inner section.normal blockquote {
  margin: 1.5rem 0;
  padding: 0.2rem 0 0.2rem 1rem;
  border-left: 3px solid rgba(135, 89, 50, 0.34);
  color: #5e5245;
  background: transparent;
}

.book.with-site-switcher .book-body .page-wrapper .page-inner section.normal a {
  color: #875932;
}

.book.with-site-switcher .book-body .page-wrapper .page-inner section.normal code {
  padding: 0.12em 0.35em;
  border-radius: 6px;
  background: rgba(135, 89, 50, 0.09);
  color: #5c3b22;
}

.book.with-site-switcher .book-body .page-wrapper .page-inner section.normal pre {
  border-radius: 18px;
  border: 1px solid rgba(53, 41, 27, 0.08);
  box-shadow: var(--hb-shadow-soft);
}

.book.with-site-switcher .hb-inline-pager {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
  margin: 30px 0 18px;
}

.book.with-site-switcher .hb-inline-pager__link {
  display: block;
  min-width: 0;
  padding: 14px 16px;
  border: 1px solid rgba(53, 41, 27, 0.10);
  border-radius: 18px;
  background: rgba(255, 252, 245, 0.72);
  color: #2d2418;
  text-decoration: none;
  box-shadow: var(--hb-shadow-soft);
}

.book.with-site-switcher .hb-inline-pager__link:hover,
.book.with-site-switcher .hb-inline-pager__link:focus-visible {
  border-color: rgba(135, 89, 50, 0.28);
  background: rgba(255, 252, 245, 0.92);
}

.book.with-site-switcher .hb-inline-pager__link--next {
  text-align: right;
}

.book.with-site-switcher .hb-inline-pager__eyebrow {
  display: block;
  margin-bottom: 6px;
  color: #875932;
  font-family: "Avenir Next", "PingFang SC", sans-serif;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.10em;
  text-transform: uppercase;
}

.book.with-site-switcher .hb-inline-pager__title {
  display: block;
  color: #1f1812;
  font-size: 0.98rem;
  font-weight: 700;
  line-height: 1.45;
}

.book.with-site-switcher .hb-agentway-cta {
  margin: 0 0 6px;
  padding: 18px 18px 16px;
  border: 1px solid rgba(53, 41, 27, 0.10);
  border-radius: 22px;
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.42), transparent 100%),
    rgba(247, 241, 230, 0.86);
  box-shadow: var(--hb-shadow-soft);
}

.book.with-site-switcher .hb-agentway-cta__eyebrow {
  margin: 0 0 8px;
  color: #875932;
  font-family: "Avenir Next", "PingFang SC", sans-serif;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

.book.with-site-switcher .hb-agentway-cta h3 {
  margin: 0;
  color: #1f1812;
  font-size: 1.26rem;
  line-height: 1.3;
}

.book.with-site-switcher .hb-agentway-cta p {
  margin: 10px 0 0;
  max-width: none;
  color: #4f4336;
}

.book.with-site-switcher .hb-agentway-cta__actions {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 14px;
}

.book.with-site-switcher .hb-agentway-cta__link {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 40px;
  padding: 0 14px;
  border-radius: 999px;
  border: 1px solid rgba(53, 41, 27, 0.10);
  background: rgba(255, 252, 245, 0.82);
  color: #2d2418;
  font-family: "Avenir Next", "PingFang SC", sans-serif;
  font-size: 13px;
  font-weight: 700;
  text-decoration: none;
}

.book.with-site-switcher .hb-agentway-cta__link--primary {
  background: #312015;
  border-color: #312015;
  color: #f8f4ea;
}

.book.with-site-switcher #book-search-input {
  margin: 0 16px 12px;
  padding: 0;
  background: transparent;
}

.book.with-site-switcher #book-search-input input {
  height: 44px;
  border: 1px solid rgba(53, 41, 27, 0.10);
  border-radius: 999px;
  background: rgba(255, 252, 245, 0.78);
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.65);
  color: #3a2e22;
  font-size: 14px;
}

.book.with-site-switcher .summary {
  padding-bottom: 32px;
}

.book.with-site-switcher .summary li a,
.book.with-site-switcher .summary li span {
  color: #5d5042;
  border-bottom: none;
}

.book.with-site-switcher .summary li.chapter.active > a,
.book.with-site-switcher .summary li.active > a {
  color: #1f1812;
  font-weight: 700;
}

.book.with-site-switcher .summary li.chapter {
  margin: 2px 10px;
  border-radius: 14px;
}

.book.with-site-switcher .summary li.chapter > a {
  border-radius: 14px;
}

.book.with-site-switcher .summary li.chapter.active > a {
  background: rgba(255, 252, 245, 0.70);
}

.book.with-site-switcher .book-header {
  border-bottom: 1px solid rgba(53, 41, 27, 0.08);
  background: rgba(249, 244, 235, 0.58);
}

.hb-site-switcher {
  position: fixed;
  top: 10px;
  left: 14px;
  right: 14px;
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
  padding: 10px 12px;
  border: 1px solid var(--hb-nav-border);
  border-radius: 22px;
  background: var(--hb-nav-bg);
  backdrop-filter: blur(18px);
  box-shadow: var(--hb-shadow-soft);
}

.hb-site-switcher__brand {
  min-width: 0;
  padding-left: 4px;
}

.hb-site-switcher__eyebrow {
  margin: 0 0 2px;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--hb-nav-muted);
}

.hb-site-switcher__title {
  margin: 0;
  font-size: 13px;
  font-weight: 700;
  line-height: 1.3;
  color: var(--hb-nav-text);
}

.hb-site-switcher__links {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
  gap: 6px;
}

@media screen and (min-width: 600px) {
  .book.with-site-switcher.with-summary .book-body {
    left: var(--hb-summary-width);
  }
}

@media screen and (max-width: 600px) {
  .book.with-site-switcher .book-summary {
    left: calc(-1 * var(--hb-summary-width));
  }

  .book.with-site-switcher.with-summary .book-summary {
    left: 0;
  }
}

.hb-site-switcher__link {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 34px;
  padding: 0 12px;
  border: 1px solid var(--hb-nav-border);
  border-radius: 999px;
  background: var(--hb-nav-pill);
  color: var(--hb-nav-text);
  font-size: 12px;
  font-weight: 600;
  text-decoration: none;
  transition: transform 120ms ease, background-color 120ms ease, color 120ms ease, box-shadow 120ms ease;
}

.hb-site-switcher__link:hover,
.hb-site-switcher__link:focus-visible {
  transform: translateY(-1px);
  text-decoration: none;
  box-shadow: var(--hb-shadow-soft);
}

.hb-site-switcher__link.is-active {
  background: var(--hb-nav-pill-active);
  border-color: var(--hb-nav-pill-active);
  color: var(--hb-nav-pill-active-text);
}

@media (max-width: 860px) {
  :root {
    --hb-summary-width: 290px;
  }

  .book.with-site-switcher .book-summary,
  .book.with-site-switcher .book-body {
    padding-top: 92px;
  }

  .hb-site-switcher {
    top: 8px;
    left: 8px;
    right: 8px;
    align-items: center;
    padding: 8px 10px;
    gap: 10px;
  }

  .book.with-site-switcher .book-summary {
    width: var(--hb-summary-width);
  }

  .book.with-site-switcher .book-body .page-wrapper .page-inner {
    margin: 18px 14px 28px;
    padding: 28px 24px 30px;
  }

  .hb-site-switcher__links {
    flex: 1 1 auto;
    justify-content: flex-end;
  }

  .hb-site-switcher__link {
    min-width: fit-content;
  }
}

@media (max-width: 640px) {
  :root {
    --hb-summary-width: min(86vw, 320px);
  }

  .book.with-site-switcher .book-summary,
  .book.with-site-switcher .book-body {
    padding-top: 86px;
  }

  .book.with-site-switcher .book-summary {
    width: var(--hb-summary-width);
  }

  .book.with-site-switcher .book-body .page-wrapper .page-inner {
    margin: 12px 8px 20px;
    padding: 20px 16px 22px;
    border-radius: 22px;
  }

  .book.with-site-switcher .book-body .page-wrapper .page-inner section.normal {
    font-size: 16px;
    line-height: 1.82;
  }

  .book.with-site-switcher .book-body .page-wrapper .page-inner section.normal h1 {
    font-size: 1.75em;
  }

  .book.with-site-switcher .book-body .page-wrapper .page-inner section.normal h2 {
    font-size: 1.28em;
  }

  .hb-site-switcher {
    top: 6px;
    left: 6px;
    right: 6px;
    flex-direction: column;
    align-items: stretch;
    padding: 8px 10px;
    border-radius: 18px;
  }

  .hb-site-switcher__brand {
    width: 100%;
    padding-left: 0;
  }

  .hb-site-switcher__eyebrow {
    display: none;
  }

  .hb-site-switcher__links {
    display: flex;
    flex-wrap: nowrap;
    width: 100%;
    overflow-x: auto;
    justify-content: flex-start;
    padding-bottom: 2px;
    scrollbar-width: none;
  }

  .hb-site-switcher__links::-webkit-scrollbar {
    display: none;
  }

  .hb-site-switcher__link {
    flex: 0 0 auto;
    min-height: 32px;
    padding: 0 10px;
  }

  .hb-site-switcher__title {
    font-size: 12px;
  }

  .book.with-site-switcher .hb-inline-pager {
    grid-template-columns: 1fr;
    gap: 10px;
    margin: 24px 0 16px;
  }

  .book.with-site-switcher .hb-inline-pager__link--next {
    text-align: left;
  }

  .book.with-site-switcher .hb-agentway-cta {
    margin-top: 22px;
    padding: 16px 14px 14px;
    border-radius: 18px;
  }

  .book.with-site-switcher .hb-agentway-cta__actions {
    flex-direction: column;
  }

  .book.with-site-switcher .hb-agentway-cta__link {
    width: 100%;
  }
}
</style>
""".strip()
SITE_INDEX_CSS = """
<style>
:root {
  --page-bg: #f4efe4;
  --panel-bg: rgba(252, 248, 239, 0.82);
  --panel-strong: rgba(247, 241, 230, 0.94);
  --panel-border: rgba(61, 47, 31, 0.12);
  --text-strong: #221b14;
  --text-body: #4c4135;
  --text-muted: #786b5c;
  --accent: #875932;
  --accent-strong: #312015;
  --accent-soft: #efe3d5;
  --shadow: 0 24px 60px rgba(50, 37, 23, 0.10);
  --shadow-soft: 0 10px 24px rgba(50, 37, 23, 0.08);
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  min-height: 100vh;
  font-family: "Iowan Old Style", "Palatino Linotype", "Noto Serif SC", "Source Han Serif SC", serif;
  color: var(--text-body);
  background:
    radial-gradient(circle at top left, rgba(187, 145, 94, 0.16), transparent 26%),
    radial-gradient(circle at 85% 10%, rgba(120, 100, 76, 0.12), transparent 20%),
    linear-gradient(180deg, #f8f3ea 0%, #f1eadc 100%);
}

a {
  color: inherit;
}

.site-shell {
  width: min(1180px, calc(100% - 32px));
  margin: 0 auto;
  padding: 16px 0 44px;
}

.hero {
  position: relative;
  overflow: hidden;
  padding: 18px 22px 34px;
  border: 1px solid var(--panel-border);
  border-radius: 30px;
  background:
    linear-gradient(135deg, rgba(255, 255, 255, 0.55), transparent 46%),
    linear-gradient(180deg, var(--panel-strong), rgba(249, 243, 233, 0.90));
  backdrop-filter: blur(16px);
  box-shadow: var(--shadow);
}

.hero::after {
  content: "";
  position: absolute;
  inset: auto -12% -28% auto;
  width: 320px;
  aspect-ratio: 1;
  border-radius: 999px;
  background: radial-gradient(circle, rgba(135, 89, 50, 0.12), transparent 70%);
  pointer-events: none;
}

.hero__eyebrow {
  margin: 0 0 6px;
  font-size: clamp(1.05rem, 2vw, 1.48rem);
  font-weight: 700;
  line-height: 1.3;
  letter-spacing: 0.03em;
  color: var(--accent);
}

.hero h1 {
  margin: 0;
  max-width: 14ch;
  font-size: clamp(1.72rem, 3.3vw, 2.72rem);
  line-height: 1.08;
  color: var(--text-strong);
}

.hero p {
  margin: 10px 0 0;
  max-width: 760px;
  font-size: 0.98rem;
  line-height: 1.62;
}

.hero__principles {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 12px;
}

.hero__principle {
  flex: 1 1 220px;
  padding: 10px 12px 11px;
  border: 1px solid rgba(61, 47, 31, 0.10);
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.48);
  box-shadow: var(--shadow-soft);
}

.hero__principle strong {
  display: block;
  margin-bottom: 4px;
  color: var(--text-strong);
  font-size: 0.9rem;
}

.hero__principle span {
  display: block;
  color: var(--text-muted);
  font-size: 0.88rem;
  line-height: 1.5;
}

.library {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 22px;
  position: relative;
  z-index: 1;
  margin-top: 18px;
  padding: 0 18px;
}

.book-card {
  display: grid;
  grid-template-columns: minmax(0, 0.8fr) minmax(0, 1.2fr);
  gap: 24px;
  align-items: start;
  padding: 24px;
  border: 1px solid var(--panel-border);
  border-radius: 28px;
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.42), transparent 100%),
    var(--panel-bg);
  box-shadow: 0 28px 64px rgba(41, 30, 18, 0.12);
}

.book-card__cover-wrap {
  position: relative;
}

.book-card__cover {
  display: block;
  width: 100%;
  aspect-ratio: 5 / 8;
  object-fit: cover;
  border-radius: 22px;
  border: 1px solid rgba(61, 47, 31, 0.14);
  background: #f6f0e4;
  box-shadow: 0 18px 40px rgba(42, 31, 20, 0.16);
}

.book-card__body {
  display: flex;
  flex-direction: column;
  gap: 16px;
  min-width: 0;
}

.book-card__meta,
.book-card__facts {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
}

.book-card__meta span,
.book-card__facts span {
  display: inline-flex;
  align-items: center;
  min-height: 34px;
  padding: 0 12px;
  border-radius: 999px;
  border: 1px solid rgba(61, 47, 31, 0.10);
  background: rgba(255, 255, 255, 0.54);
  color: var(--text-muted);
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

.book-card__kicker {
  margin: 0;
  color: var(--accent);
  font-size: 0.88rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.book-card h2 {
  margin: 0;
  font-size: clamp(1.8rem, 3vw, 2.55rem);
  line-height: 1.08;
  color: var(--text-strong);
}

.book-card__lede {
  margin: 0;
  color: var(--text-body);
  font-size: 1rem;
  line-height: 1.8;
}

.book-card__summary {
  margin: 0;
  color: var(--text-muted);
  line-height: 1.75;
}

.book-card__actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: auto;
}

.button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 48px;
  padding: 0 18px;
  border-radius: 999px;
  text-decoration: none;
  font-weight: 700;
  font-size: 0.98rem;
  transition: transform 160ms ease, background-color 160ms ease, color 160ms ease, box-shadow 160ms ease;
}

.button:hover,
.button:focus-visible {
  transform: translateY(-1px);
  box-shadow: var(--shadow-soft);
}

.button--primary {
  background: var(--accent-strong);
  color: #f8f4ea;
}

.button--secondary {
  border: 1px solid var(--panel-border);
  background: rgba(255, 255, 255, 0.58);
  color: var(--text-strong);
}

.footer-note {
  margin-top: 20px;
  font-size: 14px;
  color: var(--text-muted);
  text-align: center;
  line-height: 1.7;
}

.seo-sections {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 18px;
  margin-top: 22px;
}

.seo-block {
  padding: 18px 18px 16px;
  border: 1px solid var(--panel-border);
  border-radius: 22px;
  background: rgba(255, 252, 246, 0.62);
  box-shadow: var(--shadow-soft);
}

.seo-block h3 {
  margin: 0 0 10px;
  color: var(--text-strong);
  font-size: 1.1rem;
}

.seo-block p {
  margin: 0;
  color: var(--text-body);
  line-height: 1.72;
}

.seo-block__actions {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 14px;
}

.seo-block__actions .button {
  min-height: 42px;
  padding: 0 16px;
  font-size: 0.94rem;
}

@media (max-width: 860px) {
  .site-shell {
    width: min(100%, calc(100% - 20px));
    padding: 14px 0 28px;
  }

  .hero,
  .book-card {
    padding: 18px;
    border-radius: 22px;
  }

  .hero {
    padding-bottom: 20px;
  }

  .hero__principles,
  .seo-sections,
  .library {
    grid-template-columns: 1fr;
  }

  .library {
    margin-top: 14px;
    padding: 0;
  }

  .book-card {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 540px) {
  .hero__eyebrow {
    font-size: clamp(1rem, 5.4vw, 1.32rem);
  }

  .hero h1 {
    max-width: 100%;
    font-size: clamp(1.5rem, 7vw, 2.05rem);
  }

  .hero__principles {
    display: grid;
    grid-template-columns: 1fr;
    gap: 8px;
  }

  .book-card__meta {
    gap: 8px;
  }

  .book-card__actions {
    flex-direction: column;
  }

  .button {
    width: 100%;
  }
}
</style>
""".strip()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Assemble a single GitHub Pages site for both books."
    )
    parser.add_argument(
        "--dist-dir",
        default=str(DIST_DIR),
        help="Output directory for the combined site.",
    )
    parser.add_argument(
        "--site-url",
        default=os.environ.get("SITE_URL", DEFAULT_SITE_URL).strip(),
        help="Public base URL for absolute Open Graph and Twitter card URLs.",
    )
    parser.add_argument(
        "--custom-domain",
        default=os.environ.get("CUSTOM_DOMAIN", DEFAULT_CUSTOM_DOMAIN).strip(),
        help="Custom domain written to dist/CNAME for GitHub Pages.",
    )
    parser.add_argument(
        "--repository-url",
        default=os.environ.get("REPOSITORY_URL", DEFAULT_REPOSITORY_URL).strip(),
        help="Repository URL shown in the per-book site switcher.",
    )
    return parser.parse_args()


def load_book_metadata(book_dir: Path, locale: str) -> dict[str, str]:
    book_json = load_meta(book_dir, None if locale == "zh-Hans" else locale)
    extras_by_locale = {
        "zh-Hans": {
            "book1-claude-code": {
                "kicker": "Runtime Discipline",
                "lede": "围绕 Claude Code 的运行时骨架展开，重点讨论控制面、连续性、恢复路径与验证分工。",
                "summary": "适合想先建立完整框架的人。它追问的是一个 agent 系统为什么会长出 Query Loop、权限判定、上下文治理和团队制度这些器官。系统要有体面，残局就得有人接。",
                "facts": ("Control Plane", "Query Loop", "Recovery"),
            },
            "book2-comparing": {
                "kicker": "Comparative Harness",
                "lede": "沿着控制面、状态、策略与本地治理比较 Claude Code 和 Codex 两条 harness 路线。",
                "summary": "适合已经熟悉 agent coding 工具、想直接看架构分歧与选型判断的人。它比较的是控制权、状态治理和组织纪律分别住在哪一层。规矩写在哪里，系统以后就长成什么样。",
                "facts": ("Policy Layer", "State", "Local Rules"),
            },
        },
        "en": {
            "book1-claude-code": {
                "kicker": "Runtime Discipline",
                "lede": "A close reading of Claude Code's runtime structure, focused on control planes, continuity, recovery paths, and verification work split.",
                "summary": "Best for readers who want the full frame first. It asks why an agent system grows organs such as a query loop, permission checks, context governance, and team rules. If a system is meant to stay composed, someone has to handle the messy endings.",
                "facts": ("Control Plane", "Query Loop", "Recovery"),
            },
            "book2-comparing": {
                "kicker": "Comparative Harness",
                "lede": "A comparison of Claude Code and Codex through control planes, state, policy, and local governance.",
                "summary": "Best for readers who already know coding-agent tools and want the architectural split and selection logic directly. The real comparison is where control, state discipline, and organizational rules actually live.",
                "facts": ("Policy Layer", "State", "Local Rules"),
            },
        },
    }
    extras = extras_by_locale.get(locale, {}).get(book_dir.name, {})
    prefix = locale_prefix(locale)
    cover_rel = str(book_json.get("cover_image", f"assets/cover-wxb.svg")).strip() or "assets/cover-wxb.svg"
    cover = f"{book_dir.name}/{cover_rel}"
    return {
        "slug": book_dir.name,
        "locale": locale,
        "locale_prefix": prefix,
        "title": book_json.get("title", book_dir.name),
        "description": book_json.get("description", ""),
        "cover": cover,
        "kicker": extras.get("kicker", ""),
        "lede": extras.get("lede", book_json.get("description", "")),
        "summary": extras.get("summary", book_json.get("description", "")),
        "facts": extras.get("facts", ()),
        "pdf_path": book_json.get("outputs", {}).get("pdf", ""),
    }


def normalize_site_url(site_url: str) -> str:
    return site_url.rstrip("/")


def join_public_url(site_url: str, relative_path: str) -> str:
    if not site_url:
        return relative_path
    return f"{normalize_site_url(site_url)}/{relative_path.lstrip('/')}"


def collect_site_urls(dist_dir: Path) -> list[str]:
    urls: list[str] = []
    for html_path in sorted(dist_dir.rglob("*.html")):
        relative = html_path.relative_to(dist_dir).as_posix()
        if (
            relative.startswith("og/")
            or "/exported/" in f"/{relative}"
            or relative.startswith("exported/")
        ):
            continue
        if relative == "index.html":
            urls.append("")
        elif relative.endswith("/index.html"):
            urls.append(relative[: -len("index.html")])
        else:
            urls.append(relative)
    return urls


def safe_stem(value: str) -> str:
    stem = re.sub(r"[^a-zA-Z0-9_-]+", "-", value.strip().lower()).strip("-")
    return stem or "page"


def split_title_lines(title: str, max_len: int = 18) -> list[str]:
    text = re.sub(r"\s+", " ", title).strip()
    if not text:
        return ["Harness Books"]
    chunks: list[str] = []
    current = ""
    for char in text:
        if len(current) >= max_len and char in " ：:，,、）)]】 ":
            if current.strip():
                chunks.append(current.strip())
            current = ""
            continue
        current += char
        if len(current) >= max_len and char in "：:，,、 ":
            chunks.append(current.strip())
            current = ""
    if current.strip():
        chunks.append(current.strip())
    if len(chunks) == 1 and len(chunks[0]) > max_len + 4:
        midpoint = len(chunks[0]) // 2
        chunks = [chunks[0][:midpoint].strip(), chunks[0][midpoint:].strip()]
    return chunks[:3]


def build_og_svg(
    *,
    eyebrow: str,
    title: str,
    subtitle: str,
    footer: str,
    accent_mode: str = "single",
) -> str:
    title_lines = split_title_lines(title, max_len=16)
    title_y = 340
    line_gap = 110
    title_text = "\n".join(
        f'<text x="110" y="{title_y + index * line_gap}" fill="#1f1812" '
        f'font-family="Iowan Old Style, Palatino Linotype, Noto Serif SC, serif" '
        f'font-size="78" font-weight="700">{escape(line)}</text>'
        for index, line in enumerate(title_lines)
    )
    accent_markup = (
        '<rect x="0" y="0" width="1200" height="24" fill="#8b5b31"/>'
        '<rect x="0" y="24" width="1200" height="10" fill="#241a12"/>'
        if accent_mode == "single"
        else '<rect x="0" y="0" width="600" height="34" fill="#241a12"/>'
        '<rect x="600" y="0" width="600" height="34" fill="#8b5b31"/>'
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630" role="img" aria-label="{escape(title)}">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#f8f3ea"/>
      <stop offset="100%" stop-color="#efe6d8"/>
    </linearGradient>
    <radialGradient id="glow" cx="1" cy="0" r="1">
      <stop offset="0%" stop-color="rgba(139,91,49,0.18)"/>
      <stop offset="100%" stop-color="rgba(139,91,49,0)"/>
    </radialGradient>
  </defs>
  <rect width="1200" height="630" fill="url(#bg)"/>
  {accent_markup}
  <circle cx="1030" cy="120" r="180" fill="url(#glow)"/>
  <rect x="64" y="72" width="1072" height="486" rx="30" fill="rgba(255,252,246,0.72)" stroke="rgba(53,41,27,0.12)"/>
  <text x="110" y="132" fill="#8b5b31" font-family="Avenir Next, PingFang SC, sans-serif" font-size="20" font-weight="700" letter-spacing="5">{escape(eyebrow.upper())}</text>
  {title_text}
  <text x="110" y="500" fill="#4f4337" font-family="Iowan Old Style, Palatino Linotype, Noto Serif SC, serif" font-size="30">{escape(subtitle)}</text>
  <line x1="110" y1="538" x2="1090" y2="538" stroke="rgba(139,91,49,0.28)" stroke-width="2"/>
  <text x="110" y="580" fill="#736656" font-family="Avenir Next, PingFang SC, sans-serif" font-size="22" letter-spacing="2">{escape(footer)}</text>
</svg>
"""


def write_og_image(dist_dir: Path, relative_path: str, svg: str) -> None:
    output_path = dist_dir / relative_path
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(svg, encoding="utf-8")


def ensure_honkit_output(book_dir: Path, locale: str) -> Path:
    locale_build = book_dir / "_book" / locale
    if locale != "zh-Hans" and (locale_build / "index.html").exists():
        return locale_build
    candidates = [
        book_dir / "_book",
        book_dir / book_dir.name / "_book",
    ]
    for output_dir in candidates:
        if (output_dir / "index.html").exists():
            return output_dir
    raise SystemExit(
        f"Missing Honkit output for {book_dir.name}. Build the site first with "
        f"`python3 tools/book-kit/build_honkit.py {book_dir.name}` or "
        f"`python3 tools/book-kit/build_honkit.py {book_dir.name} --locale {locale}`."
    )


def copy_book_output(book_dir: Path, target_dir: Path, locale: str) -> None:
    source_dir = ensure_honkit_output(book_dir, locale)
    if target_dir.exists():
        shutil.rmtree(target_dir)
    ignore_patterns = ["_texdebug", "_debug", "*.md"]
    if locale == "zh-Hans":
        ignore_patterns.extend(
            [item["prefix"] for item in SITE_LOCALES if item["prefix"]]
        )
    shutil.copytree(
        source_dir,
        target_dir,
        ignore=shutil.ignore_patterns(*ignore_patterns),
    )

    assets_dir = book_dir / "assets"
    if assets_dir.exists():
        target_assets = target_dir / "assets"
        if target_assets.exists():
            shutil.rmtree(target_assets)
        shutil.copytree(assets_dir, target_assets)

    diagrams_dir = book_dir / "diagrams"
    if diagrams_dir.exists():
        target_diagrams = target_dir / "diagrams"
        if target_diagrams.exists():
            shutil.rmtree(target_diagrams)
        shutil.copytree(diagrams_dir, target_diagrams, ignore=shutil.ignore_patterns("*.puml"))

    exported_dir = book_dir / "exported"
    if exported_dir.exists():
        target_exported = target_dir / "exported"
        if target_exported.exists():
            shutil.rmtree(target_exported)
        shutil.copytree(exported_dir, target_exported)


def build_switcher_markup(
    current_slug: str,
    current_page: str,
    books: list[dict[str, str]],
    repository_url: str,
    locale: str,
) -> str:
    strings = locale_config(locale)
    current_prefix = locale_prefix(locale)
    current_dir = str(Path(current_prefix) / current_slug) if current_prefix else current_slug
    home_target = str(Path(current_prefix) / "index.html") if current_prefix else "index.html"
    link_parts = [
        f'<a class="hb-site-switcher__link" href="{escape(relative_href(current_dir, home_target))}">{escape(strings["home_label"])}</a>'
    ]
    current_book = next(book for book in books if book["slug"] == current_slug)
    for book in books:
        classes = "hb-site-switcher__link"
        if book["slug"] == current_slug:
            classes += " is-active"
        target = (
            str(Path(book["locale_prefix"]) / book["slug"] / "index.html")
            if book["locale_prefix"]
            else str(Path(book["slug"]) / "index.html")
        )
        link_parts.append(
            f'<a class="{classes}" href="{escape(relative_href(current_dir, target))}">'
            f'{escape(book["title"])}</a>'
        )
    for locale_item in SITE_LOCALES:
        target = localized_book_target(current_slug, current_page, locale_item["code"])
        classes = "hb-site-switcher__link"
        if locale_item["code"] == locale:
            classes += " is-active"
        link_parts.append(
            f'<a class="{classes}" href="{escape(relative_href(current_dir, target))}" '
            f'data-hb-locale="{escape(locale_item["code"])}">{escape(locale_item["name"])}</a>'
        )
    if current_book.get("pdf_path"):
        pdf_target = (
            str(Path(current_prefix) / current_slug / current_book["pdf_path"])
            if current_prefix
            else str(Path(current_slug) / current_book["pdf_path"])
        )
        link_parts.append(
            f'<a class="hb-site-switcher__link" href="{escape(relative_href(current_dir, pdf_target))}" download>'
            f'{escape(strings["download_pdf_label"])}</a>'
        )
    if repository_url:
        link_parts.append(
            f'<a class="hb-site-switcher__link" href="{escape(repository_url)}" target="_blank" rel="noopener noreferrer">{escape(strings["github_label"])}</a>'
        )

    links_html = "".join(link_parts)
    return (
        f'<div class="hb-site-switcher" role="navigation" aria-label="{escape(strings["switcher_aria"])}">'
        '<div class="hb-site-switcher__brand">'
        f'<p class="hb-site-switcher__eyebrow">{escape(strings["site_label"])}</p>'
        f'<p class="hb-site-switcher__title">{escape(current_book["title"])}</p>'
        "</div>"
        f'<div class="hb-site-switcher__links">{links_html}</div>'
        "</div>"
    )


def inject_switcher(
    book_publish_dir: Path,
    current_slug: str,
    books: list[dict[str, str]],
    repository_url: str,
    locale: str,
) -> None:
    for html_path in book_publish_dir.rglob("*.html"):
        if "gitbook" in html_path.parts:
            continue
        html = html_path.read_text(encoding="utf-8")
        if "hb-site-switcher" in html:
            continue
        current_page = html_path.relative_to(book_publish_dir).as_posix()
        switcher_markup = build_switcher_markup(
            current_slug, current_page, books, repository_url, locale
        )
        html = html.replace(
            'content="width=device-width, initial-scale=1, user-scalable=no"',
            'content="width=device-width, initial-scale=1, viewport-fit=cover"',
        )
        html = html.replace("</head>", f"{BOOK_SWITCHER_CSS}\n{LOCALE_SWITCH_SCRIPT}\n</head>", 1)
        html = html.replace(
            "<body>",
            f"<body>\n{switcher_markup}",
            1,
        )
        html = html.replace(
            '<div class="book honkit-cloak">',
            '<div class="book honkit-cloak with-site-switcher">',
            1,
        )
        html_path.write_text(html, encoding="utf-8")


def build_agentway_cta(book: dict[str, str], locale: str) -> str:
    strings = locale_config(locale)
    title = strings["cta_title"]
    body = strings["cta_body_book2"] if book["slug"] == "book2-comparing" else strings["cta_body_default"]
    agentway_base = "https://agentway.dev" if locale == "en" else "https://agentway.dev/zh"
    pricing_url = f"{agentway_base}/pricing"
    return (
        '<aside class="hb-agentway-cta" aria-label="Further Reading">'
        f'<p class="hb-agentway-cta__eyebrow">{escape(strings["further_reading_label"])}</p>'
        f"<h3>{escape(title)}</h3>"
        f"<p>{escape(body)}</p>"
        '<div class="hb-agentway-cta__actions">'
        f'<a class="hb-agentway-cta__link hb-agentway-cta__link--primary" href="{escape(agentway_base)}">{escape(strings["cta_primary"])}</a>'
        f'<a class="hb-agentway-cta__link" href="{escape(pricing_url)}">{escape(strings["cta_secondary"])}</a>'
        "</div>"
        "</aside>"
    )


def extract_navigation_target(html: str, direction: str) -> tuple[str, str] | None:
    match = re.search(
        rf'<a href="([^"]+)" class="navigation navigation-{direction}\s*[^"]*" aria-label="([^"]+)">',
        html,
    )
    if not match:
        return None
    href = html_unescape(match.group(1)).strip()
    aria_label = html_unescape(match.group(2)).strip()
    label = aria_label.split(":", 1)[1].strip() if ":" in aria_label else aria_label
    if not href or not label:
        return None
    return href, label


def build_inline_pager(html: str, locale: str) -> str:
    strings = locale_config(locale)
    links: list[str] = []
    prev_target = extract_navigation_target(html, "prev")
    next_target = extract_navigation_target(html, "next")

    if prev_target:
        href, label = prev_target
        links.append(
            '<a class="hb-inline-pager__link hb-inline-pager__link--prev" '
            f'href="{escape(href)}">'
            f'<span class="hb-inline-pager__eyebrow">{escape(strings["prev_label"])}</span>'
            f'<span class="hb-inline-pager__title">{escape(label)}</span>'
            "</a>"
        )

    if next_target:
        href, label = next_target
        links.append(
            '<a class="hb-inline-pager__link hb-inline-pager__link--next" '
            f'href="{escape(href)}">'
            f'<span class="hb-inline-pager__eyebrow">{escape(strings["next_label"])}</span>'
            f'<span class="hb-inline-pager__title">{escape(label)}</span>'
            "</a>"
        )

    if not links:
        return ""
    return '<nav class="hb-inline-pager" aria-label="Chapter navigation">' + "".join(links) + "</nav>"


def build_endcap(html: str, book: dict[str, str], locale: str) -> str:
    pager = build_inline_pager(html, locale)
    cta = build_agentway_cta(book, locale)
    return f'<div class="hb-endcap">{pager}{cta}</div>'


def inject_agentway_cta(book_publish_dir: Path, book: dict[str, str], locale: str) -> None:
    for html_path in book_publish_dir.rglob("*.html"):
        if "gitbook" in html_path.parts:
            continue
        html = html_path.read_text(encoding="utf-8")
        endcap = build_endcap(html, book, locale)
        if '<div class="hb-endcap">' in html:
            html = re.sub(
                r'<div class="hb-endcap">.*?</div>',
                endcap,
                html,
                count=1,
                flags=re.S,
            )
            html_path.write_text(html, encoding="utf-8")
            continue
        if '<aside class="hb-agentway-cta"' in html:
            html = re.sub(
                r'<aside class="hb-agentway-cta" aria-label="[^"]*">.*?</aside>',
                endcap,
                html,
                count=1,
                flags=re.S,
            )
            html_path.write_text(html, encoding="utf-8")
            continue
        html = html.replace(
            "</section>\n                            \n    </div>\n    <div class=\"search-results\">",
            f"</section>\n{endcap}\n                            \n    </div>\n    <div class=\"search-results\">",
            1,
        )
        html_path.write_text(html, encoding="utf-8")


def extract_body_h1_text(html: str) -> str | None:
    match = re.search(
        r'<section class="normal markdown-section">.*?<h1[^>]*>(.*?)</h1>',
        html,
        re.S,
    )
    if not match:
        return None
    text = re.sub(r"<[^>]+>", "", match.group(1))
    text = html_unescape(text).strip()
    return re.sub(r"\s+", " ", text) or None


def sync_page_titles(book_publish_dir: Path, book: dict[str, str]) -> None:
    for html_path in book_publish_dir.rglob("*.html"):
        if "gitbook" in html_path.parts:
            continue
        html = html_path.read_text(encoding="utf-8")
        body_h1 = extract_body_h1_text(html)
        if not body_h1:
            continue
        browser_title = body_h1 if body_h1 == book["title"] else f"{body_h1} · {book['title']}"
        html = re.sub(
            r"(<div class=\"book-header\".*?<h1>\s*<i[^>]*></i>\s*<a href=\"\.\"[^>]*>)(.*?)(</a>)",
            lambda match: f"{match.group(1)}{escape(body_h1)}{match.group(3)}",
            html,
            count=1,
            flags=re.S,
        )
        html = re.sub(
            r"<title>.*?</title>",
            f"<title>{escape(browser_title)}</title>",
            html,
            count=1,
            flags=re.S,
        )
        html_path.write_text(html, encoding="utf-8")


def inject_social_meta(
    html: str,
    *,
    page_title: str,
    description: str,
    page_url: str,
    image_url: str,
    image_alt: str,
) -> str:
    html = re.sub(
        r'<meta name="description" content="[^"]*"\s*/?>',
        f'<meta name="description" content="{escape(description)}">',
        html,
        count=1,
    )
    meta_block = f"""
    <link rel="canonical" href="{escape(page_url)}">
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="Harness Books">
    <meta property="og:title" content="{escape(page_title)}">
    <meta property="og:description" content="{escape(description)}">
    <meta property="og:url" content="{escape(page_url)}">
    <meta property="og:image" content="{escape(image_url)}">
    <meta property="og:image:alt" content="{escape(image_alt)}">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{escape(page_title)}">
    <meta name="twitter:description" content="{escape(description)}">
    <meta name="twitter:image" content="{escape(image_url)}">
    <meta name="twitter:image:alt" content="{escape(image_alt)}">
""".rstrip()
    return html.replace("</head>", f"{meta_block}\n</head>", 1)


def inject_json_ld(html: str, payload: dict) -> str:
    script = (
        '<script type="application/ld+json">'
        f'{json.dumps(payload, ensure_ascii=False)}'
        "</script>"
    )
    return html.replace("</head>", f"{script}\n</head>", 1)


def chapter_label_from_title(page_title: str, book_title: str) -> str:
    suffix = f" · {book_title}"
    if page_title.endswith(suffix):
        return page_title[: -len(suffix)].strip()
    return page_title.strip()


def inject_book_social_meta(
    book_publish_dir: Path,
    book: dict[str, str],
    site_url: str,
    dist_dir: Path,
) -> None:
    description = book.get("lede") or book.get("description") or book["title"]
    book_root = (
        f'{book["locale_prefix"]}/{book["slug"]}/'
        if book["locale_prefix"]
        else f'{book["slug"]}/'
    )
    for html_path in book_publish_dir.rglob("*.html"):
        if "gitbook" in html_path.parts:
            continue
        html = html_path.read_text(encoding="utf-8")
        title_start = html.find("<title>")
        title_end = html.find("</title>", title_start + 7)
        page_title = book["title"]
        if title_start != -1 and title_end != -1:
            page_title = html[title_start + 7:title_end].strip()
        if 'property="og:title"' in html or 'name="twitter:title"' in html:
            continue
        relative_html = html_path.relative_to(dist_dir).as_posix()
        page_dir = relative_html.rsplit("/", 1)[0] if "/" in relative_html else ""
        stem = Path(relative_html).stem
        page_url = join_public_url(
            site_url,
            book_root if stem == "index" else relative_html,
        )
        og_relative = f"{OG_DIRNAME}/{book['slug']}/{safe_stem(stem)}.svg"
        write_og_image(
            dist_dir,
            og_relative,
            build_og_svg(
                eyebrow=book["kicker"] or "Harness Books",
                title=page_title,
                subtitle=book["title"],
                footer="HARNESS BOOKS / ZEN EDITION",
                accent_mode="single" if book["slug"] == "book1-claude-code" else "split",
            ),
        )
        html = inject_social_meta(
            html,
            page_title=page_title,
            description=description,
            page_url=page_url,
            image_url=join_public_url(site_url, og_relative),
            image_alt=f"{book['title']} {locale_config(book['locale'])['book_cover_alt_suffix']}",
        )
        html = inject_json_ld(
            html,
            {
                "@context": "https://schema.org",
                "@type": "TechArticle",
                "headline": page_title,
                "description": description,
                "url": page_url,
                "image": join_public_url(site_url, og_relative),
                "isPartOf": {
                    "@type": "Book",
                    "name": book["title"],
                    "url": join_public_url(site_url, book_root),
                },
                "author": {
                    "@type": "Organization",
                    "name": "AgentWay",
                    "url": "https://agentway.dev",
                },
            },
        )
        html = inject_json_ld(
            html,
            {
                "@context": "https://schema.org",
                "@type": "Book",
                "name": book["title"],
                "url": join_public_url(site_url, book_root),
                "description": book.get("description", ""),
                "author": {
                    "@type": "Organization",
                    "name": "AgentWay",
                    "url": "https://agentway.dev",
                },
            },
        )
        html = inject_json_ld(
            html,
            {
                "@context": "https://schema.org",
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": 1,
                        "name": "Harness Books",
                        "item": join_public_url(site_url, ""),
                    },
                    {
                        "@type": "ListItem",
                        "position": 2,
                        "name": book["title"],
                        "item": join_public_url(site_url, book_root),
                    },
                    {
                        "@type": "ListItem",
                        "position": 3,
                        "name": chapter_label_from_title(page_title, book["title"]),
                        "item": page_url,
                    },
                ],
            },
        )
        html_path.write_text(html, encoding="utf-8")


def make_index_html(books: list[dict[str, str]], repository_url: str, locale: str) -> str:
    strings = locale_config(locale)
    current_prefix = locale_prefix(locale)
    cards = []
    for index, book in enumerate(books, start=1):
        facts_html = "".join(
            f"<span>{escape(fact)}</span>" for fact in book.get("facts", ())
        )
        pdf_action = ""
        if book.get("pdf_path"):
            pdf_target = (
                f'{book["slug"]}/{book["pdf_path"]}'
            )
            pdf_action = (
                f'<a class="button button--secondary" '
                f'href="{escape(pdf_target)}" download>'
                f'{escape(strings["download_pdf_label"])}</a>'
            )
        cards.append(
            f"""
<article class="book-card">
  <div class="book-card__cover-wrap">
    <img class="book-card__cover" src="{escape(book["cover"])}" alt="{escape(book["title"])} {escape(strings["book_cover_alt_suffix"])}" loading="lazy">
  </div>
  <div class="book-card__body">
    <div class="book-card__meta">
      <span>Book {index:02d}</span>
      <span>{escape(book["slug"])}</span>
    </div>
    <p class="book-card__kicker">{escape(book["kicker"])}</p>
    <div>
    <h2>{escape(book["title"])}</h2>
    </div>
    <p class="book-card__lede">{escape(book["lede"])}</p>
    <div class="book-card__facts">{facts_html}</div>
    <p class="book-card__summary">{escape(book["summary"])}</p>
    <div class="book-card__actions">
      <a class="button button--primary" href="{escape(book["slug"])}/">{escape(strings["read_online_label"])}</a>
      <a class="button button--secondary" href="{escape(book["slug"])}/index.html">{escape(strings["toc_label"])}</a>
      {pdf_action}
    </div>
  </div>
</article>
""".strip()
        )

    cards_html = "\n".join(cards)
    language_links = []
    current_dir = current_prefix or "."
    for item in SITE_LOCALES:
        target = f'{item["prefix"]}/index.html' if item["prefix"] else "index.html"
        classes = "button button--secondary"
        if item["code"] == locale:
            classes = "button button--primary"
        language_links.append(
            f'<a class="{classes}" href="{escape(relative_href(current_dir, target))}" '
            f'data-hb-locale="{escape(item["code"])}">{escape(item["name"])}</a>'
        )
    language_switch = "".join(language_links)
    return f"""<!DOCTYPE html>
<html lang="{escape(strings["root_lang"])}" data-locale="{escape(locale)}"{' data-hb-autodetect="1"' if locale == 'zh-Hans' else ''}>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{escape(strings["root_title"])}</title>
  <meta name="description" content="{escape(strings["root_description"])}">
  {SITE_INDEX_CSS}
  {LOCALE_SWITCH_SCRIPT}
</head>
<body>
  <main class="site-shell">
    <section class="hero">
      <p class="hero__eyebrow">{escape(strings["hero_eyebrow"])}</p>
      <h1>{escape(strings["hero_title"])}</h1>
      <div class="seo-block__actions">
        {language_switch}
        <a class="button button--secondary" href="{escape(repository_url)}" target="_blank" rel="noopener noreferrer">{escape(strings["repo_button"])}</a>
      </div>
    </section>
    <section class="library" aria-label="Official books">
      {cards_html}
    </section>
    <section class="seo-sections" aria-label="Harness engineering guide">
      <article class="seo-block">
        <h3>{escape(strings["seo_what"])}</h3>
        <p>{escape(strings["seo_what_body"])}</p>
      </article>
      <article class="seo-block">
        <h3>{escape(strings["seo_learn"])}</h3>
        <p>{escape(strings["seo_learn_body"])}</p>
      </article>
      <article class="seo-block">
        <h3>{escape(strings["seo_agentway"])}</h3>
        <p>{escape(strings["seo_agentway_body"])}</p>
        <div class="seo-block__actions">
          <a class="button button--primary" href="{escape('https://agentway.dev' if locale == 'en' else 'https://agentway.dev/zh')}">{escape(strings["cta_primary"])}</a>
          <a class="button button--secondary" href="{escape(('https://agentway.dev' if locale == 'en' else 'https://agentway.dev/zh') + '/pricing')}">{escape(strings["cta_secondary"])}</a>
        </div>
      </article>
    </section>
    <p class="footer-note">{escape(strings["footer_note"])}</p>
  </main>
</body>
</html>
"""


def write_root_files(
    dist_dir: Path,
    books: list[dict[str, str]],
    site_url: str,
    custom_domain: str,
    repository_url: str,
    locale: str,
) -> None:
    strings = locale_config(locale)
    prefix = locale_prefix(locale)
    locale_dir = dist_dir if not prefix else dist_dir / prefix
    locale_dir.mkdir(parents=True, exist_ok=True)
    index_html = make_index_html(books, repository_url, locale)
    root_og_relative = f"{OG_DIRNAME}/{'site-home' if not prefix else f'site-home-{prefix}'}.svg"
    write_og_image(
        dist_dir,
        root_og_relative,
        build_og_svg(
            eyebrow="Harness Books",
            title="Harness Engineering 的两条阅读路径" if locale == "zh-Hans" else "Two Reading Paths into Harness Engineering",
            subtitle="Claude Code / Codex / Control Plane / Recovery / Policy",
            footer=strings["og_footer_home"],
            accent_mode="split",
        ),
    )
    index_html = inject_social_meta(
        index_html,
        page_title=strings["root_title"],
        description=strings["root_description"],
        page_url=join_public_url(site_url, f"{prefix}/" if prefix else ""),
        image_url=join_public_url(site_url, root_og_relative),
        image_alt=f'{strings["root_title"]} preview',
    )
    index_html = inject_json_ld(
        index_html,
        {
            "@context": "https://schema.org",
            "@type": "WebSite",
            "name": strings["root_title"],
            "url": join_public_url(site_url, f"{prefix}/" if prefix else ""),
            "description": strings["root_description"],
            "publisher": {
                "@type": "Organization",
                "name": "AgentWay",
                "url": "https://agentway.dev",
            },
        },
    )
    (locale_dir / "index.html").write_text(index_html, encoding="utf-8")
    if not prefix:
        (dist_dir / ".nojekyll").write_text("", encoding="utf-8")
    if custom_domain and not prefix:
        (dist_dir / "CNAME").write_text(custom_domain + "\n", encoding="utf-8")
        robots_body = "User-agent: *\nAllow: /\nSitemap: " + join_public_url(site_url, "sitemap.xml") + "\n"
        (dist_dir / "robots.txt").write_text(robots_body, encoding="utf-8")


def write_sitemap(dist_dir: Path, site_url: str) -> None:
    if not site_url:
        return
    urls = collect_site_urls(dist_dir)
    body = "\n".join(
        f"  <url><loc>{escape(join_public_url(site_url, url))}</loc></url>"
        for url in urls
    )
    sitemap = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{body}\n"
        "</urlset>\n"
    )
    (dist_dir / "sitemap.xml").write_text(sitemap, encoding="utf-8")


def main() -> None:
    args = parse_args()
    dist_dir = Path(args.dist_dir).resolve()
    site_url = normalize_site_url(args.site_url)
    custom_domain = args.custom_domain.strip()
    repository_url = args.repository_url.strip()

    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    dist_dir.mkdir(parents=True, exist_ok=True)

    for locale_item in SITE_LOCALES:
        locale = locale_item["code"]
        prefix = locale_item["prefix"]
        books = [load_book_metadata(REPO_ROOT / slug, locale) for slug in BOOK_DIRS]

        for book in books:
            book_dir = REPO_ROOT / book["slug"]
            base_dir = dist_dir if not prefix else dist_dir / prefix
            target_dir = base_dir / book["slug"]
            copy_book_output(book_dir, target_dir, locale)
            inject_switcher(target_dir, book["slug"], books, repository_url, locale)
            inject_agentway_cta(target_dir, book, locale)
            sync_page_titles(target_dir, book)
            inject_book_social_meta(target_dir, book, site_url, dist_dir)

        write_root_files(dist_dir, books, site_url, custom_domain, repository_url, locale)
    write_sitemap(dist_dir, site_url)


if __name__ == "__main__":
    main()
