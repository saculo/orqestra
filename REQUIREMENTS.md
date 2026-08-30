# orqestra — Requirements

> A workflow tool for Claude Code. Distributed as a plugin. Stateful through Markdown.
> A deliberately simpler descendant of [nit](../nit), borrowing BMAD's execution model.

---

## 1. What orqestra is

orqestra drives software delivery through **workflows**. A workflow is an ordered set of **steps**.
Each workflow has exactly one **orchestrator** that decides which step runs next, resolves who runs it,
dispatches, reads back the result, and gates the human where the config says to.

### 1.1 The two layers

orqestra separates **planning** from **delivery**. This is the core structural decision.

```
  PLANNING                                          DELIVERY
  ────────────────────────────────────────          ──────────────────────────────────────
  produces designed work units, then stops          takes one work unit to a merged PR

  greenfield    clarify → phases → tasks            task pipeline   design-check
  add-phase     phase → tasks                                       implement
  bugfix        reproduce → diagnose                                qa
                    ↓                                               review          [GATE]
                plan → design         [GATE] ──────────────────▶    push (gh)
                                                                    pr-comments
                                                                    merge           [GATE]
```

A planning workflow ends when every task in the phase has a `DESIGN.md`. Nothing is built yet.
Then **one delivery pipeline runs per task**, independently, taking that single task from design to a
merged PR. Phase close (`review-phase`) runs once all tasks in the phase are merged.

### 1.2 Workflows

| Workflow | Entry command | Layer | Purpose |
|---|---|---|---|
| greenfield | `/orqestra:greenfield` | planning | New project: clarify → phases → tasks → plan → design |
| add-phase | `/orqestra:add-phase` | planning | Add a phase to an orqestra-managed project |
| bugfix | `/orqestra:bugfix` | planning | Reproduce, diagnose, plan and design a fix |
| **task** | `/orqestra:task <ID>` | delivery | One task: implement → qa → review → push → PR comments → merge |
| pr-comments | `/orqestra:pr-comments <PR>` | delivery | Triage and resolve review comments. Step of the task pipeline; also standalone. |
| close-phase | `/orqestra:close-phase <N>` | — | Verify the phase's success criteria, write the summary |

### 1.3 Design principles

1. **The artifacts are the state.** There is no `state.json`, no `STATE.md`, no ledger. Every artifact
   carries YAML frontmatter with `status`. The orchestrator learns where it is by globbing `.orqestra/`
   and reading frontmatter. Nothing to desync, resumable by construction.
2. **No code.** No CLI, no JSON Schema, no build step, no runtime dependency beyond `git` and `gh`.
   Skills, agents, commands, Markdown. If a rule cannot be expressed as an instruction in a skill, it
   is not a v1 rule. **One deliberate seam**: all state derivation lives in a single skill (§7.10), so
   if prompt-based globbing proves unreliable it becomes a script without touching anything else —
   see §12 on how GSD and BMAD draw this line.
3. **Markdown is the wire format, and every wire has a schema.** Every handoff between steps,
   workflows, and sessions is a `.md` file with a declared schema — exact frontmatter keys, closed
   value vocabularies, ordered headings, fixed table columns (§4.4, §4.8). Skills are deterministic in
   what they emit; a step reading an artifact knows its shape without inferring it. Markdown rather
   than JSON, schema-bearing rather than free-form.
4. **Sharded steps.** An orchestrator skill is a small entrypoint plus one file per step, loaded only
   when that step runs. Context economy is a first-class concern.
5. **One task, one pipeline, one PR.** Delivery is per task and sequential within a task. Two tasks
   may be at different stages, but a task never runs two steps at once.
6. **orqestra-managed only.** Every workflow assumes the project was built by orqestra from scratch.
   `.orqestra/` exists and is populated; `PROJECT.md`, phases, and tasks are readable context. There is
   no brownfield adoption path in v1 (§10).
7. **Simpler than nit, on purpose.** nit has 21 skills, 8 archetypes, a Bun supervisor state machine,
   26 JSON schemas, and a repair/rework/escalate protocol. orqestra has a comparable number of skills
   and none of the rest — no archetypes, no state machine, no schemas, and one rework rule. The
   simplification is not a smaller skill count; it is the machinery underneath them.

### 1.4 Lineage — what is taken and what is dropped

| From nit | Verdict |
|---|---|
| Orchestrator/step separation | **Taken.** The core idea. |
| Role routing (task type → engineer) | **Taken**, extended into the routing triple (§5). |
| Human gates at boundaries | **Taken**, but configurable per workflow (§6). |
| `qa` as a step in every task | **Taken** — it is a step of the delivery pipeline. |
| Bun CLI supervisor, `state.json` transitions | **Dropped.** |
| Schemas on every inter-step artifact | **Taken** — every artifact has one (§4.4, §4.8). Skills must be deterministic in what they emit. |
| JSON Schema as the *format*, `ajv`, `nit validate` | **Dropped.** The schemas are Markdown contracts — frontmatter keys, ordered headings, fixed table columns — enforced by template and orchestrator, not by a validator binary. |
| 8 archetypes with rejection routing | **Dropped.** One step order per workflow; one rework rule. |
| Just-in-time design (design inside the task loop) | **Changed.** Design belongs to planning; the delivery pipeline guards against staleness instead (§7.4 preflight). |
| Boundaries/modules registry, ADRs, PLRs | **Dropped from v1.** See §10. |

| From BMAD v6 | Verdict |
|---|---|
| LLM-interpreted instructions, no execution engine | **Taken.** |
| Sharded `step-NN-*.md` micro-files | **Taken.** |
| State discovered by scanning output locations | **Taken**, sharpened with frontmatter `status`. |
| Review "lenses" — one review skill, many stances | **Taken** (§7.7). |
| `memlog` / `memories.md` shared working memory | **Taken** as `decisions/` (§4.7). |
| Python renderer, TOML customization layers, `_bmad/render/` | **Dropped.** |
| Scale-adaptive levels (process weight by project size) | **Deferred.** See §10. |

| From GSD Core | Verdict |
|---|---|
| A git commit per completed unit of work | **Taken** (§4.6). |
| `AskUserQuestion` as the gate mechanism | **Taken** (§6). |
| `CONTEXT.md` — shared knowledge across fresh-context subagents | **Taken** as `decisions/` (§4.7). |
| `gsd-tools.cjs` — deterministic state queries in code | **Deferred**, but the seam is placed (§7.10, §12). |
| Parallel research fan-out at planning | **Deferred.** See §10. |
| Punch lists at verify | **Deferred.** See §10. |
| Cross-runtime installer (Codex, Cursor, Copilot, …) | **Dropped.** Claude Code only. |

---

## 2. Distribution and installation

orqestra ships as a **Claude Code plugin**.

```
orqestra/
├── .claude-plugin/
│   └── plugin.json            # name, description, version, author — `name` is the skill namespace
├── skills/                    # one directory per skill — the folder name IS the invocation name
│   ├── init/SKILL.md          #   → /orqestra:init
│   ├── task/SKILL.md          #   → /orqestra:task    (+ step-*.md shards)
│   └── …
├── agents/                    # 8 subagent personas
├── templates/                 # artifact schemas in executable form (§4.8.3)
└── README.md
```

**There is no `commands/` directory.** Claude Code namespaces plugin skills automatically from
`plugin.json`'s `name`, so `skills/task/` *is* `/orqestra:task` — and the docs are explicit that
`commands/` is the legacy flat form and that new plugins should use `skills/`. A parallel command file
per skill would be a second place for the same invocation to be described, and therefore a second place
to drift. Skills take their arguments from `$ARGUMENTS` and declare `argument-hint` in frontmatter.

### 2.1 Development and installation

**orqestra loads itself in its own repository, with no flag and no install.** `.claude/skills/orqestra/`
holds a `.claude-plugin/` manifest, so Claude Code loads it as a **skills-directory plugin** —
`orqestra@skills-dir` — on the next session in this repo. Its component directories are **symlinks to
the plugin at the repo root**, so there is exactly one copy of every skill, agent, and template:

```
.claude/skills/orqestra/
├── .claude-plugin  →  ../../../.claude-plugin      the manifest, and the `orqestra:` namespace
├── skills          →  ../../../skills
├── agents          →  ../../../agents
├── templates       →  ../../../templates
└── scripts         →  ../../../scripts
```

Three conditions, all of them project-scope rules rather than anything orqestra chose:

| Condition | Why |
|---|---|
| **Trust the workspace** | A project-scope skills-dir plugin ships in the repo and reaches everyone who clones it, so it loads only behind the trust gate. Trusting a parent folder does not count, and `-p` does not either |
| **Launch from the repo root** | Project-scope skills-dir plugins do **not** walk up to the repository root the way plain skills do. From a subdirectory, orqestra is simply absent — `/reload-plugins` after `cd` recovers it |
| **Do not also pass `--plugin-dir .`** | Two copies of the same plugin under different names |

Editing a `SKILL.md` takes effect immediately. Editing anything else — `agents/`, `templates/`,
`hooks/` — needs `/reload-plugins`.

```bash
claude                                          # orqestra is already here
/reload-plugins                                 # after editing agents/ or templates/
claude plugin validate .                        # structural validation, on the real directory
```

**Validate the repo root, not the symlinked copy.** `claude plugin validate .claude/skills/orqestra`
passes with a warning that says so: the validator does not follow symlinks, though a session loading
the plugin does.

This resolves what would otherwise be a bootstrap deadlock. orqestra plans its own delivery from
PHASE-2 onward (§13), which requires orqestra to be runnable *in its own repository* — and it cannot
install itself from a marketplace before the marketplace work is done. The skills directory dissolves
it without one, and `--plugin-dir .` remains available for loading the tree from anywhere else.

**Symlinks are the whole design.** Copying the plugin into `.claude/` would create a second source of
truth for ~90 files that drift the first time someone edits one and not the other; moving it there
would repoint every path in this document, `modules.md`, and the conformance checker. Neither buys
anything the links do not. The cost is that a checkout on a filesystem without symlinks — Windows
without developer mode — gets broken links and must fall back to `claude --plugin-dir .`.

For distribution, a `.claude-plugin/marketplace.json` lists the plugin and users run
`/plugin marketplace add <repo>` then `/plugin install orqestra@<marketplace>`. That is packaging work,
deferred to PHASE-5 — nothing before it needs a marketplace to exist.

**External dependency**: `gh` (GitHub CLI), authenticated. Used by the delivery pipeline's push and
pr-comments steps. `init` verifies `gh auth status` and warns if absent.

---

## 3. Initialization

`/orqestra:init` scaffolds `.orqestra/` in the current repo. It is the only step that writes config.

Behaviour:

1. Refuse if `.orqestra/` already exists, unless `--force`.
2. Ask for: project name, primary stack (java / typescript / python / go / …), and optional description.
   Stack is auto-suggested from repo contents (`pom.xml`, `package.json`, …) and always confirmed.
3. Verify `git` remote and `gh auth status`. Warn — do not fail — if `gh` is missing; the planning
   layer works without it, only delivery needs it.
4. Write the tree below.
5. **Commit it** — `orqestra: initialize workspace` (§4.6).
6. Print what was written and the suggested next command.

```
.orqestra/
├── config.md                  # gates, routing table, stack, conventions  (§6)
├── modules.md                 # the module registry — routing key           (§5.1)
├── PRD.md                     # created empty with a template if absent   (greenfield input)
├── decisions/                 # one file per decision + INDEX.md            (§4.7)
├── project/
│   └── PROJECT.md             # stack, build/test commands, conventions
├── phases/                    # populated by create-phases
└── work/                      # bugfix runs, and standalone pr-comments runs
```

**v1 is greenfield-only.** `init` does not scan an existing codebase to produce a modules/conventions
map. `PROJECT.md` starts as a stub and is filled in during the first phase's design — from that point
on every workflow reads it as the project's ground truth.

---

## 4. State model

### 4.1 The rule

**Artifacts are the state.** No file exists whose only job is to record status.

Every artifact begins with YAML frontmatter:

```yaml
---
id: TASK-003
type: task                  # phase | task | plan | design | implementation | qa | review | pr | phase-summary | bug
status: in-progress         # see §4.2
workflow: greenfield
phase: PHASE-1
module: api                 # THE routing key — agent/stack/expertise all come from its row (§5.1)
stack: java                 # advisory context, from the module row; never a routing input
depends_on: [TASK-001]
attempts: 1                 # rework counter, see §8
updated: 2026-08-24
---
```

To answer *"where am I?"* the orchestrator globs `.orqestra/**/*.md`, reads frontmatter, and picks the
first artifact not in a terminal status, in phase → task → step order. That is the whole state engine.

### 4.2 Status vocabulary

One vocabulary, all artifact types:

| status | Meaning | Terminal |
|---|---|---|
| `pending` | Exists as a plan; not started | no |
| `in-progress` | Being worked | no |
| `awaiting-approval` | Parked at a gate; needs a human | no |
| `changes-requested` | Reviewed, sent back for rework | no |
| `blocked` | Cannot proceed; reason recorded in the artifact | no |
| `done` | Complete and accepted | **yes** |
| `superseded` | Replaced (e.g. a split task) | **yes** |

### 4.3 Deriving a task's stage

A task's position in the two-layer flow is **derived from which artifacts exist and their status** —
never stored. This is the BMAD discovery model doing its job.

| Artifacts present (all `done`) | Stage | Next command |
|---|---|---|
| `TASK.md` | created | `/orqestra:greenfield` (continues planning) |
| `+ PLAN.md` | planned | — planning continues |
| `+ DESIGN.md` | **designed — planning complete** | `/orqestra:task <ID>` |
| `+ IMPLEMENTATION.md` | implemented | `/orqestra:task <ID>` (resumes) |
| `+ QA.md` | verified | `/orqestra:task <ID>` |
| `+ REVIEW.md` (`verdict: passed`) | reviewed | `/orqestra:task <ID>` |
| `+ PR.md` (`state: open`) | pushed | `/orqestra:task <ID>` |
| `+ RESOLUTION.md`, `PR.md` (`state: merged`) | **delivered** | next task |

