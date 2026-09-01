---
id: TASK-028
type: task
status: pending
updated: 2026-09-01
phase: PHASE-1
module: docs
stack: markdown
origin: feature
bug:
depends_on: [TASK-046, TASK-011]
serves: [SC-7]
attempts: 0
---

## Goal

**D2 is stated and unenforced. A dispatched agent can write any artifact it likes, and nothing looks.**

D2 says it plainly: "A dispatch declares exactly one `WRITE:` path. **Any write outside it is a
contract violation**, and the orchestrator rejects the step rather than accepting the artifact." The
rule is correct and needs no change. What is missing is the second half — the orchestrator is told to
reject the step and given no way to know there is anything to reject.

**Found by running `/orqestra:task TASK-015` on 2026-08-26.** The `qa-engineer`, dispatched with
`WRITE: .../TASK-015/QA.md`, wrote `QA.md` and then:

| what it did | what forbids it |
|---|---|
| wrote `.../TASK-015/REVIEW.md`, `verdict: passed`, `status: done` | D1 — `REVIEW.md`'s sole writer is `review-task`. D2 — one `WRITE:` path |
| ran `git commit`, creating `548d3c1` | `skills/qa/SKILL.md:35`, "Do not commit — `step-push.md` owns git (D1)" |

Neither was detected. The orchestrator read `QA.md`'s frontmatter, saw `result: passed`, and would have
advanced to review exactly as if the step had been clean. The violation surfaced because a `git status`
was run for an unrelated reason, and the artifact was caught before it did damage — but the damage it
would have done is the point: `REVIEW.md` carried `status: done`, which makes `status` derive the stage
`reviewed` and sends the next run straight to **push**. The gate before the remote, gone, with no
human involved and nothing in the workspace recording that a gate was skipped.

Every reason the rule exists was live in that artifact. It reviewed a `QA.md` superseded a minute
later, so it was silent on the two findings an independent review then graded **major**. And it vouched
for the independence of the qa evidence — which was the one check it could not make, being the same
agent.

**The counterpart to TASK-011, from the other side.** That task stops orchestrators writing what they
do not own. This one stops workers doing it, and the shared root is the same: D1 and D2 name owners,
and nothing in the pipeline ever checks who actually held the pen. A charter rule with no verification
is invisible — the argument SC-7 was added on.

## Acceptance Criteria

| id | criterion |
|---|---|
| AC-1 | The orchestrator's on-return procedure states a **mechanical** check that a step wrote only its `WRITE:` path — an inspection of the working tree, comparable against the envelope, needing no judgement — and states it once where every step inherits it rather than per step |
| AC-2 | D2 says what "rejects the step" means concretely: what happens to the out-of-contract artifact, whether the step is re-dispatched or blocked, and whether the attempt is spent. Today the consequence is named and undefined |
| AC-3 | The spec forbids a dispatched agent from running `git` at all, at charter level rather than in one skill's prose. `skills/qa/SKILL.md:35` states it for qa only; seven other agents hold `Bash` and are told nothing |
| AC-4 | An out-of-contract write is **recorded**, not merely rejected — a step that violated its envelope leaves evidence in the workspace, so the violation is visible after the fact rather than only to whoever happened to be looking |

## Out of Scope

**Changing any skill under `skills/`.** This is the `docs` module: `REQUIREMENTS.md` only (D14). The
plugin change is a separate task and must come second, since the skills cite these sections rather than
restating them (D-019).

**TASK-011's four gate-write sites and its `attempts` instructions.** Same root cause, already filed,
and the two tasks must not both amend D1's writer table. Hence `depends_on: [TASK-011]` — not because
this work needs that work, but because they collide textually. `TASK-046` joins the list for a
different reason: AC-1's check compares what a step wrote against its `WRITE:` path, and D-031 measured
that a step under a `Write`-denying caller writes nothing at all — which that check would read as
clean. It must not ship against a tool pool that makes every step look compliant.

**Whether `attempts++` belongs to the task orchestrator.** TASK-011's table lists four sites where an
orchestrator is told to write and cannot; `step-review.md:48`, `step-qa.md:37` and `step-merge.md:42`
are three more it does not list. Extending that table is TASK-011's call, not this task's (D3).

**Detecting the violation retroactively across existing artifacts.** This task defines the check for
dispatches going forward. Auditing what previous runs may already have written is separate work, and
worth doing once the check exists to define what it is auditing for.
