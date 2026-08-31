---
id: TASK-042
type: task
status: pending
updated: 2026-08-31
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

**§5 sends the orchestrator to the wrong file for the routing table.**

`REQUIREMENTS.md:717`:

> The orchestrator never decides these by prose or intuition — it reads the routing table in
> `config.md`…

The routing table it means is `modules.md`'s — the module registry, whose row supplies the agent,
stack, expertise and paths for a dispatch (`:209`, `:727`). `config.md` has a routing table too, a
different one: step → skill → subagent for the delivery pipeline. An orchestrator following `:717`
literally looks in the wrong place for the row that resolves a module.

Found by TASK-037's qa, ruled out of its scope by its review — it fails no criterion of that task and
predates it, traced to `a660327`. Filed rather than left in a review artifact, because a defect
recorded only in `REVIEW.md` is one nobody reads again.

**Why it has not bitten.** Both files exist and both contain something called a routing table, so a
reader who already knows the system substitutes the right one silently. That is what makes it a
documentation defect rather than a broken workflow, and also why it survived.

## Acceptance Criteria

| id | criterion |
|---|---|
| AC-1 | §5:717 names the file that actually holds the row it describes |
| AC-2 | The two routing tables are distinguishable wherever the spec refers to either — a reader can tell which is meant without knowing the answer already |
| AC-3 | No other place sends a reader to the wrong one. Checked by searching for the *concept* — "routing", "the row", "resolves", "registry" — not only for the phrase "routing table", since a check anchored on one surface form misses another |
| AC-4 | Nothing is renumbered; ~90 files cite §-numbers |

## Out of Scope

`config.md` and `modules.md` themselves, and `templates/` copies of either — all `plugin` or workspace
state. This task corrects what the specification says about them (D14, D-019).

Merging or renaming either table. Two routing tables answering two different questions may well be
right; this task makes the spec say which is which.
