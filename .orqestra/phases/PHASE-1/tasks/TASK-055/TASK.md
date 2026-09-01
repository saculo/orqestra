---
id: TASK-055
type: task
status: pending
updated: 2026-09-01
phase: PHASE-1
module: plugin
stack: markdown
origin: feature
bug:
depends_on: []
serves: [SC-5]
attempts: 0
---

## Goal

**The configured test chain runs three of the repository's seven checks, and `&&` hides the rest of the
results as soon as one fails.**

`.orqestra/config.md:33`:

```
test_command: python3 scripts/check-templates.py && python3 scripts/test-check-envelopes.py && python3 scripts/check-envelopes.py
```

Omitted: `test-check-templates.py` (15 cases), `check-decisions.py` (31 decisions),
`check-step-refs.py` (43 references), `test-check-step-refs.py` (28 cases). Every one of them was built
by a task that needed it, and none of them gates anything — a regression in the decision schema or a
broken step reference merges while the configured suite reports green.

**The `&&` chain is the second half.** It is a short-circuit, so the first failure suppresses every
later result. A run that breaks two checkers reports one, gets fixed, and reports the next — turning
one diagnosis into several rounds. A test runner should say everything that is wrong on the first run.

**Third: the workspace scan has nowhere to live.** `check-templates.py --target .orqestra` fails on 19
historical artifacts, correctly, and D-030 makes it a diagnostic rather than a gate. But a permanently
red command that everyone is told to ignore is the condition under which a genuine new failure gets
read as historical noise. It needs a form in which new violations fail and known ones do not — which is
TASK-023's subject, and this task must not preempt it.

## Acceptance Criteria

| id | criterion |
|---|---|
| AC-1 | One runner — `scripts/check-all.py` — executes every check in the repository and is what `test_command` invokes |
| AC-2 | It runs **all** checks regardless of individual failures and reports every result, then exits nonzero if any failed |
| AC-3 | Adding a new checker requires no edit to `.orqestra/config.md` or to `templates/config.md`, so the omission cannot recur by someone forgetting |
| AC-4 | `templates/config.md`'s `test_command` ships the same runner, so a new project gets full coverage rather than this repository's historical three |
| AC-5 | The historical workspace scan is reported separately and explicitly, never silently folded into the pass/fail verdict |

## Out of Scope

**Making the workspace scan green.** TASK-023 and D-030. This task gives it a place to be reported; it
does not migrate 19 artifacts or design the grandfather list.

**Writing new checks.** TASK-048's envelope check, TASK-028's contract check and TASK-038's enumeration
check are each their own task. This one runs what exists and makes what comes next automatic.

**A CI configuration.** No CI exists yet; `test_command` is the interface, and a workflow file is
PHASE-5 (§12).