### 4.4 Artifact schemas

**Every file passed between steps has a schema.** Skills must be deterministic in what they emit —
a step that reads `DESIGN.md` has to know exactly what shape it will find, without inference.

A schema has four parts, all expressible in Markdown:

| Part | What it fixes |
|---|---|
| **Frontmatter contract** | Exact keys, their types, and closed value vocabularies (§4.4.3). |
| **Heading contract** | Exact `##` headings, **in order**. No undeclared headings. No `###` where `##` is declared. |
| **Section shape** | For table sections, the exact column headers, in order (§4.8.2). |
| **Template** | A fill-in-the-blank file in `templates/` the step copies and completes (§4.8.3). |

The full catalogue of all twenty artifacts is §4.8.

#### 4.4.1 Two rules that keep schemas honest

**Rule A — if a later step branches on it, it lives in frontmatter.** Never only in prose. A step
deciding what to do next must read one YAML key, never parse a paragraph. This is what makes the
workflow deterministic rather than interpretive: `verdict: changes-requested` drives the rework loop,
not the tone of `## Findings`.

**Rule B — every frontmatter field names its consumer.** If no step, gate, or `status` query reads a
field, delete it. Borrowed from nit's ADR-0007 (*"every declared field must have a proven consumer"*),
which exists because nit's own registries accumulated fields nothing ever read. Schemas rot by growing,
not by shrinking.

#### 4.4.2 Empty sections

A required section with nothing to report contains the literal `_none_`. Never omit the heading, never
leave it blank.

This matters more than it looks. It makes "empty" **explicit rather than ambiguous** — the difference
between *the reviewer found no blockers* and *the reviewer forgot to fill this in* — and it makes the
check `grep -A1 '^## Findings' | grep -q .` rather than a judgement call.

#### 4.4.3 Closed vocabularies

Every enumerated field draws from a fixed set. A value outside the set is a contract failure, not a
creative choice.

| Field | Values |
|---|---|
| `status` | `pending` · `in-progress` · `awaiting-approval` · `changes-requested` · `blocked` · `done` · `superseded` |
| `type` | one of the twenty artifact types in §4.8 |
| `agent` (in `modules.md`) | `analyst` · `architect` · `backend-engineer` · `frontend-engineer` · `devops-engineer` · `agentic-engineer` · `qa-engineer` · `reviewer` — a name with no file in `agents/` is a config error |
| `verdict` (review) | `passed` · `changes-requested` · `failed` |
| `result` (qa) | `passed` · `failed` |
| `severity` (review finding) | `blocker` · `major` · `minor` · `nit` |
| `severity` (bug) | `blocker` · `major` · `minor` — no `nit`; a bug nobody would file is not a bug |
| `deviation` (implement) | `none` · `minor` · `moderate` · `major` — the frontmatter field **and** the `## Deviations` column, which is named `deviation` for exactly this reason |
| `comment_verdict` | `accept` · `reject` · `discuss` |
| `pr_state` | `open` · `merged` · `closed` |
| `criteria_met` | `true` · `false` |
| `blocked_reason` | **work**: `contradictory-input` · `criterion-unsatisfiable` · `no-reproduction` · `design-invalid` · `max-attempts` · `contract` · `needs-splitting` <br> **delivery**: `deps-unmerged` · `dirty-tree` · `branch-conflict` · `push-rejected` · `merge-conflict` · `ci-red` · `gh-auth` |

#### 4.4.4 Common frontmatter

Present on every artifact:

```yaml
---
id: TASK-003          # the artifact's own id, or its owner's
type: design          # §4.8 catalogue
status: done          # §4.4.3
updated: 2026-08-24   # ISO 8601 date
---
```

Per-type additions are listed in the catalogue. **Frontmatter is additive-only** — a schema may gain
optional keys in a later version, never rename or repurpose an existing one.

#### 4.4.5 How schemas are enforced in v1

1. **By construction.** The step skill is given the template and instructed to emit its structure
   verbatim. Most compliance comes from here.
2. **By the orchestrator.** After a step returns, before advancing, the orchestrator checks the
   artifact against its schema: frontmatter keys present, values within vocabulary, headings present
   in order, no undeclared headings, no blank required section. Fail → re-dispatch **once** with the
   specific violations named. Fail again → `blocked` with `blocked_reason: contract`.
3. **Never by patching.** The orchestrator does not fix a malformed artifact itself. Its
   `disallowed-tools` removes `Write` and `Edit` for the turn (§7.0.1); across a gate the rule is
   behavioural, and the `control` skills (`approve`, `reject`, `unblock`) are the named exception —
   they patch exactly one frontmatter field, on a human's instruction, and nothing else.

This is the deliberate simplification of nit's 26 JSON Schemas: the same determinism where it pays,
zero code. And because every rule above is mechanically checkable, the deferred hook or CLI (§12) is a
drop-in — the schemas are written now in the form a 20-line checker would want.

### 4.5 Full state tree

```
.orqestra/
├── config.md
├── modules.md                               # module registry (§5.1)
├── PRD.md
├── CLARIFICATIONS.md                        # greenfield step 2 output
├── decisions/                               # INDEX.md + D-NNN-*.md            (§4.7)
├── project/
│   └── PROJECT.md
├── phases/
│   ├── PHASES.md                            # index: all phases, order, rationale
│   ├── PHASE-1/
│   │   ├── PHASE.md                         # goal, success criteria SC-1..N, status
│   │   ├── PHASE_SUMMARY.md                 # written by review-phase / close-phase
│   │   └── tasks/
│   │       ├── TASKS.md                     # index: all tasks in this phase, dep order
│   │       ├── TASK-001/
│   │       │   ├── TASK.md                  # what + acceptance criteria + which SC it serves
│   │       │   │                            # ── planning layer ──
│   │       │   ├── PLAN.md                  # approach, affected areas, risks, open questions
│   │       │   ├── DESIGN.md                # components, interfaces, structure
│   │       │   │                            # ── delivery layer ──
│   │       │   ├── IMPLEMENTATION.md        # what was built, deviations, tech debt
│   │       │   ├── QA.md                    # test strategy, results, coverage of criteria
│   │       │   ├── REVIEW.md                # verdict + findings
│   │       │   ├── PR.md                    # branch, PR number/url, state
│   │       │   ├── COMMENTS.md              # triaged PR review comments
│   │       │   └── RESOLUTION.md            # per comment: action taken, reply sent
│   │       └── TASK-002/…
│   └── PHASE-2/…
└── work/
    ├── BUG-001/
    │   ├── BUG.md                           # report, repro, scope
    │   ├── DIAGNOSIS.md                     # root cause + evidence
    │   └── → promoted to a TASK under the current phase for delivery (§7.5)
    └── PR-142/                              # standalone pr-comments run, PR not tied to a task
        ├── COMMENTS.md
        └── RESOLUTION.md
```

Task numbering is **continuous across phases** — `TASK-014` follows PHASE-1's last task; it does not
reset. Bug directories are numbered per repo.

### 4.6 Artifact commits

**Every completed step commits its own artifacts.** Borrowed from GSD, where each completed phase
generates a commit, "making the entire development chain inspectable and resumable."

The consequence is the point: **the planning history becomes git history.** `git log -- .orqestra/`
shows how the design actually evolved; a bad phase plan is undone with `git revert`, not by hand-editing
Markdown; and "artifacts are the state" (§4.1) becomes durable rather than merely conventional.

Rules:

- Commit **only `.orqestra/`** paths at planning steps. Source changes are committed by the delivery
  pipeline's `implement`/`push` steps, on the task branch, separately.
- One commit per completed step, immediately after its contract check (§4.4) passes — never before.
- **Message convention** — `<scope>: <subject>`, per `config.md`'s `commit_style: scoped` (D-018). The
  scope is the **most specific scope that owns the change**, chosen by a ladder that always terminates:

  | | test | scope |
  |---|---|---|
  | 1 | A task owns the change — any commit made while that task is in flight, source or artifact | `TASK-NNN` |
  | 2 | Otherwise, a phase's planning owns it — `create-phases`, `create-tasks`, `clarify` | `PHASE-N` |
  | 3 | Otherwise — `init` scaffolding, workspace configuration, repo-wide work no task covers | `orqestra` |

  ```
  TASK-001: review — REVIEW.md passed
  PHASE-1: create-tasks — TASKS.md + 3 tasks
  orqestra: initialize workspace
  orqestra: record D-004 — use Flyway for migrations
  ```

  **No conventional-commit type prefix.** `feat(`, `fix(`, `chore(`, `docs(`, `test(` appear in no
  commit this project makes. Nearly every commit here is a `fix` or a `chore` and choosing between them
  is a coin flip, while the task id leads a reader to `TASK.md`, `DESIGN.md`, `REVIEW.md`, and the
  success criterion the work serves. One prefix turns `git log --oneline` into an index into the
  workspace.

  The subject is free prose. Only the prefix is constrained, and rule 3 is what makes the ladder
  **total**: every commit has exactly one correct scope, so no judgement is left at the moment of
  writing.

- Planning commits land on the **current branch** (typically the default branch). Delivery-pipeline
  artifact commits land on the **task branch**, so a task's `.orqestra/` record travels with its PR
  and merges with it.
- A rejected gate does **not** revert the commit. The rework produces a new commit; the history shows
  the rejection happened. This is deliberate — the record of what was tried is the value.
- `no_commit: true` in `config.md` disables the whole mechanism for users who prefer to stage manually.

### 4.7 Decisions — shared memory across fresh contexts

Every step runs in a fresh subagent context. That is the design (§5.4) and the reason quality does not
decay across a long phase — but it has one cost: **a fresh agent will happily re-litigate a decision
settled three tasks ago.** GSD solves this with `CONTEXT.md`, BMAD v6 with `memlog`, described as
"shared working memory across skills, replacing per-skill decision logs." orqestra uses a `decisions/` directory.

#### 4.7.1 One file per decision, plus an index

A single growing `DECISIONS.md` has three problems: it is a merge-conflict magnet when two task
branches both record a decision, a decision cannot be reverted independently, and it is read in full on
**every** dispatch — so it gets more expensive precisely as the project gets longer.

So: **a directory of one-decision files, plus a generated index.**

```
.orqestra/decisions/
├── INDEX.md                              # every dispatch reads THIS
├── D-001-monorepo-layout.md
├── D-002-postgres-over-sqlite.md
├── D-003-no-orm.md
└── D-004-flyway-for-migrations.md
```

The index is a table — id, title, area, status, one-line summary — and nothing more:

```markdown
| id | decision | area | status | summary |
|---|---|---|---|---|
| D-002 | Postgres over SQLite | storage | active | Need concurrent writers from PHASE-2 |
| D-003 | No ORM | storage | active | Hand-written SQL; queries stay inspectable |
| D-004 | Flyway for migrations | storage | active | Versioned SQL under `db/migration` |
| D-001 | Monorepo layout | structure | superseded by D-009 | — |
```

**The reading rule — this is where the design pays off:**

- Every dispatch reads `INDEX.md`. Always, unconditionally. It stays small: one line per decision, so a
  hundred decisions is still a hundred lines.
- An agent opens an individual `D-NNN-*.md` **only** when the index summary touches its work. Designing
  the storage layer? Open the three `storage` rows. Building a login form? Open none.

That is the whole point: **unconditional awareness, conditional detail.** One growing file forces a
choice between reading everything and reading nothing.

It also solves the growth problem outright (previously an open question in §11): superseding is a status
change in one row, and archiving is moving files — no rewriting, no `DECISIONS_ARCHIVE.md`.

A decision file:

```markdown
---
id: D-004
type: decision
status: active            # active | superseded
updated: 2026-08-24
area: storage
supersedes: —
superseded_by: —
---

# D-004 — Use Flyway for schema migrations

**When:** 2026-08-24 · PHASE-1 / TASK-003 · design
**Decision:** Flyway, versioned SQL under `src/main/resources/db/migration`.
**Why:** Team knows it; Liquibase's XML abstraction buys nothing here.
**Constrains:** Any task adding tables writes a numbered migration — never DDL at runtime.
```

`## Constrains` is the field that earns the file. It states what a *future* task must do — which is the
only reason a fresh agent needs to read a decision at all.

**Contract:**

- **Append-only.** Files are never edited after they are written, and never deleted. Reversing a
  decision writes a new file and flips the old row to `superseded by D-NNN`.
- **The index is regenerated, not hand-edited** — it is derived from the files, so it cannot drift.
- **Written by**: `design` and `implement` (technical), `clarify` and `create-phases` (product and
  scope), and the human at any gate.
- **Ids are global** and never reused, across phases and workflows both.

Entries carry `D-NNN` ids so `DESIGN.md` and `REVIEW.md` can cite them. When `review-task` finds code
contradicting a decision, it cites the id rather than re-arguing it.

**Scope discipline** — this is the file most likely to rot into a junk drawer. It records **decisions
that constrain future work**, not a changelog, not a summary of what was built, and not anything
already stated in `DESIGN.md` for the current task. If a future task would not be wrong for not knowing
it, it does not go in.

### 4.8 Schema catalogue

Twenty-two artifacts. Common frontmatter (§4.4.4) is implied on every row unless the row says
**no common frontmatter**; the column otherwise lists **additions**. Headings are required, in the order
given.

Only `config.md` takes the exemption, and it earns it: it is *configuration*, not project state, so
`status` and `updated` on it would be fields nothing reads — which Rule B (§4.4.1) forbids.

#### 4.8.1 The catalogue

