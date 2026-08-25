---
id: MODULES
type: modules
status: done
updated: 2026-08-24
module_count: 2
---

## Modules

| module | paths | agent | stack | expertise |
|---|---|---|---|---|
| plugin | skills/, agents/, templates/, scripts/, .claude-plugin/ | agentic-engineer | markdown | claude-expert, orqestra-conventions |
| docs | REQUIREMENTS.md, README.md | architect | markdown | orqestra-conventions |

<!-- WHY `docs` IS HANDLED BY `architect`, NOT AN ENGINEER

     REQUIREMENTS.md is a specification. Changing it means reasoning about the design —
     what a rule constrains, what it contradicts, what breaks if it moves. That is the
     architect's job, and no engineer persona is a good fit for it.

     This is the case the old `task_type` enum could not express: docs is not backend,
     frontend, devops, or agentic, and picking one just to reach an agent was contortion.
     The row now names the agent directly (§5.1.1).

     WHY ONLY TWO MODULES

     The temptation was five: skills, agents, commands, templates, docs. nit split `cli/`
     from `.claude/` and found every task crossed between them, which made the boundary
     useless and every task a violation.

     Same here. "Make init produce a valid workspace" touches skills/init/SKILL.md,
     templates/config.md, and templates/modules.md. Splitting templates from skills would
     make that one task span two modules — and D14 would force it into two tasks, shipping
     a schema without the skill that writes it. Incoherent.

     Modules are things that CO-CHANGE. Split only where a change to one genuinely does not
     imply a change to the other. Here, docs changes independently; nothing else does.
     Adding a CLI (§12) would justify a third module — it would change on its own schedule.

     REGISTRY CORRECTION, PHASE-1 / TASK-001: `scripts/` was added because the task that
     built the conformance checker had nowhere to put it — every module boundary excluded
     it, so the work was literally outside D14. Found by doing the work, not by reading.

     `.orqestra/` deliberately belongs to NO module: it is workspace state that workflows
     write as they run, not source that a task edits. A task never "changes .orqestra/"
     as its deliverable; it produces artifacts there as a side effect of its steps.

     `.claude/skills/orqestra/` belongs to no module either, for a different reason: every
     entry in it is a SYMLINK to a path already inside the `plugin` module (§2.1, D-013).
     Editing `skills/design/SKILL.md` is a `plugin` change whichever path you reach it by.
     Listing it as its own module would double-count the same files and let a task claim
     it had stayed inside one module while editing another's source.

     `.claude/skills/claude-expert/` and `.claude/skills/orqestra-conventions/` are the
     real, non-symlinked expertise skills (§5.3) — plain skills, no manifest, so they load
     alongside the plugin rather than inside it.
-->
