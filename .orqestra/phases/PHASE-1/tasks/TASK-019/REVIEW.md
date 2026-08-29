---
id: TASK-019
type: review
status: awaiting-approval
updated: 2026-08-29
task: PHASE-1/TASK-019
verdict: passed
lenses: [correctness, design]
required: []
review_round: 1
---

## Verdict

**Passed.** The change does the one thing the task exists to do, and does it at the layer that
actually holds the guarantee: `Skill` is granted in all eight `agents/*.md` `tools:` lines, the
unexecutable *"Load the module expertise skills"* bullet is replaced in all eight by an identical
invoke-by-name block, all nine envelope-dispatched skills open their `## Return` with `SKILLS:`,
and `D-025` records why with four `Constrains:` rules a future agent can be held to. I verified
the four criteria independently rather than reading QA's word for them, and each holds. The four
findings below are all `minor`/`nit` — `required` is empty, so nothing here is worth a rework
attempt. The work's real weakness is not in the diff: it ran with **no `PLAN.md` and no
`DESIGN.md`**, which `IMPLEMENTATION.md` records as a moderate deviation rather than defending.
That leaves the `design` lens with no design to judge fidelity against, and it is the reason the
gate below matters more than usual.

## Findings

| id | severity | file:line | finding |
|---|---|---|---|
| F-1 | minor | `.orqestra/phases/PHASE-1/tasks/TASK-019/IMPLEMENTATION.md:8` | The file accounting is wrong in both places it appears. `files_changed: 29` and line 108's *"Two of the 29 changed files are `.orqestra/decisions/`"* cannot both be true: `git diff --name-only master...HEAD` is **39** files — 29 under `skills/`, `agents/`, `scripts/`, and 10 under `.orqestra/`. The two decision files are *additional* to the 29, not among them. The floor check still passes (no file lies outside `plugin`'s `paths` ∪ `.orqestra/`, and the boundary crossing is deliberately flagged), so this is an artifact-accuracy defect, not an unrecorded deviation. |
| F-2 | minor | `agents/analyst.md:24` (and the same block in all seven other personas) | The new block instructs *"Invoke `SKILL` first … before you do anything else"* **unconditionally**, but `skills/bugfix/step-diagnose.md` dispatches the analyst with no `SKILL:` field — the one envelope of nine that lacks it. An analyst dispatched at `diagnose` is therefore told to invoke a field its envelope does not supply, and the persona carries no clause for the absent case. The omission itself is recorded and correctly owned by TASK-024 (`skills/diagnose/` does not exist) and `check-envelopes.py` flags it; the *persona-side* gap is new, introduced by this diff, and inside this module. |
| F-3 | minor | `.orqestra/phases/PHASE-1/tasks/TASK-019/QA.md:71` | AC-2's evidence is the dispatched agent's self-report that it invoked its own skills, corroborated only by greps showing that phrases in `skills/qa/SKILL.md` are absent from `agents/qa-engineer.md`. That is consistent with the criterion but is not independent of the agent being tested — the same self-witness class that AC-1 was re-filed to TASK-031 precisely because it could not be verified from inside. The floor check "every AC-N has a real assertion behind it" passes for AC-3, AC-4 and AC-6 (greps and `check-decisions.py`, the latter with a negative control); AC-2 is the one row resting on attestation. |
| F-4 | nit | `skills/design/SKILL.md:69` | `SKILLS:` is padded to three spaces while the eight lines under it use five, making this the only one of the nine dispatch skills whose `## Return` block does not align on one column. No behavioural effect. Already carried as QA I-1. |

## What Would Change This Verdict

_n/a_

## Notes

- **The floor, all four checks.** (1) **Module paths** — every changed file is inside `plugin`'s
  `paths` or under `.orqestra/`, which `modules.md` deliberately assigns to no module; nothing
  outside either. (2) **`IMPLEMENTATION.md` accounts for the diff** — it does, including the
  `skills/task/step-qa.md` `EXPERTISE` correction and the `pr-comments` exclusion, both of which
  I checked and both of which are right; F-1 is a counting slip inside an otherwise complete
  account. (3) **Coverage map** — see F-3. (4) **No code contradicts an active `D-NNN`** — checked
  against D-024, D-019, D-012, D2/D16.

- **AC-3 re-verified independently, not read from QA.** `agents/analyst.md` and
  `agents/architect.md` hold `Skill, Read, Write, Glob, Grep` — no `Edit`, no `Bash` — and a scan
  for instructions requiring either returns nothing in either file. The newly-delivered layer does
  not reintroduce the defect either: `skills/plan/SKILL.md:5` and `skills/design/SKILL.md:5` both
  declare `disallowed-tools: Agent, Edit, NotebookEdit, Bash`, so the step skill an analyst now
  actually loads agrees with the persona's allowlist rather than contradicting it. That agreement
  is the part worth noting — this task's whole effect is to make step skills reach the agent, and
  a step skill instructing a forbidden action would have created exactly the class of defect the
  task set out to remove.

- **The `SKILLS:`-first invariant holds across the closed set, checked mechanically.** The nine
  `SKILL:` targets in the tree — `review-phase`, `create-phases`, `create-tasks`, `plan`, `design`,
  `create-phase`, `implement`, `qa`, `review-task` — each open their `## Return` block with
  `SKILLS:`. `clarify`, `create-task` and `init` do not, and correctly: none is dispatched with an
  envelope. This is D-025's third `Constrains:` rule satisfied as a set, not per-file.

- **Design lens, honestly bounded.** There is no `DESIGN.md`, so there are no components,
  interfaces or boundaries to judge fidelity against, and §7.8.2's *how I would have written it*
  rule leaves little else this lens can say. I judged structure against `PROJECT.md`'s layout and
  the module's conventions instead: the eight persona edits are byte-identical to each other, the
  decision lives where decisions live, and the checker sits beside `check-templates.py`. Nothing
  is misplaced. But **a passed review is not a substitute for the design step that was skipped**,
  and the human at the gate should read it that way.

- **D-019 tension, resolved correctly and worth stating.** `check-envelopes.py` *cites* §5.5, and
  D-019 says code citing a section inherits it, so docs leads. §5.5's always-class is wrong for a
  dispatch with no single scope unit, which is why the checker exits 1 on
  `skills/greenfield/step-phases.md`. Encoding the spec as written and leaving the check red — 
  rather than bending the checker to make it green — is the right call under D-019, and it is why
  the `docs` fix is TASK-030's rather than this task's.

- **`check-envelopes.py` limitations are self-reported, which is the reason they are not
  findings.** `IMPLEMENTATION.md`'s `## Tech Debt` already names the one-level `skills/*/*.md`
  glob, the unencoded `EXPERTISE additionally` rule, and the 755-vs-644 mode inconsistency. I
  found one more of the same class: `envelopes()` keys on any line starting `ROLE:` without
  requiring it to be inside a fence, so a prose occurrence would absorb fields up to the next
  fence anywhere in the file. No such case exists in the tree, and the script is dev-only
  (D-001, D-015).

- **Not re-run:** the test suite. Per rule 2, `QA.md`'s results are taken as given; the commands
  quoted above are the reviewer's own `git` reads and greps.
