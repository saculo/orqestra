---
id: TASK-047
type: task
status: pending
updated: 2026-09-01
phase: PHASE-1
module: docs
stack: markdown
origin: feature
bug:
depends_on: []
serves: [SC-5]
attempts: 0
---

## Goal

**Amending a phase definition is a sanctioned act with no section governing it. Three amendments have
been made citing a section that does not cover them.**

`PHASE-1/PHASE.md` carries three inline amendment records — `SC-2 AMENDED 2026-08-25`,
`SC-7 ADDED 2026-08-26`, `SC-7 AMENDED 2026-09-01`. The first two cite **§8.2**. §8.2 is *"Recovery —
un-wedging a run"*: it covers `blocked_reason`, `/orqestra:unblock`, a safe-to-hand-edit table whose
rows are `status`, `attempts`, `depends_on`, `id`, `type`, `phase`, and four recovery moves. Every one
of them is about a **task artifact mid-run**. None is about a phase criterion.

The third dropped the citation rather than repeating it, which is why the gap is now visible.

**The rule the amendments assert is not written anywhere.** They say it consistently and confidently —
*"amending a success criterion is a phase-definition change and a human's call, not a task's"*
(`PHASE.md:35-36`) — and it is a good rule. `create-phases` and `create-phase` write criteria;
`review-phase` and `close-phase` verify them; nothing says who may change one afterwards, when, or what
must be recorded. Three tasks have already declined to touch a criterion on the strength of a rule the
specification does not contain, and were right to.

**Why it is worth a section rather than a comment.** A phase criterion is the only artifact content
that **grades other work**. `close-phase` gates a milestone on it and `review-phase` writes a
`criteria_met` verdict against it, so an unrecorded criterion change silently rewrites the standard
that already-merged tasks were judged by. That is the one edit in the workspace that must leave a
record, and it is the one edit with no stated procedure.

The house form already exists and needs describing rather than inventing: an inline HTML comment
adjacent to the criteria table, naming what changed, the date, that a human decided it, and the reason
in enough detail that the next reader can tell a correction from a goalpost move. All three existing
records follow it. Two of them also carry a **lesson about why the criterion expired** — SC-2's format
string, SC-7's unmeasured mechanism — which is the part that makes the record worth more than a
changelog line.

## Acceptance Criteria

| id | criterion |
|---|---|
| AC-1 | A section states who may amend a phase criterion, when, and that it is never a task's act — the rule three amendments already assert and no section carries |
| AC-2 | It states what an amendment must record, matching the form `PHASE.md`'s three existing records already use, so they are conformant rather than retrospectively wrong (D-030) |
| AC-3 | It distinguishes **amending** a criterion from **adding** one, since `SC-7 ADDED` widened a phase mid-flight and its own comment says so — a widening and a correction are not the same act and should not read the same |
| AC-4 | It says what happens to work already verified against the old wording — `PHASE.md:45-47` decided a frozen `QA.md` is not rewritten (D5, D-030) and that precedent should be stated once rather than re-argued per amendment |
| AC-5 | `PHASE.md`'s two `(§8.2)` citations point at the new section, and §8.2 is unchanged — it is correct about what it does cover |

## Out of Scope

**Any skill under `skills/`.** `docs` module (D14). No skill reads or cites the missing section today,
so nothing follows this — unusually for a docs task, there is no plugin half.

**Amending any criterion.** This task writes the procedure. SC-7's amendment was already made under it
in draft form on 2026-09-01 and stands on the human decision recorded there, not on this task.

**A `/orqestra:amend-phase` command.** The act is rare, human-only, and a two-line file edit; a skill
for it is a v2 question (§12) and would need its own decision.

**§8.2 itself.** Correct about un-wedging a run. It is the citation that is wrong, not the section.
