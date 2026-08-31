---
id: TASK-037
type: task
status: pending
updated: 2026-08-30
phase: PHASE-1
module: docs
stack: markdown
origin: feature
bug:
depends_on: []
serves: [PHASE-3/SC-1]
attempts: 0
---

## Goal

**The specification says a `BUG` carries `module:`. It does not, and a checker now enforces the claim.**

Found by TASK-033's review (F-1), verified against `templates/BUG.md`, whose frontmatter is `id`,
`type`, `status`, `updated`, `bug`, `severity` — no `module:`.

The claim appears twice and has already been built on:

| where | what it says | shipped by |
|---|---|---|
| §5.5:957 | the four module fields are "mandatory **iff** the scope key is `TASK` or `BUG` — those units carry `module:` in their frontmatter" | TASK-029 |
| §5.1.1:795 | "a `BUG` carries `module:` too, so §5.5's conditional class is mandatory there as well" | TASK-033 |

`scripts/check-envelopes.py` encodes the first (TASK-030). So a `BUG`-scoped envelope **must** carry
`MODULE`/`PATHS`/`STACK`/`EXPERTISE`, and nothing can derive them: `skills/bugfix/step-diagnose.md`
supplies four values today with no frontmatter key behind them.

**Three steps passed this.** TASK-029 wrote it, TASK-030 encoded it, TASK-033 repeated it, and every
qa and review in between passed. A false premise stated once becomes a rule, then a check.

## Acceptance Criteria

| id | criterion |
|---|---|
| AC-1 | §4.8.1's `BUG.md` row lists `module` among its frontmatter additions, so the specification says a bug carries its module — the claim at §5.5:957 and §5.1.1:795 becomes true rather than being softened |
| AC-2 | A decision records that a bug carries its module in frontmatter, and why — so the next reader finds the reason rather than inferring it from a catalogue cell |
| AC-3 | The specification is internally consistent afterwards: §4.8.1, §5.5:957, §5.1.1:795 and §7.3 agree, checked by reading the workflow end to end rather than by grepping one phrase |
| AC-4 | No other place in `REQUIREMENTS.md` still asserts the version that turns out to be wrong — checked by search, and by set-difference where the claim is an enumeration |

<!-- AMENDED 2026-08-31, by human decision (§8.2), after plan traced the module's real source.

     THE FINDING PLAN RETURNED, and it is finer than the task was written for: the
     OBLIGATION is right and satisfiable — MODULE/PATHS/STACK/EXPERTISE are mandatory for a
     BUG dispatch and the value exists. What was false is the WARRANT under it. `MODULE: api`
     comes from a human typing it at step-intake ("which module, if known"), lives as PROSE in
     BUG.md's `## Scope`, and becomes a `module:` KEY only at step-promote — on the TASK.
     check-envelopes.py keys on the scope key and never reads frontmatter, so step-diagnose.md
     passes today by unchecked convention rather than by meeting a rule.

     RESOLUTION (a) CHOSEN: make the specification TRUE rather than softening it. A bug is
     diagnosed against a module; the frontmatter is where that belongs. So the claim stays and
     BUG.md changes to match it — which also means nothing in §5.5, §5.1.1 or D-027 needs
     correcting, because the warrant becomes true.

     SPLIT, docs leading. `orqestra-conventions` says a schema change is three edits always
     together — §4.8's catalogue row, the templates/ file, and the skill that writes it. Here
     they span two modules and D14 forbids one task doing both. The two rules cannot both be
     honoured, and this is the project's first schema change to span modules. Chosen: docs
     leads (D-019), TASK-040 follows, and the schema is briefly inconsistent between the two
     merges. That window is accepted deliberately, not overlooked.

     Q3 FOLDS INTO TASK-040 rather than being filed separately. Once `module` is a schema key,
     intake MUST populate it — "if known" stops being available — so the question answers
     itself under (a) and a separate task would overlap.

     ALSO CORRECTED, from plan: this premise predates TASK-029. TASK-015/DESIGN.md:52 already
     asserted it, so the orchestrator's "TASK-029 wrote it, TASK-030 encoded it, TASK-033
     repeated it" was three links of four. -->

## Out of Scope

Deciding by fiat. Both resolutions are defensible — a bug is diagnosed *against* a module, so
`module:` may belong in `BUG.md`; or a bug's module is genuinely resolved elsewhere and the spec
should say where. The design step chooses, with the reason recorded.

`templates/BUG.md` and `skills/bugfix/step-intake.md` — both `plugin`, both **TASK-040's**, which
depends on this. Docs leads (D-019).

`scripts/check-envelopes.py`'s docstring, which restates the warrant. `plugin`, and it becomes true
rather than wrong once TASK-040 lands, so it needs no edit at all.