| Artifact | Written by | Frontmatter additions | Required headings, in order |
|---|---|---|---|
| `config.md` | `init` | **no common frontmatter** — `project` `stack` `version` | `## Gates` · `## Rework` · `## Delivery` · `## Version control` · `## Routing` · `## Conventions` |
| `modules.md` | `init`, then the human | `module_count` | `## Modules` |
| `PROJECT.md` | `design` (first task), appended after | `stack` | `## Stack` · `## Layout` · `## Commands` · `## Conventions` · `## Testing` · `## Git and GitHub` · `## Traps` |
| `PRD.md` | **human** | none | none — the one free-form input; `clarify` imposes structure downstream |
| `CLARIFICATIONS.md` | `clarify` | `source_prd` `open_count` | `## Resolved` · `## Assumptions` · `## Open` |
| `decisions/INDEX.md` | regenerated from the files (§4.7) | `count` `next_id` | `## Decisions` |
| `decisions/D-NNN-*.md` | `design`, `implement`, `clarify`, `create-phases`, human | `area` `supersedes` `superseded_by` | `# D-NNN — <title>` then `**When**` `**Decision**` `**Why**` `**Constrains**` |
| `PHASES.md` | `create-phases` | `phase_count` | `## Phases` · `## Ordering Rationale` |
| `PHASE.md` | `create-phases` / `create-phase` | `phase` `criteria_count` | `## Goal` · `## Success Criteria` · `## Scope` · `## Out of Scope` |
| `TASKS.md` | `create-tasks` | `phase` `task_count` | `## Tasks` · `## Dependency Order` |
| `TASK.md` | `create-tasks` / `create-task` | `phase` `module` `stack` `origin` `bug` `depends_on` `serves` `attempts` | `## Goal` · `## Acceptance Criteria` · `## Out of Scope` |
| `PLAN.md` | `plan` | `task` | `## Approach` · `## Affected Areas` · `## Risks` · `## Open Questions` |
| `DESIGN.md` | `design` | `task` `decisions` | `## Components` · `## Interfaces` · `## Structure` · `## Decisions` · `## Test Strategy` |
| `IMPLEMENTATION.md` | `implement` | `task` `deviation` `files_changed` | `## Changes` · `## Deviations` · `## Tech Debt` |
| `QA.md` | `qa` | `task` `result` `test_command` | `## Test Strategy` · `## Results` · `## Criteria Coverage` · `## Issues` |
| `REVIEW.md` | `review-task` | `task` `verdict` `lenses` `required` `review_round` | `## Verdict` · `## Findings` · `## What Would Change This Verdict` · `## Notes` |
| `PR.md` | `push` (task pipeline) | `task` `branch` `pr_number` `pr_url` `pr_state` | `## Summary` · `## Commits` · `## CI` |
| `COMMENTS.md` | `pr-comments` triage | `pr_number` `comment_count` `unresolved` | `## Comments` |
| `RESOLUTION.md` | `pr-comments` reply | `pr_number` `accepted` `rejected` `discussing` | `## Resolutions` · `## Replies Sent` |
| `PHASE_SUMMARY.md` | `review-phase` | `phase` `criteria_met` | `## Criteria` · `## Deviations` · `## Tech Debt` · `## Verdict` |
| `BUG.md` | `bugfix` intake | `bug` `severity` | `## Report` · `## Reproduction` · `## Expected vs Actual` · `## Scope` |
| `DIAGNOSIS.md` | `diagnose` | `bug` `root_cause_found` `task` | `## Root Cause` · `## Evidence` · `## Fix Direction` · `## Regression Risk` |

#### 4.8.2 Section shapes

Where a section is a table, the column headers are part of the schema — exact, in order. This is what
lets a downstream step read a row by position instead of interpreting prose.

| Artifact · section | Columns |
|---|---|
| `PHASE.md` · `## Success Criteria` | `id` (`SC-N`) · `criterion` · `verified by` |
| `modules.md` · `## Modules` | `module` · `paths` · `agent` · `stack` · `expertise` |
| `PHASES.md` · `## Phases` | `id` · `goal` · `criteria` · `status` |
| `TASKS.md` · `## Tasks` | `id` · `title` · `module` · `depends_on` · `serves` |
| `TASK.md` · `## Acceptance Criteria` | `id` (`AC-N`) · `criterion` |
| `IMPLEMENTATION.md` · `## Deviations` | `deviation` · `from design` · `what` · `why` |
| `QA.md` · `## Criteria Coverage` | `criterion` (`AC-N`) · `covered by` · `result` |
| `REVIEW.md` · `## Findings` | `id` (`F-N`) · `severity` · `file:line` · `finding` |
| `COMMENTS.md` · `## Comments` | `#` · `thread` · `file:line` · `summary` · `verdict` · `action` |
| `RESOLUTION.md` · `## Resolutions` | `#` · `verdict` · `action taken` · `commit` · `thread resolved` |
| `PHASE_SUMMARY.md` · `## Criteria` | `id` · `criterion` · `met` · `evidence` |

**Id chains are the point.** `SC-N` in `PHASE.md` → cited by `TASK.md.serves` → `AC-N` in `TASK.md` →
cited by `QA.md`'s coverage table → rolled up in `PHASE_SUMMARY.md`. `F-N` in `REVIEW.md` → consumed
by the rework loop. `D-NNN` in `decisions/` → cited by `DESIGN.md` and `REVIEW.md`. Every id is
traceable end to end without reading a sentence.

#### 4.8.3 Templates

The plugin ships `templates/<ARTIFACT>.md` — one per catalogue row, containing the exact frontmatter
skeleton and headings, with guidance as HTML comments the step strips on write.

```markdown
---
id:
type: review
status:
updated:
task:
verdict:          # passed | changes-requested | failed
lenses: []
required: []      # F-N ids the rework loop must address
review_round: 1   # 1 = first review · 2 = re-review of a disputed `failed`
---

## Verdict
<!-- One paragraph. State the verdict and the single reason for it. -->

## Findings
<!-- Table: id | severity | file:line | finding
     Severity is the only grade. Every blocker and major goes in frontmatter
     `required`; no minor or nit may. `_none_` if clean. -->

## What Would Change This Verdict
<!-- Required when `verdict: failed`. `_n/a_` otherwise. -->

## Notes
<!-- Non-blocking observations. `_none_` if none. -->
```

A step skill's contract is then one line: *copy `templates/REVIEW.md`, fill it, change nothing
structural.* The template is the schema in executable form — which is why templates live in the plugin
and not in this document, and why §4.8.1 stays a catalogue rather than twenty inlined examples.

#### 4.8.4 Versioning

`config.md` carries `version: 1`. v1 ships version 1 and **additive changes only** (§4.4.4), so no
migration path exists and none is implemented.

That is deliberate rather than an omission. A migration mechanism written before any schema has ever
changed is a guess at a problem nobody has had — the same *build only what this phase needs now* rule
that governs phases (§7.6). When a schema first changes incompatibly, the version increments and the
upgrade path gets designed against the actual change. Until then, `init` refuses to touch an existing
workspace (§3) and that is the whole story.

#### 4.8.5 Altitude — the two artifacts that are deliberately not lists

Most artifacts in the catalogue are enumerable, and their schemas say so: tables with fixed columns,
ids that chain. Two are not, and both were made worse by being treated as if they were.

**`DESIGN.md` states structure, not files** (D-020). The design's `## Structure` names the areas,
layers, and boundaries the work lands in — it never lists paths to create. Two reasons, and the
second is the larger one. A path list goes stale the moment another task merges, so preflight's
freshness check (§7.4) spent its attention on filenames rather than on whether the design still
held. And an engineer handed a checklist satisfies the checklist: the file plan quietly replaced
the acceptance criteria as the definition of done, which is exactly backwards, since the criteria
are what `qa` measures. The architect reads the code once; the engineer reads it while typing, and
is better placed to choose placement inside the boundaries the design sets.

The boundary is unchanged: the whole change stays inside the task's module `paths` (§5.2, D2), and
`review-task` still checks the diff against them. What moved is who picks the filename, not who owns
the constraint.

**`PROJECT.md` records what is expensive to find, not what is true** (D-021). Every fact in it faces
one test: *what does this cost to retrieve at the moment an agent needs it?* Cheap — readable from
the code, the build file, or the framework's own docs — it stays out. Expensive, or learned only
by getting it wrong once, it goes in. The file loads on every dispatch in every workflow, so a line
restating what a competent engineer already assumes is not merely redundant; it displaces the line
that would have saved a rework cycle.

Its `## Git and GitHub` section ships with a fixed set of rules rather than a blank heading, because
these are the mistakes that cost the most and are recoverable the least — a discarded dirty tree, a
force-push under an open review, a second PR for a task that already had one. §7.4.2 tells the
orchestrator how to *detect* those conditions; `PROJECT.md` states them where every agent already
reads, in the project's own copy, so the rule is present at the moment the temptation is. The template
carries them as body text, not guidance, precisely so `init` and `design` copy them through (D16).

Both changes were made **before v1 shipped and before any pipeline ran end to end**, which is the only
window in which they are cheap — §4.8.4's *additive changes only* rule governs released schemas, and
the nine `DESIGN.md` files already written under this project's own PHASE-1 are frozen (D5) rather than
migrated. The schema is read forward. A tenth design written against the old headings would be the
signal that the window has closed.

---

## 5. The routing triple

The central mechanism. For every step, the orchestrator resolves three things, never one:

```
step  →  ( step skill , subagent , expertise skills[] )
```

**Example.** Task `TASK-007`, `module: api`, current step `implement`:

```
implement  →  ( skills/implement , agents/backend-engineer , [java-expertise, test-quality] )
```

The `implement` skill defines *the procedure* for implementing. `backend-engineer` defines *who* is
doing it — its perspective, tools, and standards. `java-expertise` supplies *domain knowledge* for the
language. Three separable concerns, composed at dispatch.

The orchestrator never decides these by prose or intuition — it reads the routing table in `config.md`.

### 5.1 The module registry — where routing actually comes from

A real project is not one stack. It is five modules: a Spring service, a Celery worker, a Vue app,
Argo manifests, and the docs. **A Spring service and a Celery worker are both "backend"** — same
persona, entirely different conventions. And **docs are neither** — the right reader for a
specification is the architect, not an engineer.

So the routing key is the **module**, and the module row names the agent **directly**.
`.orqestra/modules.md`:

```markdown
| module | paths              | agent             | stack      | expertise                            |
|--------|--------------------|-------------------|------------|--------------------------------------|
| api    | services/api       | backend-engineer  | java       | java-expertise, spring-conventions   |
| worker | services/worker    | backend-engineer  | python     | python-expertise, celery-conventions |
| web    | apps/web           | frontend-engineer | typescript | ts-expertise, vue-conventions        |
| infra  | deploy/, charts/   | devops-engineer   | yaml       | argo-conventions, k8s-conventions    |
| docs   | docs/, README.md   | architect         | markdown   | house-style                          |
```

Every task carries `module:` in its frontmatter, and **the agent, stack, and expertise all come from
that one row** — never set independently. One key instead of three that can disagree is a determinism
win (D7, D9): there is no state in which a task claims one language while its module is another.

**The `expertise` cell is a list, not a slot.** A module names as many skills as it has distinct
concerns — `python-expertise, celery-conventions, worker-testing` — and every one of them loads on
every step of every task in that module. Splitting by concern is the preferred shape once a single
skill grows past what fits in one reader's head, because the alternative is one file that every step
pays for in full to reach the paragraph it needed (§5.3).

The triple resolves in **one lookup, with nothing in between**:

```
TASK-041  module: worker  →  step   implement
                             agent  backend-engineer          (named by the row)
                             skills python-expertise,
                                    celery-conventions        (named by the row)
```

#### 5.1.1 Why there is no `task_type`

An earlier design routed `task_type` → agent through a second table in `config.md`. That indirection is
gone, and its field with it.

**The agent is named directly because the enum could not express the real cases.** `docs` is not
backend, frontend, devops, or agentic — but it has a natural owner, and forcing it into the enum to
reach one is contortion. Meanwhile `api` and `worker` shared a `task_type` while sharing nothing else.

Removing it also satisfies Rule B (§4.4.1): once the row names the agent, nothing branches on
`task_type`, and **a field with no consumer is deleted, not kept for tidiness.**

`stack` survives on different grounds. Nothing routes on it — it is **advisory context**, carried in the
envelope so an agent knows the language before its expertise skills load, and shown in `status`. That
is a real consumer, so it stays; but it is not a routing input, and a task never sets it.

**Expertise applies to every step of the task, not just implement.** Designing a Vue module should load
the Vue conventions; QA on a Spring service should know how that project tests Spring. The agent
changes per step; the module's expertise travels with the task throughout.

| step | skill | subagent | expertise |
|---|---|---|---|
| plan | `plan` | `analyst` | module's |
| design | `design` | `architect` | module's |
| implement | `implement` | **the module's `agent`** | module's |
| qa | `qa` | `qa-engineer` | module's |
| review | `review-task` | `reviewer` | module's |
| pr-comments | `pr-comments` | **the module's `agent`** | module's |
| diagnose | `diagnose` | `analyst` | module's |

Only `implement` and `pr-comments` vary by module — they write the code, so they need the module's
persona. Every other row is a fixed role that does the same job everywhere; what changes for them is
the expertise they load, not who they are. No count is given, because the next row added would
falsify it.

`diagnose` is the one row that is not a step of the task pipeline — it runs in the `bugfix` workflow,
against a `BUG.md` rather than a `TASK.md`. It belongs in this table anyway, because the module's
expertise reaches it in exactly the same way: a `BUG` carries `module:` too, so §5.5's conditional
class is mandatory there as well and the lookup is identical.

### 5.2 One task, one module

**A task belongs to exactly one module.** A change spanning the API and the web app is two tasks, with
`depends_on` ordering them (D13, §7.6.1).

This is not bureaucracy — it is what makes the rest work. One module means one agent, so dispatch
resolves unambiguously; one PR touching one area, so review stays coherent; and a checkable boundary,
since **`review-task` flags any file changed outside the task's module `paths`**. A task that
must span modules is a design smell exactly as often as it is a real need, and splitting it surfaces
which.

The one legitimate exception is a shared interface change, and it is still two tasks: define the
contract in the owning module, then consume it in the other.

### 5.3 User-authored module skills — the extension point

`spring-conventions`, `celery-conventions`, `vue-conventions`, `argo-conventions` are **not shipped by
orqestra**. You write them, for your project, and orqestra loads them by name.

