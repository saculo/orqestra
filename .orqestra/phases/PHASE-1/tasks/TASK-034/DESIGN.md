---
id: TASK-034
type: design
status: awaiting-approval
updated: 2026-08-30
task: TASK-034
decisions: []
---

## Components

| # | component | responsibility | serves |
|---|---|---|---|
| C1 | The `diagnose` step skill | A single-file `step`-class skill, sibling of `plan`, declaring the §7.0 class fields and a description carrying its own trigger phrases. Its subject is a `BUG`, never a `TASK` | AC-1 |
| C2 | The falsification procedure | The ordered steps that take a reader from a recorded reproduction to a cause **with evidence** — read the reproduction, locate the symptom's surface, then work back and try to *disprove* the first plausible cause before writing it down | AC-1 |
| C3 | The outcome contract | The mapping from what the diagnosis found to `status` + `root_cause_found` + the return's `STATUS`. This is the component that keeps "no cause found" a `done` outcome | AC-1 |
| C4 | The gate-feeding `## Return` block | Nine lines opening with `SKILLS:`, carrying the verdict and the four fields the diagnosis gate renders | AC-1, AC-2 |
| C5 | The blocked table | The two conditions that stop the step, each mapped to a value already in §4.4.3's closed list | AC-1 |
| C6 | The `SKILL:` line in the diagnose envelope | The one always-class field missing from `skills/bugfix/step-diagnose.md`'s dispatch, making the D-025 triple complete for the last envelope | AC-3 |
| C7 | The corrected analyst description | One frontmatter line naming the steps the persona is actually dispatched at | AC-5 |

AC-4 gets no component of its own. It is a **constraint on how C1–C5 are written** — see `## Interfaces`,
reference shape — because a checker that must stay green is satisfied by discipline in the new file, not
by a new artifact.

## Interfaces

**C1 frontmatter.** Exactly the `step` row of §7.0's class table (:1081), no additions:

```yaml
name: diagnose                                        # the folder name is the invocation name (D-012)
description: "…"                                      # trigger phrases in the description, not the body
allowed-tools: Read, Write, Glob, Grep
disallowed-tools: Agent, Edit, NotebookEdit, Bash
```

The `> **Invocation**: … · **Class**: step` banner states that it is dispatched by `bugfix` at the
diagnose step, to the `analyst` subagent, **and that it is gated** — `plan`'s banner has no gate to
declare and `design`'s does; diagnose follows `design`.

**No `Bash` is the load-bearing consequence.** A `step` skill cannot execute anything. The reproduction
is *read*, never re-run; commit attribution is available only where the reproduce step already recorded
it. C2 must be written as a reading procedure, and must not instruct work the tool set forbids.

**C3 outcome contract.** The table the skill states verbatim, because this is the distinction an
engineer working by analogy with `plan` will get wrong:

| what the diagnosis established | `status` | `root_cause_found` | return `STATUS` | reaches the gate |
|---|---|---|---|---|
| a cause, with evidence that survives falsification | `done` | `true` | `done` | yes |
| no cause — investigated honestly, nothing established | `done` | `false` | `done` | **yes** |
| `BUG.md#Reproduction` holds no established failing reproduction | `blocked` | `false` | `blocked` | no |
| the report and the reproduction disagree on observed behaviour | `blocked` | `false` | `blocked` | no |

`root_cause_found: false` with `status: done` is a **result**, not a failure. The gate in
`skills/bugfix/step-diagnose.md` offers `[ Investigate further ]`, and that branch is reachable only from
an artifact that gets to the gate; a `blocked` one never does. This is the same shape as a `failed`
review (D-015) and a `failed` qa result — the verdict key carries the negative answer, `status` carries
only whether the step could run. The skill states the reason alongside the rule, so the case survives.

**C4 `## Return`** — nine lines on `done`, five on `blocked`:

```
SKILLS:            <the SKILL and EXPERTISE names you invoked, or `none`>
STATUS:            done | blocked
ROOT_CAUSE_FOUND:  true | false          # mirrors the frontmatter key the orchestrator reads
ROOT CAUSE:        <one line — the cause, not the symptom>
EVIDENCE:          <one line — what proves it>
DIRECTION:         <one line — where the fix belongs, roughly what shape>
RISK:              <one line — what the fix could break>
SCHEMA:            ok
BLOCKED:           <reason> — <what a human must decide>
```

