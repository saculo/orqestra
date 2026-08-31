---
id: TASK-040
type: pr
status: done
updated: 2026-08-31
task: TASK-040
branch: feat/TASK-040-bug-carries-its-module
pr_number: 12
pr_url: https://github.com/saculo/orqestra/pull/12
pr_state: open
---

## Summary

The other two thirds of the schema change TASK-037 began. `templates/BUG.md` carries `module:`,
`## Scope` stops carrying it, `step-intake.md` establishes it once, and reproduce, diagnose and
promote read the key rather than re-deriving it from the symptom. `config.md`'s stale `test_command`
comment is deleted, as its own text instructed.

**Master is green** — the window TASK-037 opened deliberately is closed. `check-templates.py` 1 → 0,
`test-check-templates.py` 3-of-15 failing → 15 of 15, all seven checkers standalone at 0, and the
`test_command` chain passing end to end.

Two rulings shaped it. **Intake never blocks**: §4.4.3 has no `blocked_reason` for an incomplete
input, and `BUG.md` — the only artifact intake writes — is precisely the file a block cannot produce.
A human is present at intake by construction. And **AC-2 is held by prose**, disclosed rather than
disguised: an empty `module:` passes `check-templates.py` and `check_instance` never globs
`work/*/BUG.md`.

## Commits

| commit | subject |
|---|---|
| `3620d77` | TASK-040: plan — the schema change, and one edge with no vocabulary for it |
| `9d9e3b5` | TASK-040: amend AC-2, settle OQ-3 and OQ-4 (§8.2) |
| `2047cb6` | TASK-040: design — the key becomes the source, and prose stops being one |
| `f742db0` | TASK-040: design gate approved |
| `0918430` | TASK-040: implement — the key is the source, and master is green |
| `b86bdcb` | TASK-040: qa — passed, 5 of 5 |
| `45830be` | TASK-040: review — passed, 0 required, 3 advisory |
| `bc57b43` | TASK-040: review gate approved |

Eight commits, `attempts: 0` — nothing was reworked.

## CI

`gh pr checks 12` at 2026-08-31: **no checks reported**. The repository has no CI workflow. No review
threads.

Every checker was run **standalone**, because `test_command` chains with `&&` and this task's headline
claim is that seven of them pass — verifying through the chain alone would be circular.

| command | result |
|---|---|
| `python3 scripts/check-templates.py` | exit 0 — **was 1** |
| `python3 scripts/test-check-templates.py` | 15 of 15, exit 0 — **was 3 failing** |
| `python3 scripts/check-envelopes.py` | 10 envelopes, exit 0 |
| `python3 scripts/test-check-envelopes.py` | 25 cases, exit 0 |
| `python3 scripts/check-step-refs.py` | 41 references, exit 0 |
| `python3 scripts/test-check-step-refs.py` | 28 cases, exit 0 |
| `python3 scripts/check-decisions.py` | 29 decisions, exit 0 |
| `config.md` `test_command` chain | **exit 0 end to end** |

The evidence that matters is not the table. A red-to-green task invites the question of whether the
checks stopped looking, so qa probed in a throwaway `master` worktree: empty `module:` → exit 0,
`module: plugin` → exit 0, extra key `foo:` → **exit 1**. So the green proves the key **set** matches
§4.8.1 **in both directions**, and proves nothing about a value — recorded as a limit rather than
implied. AC-4's green was explicitly refused as evidence and replaced with a trace.

`check-templates.py --target .orqestra` still exits 1. Confirmed pre-existing by worktree diff —
output byte-identical but for `checked 167 → 170`, zero `BUG` mentions — and spanning TASK-001…
TASK-010, not the two artifacts `IMPLEMENTATION.md` claims (F-1).

## Advisory findings

**F-1** the two-vs-nineteen figure · **F-2** `step-intake.md:34-35`'s abandonment branch has no shape
in `## Report` · **F-3** `step-diagnose.md:64` instructs a `MODULE` line in a gate block that does not
contain one, and the block is what gets copied.