This is the design you asked for: **one `implement` skill, a few base agents, and a swappable knowledge
layer per module.** The procedure (`implement`) and the persona (`backend-engineer`) stay fixed and
maintained by orqestra; what changes between a Spring service and a Celery worker is knowledge, and
knowledge is the part only you have.

**Where they live**: `.claude/skills/<name>/SKILL.md` in the project — Claude Code's native project
skill directory, so no discovery mechanism is needed. Committed with the repo, versioned with it,
reviewable in a PR like anything else.

**What they contain**: conventions, idioms, and project-specific rules that a competent engineer in
that stack would not know without being told. See `templates/EXPERTISE.template.md`.

- ✅ "Controllers return `ResponseEntity`, never raw DTOs. Errors go through `GlobalExceptionHandler`."
- ✅ "Celery tasks are idempotent and take only JSON-serializable args — we replay from the DLQ."
- ✅ "Vue components are `<script setup>` with the Composition API. No Options API in new code."
- ❌ "Java is a statically typed language." — the model knows.

**One module, several skills.** The `expertise` cell is a comma-separated list, and the natural split
is by concern: the language, the framework, the project's testing patterns. `EXPERTISE.template.md`
caps a single skill at roughly 150 lines for this reason — past that, split it and name both in the row
rather than growing one file every step must load whole.

**Adding a module** is two steps and no orqestra changes: add a row to `modules.md`, write the skills it
names. That is the whole extension story.

**Missing skills**: if a named expertise skill is not installed, the orchestrator **warns once and
dispatches without it** rather than failing. A missing convention file degrades quality; a hard failure
stops delivery. The warning names the module and the skill so the gap is visible rather than silent.

### 5.4 Subagents

`agents/` — each a focused persona, kept short:

| Agent | Role |
|---|---|
| `analyst` | Understands the task, surfaces risks and unknowns. Owns `plan`. |
| `architect` | Designs components, interfaces, structure. Owns `design`. |
| `backend-engineer` | Server-side implementation. |
| `frontend-engineer` | UI implementation. |
| `devops-engineer` | Infra, CI, deploy, containers. |
| `agentic-engineer` | Agents, skills, prompts, LLM integrations. |
| `qa-engineer` | Test strategy and test implementation. Owns `qa`. |
| `reviewer` | Correctness, design, security, performance review. Owns `review-*`. |

Agents are dispatched by the orchestrator via subagent dispatch — never invoked by hand. Context
isolation per step is the reason: the orchestrator's own context must survive a whole pipeline.

### 5.5 The dispatch envelope

The triple describes *who* runs a step. The envelope is *how* they are told to. nit could hand a
subagent an `input.json` because its CLI wrote one; orqestra dispatches with a prompt, so the envelope
is a fixed block of text — **same order, every dispatch, every workflow**, drawn from a closed set of
fields. *Which* of those fields a given dispatch must carry is a separate question, and not a judgement
call either: the obligation table below answers it per field, and it is the only thing that does.

```
ROLE:      orqestra:backend-engineer
STEP:      implement
SKILL:     orqestra:implement
TASK:      PHASE-1/TASK-007
MODULE:    api
PATHS:     services/api
STACK:     java
EXPERTISE: java-expertise, spring-conventions

READ:
  .orqestra/phases/PHASE-1/tasks/TASK-007/TASK.md
  .orqestra/phases/PHASE-1/tasks/TASK-007/PLAN.md
  .orqestra/phases/PHASE-1/tasks/TASK-007/DESIGN.md
  .orqestra/project/PROJECT.md
  .orqestra/decisions/INDEX.md

TEMPLATE:  ${CLAUDE_PLUGIN_ROOT}/templates/IMPLEMENTATION.md
WRITE:     .orqestra/phases/PHASE-1/tasks/TASK-007/IMPLEMENTATION.md

REWORK:    REVIEW.md — address findings F-2, F-5 only.     # present only on a re-dispatch
RETURN:    at most 10 lines, per the skill's Return contract.
```

**`ROLE` is the module's `agent`, dispatched under the plugin namespace.** Plugin agents are namespaced
exactly as skills are, so the row's `backend-engineer` is dispatched as the subagent type
`orqestra:backend-engineer`. The registry stores the bare name; the envelope and the dispatch use the
namespaced one. An `agent` value with no matching file in `agents/` is a config error, not a fallback.

**`SKILL` names the step skill, and the agent invokes it.** `STEP` is the stage — it appears in the
`status` table, in reports, and in artifact frontmatter. `SKILL` is the plugin skill carrying the
*procedure* for that stage, namespaced like any other. Collapsing the two would be wrong as often as it
would be right: `STEP: review` runs `SKILL: orqestra:review-task` (§5.1.1). The consumer is the
dispatched agent, which invokes the skill and follows what it returns — the persona says who is
working, the step skill says what the work is, and neither has to duplicate the other (D4: the envelope
is the only channel, so a procedure not named here is a procedure the agent has to invent).

**Why the skill is invoked and never read.** A step skill's body names its own template as
`${CLAUDE_PLUGIN_ROOT}/templates/DESIGN.md`. That variable is expanded by the harness at the moment a
skill is **invoked**; a `Read` of the same file returns it as a literal string and nothing downstream
expands it. An agent handed the procedure by `Read` therefore receives a `TEMPLATE:` path it cannot
open, and D16 — copy the template, never reproduce it from memory — silently becomes unfollowable. So
`SKILL` carries a name, not a path. The envelope's own `TEMPLATE:` line carries the prefix and gets
away with it for the mirror-image reason: the orchestrator composes the envelope from inside an invoked
skill, so the value is already expanded by the time an agent reads it. A bare
`templates/IMPLEMENTATION.md` would resolve against the user's project root, where orqestra's templates
do not exist.

**`EXPERTISE` names the module's expertise skills, and the agent invokes those too** — bare names,
neither paths nor namespaced, because they are the project's own skills in `.claude/skills/` rather
than the plugin's (§5.3). **This requires `Skill` in the dispatched agent's `agents/*.md` `tools:`**,
the one layer that binds for a whole subagent run (§7.0.1, D-024). The contract names its own
precondition because it cannot enforce it from this side: where that grant is missing, `SKILL` and
`EXPERTISE` are both inert. The dispatch does not fail — it degrades to the bare persona, with no
procedure and no project conventions, and returns plausible work that follows none of this project's
rules. That is the worst failure shape available, which is why the requirement is stated here rather
than left to be discovered.

**`MODULE` and `PATHS` carry the row the routing came from.** `MODULE` is the task's `module:` — the
single key that resolved `ROLE`, `STACK`, `EXPERTISE`, and `PATHS` from one `modules.md` row (§5.1,
D-004); the agent cites it, and `review-task` looks the row up by it. `PATHS` is that row's `paths`,
and it is a boundary rather than a hint: the agent writes nothing outside it, and `review-task` flags
any changed file that falls outside as a `major` finding (§5.2, §7.8.1, D2). Both travel in the
envelope because that check has to be mechanical — a reviewer who must go and find the row itself is a
reviewer who sometimes does not.

**Paths, never contents.** The orchestrator names the files; the agent reads them itself, in its own
context. Inlining an artifact into the envelope would move it through the orchestrator's context —
which is the exact cost subagents exist to avoid.

**The scope field.** Every envelope names the unit the step operates on, in one line immediately after
`SKILL`: `TASK:`, `PHASE:`, `BUG:`, or `PROJECT:`. The first three name an artifact on disk. `PROJECT:`
exists because some dispatches are composed **before any scope unit does** — `create-phases` runs when
the project has no phase, no task and no bug to name — and it carries the project name from
`.orqestra/config.md`. Without it those envelopes could satisfy the row only by inventing a unit that
does not exist, and a rule no conformant envelope can satisfy is a broken rule, not a strict one
(D-027).

**Which fields are mandatory.** Four obligation classes, each with a condition decidable by looking at
exactly one thing:

| Field | Obligation | Condition |
|---|---|---|
| `ROLE` `STEP` `SKILL` `READ` `TEMPLATE` `WRITE` `RETURN` | always | — |
| the scope — exactly one of `TASK` `PHASE` `BUG` `PROJECT` | always | which unit of work the step operates on. `PROJECT` is the dispatch composed before any scope unit exists; its value is the project name from `.orqestra/config.md` `project:` (D-027) |
| `MODULE` `PATHS` `STACK` `EXPERTISE` | conditional | mandatory **iff** the scope key is `TASK` or `BUG` — those units carry `module:` in their frontmatter. **Must be omitted** under `PHASE` and `PROJECT` — carrying them there is a violation, not a harmless extra: `templates/PHASE.md` carries no `module:`, and a `PROJECT` dispatch has no scope unit at all. The scope key decides, never a list of step names (D-027) |
| `EXPERTISE` | additionally | omitted when the module row's `expertise` cell is empty. The row decides, never the agent: §5.3's warn-once rule covers a *named* skill that is not installed, and does not license dropping the field |
| `LENSES` `ROUND` | step-specific | mandatory on a `review` dispatch and permitted on no other. `LENSES` is the resolved lens set (§7.8.2); `ROUND` is `1`, or `2` on the re-review of a disputed `failed` (§8.1), and the reviewer writes it to `REVIEW.md.review_round`. Both sit immediately after the scope field |
| `REWORK` | re-dispatch only | — |

**The list is closed.** A field appearing in no row above is not part of the envelope, and adding one is
a contract violation in the same way an omission is: a field no step is contracted to read is a field
the receiving agent is entitled to ignore, so inventing one hides the instruction rather than delivering
it (Rule B, §4.4.1, applied to the envelope rather than to frontmatter). Every condition in the table is
answered by something the orchestrator has already read to route the dispatch, so **an omission is a
contract violation rather than a judgement call**, and a dispatch missing a field its class requires is
rejected exactly as a missing `WRITE:` is (D2).

`REWORK` is precise when it appears: *these findings, nothing else.* A re-dispatch without it produces
a full redo, which is how rework loops turn into rewrite loops.

#### 5.5.1 The return contract — and why it matters more than it looks

An agent returns **at most 10 lines**: a status, a one-line outcome, a few lines of substance, and a
blocked reason if it blocked. It does **not** return the artifact.

The orchestrator then reads that artifact's **frontmatter only** — `status`, `verdict`, `result`,
`deviation` — and branches on it (Rule A, §4.4.1). It never reads the body.

This is the load-bearing rule of the whole design. Context isolation is trivially defeated at the
moment of *return*: if the orchestrator ingests each artifact it dispatched, its context fills with
precisely the material subagents were spawned to keep out, and quality decays across a phase exactly
as it would in one long session. Fresh contexts going in are worthless without a narrow channel coming
back.

It also pays a second time: **the agent's return text is the gate summary.** When a step is gated, the
orchestrator presents those lines to the human via `AskUserQuestion` (§6.1) rather than opening the
artifact to summarize it. One narrow channel serves both purposes, and no artifact body ever needs to
enter the orchestrator's context.

---

## 6. Configuration and gates

`.orqestra/config.md` — human-editable Markdown, read by every orchestrator.

```markdown
---
project: orqestra
stack: typescript
version: 1
---

## Gates

| workflow      | mode   | gate after                                    |
|---------------|--------|-----------------------------------------------|
| greenfield    | gated  | phases, tasks, design                         |
| add-phase     | gated  | phase, tasks, design                          |
| bugfix        | semi   | diagnosis, design                             |
| task          | gated  | review, merge                                 |
| pr-comments   | semi   | triage                                        |
| close-phase   | gated  | summary                                       |

## Rework

max_attempts: 3          # rework cycles per step before escalating to the human

## Delivery

branch_pattern: feat/{task_id}-{slug}
commit_style: conventional
pr_draft: false
auto_merge: false        # merge is a human decision unless set true
test_command: npm test

## Version control

no_commit: false         # true disables artifact commits entirely (§4.6)
artifact_commit_scope: .orqestra/

## Routing
… (see §5.1)
```

**Gate modes**: `gated` (stop at every listed gate) · `semi` (stop only at the listed gates) ·
`auto` (never stop; report at the end). Per-workflow, as requested.

### 6.1 How a gate is presented

At a gate the orchestrator sets the artifact to `awaiting-approval`, presents a **summary of the
artifact — not the raw file** — and asks via **`AskUserQuestion`**, not by stopping and waiting for a
typed command. GSD uses the tool the same way, for "Approve roadmap?"-style decision points. This is
the single most frequent interaction in orqestra — dozens of times per phase — so it must be one
keystroke, and it can offer real choices rather than a binary:

| Gate | Options offered |
|---|---|
| phases | approve · reorder · reject with reason |
| tasks | approve · split a task · add a task · reject with reason |
| design | approve · reject with reason · request an alternative approach |
| review | approve · reject with reason · accept findings as tech debt |
| merge | merged (confirm) · hold · reject with reason |

`/orqestra:approve` and `/orqestra:reject "<why>"` remain as commands, for resuming a gate in a **new
session** — the tool call does not survive a session boundary, but `status: awaiting-approval` in the
artifact does. That is the resumability path, and it is why the status still has to be written.

