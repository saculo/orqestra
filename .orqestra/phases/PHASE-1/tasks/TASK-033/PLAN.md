---
id: TASK-033
type: plan
status: done
updated: 2026-08-30
task: TASK-033
---

## Approach

**Amend `REQUIREMENTS.md` so `diagnose` is a named step skill, in five places, in one edit.**

The substantive question first, because it changes what the amendment says.

**§4.8.1:584's row is not honest — it was written around an absence.** The evidence is in the
spec itself, not in TASK-034's wish. §5.5:947 states the envelope obligation table:
`ROLE STEP SKILL READ TEMPLATE WRITE RETURN` are **always** mandatory, with no condition and no
exemption. `skills/bugfix/step-diagnose.md` carries a real dispatch envelope (`ROLE:
orqestra:analyst`, `STEP: diagnose`, `TEMPLATE: ${CLAUDE_PLUGIN_ROOT}/templates/DIAGNOSIS.md`,
`WRITE: .orqestra/work/BUG-003/DIAGNOSIS.md`) and omits `SKILL`. So the spec **already requires**
`diagnose` to name a skill; §4.8.1:584 does not describe an intended absence, it records a place
the spec disagrees with itself. Amending it is restoring consistency, not adding a rule.

**The pointer's premise needs one correction, and it sharpens rather than weakens the case.**
§4.8.1:584 is *not* the only row whose "Written by" cell names a workflow-plus-step. Line 583 —
`BUG.md` | `` `bugfix` intake `` — has exactly the same shape. The distinction that decides which
is honest is **whether the step dispatches a subagent**. Grepping `ROLE:` across `skills/bugfix/`
returns exactly one hit, `step-diagnose.md:8`. `intake`, `reproduce`, `promote` and `handoff` run
inline in the orchestrator's own turn; they compose no triple, so §5.5 does not reach them and
"`bugfix` intake" is a truthful description of who writes `BUG.md`. `diagnose` alone is
envelope-dispatched, so `diagnose` alone needs a skill. **Line 583 stays as it is** — changing it
would be the partial-amendment failure in reverse.

**Skill name: `diagnose`**, invoked as `orqestra:diagnose`, so that §4.8.1's cell reads a bare
`` `diagnose` `` exactly as `plan`, `design`, `qa`, `review-task` do. This is the name TASK-034's
AC-3 must author for `check-envelopes.py` to reach exit 0 (`SKILL: orqestra:diagnose`), and it
follows D-012 — the folder name is the invocation name, so `skills/diagnose/` is the only spelling
that yields it. No alternative was defensible: `bugfix-diagnose` would be the sole hyphenated
compound in a 22-name inventory, and `root-cause` renames the step, which §7.3 and the `status`
table cite by the name `diagnose`.

**Alternative considered and rejected: amend only §4.8.1 and §5.1.1** (a literal reading of AC-1
and AC-2). Rejected because the grep below found three further statements that assume the absence,
two of them numeric. A spec that says "22 skills" twice while shipping 23 is worse than one that
says `` `bugfix` diagnose `` once, because the count reads as verified and nobody re-derives it.
AC-3's "agrees with both" is the licence to close all five.

**Alternative considered and rejected: a new subsection for non-pipeline step skills.** §5.1.1's
table is the one AC-2 names, and its own selection rule — the steps whose subagent is the same in
every module — admits `diagnose` without strain (it is always `analyst`). Inventing §5.1.2 to hold
one row splits a rule across two places, which `orqestra-conventions` names as the failure that
makes a rule disagree with itself.

**No section is renumbered** (AC-3). Every edit is a row appended to an existing table, a cell
rewritten in place, or a count corrected. Nothing is inserted above a numbered heading. Two of the
five edits are prose that a row addition falsifies, and they must move in the same commit:

