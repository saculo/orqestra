---
id: TASK-005
type: design
status: done
updated: 2026-08-25
task: TASK-005
decisions: []
---

## Components

The fixture, generated from the real templates so every artifact conforms:

| task | artifacts | expected stage |
|---|---|---|
| TASK-001..008 | one per stage, all `done` | created · planned · designed · implemented · verified · reviewed · pushed · delivered |
| TASK-009 | `IMPLEMENTATION.md` `status: changes-requested` | **designed** — the chain stops *before* a non-`done` artifact |
| TASK-010 | `QA.md` `result: failed` | **implemented** |
| TASK-011 | `REVIEW.md` `verdict: changes-requested` | **verified** — qa genuinely passed |
| TASK-012 | `IMPLEMENTATION.md` `status: blocked` | **blocked**, reason as headline, ranked first |
| TASK-013 | corrupted frontmatter | **unknown**, never a guess |

## Interfaces

Unchanged. `status` stays read-only.

## File Plan

| path | action | purpose |
|---|---|---|
| `skills/status/SKILL.md` | modify | Corrections the grading exposes |

## Decisions

- **Expected answers written before running.** Grading after the fact is how a plausible wrong answer
  gets accepted.
- **The fixture is generated from `templates/`**, not hand-written, so schema conformance is verified by
  `check-templates.py --target` before `status` ever sees it.

## Test Strategy

Run `status`, compare every row to the table above. Any disagreement is investigated to decide which
side is wrong — the tool or the criterion.
