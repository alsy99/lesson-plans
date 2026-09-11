---
name: tfi-lesson-plan
description: >-
  Generates Teach For India / school lesson plans in the Khansa LP spreadsheet
  format (Concept, Sub-concept, 3D Blooms, SWBAT, SPARK hook, I DO / WE DO /
  YOU DO, CFUs, graded formatives). Extracts textbook chapters from PDFs via
  scripts/list_chapters.py and scripts/extract_chapter.py. Use when creating or
  revising lesson plans, LPs, chapter plans, period plans, maths lesson sheets,
  or when the user mentions Khansa LP, ALS flow, SPARK, CFU, GP/IP, textbook
  PDF, or mentor review of lesson plans.
---

# TFI Lesson Plan Generator

Build period-level lesson plans that match the **Grade LP spreadsheet template** and pass **mentor review standards** distilled from Ashitha Sivadas comments on Khansa’s LPs.

Before writing plans, also read:
- [mentor-review-rules.md](mentor-review-rules.md) — hard rules from sheet comments
- [template.md](template.md) — column schema + period output shape
- [voice-and-script.md](voice-and-script.md) — Asking/Students dialogue voice
- [pdf-extraction.md](pdf-extraction.md) — extract chapter text from textbook PDFs

## Inputs to collect (ask only what is missing)

1. Grade, subject, chapter/unit title (and Part 1 / Part 2 names if applicable)
2. Number of periods + period length (default **40 minutes**)
3. Textbook PDF and/or curriculum notes, page refs, known student struggles
4. Calendar dates (skip weekends / no-class days unless user overrides)
5. Output form: markdown table, CSV rows, or filled sheet language

## Workflow

0. **If a textbook PDF is provided**, extract the chapter first (see [pdf-extraction.md](pdf-extraction.md)):
   - Ensure venv: `bash ~/.cursor/skills/tfi-lesson-plan/scripts/setup_venv.sh` (once)
   - Inspect: `scripts/.venv/bin/python scripts/list_chapters.py "/path/to/book.pdf"`
   - Extract: `scripts/.venv/bin/python scripts/extract_chapter.py "/path/to/book.pdf" --chapter N -o ~/Downloads/chN_extract.md --also-txt`
   - Read the extract and ground examples/exercises in the LP. If the PDF is scanned (low text), say so and use a text chapter PDF or user-provided notes — do not invent the chapter.
1. **Scope the chapter** into a period sequence. Prefer **one tight SWBAT per period**. Split fat outcomes (e.g. addition one day, subtraction next).
2. **Map prerequisites**. If prior concepts were a struggle, schedule a **2–5 min recap** before main flow (e.g. tenths↔hundredths, mixed↔improper).
3. **For each period**, fill every required column in [template.md](template.md). No empty mandatory cells.
4. **Write the flow** as timed ALS: SPARK/Do Now → I DO → WE DO (GP) → YOU DO (IP) → exit/HW. Sum of times ≤ period length. Follow [voice-and-script.md](voice-and-script.md).
5. **Align** skill (3D Blooms) ↔ SWBAT ↔ IP/graded formative. Extract CFUs from the flow into the CFU column.
6. **Self-check** against [mentor-review-rules.md](mentor-review-rules.md) before delivering.
7. Leave **Teacher Reflections** blank for post-class fill.

## Utility scripts

| Script | Purpose |
|---|---|
| [scripts/setup_venv.sh](scripts/setup_venv.sh) | Create `.venv` + install `pypdf` |
| [scripts/list_chapters.py](scripts/list_chapters.py) | Outline, chapter hits, text-density check |
| [scripts/extract_chapter.py](scripts/extract_chapter.py) | Extract chapter by `--chapter`, `--title`, or `--pages` |
| [scripts/requirements.txt](scripts/requirements.txt) | Python deps |

Execute these scripts (do not re-implement ad hoc). Full command examples: [pdf-extraction.md](pdf-extraction.md).

## Voice & scripting (required)

Plans are the **teacher’s own lesson script**, not instructions from an AI to a teacher.

1. **Continuous verb labels** in flow/hook (not bare imperatives):
   - `Writing:` / `Asking:` / `Saying:` / `Showing:` / `Drawing:` / `Concluding:`
   - Not: `Write:` / `Ask:` / `Say:` / `Conclude:` / `Tell the teacher to…`
2. **I DO = dialogue script** (CH3 style): timed mini-sections → `Asking:` + quoted question → `Students:` + expected response → `Saying:` / `Writing:` → next move. End a beat with `Concluding:` when the idea lands.
3. **No meta / coach voice**. Ban phrases like: “Teacher circulates; minimal talk”, “Lead to:”, “Emphasize that…”, “Make sure you…”, “ONE method only today”, “When: after GP”, “Remind the teacher to…”. Describe the class in continuous voice instead (`Moving around the groups.` / `Pairs are writing…`).
4. **WE DO / YOU DO** in continuous description + explicit IP question stems (gerunds in stems OK: “Writing an expression…”, “Finding the value…”).

See [template.md](template.md) for the I DO script shape.

## Pedagogical defaults (from strong CH3 plans)

- **Hook**: visual, contextual, textbook-linked when possible (food, measurement, nail/pencil-style situations). Create *need* for the concept.
- **Methods**: One primary method well per period; extras only if time remains.
- **GP (WE DO)**: Student/group ownership; teacher moves around and helps when needed (worded in script voice, not as a directive).
- **IP (YOU DO)**: Explicit question(s) aligned to SWBAT.
- **Word problems / major breakdowns**: In class, not as first homework. Breakdown steps appear inside the I DO script as Asking/Students/Writing.
- **Language**: Simple SPARK/hook prompts.

## AI usage policy (mentor expectation)

Use AI only to **sequence and word** the teacher’s own activities. Output must read as Khansa’s plan: concrete numbers, textbook refs, local context, timed Asking/Students scripts—not a generic AI lesson or a coach telling the teacher what to do.

## Output checklist (every period)

- [ ] Dates are school days; chapter/part names filled where the sheet needs them
- [ ] Concept + all sub-concepts visible and covered in the flow
- [ ] Blooms skill matches SWBAT and assessment
- [ ] Timed sections; total ≤ period length
- [ ] Recap included when prior struggle is known
- [ ] I DO is Asking:/Students:/Saying:/Writing: dialogue (continuous verbs), not coach instructions
- [ ] No meta AI-to-teacher phrasing (“Lead to”, “circulate; minimal talk”, “make sure you…”)
- [ ] YOU DO / IP question written explicitly; aligned to objective
- [ ] CFUs listed in CFU column (pulled from flow), with brief expected answers
- [ ] Graded formative / HW appropriate (no unsupported word-problem HW)
- [ ] Hook is visual/contextual; not pure lecture
- [ ] Reflections left blank for after class
