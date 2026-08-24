---
id: PROJECT
type: project
status: in-progress
updated: 2026-08-24
stack: markdown
---

## Stack

A Claude Code plugin. No runtime, no build step, no dependencies beyond `git` and `gh` (§1.3
principle 2). Everything ships as Markdown: skills, agents, commands, templates, plus one
`plugin.json`.

## Layout

```
.claude-plugin/plugin.json   manifest
skills/                      22 skills; the folder name IS the /orqestra:<name> command
                             orchestrators sharded into step-<name>.md
agents/                      8 subagent personas
templates/                   21 artifact schemas in executable form
REQUIREMENTS.md              the specification, and this project's PRD
.claude/skills/              this project's own expertise skills (§5.3)
```

## Commands

| | |
|---|---|
| build | none |
| test | **none yet** — PHASE-1 SC-5 establishes the eval harness |
| run | `claude --plugin-dir .` · `/reload-plugins` after edits |
| validate | `claude plugin validate .` |
| lint | schema conformance of `templates/` against `REQUIREMENTS.md` §4.8 |

## Conventions

- **Skills follow `templates/SKILL.template.md`.** Class first — it fixes `allowed-tools`.
- **The determinism charter (§14) is cited by number, never restated.** A rule written in two places
  is a rule that will disagree with itself.
- **Orchestrators hold no `Write`; step skills hold no `Task`.** Structural, not aspirational.
- **Step files are named, never numbered.** Order lives in the SKILL.md index table.
- Module-specific conventions belong in that module's expertise skill, not here (§5.3):
  - `.claude/skills/claude-expert/` — Claude Code plugin authoring, for the `plugin` module
  - `.claude/skills/orqestra-conventions/` — spec structure, citation, and voice, for both modules
