---
id: TASK-030
type: implementation
status: done
updated: 2026-08-30
task: PHASE-1/TASK-030
deviation: minor
files_changed: 4
---

## Changes

**C1 — the amended obligation rule** (`scripts/check-envelopes.py`). `SCOPE` gains `PROJECT`, so the
exactly-one-of message now reads `TASK/PHASE/BUG/PROJECT`. Two new constants name the two sides of
D-027: `MANDATES_CONDITIONAL = {TASK, BUG}` and `FORBIDS_CONDITIONAL = {PHASE, PROJECT}`. The
conditional check moved inside the `else` of the scope-count branch, so with zero or two scope keys
the class is undecidable and no conditional verdict is emitted — the scope problem is the whole
report. The all-or-nothing message `partial conditional class — missing …` is replaced by two
scope-keyed messages: `missing <fields> — mandatory under <SCOPE>` and
`<fields> must be omitted under <SCOPE>`. `check(step, fields)` keeps its signature and inputs; no
file is read, no field value is inspected.

**C1 — the docstring.** The four-class summary now states the scope-keyed rule and that a present
conditional field under `PHASE`/`PROJECT` is forbidden, not merely unnecessary (§5.5). A new
`DELIBERATELY NOT CHECKED` paragraph records that §5.5 row 4's `EXPERTISE`-when-`expertise`-is-empty
omission is scoped out, why (the fact lives in `modules.md`, not the envelope; the two rejected
alternatives), and the exact condition to revisit under — the first module registered with an empty
`expertise` cell.

**C2 — the envelope** (`skills/greenfield/step-phases.md`). One line, `PROJECT:   orqestra`,
immediately after `SKILL:` in the scope position. The step file learned nothing about the checker: no
marker, no exemption comment. `check-envelopes.py --verbose` now lists it conformant.

**C3 — the harness** (`scripts/test-check-envelopes.py`). 19 cases became 24. `BASE` is redefined as
`SCOPED + CONDITIONAL` — the minimum conformant dispatch under `TASK`/`BUG` — with `SCOPED` (always
class plus one scope field) and a `scoped(key)` helper for the scopes that forbid the conditional
class. Five cases added: `PROJECT is an accepted scope`, `conditional fields under PROJECT are
caught`, `conditional fields under PHASE are caught`, `missing conditional class under BUG is
caught`, `PROJECT alongside TASK is two scope fields`. The regression guards `no scope field is
caught` and `two scope fields are caught` were repaired by the `BASE` change alone; their
expectations are untouched, as are the step-specific, closed-list and duplicate cases'.

**C4 — the suite** (`.orqestra/config.md:33`). `test_command` is now
`python3 scripts/check-templates.py && python3 scripts/test-check-envelopes.py && python3
scripts/check-envelopes.py` — harness before repo scan, so the known-red scan cannot hide the harness
result. This file is outside every module's `paths`; the edit is sanctioned by TASK.md's amendment
(§8.2) on the TASK-001 precedent. `templates/config.md:38`'s `test_command` stays empty.

**Verification** (all run from the repo root):

| command | exit | result |
|---|---|---|
| `python3 scripts/test-check-envelopes.py` | 0 | 24 cases pass |
| `python3 scripts/check-envelopes.py` | **1** | 10 envelopes checked, 1 non-conformant: `skills/bugfix/step-diagnose.md:8 — missing SKILL`. **Expected and correct.** That envelope needs a `SKILL:` naming `skills/diagnose/`, which is TASK-034's. Nothing here suppresses it — no allowlist, no skip-list, no invented value |
| `python3 scripts/check-templates.py` | 0 | clean |
| `python3 scripts/check-decisions.py` | 0 | clean |
| `python3 scripts/check-step-refs.py` | 0 | clean |
| `python3 scripts/test-check-templates.py` | 0 | clean |
| `python3 scripts/test-check-step-refs.py` | 0 | clean |

## Deviations

| deviation | from design | what | why |
|---|---|---|---|
| minor | Test Strategy names the cases that change and the ones that must not; `conformant with full conditional class` appears in neither list | Repurposed it into `missing conditional class under TASK is caught` (fields `SCOPED`, expecting the mandatory-under-`TASK` message) | Under the redefined `BASE` its old fields `BASE + CONDITIONAL` become duplicates, so it could not stand unchanged. Restating it as `BASE` would have made it a byte-identical copy of `minimum conformant dispatch`. Repointing it keeps a real assertion and gives the new `…under BUG` case its `TASK`-side mirror — the case the old `minimum conformant dispatch` content becomes once `TASK` mandates the four |

## Tech Debt

`scripts/test-check-envelopes.py`'s docstring still says "today's ten envelopes", which is accurate now
but is a count that will drift as skills are added. Not fixed — unrelated to this task (D3), and the
sentence is illustrative rather than load-bearing.
