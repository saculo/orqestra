---
id: TASK-019
type: implementation
status: done
updated: 2026-08-27
task: PHASE-1/TASK-019
deviation: moderate
files_changed: 29
---

## Changes

Recorded after the fact. The code was already written and committed by direct human instruction,
without a plan or design step (see `## Deviations`); this artifact was verified against
`git diff master...HEAD` on `feat/TASK-019-agents-invoke-their-skills`, not against the commit
messages. Three commits: `b40d90d`, `c9fd23e`, `6f59426`.

**Agent tool grants** — `agents/agentic-engineer.md`, `analyst.md`, `architect.md`,
`backend-engineer.md`, `devops-engineer.md`, `frontend-engineer.md`, `qa-engineer.md`,
`reviewer.md`. `Skill` added first in each `tools:` list. Verified: all eight carry it. **AC-4 met**
on the grant; the decision half is `D-025` (below).

**Persona instruction** — the same eight files. The unexecutable bullet *"Load the module expertise
skills named in your envelope"* is replaced in all eight by an identical block instructing invocation
of `SKILL` then every `EXPERTISE` skill via the `Skill` tool, stating that these are names and not
paths and that `Read` leaves a step skill's template paths unresolved (D-025). `6f59426` reworded that
sentence to describe the plugin-root placeholder rather than embed it — written literally, the token
expanded when the persona was loaded and the explanation said nothing. **AC-6 met**: no persona now
instructs a path-read of a step skill, and no persona contains the literal token. **AC-3 met** by
inspection of all eight: the replaced bullet was the only instruction any persona gave that its
`tools:` forbade; nothing in `analyst.md`/`architect.md` (no `Bash`, no `Edit`) asks for either.

**Envelopes** — `SKILL:` added to 9 of the 10 dispatch envelopes in `skills/`
(`close-phase/SKILL.md`, `greenfield/step-phases.md`, `step-tasks.md`, `step-plan-design.md` ×2,
`add-phase/step-define-phase.md`, `task/step-implement.md`, `step-qa.md`, `step-review.md`). Missing
conditional fields filled in: `step-plan-design.md` gained `MODULE`/`PATHS`/`STACK`/`EXPERTISE` on
both its plan and design dispatches; `step-qa.md` gained `MODULE`/`PATHS`; `step-review.md` gained all
four, placed after `LENSES`/`ROUND` per §5.5; `step-diagnose.md` gained `PATHS`/`STACK`;
`step-define-phase.md` gained `PHASE:`. `step-qa.md`'s `EXPERTISE` changed from
`java-expertise, test-quality` to `java-expertise, spring-conventions`, matching §5.1's `api` row —
the row decides, never the agent (§5.5). **AC-5 is not met** — see `## Deviations`.

**Return contract** — `SKILLS:` added to the `## Return` block of every skill that is dispatched
with an envelope: `skills/implement/SKILL.md`, `qa/`, `plan/`, `design/`, `review-task/`,
`review-phase/`, and — closing a gap found in this artifact's own first pass — `create-tasks/`,
`create-phases/`, `create-phase/`. That is all nine `SKILL:` envelopes in the tree. This is the
detection layer D-025 names: `tools:` grants the capability but cannot compel its use.

**Rework, QA finding I-3.** `SKILLS:` was the *second* return line in `skills/implement/SKILL.md`
and `skills/review-phase/SKILL.md`, and the first in the other seven — while all eight personas
instruct *"Your first `RETURN` line names what you loaded"* and D-025 says the return *"opens
with"* it. `SKILLS:` is now the first line of the `## Return` block in both files, each keeping its
own column alignment (`STATUS:` moved to second). All nine dispatch skills now open their return
with `SKILLS:`, so no skill contradicts the persona that dispatches to it. No other file touched.

`skills/pr-comments/` was checked and deliberately left alone. It is an `orchestrator+` sub-workflow
invoked by `skills/task/step-pr-comments.md` as `Skill: orqestra:pr-comments` with a PR number and
`--task`, not dispatched to a subagent with an envelope. It has no `SKILL:`/`EXPERTISE:` lines to
report and no `## Return` section at all, so D-025's obligation does not reach it.

**`scripts/check-envelopes.py`** (new, 127 lines, CPython 3 stdlib only, mode 755). Encodes §5.5's
obligation table as four classes — always / scope / conditional-as-a-set / step-specific — plus the
closed-list and duplicate-field rules, and names the violated class per finding. Exits 0/1/2.

**`.orqestra/decisions/D-025-agents-invoke-their-skills.md`** and its `INDEX.md` row — the decision
AC-4 requires, including the harness probe table that verified a subagent can invoke both a namespaced
plugin skill and a bare expertise skill, and that `${CLAUDE_PLUGIN_ROOT}` does expand for subagents.

