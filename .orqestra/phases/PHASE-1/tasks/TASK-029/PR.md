---
id: TASK-029
type: pr
status: done
updated: 2026-08-30
task: TASK-029
branch: feat/TASK-029-project-wide-dispatch-scope
pr_number: 7
pr_url: https://github.com/saculo/orqestra/pull/7
pr_state: open
---

## Summary

§5.5's obligation table required exactly one of `TASK` `PHASE` `BUG` on every envelope, but
`create-phases` builds *all* of a project's phases from the PRD — no such unit exists, so no value
could satisfy the rule. `check-envelopes.py` had been correctly reporting a violation against a rule
that was itself wrong.

Two rows amended, nothing renumbered. The scope row gains `PROJECT`, whose value is the project name
from `config.md`, so a dispatch composed before any scope unit exists can conform without inventing
one. The conditional row now keys off the **scope key** — mandatory iff `TASK` or `BUG`, must be
omitted under `PHASE` and `PROJECT` — instead of stating a rule and listing its exceptions by step
name. That is one lookup, which is what AC-1 required, and it is what makes F-4 close generically:
`close-phase` and `add-phase/step-define-phase.md` are reached without either being named.

Recorded as **D-027**. F-3 fixed where it pointed.

## Commits

| commit | subject |
|---|---|
| `027d9b8` | TASK-029: plan — amend §5.5's two rows in place, no renumbering |
| `5aa8034` | TASK-029: amend AC-2 and AC-3 by human decision (§8.2) |
| `4e6f998` | TASK-029: design — PROJECT is the fourth scope value |
| `161d7bc` | TASK-029: design gate approved |
| `1892ee5` | TASK-029: implement — blocked, the docs engineer cannot edit |
| `7f8816f` | TASK-029: implement — still blocked, agent definitions are a startup snapshot |
| `525a74c` | TASK-029: implement — §5.5 admits PROJECT, and the scope key decides |
| `d08ae3e` | TASK-029: qa — passed, 3 of 3 |
| `d152dac` | TASK-029: review — changes-requested, F-1 on the module boundary |
| `44f1fcc` | TASK-029: rework — F-1 re-attributed, F-2 closed |
| `ed86950` | TASK-029: review round 2 — passed, 0 required |
| `2774590` | TASK-029: review gate approved |

Twelve commits, and the two blocked ones are kept deliberately: they record that implement was
prevented twice by the environment rather than failing. `attempts` is **0** — nothing the engineer
produced was ever reworked. The prerequisite that unblocked it, `agents/architect.md` gaining `Edit`
and `Bash`, is **not** in this branch: it landed on `master` as `81d4139` after review found it
outside the `docs` module's paths.

## CI

`gh pr checks 7` at 2026-08-30: **no checks reported**. The repository has no CI workflow, so this is
absence rather than pending. No review threads on the PR.

| command | result |
|---|---|
| `python3 scripts/check-templates.py` | 21 of 22 catalogue rows, all conform, exit 0 |
| `python3 scripts/check-decisions.py` | 27 decisions, 0 findings, exit 0 |
| `python3 scripts/check-step-refs.py` | 40 references, 0 findings, exit 0 |
| `python3 scripts/test-check-templates.py` | 15 cases, 15 pass, exit 0 |
| `python3 scripts/test-check-step-refs.py` | 28 cases, 28 pass, exit 0 |
| `python3 scripts/test-check-envelopes.py` | 19 cases, 19 pass, exit 0 |
| `python3 scripts/check-envelopes.py` | **exit 1** on `greenfield/step-phases.md` — expected; TASK-030 applies this amendment (D-019) |

The verification that carries weight is not in that table. A spec change has no behaviour to execute,
so qa transcribed the amended rule into a throwaway harness and ran it over the ten real envelopes
and eight fixtures. `TASK`-scoped with all four module fields dropped → violation; with only
`EXPERTISE` dropped → violation; `BUG`-scoped with all four dropped → violation. The widening reaches
only the `PHASE`/`PROJECT` side, so nothing the checker catches today becomes legal. That harness
could not be committed — `scripts/` is the `plugin` module (D14) — so review re-derived every
criterion by hand against the same ten envelopes rather than accept the narrative.
