---
id: D-023
type: decision
status: active
updated: 2026-08-25
area: workflow
supersedes: —
superseded_by: —
---

# D-023 — Review has a floor of four checks that no lens configuration can switch off

**When:** 2026-08-25 · PHASE-1
**Decision:** `review-task` runs four checks on every review regardless of lenses (§7.8.1): the module
`paths` boundary, unrecorded deviations against `IMPLEMENTATION.md`, `QA.md`'s coverage map against the
acceptance criteria, and contradictions of an active `D-NNN`. The lens table (§7.8.2) is elective
attention layered on top.

**Why:** the skill already ran all four unconditionally in its procedure while its rules said *"apply
only the lenses you were given"* — so it forbade recording what it had just instructed the reviewer to
find. Three of nine procedure steps were outside the lens system with no vocabulary for saying so.

The coverage check is the one that mattered most, and it was the worst placed. It was written as *"a
finding under the `tests` lens"*, and `tests` is not in the default `correctness,design`. So on a
default run: **`qa` wrote the tests, `qa` graded its own coverage, and nothing independent looked at
either.** The reviewer is forbidden to re-run the suite (correctly — that is qa's artifact, D2), which
made the coverage cross-check the only audit available, and it was disabled by default.

**Why not just add `tests` to the default lenses:** it would have fixed the coverage hole while leaving
the contradiction, and the other three checks would still have been lens-less instructions the rules
forbade recording. The floor names the real structure — a fixed contract check plus elective quality
attention — instead of pretending everything review does is a lens.

**Constrains:** a new check belongs in the floor only if it guards a **contract** (a boundary, a
schema, a settled decision, an id chain) rather than a quality opinion. Quality opinions become lenses,
and lenses stay optional. The `design` lens is explicitly bounded by the same reasoning: coupling that
violates a stated boundary is a finding, a simpler approach the reviewer preferred is a `## Notes`
entry, never a finding (§7.8.2).