What this carries that `plan`'s return does not, and why:

- **The four gate fields.** §5.5.1 forbids the orchestrator reading the artifact body, yet the gate block
  renders `ROOT CAUSE`, `EVIDENCE`, `DIRECTION`, `RISK`. Those four lines can reach the human **only**
  through the return text. `plan`'s `AREAS`/`RISKS` pair does not carry them. The field names match the
  gate's labels one-to-one so the orchestrator renders rather than interprets.
- **`ROOT_CAUSE_FOUND`.** Named identically to the frontmatter key on purpose: the human at the gate and
  the orchestrator reading frontmatter must be looking at the same fact, and a differently-named return
  field invites them to diverge.
- **No `OUTCOME:` line.** `ROOT CAUSE` *is* the outcome; a separate one would restate it and cost the
  line that puts the block at the 10-line ceiling with no room left.
- **On `blocked`, the four gate lines are omitted** rather than filled with `n/a` — there is no gate to
  feed, and padding a return with placeholders is how a 10-line ceiling gets breached.

**C5 blocked values**, both from §4.4.3's closed list, nothing invented: `no-reproduction` (the §7.3
precondition is absent — detecting it, never re-establishing it, which is the reproduce step's job) and
`contradictory-input` (report and reproduction disagree). `plan`'s `needs-splitting` and
`criterion-unsatisfiable` do not appear: a bug has no acceptance criteria to satisfy and no task to
split.

**C6 envelope line.** `SKILL:      orqestra:diagnose`, inserted between `STEP:` and `BUG:` — §5.5 puts
the scope field immediately after `SKILL`, so this is an insertion point, not an append. Nothing else in
that file changes (Out of Scope).

**C7 description contract.** True for all five dispatches, naming no single one as if it were the only
one. The set is `create-phases` · `create-phase` · `create-tasks` · `plan` · `diagnose` (established by
`grep -rn -A1 '^ROLE: *orqestra:analyst' skills/`, not assumed), and the description must not name
`PLAN.md` as the artifact it produces, since two of the five produce something else.

**Reference shape (AC-4).** Any step file the new `SKILL.md` names — `skills/bugfix/step-diagnose.md` is
the likely one — appears in **prose, in backticks, plugin-relative, without `${CLAUDE_PLUGIN_ROOT}`**. A
prose citation is not a `Read` argument, so the variable would be wrong there (D-026); the same string in
a table row would require it, which is `check-step-refs.py`'s first shape rule. **Do not put a step-file
reference in a table row in this skill.**

**Consumed, not derived.** `MODULE`, `PATHS`, `STACK`, `EXPERTISE` arrive in the envelope and §5.5 makes
composing them the orchestrator's obligation. The skill reads them from the envelope and **says nothing
about where a bug's module comes from** — that question is TASK-037's, and any sentence here that
presumed an answer would need editing when TASK-037 lands.

## Structure

The change lands in three areas of the `plugin` module, in this order, because each depends on the one
before it:

1. **`skills/`, as a new step-skill directory beside `plan`.** One `SKILL.md`, no shards: every
   `step`-class skill is a single file, and sharding is the *orchestrator's* context-economy lever, not
   a step's. It follows the house section order — Inputs · Output · Procedure · Return · When you cannot
   proceed · Rules — and stays under the ~150-line sharding threshold, as `plan` does at 87.
2. **The `bugfix` orchestrator's diagnose step file**, once the skill exists. A `SKILL:` line naming a
   skill that is not yet on disk is a dangling dispatch, so the envelope is edited second.
3. **`agents/`, the analyst persona's `description` line only.** Its body stays as it is. The body's
   plan-shaped prose is exactly what D-025 says the invoked skill supersedes; widening the persona's
   body would put diagnose-shaped instructions in two places, which is the duplication this project
   names as a rule that will disagree with itself.

**What must not be reached into:**

- **`REQUIREMENTS.md`** — a different module (D14), and TASK-033 already landed the amendments.
- **`templates/DIAGNOSIS.md`** — already conformant to §4.8.1:585. The skill copies it; it does not
  restate its headings as a checklist.
