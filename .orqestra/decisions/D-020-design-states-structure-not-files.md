---
id: D-020
type: decision
status: active
updated: 2026-08-25
area: schemas
supersedes: —
superseded_by: —
---

# D-020 — `DESIGN.md` states structure, not files

**When:** 2026-08-25 · PHASE-1 · after nine designs written against the old schema
**Decision:** `DESIGN.md`'s third heading is `## Structure` — prose naming the areas, layers, and
boundaries the work lands in. The old `## File Plan` table (`path` · `action` · `purpose`) is removed
from the catalogue (§4.8.1), from §4.8.2, and from the template. **The architect no longer names files
to create; the engineer chooses placement inside the boundaries the design sets.**

**Why:** Two failures, and the second is the larger one.

- **A path list goes stale on every merge.** Preflight's freshness check (§7.4) opened with "do the
  files in `## File Plan` exist as the plan expects" — so the check spent its attention on filenames
  rather than on whether the design still held. Every unrelated task that merged first could invalidate
  a design that was in fact still correct.
- **An engineer handed a checklist satisfies the checklist.** The file plan quietly became the
  definition of done, displacing the acceptance criteria — which is backwards, because `AC-N` is what
  `qa` measures and what `PHASE_SUMMARY.md` rolls up. Nothing in the pipeline ever verified the file
  plan, so it carried authority it had not earned.

The architect reads the code once; the engineer reads it while typing. Placement is the engineer's
information advantage, and the design was spending its own altitude to overrule it.

**What did not change:** the boundary. The whole change still lands inside the task's module `paths`
(§5.2, D2), and `review-task` still flags any file in the diff that falls outside them. What moved is
who picks the filename — not who owns the constraint.

**Constrains:**

- `design` must not emit paths for files that do not yet exist; a path appears in `## Structure` only as
  an existing thing being extended.
- `plan`'s `## Affected Areas` is reconnaissance over existing code, not a forecast of files to create.
- `implement` derives its build order from `## Components` and `## Structure`, and chooses paths from
  `PROJECT.md`'s `## Layout`.
- **File placement is no longer a deviation.** It was listed as the canonical `minor` deviation in
  `IMPLEMENTATION.md`; with no file plan to depart from, that classification is incoherent. Placement
  belongs in `## Changes`; only a boundary actually crossed goes in `## Deviations`.
- `review-task` must not raise placement as a `design`-lens finding. It is judged against
  `PROJECT.md`'s layout and the module's conventions — and against the module `paths` boundary (§5.2),
  which review does still check.
- The nine `DESIGN.md` files already written under PHASE-1 carry the old heading and are frozen (D5) —
  they are not migrated, and the schema is read forward, not backward.
