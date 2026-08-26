---
id: TASK-015
type: qa
status: done
updated: 2026-08-26
task: TASK-015
result: passed
test_command: git diff master..HEAD -- REQUIREMENTS.md; heading/anchor and byte-region comparison against master
---

## Test Strategy

This is a specification change, so "actual behaviour" is what the amended §5.5 **permits, requires, and
contradicts**. Nothing here is inferred from the implementation report; every claim below was
re-derived from the file and the diff.

Three kinds of check were run.

**Textual conformance, per criterion.** Read the amended §5.5 body (lines 856–948) as a dispatching
orchestrator would, and asked of each criterion the question a reader would actually ask.

**Structural regression, mechanically.** The renumbering hazard is the one that cannot be caught by
reading, because every stale `§5.5.1` citation still resolves — it just resolves to the wrong text
(21 citations of `5.5.1` across `agents/`, `skills/`, `REQUIREMENTS.md`, `.orqestra/`). So the check
was byte-level, not visual:

- heading list extracted from both revisions and `diff`ed as text (106 vs 106, identical strings);
- every heading at or after old line 896 confirmed to shift by **exactly +54**, every heading before
  it confirmed **unmoved**;
- `cmp` of old lines 1–861 against new 1–861, and of old 896–2031 against new 950–2085.

Both `cmp` runs are byte-identical. The entire change is confined to old 862–895 → new 862–949. This
is stronger than the implementation's own heading-count argument and independently confirms it.

**Mechanical-rule exercise (AC-2).** The obligation table is only worth anything if it yields a yes/no
per field without interpretation, so it was applied to all nine real envelopes in `skills/` — including
the two the design named as hardest. Verdicts fell out of the condition column alone; see below.

## Results

| check | outcome |
|---|---|
| `git diff --numstat master..HEAD` | `REQUIREMENTS.md` 58/4; `IMPLEMENTATION.md` 71/0. No other file in the diff |
| headings, count | 106 → 106 |
| headings, text | `diff` of the two heading lists: **empty**. No heading added, dropped, reworded, or renumbered |
| anchor shift | every heading from old 896 onward: exactly **+54**. Every heading before: **+0** |
| `cmp` lines 1–861 (old vs new) | identical |
| `cmp` old 896–2031 vs new 950–2085 | identical |
| collateral edit | **none** — no reflow, rewording, or drop anywhere outside §5.5's body, despite the whole file being rewritten through `Write` |
| `grep "loads first"` in `REQUIREMENTS.md` | 0 hits — the superseded wording is gone, not duplicated |
| AC-2 rule applied to 9 envelopes | 9/9 decided with no judgement call |

**AC-2 exercised, not just read.** Applying the table to the two cases the design flagged:

- `skills/task/step-review.md` — scope `TASK: PHASE-1/TASK-007`, a task with a module, so all four of
  `MODULE` `PATHS` `STACK` `EXPERTISE` are mandatory. It carries none. Verdict: **non-conformant**, and
  the verdict required nothing but the frontmatter the orchestrator already read.
