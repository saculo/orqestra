---
id: TASK-001
type: plan
status: done
updated: 2026-08-24
task: TASK-001
---

## Approach

Parse the §4.8.1 catalogue out of `REQUIREMENTS.md` at run time and check every `templates/` file
against it. The catalogue is the single source of truth (D-003), so the check must **read** it rather
than restate it — a checker with its own copy of the rules is a second source that drifts, which is the
failure this whole project keeps eliminating.

Python 3 for the parsing. It is dev-only tooling, not shipped behaviour — see Risks.

## Affected Areas

- `scripts/check-templates.py` — new, the whole deliverable
- `.orqestra/config.md` — `test_command` gains the invocation
- `.orqestra/modules.md` — `scripts/` must join the `plugin` module's paths; it belongs to none today

Verified by reading `REQUIREMENTS.md` §4.8.1 and every file in `templates/`.

## Risks

- **D-001 says no code.** A conformance checker is arguably code. The distinction that resolves it: the
  plugin has no runtime dependency on this script — users who install orqestra never execute it. It is
  a development test, like `claude plugin validate`. Recorded as D-015 rather than left implicit.
- **The catalogue may itself be wrong.** Where a template and the catalogue disagree, the fix may belong
  on the catalogue side — which is `REQUIREMENTS.md`, the `docs` module, and therefore a different task
  (D14). This task cannot fix those, only report them.
- **Heading extraction must ignore fenced code and HTML comments.** Templates carry their guidance in
  comments and their table shapes in fenced blocks; a naive `^## ` scan would read those as headings.

## Open Questions

_none_
