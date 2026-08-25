---
id: MODULES
type: modules
status: done
updated:
module_count: 1
---

## Modules
<!-- THE ROUTING KEY (§5.1). Every task names exactly one module; its agent, stack,
     and expertise all derive from that row — never set independently (D7, D9, D14).

     paths     — the boundary. An agent may not write outside them, and review-task
                 flags any file in the diff that falls outside as a `major` finding.
     agent     — the subagent that implements this module, named DIRECTLY. One of the
                 files in agents/. There is no task_type enum in between (§5.1.1):
                 a docs module is best handled by `architect`, which no engineer enum
                 could express. A name with no file in agents/ is a config error.
     stack     — advisory context only, shown in the envelope and in status.
                 NOT a routing input.
     expertise — YOUR skills, in .claude/skills/. See templates/EXPERTISE.template.md.
                 A COMMA-SEPARATED LIST — a module usually names several, split by
                 concern (the language, the framework, this project's testing
                 patterns). All of them load on every step of every task in the
                 module, so split rather than grow one file past ~150 lines.
                 A missing one warns and dispatches without it; it never blocks.

     Adding a module is two steps and no orqestra changes: add a row, write the skill
     it names. `create-tasks` blocks on a module that is not listed here (D11). -->

| module | paths | agent | stack | expertise |
|---|---|---|---|---|
| app | src/ | backend-engineer | java | java-expertise |