A rejection sets `changes-requested` and re-runs the step with the comment as input.
**Never hand-edit an artifact to satisfy your own feedback** — reject with the reasoning and let the
step re-run. (nit's rule; kept verbatim because it is the one that decays fastest.)

---

## 7. Skills

`skills/<name>/SKILL.md` (+ `step-NN-*.md` for orchestrators).

### 7.0 Skill anatomy

Twenty-two skills have to be written consistently, by different hands, months apart. The authoring
contract lives in **`templates/SKILL.template.md`** — copy it, fill the blanks, delete the comments.

Every skill declares a **class** first, and the class fixes everything else:

| Class | Skills | `allowed-tools` (pre-approved) | `disallowed-tools` (removed) |
|---|---|---|---|
| orchestrator | `greenfield`, `add-phase`, `bugfix`, `task`, `close-phase` | Read, Glob, Grep, Skill, Agent, AskUserQuestion (+Bash for `task`, `bugfix`, `close-phase`) | Write, Edit, NotebookEdit |
| planning | `create-phases`, `create-phase`, `create-tasks`, `create-task`, `clarify` | Read, Write, Glob, Grep, AskUserQuestion | Agent, Edit, NotebookEdit |
| step | `plan`, `design` | Read, Write, Glob, Grep | Agent, Edit, NotebookEdit, Bash |
| step+build | `implement`, `qa` | Read, Write, Edit, Glob, Grep, Bash | Agent |
| step+review | `review-task`, `review-phase` | Read, Write, Glob, Grep, Bash | Agent, Edit, NotebookEdit |
| query | `status` | Read, Glob, Grep | Agent, Write, Edit, NotebookEdit, Bash |
| setup | `init` | Read, Write, Glob, Grep, Bash, AskUserQuestion | Agent, Edit, NotebookEdit |
| control | `approve`, `reject`, `unblock`, `pr-comments` | …whatever the job needs | NotebookEdit |

Two rules matter more than the rest:

- **An orchestrator never writes an artifact.** It cannot patch a malformed one even when tempted
  (§4.4.5).
- **A step skill never dispatches.** It does its own work. Nesting dispatches makes the routing triple
  unauditable.

**How much of that the frontmatter actually enforces is not what this document said until §7.0.1**, and
the correction matters enough to have its own subsection.

#### 7.0.1 What the tool fields actually enforce

This document previously said the two rules above were *"enforced by the tool list rather than by
instruction, which is the point."* **That was wrong**, and it was wrong in the direction that matters:
it claimed a guarantee the plugin did not have, so nobody looked for one.

`allowed-tools` in a `SKILL.md` is a **pre-approval grant, not an allowlist.** Claude Code's own
documentation is explicit — the field lists "tools Claude can use without asking permission during the
turn that invokes this skill", and *"it does not restrict which tools are available: every tool remains
callable."* An orchestrator whose `allowed-tools` omits `Write` can still call `Write`; it merely
prompts first. Every "cannot" in this document that rested on that field was a "would be asked to".

Four layers exist, and only two of them bind:

| Layer | Field | Binds? | For how long |
|---|---|---|---|
| Dispatched subagent | `agents/*.md` `tools:` | **Yes** — a true allowlist | The whole subagent run |
| Dispatched subagent | `agents/*.md` `disallowedTools:` | **Yes** — a denylist | The whole subagent run |
| Skill | `disallowed-tools:` | **Yes** — removed from the pool | Until the user's next message |
| Skill | `allowed-tools:` | **No** — pre-approval only | (grants, never restricts) |

Note the casing: the agent field is `disallowedTools`, the skill field is `disallowed-tools`. They are
different files with different conventions, and a camelCase key in a `SKILL.md` is silently ignored.

**The consequence is a clean split, and it is good news for the part that matters most.** Every step
skill runs inside a dispatched subagent, and `agents/*.md` `tools:` is a real allowlist — so *"a step
skill never dispatches"* and *"the reviewer holds no `Edit`"* are genuinely structural on the pipeline
path, enforced by `agents/`, not by the skill. That is where those guarantees now live and where they
should be read.

**The orchestrators are the exposed ones.** They run in the main session, not in a subagent, so their
only mechanism is `disallowed-tools` — which clears at the user's next message, and an orchestrator
gates for user input by design. Protection therefore lasts a turn, and the rule that most needed
enforcing is the one least enforceable.

That is stated rather than papered over. Within a turn the field is real and worth having, so every
orchestrator now carries it. Across a gate the contract is behavioural — backed by the fact that an
orchestrator is the one component a human is watching at every gate, which is the weakest guarantee in
the system and is now labelled as such.

**Hardening (optional, not v1)**: a `PreToolUse` deny rule on `Write`/`Edit` for the orchestrator's
session, or a project `settings.json` deny rule, makes it durable. Same shape as the optional
`git checkout -b` hook in §7.4.2: enforcement moves from *what the orchestrator was told* to *what the
harness permits*. Deferred for the same reason — it is worth building once there is a run to test it
against.

**The `control` class exists because three skills broke the rule and the table hid it.** `approve`,
`reject`, and `unblock` declared themselves `orchestrator+` while holding `Write` and `Edit` — they
must set one frontmatter field on a human's behalf and then resume. §4.4.5 cited the orchestrator rule
as its guarantee that nothing patches an artifact, while these three could patch anything. Their real
constraint is **scope, not tools**: each edits exactly one frontmatter field of exactly one artifact.
No tool list can express that, so it is stated as a rule and named as the exception rather than
smuggled through a class it never fit.

Fixed section order in every `SKILL.md`: Invocation/Class · Inputs · Output · Procedure · Return ·
When you cannot proceed · Rules. **Shard into `step-<name>.md` when a skill exceeds ~150 lines or four
steps** — this is the main context-economy lever, and it is why orchestrators are entry points rather
than monoliths.

**Step files are named, never numbered** — `step-preflight.md`, `step-implement.md`, `step-push.md`.
The order lives in one place: the step index table in `SKILL.md`. Numbering a filename encodes
sequence in two places at once, so inserting a step means renaming every file after it and updating
every cross-reference — the same failure this document hit with its own section numbers. A named file
is stable for the life of the skill; only the index table changes when the order does.

Every orchestrator obeys the same contract:

- **Never writes an artifact itself.** It reads state, dispatches, and gates. Declared by
  `allowed-tools: Read, Glob, Grep, Skill, Agent` and backed for the turn by
  `disallowed-tools: Write, Edit, NotebookEdit` (§7.0.1). The delivery orchestrator additionally gets
  `Bash` for `gh` and `git`.
- **Resumable.** Re-running the command re-derives position from frontmatter (§4.3) and continues.
  Idempotent — an artifact already `done` is skipped, not redone.
- **Never advances past `blocked`.**

### 7.1 `greenfield` — planning

```
step-preflight.md      verify .orqestra/ exists, PRD.md non-empty
step-clarify.md        interactive Q&A on PRD gaps → CLARIFICATIONS.md
step-phases.md         → create-phases → PHASES.md + PHASE-N/PHASE.md      [GATE: phases]
step-tasks.md          → create-tasks <N> → TASKS.md + TASK-NNN/TASK.md    [GATE: tasks]
step-plan-design.md    per task in the phase: plan → design                [GATE: design]
step-handoff.md        report: every task designed; list the /orqestra:task commands to run
```

**Ends here.** The phase is fully planned and designed; nothing is built. Delivery is per task (§7.4).

Step 02 is invoked **directly, not through a subagent** — its questions must reach the human, not an
agent. (nit learned this the hard way; it is called out in `nit:orchestrate` explicitly.)

The plan-design step designs every task in the phase up front. See §7.4 preflight for how staleness is handled.

### 7.2 `add-phase` — planning

```
step-preflight.md      verify orqestra-managed; previous phase status == done
step-define-phase.md   → create-phase (singular) → PHASE-N/PHASE.md        [GATE: phase]
step-tasks.md          → create-tasks <N>                                  [GATE: tasks]
step-plan-design.md    per task: plan → design                             [GATE: design]
step-handoff.md        same as greenfield
```

`step-plan-design.md` is **the same file** in both workflows, referenced not duplicated. Divergence between
the two planning tails is the most likely maintenance failure, so they must share.

### 7.3 `bugfix` — planning

```
step-intake.md         bug report from args or interactive → work/BUG-NNN/BUG.md
step-reproduce.md      establish a failing reproduction against the current build
step-diagnose.md       root cause + evidence → DIAGNOSIS.md                [GATE: diagnosis]
step-promote.md        → create-task: a TASK-NNN under the current phase, module from the
                            touched area, linked back to BUG-NNN
step-plan-design.md    → plan → design for that task                       [GATE: design]
step-handoff.md        report the /orqestra:task command to run
```

Rule: **no fix without a failing reproduction first.** If step 02 cannot reproduce, the workflow goes
`blocked` and asks the human — it does not guess at a fix.

#### 7.3.1 What kind of task does a bug become?

**Not a module or an agent of its own.** Routing comes from *where the fix lands* — a bug in the `api`
module is `module: api`, implemented by whatever agent that row names, exactly as a feature there would
be. There is no "bugfix engineer", and asking for one is the same mistake as asking who implements a
`frontend` bug.

Provenance is a **separate axis**, carried in two fields:

```yaml
module: api               # routing — where the fix lands, hence who implements it
origin: bug               # provenance — where it came from  (feature | bug)
bug: BUG-001              # backlink to the diagnosis
```

`origin` is not decoration; three things read it:

| Reader | Behaviour when `origin: bug` |
|---|---|
| `review-task` | Adds the `regression-risk` lens by default (§7.8) — the failure mode that matters for a fix |
| `qa` | Requires a test that **fails against the pre-fix code**, not merely a passing suite |
| `close-phase` | Reports fixes separately from features in `PHASE_SUMMARY.md` |

Beyond that, the task is ordinary: same pipeline, same gates, same PR flow. That reuse is the point —
`origin` changes emphasis, never the machinery. It is also why the bugfix workflow is *planning* only
(§1.1): once diagnosed, a bug has nothing left that a feature task does not already handle.

### 7.4 `task` — delivery

**One pipeline run per task.** `/orqestra:task <TASK-ID>`.

```
step-preflight.md      four checks, in order, all must pass before anything runs:

                          (a) DEPENDENCIES — every id in TASK.md.depends_on has status: done
                              AND its PR.md pr_state: merged.  → §7.4.1
                          (b) WORKING TREE — clean, on the base branch, base up to date with origin.
                          (c) PLANNING COMPLETE — PLAN.md and DESIGN.md both exist and are done.
                              Missing → dispatch the missing steps in order (plan, then design),
                              then gate the design. Never continue without them.  → §7.4.3
                          (d) DESIGN FRESHNESS — does DESIGN.md still hold against current HEAD? Do
                              the files it names exist as expected? Have its assumptions been
                              invalidated by tasks merged since it was written?
                              → holds: continue · stale: re-run `design`, re-gate

step-implement.md      → implement, routed triple (skill + engineer subagent + stack expertise)
                          → IMPLEMENTATION.md

step-qa.md             → qa, qa-engineer + the task's stack expertise
                          write/extend tests, run the suite, verify every acceptance criterion
                          against actual behaviour
                          → QA.md · failing → back to implement, attempts++

step-review.md         → review-task, reviewer, lenses from config
                          → REVIEW.md                                          [GATE: review]
                          verdict changes-requested → back to implement, attempts++

step-push.md           git: branch from branch_pattern, commit (commit_style), push
                          gh pr create --title --body (body generated from TASK.md + IMPLEMENTATION.md)
                          → PR.md  (branch, PR number, url, state: open)

step-pr-comments.md    → pr-comments sub-workflow (§7.5) against PR.md's number
                          loops until no unresolved threads remain

step-merge.md          report PR state and CI status                        [GATE: merge]
                          auto_merge: false → human merges, orchestrator confirms and records
                          auto_merge: true  → gh pr merge
                          → PR.md state: merged · TASK.md status: done
```

The implement · qa · review steps form the **rework loop**: qa failure or a `changes-requested` review returns to implement
with the findings as input, incrementing `attempts` (§8).

`step-push.md` is the **only** step in orqestra that touches the remote. Nothing before it pushes.

#### 7.4.1 The dependency gate

**A task's pipeline may not start until every task it depends on is merged.** Not merely `done` —
merged, `PR.md.pr_state: merged`. `done` without merge means the code is not on the base branch, so a
dependent task would branch from a tree missing the thing it depends on and generate a conflict the
design never accounts for.

Checked at preflight check (a), before any work: for each id in `TASK.md.depends_on`, read that task's `TASK.md`
frontmatter and its `PR.md`. Any dependency not merged → `blocked`, `blocked_reason: deps-unmerged`,
naming which ones and their current stage. **The pipeline stops before step 02** — nothing is written,
no branch is created, nothing to unwind.

The consequence is deliberate and worth seeing clearly: **an unmerged PR stalls everything downstream
of it.** That is the correct behaviour — it is what keeps sequential delivery honest — but it means a
PR sitting in review blocks the phase, so `status` (§7.10) reports an unmerged PR as *the* thing
holding up the run rather than as a completed task.

**Escape hatch**: `require_merged_deps: false` in `config.md` relaxes the check to `status: done`, for
users who merge in batches. Off by default, because the failure it prevents is a conflict discovered at
step 05 — after implement, qa, and review have all been paid for.

**Hardening (optional, not v1)**: the same check as a `PreToolUse` bash hook on `git checkout -b`,
refusing branch creation when dependencies are unmerged. That moves enforcement from *the orchestrator
remembers* to *the harness refuses* — the same upgrade path as the schema-check hook (§12), and equally
free of a CLI. v1 relies on the preflight step, which always runs and cannot be skipped, because a pipeline that
begins at preflight by construction cannot begin anywhere else.

#### 7.4.2 Delivery failure modes

The push, pr-comments, and merge steps touch git, GitHub, and CI, and every one of these happens in a real project's first week.
Defined outcomes, not improvisation:

| Condition | Detected by | Action |
|---|---|---|
| Dependency not merged | preflight check (a) | `blocked: deps-unmerged` — before any work |
| Dirty working tree | `git status --porcelain` | `blocked: dirty-tree` — never stash, never commit someone else's changes |
| Base behind origin | `git rev-list --count @..@{u}` | `git pull --ff-only`; fails → `blocked: branch-conflict` |
| Branch already exists, same task | `git rev-parse --verify` | **Adopt it** — this is a resumed run, not a collision |
| Branch already exists, different task | branch name vs `TASK.md.id` | `blocked: branch-conflict` |
| Push rejected (non-fast-forward) | `git push` exit | Rebase onto base **once**, retry; fails again → `blocked: push-rejected` |
| PR already open for the branch | `gh pr list --head <branch>` | **Adopt it** — update `PR.md`, never open a second |
| `gh` not authenticated | `gh auth status` | `blocked: gh-auth` |
| CI still pending at merge gate | `gh pr checks` | **Report and hold** — not a block; present state and wait |
| CI red | `gh pr checks` | `blocked: ci-red`, naming the failing jobs |
| Merge conflict with base | `gh pr view --json mergeable` | `blocked: merge-conflict` — a human resolves; orqestra never auto-resolves |
| Re-running `/orqestra:task` after PR exists | stage derivation (§4.3) | Resume at pr-comments — the stage table makes this automatic |

Two principles behind the table. **Adopt, never duplicate** — an existing branch or PR for this task is
evidence of a resumed run, and creating a second is the one failure that is genuinely hard to undo.
**Never auto-resolve conflicts** — a rebase retried once is the entire automatic recovery budget;
anything beyond that is a human decision about intent, not a mechanical merge.

#### 7.4.3 The planning gate

**No task reaches implement without `PLAN.md` and `DESIGN.md`.** Both `done`, both in the task
directory, checked at preflight check (c) before any work and before any branch exists.

This is not a precondition the caller is trusted to have met. `/orqestra:task` is documented as taking
a task at stage `designed` or later, and for a long time that sentence was the only thing enforcing it —
which is to say nothing enforced it. A task whose code was written by hand and whose `IMPLEMENTATION.md`
was back-filled afterwards passes every other check in the pipeline: the tree is clean, the dependencies
are merged, qa runs, review runs, and the first artifact that records the omission is
`IMPLEMENTATION.md`'s own deviation table — written by the step that should never have run.

**Missing → backfill, do not block.** The pipeline dispatches what is missing, in order:

| State at preflight | Action |
|---|---|
| No `PLAN.md`, no `DESIGN.md` | Dispatch `plan`, then `design`, then gate the design |
| `PLAN.md` only | Dispatch `design`, then gate the design |
| Both present, one not `done` | **Block** — an artifact mid-flight is a resumed run, not a gap to fill |
| Both `done` | Continue to check (d) |

Backfilling rather than blocking is deliberate. The missing artifacts are recoverable by the two steps
that exist to produce them, and a block here would ask a human to run `/orqestra:plan` and
`/orqestra:design` by hand — the same manual route that produced the gap. **The design is always
re-gated after a backfill**, on the same reasoning as check (d)'s refresh: a human has not seen it.

**Why the check is presence, not the caller's word.** Stage derivation (§4.3) stops at the first gap, so
a task with `IMPLEMENTATION.md` but no `PLAN.md` derives as `created` — and `status` (§7.10) reports it
as *needing plan and design* while a full implementation sits in the directory. The derivation is right
and the report is misleading, which is why §7.10 flags artifacts found past the gap rather than
silently ignoring them.

### 7.5 `pr-comments` — delivery, sub-workflow and standalone

Runs as step 06 of the task pipeline, and standalone as `/orqestra:pr-comments <PR>` for a PR not tied
to an orqestra task (output goes to `work/PR-NNN/`).

```
step-fetch.md          gh pr view / gh api → all review comments and threads, human and bot
step-triage.md         → COMMENTS.md, one row per comment                   [GATE: triage]
step-resolve.md        per accepted comment: fix, routed by the task's module
step-verify.md         re-run the test suite; nothing regressed
step-reply.md          commit + push the follow-ups; reply to each thread; resolve threads
                          → RESOLUTION.md
step-recheck.md        re-fetch: new comments since? → loop to triage · none → done
```

`COMMENTS.md` triage table:

| # | thread | file:line | comment (summary) | verdict | action |
|---|---|---|---|---|---|
| 1 | t_abc | `Foo.java:42` | null check missing | `accept` | add guard + test |
| 2 | t_def | `Bar.ts:11` | rename to `x` | `discuss` | ask author: conflicts with convention |
| 3 | t_ghi | `Baz.go:88` | use a map here | `reject` | n≤3, O(n) is correct; reply drafted |

Verdicts: `accept` · `reject` (with drafted reasoning for the human to send) · `discuss` (needs the
human). **Never silently ignore a comment** — every one gets a row and a recorded outcome.

### 7.6 Planning skills

| Skill | Produces | Notes |
|---|---|---|
| `create-phases` | `PHASES.md` + `PHASE-N/PHASE.md` | Breaks PRD into milestones with `SC-N` success criteria. Rule: **build only what this phase needs now** — no infrastructure "for later". |
| `create-phase` | one `PHASE-N/PHASE.md` | Singular. For add-phase; appends, never renumbers finished phases. |
| `create-tasks` | `TASKS.md` + `TASK-NNN/TASK.md` | One task = one PR = one coherent change. Every task cites the `SC-N` it serves; a task serving none is out of scope. Assigns exactly one `module`. |
| `create-task` | one `TASK-NNN/TASK.md` | Singular. Used by bugfix promotion, and as the **task-splitting** entry point → `TASK-007a`/`007b`, original goes `superseded`. |

#### 7.6.1 Task sizing

**A task is as small as it can be and as big as it needs to be.** There is no target size, no story
points, no estimate. The test is coherence: *does this describe one change a reviewer can hold in their
head at once?*

The practical signal is **acceptance criteria count**. Past roughly five `AC-N` entries, a task is
usually two tasks wearing one name — and the cost is concrete, not aesthetic: one oversized task means
one oversized PR, one review that misses things, and a rework loop that churns because each attempt
fixes some criteria and breaks others.

**When a task is too big, split it — never shrink the criteria.** Dropping an `AC` to make a task fit
loses the requirement; splitting keeps all of them and puts them in order:

```
TASK-007  (8 AC, spans the API and the store)
   ↓ split
TASK-007a  session store        AC-1..AC-4   depends_on: []
TASK-007b  session API surface  AC-5..AC-8   depends_on: [TASK-007a]
```

The rules:

- The **original goes `superseded`**, never deleted. It records that the split happened and why.
- The split parts carry `depends_on` in the order the work must actually happen, so the dependency gate
  (§7.4.1) enforces the sequence rather than trusting anyone to remember it.
- **Every `AC` from the original lands in exactly one part.** No criterion is dropped, none duplicated —
  this is checkable, and it is the whole reason splitting is safe.
- Each part still cites the phase `SC-N` it serves. A split that produces a part serving no success
  criterion means the criterion was wrong, not the split.

Splitting is legitimate at three moments: during `create-tasks`, at the tasks gate when a human says
so, and mid-pipeline when `implement` blocks — that last case is `blocked_reason: needs-splitting`,
which routes to `create-task` rather than to rework, because no amount of retrying fixes a task that is
two tasks.

### 7.7 Step skills

Every step reads `decisions/INDEX.md` in addition to the artifacts below (§4.7). Output structure is fixed by
the schema catalogue (§4.8) and the shipped template — **deliberately not restated here**, because a
heading list written in two places is a heading list that will disagree with itself.

| Skill | Reads | Writes | Template |
|---|---|---|---|
| `plan` | `TASK.md`, `PROJECT.md` | `PLAN.md` | `templates/PLAN.md` |
| `design` | `TASK.md`, `PLAN.md` | `DESIGN.md` | `templates/DESIGN.md` |
| `implement` | `TASK.md`, `PLAN.md`, `DESIGN.md` | `IMPLEMENTATION.md` | `templates/IMPLEMENTATION.md` |
| `qa` | `TASK.md`, `DESIGN.md`, `IMPLEMENTATION.md` | `QA.md` | `templates/QA.md` |
| `review-task` | all of the above + the diff | `REVIEW.md` | `templates/REVIEW.md` |
| `review-phase` | every task in the phase | `PHASE_SUMMARY.md` | `templates/PHASE_SUMMARY.md` |
| `diagnose` | `BUG.md`, `PROJECT.md` | `DIAGNOSIS.md` | `templates/DIAGNOSIS.md` |

**`implement` deviation policy** (from nit; it prevents silent scope drift):

- **minor** (naming, file placement) → proceed, record it
- **moderate** (different approach, extra component) → proceed, record it
- **major** (the design is wrong, or scope must change) → **stop**, set `blocked`, do not implement past it

**`qa`** verifies criteria against actual behaviour, not intent. A criterion that cannot be satisfied
is a `blocked` outcome, not a failed test — the task or its criteria need changing.

### 7.8 Review lenses

**One review skill per scope, many stances — BMAD's "lenses" idea instead of five review skills.**
`review-task` is invocable standalone: `/orqestra:review-task <TASK-ID>`.

#### 7.8.1 The floor — always checked, never optional

**Lenses are elective; four checks are not.** They run on every review whatever lenses were given,
because each one guards a contract the pipeline depends on rather than a quality opinion:

| Floor check | Why it cannot be elective |
|---|---|
| **Module boundary** — every file in the diff inside the task's module `paths` (§5.2) | A file outside them is attributed to the wrong PR and reviewed by the wrong people. `major`. |
| **Unrecorded deviations** — `IMPLEMENTATION.md` accounts for what the diff actually did | An undeclared deviation defeats the whole deviation ladder, and nothing else looks for it. |
| **Criteria coverage** — every `AC-N` in `QA.md`'s map has a real assertion behind it | `qa` writes the tests and grades its own coverage. This is the only independent check on it, and putting it behind the `tests` lens meant a default run had none at all. |
| **Settled decisions** — no code contradicts an active `D-NNN` | Re-litigating a decision silently is how shared memory decays (§4.7). |

The distinction was missing before, and the omission was not cosmetic: `review-task`'s procedure ran
all four unconditionally while its rules said *apply only the lenses you were given*, so the skill
forbade recording what it had just instructed the reviewer to find.

#### 7.8.2 The lenses — elective attention

Selectable by argument or config, default `correctness,design`, and carried to the reviewer in the
envelope's `LENSES` field (§5.5):

| lens | Looks for |
|---|---|
| `correctness` | Does it do what the acceptance criteria say? Edge cases, error paths. |
| `design` | Fit with `DESIGN.md`'s components, interfaces, and boundaries; cohesion and coupling. |
| `security` | Injection, authz, secrets, unsafe defaults. |
| `performance` | Complexity, N+1, allocation in hot paths. |
| `regression-risk` | What existing behaviour could this break? (default for bug-derived tasks) |
| `tests` | Beyond the floor's coverage check: are the assertions real, or do they pass regardless? |

**The `design` lens stops at the boundary the design drew.** Cohesion and coupling that violate
`DESIGN.md`'s stated boundaries are findings. A simpler approach the reviewer would have preferred is
not — that is the *how I would have written it* judgement the whole skill forbids, and it used to be
licensed by the phrase "simplification opportunities" sitting in this very table. Such observations go
in `## Notes`.

#### 7.8.3 Severity carries the weight; `required` lists the ids

Verdict, in frontmatter: `passed` · `changes-requested` · `failed`.

`## Findings` rows carry `severity` (§4.4.3) and nothing else that grades them. The old `required`
column is gone: two independently-settable fields encoding one decision made `severity: nit,
required: yes` representable, and the template then spent three lines pleading against a state its own
schema permitted. One derivation rule replaces the plea:

> **Every `blocker` and `major` finding goes in frontmatter `required`. No `minor` or `nit` may.**

`required: [F-2, F-5]` is therefore an index, not a second opinion — mechanically derivable, and
checkable. It exists in frontmatter because **the orchestrator reads frontmatter only** (§4.4.1
Rule A) and must build `REWORK: address F-2, F-5` from it; before this the orchestrator was instructed
to name ids it had no contracted way to obtain.

**Choose between the last two deliberately** — they route differently (§8.1). `changes-requested` means
*fixable by implement*; it loops. `failed` means *rework cannot save this*; it stops and asks a human,
who may also order a re-review if the verdict itself looks mistaken. Marking something `failed` that is
merely hard to fix stops a pipeline that would have converged; marking something `changes-requested`
that is genuinely unbuildable burns all three attempts proving it.

### 7.9 `close-phase`

`/orqestra:close-phase <N>` — runs `review-phase` once every task in the phase is `done` (merged).

Verifies the phase **criterion by criterion** against actual behaviour, and aggregates deviations, tech
debt, and review findings across the phase's tasks, each tagged with its task. Writes
`PHASE_SUMMARY.md` with `criteria_met: true|false`.

If `false`, the phase does **not** advance — present the unmet criteria and let the human decide: add
tasks, or accept as-is. **The orchestrator does not invent gap tasks.**

### 7.10 `status` — the single state authority

`/orqestra:status` — globs `.orqestra/`, prints a table of every task with its derived stage (§4.3),
what is waiting on a human, and the single next command to run. Read-only.

**This skill is the only place in orqestra that derives state.** No orchestrator globs `.orqestra/`
itself; each one invokes `status` and reads its answer. That rule costs nothing to follow and buys two
things:

1. **No drift.** Five orchestrators inferring "which stage is this task at?" independently is five
   chances to disagree. One implementation cannot disagree with itself.
2. **A swap-ready seam.** Determining which files exist with which frontmatter is exactly the class of
   question GSD moved out of prompts and into `gsd-tools.cjs`, on the principle that *"deterministic
   logic belongs in code, not in prompts"* — an LLM answers it correctly almost always, and *almost*
   compounds badly over forty tasks. v1 stays codeless (§1.3 principle 2). If it misfires in practice,
   `skills/status/SKILL.md` grows a `state.cjs` beside it and **nothing else in orqestra changes** —
   because nothing else in orqestra knows how state is derived.

The seam is placed deliberately, in the one spot where prompt-based logic is weakest. See §12.

#### 7.10.1 Artifacts found past the gap

Stage derivation walks the chain and **stops at the first gap** (§4.3). That is correct — a task with no
`PLAN.md` is not `implemented` however many later artifacts exist — but stopping silently hides the one
state worth seeing: artifacts that exist *beyond* the gap, which can only mean a step ran that the
pipeline would not have dispatched.

`status` therefore reports the derived stage **and** names what it found past the gap:

```
⚠ TASK-019  agents invoke skills   plugin  created   IMPLEMENTATION.md, QA.md, REVIEW.md exist
                                                     past the gap → /orqestra:task TASK-019 backfills
```

Never report such a task as merely *needing plan and design*: that is true of the artifacts and false
about the work, and it is the reporting that let the gap survive nine commits. The next command is
`/orqestra:task <ID>`, whose preflight check (c) backfills the missing steps (§7.4.3).

### 7.11 Output conventions

You will read this output hundreds of times per project. It has one job: **say where you are, what
just happened, and what happens next** — in as few lines as possible.

**The iron rule: never print an artifact's contents.** Not at a step, not at a gate. The orchestrator
does not have the body in context anyway (§5.5.1), and printing it would defeat the reason it does not.
Everything below is built from frontmatter plus the agent's ≤10-line return.

**Dispatching a step** — one line, showing the resolved triple so routing is visible rather than
implicit:

```
▸ PHASE-1 / TASK-007 · implement · backend-engineer + java-expertise, test-quality
```

**Step completed** — one line, outcome from frontmatter:

```
✓ implement · 7 files · deviation: minor · 41s
✗ qa · 2 of 9 criteria failed → returning to implement (attempt 2 of 3)
```

**At a gate** — the agent's return lines verbatim, then `AskUserQuestion` (§6.1). Nothing else:

```
▸ GATE · review · TASK-007

  VERDICT  passed
  Findings 3 minor, 0 blocking. Retry logic reads cleanly; the backoff cap is
  arbitrary but harmless. Tests cover all 4 acceptance criteria.

  [ Approve ]  [ Reject with reason ]  [ Accept findings as tech debt ]
```

**Blocked** — reason, cause, and the specific next action. Never a bare status:

```
⛔ TASK-007 blocked · deps-unmerged
   TASK-004 is at stage `pushed` (PR #139 open, not merged).
   → merge #139, then: /orqestra:task TASK-007
```

**`/orqestra:status`** — the whole project in one table, then the single next command:

```
PHASE-1  Authentication                                   3/5 tasks

  TASK-004  session store      api       pushed      PR #139 open ← waiting on you
  TASK-005  login endpoint     api       designed    blocked by TASK-004
  TASK-006  logout             api       done        merged
  TASK-007  password reset     api       designed    ready
  TASK-008  login form         web       created     needs plan + design

→ Next: merge PR #139, then /orqestra:task TASK-005
```

Conventions: `▸` in progress · `✓` done · `✗` failed but recoverable · `⛔` blocked · `←` needs a human.
Stage names come from §4.3 verbatim, never paraphrased — the words in the table are the words in the
spec, so a user can look them up.

### 7.12 Skill inventory (v1)

```
PLANNING ORCHESTRATORS    DELIVERY ORCHESTRATORS    PLANNING SKILLS    STEP SKILLS
greenfield                task                      create-phases      plan
add-phase                 pr-comments               create-phase       design
bugfix                                              create-tasks       implement
                                                    create-task        qa
GATE CONTROL              UTILITY                   clarify            review-task
approve · reject          status · close-phase                         review-phase
unblock                                                                diagnose
```

This grid is the whole inventory. The folder name is the invocation name (§2), so it is also the
command list. No count is written here or in §2: `ls skills/` is the count, and a number stated in
prose is falsified by the next skill added — which is how this line came to say 22 twice, 1500 lines
apart, while the tree said otherwise. Expertise skills are pluggable, live in the project's own
`.claude/skills/`, and are not part of this inventory (§5.3).

---

## 8. Rework and escalation

The single rework rule, replacing nit's repair/rework/escalate protocol:

1. A step's output fails its **contract check** (§4.4) → re-dispatch once with the missing pieces named.
2. **qa fails** → back to `implement` with `QA.md` as input; `attempts++`.
3. A **review** returns `changes-requested` → back to `implement` with `REVIEW.md` as input; `attempts++`.
4. A **review** returns `failed` → **not a loop and not an automatic block.** See §8.1.
5. A **human rejects** at a gate → re-run that step with the rejection comment as input; `attempts++`.
6. `attempts` exceeds `max_attempts` (default 3) → set `blocked`, present everything tried, **stop**.
   Do not retry. A blocked task re-dispatched unchanged blocks again on the same step — fix the cause.

**Everything that loops, loops back to `implement`.** Not to the step that failed. qa failing does not
re-run qa; a rejected review does not re-run review. There is exactly one place work is redone, and
naming any other step as the rework target tells a reader the wrong thing about what happens next.

### 8.1 `changes-requested` versus `failed`

These are different failures and the workflow must not collapse them.

**`changes-requested` — the loop.** The work is fixable where it stands: named findings, a return to
`implement` with exactly those findings in `REWORK`, `attempts++`. This is the ordinary path and it
runs without asking anyone.

**`failed` — not the loop.** The reviewer is saying rework cannot save this: the approach is wrong, the
design does not hold, the task is not buildable as specified. Sending that back to `implement` burns
attempts on a problem implement cannot solve, and it is the single most wasteful thing the pipeline can
do.

But a `failed` verdict may also simply be **wrong** — a reviewer reading a stale design, missing
context, or applying a lens the task never claimed. So `failed` neither loops nor blocks. It offers two
routes, and a human chooses:

| route | when | effect |
|---|---|---|
| **Re-review** | The verdict looks mistaken — stale context, misread design, wrong lens | Re-dispatch `review-task` with why the first verdict is disputed. **Does not increment `attempts`** — no implementation work is being redone. Allowed **once**; a second `failed` goes to the human |
| **Ask the human** | The verdict looks right | Present the finding and stop. The decision is theirs: revisit the design, split the task, accept it as-is, or abandon it |

The budget matters: a re-review is cheap and sometimes correct, but two independent reviews reaching
`failed` is evidence, not noise. **Never re-review a third time** — at that point the disagreement is
about the task, not the code, and only a human can settle it.

**The budget lives in `REVIEW.md.review_round`** (`1` on a first review, `2` on a re-review), and it has
to. `attempts` deliberately does not increment, and the re-review overwrites the same `REVIEW.md` path,
so without the field a resumed session cannot tell a first `failed` from a second and the "once only"
rule silently becomes "as often as the pipeline restarts". This is the same reasoning that makes a gate
write `awaiting-approval` before calling `AskUserQuestion` (§6.1): **a budget enforced only by what the
orchestrator remembers is not enforced.** The orchestrator refuses a re-review when it reads
`review_round: 2` and goes straight to the human, carrying the superseded first review — recoverable
from the artifact commit that recorded it (§4.6).

`blocked` remains the outcome when the human chooses no route, or when they decide the design must be
revisited (`blocked_reason: design-invalid`). It is where `failed` may *end up*, never where it starts.

### 8.2 Recovery — un-wedging a run

Unblocking is a human act. `/orqestra:unblock <ID>` is the sanctioned path: it shows the recorded
`blocked_reason`, asks what was addressed, resets `status: in-progress` and `attempts: 0`, and appends
a line to the artifact recording that a human intervened and why. That last part matters — an unblock
with no record is indistinguishable from a bug next week.

**A blocked task re-dispatched unchanged blocks again on the same step.** Fix the cause first. This is
the rule people break, every time, because unblocking feels like progress.

#### What is safe to hand-edit

| Field | Safe? | Notes |
|---|---|---|
| `status` | ✅ | Only to `in-progress` after the cause is fixed, or `superseded` to abandon |
| `attempts` | ✅ | Reset to 0 when you have genuinely changed the inputs |
| `depends_on` | ✅ | Correcting a planning mistake is legitimate |
| Body prose | ✅ | Except: never to satisfy your own review feedback (§6.1) |
| `id`, `type`, `phase` | ❌ | These are the artifact's identity; the stage table (§4.3) reads them |
| Artifact filenames | ❌ | Stage derivation is by path. Renaming makes a task invisible |
| Deleting an artifact | ⚠️ | Legitimate, but it *means* something — see below |

#### The four recovery moves

1. **Redo a step** — **delete its artifact.** Stage derivation (§4.3) is by artifact presence, so
   removing `REVIEW.md` puts the task back at "verified" and the next `/orqestra:task` re-runs review.
   No status surgery, no special command. The artifact is recoverable from git (§4.6), which is what
   makes deletion safe enough to be the mechanism rather than a hazard.
2. **Abandon a task** — `status: superseded`, with a body note saying why. Never delete the directory;
   the record of an abandoned attempt is worth more than the tidiness.
3. **Roll back a phase plan** — `git revert` the planning commits. This is a capability artifact
   commits bought (§4.6): before them, a bad `PHASES.md` had to be hand-unwritten.
4. **Restart a task cleanly** — delete every delivery artifact (`IMPLEMENTATION.md` onward), reset
   `attempts: 0`, delete the branch and close the PR by hand. Planning artifacts survive; the task
   returns to "designed".

Note what these have in common: **the state model does the work.** Because artifacts *are* the state
(§4.1), recovery is file operations rather than a transition protocol — which is the payoff for not
having a `state.json` to repair.

---

## 9. Worked example

### Planning

```
/orqestra:init                     → .orqestra/ scaffolded, stack: java, gh auth ✓
  (write PRD.md)
/orqestra:greenfield
  · preflight               ✓
  · clarify                 → CLARIFICATIONS.md   (interactive)
  · create-phases           → PHASES.md, PHASE-1/PHASE.md (SC-1..SC-4)
           ▸ GATE                  → /orqestra:approve
  · create-tasks 1          → TASK-001 (backend), TASK-002 (backend), TASK-003 (frontend)
           ▸ GATE                  → /orqestra:approve
  · per task: plan → design → PLAN.md + DESIGN.md  ×3
           ▸ GATE                  → /orqestra:approve
  · handoff                 → "run /orqestra:task TASK-001"
```

### Delivery — one pipeline per task

```
/orqestra:task TASK-001
  · design-check            ✓ holds
  · implement    → backend-engineer + java-expertise, test-quality  → IMPLEMENTATION.md
  · qa           → qa-engineer + java-expertise                      → QA.md  [2 failures]
  · implement    → re-run with QA.md, attempts: 2                    → IMPLEMENTATION.md
  · qa                                                               → QA.md  [green]
  · review       → reviewer, lenses: correctness,design              → REVIEW.md [passed]
           ▸ GATE                  → /orqestra:approve
  · push         → git branch feat/TASK-001-user-auth, commit, push
                        → gh pr create                                      → PR.md  #142 open
  · pr-comments  → 4 comments: 3 accept, 1 reject (drafted reply)    → COMMENTS.md
                        → fix, verify, push, reply, resolve threads         → RESOLUTION.md
                        → re-check: no new comments                        ✓
  · merge        → CI green, 1 approval
           ▸ GATE                  → human merges → PR.md merged, TASK.md done

/orqestra:task TASK-002 …
/orqestra:task TASK-003 …

/orqestra:close-phase 1            → PHASE_SUMMARY.md  criteria_met: true
           ▸ GATE                  → /orqestra:approve → PHASE-1 done
/orqestra:add-phase                → plan PHASE-2
```

---

## 10. Scope boundaries

**In v1**

- Three planning workflows, one delivery pipeline, pr-comments as both step and standalone
- `close-phase`, standalone `review`, `status`
- Plugin distribution, `init` scaffolding, `gh` integration
- Markdown state with frontmatter, derived stages, contract checks
- Routing triple, 8 subagents, pluggable expertise skills
- Per-workflow gate configuration, one rework rule

**Explicitly out of v1**

| Deferred | Why |
|---|---|
| Brownfield adoption (codebase scan → `CODEBASE.md`) | Every workflow assumes an orqestra-built project. |
| Parallel delivery pipelines | The design permits it — pipelines are per task and independent — but v1 does not orchestrate it. Running two by hand is the user's risk. |
| ADRs, Phase Learning Records | nit has them; they earn their place only once the core loop is proven. |
| Module/boundary registry, dependency rules | nit's own experience: badly-drawn module boundaries make every task cross them. Not worth the cost in v1. |
| Any CLI or schema validation | Principle 2. Revisit only if contract checks measurably fail. |
| Non-GitHub forges | `gh` only. GitLab/Gitea would need a forge abstraction. |
| **Parallel research fan-out** (GSD) | Planning would dispatch N researchers at once — stack, features, architecture, pitfalls — each to its own file, then synthesize. Cheap and effective; considered for v1 and held back. First thing to add if planning quality disappoints. |
| **Punch lists** (GSD) | `QA.md` / `REVIEW.md` findings as numbered, closeable items with ids and severity, consumed one by one by the rework loop, instead of prose. Add when `attempts` churn becomes hard to diagnose. |
| **Size-adaptive pipelines** (BMAD v6) | `size: s\|m\|l` on a task, where `s` skips `plan` and `design`. Add when the seven-step pipeline starts feeling heavy on one-line changes — which is the signal BMAD rebuilt v6 around. |

---

## 11. Open questions

1. **Design staleness.** Planning designs every task in the phase up front, so `TASK-005`'s design is
   written against a codebase `TASK-001..004` will have changed. the preflight design check guards it, but
   the guard's judgement is the weak point. Alternative if it proves unreliable: planning writes
   `DESIGN.md` only for the first N tasks, and the delivery pipeline designs the rest just-in-time
   (nit's model). **Proposal:** ship the guard, measure, fall back if it misfires.
2. **CI wait at merge.** Should the merge step poll CI to green before gating, or report status once and
   hand over? **Proposal:** report once; polling is a background-task concern, not v1.
3. **Bot comments.** CodeRabbit and similar produce high-volume, low-signal comments. Should triage
   filter bots by default? **Proposal:** include them, but triage may batch-`reject` a bot thread with
   one drafted reply rather than one per comment.
4. **Expertise skill ownership.** Does orqestra ship a starter set (java, typescript, python), or only
   define the contract and let users bring their own? **Proposal:** ship none, document the contract,
   detect and warn on missing ones.
5. **PRD location.** `.orqestra/PRD.md` or repo-root `PRD.md`? nit uses repo root.
   **Proposal:** accept either, prefer repo root, path recorded in `config.md`.
6. ~~**`DECISIONS.md` growth.**~~ **Resolved** by the one-file-per-decision split (§4.7.1): every
   dispatch reads only `INDEX.md`, which grows one line per decision, and detail is opened on demand.

---

## 12. Appendix — how the reference frameworks use a CLI

Recorded because it is the decision orqestra most needs to keep revisiting. The three frameworks differ
in **how much authority lives in code rather than in the prompt**.

| | What the CLI does | What it never does |
|---|---|---|
| **nit** | Owns the state machine. `nit continue` computes the next step, dispatches, validates `output.json` against 26 JSON schemas, writes `state.json`. Plus `validate`, `route`, `approve`, `reject`, `boundaries`, `deps`. | Almost nothing structural is left to the LLM. |
| **GSD Core** | Two jobs. (1) Installer: `npx @opengsd/gsd-core`, cross-runtime. (2) **A query tool the commands shell out to** — `INIT=$(node ./.claude/get-shit-done/bin/gsd-tools.cjs init new-project)` returns JSON: which files exist, config values, current phase number. | It never *decides*. It answers factual questions about the filesystem. |
| **BMAD v6** | Installer (`npx bmad-method install`, commander-based, configures 20+ IDEs) plus three runtime Python scripts: `resolve_config.py` (merge base→team→user), `render_skill.py` (immutable project-specific snapshot; halts if mandatory instructions are missing), `sprint_plan.py` (deterministic planning — "project state tracked by evidence, not memory"). | No orchestration. The workflow itself stays LLM-interpreted Markdown. |
| **orqestra v1** | Nothing. `git` and `gh` are the only executables, invoked directly by the delivery pipeline. | — |

**The transferable principle**, stated outright by GSD: *"Deterministic logic belongs in code, not in
prompts."* The useful question is not *whether* to have a CLI but *which questions the LLM is bad at
answering*. Globbing a directory and reporting which files exist with which frontmatter is precisely
that class — done correctly almost every time, which across forty tasks means wrong repeatedly.

**Decision: no CLI in v1.** orqestra stays codeless and confines that question to one skill (§7.10),
so if it misfires the fix is one file rather than a refactor.

Two things make adding it later cheap, and both are deliberate:

1. **The state seam** (§7.10) — nothing but `status` knows how state is derived.
2. **The schemas are already mechanically checkable** (§4.4, §4.8). Ordered headings, closed
   vocabularies, `_none_` for empty sections, fixed table columns — every rule is `grep`-shaped on
   purpose. A checker does not need designing later; it needs writing.

The likeliest first exception is not a CLI at all. GSD's *hooks* — SessionStart version check,
PostToolUse formatting, a statusline showing the current task — are local shell, no install story, no
runtime dependency, and so do not violate principle 2. A `PostToolUse` hook that validates an artifact
against its schema on write (§4.4.5) would move enforcement from "the orchestrator remembers to check"
to "the harness checks", which is the single highest-value non-CLI determinism available.

**Watch for these triggers**, in likelihood order: state derivation consuming noticeable context on a
phase with 10+ tasks (a token problem you will feel before you see a bug); a resume landing on the
wrong step; the `attempts` counter looping or escalating early; contract violations getting waved
through. Any one of them, and `skills/status/state.cjs` earns its place.

Sources: [gsd-core](https://github.com/open-gsd/gsd-core) ·
[Anatomy of Claude Code Workflows](https://www.codecentric.de/en/knowledge-hub/blog/the-anatomy-of-claude-code-workflows-turning-slash-commands-into-an-ai-development-system) ·
[BMAD workflow architecture](https://deepwiki.com/bmad-code-org/BMAD-METHOD/8.1-workflow-architecture) ·
[BMAD installation](https://deepwiki.com/bmad-code-org/BMAD-METHOD/2.1-installation)

---

## 13. Build order for v1

The spec describes a destination. This is the route. Five milestones, each independently useful, each
ending in something you can actually run.

**The rule that shapes all of it: dogfood from M2.** From the moment planning works, orqestra plans
its own remaining milestones. nit found its worst design flaws this way — a framework that is painful
to use on itself is painful, and there is no other way to learn that as cheaply.

### M1 — The substrate

`init` · `status` · all 20 templates · the schema catalogue

Nothing orchestrates yet. `init` scaffolds `.orqestra/`, `status` reads an empty tree and says so.

**Why first:** `status` is the state authority (§7.10) and every later milestone calls it, so it is
built once and depended on everywhere. Writing all 20 templates before any skill also forces the
schemas to be real — a schema you have not written a template for is a schema you have not finished
designing.

**Done when:** `init` scaffolds a clean tree, `status` reports it correctly, and every catalogue row
has a template.

### M2 — Planning

`greenfield` · `clarify` · `create-phases` · `create-tasks` · `plan` · `design`

The first complete workflow: PRD in, designed tasks out. Gates, `AskUserQuestion`, artifact commits,
the decisions index, the dispatch envelope.

**Why second:** it exercises everything structural — dispatch, gates, schemas, commits, state
derivation — without touching git branches, `gh`, or CI. If the envelope or the return contract is
wrong, you find out here, where the only cost is a re-run.

**▶ Start dogfooding.** Use M2 to plan M3–M5.

**Done when:** a real PRD produces phases, tasks, plans, and designs, and re-running mid-way resumes
correctly rather than redoing work.

### M3 — The inner delivery loop

`task` steps 01–04 · `implement` · `qa` · `review-task`

Local delivery: preflight, implement, qa, review, rework. No push, no PR. The rework loop and the
`attempts` budget get exercised for the first time.

**Why here:** it is the highest-risk part of the design that does not involve the network. Prove the
loop terminates — that a `changes-requested` review actually converges instead of oscillating — before
adding remote state that makes failures expensive to unwind.

**Done when:** a task goes design → merged-quality code locally, and a deliberately bad implementation
converges through rework rather than looping to `max-attempts`.

### M4 — The remote

`task` steps 05–07 · `pr-comments` · the failure-mode table (§7.4.2)

Push, PR creation, comment triage and resolution, the merge gate. The dependency gate (§7.4.1) becomes
meaningful here, because until now nothing was merged.

**Why fourth:** every failure mode in §7.4.2 is a real-world condition you cannot simulate honestly
until real branches and real PRs exist. Build it when you can test it.

**Done when:** a task reaches a merged PR unattended except at gates, and each row of §7.4.2 has been
hit at least once — deliberately, by breaking things on purpose.

### M5 — The rest of the lifecycle

`add-phase` · `bugfix` · `close-phase` · `review-phase`

Second phase onward, bug intake through diagnosis and promotion, phase close.

**Why last:** all three are compositions of machinery M1–M4 already proved. `add-phase` shares
planning's tail; `bugfix` promotes a bug into a normal task and reuses the delivery pipeline whole;
`close-phase` reads artifacts that by now exist. Little new mechanism, mostly wiring — which is exactly
what you want at the end.

**Done when:** a full second phase runs end to end, and a bug goes report → diagnosis → task →
merged PR.

### Sequencing notes

- **M1 → M2 → M3 → M4 → M5 is a hard chain.** Each milestone consumes the previous one's output; there
  is no useful parallelism.
- **The three deferred features** (§11) have natural homes if their triggers fire: parallel research
  fan-out in M2, punch lists in M3, size-adaptive pipelines in M4 — where the seven-step pipeline first
  starts feeling heavy on small work.
- **The schema-check hook** (§12) is worth adding the first time M3's rework loop wastes a cycle on a
  malformed artifact. Not before — you will not know the shape of the failure until you see it.
- **Version 1.0** is the end of M5. Before that, the schema version stays `1` and changes stay additive
  (§4.8.4), because you are the only user and migration is not yet worth building.

---

## 14. The determinism charter

Skills must be deterministic in **structure**. Given the same inputs, the same step must touch the same
files, emit the same shape, and make the same routing choices — even when the prose inside differs.

**What cannot be made deterministic, and should not be faked:** the content. A good design, working
code, and a sound review judgement are model work, and pretending otherwise produces rigid skills that
fail on the first unusual task. Everything below constrains *structure, scope, and disposition* —
never the thinking.

Every skill cites these by number rather than restating them.

### D1 — Single writer

**Every artifact has exactly one skill permitted to write it.** Not "usually" — exclusively.

| Artifact | Sole writer |
|---|---|
| `PLAN.md` | `plan` |
| `DESIGN.md`, `decisions/D-NNN-*.md` | `design` |
| `IMPLEMENTATION.md` | `implement` |
| `QA.md` | `qa` |
| `REVIEW.md` | `review-task` |
| `PHASE_SUMMARY.md` | `review-phase` |
| `TASK.md`, `TASKS.md` | `create-tasks` / `create-task` |
| `PHASE.md`, `PHASES.md` | `create-phases` / `create-phase` |
| `PR.md` | `task` (`step-push.md`) |
| `COMMENTS.md`, `RESOLUTION.md` | `pr-comments` |
| `config.md`, `PROJECT.md` | `init`, then `design` for `PROJECT.md` |

Two writers means two shapes and a merge question nobody answers the same way twice.

### D2 — One write target per dispatch

A dispatch declares exactly one `WRITE:` path. **Any write outside it is a contract violation**, and
the orchestrator rejects the step rather than accepting the artifact. Source code is the sole exception,
and only for `implement` (production code) and `qa` (test code) — declared in the envelope, never
assumed.

### D3 — Artifact isolation

**A step working on one artifact may not touch another of the same kind.** Planning `TASK-007` must not
read, edit, or "while I'm here" fix `TASK-006`. Working in `PHASE-2` must not touch `PHASE-1`.

Cross-task reads happen **only** through the declared `READ:` list — which is how a task legitimately
sees its dependency's design, and the only way it does.

This is the rule most often broken with good intentions: an agent notices an inconsistency in a
neighbouring task and corrects it. The correction is invisible to that task's own pipeline, unreviewed,
and attributed to the wrong PR.

### D4 — Read-list closure

An agent uses **only** what the `READ:` list names, plus the repo files its own task concerns. Not
recollection, not inference about other tasks, not conventions it assumes exist. Something needed but
not listed is a **block**, not a guess — and usually means the envelope is wrong, which is worth
knowing.

### D5 — Frozen when done

An artifact with `status: done` that has been committed is **immutable**. The only path back is the
sanctioned rework route, which reopens it explicitly and increments `attempts`.

No skill edits a done artifact to make its own output fit. If `DESIGN.md` is wrong, `implement` blocks
with `design-invalid` — it does not quietly correct the design and proceed.

### D6 — Ordered procedure

A skill's numbered procedure runs **in order, none skipped, none reordered**. Where order genuinely does
not matter, the skill says so explicitly. Silence means it matters.

### D7 — Closed vocabularies

Every field another step branches on is an enum (§4.4.3). No free-text status, no invented severity, no
new blocked reason. A value outside the set is a contract failure, not a creative choice.

### D8 — Deterministic identifiers

| Id | Rule |
|---|---|
| `TASK-NNN` | `max(existing across all phases) + 1`. Global, never reset per phase, never reused |
| `D-NNN` | `max(existing) + 1`. Global across phases and workflows |
| `SC-N`, `AC-N`, `F-N` | Sequential within their artifact, from 1 |
| Split tasks | `TASK-NNNa`, `TASK-NNNb` — suffix the original, never renumber |
| Slugs | Lowercase, hyphens, from the title, ≤ 5 words, stop-words dropped |

Slug rules matter more than they look: they determine branch names and decision filenames, so an
ad-libbed slug means a resumed run cannot find its own branch (§7.4.2 "adopt, never duplicate").

### D9 — Precedence when sources conflict

Fixed, not judged:

```
decisions/D-NNN  >  TASK.md  >  DESIGN.md  >  PLAN.md
```

- `TASK.md` beats `DESIGN.md`: a design that does not satisfy the criteria is wrong, not the criteria.
- `decisions/` beats everything: a settled decision is settled. Code contradicting one is a finding; a
  design contradicting one is a block.
- **A conflict the chain does not resolve is `contradictory-input`** — block, never pick.

### D10 — Tie-breaking

When several options are equally valid, take the **lowest id**. Next actionable task, next finding to
address, next comment to resolve. Never "whichever seems most important" — that is the choice that
differs between two runs of the same state.

### D11 — Block by default

**When the correct action is unclear, block.** Do not improvise, do not pick the likely intent, do not
proceed on the balance of probabilities.

This is the disposition rule, and it is the one that buys the most determinism, because the largest
source of divergence is a model choosing to be helpful in an underspecified situation. A block costs one
human decision; a guess costs a rework cycle, or ships something nobody asked for.

### D12 — Self-verify and declare

Before returning, a skill checks its own artifact against the schema — frontmatter keys, vocabularies,
headings in order, no undeclared headings, `_none_` in empty sections — and states the result:

```
SCHEMA: ok
```

Declaring it forces the check to happen. The orchestrator verifies independently (§4.4.5); the
declaration is not trusted, it is a prompt to actually look.

### D13 — One task, one delivery

**A task must be deliverable by one engineer, in one PR, in one pipeline run.** A task requiring two
modules, two branches, or a partial merge is not a task — it is two, and it gets split (§7.6.1)
rather than attempted.

### D14 — One task, one module

**A task belongs to exactly one module** (§5.2). Not "usually one", not "one primarily".

This is the rule the rest of the routing rests on:

- **One module → one agent**, so dispatch resolves in a single lookup with nothing to weigh.
- **One module → one expertise set**, so the conventions loaded are the right ones and only those.
- **One module → one `paths` list**, which makes the boundary *checkable*: `review-task` flags any file
  in the diff outside it as a `major` finding. Artifact isolation (D3) stops being an instruction an
  agent may drift from and becomes something a reviewer verifies against the actual diff.
- **One module → one coherent PR**, reviewed by the people who own that area.

A change spanning two modules is **two tasks**, ordered by `depends_on` (§7.6.1). The apparent
exception — a shared interface change — is still two tasks: define the contract in the owning module,
consume it in the other. That ordering is not overhead; it is the thing that makes the dependency gate
(§7.4.1) able to guarantee the contract exists before anything consumes it.

`create-tasks` blocks on a module not in the registry (D11) rather than inventing one, and `implement`,
`design`, and `plan` all block with `needs-splitting` when the work escapes their module.

### D15 — No parallelism

One step at a time within a task; one task at a time within a phase. Even where steps look independent.
Concurrency is the fastest way to make a run unreproducible, and orqestra gains nothing from it that
sequencing does not already give.

### D16 — Copy templates literally

A template is copied from `templates/`, not reproduced from memory. Structure regenerated from
recollection drifts within a handful of uses — which is the entire reason the templates ship as files.
