---
id: TASK-015
type: implementation
status: done
updated: 2026-08-27
task: TASK-015
deviation: minor
files_changed: 1
---

## Changes

**Rework round 1 — `REVIEW.md` F-1 and F-2 only, both on AC-2.** F-3 and F-4 were left untouched, as
instructed. Everything from the first round stands unchanged; the five components (C1–C5) are still in
`REQUIREMENTS.md` §5.5 exactly as recorded below in the previous round's account, which this section
now supersedes only where the two findings touch it.

**F-1 — §5.5's opening sentence no longer contradicts the table it introduces (REQUIREMENTS.md:856–860).**
The clause *"same fields, same order, every dispatch, every workflow"* stated as universal what the new
obligation table makes conditional, so a reader stopping at the opening line and a reader reaching the
table came away with different contracts and needed D9 to break the tie. The **order** half was true and
survives in bold; the **fields** half now says what is actually the case — the envelope draws from a
closed set, and *which* of those fields a given dispatch must carry is answered per field by the table,
"and it is the only thing that does". The sentence now points at the table instead of pre-empting it.

**F-2 — the table declares a step-specific class, and closes the list (REQUIREMENTS.md:932–945).**
Two gaps, one finding. The classes were always / scope / conditional-on-module / re-dispatch-only, none
of which is the step-specific class AC-2 names and DESIGN.md C4 promised; and an undeclared field was
neither permitted nor forbidden, so applying the table to a `review` dispatch returned no verdict at all
on the `LENSES:` and `ROUND:` that `skills/task/step-review.md:17–18` actually carries. Both are closed:

- A fifth row — `LENSES` `ROUND`, **step-specific**: mandatory on a `review` dispatch and permitted on
  no other, with each field's meaning and consumer named (`LENSES` the resolved lens set, §7.8.2;
  `ROUND` the `1`/`2` the reviewer writes to `REVIEW.md.review_round`, §8.1) and their position in the
  fixed order stated — immediately after the scope field, which is where the real envelope puts them.
  The intro line now reads *four* obligation classes, not three.
- A closing paragraph states that **the list is closed**: a field in no row is not part of the envelope,
  and adding one is a contract violation in the same way an omission is, because a field no step is
  contracted to read is one the receiving agent may ignore — Rule B (§4.4.1) applied to the envelope
  rather than to frontmatter. The existing "an omission is a contract violation rather than a judgement
  call" sentence is preserved verbatim inside it.

`LENSES` and `ROUND` previously returned zero hits in `REQUIREMENTS.md`; both now appear, defined.

**Structural verification.** No heading was added, moved, or renumbered. §5.5 is still line 856; §5.5.1
moved 950 → 957 (+7, the whole of the §5.5 edit) and keeps its number, so the ten return-contract
citations still resolve to the return contract. Every anchor before §5.5 is unmoved (§5.1 at 718),
everything between §5.5 and §7.8.2 shifted by exactly +7 (§7.0.1 1075 → 1082, §7.8.1 1420 → 1427), and
everything after by exactly +8 (§8.1 1604 → 1612, D2 1952 → 1960, D16 2082 → 2090) — the +1 being the
deviation below. Uniform shifts are the check that no text outside the two edited regions changed.

## Deviations

| deviation | from design | what | why |
|---|---|---|---|
| minor | `## Structure`: "§5.5's body … is the entire write surface" | One clause added to §7.8.2's intro line (REQUIREMENTS.md:1443–1444): the lens default is now "carried to the reviewer in the envelope's `LENSES` field (§5.5)" | F-2's evidence was that §7.8.2 "describes lenses as selectable without ever putting them in the envelope". Declaring `LENSES` in §5.5 while the section that owns lenses stays silent leaves the same one-way link that let the field exist in `skills/` unnoticed by the spec. One clause, no heading touched, inside `docs` `PATHS` |

## Tech Debt

- **Nine envelopes in `skills/` are non-conformant as of this merge**, plus `skills/task/SKILL.md:64`,
  which restates §5.5's field list inline and now disagrees with it. Unchanged from round 1 and still
  the intended sequencing (D14, D-019) — but the step-specific row narrows the gap by one: with
  `LENSES`/`ROUND` now declared, `step-review.md` is short only `MODULE`, `PATHS`, `STACK`, `EXPERTISE`
  rather than carrying two fields the spec did not recognise at all.
- **`agents/architect.md` grants no `Edit`.** The `docs` module routes `implement` to `architect`
  (§5.1.1), so a two-finding rework of a 2086-line file was again done by rewriting the whole file
  through `Write`. It verified clean (uniform anchor shifts, above), but this is the second round on the
  same mechanism and the review already flagged it as a growing gamble. The fix is one word in
  `agents/architect.md` `tools:` — TASK-019's file, alongside the `Skill` grant this amendment
  presupposes.
- F-3 (REQUIREMENTS.md:870, the `api` row's `expertise` disagreeing with §5.1:731) and F-4
  (REQUIREMENTS.md:939, a `PHASE`-scoped `review-phase` dispatch reached by neither clause of the
  module condition) are **not addressed**, per the rework instruction. Both are `minor` and both remain
  open against §5.5.
