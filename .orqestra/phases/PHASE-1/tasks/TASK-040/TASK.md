---
id: TASK-040
type: task
status: pending
updated: 2026-08-31
phase: PHASE-1
module: plugin
stack: markdown
origin: feature
bug:
depends_on: [TASK-037]
serves: [PHASE-3/SC-1]
attempts: 0
---

## Goal

**`BUG.md` must carry the `module:` the specification now says it carries.**

TASK-037 adds `module` to §4.8.1's `BUG.md` row and records the decision. This is the other two
thirds of that schema change — `orqestra-conventions` says a schema change is three edits always
together, and they span two modules, so docs led and this follows.

Until both land the schema is inconsistent: §4.8.1 lists a key `templates/BUG.md` does not have. That
window is deliberate and TASK-037 records why; closing it is this task.

**The provenance this fixes.** `MODULE: api` on a BUG dispatch is typed by a human at intake — *"which
module, if known"* — and lives as **prose** in `BUG.md`'s `## Scope`. It becomes a `module:` key only at
step-promote, on the *TASK*. So `skills/bugfix/step-diagnose.md` supplies four module fields today with
no frontmatter key behind them, and `check-envelopes.py` passes it because it keys on the scope key and
never reads frontmatter. A rule met by unchecked convention, not by a schema.

**"If known" stops being available.** Once `module` is a schema key it is required, so intake must
establish it rather than invite it. That was recorded as an open question on TASK-037 and folds in here,
because resolution (a) answers it: a bug whose module is unknown cannot produce a conformant
`step-diagnose.md` envelope, and the checker would reject it.

## Acceptance Criteria

| id | criterion |
|---|---|
| AC-1 | `templates/BUG.md` carries `module:` in its frontmatter, and **both** `python3 scripts/check-templates.py` **and** `python3 scripts/test-check-templates.py` exit 0 against §4.8.1's amended row — the harness is red in the same window and a literal reading of the checker alone would leave it failing |
| AC-2 | `skills/bugfix/step-intake.md` establishes the module rather than inviting it — a bug cannot be created without one, and the skill says what to do when the reporter does not know |
| AC-3 | The `## Scope` prose and the new key do not disagree: whatever intake writes in one is consistent with the other, or the prose stops carrying the module |
| AC-4 | `python3 scripts/check-envelopes.py` and the `config.md` `test_command` chain still exit 0, and `step-diagnose.md`'s `MODULE:` now has a frontmatter key behind it rather than a convention |
| AC-5 | `.orqestra/config.md`'s `test_command` comment is true when this lands — it currently names a window TASK-034 already closed, while a different check is red. Correct it or delete it as its own text instructs; do not leave it describing a failure that is not the one occurring |

## Out of Scope

`REQUIREMENTS.md` — TASK-037's, landed first (D-019). If this task finds the spec still wrong after it,
that is a finding to report, not an edit to make.

`scripts/check-envelopes.py`. Its docstring restates the warrant that was false; once this lands the
warrant is true and the docstring needs no change.

<!-- AC-5 ADDED 2026-08-31 by human decision (§8.2), found while implementing TASK-037.

     `.orqestra/config.md:34-40` says check-envelopes.py is "red BY DESIGN" on
     step-diagnose.md. TASK-034 closed that; run directly the checker exits 0. The comment
     also instructs "DELETE THESE LINES when the scan goes green" — it did, and nobody did.

     What makes it worth an AC rather than a note: the comment exists to stop a second
     failure hiding inside a familiar one, and right now the suite IS red for a different
     reason — the BUG.md window this task closes. It became the thing it was written to
     prevent.

     Folded here because config.md is `plugin`, TASK-037 is `docs`, and this task closes
     the window the comment should describe. The correction lands exactly when its
     condition is met. -->

Widening the change to other artifacts. `TASK.md` already carries `module:`; `PHASE.md` deliberately
does not (D-027).
