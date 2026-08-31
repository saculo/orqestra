---
id: TASK-037
type: pr
status: done
updated: 2026-08-31
task: TASK-037
branch: feat/TASK-037-bug-module-provenance
pr_number: 11
pr_url: https://github.com/saculo/orqestra/pull/11
pr_state: merged
---

## Summary

The spec said a `BUG` carries `module:`; `templates/BUG.md` did not have the key, and
`check-envelopes.py` had already encoded the claim as a rule. Plan traced where the value actually
comes from — typed by a human at intake, held as **prose** in `## Scope`, becoming a `module:` key only
at promote, on the *TASK* — and found the checker keys on the **scope key**, never frontmatter. So the
obligation was right and satisfiable; the **warrant** under it was false.

Resolution (a) at the gate: make the specification true rather than soften it. §4.8.1's `BUG.md` row
gains `module`, §7.3's promote clause carries it forward, **D-029** records why a `BUG` has a module
where a `PHASE` does not, and §5.5:957 and §5.1.1:795 needed no edit — under (a) they become accurate.

The docs third of a three-edit schema change whose edits span two modules. `templates/BUG.md` and
`step-intake.md` are **TASK-040's**.

## Commits

| commit | subject |
|---|---|
| `5447a0f` | TASK-037: plan — the obligation is right, the warrant under it is false |
| `2391235` | TASK-037: resolution (a), split docs-first, TASK-040 files the rest |
| `74f788c` | TASK-037: design — the docs third, deliberately red for one window |
| `550a361` | TASK-037: design gate approved, and the INDEX gap filed as TASK-041 |
| `9061ec5` | TASK-037: implement — §4.8.1 declares module on BUG.md |
| `a7b349c` | TASK-040: add AC-5 — the test_command comment must be true when it lands |
| `fac06bf` | TASK-037: qa — failed, 2 of 4 |
| `3209fbf` | TASK-037: rework — MODULE comes from the scope unit, not from the task |
| `9c76f92` | TASK-037: qa round 2 — passed, 4 of 4 |
| `e07866f` | TASK-037: review — passed, 0 required, 1 advisory |
| `612c818` | TASK-037: review gate approved; TASK-040 AC-1 widened, :717 filed as TASK-042 |

Eleven commits, `attempts: 1 of 3`. The failed qa is kept: it caught a self-contradiction this task
introduced on its own subject, and the sweep that missed it is why the rework records its search terms.

## CI

`gh pr checks 11` at 2026-08-31: **no checks reported**. Merged as `316bdd3`. The repository has no CI workflow. No review
threads.

Every checker was run **directly**, because `config.md`'s `test_command` chains with `&&` and a failing
`check-templates.py` stops the rest from executing — a chained "pass" would be a result never produced.

| command | result |
|---|---|
| `python3 scripts/check-decisions.py` | 29 decisions, exit 0 — was **red before implement ran** (see below) |
| `python3 scripts/check-envelopes.py` | 10 envelopes, exit 0 |
| `python3 scripts/check-step-refs.py` | 41 references, exit 0 |
| `python3 scripts/test-check-envelopes.py` | 25 cases, exit 0 |
| `python3 scripts/test-check-step-refs.py` | 28 cases, exit 0 |
| `python3 scripts/check-templates.py` | **exit 1** — exactly one finding, `BUG.md frontmatter missing: module`, closed by TASK-040 |
| `python3 scripts/test-check-templates.py` | **exit 1** — 3 of 15, same window, closed by TASK-040 |

Both reds are the deliberate one-merge window. Review judged it defensible on a ground stronger than
precedent: **`.orqestra/work/` is empty, so no `BUG.md` instance exists** and nothing is misrouted.
Writing `module?` would have bought a green check by marking a required key optional.

`check-decisions.py` was red *before implement*, because the design step wrote D-029 and holds no `Edit`
to register its INDEX row. Implement closed the instance; **TASK-041** carries the class.

## Follow-ups

**TASK-040** (`plugin`, depends on this) — the other two thirds of the schema change. Its AC-1 was
widened here to name `test-check-templates.py`, which a literal reading would have left red while the
task reported success; AC-5 was added for `config.md`'s stale `test_command` comment.

**TASK-041** — a design step cannot register the decision it writes.

**TASK-042** — §5:717 sends the orchestrator to `config.md` for a routing table that lives in
`modules.md`.
