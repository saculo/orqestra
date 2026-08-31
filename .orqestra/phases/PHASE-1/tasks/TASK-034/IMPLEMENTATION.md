---
id: TASK-034
type: implementation
status: done
updated: 2026-08-31
task: TASK-034
deviation: none
files_changed: 3
---

## Changes

**C1–C5 — the `diagnose` step skill.** New `skills/diagnose/SKILL.md`, 138 lines, a single file
beside `plan` with no shards. Frontmatter is §7.0's `step` row exactly (`Read, Write, Glob, Grep` /
`Agent, Edit, NotebookEdit, Bash`); the banner declares dispatch by `orqestra:bugfix` to `analyst`
and that the step is **gated**, following `design`. Section order is the house one — Inputs · Output
· Procedure · Return · When you cannot proceed · Rules — with `## The outcome contract` inserted
between Procedure and Return.

- **C2, the falsification procedure** is ten steps, written as a *reading* procedure: read the
  recorded reproduction, locate the surface where the wrong behaviour becomes observable, work back
  to a candidate, then try to disprove it by naming what would have to be true and checking it in
  the code. A standing note before step 1 states that the step holds no `Bash`, so the reproduction
  is read and never re-run. No step instructs a command, a test run, or history attribution — that
  is TASK-019's AC-3 defect class and the tool set forbids it. The *bar* is not restated: step 4
  cites `skills/bugfix/step-diagnose.md`'s `## The bar`, where it already lives in the repo's own
  words. **Amended in rework round 1 — see the rework note at the end of this section.**
- **C3, the outcome contract** is DESIGN.md's four-row table verbatim, with the reason beside it:
  `status` records only whether the step could run, `root_cause_found` carries the verdict, the same
  shape as D-015 and a `failed` qa result. `root_cause_found: false` with `status: done` reaches the
  gate, which is the only way the gate's `[ Investigate further ]` branch is reachable.
- **C4, the Return** opens with `SKILLS:` (AC-2) and is nine lines on `done` — `ROOT_CAUSE_FOUND`
  plus one line per gate label (`ROOT CAUSE`, `EVIDENCE`, `DIRECTION`, `RISK`) — and five on
  `blocked`, with the four gate lines omitted rather than padded. No `OUTCOME:` line, per design.
- **C5, the blocked table** carries `no-reproduction` and `contradictory-input` only, both from
  §4.4.3's closed list, with a sentence saying not to reach for a task-shaped reason.
- **Reference shape (AC-4).** Every step-file reference sits in prose, backticked, plugin-relative,
  with no `${CLAUDE_PLUGIN_ROOT}` — `check-step-refs.py --verbose` lists them at
  `skills/diagnose/SKILL.md:57` and `:128` as resolving (D-026). (Round 1 shipped one such reference;
  the rework made it two.)
- **Provenance says nothing.** `## Inputs` states that `MODULE`/`PATHS`/`STACK`/`EXPERTISE` arrive in
  the envelope and are the orchestrator's obligation (§5.5), and never where a bug's module comes
  from. If TASK-037 adds `module:` to `BUG.md`, no line here changes.

**C6 — the envelope.** `skills/bugfix/step-diagnose.md` gains one line, `SKILL:     orqestra:diagnose`,
inserted between `STEP:` and `BUG:` per §5.5's scope-field placement. Nothing else in that file
changed.

**C7 — the analyst description.** `agents/analyst.md`'s `description` now names the artifact set
generically and all five dispatch steps — create-phases, create-phase, create-tasks, plan, diagnose —
established by `grep -rn -A1 '^ROLE: *orqestra:analyst' skills/`, not assumed. It no longer names
`PLAN.md` as *the* artifact, since three of the five produce something else. The persona body is
unchanged: D-025 makes the invoked skill supersede it (AC-5).

**Verification run** (from the repo root, after the change):

| command | exit |
|---|---|
| `python3 scripts/check-envelopes.py` | **0** — `checked 10 dispatch envelopes against §5.5 · all envelopes conform` |
| `python3 scripts/check-step-refs.py` | 0 |
| `python3 scripts/check-templates.py` | 0 — 21 templates |
| `python3 scripts/check-decisions.py` | 0 |
| `python3 scripts/test-check-envelopes.py` | 0 — 25 obligation cases |
| `python3 scripts/test-check-step-refs.py` | 0 |
| `python3 scripts/test-check-templates.py` | 0 |

