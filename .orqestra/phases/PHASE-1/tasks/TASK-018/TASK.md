---
id: TASK-018
type: task
status: pending
updated: 2026-08-26
phase: PHASE-1
module: docs
stack: markdown
origin: feature
bug:
depends_on: []
serves: [SC-5]
attempts: 0
---

## Goal

**`PROJECT.md` has no writer, so it stays a stub forever.**

`init` deliberately writes a stub and says the first design fills it. `design` declares `DESIGN.md` and
decision files as its outputs; nothing in its procedure touches `PROJECT.md`. D1 lists it as written by
"`init`, then `design` for `PROJECT.md`" — an assignment `design` does not implement.

This is load-bearing: every engineer and qa dispatch reads `PROJECT.md` for commands, layout, testing
rules, and traps. In this repo it is rich because it was written by hand. In any project that used
orqestra as documented, it would be empty, and every dispatch would read an empty file.

Same class as TASK-011: an assignment nothing performs, failing silently.

## Acceptance Criteria

| id | criterion |
|---|---|
| AC-1 | Exactly one skill owns `PROJECT.md` after `init`, and its procedure states when it writes and what it must fill |
| AC-2 | D1's row agrees with that procedure rather than describing an intention |
| AC-3 | The spec says what a dispatch does when `PROJECT.md` is still a stub — proceed, warn, or block — rather than leaving it to each agent |
| AC-4 | D-021's cost-to-retrieve test governs what goes in, so the owner has a rule rather than a blank page |

## Out of Scope

`skills/design` and `skills/init` — `plugin`, follows (D-019).
