---
id: TASK-034
type: review
status: done
updated: 2026-08-31
task: TASK-034
verdict: changes-requested
lenses: [correctness, design]
required: [F-1]
review_round: 1
---

## Verdict

The skill is a real procedure, not a stub: an analyst holding only `Read`/`Write`/`Glob`/`Grep` can
follow steps 1–10 against a `BUG.md` and reach a defensible cause, because step 4 gives a *test*
("name at least one thing that would have to be true if the candidate were the cause, and check it in
the code") rather than an exhortation to read carefully. The outcome contract is correct and
orchestrator-legible, all five criteria are met, and the floor is clean. One thing sends it back:
step 4 cites `skills/bugfix/SKILL.md`'s rule 3 as the bar this step meets, and rule 3 instructs the
opposite disposition on the single branch this task exists to protect.

## Findings

| id | severity | file:line | finding |
|---|---|---|---|
| F-1 | major | `skills/diagnose/SKILL.md:57` | The sentence "The bar is `skills/bugfix/step-diagnose.md`'s and rule 3 of `skills/bugfix/SKILL.md`'s — it is stated there, and this step meets it rather than restating it" is false in both halves. Rule 3 (`skills/bugfix/SKILL.md:103`) reads "Never diagnose past the first plausible cause. Evidence, **or block**." This step does *not* meet that: its outcome contract at :81 makes an unproven cause `status: done` / `root_cause_found: false`, gate-reaching, and :85 says in bold "Row two is not a block." And it *does* restate it — rule 1 at :128 repeats the rule verbatim with a different ending ("Evidence, or `root_cause_found: false`"). Citation is this project's consistency mechanism; a citation whose target instructs the opposite disposition sends a fresh analyst to authoritative text that deletes the `[ Investigate further ]` branch. One-line fix, either end (both files are inside `plugin`'s `paths`) |
| F-2 | minor | `skills/diagnose/SKILL.md:91` | "On `done`, nine:" — the fenced block below it is eight lines (`SKILLS`, `STATUS`, `ROOT_CAUSE_FOUND`, `ROOT CAUSE`, `EVIDENCE`, `DIRECTION`, `RISK`, `SCHEMA`). Inherited from `DESIGN.md`, which miscounts the same way by folding the `done` and `blocked` variants into one nine-line listing, so it is not a deviation. The literal block governs and the ceiling is "at most 10", so nothing breaks; but a stated count that disagrees with the block beneath it invites a fresh agent to pad a ninth line |

## What Would Change This Verdict

_n/a_

## Notes

**Ruling on the issue `QA.md` recorded as pre-existing.** qa is right that the *contradiction* predates
this task: `skills/bugfix/step-diagnose.md:31` on `master` already says "`root_cause_found: false` is an
honest and useful outcome", so `skills/bugfix/SKILL.md:103` was already the outlier against its own step
file before a line of this task was written. What is **not** pre-existing is `skills/diagnose/SKILL.md:57`,
a line this task introduces, which asserts that rule 3 is the bar this step meets. That assertion is
this task's, it is false, and it is what F-1 is about. The repair may equally be made at :103 — this
review does not prescribe which end — but shipping the citation unchanged is not an option, which is
why it is a finding here rather than a follow-up.

**Bash-freedom, judged as the dispatched analyst.** The procedure is genuinely executable without
execution. The one place the *surrounding* workflow oversells it: the gate exemplar at
`skills/bugfix/step-diagnose.md:42-43` shows evidence including "Introduced in TASK-004 (commit
a3f21c8)" — commit attribution the analyst cannot produce, and which `templates/BUG.md` has no section
to carry forward from reproduce. The new skill handles this honestly (the standing note before step 1,
and rule 2), so it is not a finding on this file; it is an argument for a `## Attribution` slot in
`templates/BUG.md`, or a less flattering exemplar, in a later task.

**Orchestrator-legibility of the outcome contract.** Checked as asked. An orchestrator reading
frontmatter only sees `status: done` + `root_cause_found: false` and gates — correct. The four return
lines carry the gate's labels name-for-name (`ROOT CAUSE`, `EVIDENCE`, `DIRECTION`, `RISK`), so the gate
renders without reading the body (§5.5.1). `ROOT_CAUSE_FOUND` mirroring the frontmatter key is the right
call. No gap here.

**AC-5 verified independently.** `grep -n "STEP:"` across every file containing `ROLE: orqestra:analyst`
yields exactly `create-phases`, `create-tasks`, `create-phase`, `plan`, `diagnose` — the five the new
description names, with no sixth and no name mismatch. Widening did not make it vague: it still names a
bounded artifact set and keeps the two negative clauses ("Does not design and does not write code")
that make agent selection discriminating.

**Floor, all four.** Three source files, all inside `skills/`, `agents/` — `.orqestra/` artifacts are
workspace state belonging to no module by `modules.md`'s own note, not a boundary violation.
`IMPLEMENTATION.md` accounts for the diff component by component with `deviation: none`, and the analyst
diff really is the one line it claims. `QA.md`'s coverage map has a real assertion behind every AC,
including the soft one: AC-1 was verified by live invocation plus a substitution test, not by the
checker that AC-3 uses — qa correctly identified that `check-envelopes.py` goes green on the `SKILL:`
line alone and would pass a stub. No active decision is contradicted: D-025 (return opens `SKILLS:`;
`agents/analyst.md` holds `Skill`), D-026 (prose reference plugin-relative, template path carries
`${CLAUDE_PLUGIN_ROOT}`), D-015 (cited correctly as the shape the outcome contract copies), D-028
(§4.8.1:585 already names `diagnose` as writer, landed by TASK-033) all hold.