- `skills/greenfield/step-phases.md` — `create-phases`, no scope unit with a module, so the four are
  correctly absent. Verdict: **conformant on those four**. (Separately it carries no scope field at
  all, which the "always" class does require — also TASK-019's, per the same debt entry.)

The rule also decides the cases the design did not name: `step-plan-design.md` (both envelopes) and
`step-qa.md` are non-conformant, `step-diagnose.md` conformant except `PATHS`. Nine for nine, no
interpretation. That is what AC-2 asked for.

**The intentional divergence is recorded as debt, not as done.** §5.5 states the `Skill` grant as a
**precondition it cannot enforce** ("This requires `Skill` in the dispatched agent's `agents/*.md`
`tools:`") and names the failure when it is unmet — it never asserts the grant exists. Verified against
reality: all eight `agents/*.md` `tools:` lines still omit `Skill`, and all eight personas still say
"Load the module expertise skills". `IMPLEMENTATION.md` records both the nine `skills/` envelopes and
`skills/task/SKILL.md:64`'s now-disagreeing inline field list under `## Tech Debt`, attributed to
TASK-019 (D14, D-019). Correct sequencing, correctly declared.

## Criteria Coverage

| criterion | covered by | result |
|---|---|---|
| AC-1 | §5.5 `EXPERTISE` paragraph: "the agent **invokes** those too"; precondition stated in its own text as `Skill` in `agents/*.md` `tools:` with §7.0.1 and D-024 both cited; unmet-precondition failure named (silent degradation to bare persona). `grep`: no surviving "loads first" | passed |
| AC-2 | Obligation table, three classes; condition is `TASK.md`/`BUG.md` frontmatter carrying `module:` — mechanical, as the design settled it. Closing sentence states the consequence ("an omission is a contract violation rather than a judgement call... rejected exactly as a missing `WRITE:` is", D2). Exercised against all 9 `skills/` envelopes | passed |
| AC-3 | §5.5's example now carries every always-mandatory field (`ROLE` `STEP` `SKILL` scope `READ` `TEMPLATE` `WRITE` `RETURN`) plus all four conditionals, in the fixed order. `MODULE:` and `PATHS:` occurred **nowhere** in `REQUIREMENTS.md` before this change and are now **defined in prose**, each with its consumer named, not merely shown in the block | passed, see I-1 |
| AC-4 | New `SKILL` field, defined as the namespaced step skill the agent invokes; separated from `STEP` by the case that proves one field cannot serve both (`STEP: review` → `SKILL: orqestra:review-task`); consumer named (the dispatched agent), grounded in D4 | passed |
| AC-5 | "Why the skill is invoked and never read" states the asymmetry (expands on **invoke**, literal string on `Read`) *and* its consequence (a dead `TEMPLATE:` path, making D16 unfollowable). §5.5's own `TEMPLATE:` line corrected from the bare relative `templates/IMPLEMENTATION.md`, with the mirror-image reason given | passed |
| regression: no renumbering | 106/106 headings, heading text `diff` empty, uniform +54 shift from old line 896 | passed |
| regression: no collateral edit | `cmp` byte-identical on both untouched regions; diff confined to §5.5's body | passed |

## Issues

**I-1 — minor. §5.5's example now contradicts §5.1's own module registry.**

- *Criterion*: AC-3 (the example must be conformant to what §5.5 declares).
- *Observed*: the example reads `MODULE: api` with `EXPERTISE: java-expertise, test-quality`. §5.1's
  registry gives the `api` row as `java-expertise, spring-conventions`.
- *Expected*: `EXPERTISE: java-expertise, spring-conventions`, or a `MODULE` whose row matches.
- *Why it is a defect of this change*: the `EXPERTISE` line is pre-existing and was harmless while no
  `MODULE` was shown. Adding `MODULE: api` is what makes it checkable — and it now fails the check that
  the same section's new prose states two paragraphs later: "`MODULE` is ... the single key that
  resolved `ROLE`, `STACK`, `EXPERTISE`, and `PATHS` from one `modules.md` row". `STACK: java` and
  `PATHS: services/api` do match the row; only `expertise` diverges. The canonical example of the rule
  therefore demonstrates a violation of it. One-word fix. (`skills/task/step-qa.md` carries the same
  pair, but that is `plugin` and out of scope — D14.)

**I-2 — minor. The obligation table's condition names only `TASK.md`/`BUG.md`, leaving `PHASE`-scoped dispatches undecided by the literal text.**

- *Criterion*: AC-2 (an omission must be a violation, not a judgement call).
- *Observed*: the condition reads "mandatory **iff** the scope unit has a module — its
  `TASK.md`/`BUG.md` frontmatter carries `module:`". The prose then excuses `create-phases` and
  `create-tasks` by name. Neither covers `close-phase`'s `review-phase` dispatch, which is
  `PHASE`-scoped **after** its tasks have modules. A reader must decide whether the enumeration means
  "look at `PHASE.md` too, find no `module:`, omit the four" or "this rule does not address `PHASE`
  scopes".
- *Expected*: the right answer is reachable — `templates/PHASE.md` frontmatter carries no `module:`
  key, so a phase never has one and the four are correctly omitted — but it is reached by inference
  from a file §5.5 does not name, which is one inference more than AC-2 allows.
- *Suggested*: name the scope unit's own frontmatter generically, or add `PHASE.md` to the enumeration.

Neither issue falsifies a criterion; both are single-line corrections inside §5.5 and are for the
reviewer to grade.
