---
id: D-016
type: decision
status: active
updated: 2026-08-25
area: workflow
supersedes: —
superseded_by: —
---

# D-016 — Rework routes to the step that owns the fix

**When:** 2026-08-25 · PHASE-1 / TASK-005 · deferred to PHASE-3
**Decision:** Every finding carries an `owner` — `implement` (default) · `qa` · `design`. The rework
loop dispatches each finding to its owner, in dependency order (design → implement → qa). A
`design`-owned finding is a **gate**, not a loop. The rule is: *rework returns to the step that owns the
fix, never to the step that found it.*

**Why:** "Everything loops back to `implement`" replaced a worse bug — `status` naming the step that
*failed* as the rework target — but over-corrected into a constant. It routes by nothing at all, and
`implement` is the wrong owner in at least three cases:

- A `tests`-lens finding ("this test asserts nothing") is a defect in **test code**, which `qa` writes
  and holds `Edit` for. `implement` does not own it.
- A qa failure caused by a **wrong test** rather than wrong code sends `implement` to fix code that is
  already correct.
- A design problem too mild for a `failed` verdict loops until `attempts` runs out, because
  `implement` cannot change a design.

The first exposes a real ownership hole: `qa` writes test code and is forbidden from touching the
implementation; `implement` builds "tests included". **Test code has two writers and no defined owner**,
so a `tests`-lens finding currently has nowhere correct to go.

**Constrains:** PHASE-3 implements this, alongside the rework-loop criteria (SC-2, SC-3) that are the
natural place to prove it converges.

- `REVIEW.md` `## Findings` gains an `owner` column: `id | severity | file:line | finding | owner | required`.
- `QA.md` `## Issues` distinguishes a code defect from a test defect the same way.
- `step-review.md` and `step-qa.md` dispatch per owner rather than unconditionally to `implement`.
- **Settle test-code ownership explicitly** while doing it. One of `qa` or `implement` owns test files;
  two writers on one artifact is what D1 exists to prevent.
- Spans `docs` (§4.8.2 catalogue, §8.1) and `plugin` (templates, skills) — **two tasks** (D14).
