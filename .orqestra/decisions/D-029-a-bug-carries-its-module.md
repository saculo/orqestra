---
id: D-029
type: decision
status: active
updated: 2026-08-31
area: schemas
supersedes:
superseded_by:
---

# D-029 — A `BUG` carries `module:` in its frontmatter

**When:** 2026-08-31 · PHASE-1/TASK-037 · design
**Decision:** `BUG.md`'s frontmatter carries **`module:`** — §4.8.1's row lists it, `templates/BUG.md`
carries the key, and `bugfix` intake **establishes** it rather than inviting it. A bug names the one
module it belongs to, exactly as a task does (§5.2). A bug whose module is unknown is not creatable;
"which module, if known" is not available once the key is part of the schema.
**Why:** `MODULE` `PATHS` `STACK` `EXPERTISE` are mandatory on a `BUG` dispatch, and the scope key alone
decides that (§5.5, D-027). Until this decision nothing behind that obligation was a schema key: intake
asked for the module optionally, the answer lived as **prose** in `BUG.md`'s `## Scope`, `reproduce`
re-derived it from the symptom, and `step-diagnose.md` composed `MODULE:` from that. `check-envelopes.py`
keys on the scope key and never reads frontmatter, so the obligation was met by unchecked convention
rather than by a schema — the failure mode that produced this contradiction in the first place.
A `BUG` is a scope unit that **routes a dispatch**, and every other routing key in orqestra lives in
frontmatter and resolves the whole triple in one lookup (§5.1, D-004); prose that four steps re-read and
re-derive is the state that can disagree with itself. Rule B (§4.4.1) is satisfied — the key has real
consumers: `check-templates.py` proves it against §4.8.1, `step-diagnose.md` reads it to compose the
envelope instead of re-deriving it, and `step-promote.md` carries it onto the task.
**Why a `BUG` and not a `PHASE`:** D-027 put `PHASE` and `PROJECT` on the other side of the same rule
because those units route no module-scoped work — a phase spans modules by construction, and a `PROJECT`
dispatch has no scope unit at all, so a `module:` on either would be a field with no true value. A bug is
always about one module: the fix lands somewhere, and where it lands is who implements it (§7.3.1). The
dividing line is not "big unit vs small unit" — it is whether the unit routes one module's work.
**Constrains:**
- Every `BUG.md` written from now carries `module:`. `bugfix` intake may not create a bug without one and
  may not fall back to `## Scope` prose; a module the reporter does not know is established by the
  workflow, or intake blocks (D11).
- `## Scope` in `templates/BUG.md` stops carrying the module. A rule written in two places is one that
  will disagree with itself.
- `step-diagnose.md` and `step-promote.md` **read** the module from the BUG's frontmatter and never
  re-derive it from the symptom. When diagnosis finds the fix lands elsewhere, the BUG's frontmatter is
  amended and the dispatch recomposed — never a `MODULE:` that disagrees with the artifact it names.
- Any future scope unit added to §5.5 states in §4.8 whether its frontmatter carries `module:` (D-027),
  and this decision fixes the test it answers: a unit that routes one module's work carries the key; a
  unit that does not, omits it.
