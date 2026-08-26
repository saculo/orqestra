---
id: TASK-015
type: plan
status: done
updated: 2026-08-26
task: TASK-015
---

## Approach

**Amend §5.5 in place; append one subsection if the field table needs its own home. Renumber nothing.**

§5.5 today is a single canonical envelope example plus three short paragraphs of prose. The whole change
fits inside it: correct the `EXPERTISE` sentence (line 892), add `MODULE`/`PATHS`/`SKILL` to the example
block (lines 862–881), and add a mandatory-versus-step-specific table after it. Amending prose and a
fenced block changes no section number, so none of the citations break (see Risks).

The alternative — inserting a new `§5.5.2 Envelope fields` — was rejected as unnecessary rather than
unsafe. Appending after §5.5.1 is legal per the append-not-insert rule (PROJECT.md, D-007's reasoning),
but §5.5 is 26 lines of prose; a table belongs in it, not beside it. What is *not* safe under any reading
is inserting between §5.5 and §5.5.1: `§5.5.1` is cited nine times from `agents/*.md` and once from
§7.11, and every one of those is a return-contract citation that must keep pointing at the return
contract.

**The `EXPERTISE`-as-paths change is a correction of fact, not a design choice.** No agent file grants
`Skill` (verified: all eight `agents/*.md` `tools:` lines, below). Under D-024 that list is a true
allowlist for the whole subagent run, so a name in `EXPERTISE` resolves to nothing. Every agent holds
`Read`. Paths therefore close the gap with no tool change, and match §5.5's own *"paths, never contents"*
doctrine — which is the same argument, applied to the same field, one paragraph apart.

**Scope correction that shapes AC-3** — see Open Questions Q1. The premise in TASK.md ("the qa and
review envelopes in §7.4 omit `MODULE`, `PATHS`, `STACK`, and the planning envelopes omit `EXPERTISE`")
is true of the envelopes, but those envelopes are **not in §7.3/§7.4/§7.5**. Those sections contain step
*listings*, not envelopes. The envelopes are in `skills/`, which is the `plugin` module and TASK-019's
work (D14). Inside this task's `PATHS`, AC-3 has exactly one subject: the §5.5 example itself — which
omits `MODULE` and `PATHS` too, so the contract's own illustration violates it.

## Affected Areas

All inside `REQUIREMENTS.md`. Files opened and verified:

| Location | State found | What this task touches |
|---|---|---|
| `REQUIREMENTS.md:856–894` (§5.5) | The **only** envelope example in the spec. Fields: `ROLE STEP TASK STACK EXPERTISE READ TEMPLATE WRITE REWORK RETURN` | The example block and the `EXPERTISE` sentence (line 892) |
| `REQUIREMENTS.md:896–913` (§5.5.1) | Return contract. Cited 9× from `agents/`, 1× from §7.11 | **Nothing.** Must not move or renumber |
| `REQUIREMENTS.md` — `MODULE:`/`PATHS:` | **Zero occurrences anywhere in the file** (grepped) | Both fields must be *introduced*, not merely added to an example |
| `REQUIREMENTS.md:1127–1290` (§7.3/§7.4/§7.5) | Step listings and a triage table. **No envelope examples at all** | Nothing — see Q1 |
| `REQUIREMENTS.md:1898–1922` (D2, D3, D4) | D2 fixes one `WRITE:`; D3/D4 make `READ:` the sole cross-artifact channel | Nothing edited; D4 is the reason AC-4's `SKILL` path must be *in the envelope* rather than assumed |
| `REQUIREMENTS.md:1021–1065` (§7.0.1) | Names which tool field binds at which layer | Cited by the new `EXPERTISE`/`SKILL` prose; not edited |
| `REQUIREMENTS.md:790–836` (§5.2, §5.3) | §5.2: `review-task` flags files outside the module's `paths`. §5.3: expertise skills are single files, "loaded by every step", capped ~150 lines | The reason `PATHS` is mandatory, and the evidence for Q2 |

Verified outside `REQUIREMENTS.md` as **evidence only** — not edited, all owned by TASK-019:

- `agents/*.md` — eight `tools:` lines, none contains `Skill`:
  `analyst`/`architect` → `Read, Write, Glob, Grep`; `reviewer` → `+ Bash`; the four engineers and
  `qa-engineer` → `Read, Write, Edit, Glob, Grep, Bash`. AC-1's premise is a fact, not an inference.
- The nine real envelope examples: `skills/task/step-{implement,qa,review}.md`,
  `skills/greenfield/step-{phases,tasks,plan-design}.md` (two), `skills/add-phase/step-define-phase.md`,
  `skills/bugfix/step-diagnose.md`, `skills/close-phase/SKILL.md`. **Only `step-implement.md:35–36`
  carries `MODULE` and `PATHS`.** Five planning/review envelopes carry no `EXPERTISE`; `step-review.md`
  carries no `STACK`, `MODULE`, `PATHS`, or `EXPERTISE`.
- `skills/task/SKILL.md:64` restates the field list inline — *"exactly as §5.5 specifies — `ROLE`,
  `STEP`, `TASK`, `STACK`, `EXPERTISE`, `READ`…"*. It goes stale the moment §5.5 gains fields. TASK-019's
  problem, but it is the one place a restatement (not a citation) will silently disagree.
- `templates/EXPERTISE.template.md` — single `SKILL.md`, no `references/`, no `scripts/`, explicit ~150
  line cap. `.claude/skills/` contains exactly two files, both single-file. Evidence for Q2.
- `skills/plan/SKILL.md` — read end to end as a file. Evidence for Q3.

Not in the catalogue: the envelope is not an artifact schema, so D-003's three-edit rule and
`scripts/check-templates.py` do not apply. This is genuinely a one-file change.

## Risks

- **§5.5.1 must not move.** Nine `agents/*.md` files and `REQUIREMENTS.md:1460` cite it for the return
  contract. An amendment that inserts a subsection *before* it, or promotes the field table to `§5.5.1`,
  re-points all ten citations at the wrong text — and they would still resolve, so nothing errors. This
  is the concrete form of the "renumbering is expensive" rule (PROJECT.md; D-021's neighbour). Amending
  §5.5's body and appending at most a `§5.5.2` avoids it entirely.
- **A mandatory-field table makes nine existing envelopes non-conformant on the day it merges.** That is
  the intent (D-019: the spec leads), but between TASK-015 merging and TASK-019 merging, `skills/` cites
  a contract it violates. If TASK-019 slips, the gap is a live inconsistency, not a pending one.
- **`MODULE` and `PATHS` are being introduced, not corrected.** Neither string exists in
  `REQUIREMENTS.md`. Anyone reading only §5.5 today would conclude `step-implement.md`'s `PATHS:` line is
  a local invention — and would be right. The amendment must define them, not merely list them, or §5.2's
  "`review-task` flags any file changed outside the task's module `paths`" keeps having no envelope field
  behind it.
- **`TEMPLATE:` in §5.5 reads `templates/IMPLEMENTATION.md`; every real skill writes
  `${CLAUDE_PLUGIN_ROOT}/templates/IMPLEMENTATION.md`.** A bare relative path does not resolve from a
  user project's cwd. Adding `SKILL:` as a path (AC-4) reproduces this defect unless the prefix question
  is settled — see Q4. This is inside `REQUIREMENTS.md`, so it is fixable here, but it is not in any AC.
- **The mandatory set is a judgement with a real cost.** Making `EXPERTISE` mandatory means the five
  planning envelopes must carry it — but planning steps (`create-phases`, `create-tasks`) run before a
  module is assigned, so there is nothing to name. A table that says "mandatory" without an escape makes
  those envelopes permanently non-conformant. Q5.
- Low: the `## Approach` reading of AC-3 narrows a criterion to one example. If the design or review
  reads AC-3 literally (§7.3/§7.4/§7.5), the task fails a criterion that its own module cannot satisfy.
  Q1 exists to settle this before implement, not at review.

## Open Questions

**Q1 — AC-3 names sections that contain no envelopes. Which reading governs?**
§7.3, §7.4 and §7.5 contain step listings only; the envelopes are in `skills/` (`plugin`, TASK-019,
D14). Two defensible readings: (a) AC-3 applies to the one envelope in `REQUIREMENTS.md` — the §5.5
example — and the nine in `skills/` are TASK-019's AC; or (b) AC-3 is mis-scoped and should be amended to
say so. Either is fine; guessing is not, because (b) changes what "done" means. **Recommendation: (a),
with AC-3 reworded to "the §5.5 example carries every field it declares mandatory."**

**Q2 — Is `EXPERTISE`-as-paths sufficient, or do some expertise skills need `Skill` invocation?**
Verified evidence says **paths are sufficient, by design**: `templates/EXPERTISE.template.md` specifies a
single `SKILL.md`, caps it at ~150 lines, and §5.3 says it is "loaded by every step". No bundled
`scripts/` or `references/` anywhere; both of this project's own expertise skills are one file. An
expertise skill with progressive disclosure would be outside the template orqestra ships. **But the
template is guidance, not enforcement** — a user could ship one with `references/`, and `Read` on the
`SKILL.md` would give the agent a pointer it cannot follow. Does §5.5 (a) state the single-file
constraint as a requirement of the `expertise` column, or (b) stay silent and accept the degradation?
This is the question TASK-019 AC-4 inherits, and (a) is cheap to write now.

**Q3 — Does naming the step skill's path in `READ` conflict with anything?**
Verified against `skills/plan/SKILL.md`, read as a file: no conflict, and it reads well as prose —
Invocation, Inputs, Output, Procedure, Return, When you cannot proceed, Rules, in that order, none of it
assuming it was invoked. D4 (read-list closure) positively *requires* it to be in `READ:` if the agent is
to use it at all. **One real hazard**: the frontmatter. `allowed-tools: Read, Write, Glob, Grep` and
`disallowed-tools: Agent, Edit, NotebookEdit, Bash` are inert when the file is read rather than invoked —
the binding list is `agents/analyst.md` `tools:` (D-024, §7.0.1). An agent reading those two lines as
prose can conclude it holds or lacks a tool it does not. They happen to agree for `plan`/`analyst` today,
so nothing is broken yet, but nothing keeps them agreeing. Should §5.5 say "read the skill's body; its
tool frontmatter does not bind you — §7.0.1 does"? Or is a separate `SKILL:` field (rather than a `READ:`
entry) the clearer place to hang that caveat?

**Q4 — Is `SKILL:` written as `${CLAUDE_PLUGIN_ROOT}/skills/<step>/SKILL.md` or bare?**
§5.5's existing `TEMPLATE:` line is bare and relative; all nine real skills use the
`${CLAUDE_PLUGIN_ROOT}` prefix. Whether that variable expands inside prompt text an orchestrator composes
is **not verified here** — I have no way to test it, and asserting either way would be a guess. The
answer decides both `SKILL:` and whether §5.5's `TEMPLATE:` line is itself a defect worth fixing in the
same edit.

**Q5 — Which fields are mandatory when there is no module?**
`create-phases` and `create-tasks` run before any task has a module, so `MODULE`, `PATHS`, `STACK` and
`EXPERTISE` have no values. Options: three tiers (always / when a task is in scope / when a module is
assigned), or two tiers plus an explicit "omitted because not yet determined" rule. AC-2 says an omission
must be "a contract violation rather than a judgement call" — that only holds if the table's conditions
are mechanical.
