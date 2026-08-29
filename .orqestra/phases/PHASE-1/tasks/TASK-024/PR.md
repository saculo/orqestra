---
id: TASK-024
type: pr
status: done
updated: 2026-08-30
task: TASK-024
branch: feat/TASK-024-referenced-step-files-exist
pr_number: 6
pr_url: https://github.com/saculo/orqestra/pull/6
pr_state: open
---

## Summary

Three step files were referenced and did not exist: `add-phase` and `bugfix` claimed to share steps
from `greenfield` but named unqualified local filenames in their index tables, so under D-007 the
orchestrator was told to read a file that was not there.

Reconnaissance found **nine** sites, not three. The six beyond the known list matter more: three
prose references to `step-push.md` in `skills/implement/` and `skills/qa/` were bare filenames
naming a file that lives in `skills/task/`, so they resolved against their own skill's directory and
pointed at files that have never existed. Shape errors, not typos.

**D-026** records the rule that makes this a convention rather than nine edits: an index cell is read
by an *invoked* skill so it carries `${CLAUDE_PLUGIN_ROOT}`; a `step-*.md` is reached by `Read` where
the token is inert, so those sites are plugin-relative (D-025). Same-skill references stay bare.

`scripts/check-step-refs.py` enforces it, using inline-code spans as the discriminator so prose can
be scanned without false positives, and walking references → filesystem so a dangling reference
cannot hide behind a file that exists.

Review passed, 0 required. F-1 was fixed at the gate rather than deferred: D-026's constraint was
overstated and contradicted ten correct `TEMPLATE:` lines.

## Commits

| commit | subject |
|---|---|
| `bfe32d7` | TASK-024: plan — qualify the rows, then check every index table |
| `94f3036` | TASK-024: design — reference shape follows how the file is loaded |
| `5bf6328` | TASK-024: design gate approved |
| `c98914a` | TASK-024: implement — every step reference resolves, in its right shape |
| `5081338` | TASK-024: qa — passed, 3 of 3 |
| `60d6c5a` | TASK-024: review — passed, 0 required |
| `2b4204c` | TASK-024: review gate approved, and D-026 corrected (F-1) |

Seven commits. The first task in this repository to run the full pipeline from an unplanned start —
preflight check (c) backfilled `plan` and `design` (§7.4.3), and both gates were answered by a human.

## CI

`gh pr checks 6` at 2026-08-30: **no checks reported**. The repository has no CI workflow, so this is
absence rather than pending. No review threads on the PR.

The suite was run by hand before push:

| command | result |
|---|---|
| `python3 scripts/check-step-refs.py` | 40 references, 0 findings, exit 0 — **9 findings on pre-fix `master`** |
| `python3 scripts/test-check-step-refs.py` | 28 cases, 28 pass, exit 0 |
| `python3 scripts/check-templates.py` | 21 of 22 catalogue rows, all conform, exit 0 |
| `python3 scripts/check-decisions.py` | 26 decisions, 0 findings, exit 0 |
| `python3 scripts/test-check-templates.py` | 15 cases, 15 pass, exit 0 |
| `python3 scripts/test-check-envelopes.py` | 19 cases, 19 pass, exit 0 |
| `python3 scripts/check-envelopes.py` | exit 1 on two envelopes — both **TASK-030**, pre-existing and out of scope |

Two figures carry the weight. The reference total is **40 before and after**, so the corrections
rewrote references rather than deleting them. And QA's inverted straw-man checker — glob `step-*.md`,
confirm each exists — **fails 10 of the 23 committed cases**, including all three direction cases,
which is what makes the direction guarantee measured rather than asserted.
