---
id: D-015
type: decision
status: active
updated: 2026-08-25
area: workflow
supersedes: —
superseded_by: —
---

# D-015 — A `failed` review is a gate, not a block

**When:** 2026-08-25 · PHASE-1 / TASK-005 review of rework semantics
**Decision:** `changes-requested` loops back to `implement` and costs an attempt. `failed` does
neither — it stops and asks a human, offering a **re-review** (once, not counted against `attempts`),
revisiting the design, accepting the findings as debt, or abandoning the task.
**Why:** The two verdicts were collapsed: `failed` went straight to `blocked`. That treats the
reviewer as infallible, and a `failed` verdict can be wrong — a stale design, missing context, a lens
the task never claimed. It also has no route back short of manual recovery. Meanwhile routing `failed`
into the loop would burn three attempts on a problem `implement` cannot solve. Two distinct failures
need two distinct routes.
**Constrains:** Never auto-block a `failed` review, and never send one to `implement`. A re-review is
allowed **once**; two independent `failed` verdicts go to the human, because at that point the
disagreement is about the task rather than the code. `review-task` must state *what would change its
mind*, since its verdict may be disputed.
