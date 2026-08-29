---
id: TASK-029
type: design
status: awaiting-approval
updated: 2026-08-30
task: TASK-029
decisions: [D-027]
---

## Components

Four amendments to `REQUIREMENTS.md` §5.5, plus one decision file. No new section, no renumbering.

| # | Component | Responsibility | Serves |
|---|---|---|---|
| C1 | **The scope row, amended** | The obligation table's scope row admits a fourth key, `PROJECT`, and states that exactly one of `TASK` `PHASE` `BUG` `PROJECT` appears. A dispatch composed before any scope unit exists carries `PROJECT`. | AC-1, AC-2 |
| C2 | **The conditional row, amended** | `MODULE` `PATHS` `STACK` `EXPERTISE` are keyed off the **scope key**, not off a list of step names and not off `TASK.md`/`BUG.md` specifically: mandatory under `TASK` and `BUG`, omitted under `PHASE` and `PROJECT`. The named-steps clause (`create-phases` and `create-tasks`) goes. | AC-2, AC-3 (F-4) |
| C3 | **The scope-field paragraph** | One short paragraph of prose before the obligation table stating what the scope field is and why `PROJECT` exists — the project-wide dispatch has no unit to name, and a rule no envelope can satisfy is a broken rule. House convention: every rule states its reason. | AC-1 |
| C4 | **The example envelope's `EXPERTISE` line** | `MODULE: api` in the §5.5 example must carry §5.1's `api` row verbatim — `java-expertise, spring-conventions`, not `java-expertise, test-quality`. Two statements of one row that disagree is the exact failure §5.1 exists to prevent. | AC-3 (F-3) |
| C5 | **`decisions/D-027-project-is-a-scope-value.md`** | Records the scope-key contract as durable, with its `Constrains` line, because it fixes the shape of every future dispatch and every future envelope check (§4.7). | AC-1 |

C4 is a one-line correction with no relationship to C1–C3; it is here only because AC-3 covers F-3, it
is inside this module, and leaving it costs a future reader a contradiction to resolve.

## Interfaces

**The scope line, after the amendment.** Exactly one of these appears in every envelope, in the scope
position (immediately after `SKILL`, before `MODULE`/`READ`):

```
TASK:      PHASE-1/TASK-007        # a task
PHASE:     PHASE-1                 # a phase
BUG:       BUG-003                 # a bug
PROJECT:   orqestra                # every phase / the project itself — no scope unit exists yet
```

`PROJECT`'s value is the project name as recorded in `.orqestra/config.md` `project:`. That file is
read by every orchestrator (§6), so the value is already in hand at compose time and §5.5's closing
invariant — *every condition is answered by something the orchestrator has already read to route the
dispatch* — still holds. The key, not the value, is what any rule reads.

**The conditional class, after the amendment.** One lookup answers it:

| scope key | `MODULE` `PATHS` `STACK` `EXPERTISE` | because |
|---|---|---|
| `TASK` | mandatory | `TASK.md` frontmatter carries `module:` |
| `BUG` | mandatory | `BUG.md` frontmatter carries `module:` |
| `PHASE` | omitted | `templates/PHASE.md` frontmatter carries `id`, `type`, `status`, `updated`, `phase`, `criteria_count` — **no `module:`**. Verified. |
| `PROJECT` | omitted | there is no scope unit at all |

The `EXPERTISE`-additionally row, the `LENSES`/`ROUND` row and the `REWORK` row are untouched. The
closed-list paragraph is untouched: `PROJECT` is admitted by a row, so the list stays closed.

**What this makes true of the real envelopes**, all outside this module and edited by TASK-030:

- `greenfield/step-phases.md` gains `PROJECT:` and keeps omitting all four module fields — conformant
  by the rule, not by an exception naming it. That is AC-2.
- `close-phase/SKILL.md` and `add-phase/step-define-phase.md` are `PHASE`-scoped and omit all four
  today. They become conformant **unchanged**, by the rule rather than by enumeration. That is F-4.
- `greenfield/step-tasks.md` and the seven `TASK`/`BUG`-scoped envelopes are unaffected: their class is
  what it was, so no currently-caught omission becomes legal.

## Structure

Everything lands in the `docs` module — `REQUIREMENTS.md` only. `README.md` is listed in the module row
but does not exist in the repository, so no work follows from it.

