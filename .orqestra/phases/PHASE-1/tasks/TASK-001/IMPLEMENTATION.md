---
id: TASK-001
type: implementation
status: done
updated: 2026-08-24
task: TASK-001
deviation: minor
files_changed: 3
---

## Changes

- **`scripts/check-templates.py`** (new, ~120 lines) — parses §4.8.1 and checks all 20 schema-bearing
  templates for frontmatter keys, heading presence, and heading order. Reports every violation with the
  artifact name and the specific problem; exits 0 / 1 / 2.
- **`.orqestra/config.md`** — `test_command: python3 scripts/check-templates.py`.
- **`.orqestra/modules.md`** — `scripts/` added to the `plugin` module's paths.

## Deviations

| severity | from design | what | why |
|---|---|---|---|
| minor | none planned | Added the `EXEMPT_MARKER` mechanism for rows opting out of common frontmatter | Discovered while running: `config.md` legitimately has no `status`/`updated`. The mechanism is plugin-side and shippable now; the catalogue flips to use it in TASK-007 |
| minor | none planned | Corrected `modules.md` to include `scripts/` | The task had nowhere to put its own deliverable — every module boundary excluded `scripts/`, so the work was outside D14 |

## Tech Debt

- **Two live conformance failures remain**, both on the catalogue side and therefore out of this
  module's reach (D14). Handed to TASK-007:
  1. `config.md` — the catalogue implies common frontmatter on every row; `config.md` is configuration,
     not project state, and should be marked exempt using the new marker.
  2. `TASK.md` — the catalogue row omits `bug`, which the template carries for the `origin: bug`
     backlink (§7.3.1).
- The checker validates **templates** only. Runtime artifact validation is the orchestrator's contract
  check (§4.4.5) and is not covered here.
