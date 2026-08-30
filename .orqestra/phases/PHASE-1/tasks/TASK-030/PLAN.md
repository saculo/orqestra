---
id: TASK-030
type: plan
status: done
blocked_reason:
updated: 2026-08-30
task: PHASE-1/TASK-030
---

## Approach

Two of AC-1's three moving parts are ready; the third is not, and it is not a small third.

**Ready — the `PROJECT` scope work.** `skills/greenfield/step-phases.md` carries zero scope fields, which
`check-envelopes.py` reports as `0 scope fields`. TASK-029 is merged and §5.5 now admits `PROJECT` as a
fourth scope value (D-027), so the envelope gains a `PROJECT:` line immediately after `SKILL:`, carrying
the project name from `.orqestra/config.md` `project:` — for this repo, `orqestra`. Correspondingly
`check-envelopes.py` learns the amended rule, which is two changes, not one:

1. `PROJECT` joins the scope set, so exactly-one-of becomes four-way.
2. The conditional class stops being merely all-or-nothing and becomes **scope-dependent**:
   mandatory iff the scope key is `TASK` or `BUG`, and **must be omitted** under `PHASE` and `PROJECT`
   (§5.5 obligation table, row 3). §5.5 was made prescriptive on exactly that point so the checker would
   not have to guess (TASK-029 F-2). `check()` already receives the full field list, so the scope key is
   available without changing its signature or its inputs.

`scripts/test-check-envelopes.py` is the place that proves the checker would notice a violation not
currently in the tree, so it moves with the checker — the existing cases assert the *old* all-or-nothing
rule and one of them (`"PHASE is an accepted scope"`) is only accidentally still correct.

**Not ready — the `SKILL` work.** See `## Open Questions`; it is why this plan blocks.

**AC-2** is independent and small: `.orqestra/config.md:33`'s `test_command` names `check-templates.py`
alone. Adding `check-envelopes.py` (and, defensibly, its test) makes a non-conformant envelope fail the
suite. Alternative considered and rejected: adding all six scripts at once — that is a larger change than
AC-2 asks for and would fold in `check-decisions.py`/`check-step-refs.py` results this task has no
mandate to make green.

Alternative considered for AC-1 as a whole: fabricate a plausible `SKILL:` value for `step-diagnose.md`
so the checker goes green. Rejected — TASK.md's Out of Scope forbids exactly this, and under D-025 the
value would be *invoked*, so a name pointing at nothing degrades the dispatch to a bare persona (§5.5,
the "worst failure shape available").

## Affected Areas

Files read, not inferred:

- `scripts/check-envelopes.py` — `SCOPE = ["TASK", "PHASE", "BUG"]` (line 31); the conditional check
  (lines 71–74) is all-or-nothing and scope-blind. The docstring's four-class summary (lines 10–17)
  restates the rule and would go stale with the code.
- `scripts/test-check-envelopes.py` — 19 cases; the scope cases (lines 50–58) and conditional cases
  (lines 60–64) both encode the pre-D-027 rule.
- `skills/greenfield/step-phases.md` — envelope at line 13. `ROLE STEP SKILL READ TEMPLATE WRITE RETURN`
  present, no scope field, no conditional fields. Adding `PROJECT:` alone makes it conformant.
- `skills/bugfix/step-diagnose.md` — envelope at line 8. `BUG MODULE PATHS STACK EXPERTISE` present and
  correct; `SKILL:` absent.
- `.orqestra/config.md` — line 33, `test_command: python3 scripts/check-templates.py`. Outside every
  module's `paths` by design (`modules.md`, the `.orqestra/` comment), **but** TASK-001 set this exact
  line as a `plugin` task and its PLAN/DESIGN/IMPLEMENTATION all name it. Precedent, not a new licence:
  a task may write the workspace's own config where an AC names it. `templates/config.md:38` has an
  empty `test_command` and must stay empty — it seeds *other* projects.
