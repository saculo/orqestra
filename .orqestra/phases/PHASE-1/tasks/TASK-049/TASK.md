---
id: TASK-049
type: task
status: pending
updated: 2026-09-01
phase: PHASE-1
module: docs
stack: markdown
origin: feature
bug:
depends_on: []
serves: [SC-4]
attempts: 0
---

## Goal

**After rework, a stale `QA.md` still says `passed`, and `status` believes it. The task resumes at
review, and the changed code is never re-verified.**

Stage derivation reads artifact presence and frontmatter and nothing else
(`skills/status/SKILL.md:38-51`). Its three documented traps are all about artifacts that are *absent*
or *failing*. There is no trap for the one that matters most: an artifact that **passed against a
different generation of the source**.

The sequence, entirely within documented behaviour:

| | state on disk | derived stage |
|---|---|---|
| review returns `changes-requested` | `QA.md` `passed`, `REVIEW.md` `changes-requested` | `verified` — correct, *"qa genuinely passed"* |
| implement re-runs and the session ends | new `IMPLEMENTATION.md`, **old `QA.md` still `passed`** | `verified` |
| next `/orqestra:task` | resumes at **review** | QA of the changed code never runs |

Merge-gate rejection routes back to implement the same way (`skills/task/step-merge.md:39-45`), and
there both `QA.md` and `REVIEW.md` survive as passing — so a resume can reach **push** with neither
artifact having seen the current code.

**Artifact presence does not prove the artifact evaluated the current implementation.** That is the
missing invariant, and §4.3's table cannot express it because no artifact records *which* source it
judged. `status` is not wrong; it is answering a question the schema cannot ask.

**Why this serves SC-4 rather than a pipeline criterion.** SC-4 requires `status` to derive the correct
stage for every row of the §4.3 table including its traps. This is a fourth trap, and the most
dangerous of the four, because the first three under-report and this one **over-reports** — it advances
a task past a gate rather than parking it short of one.

## Acceptance Criteria

| id | criterion |
|---|---|
| AC-1 | Every delivery artifact records what source generation it judged — a commit SHA or a monotonic revision — added to the §4.8.1 catalogue for `IMPLEMENTATION.md`, `QA.md`, `REVIEW.md` and `PR.md` |
| AC-2 | §4.3 states that a stage advances only when the artifact's recorded generation matches the current one, and a mismatched artifact is treated as absent rather than as passing |
| AC-3 | The rule is stated for **both** routes back to implement — review `changes-requested` and merge-gate rejection — since the second leaves two passing artifacts, not one |
| AC-4 | Added as a fourth trap to §4.3's trap list with its reason, so SC-4's verification covers it and a fixture can be built for it |
| AC-5 | §8.2's recovery moves stay consistent: "redo a step — delete its artifact" must still work, and the new field must not make a hand-deleted artifact ambiguous |

## Out of Scope

**`skills/status`, `skills/task`, and the templates.** `plugin` (D14), and the skills cite §4.3 rather
than restating it, so docs leads (D-019). The plugin half is a separate task and lands second.

**Making rework delete downstream artifacts instead.** A plausible alternative — on any route back to
implement, delete `QA.md` and `REVIEW.md` — and it may be the better answer, since §8.2 already makes
deletion the recovery mechanism. This task should choose between recording generations and deleting
artifacts, and say why; it should not do both.

**`attempts` as the generation counter.** It counts rework cycles per step, not source generations, and
TASK-052 shows its semantics are already contested.
