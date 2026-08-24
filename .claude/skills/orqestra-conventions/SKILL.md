---
name: orqestra-conventions
description: "Project conventions for orqestra itself — how its specification is structured and cited, how the determinism charter is referenced, its house voice, and the rules that govern edits to REQUIREMENTS.md. Use when working on any orqestra module, and especially when editing the specification."
---

# orqestra — Project Conventions

Applies to every module. `REQUIREMENTS.md` is both the specification and this project's PRD.

## Structure

`REQUIREMENTS.md` is numbered and **cited by number everywhere else**: `§5.1` for the module registry,
`§7.4.2` for delivery failure modes, `§14` for the determinism charter, `D1`–`D16` for individual rules.

Citations are the mechanism that keeps ~90 files consistent without duplicating text. **Never restate a
rule you can cite.** A rule written in two places is one that will disagree with itself — this is not
hypothetical, it is why `§7.7` stopped listing required headings and points at the catalogue instead.

## Conventions

- **Cite the charter by number.** `(D11)`, not "block rather than guess, because…". The number is
  stable; the wording is not.
- **Renumbering sections is expensive** — every citation across every skill breaks. Prefer appending a
  subsection (`§5.1.1`) to inserting one. This is the same reasoning as D-007 on step filenames, and the
  project has been bitten by it once already.
- **Every rule states its reason.** A bare rule is followed until it is inconvenient; a rule with a
  reason survives.
- **Schema changes are three edits, always together**: the §4.8 catalogue row, the `templates/` file,
  and the skill that writes it. Any one alone leaves the schema broken (D-003).
- **Decisions that constrain future work go in `.orqestra/decisions/`**, with the `**Constrains:**` line
  filled in. If you cannot write that line, it is a note, not a decision.

## Patterns

Voice: direct, specific, no hedging. Prefer the concrete failure over the abstraction.

```
✅  "A dirty tree is always a human's uncommitted work. Touching it is the one mistake
     that loses something orqestra cannot recreate."
❌  "Care should be taken when the working tree contains uncommitted changes."
```

Tables for anything enumerable — conditions and outcomes, steps and gates, fields and consumers. Prose
for the reasoning that explains why the table looks like that.

## Testing

Behavioural criteria only. `SC-N` in a phase and `AC-N` in a task describe **what is observably true
when the work is done**, never what was written. Much of this plugin already exists as an untested
draft, so "write skill X" would be trivially met and prove nothing.

## Traps

- **Do not** add a frontmatter field without naming its consumer (Rule B, §4.4.1). The `task_type` field
  was removed for exactly this: once the module row named the agent directly, nothing branched on it.
- **Do not** split a module by file type. Modules are things that co-change (D-010).
- **Do not** edit `REQUIREMENTS.md` and the skills in separate tasks. The spec and its implementation
  are one module and change together.
- **Do not** describe orqestra's own progress as further along than it is. Nothing has been run yet;
  the phases say so, and the honest state is more useful than an encouraging one.
