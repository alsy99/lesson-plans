#!/usr/bin/env python3
"""Extract one chapter (or page range) from a textbook PDF to markdown/text.

Examples:
  # discover markers first
  python list_chapters.py "/path/to/book.pdf"

  # by chapter number
  python extract_chapter.py "/path/to/book.pdf" --chapter 4 -o ~/Downloads/ch4.md

  # by title keywords
  python extract_chapter.py "/path/to/book.pdf" --title "Expressions using Letter" -o ch4.md

  # manual page range (1-based, inclusive)
  python extract_chapter.py "/path/to/book.pdf" --pages 80-105 -o ch4.md

  # also emit plain text
  python extract_chapter.py book.pdf --chapter 4 -o ch4.md --also-txt
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def require_pypdf():
    try:
        from pypdf import PdfReader  # noqa: F401
    except ImportError:
        print(
            "Missing pypdf. From this scripts/ folder run:\n"
            "  python3 -m venv .venv && .venv/bin/pip install -r requirements.txt\n"
            "Then use:  .venv/bin/python extract_chapter.py ...",
            file=sys.stderr,
        )
        sys.exit(1)
    from pypdf import PdfReader

    return PdfReader


START_PATTERNS = [
    # Chapter 4 / CHAPTER 4: Title
    re.compile(r"(?im)^\s*chapter\s+{num}\b[:\.\s\-–—]*(?P<title>.*)$"),
    re.compile(r"(?im)^\s*ch\.?\s*{num}\b[:\.\s\-–—]*(?P<title>.*)$"),
    re.compile(r"(?im)^\s*unit\s+{num}\b[:\.\s\-–—]*(?P<title>.*)$"),
    # 4. Title at line start (weaker)
    re.compile(r"(?im)^\s*{num}\s*[\.\:\-–—]\s+(?P<title>[A-Z].{5,100})$"),
]

NEXT_PATTERNS = [
    re.compile(r"(?im)^\s*chapter\s+{num}\b"),
    re.compile(r"(?im)^\s*ch\.?\s*{num}\b"),
    re.compile(r"(?im)^\s*unit\s+{num}\b"),
]


def page_text(page) -> str:
    try:
        return page.extract_text() or ""
    except Exception:
        return ""


def compile_start(num: int):
    return [re.compile(p.pattern.format(num=num), p.flags) for p in START_PATTERNS]


def compile_next(num: int):
    return [re.compile(p.pattern.format(num=num), p.flags) for p in NEXT_PATTERNS]


def find_title_hits(reader, keywords: list[str], limit: int | None = None):
    keys = [k.lower() for k in keywords if k.strip()]
    hits = []
    n = len(reader.pages) if limit is None else min(len(reader.pages), limit)
    for i in range(n):
        t = page_text(reader.pages[i])
        low = t.lower()
        if all(k in low for k in keys):
            hits.append(i)
    return hits


def find_chapter_start(reader, chapter: int) -> tuple[int | None, str]:
    pats = compile_start(chapter)
    title = ""
    for i, page in enumerate(reader.pages):
        t = page_text(page)
        for pat in pats:
            m = pat.search(t)
            if m:
                title = (m.groupdict().get("title") or "").strip(" -:.\n\t")
                return i, title
    return None, ""


def find_chapter_end(reader, start_idx: int, chapter: int) -> int:
    """Return exclusive end page index (next chapter start, or EOF)."""
    next_num = chapter + 1
    pats = compile_next(next_num)
    for i in range(start_idx + 1, len(reader.pages)):
        t = page_text(reader.pages[i])
        for pat in pats:
            if pat.search(t):
                return i
    return len(reader.pages)


def parse_pages(spec: str, n_pages: int) -> tuple[int, int]:
    """Return 0-based [start, end_exclusive) from 1-based inclusive spec like 80-105 or 80."""
    spec = spec.strip()
    if "-" in spec:
        a, b = spec.split("-", 1)
        start_1, end_1 = int(a), int(b)
    else:
        start_1 = end_1 = int(spec)
    if start_1 < 1 or end_1 < start_1 or end_1 > n_pages:
        raise ValueError(f"Invalid --pages {spec} for PDF with {n_pages} pages")
    return start_1 - 1, end_1


def extract_range(reader, start: int, end_excl: int) -> tuple[str, dict]:
    parts = []
    chars = 0
    thin = 0
    for i in range(start, end_excl):
        t = page_text(reader.pages[i])
        chars += len(t.strip())
        if len(t.strip()) < 40:
            thin += 1
        parts.append(f"\n\n---\n<!-- PDF page {i + 1} -->\n\n{t.rstrip()}\n")
    meta = {
        "pages": end_excl - start,
        "chars": chars,
        "thin_pages": thin,
        "start_page": start + 1,
        "end_page": end_excl,
    }
    return "".join(parts).strip() + "\n", meta


def outline_chapter_range(reader, chapter: int | None, title_keys: list[str] | None):
    """Try bookmarks: return (start0, end_excl, title) or None."""
    outline = reader.outline or []
    flat = []

    def walk(items, depth=0):
        for it in items:
            if isinstance(it, list):
                walk(it, depth + 1)
                continue
            title = getattr(it, "title", None) or str(it)
            try:
                page = reader.get_destination_page_number(it)
            except Exception:
                page = None
            flat.append((depth, title, page))

    walk(outline)
    if not flat:
        return None

    def match(title: str) -> bool:
        low = title.lower()
        if chapter is not None:
            if re.search(rf"\bchapter\s*{chapter}\b", low) or re.search(
                rf"\bch\.?\s*{chapter}\b", low
            ):
                return True
            if re.match(rf"^\s*{chapter}[\s\.:\-–—]", low):
                return True
        if title_keys:
            return all(k.lower() in low for k in title_keys)
        return False

    idxs = [i for i, (_, title, page) in enumerate(flat) if page is not None and match(title)]
    if not idxs:
        return None
    i = idxs[0]
    _, title, start = flat[i]
    end = len(reader.pages)
    for j in range(i + 1, len(flat)):
        d, _, page = flat[j]
        if page is None:
            continue
        if d <= flat[i][0]:
            end = page
            break
    return start, end, title


def main() -> int:
    ap = argparse.ArgumentParser(description="Extract a textbook chapter from PDF")
    ap.add_argument("pdf", type=Path)
    ap.add_argument("--chapter", type=int, help="Chapter/unit number")
    ap.add_argument(
        "--title",
        type=str,
        help='Title keywords (space-separated ANDed), e.g. "Expressions Letter"',
    )
    ap.add_argument("--pages", type=str, help="Manual 1-based inclusive range, e.g. 80-105")
    ap.add_argument("-o", "--output", type=Path, help="Output .md path (default: stdout)")
    ap.add_argument("--also-txt", action="store_true", help="Also write .txt next to .md")
    ap.add_argument(
        "--scan-limit",
        type=int,
        default=0,
        help="For --title, only search first N pages for the start hit (0=all)",
    )
    args = ap.parse_args()

    if not args.pdf.exists():
        print(f"File not found: {args.pdf}", file=sys.stderr)
        return 1
    if not args.pages and args.chapter is None and not args.title:
        print("Provide --chapter, --title, and/or --pages", file=sys.stderr)
        return 1

    PdfReader = require_pypdf()
    reader = PdfReader(str(args.pdf))
    n = len(reader.pages)

    start = end_excl = None
    heading = ""

    if args.pages:
        try:
            start, end_excl = parse_pages(args.pages, n)
        except ValueError as e:
            print(str(e), file=sys.stderr)
            return 1
        heading = f"Pages {start + 1}-{end_excl}"
    else:
        # Prefer outline when possible
        title_keys = args.title.split() if args.title else None
        outlined = outline_chapter_range(reader, args.chapter, title_keys)
        if outlined:
            start, end_excl, heading = outlined
            print(f"Using outline: {heading!r} pages {start + 1}-{end_excl}", file=sys.stderr)
        elif args.chapter is not None:
            start, title = find_chapter_start(reader, args.chapter)
            if start is None:
                print(
                    f"Could not find Chapter {args.chapter} text marker. "
                    f"Try: list_chapters.py or --pages / --title",
                    file=sys.stderr,
                )
                return 2
            end_excl = find_chapter_end(reader, start, args.chapter)
            heading = f"Chapter {args.chapter}" + (f" — {title}" if title else "")
        else:
            keys = args.title.split()
            limit = None if args.scan_limit <= 0 else args.scan_limit
            hits = find_title_hits(reader, keys, limit)
            if not hits:
                print(f"No page contained all title keywords: {keys}", file=sys.stderr)
                return 2
            start = hits[0]
            # End at next strong chapter heading after start, else +40 pages cap heuristic
            end_excl = len(reader.pages)
            next_chap = re.compile(r"(?im)^\s*chapter\s+\d+\b")
            for i in range(start + 1, len(reader.pages)):
                if next_chap.search(page_text(reader.pages[i])):
                    end_excl = i
                    break
            # safety cap if huge
            if end_excl - start > 60:
                end_excl = start + 60
                print(
                    "WARNING: title mode capped at 60 pages; pass --pages for precision",
                    file=sys.stderr,
                )
            heading = args.title

    body, meta = extract_range(reader, start, end_excl)
    header = (
        f"# {heading}\n\n"
        f"- Source: `{args.pdf.name}`\n"
        f"- Pages: {meta['start_page']}–{meta['end_page']} "
        f"({meta['pages']} pages)\n"
        f"- Extracted characters: {meta['chars']}\n"
        f"- Low-text pages: {meta['thin_pages']}\n\n"
    )
    if meta["chars"] < 500 or meta["thin_pages"] >= max(3, meta["pages"] * 0.5):
        header += (
            "> **Warning:** Little extractable text. This PDF is likely scanned. "
            "Use a text-based chapter PDF (e.g. NCERT `gegp10N.pdf`) or OCR before planning.\n\n"
        )

    doc = header + body

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(doc, encoding="utf-8")
        print(f"Wrote {args.output} ({meta['chars']} chars, pages {meta['start_page']}-{meta['end_page']})")
        if args.also_txt:
            txt_path = args.output.with_suffix(".txt")
            # strip HTML comments for plain text
            plain = re.sub(r"<!--.*?-->", "", body, flags=re.S)
            plain = re.sub(r"\n---\n", "\n\n", plain)
            txt_path.write_text(f"{heading}\n\n{plain.strip()}\n", encoding="utf-8")
            print(f"Wrote {txt_path}")
    else:
        sys.stdout.write(doc)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
