#!/usr/bin/env python3
"""List chapter-like markers and text density for a textbook PDF.

Usage:
  python list_chapters.py "/path/to/book.pdf"
  python list_chapters.py "/path/to/book.pdf" --max-pages 40
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path


def require_pypdf():
    try:
        from pypdf import PdfReader  # noqa: F401
    except ImportError:
        print(
            "Missing pypdf. From this scripts/ folder run:\n"
            "  python3 -m venv .venv && .venv/bin/pip install -r requirements.txt\n"
            "Then use:  .venv/bin/python list_chapters.py ...",
            file=sys.stderr,
        )
        sys.exit(1)
    from pypdf import PdfReader

    return PdfReader


CHAPTER_PATTERNS = [
    re.compile(r"^\s*chapter\s+(\d+)\b[:\.\s\-–—]*(.*)$", re.I | re.M),
    re.compile(r"^\s*ch\.?\s*(\d+)\b[:\.\s\-–—]*(.*)$", re.I | re.M),
    re.compile(r"^\s*unit\s+(\d+)\b[:\.\s\-–—]*(.*)$", re.I | re.M),
    re.compile(r"(\d+)\s*\.\s*([A-Z][A-Za-z].{8,80})$", re.M),
]


def page_text(page) -> str:
    try:
        return page.extract_text() or ""
    except Exception:
        return ""


def walk_outline(reader, items=None, depth=0, rows=None):
    rows = rows if rows is not None else []
    if items is None:
        items = reader.outline or []
    for it in items:
        if isinstance(it, list):
            walk_outline(reader, it, depth + 1, rows)
            continue
        title = getattr(it, "title", None) or str(it)
        try:
            page = reader.get_destination_page_number(it) + 1
        except Exception:
            page = None
        rows.append((depth, title, page))
    return rows


def main() -> int:
    ap = argparse.ArgumentParser(description="List chapter markers in a PDF textbook")
    ap.add_argument("pdf", type=Path, help="Path to PDF")
    ap.add_argument("--max-pages", type=int, default=0, help="Only scan first N pages (0=all)")
    ap.add_argument("--min-chars", type=int, default=40, help="Min chars to treat a page as textual")
    args = ap.parse_args()

    if not args.pdf.exists():
        print(f"File not found: {args.pdf}", file=sys.stderr)
        return 1

    PdfReader = require_pypdf()
    reader = PdfReader(str(args.pdf))
    n = len(reader.pages)
    limit = n if args.max_pages <= 0 else min(n, args.max_pages)

    print(f"PDF: {args.pdf}")
    print(f"Pages: {n} (scanning {limit})")

    outline = walk_outline(reader)
    if outline:
        print("\n## Outline / bookmarks")
        for depth, title, page in outline:
            pad = "  " * depth
            pg = f"p{page}" if page else "p?"
            print(f"{pad}- {title} ({pg})")
    else:
        print("\n## Outline / bookmarks\n(none)")

    hits = []
    text_lens = []
    boilerplate = 0
    for i in range(limit):
        t = page_text(reader.pages[i])
        text_lens.append(len(t.strip()))
        low = t.lower()
        if "not to be republished" in low and len(t.strip()) < 120:
            boilerplate += 1
        for pat in CHAPTER_PATTERNS:
            for m in pat.finditer(t):
                num = m.group(1)
                title = (m.group(2) or "").strip(" -:.\n\t")
                hits.append((i + 1, num, title[:100], pat.pattern[:40]))

    print("\n## Chapter-like text hits")
    if not hits:
        print("(none found in scanned range)")
    else:
        # de-dupe by (page, num, title)
        seen = set()
        for page, num, title, _ in hits:
            key = (page, num, title.lower())
            if key in seen:
                continue
            seen.add(key)
            print(f"  p{page}: Chapter/Unit {num} — {title or '(no title on line)'}")

    nonempty = sum(1 for x in text_lens if x >= args.min_chars)
    avg = (sum(text_lens) / len(text_lens)) if text_lens else 0
    print("\n## Text density")
    print(f"  Pages with >= {args.min_chars} chars: {nonempty}/{limit}")
    print(f"  Avg chars/page (scanned): {avg:.0f}")
    print(f"  Likely boilerplate-only pages: {boilerplate}")
    if nonempty < max(3, limit * 0.05):
        print(
            "  WARNING: PDF looks mostly scanned/image-based. "
            "extract_chapter.py may return little text; use a text PDF "
            "(e.g. NCERT chapter PDF) or provide --pages after manual check."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
