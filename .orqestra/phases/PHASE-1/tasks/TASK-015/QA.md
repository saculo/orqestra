---
id: TASK-015
type: qa
status: done
updated: 2026-08-27
task: TASK-015
result: passed
test_command: python3 scratchpad/table.py <9 envelopes + §5.5's own example>; git diff 5bc3ec5 39393f8; heading-list diff vs 27349b1 and 5bc3ec5; python3 scripts/check-templates.py
---

## Test Strategy

Round 2, after the rework that closed `REVIEW.md` F-1 and F-2 (both on AC-2). All five criteria were
re-verified from `REQUIREMENTS.md` as it stands at `39393f8`, not from `IMPLEMENTATION.md`, and AC-1,
AC-3, AC-4, AC-5 were re-checked for regression rather than assumed intact.

**1. The obligation table executed, not read.** AC-2 is met only if the table returns a verdict per
field with no interpretation, so §5.5's four classes and its new closed-list rule were **encoded as a
program** and run over the nine real envelopes in `skills/` and over §5.5's own example. The program
decides from exactly what the text says it may decide from — `STEP`, the scope field, and whether the
scope unit's frontmatter carries `module:` — and prints `UNDECIDED` wherever the text yields no answer.
That is the check round 1 could not make mechanically, because two carried fields had no class at all.

**2. Per-criterion textual conformance, citations resolved.** Every section §5.5 cites was opened and
read against the claim made about it: §7.0.1 (the `tools:` layer binds for a whole subagent run),
§5.1.1 (`review` → `review-task`, the divergence AC-4 rests on), §8.1 (`review_round` 1/2, the claim
the new `ROUND` row makes), §7.8.2, §4.4.1 Rule B, D2/D4/D-004/D-024.

**3. Structural regression, by diff and heading list.** The renumbering hazard cannot be caught by
reading — a stale `§5.5.1` citation still resolves, to the wrong text. Heading lists were extracted
from the pre-task baseline (`27349b1`), from round 1 (`5bc3ec5`), and from `HEAD`, and compared as text.

## Results

| check | outcome |
|---|---|
| `git diff 5bc3ec5 39393f8 -- REQUIREMENTS.md` | 3 hunks: §5.5 opening (F-1), the table + closing paragraph (F-2), one clause in §7.8.2 (the recorded minor deviation). Nothing else in a 2093-line file |
| commit contents | `REQUIREMENTS.md` (inside `docs` `PATHS`) + this task's `IMPLEMENTATION.md`. No other file |
| headings, count | 106 (baseline) → 106 (round 1) → 106 (HEAD) |
| heading text, baseline vs HEAD | **identical, line for line** — nothing added, moved, or renumbered; `#### 5.5.1` intact |
| table applied to 9 `skills/` envelopes | **9/9 decided on every field carried**; 0 undeclared fields (round 1: 2). 7/9 fully decided on required fields; 2 hit `UNDECIDED` on the module condition — F-4, open by instruction |
| table applied to §5.5's own example | required-but-missing: **none**; carried-but-undeclared: **none** |
| `grep "same fields" REQUIREMENTS.md` | 0 hits — the contradicting clause is gone, not moved |
| `grep "LENSES\|ROUND" REQUIREMENTS.md` | now 2 and 1 hits, defined with consumers; both were 0 in round 1 |
| `python3 scripts/check-templates.py` | 20 templates, all conform |

**F-2 exercised, not inspected.** `skills/task/step-review.md` carries `LENSES:` and `ROUND:`. Before
the rework the table returned *no verdict at all* on them; it now returns `permitted` (step-specific,
mandatory on a `review` dispatch), and returns `VIOLATION-not-permitted` for the same fields on any
other step — the program tests both branches. Every other envelope's carried fields land in a declared
row, so the closed-list rule fires on nothing that exists today, which is what "closed" should mean
after the classes are complete.

## Criteria Coverage

