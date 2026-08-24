---
id: D-006
type: decision
status: active
updated: 2026-08-24
area: state
supersedes: —
superseded_by: —
---

# D-006 — One file per decision, plus a generated index

**When:** 2026-08-24 · pre-project · spec
**Decision:** `decisions/D-NNN-*.md` one per decision, with `decisions/INDEX.md` regenerated from them. Every dispatch reads the index; individual files are opened only when a row touches the work.
**Why:** A single growing DECISIONS.md is a merge-conflict magnet, cannot be reverted per-decision, and is read in full on every dispatch — getting more expensive exactly as the project gets longer. The index keeps awareness unconditional and detail conditional.
**Constrains:** Decision files are append-only. Reversing one writes a new file and flips the old row to `superseded`. The index is regenerated, never hand-edited.
