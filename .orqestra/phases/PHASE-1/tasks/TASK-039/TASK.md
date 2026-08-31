---
id: TASK-039
type: task
status: pending
updated: 2026-08-31
phase: PHASE-1
module: plugin
stack: markdown
origin: feature
bug:
depends_on: []
serves: [PHASE-3/SC-1]
attempts: 0
---

## Goal

**`bugfix`'s rule 3 tells the orchestrator to block where its own step file says done.**

`skills/bugfix/SKILL.md:103` reads:

> 3. **Never diagnose past the first plausible cause.** Evidence, or block.

`skills/bugfix/step-diagnose.md:30` has said the opposite since before TASK-034 existed:

> `root_cause_found: false` is an honest and useful outcome; a confident wrong diagnosis costs a
> designed fix, an implementation, and a review before anyone notices.

And `skills/diagnose/SKILL.md` now makes it a contract: an honest investigation establishing no cause
is `status: done`, `root_cause_found: false`, and it **reaches the gate**, where the human is offered
*Investigate further*. Rule 3 would have the orchestrator block that same result.

Found by TASK-034's qa and ruled on by its review, which established the defect predates TASK-034 —
rule 3 was already the outlier against its own step file — and correctly declined to fix a defect that
task did not cause. Recorded as tech debt in `TASK-034/IMPLEMENTATION.md` and `REVIEW.md`.

**The branch this protects is the one that matters.** A diagnosis that honestly found nothing is a
result a human must see. Blocking it hides the investigation and loses what was ruled out.

## Acceptance Criteria

| id | criterion |
|---|---|
| AC-1 | `skills/bugfix/SKILL.md` rule 3 agrees with `step-diagnose.md`'s "## The bar" and with `skills/diagnose/SKILL.md`'s outcome contract — a no-cause result reaches the gate rather than blocking |
| AC-2 | What rule 3 was right about survives: a *plausible* cause without evidence is still not a diagnosis. The fix is the outcome it prescribes, not the standard it sets |
| AC-3 | No other rule or prose in `skills/bugfix/` contradicts the outcome contract — checked by reading the workflow end to end, not by grepping for "block" |
| AC-4 | `python3 scripts/check-envelopes.py` and the `config.md` `test_command` chain still exit 0 |

## Out of Scope

`skills/diagnose/SKILL.md`'s contract and `step-diagnose.md`'s "## The bar". Both are correct; rule 3
is the outlier and moves to meet them.

`REQUIREMENTS.md` — if §7.3's walkthrough turns out to carry the same error, that is `docs` and a
separate task (D14, D-019). Report it rather than crossing.
