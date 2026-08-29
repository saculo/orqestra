---
id: TASK-029
type: qa
status: done
updated: 2026-08-30
task: TASK-029
result: passed
test_command: python3 scripts/check-templates.py
---

## Test Strategy

A spec change has no behaviour to execute, so the rule was executed instead. §5.5's amended
obligation table has exactly one consumer — `scripts/check-envelopes.py` and the ten dispatch
envelopes under `skills/` — so the amended rule was transcribed into a throwaway harness in the
scratchpad and run over all ten real envelopes plus eight synthetic fixtures. Neither `scripts/`
nor `skills/` was edited; both belong to the `plugin` module and TASK-030 owns them (D-019, D14).

The harness encodes only what §5.5:934–953 now says: scope is exactly one of `TASK` `PHASE` `BUG`
`PROJECT`; `MODULE` `PATHS` `STACK` `EXPERTISE` are mandatory iff the scope key is `TASK` or `BUG`.
The fixtures exist to prove the amendment still *discriminates* — a rule that turns the checker green
by admitting everything is the TASK-008 defect class, and is the specific regression this task risks.
Envelope field order and the `config.md` `project:` source were checked against the real files
rather than against `IMPLEMENTATION.md`'s account of them.

## Results

- `python3 scripts/check-templates.py` — 21 templates, all conform, exit 0.
- Hand-execution of the amended §5.5 over `skills/*/*.md` — 10 envelopes: **8 conform, 2 violate**.
  Both violations are pre-existing and out of this task's scope:
  `skills/bugfix/step-diagnose.md:8` missing `SKILL` (unrelated to this amendment; carried tech debt
  from TASK-015), and `skills/greenfield/step-phases.md:13` carrying no scope line at all — the
  envelope edit TASK-030 owns.
- Synthetic fixtures — **8 of 8 as expected**, 0 unexpected. Critically: `TASK`-scoped with all four
  module fields omitted → violation; `TASK`-scoped with only `EXPERTISE` dropped → violation;
  `BUG`-scoped with all four omitted → violation. The amendment does **not** widen to `TASK`/`BUG`.
- Heading structure: `diff` of every `^#{2,4} ` line, `master` vs `HEAD` — identical. No `§N`
  citation across the ~90 citing files breaks.
- `grep` for the struck clause (`scope unit has a module`, `create-phases` and `create-tasks`,
  `omit all four`) across `REQUIREMENTS.md`, `skills/`, `agents/`, `templates/` — zero hits. The old
  wording survives nowhere; there is no second, stale statement of the rule to disagree with the new one.

## Criteria Coverage

| criterion | covered by | result |
|---|---|---|
| AC-1 | Applied the amended conditional row to all ten envelopes reading **only** the scope key on the line after `SKILL` — never a step body, a `TASK.md` frontmatter, or a step-name list. All ten classes settled from that one lookup; the field-order claim ("one line immediately after `SKILL`") holds in 9 of 10 real envelopes and fails only in `step-diagnose.md`, which has no `SKILL` line at all. Scope-field paragraph at :934–940 states what a project-wide dispatch carries and why. | pass |
| AC-2 | `greenfield/step-phases.md:13` plus a `PROJECT: orqestra` line satisfies every row of the amended table while carrying no `TASK`/`PHASE`/`BUG` value — verified as fixture "PROJECT-scoped, none of the four" → conform. The value source is real and needs no invention: `.orqestra/config.md` frontmatter carries `project: orqestra`, `project` is a required key per §4.8:563, and §5.5:988 states config.md is "read by every orchestrator", so the composer already has it. Checker clause struck by §8.2 amendment, not graded. | pass |
| AC-3 (F-3) | §5.5's example envelope `EXPERTISE:` at :872 is now `java-expertise, spring-conventions`, byte-identical to §5.1's `api` row at :731. | pass |
| AC-3 (F-4) | The amended row closes `close-phase/SKILL.md:38` and `add-phase/step-define-phase.md:16` **generically**: both are `PHASE`-scoped with none of the four, both graded conformant by the harness with no edit to either file. Neither is named anywhere in the amended text; the row's discriminator is the scope key, backed by `templates/PHASE.md` carrying no `module:` key (confirmed by grep). `greenfield/step-tasks.md:14`, previously excused by name, is now covered by the same general clause. | pass |
| Regression (module fields must stay mandatory under `TASK`) | Three fixtures above, plus the three real `TASK`-scoped envelopes (`task/step-implement.md:32`, `task/step-qa.md:9`, `task/step-review.md:14`) re-read from `HEAD` — all three carry `MODULE` `PATHS` `STACK` `EXPERTISE`, and the amended rule requires all four of them. Nothing currently caught becomes legal. | pass |
| Regression (citations) | Heading diff `master...HEAD` — identical. | pass |

## Issues

| id | severity | where | issue |
|---|---|---|---|
| I-1 | minor | REQUIREMENTS.md:949 | "Omitted under `PHASE` and `PROJECT`" does not say whether omission is *required* or merely *not required*. A `PHASE`-scoped envelope carrying `MODULE` is a violation under the strict reading and conformant under the loose one. No real envelope is affected today (no `PHASE`/`PROJECT` envelope carries any of the four), so this is not a criterion failure — but TASK-030 has to pick one to encode, and picking it in `scripts/` rather than in the spec is exactly the one-way link F-4 was about. Suggest the spec state it. |
| I-2 | minor | REQUIREMENTS.md:709, :1590, :1777 | F-3's underlying mismatch is fixed only where F-3 pointed. Three other places still pair the `api` module with `java-expertise, test-quality`, contradicting §5.1:731's `java-expertise, spring-conventions`. AC-3 passes — F-4's finding named :870 and the review explicitly scoped it there ("pre-existing elsewhere in the file, which is why it is not a major") — but the file remains internally inconsistent in three spots, and a reader hitting :709 first will learn the wrong pairing. |
| I-3 | minor | `scripts/` | The amended rule wants an executable test, and this QA's harness is a throwaway in the scratchpad, not a committed one. Writing it into `scripts/` would cross into the `plugin` module (D14), so it is **not** written here. TASK-030 should carry it: at minimum the eight fixtures above, so that the checker's `SCOPE`/`MANDATORY_SCOPES` constants cannot be widened later without a test going red. |
| I-4 | informational | repo-wide | `python3 scripts/check-envelopes.py` exits 1 for the window between this task merging and TASK-030 landing — it still hardcodes `SCOPE = ["TASK","PHASE","BUG"]`. Independently confirmed, matches `IMPLEMENTATION.md`'s recorded tech debt, and is by design under D-019. Nothing here should be "fixed" first. |
| I-5 | informational | `agents/architect.md` | The branch carries an 11-line change to `agents/architect.md`, outside the `docs` module's `PATHS`. It is its own commit (`d2d1a41`) with an `orqestra:` scope, so it is not attributed to TASK-029 — noting it so review does not read it as a `PATHS` breach. |
