---
id: TASK-022
type: task
status: pending
updated: 2026-08-26
phase: PHASE-1
module: plugin
stack: markdown
origin: feature
bug:
depends_on: []
serves: [PHASE-4/SC-1]
attempts: 0
---

## Goal

**The PR review-thread fetch is not a valid command.**

`skills/pr-comments/SKILL.md` runs:

```
gh pr view <n> --json reviews,comments,reviewThreads
```

`reviewThreads` is not a `gh pr view` JSON field. Verified locally on 2026-08-26 against `gh` in this
environment: `Unknown JSON field: "reviewThreads"`. The command fails outright, so the workflow's first
step cannot run — and thread resolution state, replies, and thread mutations are not available through
`gh pr view` at all. They need `gh api graphql`.

## Acceptance Criteria

| id | criterion |
|---|---|
| AC-1 | Threads are fetched with a command that succeeds against a real PR, returning thread id, resolution state, path, line, and each comment |
| AC-2 | Replying to a thread and resolving it both work against a real PR, verified by round-tripping one |
| AC-3 | The three comment kinds GitHub distinguishes — review threads, review-level comments, issue comments — are handled distinctly rather than conflated |
| AC-4 | A `gh` version or auth failure blocks with a clear reason instead of a raw error |

## Out of Scope

The triage and resolution logic. The classification model is sound; this fixes how threads are fetched
and mutated.
