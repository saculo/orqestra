---
id: TASK-015
type: design
status: done
updated: 2026-08-26
task: TASK-015
decisions: []
---

## Components

All five live inside `REQUIREMENTS.md` §5.5, between its heading (line 856) and §5.5.1 (line 896).
Nothing else in the repository is touched.

| # | Component | Responsible for | Serves |
|---|---|---|---|
| C1 | **The `EXPERTISE` definition, rewritten** | Saying that `EXPERTISE` carries skill *names* which the agent **invokes**, and stating the precondition that makes invocation possible: `Skill` in the dispatched agent's `agents/*.md` `tools:` — the only layer that binds for a whole subagent run (§7.0.1, D-024). Names what happens when the precondition is unmet: both `EXPERTISE` and `SKILL` are inert and the dispatch degrades silently to the bare persona | AC-1 |
| C2 | **The `SKILL` field, introduced and defined** | Naming the plugin step skill the agent invokes, namespaced (`orqestra:implement`), distinct from `STEP` because the two differ in practice (`STEP: review` → `SKILL: orqestra:review-task`). Consumer (Rule B, §4.4.1): the dispatched agent, which invokes it to obtain the procedure instead of relying on its persona to duplicate it (D4 — the envelope is the sole channel) | AC-4 |
| C3 | **The invocation rationale** | One short paragraph recording the measured fact: `${CLAUDE_PLUGIN_ROOT}` expands when a skill is **invoked** and stays a literal string when the file is **read**. A step skill obtained by `Read` therefore hands the agent a dead `TEMPLATE:` path. This is why `SKILL` is a skill name to invoke and not a file path to read. Same paragraph corrects §5.5's own `TEMPLATE:` line, which is bare and relative today and does not resolve from a user project's cwd | AC-5 |
| C4 | **The field table** | Stating, per field, whether it is always mandatory, conditionally mandatory under a **mechanical** condition, or step-specific — so an omission is checkable rather than a judgement call. Introduces and defines `MODULE` and `PATHS`, which appear nowhere in `REQUIREMENTS.md` today, each with its consumer named | AC-2 |
| C5 | **The envelope example, corrected** | Carrying every field C4 declares mandatory for the dispatch it depicts (an `implement` dispatch: a task with a module), in the fixed order C4 states — today it omits `MODULE`, `PATHS`, and `SKILL` | AC-3 |

## Interfaces

The envelope is the interface. Field order is fixed and this is the whole of it; `#` trailing comments
are illustrative, not part of the contract.

```
ROLE:      orqestra:<agent>          # namespaced; the module row's bare name + plugin namespace
STEP:      <pipeline step>           # the stage — appears in reports and artifact frontmatter
SKILL:     orqestra:<skill>          # INVOKED, never read
TASK:      PHASE-N/TASK-NNN          # exactly one scope field: TASK | PHASE | BUG
MODULE:    <module>
PATHS:     <module paths>
STACK:     <stack>
EXPERTISE: <name>, <name>            # bare project-skill names (§5.3), not paths, not namespaced
READ:
  <path>
  …
TEMPLATE:  ${CLAUDE_PLUGIN_ROOT}/templates/<ARTIFACT>.md
WRITE:     <path>
REWORK:    <artifact> — <findings>   # re-dispatch only
RETURN:    at most 10 lines, per the skill's Return contract.
```

Obligation classes for C4's table — the condition column must be decidable by looking at one thing:

| Field | Class | Condition, when conditional |
|---|---|---|
| `ROLE` `STEP` `SKILL` `READ` `TEMPLATE` `WRITE` `RETURN` | always mandatory | — |
| scope: exactly one of `TASK` `PHASE` `BUG` | always mandatory | the unit of work the workflow operates on |
| `MODULE` `PATHS` `STACK` `EXPERTISE` | mandatory **iff** the scope unit has a module assigned | `TASK.md`/`BUG.md` frontmatter carries `module:`. `create-phases` and `create-tasks` run before any task has one, so they omit all four — and that is conformant, not an exception |
| `EXPERTISE` | additionally: omitted when the module row's `expertise` cell is empty | the row, not the agent's judgement. §5.3's warn-once rule covers a *named* skill that is not installed; it does not license omitting the field |
| `REWORK` | re-dispatch only | unchanged (§5.5, existing prose) |

Field definitions that must be written, not merely listed (both are new to `REQUIREMENTS.md`):

- **`MODULE`** — the task's module: the routing key that resolved `ROLE`, `STACK`, `EXPERTISE` and
  `PATHS` from one `modules.md` row (D-004, §5.1). Consumer: the agent, which cites it, and `review-task`,
  which looks the row up to get `paths`.
- **`PATHS`** — the module's `paths`, and the boundary the agent may not write outside (§5.2, D2, D3).
  Consumer: the agent while writing, and `review-task`, which flags any changed file outside them —
  the check §5.2 already requires and today has no envelope field behind it.

## Structure

One file, one section. `REQUIREMENTS.md` §5.5's body — its fenced example and the three paragraphs
after it — is the entire write surface. The task's module is `docs`; `PATHS` is `REQUIREMENTS.md`,
`README.md`, and `README.md` needs nothing.

