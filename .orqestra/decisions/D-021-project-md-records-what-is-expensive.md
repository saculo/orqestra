---
id: D-021
type: decision
status: active
updated: 2026-08-25
area: schemas
supersedes: —
superseded_by: —
---

# D-021 — `PROJECT.md` records what is expensive to find, and ships its git rules pre-written

**When:** 2026-08-25 · PHASE-1
**Decision:** `PROJECT.md` gains three headings — `## Testing`, `## Git and GitHub`, `## Traps` —
for a full set of `## Stack` · `## Layout` · `## Commands` · `## Conventions` · `## Testing` ·
`## Git and GitHub` · `## Traps` (§4.8.1). Its editorial rule is stated in the template and in §4.8.5:
**what does this fact cost to retrieve at the moment an agent needs it?** Cheap to find, leave it out.

`## Git and GitHub` is **body text in the template, not guidance** — the nine default rules ship
written, `init` copies them through literally (D16), and `design` extends rather than replaces them.

**Why:** The file loads on every dispatch, in every workflow, for every module, so its budget is the
scarcest in the system and the old four headings spent it on the wrong things — a `## Conventions`
section with no test for what belongs there fills with restated ecosystem defaults, and each such line
displaces one that would have saved a rework cycle. `## Traps` is the section that pays for itself: the
accumulated cost of past debugging is the one thing no model infers from reading the code.

The git rules are pre-written because they are asymmetric. §7.4.2 already tells the *orchestrator* how
to detect a dirty tree or an existing PR — but the destructive acts (discarding a human's uncommitted
work, force-pushing under an open review, opening a second PR for a task) are committed by *engineer*
subagents, which never read §7.4.2. Stating them in the project's own `PROJECT.md` puts the rule where
every agent already reads, at the moment the temptation is. A blank heading would have been filled by
whoever ran the first design, or not at all.

**Constrains:** `init` copies `## Git and GitHub` verbatim and may only append; it may not delete a
default rule. `design` fills the other six headings against the cost test and appends to the git
section. Anything true of one module and not the others goes in that module's expertise skills (§5.3),
never here.