| § | line | what assumes the absence | why it must change |
|---|---|---|---|
| §2 | 118 | `# 22 skills` in the repo tree | `skills/*/SKILL.md` globs to exactly 22 today; 23 after TASK-034 |
| §4.8.1 | 584 | `DIAGNOSIS.md`'s writer is `` `bugfix` diagnose `` | AC-1 |
| §5.1.1 | 777 | routing table has no `diagnose` row | AC-2 |
| §5.1.1 | 786 | "Only `implement` and `pr-comments` vary by module … **The other four**" | a sixth fixed-role row makes it five |
| §7.7 | 1447 | "Step skills" table omits `diagnose` | its own inclusion rule is *step skill that writes an artifact from a template*; `templates/DIAGNOSIS.md` exists, so `diagnose` meets it |
| §7.12 | 1642–1651 | inventory grid under `STEP SKILLS`, then "**22 skills.**" | same count, stated a second time |

§7.3:1196–1206 (the pointer's third target) needs **no edit to be consistent** — it names step
*files*, not skills, for every workflow, and `step-diagnose.md → DIAGNOSIS.md [GATE: diagnosis]` is
still true. AC-3 asks that it *agree*, and it does. Recording that here so a reviewer does not read
its absence from the edit list as an oversight, and so nobody "fixes" it into naming a skill, which
would make §7.3 the only walkthrough of six that mixes files and skills.

## Affected Areas

Everything below is inside `docs` = `REQUIREMENTS.md, README.md` (D14). Read, not inferred.

| file | what is actually there |
|---|---|
| `REQUIREMENTS.md:118` | `├── skills/ # 22 skills — the folder name IS the invocation name` |
| `REQUIREMENTS.md:583` | `` `BUG.md` `` \| `` `bugfix` intake `` — same shape as 584, **out of scope**, see Approach |
| `REQUIREMENTS.md:584` | `` `DIAGNOSIS.md` `` \| `` `bugfix` diagnose `` \| `bug` `root_cause_found` `task` \| four headings |
| `REQUIREMENTS.md:777–784` | routing table `\| step \| skill \| subagent \| expertise \|`; six rows — plan, design, implement, qa, review, pr-comments. No `diagnose` |
| `REQUIREMENTS.md:786–788` | the "other four" sentence the sixth row falsifies |
| `REQUIREMENTS.md:716` | "The orchestrator … reads the routing table in `config.md`" — the sentence that makes the boundary question below real |
| `REQUIREMENTS.md:942–960` | §5.5 obligation table; `SKILL` is **always** mandatory, and "the list is closed" |
| `REQUIREMENTS.md:1196–1206` | §7.3 walkthrough — step *filenames*, no skill names, no edit needed |
| `REQUIREMENTS.md:1441–1454` | §7.7 "Step skills" table, six rows, no `diagnose` |
| `REQUIREMENTS.md:1638–1653` | §7.12 inventory grid + "22 skills." |
| `README.md` | in `paths`, but grep found no `diagnose`/skill-count claim. **Not affected.** |

**Verified outside the module, for consequence only — not to be edited by this task:**

`skills/bugfix/step-diagnose.md` (the envelope missing `SKILL`), `templates/DIAGNOSIS.md` (exists;
§7.7's Template column can cite it), `scripts/check-envelopes.py:45` (`ALWAYS = ["ROLE", "STEP",
"SKILL", ...]`), and the 22-entry `skills/*/SKILL.md` glob that makes both counts checkable. All
`plugin` (D-010); TASK-034's, or nobody's.

**THREE ROUTING TABLES EXIST AND ONLY ONE IS MINE.** Stating it here because getting it wrong is a
module-boundary violation, not a style slip:

| table | module | this task |
|---|---|---|
| `REQUIREMENTS.md:777` | `docs` | **MINE. The only one I amend.** |
| `templates/config.md:50` | `plugin` | not mine — TASK-034 or a third task |
| `.orqestra/config.md:49` | **no module** — workspace state a workflow wrote (`modules.md` comment, lines 44–47) | not mine, and not anyone's as a deliverable |

**Which is authoritative: `REQUIREMENTS.md:777`.** The other two are *instances* of it —
`templates/config.md` the one `init` copies into a new project, `.orqestra/config.md` this
workspace's own copy. The split is deliberate (D-003: template plus the skill that writes it), and
the direction of authority is provable, not asserted: `.orqestra/config.md:53,58–64` still carries
`from the module's task_type` and a whole `task_type → subagent` table that **D-011 removed**. An
instance can drift from the spec and be wrong; the spec cannot drift from an instance. That drift
is pre-existing and outside this task.

## Risks

- **A partial amendment is worse than none, and this is the likely failure.** Five statements, two
  of them the same number written twice, 1500 lines apart. Fixing §4.8.1 and §5.1.1 alone leaves
  §7.12 asserting "22 skills." under a grid that visibly lists 23 — a contradiction in the section
  whose entire job is to be the inventory. The edit list above is the mitigation; a reviewer should
  check it against a fresh grep, not against this plan.
- **§7.7's table has an inclusion rule that is implicit.** I read it as *step skills that write an
  artifact from a template*, which admits `diagnose` and excludes `clarify`/`create-tasks` (they are
  §7.11's planning skills). If the intended rule is instead *steps of the delivery pipeline*, then
  `review-phase` at line 1454 does not belong either, and adding `diagnose` compounds an existing
  miscategorisation rather than fixing one. I could not find the rule stated anywhere; §7.7's prose
  covers only what the table deliberately omits (headings), not what it admits.
- **The §5.1.1 row commits `diagnose` to `expertise: module's`, which is only true because a BUG
  carries a module.** Verified: §5.5:949 makes `MODULE PATHS STACK EXPERTISE` mandatory iff the
  scope key is `TASK` **or `BUG`**, and `step-diagnose.md:10–14` supplies all four. So the cell is
  correct — but it is correct for a different reason than every other row in that table, where the
  module comes from `TASK.md`. If a future change makes `diagnose` run before a module is known,
  this row silently becomes false.
- **Amending §5.1.1 invites the same row into two files I must not touch.** Whether the workflow
  actually *needs* it there is genuinely unclear and is the open question below. Anyone reading
  AC-2 as "make the routing resolve" may reach for `templates/config.md`; that is `plugin`, and
  D14 makes it a different task.
- **`diagnose` in §5.1.1 sits in a table introduced by a subsection titled "Why there is no
  `task_type`".** The placement is pre-existing and awkward, and a reader may propose relocating
  the table to §5.1. That is a renumber in effect and AC-3 forbids it.

## Open Questions

1. **Does `templates/config.md:50` need a `diagnose` row for the workflow to function, and if so,
   whose task is it?** My reading says **no**, and it is worth stating why so the decision is made
   rather than defaulted: `step-diagnose.md` will carry `SKILL: orqestra:diagnose` **literally in
   its envelope** after TASK-034, so the bugfix orchestrator never performs a lookup. §5.1.1:716's
   "reads the routing table in `config.md`" describes the *delivery pipeline*, where the subagent
   varies by module and must be resolved; `diagnose` is a planning-workflow step whose agent is
   hardcoded. If that reading is wrong, a `diagnose` row is needed in `templates/config.md` and
   that is a **third task in `plugin`**, since TASK-034's four ACs do not mention it. A human should
   confirm the reading rather than let TASK-034 discover it at `check-envelopes.py`.
2. **Should §7.7 and §7.12 be amended by this task, or does AC-3's "agrees with both" stop at
   §7.3?** I have planned to include them, on the grounds that leaving "22 skills." stated twice is
   the partial amendment risk above. If the intent was a three-line change, say so — but then
   TASK-034 lands a 23rd skill against a spec that counts 22 in two places, and no AC anywhere
   catches it.
3. **`skills/diagnose/SKILL.md` will be the 23rd skill, but only once TASK-034 lands.** Do the
   counts at §2:118 and §7.12:1651 change **now** (this task, describing the intended end state,
   briefly wrong on disk) or **in TASK-034** (crossing into `docs`, which D-019 and TASK-034's own
   out-of-scope forbid)? Docs leads under D-019, so I plan the former — but it means
   `REQUIREMENTS.md` overstates the tree for the length of one task, which cuts against
   `orqestra-conventions`' rule not to describe orqestra as further along than it is.
