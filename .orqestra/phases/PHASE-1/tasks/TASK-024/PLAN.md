---
id: TASK-024
type: plan
status: done
updated: 2026-08-29
task: TASK-024
---

## Approach

Make every step file named in a SKILL.md index table resolve, by expressing cross-skill sharing as a
**plugin-root-qualified path** (`${CLAUDE_PLUGIN_ROOT}/skills/greenfield/step-*.md`) in the three rows
that are broken, and add a fifth `scripts/check-*.py` that parses every SKILL.md index table and fails
when a named file does not exist.

Two forms of sharing are defensible and AC-2 asks for a deliberate choice:

- **A — qualified path in the index table.** One file, zero drift, and it says out loud what the prose
  under each table already claims ("referenced, never copied"). There is a precedent in the tree:
  `skills/task/step-preflight.md:59` already points at `skills/greenfield/step-plan-design.md`
  cross-skill. Cost: the `file` column stops being uniformly skill-relative, so the checker must
  resolve two shapes; and a reader of `add-phase`'s table is sent into another skill's directory.
- **B — a real local file in each workflow.** Keeps the column uniform and each workflow
  self-contained. Cost: either a copy — which is exactly the drift `greenfield/SKILL.md:42-44` and
  `add-phase/SKILL.md:33-35` both name as orqestra's likeliest maintenance failure — or three
  pointer-only stub files, which is the same indirection as A plus three files and one extra hop.

A is chosen: the duplication B avoids is cosmetic (one column's shape), the duplication B risks is the
one the codebase has twice written a warning about. Neither option touches D-007 — no numbering
either way, order still lives in the index table.

The qualification must be `${CLAUDE_PLUGIN_ROOT}/...`, not the bare repo-relative form used at
`step-preflight.md:59`. Every other cross-file reference in `skills/` uses that variable (14+ sites,
all `TEMPLATE:`/`**Template**:` lines), and a bare `skills/...` path only resolves when the agent's
cwd happens to be the plugin repo — true while dogfooding via `--plugin-dir` (D-013), false once the
plugin is installed. Whether `step-preflight.md:59` is in scope to fix alongside is an open question
below.

The checker follows the shape the other four already share: CPython 3, stdlib only, `ROOT` derived
from `__file__`, findings collected then printed, exit `0` clean / `1` conformance failure / `2` the
inputs could not be read, and a module docstring that states why the check exists and that it is
dev-only with no runtime dependency from the plugin (D-001, D-015). It needs no `REQUIREMENTS.md`
row — `check-envelopes.py` and `check-decisions.py` have none — so the work stays inside `plugin`.

## Affected Areas

All inside the `plugin` module's paths (`skills/`, `scripts/`). Files opened, not inferred:

- `skills/add-phase/SKILL.md` — index table rows 29 and 30 name `step-tasks.md` and
  `step-plan-design.md`; neither exists in `skills/add-phase/`. Line 33 already says both are "the
  **shared files** from `greenfield` (D1) — referenced, never copied".
- `skills/bugfix/SKILL.md` — row 33 names `step-plan-design.md`; absent from `skills/bugfix/`.
  Line 36 makes the same sharing claim.
- `skills/greenfield/SKILL.md` — the six-row table all of whose files exist; the two shared targets
  are `skills/greenfield/step-tasks.md` and `skills/greenfield/step-plan-design.md`, both present.
- **Reconnaissance over all 22 skills is complete and the list is exactly the three TASK.md names.**
  Method: glob of `skills/*/*.md` (48 files) cross-referenced against every `step-*.md` token in
  `skills/` (39 occurrences across 8 files). The four skills with index tables are `greenfield`,
  `add-phase`, `bugfix`, `task`, `pr-comments`; `task`'s seven and `pr-comments`' six all resolve.
- `skills/qa/SKILL.md:35` and `skills/implement/SKILL.md:46,103` — unqualified `step-push.md` in
  **prose**, referring to `skills/task/step-push.md`. Not an index-table reference, so outside AC-1
  as worded, but the same hazard class.
- `skills/task/step-preflight.md:59` — repo-relative `skills/greenfield/step-plan-design.md`; the
  only existing cross-skill reference, and the model for option A.
- `scripts/check-decisions.py`, `scripts/check-envelopes.py` (read), `scripts/test-check-templates.py`
  (read) — the shared conventions listed above. `test-check-templates.py` establishes the harness
  shape: real script run as a subprocess against a throwaway fixture copy, asserting exit code and
  stdout text, so a case can break an input without touching the working tree.
- `.orqestra/project/PROJECT.md:14,42,77` — states `check-templates.py` is "the only executable file"
  and "the only automated check". Already stale (five scripts exist); belongs to no module and is not
  editable here.

## Risks

- **A checker that only globs `skills/*/step-*.md` inverts the check.** AC-1 is about references
  resolving, not about orphan files. A checker written the easy way (list files, look for a row)
  would pass today's three broken rows and fail nothing. The parse must start from the table.
- **The `file` column's regex is the whole checker.** After this change the column holds two shapes —
  bare `` `step-x.md` `` and `` `${CLAUDE_PLUGIN_ROOT}/skills/y/step-x.md` ``. A pattern that matches
  only the first silently skips exactly the rows this task added, reintroducing the defect it was
  written to prevent — the same failure mode TASK-008 closed in `check-templates.py`.
- **`skills/greenfield/step-plan-design.md:3` reads "Shared verbatim by `greenfield` and
  `add-phase`"** and does not name `bugfix`, though `bugfix/SKILL.md:36` claims the share. Pointing
  `bugfix` at that file makes a live inconsistency visible. Editing that line is arguably the
  *content* of the shared step, which TASK.md puts out of scope.
- **`step-tasks.md` is phase-shaped.** `skills/greenfield/step-tasks.md:5,9,17,31` dispatch
  `create-tasks` "for the first phase whose status is not `done`" and gate on `PHASE-1`. `add-phase`
  creates PHASE-N and needs that step; the reference resolves, but whether the file's phase-selection
  logic is correct for `add-phase` is content, not reference — flagged, not fixed.
- **`${CLAUDE_PLUGIN_ROOT}` resolution cannot be verified from this tree.** `Glob` over
  `.claude/skills/orqestra/*` returned nothing (symlinked and/or ignored), so the installed-load path
  is asserted from convention across 14 template references, not observed. The checker must therefore
  expand the variable to the repo root itself rather than depend on the runtime doing so.
- **Test harness cost.** Two of four scripts have a `test-check-*.py`; two do not. Whether AC-3's
  "runnable and cheap" implies a test harness for the new checker is unstated, and adding one roughly
  doubles the work.

## Open Questions

1. Does AC-1's "every step file named in every SKILL.md index table" extend to the **prose**
   references at `skills/qa/SKILL.md:35` and `skills/implement/SKILL.md:46,103`, and to the
   repo-relative path at `skills/task/step-preflight.md:59`? Narrow reading: index tables only, and
   those four lines stay broken-ish. Wide reading: every cross-skill file reference is qualified and
   the checker covers prose too — more robust, more surface, and the prose form is far harder to
   parse without false positives.
2. Does AC-3 require a `test-check-<name>.py` harness alongside the checker, matching
   `check-templates.py` and `check-envelopes.py`, or is the checker alone sufficient as with
   `check-decisions.py`?
3. `skills/greenfield/step-plan-design.md:3` will be wrong about who shares it once `bugfix` points
   at it. Correct that one line here, or leave it to a follow-up as "content of the shared step"?
