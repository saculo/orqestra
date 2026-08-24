---
id: TASK-007
type: implementation
status: done
updated: 2026-08-24
task: TASK-007
deviation: none
files_changed: 1
---

## Changes

`REQUIREMENTS.md`:

- **§4.8.1** — `config.md` marked **no common frontmatter**, using the marker TASK-001 built into the
  checker; the `TASK.md` row gains `bug`. These were the two defects TASK-001 handed over, and with them
  fixed the conformance check exits 0.
- **§4.8 preamble** — "Twenty artifacts" → "Twenty-two", and the exemption is documented *with its
  reason*: `config.md` is configuration, not project state, so `status` and `updated` on it would be
  fields nothing reads, which Rule B forbids.
- **§7.12** — inventory rebuilt from the shipped tree: 15 → 22, old `orchestrate-*` names replaced with
  the real folder names, and the missing `approve`/`reject`/`unblock`/`clarify` added. Now also
  documented as the command list, since the folder name is the invocation name.
- **§1.4, §7.0** — "~15 skills" and "Fifteen skills" → 22.
- **§4.7.1** — `§11.6` reworded; §11 is a numbered list, so `11.6` never resolved to a section.
- **§5.4** — agent dispatch namespacing recorded (D-014) where a reader looking up agents will find it,
  rather than only in §5.5.
- **§4.8.4** — the `init --migrate` claim removed. No such flag exists, and the section now says why a
  migration path is deliberately absent rather than merely missing.

## Deviations

_none_

## Tech Debt

**Two config keys have no consumer, and neither is fixable from this module** (D14 — both live in
`skills/` or `templates/`, which are `plugin`):

1. **`no_commit`** — §4.6 states it disables artifact commits entirely. No skill reads it, so setting it
   would silently do nothing. Either the orchestrators must honour it or §4.6 must drop the claim.
2. **`artifact_commit_scope`** — declared in `templates/config.md`, read by nothing. A textbook Rule B
   violation (§4.4.1), and the exact failure nit's ADR-0007 was written about.

**Recommended as a task in PHASE-2, not PHASE-1.** Artifact commits are first exercised by the planning
workflow, so that is where the fix is verifiable. Creating it here would be inventing scope PHASE-1 does
not describe.