| criterion | covered by | result |
|---|---|---|
| AC-1 | §5.5's `EXPERTISE` paragraph (912–922): "the agent **invokes** those too", precondition stated in its own text as `Skill` in the dispatched agent's `agents/*.md` `tools:`, with §7.0.1 and D-024 cited — §7.0.1 opened and verified to actually say that layer is a true allowlist binding for the whole subagent run. Unmet-precondition behaviour named (silent degradation to bare persona). No `Read`-implying wording survives in §5.5. Unchanged by the rework diff | passed |
| AC-2 | The four-class obligation table (934–946) plus **The list is closed** (946–953), executed as a program over 9 real envelopes and §5.5's example. Every field carried by every envelope now resolves to exactly one row; the step-specific class AC-2 names by word exists; an unlisted field is a stated violation, grounded in Rule B (§4.4.1). The opening sentence (859–861) now defers to the table instead of contradicting it, so the D9 tie-break AC-2 exists to remove is no longer needed | passed, see I-1 |
| AC-3 | §5.5's example (865–885) run through the same program: 13 fields, every one the table marks mandatory for an `implement` dispatch present, zero undeclared, in the order §5.5 fixes (`ROLE STEP SKILL TASK MODULE PATHS STACK EXPERTISE READ TEMPLATE WRITE REWORK RETURN`), `REWORK` annotated re-dispatch-only. `MODULE:` and `PATHS:` occur nowhere else in `REQUIREMENTS.md` and are defined in prose with consumers named. Not regressed: the rework did not touch the example | passed, see I-2 |
| AC-4 | The `SKILL` paragraph (893–899): namespaced step skill, the agent **invokes** it, separated from `STEP` by the case that proves one field cannot serve both — `STEP: review` → `SKILL: orqestra:review-task`, checked against §5.1.1's step table, which gives exactly that pairing. Consumer named (the dispatched agent), grounded in D4. Not regressed | passed |
| AC-5 | "Why the skill is invoked and never read" (901–910): the expansion asymmetry stated (expanded on invoke, literal string on `Read`), tied to its consequence (an unopenable `TEMPLATE:` path, D16 unfollowable), and used to derive why `SKILL` carries a name. §5.5's own `TEMPLATE:` line carries `${CLAUDE_PLUGIN_ROOT}`, with the mirror-image reason given. Not regressed | passed |
| regression: no renumbering | Heading list identical to the pre-task baseline; 106/106/106; `#### 5.5.1` still the return contract, so all ten citations to it still resolve | passed |
| regression: no collateral edit | The rework diff is 3 hunks, two in §5.5 and one recorded as a deviation; the commit touches no file outside `docs` `PATHS` plus its own artifact | passed |
| regression: deviation covered | The `minor` deviation (§7.8.2 gains "carried to the reviewer in the envelope's `LENSES` field (§5.5)") verified in place at 1445–1446 and consistent with the new table row; no heading touched | passed |

## Issues

**I-1 — the module condition still leaves two real dispatches undecided (F-4, open by instruction).**

- *Criterion*: AC-2.
- *Observed*: the program returns `UNDECIDED-module-condition` for `skills/close-phase/SKILL.md`
  (`review-phase`, `PHASE`-scoped) **and** for `skills/add-phase/step-define-phase.md`
  (`create-phase`) — neither is a `TASK`/`BUG` scope nor one of the two steps excused by name.
- *Expected*: a verdict from the text alone. This is `REVIEW.md` F-4, deliberately left open, and is
  **not graded here**. Recorded only because the mechanical run widens it by one dispatch:
  `create-phase` is hit by the same gap as `review-phase`, so naming `templates/PHASE.md` would need to
  cover both.

**I-2 — §5.5's example still contradicts §5.1's registry (F-3, open by instruction).**

- *Criterion*: AC-3.
- *Observed*: `MODULE: api` with `EXPERTISE: java-expertise, test-quality`; §5.1's `api` row (731) gives
  `java-expertise, spring-conventions`. Re-verified unchanged at `HEAD`.
- *Expected*: the row's value. Left open per the rework instruction and **not graded**.

Both remaining issues are the two `minor` findings the rework was told not to address. No new defect was
introduced by it, and nothing that AC-1, AC-3, AC-4 or AC-5 rests on moved.