- **`scripts/`** — both checkers are the acceptance instrument. Changing one to make a criterion pass
  inverts the test.
- **`.claude/skills/orqestra/`** — whole-directory symlinks, so a new `skills/diagnose/` is picked up
  with no second edit and no new link.
- **The falsification *bar*.** `skills/bugfix/step-diagnose.md` and `skills/bugfix/SKILL.md` rule 3 both
  state it. The new skill carries the *procedure* for reaching evidence and **cites** the bar; a third
  wording of it is the failure this project's conventions name explicitly.

## Decisions

- **`root_cause_found: false` is a `done` outcome, stated as a table in the skill rather than as prose.**
  The prose version is what an engineer skims; the table is what they check their work against. This is
  local to this task — the underlying rule (a verdict key carries the negative answer, `status` carries
  only whether the step ran) is already settled by D-015 and the qa `result` field, and is cited, not
  re-decided.
- **The Return drops `OUTCOME:` to fit the four gate fields.** Local: it follows from this step being
  gated on four named fields, which no other step skill is.
- **No `D-029` recorded.** Two candidates were considered and both are restatements of settled material:
  "a gated step's return must carry every field its gate renders" is §5.5.1 plus the 10-line ceiling
  applied, and "the negative verdict is not a block" is D-015's shape. Writing either as a decision file
  would create a second wording of an existing rule, and neither has a `**Constrains:**` line that is not
  already someone else's. Recorded here so the absence is a judgement, not an oversight.
- **The analyst's persona body is not widened (C7 is the description only).** AC-5 scopes it to the
  description because that is what the harness reads when selecting an agent; the body's behaviour is
  supplied by the invoked skill under D-025.

## Test Strategy

There is no test runner (§7.0 has no runtime dependency on `scripts/`); verification is behavioural plus
two dev-only checkers. Note the baseline: `check-envelopes.py` exits 1 **today** — that is this task's
precondition, so only the after-state is evidence.

| AC | what proves it |
|---|---|
| AC-3 | `python3 scripts/check-envelopes.py` exits 0 and prints `all envelopes conform` over 10 envelopes. Exit 0 does not prove *placement*: read the envelope and confirm `SKILL:` sits between `STEP:` and `BUG:` per §5.5 |
| AC-4 | `python3 scripts/check-step-refs.py` exits 0 **and** `--verbose` lists every reference the new `SKILL.md` contains. Exit 0 alone is satisfied by a file with zero references, so the verbose listing is the part that proves the references exist and are shaped right |
| AC-2 | The first line inside the `## Return` fence is `SKILLS:`. Then cross-check the field set against the gate block in `skills/bugfix/step-diagnose.md`: every label the gate renders has a return line to render from |
| AC-5 | `grep -rn -A1 '^ROLE: *orqestra:analyst' skills/` yields five steps; the description's step set equals that set exactly, and names no artifact that only one of the five produces |

**AC-1 is the one a green checker cannot prove.** D-025 means a stub passes AC-3 and AC-4 while failing
AC-1, so AC-1 is verified by inspection against five named tests:

1. **It loads and it is real.** `claude --plugin-dir .`, then `/orqestra:diagnose` — the skill triggers,
   and its body names `BUG.md` as its subject. `claude plugin validate .` stays clean.
2. **The substitution test — the anti-copy test.** No sentence in the skill is true only of a task. Grep
   the file for `TASK.md`, `acceptance criteria`, `AC-`, `depends_on`: all absent. This is the check that
   catches a skill assembled by analogy with `plan`, which looks right and is wrong about what it
   operates on.
3. **The four differences are each locatable.** A reader can point at: the `BUG` subject, the
   falsification procedure, the `root_cause_found: false` → `done` row, and the gate-wide Return. A
   missing one means the skill was copied where it should have diverged.
4. **The invariance test (Q2).** Nothing in the skill states where a bug's `module:` comes from. Read it
   asking: *if TASK-037 adds `module:` to `BUG.md`, does one line here need to change?* The answer must
   be no.
5. **The non-duplication test.** The falsification bar appears once in the repo's own words — in
   `bugfix` — and the new skill cites it. Section order and tool fields match the house pattern and
   §7.0's `step` row exactly, and the file is under ~150 lines.
