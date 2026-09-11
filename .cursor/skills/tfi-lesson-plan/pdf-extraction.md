# PDF chapter extraction

Scripts live in [scripts/](scripts/). Use them **before** drafting an LP whenever the user provides a textbook PDF.

## Setup (once per machine)

```bash
bash ~/.cursor/skills/tfi-lesson-plan/scripts/setup_venv.sh
```

Or:

```bash
cd ~/.cursor/skills/tfi-lesson-plan/scripts
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

## Commands

Always prefer the skill venv interpreter:

```bash
PY=~/.cursor/skills/tfi-lesson-plan/scripts/.venv/bin/python
SCR=~/.cursor/skills/tfi-lesson-plan/scripts
```

### 1. Inspect the PDF

```bash
"$PY" "$SCR/list_chapters.py" "/path/to/book.pdf"
```

Shows: page count, bookmarks/outline, chapter-like text hits, text-density warning (scanned books).

### 2. Extract a chapter

By number:

```bash
"$PY" "$SCR/extract_chapter.py" "/path/to/book.pdf" --chapter 4 \
  -o ~/Downloads/ch4_extract.md --also-txt
```

By title keywords (all words must appear on the start page):

```bash
"$PY" "$SCR/extract_chapter.py" "/path/to/book.pdf" \
  --title "Expressions Letter" -o ~/Downloads/ch4_extract.md
```

By manual page range (1-based inclusive):

```bash
"$PY" "$SCR/extract_chapter.py" "/path/to/book.pdf" --pages 80-105 \
  -o ~/Downloads/ch4_extract.md
```

## Scanned / image PDFs

If `list_chapters.py` warns about low text density (common for KTBS “NOT TO BE REPUBLISHED” image books):

1. Prefer a **text** chapter PDF when available (e.g. NCERT Ganita Prakash chapter `gegp10N.pdf`).
2. Or ask the user for page numbers and still run `--pages` (may be empty).
3. Do **not** invent chapter content silently — say extraction failed and use a text source.

## Agent workflow

1. Run `list_chapters.py` on the user PDF.
2. Run `extract_chapter.py` to `~/Downloads/` or the project folder.
3. Read the extract; ground the LP in its examples, exercises, and section order.
4. Cite textbook example names/pages in hooks and I DO scripts.
