---
name: init
argument-hint: "[--force]"
description: "Scaffolds the .orqestra/ workspace in a repository — config, templates for state, project stub, and the decisions directory — then commits it. The first command run in any orqestra project. Use when the user says '/orqestra:init', asks to set up orqestra, or starts a new orqestra-managed project."
allowed-tools: Read, Write, Glob, Grep, Bash, AskUserQuestion
---

> **Arguments**: `/orqestra:init [--force]`
> **Class**: planning (the one skill that writes config)

# orqestra Init

Scaffold `.orqestra/`. Runs once per project.

## Arguments

`$ARGUMENTS` may contain `--force`.

**When empty**: Anything else is ignored. Without `--force`, an existing `.orqestra/` is refused.

## Procedure

Run in order (D6):

1. **Refuse if `.orqestra/` exists**, unless `--force`. An existing workspace holds real planning state;
   overwriting it silently is unrecoverable in a way nothing else in orqestra is. Name `--force` as the
   override and stop — do not offer to do it anyway.

   **With `--force`, announce before you write, never after.** List what will be replaced and what will
   be kept, then act:

   ```
   ⚠ --force will REPLACE:
       .orqestra/config.md            (modified since init)
       .orqestra/modules.md           2 modules registered
       .orqestra/project/PROJECT.md
       .orqestra/decisions/INDEX.md   4 decisions — the files in decisions/ are NOT removed
     and will KEEP:
       .orqestra/PRD.md               your document, never overwritten
       .orqestra/phases/              3 phases, 14 tasks — untouched
   ```

   A report written *after* the write is not a warning, it is a receipt. Where `AskUserQuestion` is
   available, confirm at this point; where it is not, print the list first anyway so the record shows
   what was replaced.

   **Never delete planning state.** `--force` re-scaffolds the generated files; it does not remove
   `phases/`, `work/`, or the individual files in `decisions/`. A user asking to re-scaffold config is
   not asking to discard a project.

2. **Detect and confirm.** Suggest the stack from repo contents — `pom.xml`/`build.gradle` → java,
   `package.json` → typescript, `pyproject.toml` → python, `go.mod` → go. **Always confirm via
   `AskUserQuestion`**, never assume. Ask for the project name and an optional description.

3. **Check the environment**, reporting rather than failing:

   | Check | On failure |
   |---|---|
   | `git rev-parse --git-dir` | **Stop.** orqestra needs a git repo — artifact commits (§4.6) are load-bearing |
   | `git remote -v` | Warn. Planning works; delivery needs a remote |
   | `gh auth status` | Warn. Planning works; the delivery pipeline needs `gh` |

4. **Write the tree** — every file **copied from its template in `templates/`** and filled in, never
   composed from scratch (D16).

   **Keep the YAML frontmatter.** It is not decoration: `status` (§7.10) derives every task's stage from
   it, and the conformance check (§4.4) verifies it. A file written without frontmatter looks correct to
   a reader and is invisible to the tool. Prose may be improved; **structure may not be changed.**

```
.orqestra/
├── config.md                  # gates, rework, delivery, version control, conventions
├── modules.md                 # THE module registry — the routing key (§5.1)
├── PRD.md                     # template stub, only if absent — never overwrite an existing PRD
├── decisions/
│   └── INDEX.md               # empty table, next_id: 1
├── project/
│   └── PROJECT.md             # stack + detected commands; conventions filled in at first design
├── phases/                    # empty
└── work/                      # empty
```

5. **Populate `config.md`** from `${CLAUDE_PLUGIN_ROOT}/templates/config.md` (D16) with the confirmed stack, the default gate
   modes, and the step→agent table. Fill `test_command` and `branch_pattern` from what you detected;
   leave a detected-but-unverified command marked as such rather than presenting a guess as fact.

6. **Seed `modules.md`** with one row for the confirmed stack, and say plainly that it is a starting
   point:

   ```markdown
   | module | paths | agent | stack | expertise |
   |--------|-------|-------|-------|-----------|
   | app    | src/  | backend-engineer | java | java-expertise |

   **Write the agent name bare — `backend-engineer`, not `orqestra:backend-engineer`** (D-014). The
   registry stores the plain name; the plugin namespace is added at dispatch, in one place. Writing it
   namespaced here puts the prefix in two places and breaks the moment the plugin is renamed.
   ```

   **Every task is routed by its module row** (§5.1) — the row names the agent directly, so a docs
   module can be handled by `architect` while a service is handled by `backend-engineer`. A project with
   a Spring service, a Celery worker, a Vue app, and Argo manifests needs four rows and four sets of
   conventions — see `${CLAUDE_PLUGIN_ROOT}/templates/EXPERTISE.template.md`. Tell the user this at init, not when routing first fails:
   `create-tasks` blocks on a module that is not registered, and the fix is a two-line edit they should
   already know about.

7. **Commit**: `chore(orqestra): initialize workspace` (§4.6).

8. **Report** what was written and exactly one next command.

## PROJECT.md at init

A stub, honestly labelled. It holds the stack and whatever build and test commands you could detect —
nothing more. Conventions and layout are filled in by `design` during the first task, when there is
actual code to describe.

**Do not scan the codebase to populate it.** v1 is greenfield-only (§1.3 principle 6); a half-inferred
conventions section is worse than an empty one, because every downstream agent will trust it.

## Return

```
✓ orqestra initialized · myproject (java)

  .orqestra/config.md          gates: greenfield gated, task gated
  .orqestra/PRD.md             stub — write your product requirements here
  .orqestra/project/PROJECT.md java · mvn test
  .orqestra/modules.md         1 module: app (java) — add a row per module
  .orqestra/decisions/INDEX.md empty

  ⚠ gh not authenticated — planning works; run `gh auth login` before delivery

→ Next: write .orqestra/PRD.md, then /orqestra:greenfield
```

## Rules

1. **Never overwrite an existing `.orqestra/`** without `--force`.
2. **Never overwrite an existing `PRD.md`.** It is the human's document.
3. **Never scan the codebase** to fill `PROJECT.md` (v1 scope).
4. **Always confirm the stack.** Detection suggests; the human decides.
5. **When `AskUserQuestion` is unavailable** (a non-interactive session), do not silently assume:
   proceed with the detected values, mark them unconfirmed in the report, and say which ones need
   checking. A guess presented as a decision is the failure; a guess labelled as a guess is fine.
6. Copy templates literally (D16) — frontmatter included, always.
7. **Explain the module registry** in the report. It is the one thing a user must edit before real work,
   and the one whose absence blocks `create-tasks` (§5.1).
