---
id: TASK-007
type: plan
status: done
updated: 2026-08-24
task: TASK-007
---

## Approach

Reconcile in four passes, each mechanically checkable rather than read-by-eye, because the failure mode
here is *plausible-looking prose that is quietly false*:

1. **Catalogue** — run TASK-001's checker and resolve every mismatch on whichever side is wrong.
2. **Counts** — count the shipped tree, grep every count claimed in prose, fix the difference.
3. **Citations** — extract every `§n.n` and `Dn` reference in the spec *and in all 22 skills*, and
   confirm each resolves to something that exists.
4. **Unimplemented rules** — cross-check every config key and every flag the spec names against what
   the skills actually read.

## Affected Areas

`REQUIREMENTS.md` only — this is the `docs` module. Verified by reading §4.8.1, §7.12, §5.4, §4.8.4,
and by running the checks above.

## Risks

- **The fix may belong to the other module.** Where the spec is right and the *plugin* is wrong, this
  task cannot act (D14) — it reports, exactly as TASK-001 reported to this task.
- **Renumbering sections breaks citations everywhere.** Every skill cites the spec by number, so no
  section may be renumbered here — only appended to or corrected in place (D-007's reasoning applied to
  sections).

## Open Questions

_none_
