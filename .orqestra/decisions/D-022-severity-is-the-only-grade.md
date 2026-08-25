---
id: D-022
type: decision
status: active
updated: 2026-08-25
area: schemas
supersedes: —
superseded_by: —
---

# D-022 — Severity is the only grade a finding carries, and the rework ids live in frontmatter

**When:** 2026-08-25 · PHASE-1 · found by reading `review-task` against `step-review.md`
**Decision:** `REVIEW.md · ## Findings` loses its `required` column. `severity` (§4.4.3) is the only
grade. Frontmatter gains `required: [F-N, …]`, governed by one derivation rule:

> **Every `blocker` and `major` finding goes in `required`. No `minor` or `nit` may.**

**Why:** two defects, one cause.

- **The schema permitted the state it warned against.** `severity` and `required` were independently
  settable, so `severity: nit, required: yes` was representable — and `templates/REVIEW.md` spent three
  lines pleading against it. A closed vocabulary exists to make the bad state unrepresentable (D7);
  prose begging a reviewer not to write a legal value is the failure that rule prevents.
- **Nothing consumed `severity`.** The verdict keyed off `required`, and the rework loop consumed ids.
  By Rule B (§4.4.1) — the rule that deleted `task_type` — one of the two had to go. `severity` stays
  because it is the one a human reads at the gate, and the ladder carries the meaning.

**The second half fixes a step that could not be executed.** `step-review.md` said *"Read `REVIEW.md`
frontmatter only"* and then *"`REWORK: … address F-2, F-5 only`"*. The ids were in neither the
frontmatter nor the ≤10-line Return contract, which reported counts. The orchestrator was instructed to
name ids it had no contracted way to obtain, so in practice it would have opened the body and broken the
frontmatter-only rule. `required` in frontmatter satisfies Rule A: a later step branches on it.

**Constrains:**

- `review-task` grades each finding exactly once, then copies the `blocker`/`major` ids into `required`.
  Its self-verification (D12) checks the list against the table both ways.
- `step-review.md` builds `REWORK` from `required` verbatim, and **blocks** on `changes-requested` with
  an empty `required` — that combination is a contract failure, not an empty rework.
- Any future finding-grading field must state its consumer before it is added. `owner` (D-016, due
  PHASE-3) is the next one and inherits this: it routes, it does not grade.