**§5.5.1 must not move, and nothing may be renumbered.** `§5.5.1` is cited ten times — nine from
`agents/*.md`, once from §7.11 — and every citation is a *return contract* citation. Inserting a
subsection between §5.5 and §5.5.1, or promoting the field table to `§5.5.1`, re-points all ten at the
wrong text, and they would still resolve, so nothing would error (PROJECT.md; D-021's neighbour). The
field table therefore lives inside §5.5's body, after the example. It is small enough that this reads
better anyway; a `§5.5.2` is permitted but unnecessary.

**Out of bounds, and deliberately left non-conformant.** `skills/` and `agents/` are the `plugin`
module and TASK-019's work (D14, D-019: the spec leads when a skill cites it). The nine envelopes in
`skills/` and `skills/task/SKILL.md:64`'s inline restatement of the field list become non-conformant
the day this merges. That is the intended sequencing, not a defect of this task — but the amendment
must not silently assume they have already been fixed.

Order within the edit: define the fields, then correct the example to match. An example written first
tends to fix the shape the table then has to describe.

## Decisions

**Q2 — §5.5 says nothing about how an expertise skill is laid out.** With `Skill` in the agent's
`tools:`, invocation resolves an expertise skill's own bundled `references/` and `scripts/` the way any
skill invocation does, so the degradation that motivated the question is gone: nothing about the
envelope depends on the skill being one file. §5.3 already caps authorship at ~150 lines as guidance;
restating it in §5.5 as a *contract requirement* would put enforcement in the wrong layer and create the
second copy that eventually disagrees (PROJECT.md, "never restate a rule you can cite").

**Q3 — no separate statement about step-skill frontmatter.** The hazard was that an agent *reading* a
`SKILL.md` would take its inert `allowed-tools`/`disallowed-tools` lines as prose about what it holds.
Now that the agent invokes the skill, those lines behave as §7.0.1 already describes and the agent never
sees them as text. AC-1's precondition sentence cites §7.0.1 once; that citation is the whole treatment
the layering needs here. A second paragraph would restate D-024.

**Q5 — three obligation classes, one mechanical condition each** (table above). "Mandatory when the
scope unit has a module" is decidable from `TASK.md` frontmatter, which the orchestrator has already
read to route the dispatch. The alternative — declaring all four unconditionally mandatory with a prose
escape — leaves the planning envelopes permanently non-conformant and puts a judgement call exactly
where AC-2 forbids one.

**`SKILL` is a namespaced name, not a path** (settles the plan's Q4). AC-5's fact makes a path wrong:
the envelope text an orchestrator composes may itself have been read rather than invoked, so a
`${CLAUDE_PLUGIN_ROOT}` prefix in it is not guaranteed to expand. A skill *name* has no such dependency,
and invoking it delivers the skill's body with its own paths already expanded — which is where the
`TEMPLATE:` path an agent can actually open comes from.

**No `decisions/D-NNN-*.md` from this design.** The envelope contract's normative home is §5.5 itself;
a decision file restating it would be a second copy of a rule that is already citable by number, which
is the failure mode `§7.7` was fixed for. The `Skill` grant that this contract presupposes is TASK-019's
to record, per the task's Out of Scope.

## Test Strategy

Behavioural, and all five are checkable by reading the amended §5.5 — this is a specification change,
so "observably true when done" means a reader or a dispatching orchestrator gets the right answer.

| AC | What proves it |
|---|---|
| AC-1 | §5.5 says `EXPERTISE` is invoked, and a reader asking "what must be true for that to work?" finds `Skill` in `agents/*.md` `tools:` named in §5.5 itself, with §7.0.1/D-024 cited. Grep: no surviving occurrence of "loads first" or any wording implying `Read` |
| AC-2 | For each of the nine envelopes in `skills/`, the table yields a yes/no verdict per field with no interpretation. Spot-check the two hardest: `step-review.md` (task with a module — must gain `MODULE`, `PATHS`, `STACK`, `EXPERTISE`) and `step-phases.md` (no module — conformant without them). Both verdicts must fall out of the condition column alone |
| AC-3 | Every field the table marks mandatory for an `implement` dispatch appears in §5.5's example, in the stated order. `MODULE:`, `PATHS:` and `SKILL:` now occur in `REQUIREMENTS.md`, each defined in prose and not only shown |
| AC-4 | A reader of the envelope alone knows which skill to invoke and that invoking is the action. `SKILL` is distinguishable from `STEP` — the `review` / `orqestra:review-task` divergence is the case that proves one field cannot serve both |
| AC-5 | §5.5 states the expansion asymmetry and ties it to the consequence (a read step skill carries a dead `TEMPLATE:`). §5.5's own `TEMPLATE:` line no longer shows a bare relative path |
| Regression | `grep -n '#### 5.5.1' REQUIREMENTS.md` still finds the return contract, and no heading between §5.5 and §5.5.1 was added or renumbered. `git diff --stat` touches `REQUIREMENTS.md` and nothing else |
