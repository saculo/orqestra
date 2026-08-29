---
id: D-026
type: decision
status: active
updated: 2026-08-29
area: structure
supersedes: —
superseded_by: —
---

# D-026 — A cross-skill reference's path shape follows how its file is loaded

**When:** 2026-08-29 · PHASE-1 · TASK-024 · design

**Decision:** a reference in `skills/` to a file in another skill is written in one of two shapes,
and which one is not a choice:

| the reference sits in | shape | 
|---|---|
| a step-index `file` cell in a `SKILL.md` | `${CLAUDE_PLUGIN_ROOT}/skills/<skill>/step-<x>.md` |
| prose in a `SKILL.md`, or anywhere in a `step-*.md` | `skills/<skill>/step-<x>.md` |

A reference to a file in the **same** skill stays a bare filename — `step-push.md` — resolved
against the containing skill's directory.

**Why:** `${CLAUDE_PLUGIN_ROOT}` expands at skill invocation and **not** on `Read` (D-025). A
`SKILL.md` body is loaded by invocation, so the variable arrives expanded and an index cell can be
handed straight to `Read` as an absolute path — which is what an index cell is for (D-007: order and
navigation both live in that table). A `step-*.md` is loaded by `Read`, so the same variable arrives
as literal text and a qualified path there is inert. Prose is a citation rather than a `Read`
argument, so it takes the readable form in both places and never depends on expansion.

The alternative — one uniform shape everywhere — fails in one direction or the other: the variable
form breaks inside step files, and the bare repo-relative form only resolves while the cwd happens
to be the plugin repo, which is true under `--plugin-dir` and the skills-dir load (D-013) and false
for an installed plugin.

Copying a shared step file into each workflow was rejected: `greenfield/SKILL.md` and
`add-phase/SKILL.md` both already name divergence between the two planning tails as orqestra's
likeliest maintenance failure.

**Constrains:**

- Never write a bare filename to reach another skill's file. It resolves against the containing
  skill's directory, so it silently names a file that does not exist — the exact defect TASK-024
  closed in three index rows and four prose lines.
- Never put `${CLAUDE_PLUGIN_ROOT}` inside a `step-*.md`. It is read as a file, so the token arrives
  literal and the path is unusable (D-025).
- A new cross-skill reference must be added in the shape its location dictates, and the reference
  checker in `scripts/` enforces both the existence and the shape. A reference the checker does not
  see is a reference that will rot; if a new reference form is introduced, extend the checker in the
  same change.
- The check runs from references to the filesystem, never the reverse. Listing `step-*.md` files and
  looking for rows inverts it, and would pass a tree with three dangling references in it.
