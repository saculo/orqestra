---
id: TASK-001
type: design
status: done
updated: 2026-08-24
task: TASK-001
decisions: [D-015]
---

## Components

| component | serves | purpose |
|---|---|---|
| `parse_catalogue()` | AC-1, AC-2, AC-3 | Extracts §4.8.1 rows into name, required frontmatter, ordered headings |
| `read_template()` | AC-2, AC-3 | Extracts a template's frontmatter keys and headings, ignoring code fences and comments |
| `main()` | AC-1, AC-4, AC-5 | Compares, reports each violation by name, sets the exit code |

## Interfaces

```
python3 scripts/check-templates.py [--verbose]
  exit 0  every template conforms
  exit 1  one or more do not — each violation printed with the artifact and what is wrong
  exit 2  §4.8.1 could not be located in REQUIREMENTS.md
```

Exit 2 is separate on purpose: "the rules are unreadable" is a different failure from "the templates are
wrong", and collapsing them would report a moved section heading as twenty broken templates.

## File Plan

| path | action | purpose |
|---|---|---|
| `scripts/check-templates.py` | create | The checker |
| `.orqestra/config.md` | modify | Record `test_command` |
| `.orqestra/modules.md` | modify | Add `scripts/` to the `plugin` module |

## Decisions

- **The catalogue is parsed, never restated.** The check reads §4.8.1 at run time.
- **Three exemption classes**, each expressed *in the catalogue* rather than hard-coded: `FREEFORM`
  (`PRD.md` — declared "none"), rows declaring no headings, and rows marked **no common frontmatter**.
  The last is the mechanism `config.md` needs; the catalogue does not yet use it (TASK-007).
- **`ALIASES`** maps the two catalogue names that are not filenames (`decisions/INDEX.md`,
  `decisions/D-NNN-*.md`) onto their templates.
- **D-015** records that dev tooling is outside D-001's "no code" constraint.

## Test Strategy

Behavioural, per AC-4: break a template three ways — rename a heading, reorder two headings, add an
undeclared frontmatter key — and confirm each is reported specifically, then restore. Exit-zero is
proven on a fixture copy carrying the catalogue corrections TASK-007 will make, since the live tree
cannot go green from inside this module.
