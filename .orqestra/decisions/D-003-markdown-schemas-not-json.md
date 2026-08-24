---
id: D-003
type: decision
status: active
updated: 2026-08-24
area: schemas
supersedes: —
superseded_by: —
---

# D-003 — Markdown schemas, not JSON Schema

**When:** 2026-08-24 · pre-project · spec
**Decision:** Every inter-step artifact has a schema: exact frontmatter keys, closed vocabularies, ordered headings, fixed table columns. Expressed in Markdown and enforced by template plus orchestrator check — not by a validator binary.
**Why:** Schemas are what make skills deterministic in what they emit. JSON Schema would deliver that too, but only with a validator, which needs a runtime — contradicting D-001. Markdown contracts get most of the value at zero code, and are written grep-shaped so a checker is a drop-in later.
**Constrains:** Every new artifact type adds a row to §4.8 AND a template in `templates/`. A schema without a template is unfinished (D16).
