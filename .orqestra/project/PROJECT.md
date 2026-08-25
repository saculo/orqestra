---
id: PROJECT
type: project
status: in-progress
updated: 2026-08-25
stack: markdown
---

## Stack

A Claude Code plugin. No runtime, no build step, no dependencies beyond `git` and `gh` (§1.3
principle 2). Everything ships as Markdown: skills, agents, templates, plus one `plugin.json`.

The only executable file in the repo is `scripts/check-templates.py` — CPython 3, stdlib only, no
package manifest anywhere. There is deliberately no `commands/` directory (D-012) and no CLI (D-001).

## Layout

```
.claude-plugin/plugin.json   manifest
skills/                      22 skills; the folder name IS the /orqestra:<name> command
                             orchestrators sharded into step-<name>.md
agents/                      8 subagent personas
templates/                   the artifact schemas in executable form
scripts/                     conformance checks over templates/
REQUIREMENTS.md              the specification, and this project's PRD
.claude/skills/              this project's own expertise skills (§5.3)
.orqestra/                   this project's own workspace — belongs to no module
```

## Commands

| | |
|---|---|
| build | none |
| test | **none yet** — PHASE-1 SC-5 establishes the eval harness |
| lint | `python3 scripts/check-templates.py` — templates against §4.8.1 |
| run | `claude --plugin-dir .` · `/reload-plugins` after edits |
| validate | `claude plugin validate .` |

`--plugin-dir` loads the working tree live (D-013), so an edit is testable without packaging.

## Conventions

- **The spec is cited by number, never restated.** `§7.4.2`, `D11`, `D-018`. A rule written in two
  places is a rule that will disagree with itself.
- **Renumbering a spec section is expensive** — every citation across ~90 files breaks. Append a
  subsection (`§5.1.1`, `§4.8.5`); do not insert one.
- **A schema change is three edits, always together**: the §4.8 catalogue row, the `templates/` file,
  and the skill that writes it. Any one alone leaves the schema broken (D-003).
- **Orchestrators never write; step skills never dispatch.** How much of that the frontmatter enforces
  depends on the layer (§7.0.1): `agents/*.md` `tools:` is a true allowlist and binds for the whole
  subagent run; a skill's `disallowed-tools` binds only until the user's next message; and
  `allowed-tools` pre-approves without restricting anything. Put a guarantee where it binds, and never
  describe one as structural without checking which field carries it.
- **The subagent tool is `Agent`.** `Task` is its former name and grants nothing.
- **Step files are named, never numbered** (D-007). Order lives in the SKILL.md index table.
- **Every rule states its reason.** A bare rule is followed until it is inconvenient.
- Module-specific conventions belong in that module's expertise skills, not here (§5.3):
  - `.claude/skills/claude-expert/` — Claude Code plugin authoring, for the `plugin` module
  - `.claude/skills/orqestra-conventions/` — spec structure, citation, and voice, for both modules

## Testing

No test framework exists yet. What stands in for one:

- `python3 scripts/check-templates.py` is the only automated check — it parses the §4.8.1 catalogue and
  asserts each `templates/*.md` carries the exact frontmatter keys and headings, in order. **Run it
  after every schema edit**; it is the thing that catches a two-of-three schema change (D-003).
- Acceptance criteria here are **behavioural only**. "Write skill X" is trivially met and proves
  nothing; "`/orqestra:init` produces a workspace that `check-templates.py` passes" is a criterion.
- The eval harness that will test skill behaviour is PHASE-1 SC-5 and does not exist. Do not describe
  it as if it does.

## Git and GitHub

- **Never work on the base branch.** Every source change lands on the task branch. Nothing
  before the push step commits source, and the push step is the only thing that reaches the
  remote.
- **Never touch work you did not create.** No `stash`, no `reset --hard`, no
  `checkout -- <path>`, no `clean`. Uncommitted changes in the tree are a human's, and they
  are the one thing here that cannot be recreated. Stop and say so instead.
- **Stage explicit paths.** No `git add -A`, no `commit -a`. You commit what you changed, not
  whatever happened to be sitting next to it.
- **Never rewrite published history.** No amend, no rebase, no force-push once a commit is on
  the remote and under review — reviewers lose the lines their comments point at.
  `--force-with-lease`, on your own task branch, to finish a rebase you were told to do, is
  the single exception.
- **One task, one branch, one PR.** A branch or a PR that already exists for this task is
  adopted, never duplicated — a second one splits the review and strands the first.
- **Merging is a human's decision** unless the config says otherwise, and a conflict is always
  a human's. Never auto-resolve one.
- **`gh` is the only route to GitHub.** No raw API calls with a token scraped from the
  environment.
- **Never edit, close, or resolve another person's PR, issue, or comment.** Reply to it.
- **Never commit secrets, credentials, `.env` files, or build output.** If it is generated, it
  is regenerated.

This repo's own:

- **Base branch is `master`.** `branch_pattern: feat/{task_id}-{slug}` (`config.md`).
- **Commit subjects name the owning work** (D-018): `TASK-NNN:` for task work, `PHASE-N:` for
  phase-level work, `orqestra:` for repo-wide chores. Most specific scope that owns the change.
- **Planning commits touch `.orqestra/` only** (§4.6). Source and `.orqestra/` never share a commit,
  because a planning commit must stay revertable on its own.
- **The spec leads when a skill cites it** (D-019). A skill referencing `§4.8.5` cannot merge before the
  section exists; a skill that merely reads a file may follow.

## Traps

- **Do not** edit `REQUIREMENTS.md` and the skills that implement it in separate tasks. The spec and its
  implementation are one module and change together.
- **Do not** split a module by file type (D-010). Modules are things that co-change — `templates/` and
  `skills/` were kept together because every real task touches both.
- **Do not** add a frontmatter field without naming its consumer (Rule B, §4.4.1). `task_type` was
  deleted for exactly this.
- **Do not** describe orqestra as further along than it is. Nothing has been run end to end yet. The
  honest state is more useful than an encouraging one, and an inflated `PROJECT.md` misleads every
  future dispatch.
