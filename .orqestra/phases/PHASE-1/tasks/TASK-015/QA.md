---
id: TASK-015
type: qa
status: done
updated: 2026-08-26
task: TASK-015
result: passed
test_command: git show 5bc3ec5 --stat; md5sum region-compare of REQUIREMENTS.md against HEAD~2; obligation table applied to the 9 real envelopes in skills/
---

## Test Strategy

A specification change, so behaviour is what the amended §5.5 **permits, requires, and contradicts** for
its two consumers: a human reading it, and an orchestrator composing a dispatch from it. Nothing below
is taken from `IMPLEMENTATION.md`; every claim was re-derived from `REQUIREMENTS.md` and the diff.

**1. Per-criterion textual conformance.** §5.5's body (lines 856–948) read as a dispatching
orchestrator would, asking of each criterion the question its consumer actually asks, and cross-checking
every citation it makes (§5.1, §5.1.1, §5.3, §7.0.1, §7.8.1, D-004, D-024, D2, D4, D16) against the
cited text rather than trusting the reference.

**2. Structural regression, byte-level.** The renumbering hazard cannot be caught by reading, because a
stale `§5.5.1` citation still resolves — to the wrong text. So: heading list extracted from both
revisions and compared as text; the two untouched regions compared by checksum.

**3. The obligation table exercised, not read.** AC-2 is only met if the table yields yes/no per field
with no interpretation, so it was applied to all nine real envelopes in `skills/` — every field each
one carries and every field it omits, including fields §5.5 does not name.

## Results

| check | outcome |
|---|---|
| `git show 5bc3ec5 --stat` | `REQUIREMENTS.md` 58/4 and the task's `IMPLEMENTATION.md`. No other file |
| headings, count | 106 → 106 |
| `md5sum` lines 1–861, old vs new | `708871…` = `708871…` — identical |
| `md5sum` old 896–2031 vs new 950–2085 | `c47f72…` = `c47f72…` — identical |
| net effect | the whole change is confined to old 862–895 → new 862–949; §5.5.1 still `#### 5.5.1`, uniform +54 shift |
| `grep -i "loads first"` | 0 hits; the superseded wording is gone, not duplicated elsewhere |
| obligation table vs 9 `skills/` envelopes | 9/9 decided on every field the table names; 2 fields it does not name (see I-4) |

**AC-2 exercised.** `skills/task/step-review.md` — scope `TASK`, task has a module, so `MODULE` `PATHS`
`STACK` `EXPERTISE` are mandatory and all four are absent: **non-conformant**, decided from frontmatter
the orchestrator already read. `skills/greenfield/step-phases.md` — `create-phases`, no module, the four
correctly absent: **conformant** on that class (it carries no scope field, which the "always" class does
require). The remaining seven decide the same way. That divergence is TASK-019's by D14/D-019 and is
declared as debt, not as done — verified: all eight `agents/*.md` `tools:` lines still omit `Skill`, and
§5.5 states the grant as a precondition it cannot enforce rather than asserting it exists.

## Criteria Coverage

| criterion | covered by | result |
|---|---|---|
| AC-1 | §5.5 `EXPERTISE` paragraph reads "the agent **invokes** those too"; the precondition is in its own text — `Skill` in the dispatched agent's `agents/*.md` `tools:` — with §7.0.1 and D-024 cited, and §7.0.1 verified to actually say that layer binds for the whole subagent run. Unmet-precondition failure named (silent degradation to bare persona). No surviving `Read`-implying wording in §5.5 | passed |
| AC-2 | The three-class obligation table plus the closing sentence ("an omission is a contract violation rather than a judgement call … rejected exactly as a missing `WRITE:` is", D2). Exercised against all nine real envelopes | passed, see I-2, I-3, I-4 |
| AC-3 | §5.5's example carries all eight always-mandatory fields plus all four conditionals, in the stated order, with `REWORK` marked re-dispatch-only. `MODULE:` and `PATHS:` occurred nowhere in `REQUIREMENTS.md` before and are now defined in prose with consumers named, not merely shown | passed, see I-1 |
| AC-4 | `SKILL` defined as the namespaced step skill the agent invokes, separated from `STEP` by the divergence that proves one field cannot serve both — `STEP: review` → `SKILL: orqestra:review-task`, checked against §5.1.1's own row. Consumer named (the dispatched agent), grounded in D4 | passed |
| AC-5 | "Why the skill is invoked and never read" states the asymmetry (expands on invoke, literal string on `Read`) **and** its consequence (a dead `TEMPLATE:` path, D16 unfollowable), and derives from it why `SKILL` is a name. §5.5's own `TEMPLATE:` corrected from the bare `templates/IMPLEMENTATION.md` | passed |
| regression: no renumbering | 106/106 headings, heading text identical, `#### 5.5.1` intact | passed |
| regression: no collateral edit | both untouched regions checksum-identical despite the file being rewritten whole through `Write` | passed |