`config.md`'s whole `test_command` chain —
`check-templates.py && test-check-envelopes.py && check-envelopes.py` — **now passes, exit 0**. It
was red by design until this task; this is the first green run.

A green checker is necessary and not sufficient: `check-envelopes.py` goes green on the `SKILL:` line
alone, so under D-025 a stub would pass AC-3 and fail AC-1. Verified by inspection instead —
`claude plugin validate .` passes, the skill loads and is offered as `orqestra:diagnose`, and
`grep -nE 'TASK\.md|acceptance criteria|AC-|depends_on' skills/diagnose/SKILL.md` returns nothing,
which is DESIGN.md's substitution test for a skill assembled by analogy with `plan`.

**Rework, round 1 — F-1 only.** The review found the citation at `skills/diagnose/SKILL.md:57` false
in both halves, and a human decision (§8.2) constrained the repair to the citation: rule 3 of
`skills/bugfix/SKILL.md` is a genuine pre-existing defect — its "Evidence, or **block**" was already
the outlier against `skills/bugfix/step-diagnose.md:30` before this task existed — and is filed as its
own task, so `skills/bugfix/SKILL.md` is untouched here. Two lines changed, both in
`skills/diagnose/SKILL.md`, and they now cite one authority that actually agrees with them:

- **:57** drops the rule 3 reference entirely and names the part it means — `skills/bugfix/step-diagnose.md`'s
  `## The bar`. It adds the one thing that authority does *not* govern: what follows when nothing
  survives falsification is this skill's own outcome contract, not the cited file's.
- **:128, rule 1** was the second half of the finding — it restated the bar (with the ending swapped
  to `root_cause_found: false`), which is what :57 claimed not to do. It now defers to the same
  `## The bar` and points at step 4 as where the bar is met, keeping only the local disposition:
  `root_cause_found: false` per the outcome contract, never a block. The two lines agree, and neither
  restates a rule it can cite.

F-2 was left alone: the review marked it minor and not required, and the rework envelope scoped this
round to F-1.

**Rework verification** (repo root, after the change): `check-envelopes.py` **0**,
`check-step-refs.py` **0** — `--verbose` lists both references, `skills/diagnose/SKILL.md:57` and
`:128`, as resolving, which is the D-026 shape check for the line actually edited —
`check-templates.py` **0**, `check-decisions.py` **0**, `test-check-envelopes.py` **0**. `config.md`'s
whole `test_command` chain (`check-templates.py && test-check-envelopes.py && check-envelopes.py`)
**exits 0**.

## Deviations

| deviation | from design | what | why |
|---|---|---|---|
| _none_ | | | |

## Tech Debt

- **`templates/SKILL.template.md`'s class table lists the `step` class as "plan, design".** §7.0:1081
  now reads "`plan`, `design`, `diagnose`". A one-word divergence inside an HTML comment, not
  schema-bearing, touched by no criterion, and `check-templates.py` does not read it. Noted by PLAN.md
  and left alone (D3).
- **`.orqestra/config.md` still carries the six-line comment explaining why `check-envelopes.py` is
  red**, ending "DELETE THESE LINES when the scan goes green". The scan is now green. `.orqestra/` is
  outside this module's `PATHS`, so deleting it here would be the boundary violation D2 forbids — it
  needs the workspace's own task.
- **`skills/bugfix/SKILL.md:103`, rule 3, ends "Evidence, or **block**"**, where its own step file
  `skills/bugfix/step-diagnose.md:30` says `root_cause_found: false` is an honest outcome. It was the
  outlier before this task existed, no criterion here touches it, and a human ruled (§8.2) that fixing
  it in this diff would import a pre-existing defect. Filed as its own task; left alone (D3).
- **`agents/architect.md`'s `description` says design only**, while `modules.md` also routes the
  `docs` module's implement step to it — the fact TASK-029 blocked on twice. Same defect class as
  AC-5, deliberately excluded by TASK.md's amendment note and recorded there for a future task.