- `REQUIREMENTS.md` §5.5 (lines 856–963) — read for the amended obligation table. Not edited (docs
  module, D14; and TASK.md's Out of Scope).

Verified counts: 10 envelopes across 9 files (`step-implement.md` has one envelope; its two `REWORK:`
lines at 57–58 sit in a later fenced block the parser has already stopped at). `review-task/SKILL.md:127`
is a return-contract line, not `ROLE:`-anchored, so it is not scanned.

**Verified, and it matters:** no existing envelope carries conditional fields under a `PHASE` scope
(`close-phase/SKILL.md:38`, `greenfield/step-tasks.md:14`, `add-phase/step-define-phase.md:16` are all
scope-only). Tightening the rule to "must be omitted" therefore breaks nothing currently in the tree.

**Verified, and it disproves TASK.md:** TASK-024 never touched diagnose. `grep -c diagnose` over
`TASK-024/TASK.md` returns 0; its goal was three *step-file references* resolving, and its Out of Scope
says "the content of the shared steps". `skills/diagnose/` does not exist — 22 skill folders, none named
`diagnose`. TASK-024's own `REVIEW.md:90` hands "the absent `skills/diagnose/`" to TASK-030 explicitly,
which is where TASK.md's dependency row came from, but a review note is not a scope grant.

## Risks

- **`EXPERTISE` is not decidable from the envelope.** §5.5 row 4 says it is omitted when the module row's
  `expertise` cell is empty. A checker that requires all four conditional fields under `TASK`/`BUG` will
  therefore be wrong for a module with no expertise skills. No such module exists in `modules.md` today,
  so the current tree cannot show the bug — it would surface in a consuming project.
- **The docstring is a second copy of the rule.** `check-envelopes.py` lines 10–17 restate the obligation
  classes in prose. Changing the code and not the docstring leaves the file disagreeing with itself, which
  is the failure orqestra-conventions names directly.
- **Widening `test_command` can turn the suite red for reasons this task did not cause.** Nothing has run
  `check-decisions.py` or `check-step-refs.py` as part of `test_command` before; scoping the addition to
  `check-envelopes.py` keeps the blast radius to this task's own criterion.
- **`check-envelopes.py` cannot be run from this step** — the analyst holds no `Bash`. Every claim above
  about which envelopes fail is derived by reading the checker's logic against the grepped field lists,
  not by executing it. qa must execute it.
- **AC-1's wording ("all ten envelopes") survives a split badly.** If the diagnose half is carved out, the
  criterion must be reworded, or it fails again at qa for the same reason TASK-019's AC-5 did.

## Open Questions

1. **The diagnose blocker is unresolved, and this is the block.** TASK.md says `step-diagnose.md` is
   blocked on TASK-024; that premise is false (see `## Affected Areas`). The blocker is live. Adding
   `SKILL:` requires *naming a skill that must be authored* — `skills/diagnose/SKILL.md`, giving the
   bugfix workflow's diagnose step its procedure. Of the three dispositions:

   - **(a) author `skills/diagnose/` inside TASK-030** — rejected. Authoring a step skill is plugin-module
     work and would not be a boundary violation on its own, but it does not stop there. `REQUIREMENTS.md`
     §4.8.1 line 584 names `DIAGNOSIS.md`'s writer as "`bugfix` diagnose" — a workflow-plus-step, and the
     only row in the catalogue that does not name a skill. Every other row names one (`plan`, `design`,
     `qa`, `review-task`). Creating `orqestra:diagnose` makes that row wrong, and §5.1.1's step→skill
     routing has no `diagnose` line either. That is a `REQUIREMENTS.md` edit, which is the `docs` module
     and the architect's (D14, D-019: spec-first when a skill cites it). It is also a bigger change than
     "make envelopes conform" — a real procedure, Inputs/Output/Procedure/Return/Rules, not a stub, since
     under D-025 a `SKILL` value is invoked and naming a stub is inventing a value with extra steps.
   - **(b) `needs-splitting`** — **this is the recommendation.** AC-1 bundles two unrelated changes: one
     envelope needs a field that now exists, the other needs a skill and a spec amendment that do not.
     Split into TASK-030 (the `PROJECT` scope work + AC-2, deliverable today) and a successor pairing
     `skills/diagnose/SKILL.md` with the §4.8.1/§5.1.1/§7.3 amendments — a two-module change, so a docs
     task the plugin task depends on.
   - **(c) `criterion-unsatisfiable`** — true of AC-1 *as written*, but it understates the cause: the
     criterion is not unreachable in principle, it is bundled with work nobody has scoped. Recording it
     as unsatisfiable would lose the reason.

2. **Is `.orqestra/config.md` writable by this task?** It belongs to no module by deliberate design, so
   AC-2 asks for an edit outside `PATHS`. TASK-001 did exactly this edit and shipped, so the precedent is
   established — but it has never been written down as a rule. A human should confirm the precedent holds
   rather than have the reviewer flag it as an out-of-paths `major` finding (§7.8.1, D2).

3. **Does `test_command` gain `test-check-envelopes.py` as well?** AC-2 names only `check-envelopes.py`.
   The behavioural test is what proves the checker still catches violations after this task changes it,
   so running only the checker leaves the more valuable half unrun. Confirm the intent before qa grades it.
