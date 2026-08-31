---
id: TASK-034
type: pr
status: done
updated: 2026-08-31
task: TASK-034
branch: feat/TASK-034-diagnose-has-a-procedure
pr_number: 10
pr_url: https://github.com/saculo/orqestra/pull/10
pr_state: merged
---

## Summary

`skills/bugfix/step-diagnose.md` dispatched with no `SKILL:` because no diagnose skill existed — the
last envelope `check-envelopes.py` could not pass, and the one place D-025's composition failure
survived. Three files close it: a new `skills/diagnose/SKILL.md`, the one envelope line, and
`agents/analyst.md`'s description, which named one of the five steps it is dispatched at.

**`check-envelopes.py` exits 0 for the first time** — 10 of 10 — and `config.md`'s whole
`test_command` chain passes.

The procedure is shaped by one constraint: diagnose holds **no `Bash`** (§7.0's `step` class;
`agents/analyst.md`). Evidence comes from `BUG.md`'s recorded reproduction and from reading the code,
and step 4 is a falsification test rather than "read carefully" — which is what makes it followable
without execution rather than merely silent about it.

`root_cause_found: false` is a **done** outcome that reaches the gate, pinned in a
`status × root_cause_found` table. Mapping it to `blocked` would delete the workflow's *Investigate
further* branch.

## Commits

| commit | subject |
|---|---|
| `18145ee` | TASK-034: plan — a single-file skill on plan's shape, and one SKILL: line |
| `019af84` | TASK-034: add AC-5 by human decision (§8.2) |
| `3c32c1e` | TASK-034: design — diagnose reads, and never runs |
| `6c6cdca` | TASK-034: design gate approved |
| `1e485d6` | TASK-034: implement — diagnose has a procedure, and the suite is green |
| `b7d3aff` | TASK-034: qa — passed, 5 of 5 |
| `042aa98` | TASK-034: review — changes-requested, F-1 on a false citation |
| `6c77089` | TASK-034: rework — the citation points at authority that agrees |
| `6681746` | TASK-034: review round 2 — passed, 0 required |
| `5062fa5` | TASK-034: review gate approved, and rule 3 filed as TASK-039 |

Ten commits, `attempts: 1 of 3`.

## CI

`gh pr checks 10` at 2026-08-31: **no checks reported**. Merged as `c1d386d`. The repository has no CI workflow, so this is
absence rather than pending. No review threads.

| command | result |
|---|---|
| `python3 scripts/check-envelopes.py` | **10 of 10 envelopes, exit 0** — first time |
| `python3 scripts/check-step-refs.py` | 41 references, exit 0 — one more than before, the new skill's |
| `python3 scripts/check-templates.py` | 21 of 22 catalogue rows, exit 0 |
| `python3 scripts/check-decisions.py` | 28 decisions, exit 0 |
| `python3 scripts/test-check-envelopes.py` | 25 cases, exit 0 |
| `python3 scripts/test-check-step-refs.py` | 28 cases, exit 0 |
| `python3 scripts/test-check-templates.py` | 15 cases, exit 0 |
| `config.md` `test_command` chain | **exit 0** |

The evidence that matters is not in that table. AC-3 — `check-envelopes.py` at exit 0 — goes green the
instant the `SKILL:` line lands, whatever the named file contains, because under D-025 the value is
**invoked** rather than inspected. A stub would satisfy AC-3 and fail AC-1. So qa verified AC-1
separately by **invoking the skill**: `Skill(orqestra:diagnose)` returned the real 138-line procedure,
which is evidence the harness can load what the envelope names and which no checker in `scripts/` can
produce.

Bash-freedom was re-tested with 40 independent execution terms rather than by repeating the
orchestrator's grep — only the two prohibition lines hit.

## Follow-up filed

**TASK-039** — `bugfix/SKILL.md:103`'s "Evidence, or block" contradicts its own `step-diagnose.md:30`
and this skill's contract. Review established it predates this task and declined to fix a defect this
work did not cause; filing it beats leaving it as tech debt in two artifacts.
