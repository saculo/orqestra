---
id: TASK-024
type: implementation
status: done
updated: 2026-08-29
task: TASK-024
deviation: minor
files_changed: 8
---

## Changes

Built in the order `DESIGN.md` prescribes: **the checker first, watched failing, before a single
reference was corrected.** A checker first seen passing is one whose discrimination was never
demonstrated, which is the defect TASK-008 closed in a neighbouring file.

**Before — `scripts/check-step-refs.py` on the unfixed tree:**

```
checked 40 step references against D-026
✘ 9 unresolved or misshapen
```

All nine were `missing — no file at …`. Same command after the corrections:

```
checked 40 step references against D-026
✔ every step reference resolves, in the shape its location dictates
```

The reference total is **40 before and after**. That number holding is the evidence that the
corrections rewrote references rather than removing them — a fix that deleted a reference would
also turn the check green.

**`scripts/check-step-refs.py`** (new, CPython 3 stdlib only, mode 644). Walks every `.md` under
`skills/`, extracts inline-code spans, keeps those matching
`(${CLAUDE_PLUGIN_ROOT}/)?(dir/)*step-<name>.md` entirely, and resolves each against the rule
D-026 gives for its location. Fenced blocks and HTML comments are blanked line-for-line before
scanning, so line numbers in findings stay true to the file on disk. Exits 0/1/2.

**The nine corrections**, each in the shape its location dictates (D-026):

| file | sites | shape applied |
|---|---|---|
| `skills/add-phase/SKILL.md` | 2 index cells, 1 prose line | `${CLAUDE_PLUGIN_ROOT}/…` in cells, plugin-relative in prose |
| `skills/bugfix/SKILL.md` | 1 index cell, 1 prose line | same |
| `skills/implement/SKILL.md` | 2 prose lines | `skills/task/step-push.md` |
| `skills/qa/SKILL.md` | 1 prose line | `skills/task/step-push.md` |

The `step-push.md` references are worth naming separately: they were bare filenames pointing at a
file in `skills/task/`, so they resolved against `skills/implement/` and `skills/qa/` and silently
named files that have never existed. Not a typo — a shape error, which is why D-026 governs shape
and not merely existence.

**Two stale ownership lines**, both made false by this change rather than pre-existing:
`skills/greenfield/step-plan-design.md:3` and `skills/greenfield/SKILL.md:42` each claimed the step
is shared with `add-phase` alone. Both now name `bugfix` too. The second was **not** in the plan's
open question 3 — it was found by grepping for who actually references each shared step, rather than
trusting the one line the plan had spotted.

**`scripts/test-check-step-refs.py`** (new, mode 644). 23 cases in five groups: what counts as a
reference, the six categories that must never be flagged, existence, D-026's two shapes, and
direction. Follows `test-check-envelopes.py`'s precedent — imports the checker by
`importlib.util.spec_from_file_location` for unit-level cases, and drives it by `subprocess` over a
throwaway `shutil.copytree` of the repo for end-to-end ones.

**Evidence the suite discriminates.** The checker was run against `git archive master skills` — the
pre-fix tree — and reports **9 findings, exit 1**. The green run on the fixed tree is therefore a
result, not a property of a check that cannot fail.

The case that carries the most weight is the direction one, which the design named as the only thing
catching the inversion trap: delete `skills/greenfield/step-plan-design.md` from a copy and require
that **both** `add-phase/SKILL.md` and `bugfix/SKILL.md` appear in the output. A checker that listed
`step-*.md` files and confirmed they exist would pass that tree in silence. Its companion asserts the
converse — an orphan `step-orphan.md` that nothing references is **not** a finding, because nothing
points at it and nothing can rot.

Tests: `check-templates.py`, `check-decisions.py`, `check-step-refs.py`, `test-check-templates.py`,
`test-check-envelopes.py`, `test-check-step-refs.py` — all exit 0. `check-envelopes.py` exits 1 on
two envelopes owned by TASK-030; untouched and expected.

## Deviations

| deviation | from design | what | why |
|---|---|---|---|
| minor | scope of the stale-line fix | `DESIGN.md` inherited the plan's open question 3, which named one stale ownership line. Two were corrected — `skills/greenfield/SKILL.md:42` as well | The second makes exactly the same claim and is falsified by exactly the same change. Fixing one and leaving the other would ship a file contradicting itself, and the criterion the human widened (Q1) was about references being right, not about a line count |
| minor | build continuity | The step was dispatched to a subagent that reached the API spend limit after writing the checker and before correcting any reference. The remaining work was completed in the orchestrator session against the same design | Recorded because the dispatch record and the authorship differ, not because the work changed. The checker as committed is the subagent's; the corrections, the harness and this artifact are not. Nothing was re-derived — the design was already approved and unchanged |

## Tech Debt

- **`scripts/` file modes are inconsistent.** `check-envelopes.py` is 755; the other six, including
  both files added here, are 644. Every one is invoked as `python3 scripts/…`, so 644 is the
  majority and the mode is decorative — but the odd one out should be settled rather than copied.
  Already recorded under TASK-019; repeated here because a seventh file has now inherited the
  choice.
- **Nothing runs the checkers automatically.** `config.md`'s `test_command` is
  `check-templates.py` alone, so the other six pass only when someone remembers. There are now
  three checkers and three harnesses; a single entry point would be worth more than a seventh
  script.
- **`check-step-refs.py` covers `skills/` only.** A reference written into `agents/` or
  `templates/` is unscanned. No such reference exists today, and widening the walk risks the false
  positives D-026's discriminator exists to avoid — but the limit is real and is not stated in the
  script's own output, which reports its total as though it were coverage.