## Issues

**I-1 — minor. §5.5's example contradicts §5.1's module registry.**

- *Criterion*: AC-3.
- *Observed*: `MODULE: api` alongside `EXPERTISE: java-expertise, test-quality`. §5.1's registry gives
  the `api` row as `java-expertise, spring-conventions`.
- *Expected*: `java-expertise, spring-conventions`, or a `MODULE` whose row matches.
- *Why it is this change's defect*: the `EXPERTISE` line is pre-existing and was unfalsifiable while no
  `MODULE` was shown. Adding `MODULE: api` is what makes it checkable — and it now fails the rule §5.5
  itself states two paragraphs later, that `MODULE` "resolved `ROLE`, `STACK`, `EXPERTISE`, and `PATHS`
  from one `modules.md` row". `ROLE`, `STACK` and `PATHS` match the row; only `expertise` diverges.

**I-2 — minor. The condition names only `TASK.md`/`BUG.md`, leaving `PHASE`-scoped dispatches undecided.**

- *Criterion*: AC-2.
- *Observed*: "mandatory **iff** the scope unit has a module — its `TASK.md`/`BUG.md` frontmatter
  carries `module:`", excusing `create-phases`/`create-tasks` by name. `close-phase`'s `review-phase`
  dispatch is `PHASE`-scoped *after* its tasks have modules, and neither clause reaches it.
- *Expected*: decidable from the text. The right answer exists — `templates/PHASE.md` frontmatter has no
  `module:` key, verified — but it is reached by inference from a file §5.5 never names.

**I-3 — minor. §5.5's opening sentence now contradicts its own table.**

- *Criterion*: AC-2.
- *Observed*: line 860 still reads "the envelope is a fixed block of text — **same fields, same order,
  every dispatch, every workflow**". The new table makes four fields legitimately absent from
  `create-phases` and `create-tasks` envelopes and calls that "conformant, not an exception".
- *Expected*: one statement, not two. The specific table governs the general sentence (D9), so a careful
  reader lands right; a reader who stops at the opening line concludes every envelope must carry all
  twelve fields — which is the judgement call AC-2 exists to remove. The sentence was true before this
  change and was left unamended by it.

**I-4 — minor. The table classes no step-specific field, though AC-2 asks for exactly that.**

- *Criterion*: AC-2 ("states which fields are mandatory in every envelope **and which are step-specific**").
- *Observed*: the classes are always / scope / conditional-on-module / re-dispatch-only. `LENSES:` and
  `ROUND:`, which `skills/task/step-review.md` carries and which §7.8.2 requires be conveyed per
  dispatch, appear nowhere in `REQUIREMENTS.md` — `grep 'LENSES'` returns 0 hits. Applying the table to
  that envelope therefore yields verdicts on the four fields it is missing and **no verdict at all** on
  two of the fields it has: undeclared extras are neither permitted nor forbidden.
- *Expected*: a class covering step-specific fields, or an explicit statement that the list is closed and
  a field outside it is a violation. `REWORK` is currently the only field the section treats as
  step-scoped, and it is named in the list.

None of the four falsifies a criterion; all four are single-line corrections inside §5.5. Severity is
the reviewer's to grade — I-3 and I-4 sit closest to AC-2's own wording.