**Live evidence for AC-1 and AC-2, which the commits could not claim.** `b40d90d` states the work was
not verified live because the session held agent definitions read at startup. This dispatch is that
verification: this agent invoked `orqestra:implement`, `claude-expert` and `orqestra-conventions`
successfully, and followed `implement`'s procedure and template rather than its persona's summary.
AC-2 is met. **AC-1 is not met**: the criterion requires a probe convention planted in an expertise
skill and a fresh dispatch confirming the output honours it, and no such probe was run. QA (I-1)
found the same and named why it cannot be run from here — the expertise skills live in
`.claude/skills/`, outside this module's `paths` (D14), and no agent in `agents/` holds the subagent
tool, so neither implement nor qa can dispatch a probe. Rework to implement will not close it. A
human must either rule the live-dispatch evidence sufficient for AC-1's intent or move the probe to
the eval harness (PHASE-1 SC-5). Open, owned elsewhere, awaiting that decision.

**`.orqestra/decisions/INDEX.md` frontmatter** corrected to `count: 25`, `next_id: 26`,
`updated: 2026-08-27`. The table already held 25 rows; the header had not been updated when D-025 was
appended.

Tests: `python3 scripts/check-templates.py` — 20 templates, all conform, exit 0.
`python3 scripts/check-envelopes.py` — 10 envelopes, 2 non-conformant, exit 1. Both remaining findings
are owned elsewhere and stay open: `step-diagnose.md`'s missing `SKILL` (TASK-024) and
`step-phases.md`'s missing scope field (§5.5, `docs` module, D-019).

## Deviations

| deviation | from design | what | why |
|---|---|---|---|
| moderate | no design existed | Task ran with no `PLAN.md` and no `DESIGN.md`, by direct human instruction. TASK.md's six criteria were the whole specification | Recorded, not defended. The pipeline's plan and design steps were skipped; nothing verified the approach before it was built |
| moderate | AC-5 | `scripts/check-envelopes.py` exits **1**, on two envelopes. `skills/bugfix/step-diagnose.md` has no `SKILL:` — `skills/diagnose/` does not exist (TASK-024). `skills/greenfield/step-phases.md` has no scope field — `create-phases` creates *all* phases and has no single scope unit, yet §5.5 puts the scope field in the always class | Both are real and owned elsewhere; §5.5 lives in the `docs` module (D-019). Inventing a skill name or a scope value to turn the check green would defeat the only thing the check is for. **AC-5 is not met**, and cannot be closed inside this module — not deferred and not passing, but open pending a human sequencing call: narrow AC-5 to the eight reachable envelopes, or hold TASK-019 for TASK-024 and the §5.5 amendment |
| minor | AC-4 / D-025 | **Closed by rework.** `SKILLS:` was the second return line in `skills/implement/SKILL.md` and `skills/review-phase/SKILL.md`; it is now the first in both, matching the other seven, the persona instruction and D-025 | QA I-3. Effect was nil — the orchestrator reads the block, not the ordinal — but an instruction contradicting the file it describes is the drift D-025 exists to end, and both files are inside this module's `paths` |
| minor | module boundary | Two of the 29 changed files are `.orqestra/decisions/` — outside the `plugin` module's `paths` | AC-4 mandates the decision file, and `.orqestra/` belongs to no module per PROJECT.md's layout. Flagged so review sees it deliberately, not as an escape |

## Tech Debt

- **This task ran without plan or design.** No approach was reviewed before it was built, and the
  deviations above are the kind a design step exists to catch.
- **`check-envelopes.py` exits 1 on two findings owned by other work** — `step-diagnose.md` (TASK-024)
  and §5.5's scope-field class (`docs` module). Until both close, the check cannot be wired into
  anything that gates on exit status.
- **`check-envelopes.py` does not encode §5.5's `EXPERTISE additionally` rule** — the field is
  omitted when the module row's `expertise` cell is empty. The checker requires all four conditional
  fields as a set, so that conformant shape would be reported as a partial class. No envelope in the
  tree hits it today.
- **`check-envelopes.py` globs `skills/*/*.md` only** — one level. An envelope in a nested directory
  would be silently uncounted, and the check reports its own total as evidence of coverage.
- **`PROJECT.md` is stale**: *"The only executable file in the repo is `scripts/check-templates.py`"*.
  There are now two. Outside this module's `paths`.
- **`check-envelopes.py` is mode 755, `check-templates.py` is 644** — same directory, same invocation
  style (`python3 scripts/...`), inconsistent bit.
- **§5.5's own example envelope and §5's opening example give the `api` module
  `java-expertise, test-quality`, while §5.1's registry gives it `java-expertise,
  spring-conventions`.** `step-qa.md` was corrected to follow §5.1; the spec still contradicts itself.
  `docs` module.