Inside `REQUIREMENTS.md` the change is confined to **§5.5's body**: the obligation table's first two
data rows and one paragraph of surrounding prose, plus the one-line correction in §5.5's example
envelope. §5.5.1 and everything after it are untouched, and nothing is renumbered — no `§N` citation in
any skill breaks. This is deliberate and is the reason the table is amended in place rather than
extended with a §5.5.2: a second place stating the obligation is a second place to disagree with the
table, and §5.5 already declares the table "the only thing that answers" the field question.

**What must not reach into what.** No file under `skills/` or `scripts/` is touched here. `scripts/
check-envelopes.py` paraphrases this table in its docstring and enforces `SCOPE = ["TASK","PHASE","BUG"]`;
it will keep failing `step-phases.md` after this task merges, and that is correct — TASK-030 owns both
the checker and the ten envelope edits (D-019: docs states the rule, `plugin` applies it). An edit to
either from this task is an out-of-module change review must flag `major` (§5.2, §7.8.1, D2).

**Order.** C1 and C2 are one edit, not two. If the scope row admits `PROJECT` while the conditional row
still keys off "the scope unit has a module", a dispatch with no scope unit has no defined answer for
the four module fields and the defect reopens one level down. C3 follows the table edit; C4 is
independent of all of it.

**Not a schema change.** §4.8's three-edit rule (D-003 — catalogue row, `templates/` file, the skill
that writes it) does not apply: the envelope is a prose contract composed by orchestrators, not an
artifact schema. It has no §4.8 catalogue row and no file in `templates/`. `REQUIREMENTS.md` is the
whole edit surface.

## Decisions

- **`PROJECT` is a fourth scope value rather than a separate marker field, and the scope key decides the
  module class — D-027.** Both amended rows then resolve from one lookup, which is what AC-1 demands:
  read the key, know the class. A separate marker would leave two discriminators for a reader to
  reconcile, and the discriminators the plan weighed — the `READ` list, a list of step names — both
  require reasoning about what a dispatch "really" operates on. The plan's Rule B objection to a fourth
  value (a constant field with no consumer, §4.4.1, D-011) does not survive the human's marker decision:
  the scope key already has a consumer, because it is what the conditional row keys off. This extends an
  existing consumer instead of adding an unread field.
- **The value is the project name, not a literal `PROJECT`.** `PROJECT: PROJECT` is noise, and a scope
  line that names its unit stays uniform with the other three. Nothing branches on the value — the key
  carries the information — but the agent cites it exactly as it cites `MODULE`.
- **The conditional row states the module condition generically and names no step.** Naming steps is
  what F-4 records: the `create-phases`/`create-tasks` clause went stale the moment `close-phase` and
  `add-phase` were written, and any replacement list would go stale the same way. Local to this task.
- **F-3 is fixed here rather than restated as open.** It is one line, inside this module, and its cost
  is a contradiction between §5.5's example and §5.1's registry. Local to this task.
- **AC-2 is graded on its first clause only**, and AC-3 on F-3 and F-4 — per the human amendment
  recorded in `TASK.md` (§8.2). Not re-argued here.

## Test Strategy

Markdown; the proof is inspection against the real envelopes, done by reading, not by running.

| AC | What proves it |
|---|---|
| AC-1 | Take the amended scope row and the amended conditional row and apply each to all ten envelopes under `skills/` without reading any step's body: the scope key is visible on line 4 of every envelope, and the class follows from it with no second lookup and no judgement. Any envelope whose class cannot be settled from the key alone fails this criterion. |
| AC-2 | `greenfield/step-phases.md` as it stands, plus a `PROJECT:` line, satisfies every row of the amended table — and does so carrying no `TASK`, `PHASE`, or `BUG` value. Check the negative too: the amendment must not make the four module fields omittable for any `TASK`-scoped envelope. Walk `step-implement.md`, `step-qa.md`, `step-review.md` and confirm all four are still mandatory for them. |
| AC-3, F-4 | The amended conditional row, read against `close-phase/SKILL.md:38-41` and `add-phase/step-define-phase.md:16-19`, makes both conformant **with no edit to either file**, and does it via `templates/PHASE.md`'s missing `module:` key rather than by naming them. If either still needs an exception, F-4 is not resolved. |
| AC-3, F-3 | §5.5's example envelope `EXPERTISE` line matches §5.1's `api` row character for character. |
| Regression | No heading number in `REQUIREMENTS.md` changes. Confirm by diffing the `^#{2,4} ` lines before and after; any change there breaks citations across every skill. |
