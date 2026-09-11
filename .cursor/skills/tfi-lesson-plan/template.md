# LP spreadsheet template

Match the Khansa / TFI lesson-plan sheet column model. One **row = one period** (plan each period separately).

## Columns

| # | Column | Notes |
|---|---|---|
| A | Month | e.g. September |
| B | Period No. | Plan each period separately |
| C | Date of Lesson | School days only |
| D | Concept | Single clear concept title |
| E | Sub-concept | Bullet list of micro-ideas; all must appear in flow |
| F | SKILLS (3D Blooms) | Understanding / Comparing / Identifying / Applying / Analysing (combine only if both are truly assessed) |
| G | Learning Outcome | SWBAT… one measurable outcome |
| H | Vocabulary | Short list students will use aloud/write |
| I | Opening Hook | Engage: SPARK and/or Do Now with **question stems** + time |
| J | FLOW OF THE LESSON (ALS) | Timed I DO → WE DO (GP) → YOU DO (IP); state when students solve |
| M | CFUs / Ungraded | Extracted checks + brief expected answers |
| N | Graded Formatives | Exit / IP item / HW (aligned to SWBAT) |
| O | Differentiation | Support + stretch (do not leave blank if mixed levels) |
| P | Resources & Artefacts | Board scale, textbook page, worksheets, manipulative |
| Q | Interdisciplinary / Art Integration | Optional but fill when natural |
| R–S | Teacher Reflections A1 / A2 | Post-class |
| T–V | Submission / Review / Feedback dates | As sheet requires |

Row 2 of the sheet often labels: Skills → `3D BLOOMS`, Hook → `Engage`, CFU split → `Ungraded` | `Graded Formatives`.

## Suggested timing (40-min period)

| Block | Minutes | Role |
|---|---|---|
| Do Now / Recap (if needed) | 3–8 | Activate prior knowledge / fix known struggle |
| SPARK hook | 5–8 | Create need; visual/contextual |
| I DO | 10–15 | Teacher model + embedded CFUs |
| WE DO (GP) | 8–12 | Group/partner ownership; teacher circulates |
| YOU DO (IP) | 5–8 | Independent item aligned to SWBAT |
| Exit / assign HW | 2–3 | Graded formative or simpler HW |

Adjust blocks but keep **sum ≤ 40**. If content does not fit, split the outcome across days.

## Period output shape (markdown or CSV cell text)

### Voice rules

- Continuous labels: `Asking:` `Saying:` `Writing:` `Showing:` `Drawing:` `Concluding:`
- Expected responses under `Students:`
- No coach/AI directives to the teacher

### Flow cell

```text
Main Flow: XX min

I DO:

2. INTRODUCING <IDEA>
5–6 minutes

Writing: / Showing: …
Asking:
“…”
Students:
“…”
Saying:
“…”
Writing:
…
Concluding:
“…”

WE DO – GP (N min)

Pairs/groups are … 
Moving around the groups.

YOU DO – IP (N min)

Q: <exact stem — prefer continuous: Writing… / Finding…>

Exit (N min): …
```

### Hook cell

```text
DO NOW (N min)

Q: …

SPARK – <title> (N min)

Showing / Drawing: …
Asking:
“…”
Students:
“…”
```

### CFU cell

```text
1. <question> → <expected>
2. <question> → <expected>
```

### I DO example tone (from CH3, continuous labels)

```text
Asking:

“How many equal parts are there between 3 and 4?”

Students:

“10.”

Saying:

“Each small part is one-tenth of the whole unit.”

Asking:

“How many one-tenths make one whole unit?”

Students:

“10.”

Writing:

10 one-tenths = 1 whole unit
```

## Multi-period chapter plan

When generating a full chapter:

1. List period sequence (concept titles + SWBATs) first for approval if the user wants review.
2. Then expand each period to full columns.
3. Keep a progression (introduce → represent/compare → operate → apply), matching the subject.
4. Insert revision / LBA rows only with real plans or clear assessment focus.

## CSV export headers (single header row)

```csv
Month,Period No.,Date of Lesson,Concept,Sub-concept,SKILLS,Learning Outcome,Vocabulary,Opening Hook,FLOW OF THE LESSON,CFUs Ungraded,Graded Formatives,Differentiation,Resources & Artefacts,Interdisciplinary / Art Integration,Teacher Reflections A1,Teacher Reflections A2
```
