---
id: TASK-023
type: task
status: pending
updated: 2026-08-26
phase: PHASE-1
module: plugin
stack: markdown
origin: feature
bug:
depends_on: [TASK-013]
serves: [SC-5]
attempts: 0
---

## Goal

**Workspace mode gives false assurance.** TASK-008 closed the coverage hole; this closes the depth gap.

`main()` — template mode — checks missing keys, extra keys, missing headings, and heading order.
`check_instance()` checks only *missing* keys and *missing* headings. So a real artifact can carry
invented frontmatter, headings in the wrong order, or values outside a closed vocabulary and still pass
the check the project runs against its own workspace.

The gap matters because workspace mode is what grades real work: `status` derives stages from
frontmatter values, and a value outside its vocabulary sends an orchestrator to the wrong step silently.

## Acceptance Criteria

| id | criterion |
|---|---|
| AC-1 | `check_instance()` enforces everything template mode enforces: extra keys, extra headings, and heading order — verified by inducing each against a fixture |
| AC-2 | Closed vocabularies are validated where §4.8.1 declares them — `status`, `result`, `verdict`, `pr_state`, `blocked_reason` — so an invalid value fails rather than passing as free text |
| AC-3 | Frontmatter is parsed as YAML rather than by regex, and a malformed block fails with a clear message instead of being silently half-read |
| AC-4 | The 19 pre-existing failures are unchanged in kind by this task, or their change is stated — this task must not be the thing that makes historical drift look like a regression |

## Out of Scope

**Fixing the 19 drifted artifacts.** They are acknowledged historical drift and frozen where they record
work that actually happened (D5). Deciding their fate is its own task.

The §4.8.1 catalogue's vocabularies — `docs`, TASK-013, which lands first (D-019).
