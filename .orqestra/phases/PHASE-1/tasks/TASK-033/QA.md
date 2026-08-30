---
id: TASK-033
type: qa
status: done
updated: 2026-08-30
task: TASK-033
result: passed
test_command: python3 scripts/check-templates.py && python3 scripts/check-decisions.py && python3 scripts/check-step-refs.py && python3 scripts/check-envelopes.py
---

## Test Strategy

Round 2, against `5ce1077`. Three things: close round 1's findings, re-run the regression baseline,
and — the actual job — attack what an absence-blind check would *still* miss after round 1's lesson.

Test code was **not** written, for the same reason as round 1: the natural regression check for AC-3
and AC-4 is a `scripts/check-*.py`, and `scripts/` is the `plugin` module, outside this task's `PATHS`
(D14, D2). Stated rather than skipped. This remains the honest gap in the task — see Issues.

**Round 1's insight applied to round 1's own output.** Every defect found so far was an *absence*, and
both earlier sweeps passed by searching for what was present. So round 2 ran no substring greps for
`diagnose` at all. It ran **set-difference in both directions** between each enumeration and `ls
skills/`, and then **between the enumerations themselves**, because three lists that must stay in sync
is the same defect class as one hard-coded count and nothing in the repo checks it.

| what I ran | why that shape | result |
|---|---|---|
| §7.0 class table (:1077–1086) ∆ `ls skills/`, **both directions** | a class table with 23 rows can still be wrong two ways: a skill on disk with no class, or a class row with no directory | 23 tokens. `in table, not on disk` = **`diagnose` only**; `on disk, not in table` = **∅**. `diagnose` is the deliberate case — the spec leads (D-019) — and it is the *only* one |
| §7.12 grid ∆ `ls skills/`, both directions | §7.12 now *claims* completeness in prose, so the claim is checkable | 23 tokens. grid-only = **`diagnose` only**; tree-only = **∅**. `init` is present at :1657. Round 1's F3 is closed and the sentence is now true |
| **§7.0 class table ∆ §7.12 grid** (symmetric difference) | the cross-list check nothing in the chain had run. Two independent 23-item enumerations that must agree | **∅ — set-identical.** They agree exactly |
| §5.1.1 routing (7 rows) ⊆ class table, and §7.7 (7 rows) ⊆ class table | routing and §7.7 are subsets by construction, not enumerations of all skills; the checkable property is containment | both **⊆**, no orphans. All four tables agree on the token `diagnose` |
| every line of `REQUIREMENTS.md` naming ≥3 skill tokens, each read | catches an enumeration in a form neither round's patterns describe — a prose list, a code fence, a milestone roster | 32 lines. Two are exhaustive (§7.0, §7.12, both clean above). §13's M1–M5 rosters (:1917/1931/1947/1974) omit `diagnose` — **and also omit `approve`, `reject`, `unblock`, `create-phase`, `create-task` in `master`**, so they are demonstrably not exhaustive and assert no completeness. Not a defect |
| `analyst.md`'s `tools:` vs §7.0's `step` row | R2's class choice is a claim about tool permissions, and D-024 says `agents/` `tools:` is the durable allowlist. Checkable against the tree rather than reasoned about | `tools: Skill, Read, Write, Glob, Grep` — exactly `step`'s `allowed-tools` plus `Skill` (D-025), no `Bash`, no `Edit`. `diagnose`'s dispatched agent already **has** the permissions `step` grants and **lacks** the ones it removes. `step` is corroborated by the tree, not just argued |
| `Twenty-two artifacts` (:553) — counted, not assumed | the prompt's third question. A catalogue is a list that goes stale | §4.8.1 has **exactly 22 rows**. The number is **correct**. Its companion at :294 is not — see Issues |

## Results

| check | exit | note |
|---|---|---|
| `check-templates.py` | 0 | 21 templates conform |
| `check-decisions.py` | 0 | 28 decisions conform |
| `check-step-refs.py` | 0 | 40 step references resolve |
| `check-envelopes.py` | **1** | sole failure `skills/bugfix/step-diagnose.md:8 [diagnose] missing SKILL — always class`. **Expected**, per Out of Scope; TASK-034's AC-3. `config.md`'s `test_command` exits 1 for this reason and this reason only |

**Byte-identity, diffed not eyeballed.** `master:583` and `HEAD:584` — the `` | `BUG.md` | `bugfix`
intake | `` row — compare **`True`** on a Python string equality of the whole line. Only the line
number moved.

**No renumbering.** The full heading list (`^#{1,6} `) extracted from `git show master:REQUIREMENTS.md`
and from `HEAD`: 108 and 108, `a == b` → **`True`**. Text, order, and numeric prefixes all hold. Every
`§N` citation across the tree survives.

Tree state: `git status` clean apart from two pre-existing untracked `ORQESTRA_*.md`. The rework is
committed at `5ce1077`; nothing committed by me. `git diff master...HEAD --stat` on `REQUIREMENTS.md`
is 37 lines touched across 9 hunks.

## Criteria Coverage

| criterion | covered by | result |
|---|---|---|
| AC-1 | §4.8.1:585 is `` \| `DIAGNOSIS.md` \| `diagnose` \| `` — one backticked token, the shape `plan`/`design`/`qa`/`review-task` use. Verified again this round *and* extended: §7.7:1463 now names `templates/DIAGNOSIS.md`, and that file **exists** in `templates/`, so the catalogue row's writer and template both resolve. `check-templates.py` covers it (21 conform). §4.8.1:584 byte-identical to `master` (above); truthful under D-028 — `grep -rn '^ROLE:' skills/bugfix/` returns exactly one hit, `step-diagnose.md:8` | **pass** |
| AC-2 | §5.1.1:786 `` \| diagnose \| `diagnose` \| `analyst` \| module's \| ``. Resolving the step yields `diagnose`, not nothing. The name is unambiguous: four tables (§4.8.1, §5.1.1, §7.7, §7.12) spell it `diagnose` and `grep -in diagnos` over the whole file shows **no second spelling** — no `bugfix-diagnose`, no `root-cause`. The namespaced form `orqestra:diagnose` is forced, not guessed: D-012 makes the folder name the invocation name, §2:42 shows the `orqestra:` namespace, and §5.5 gives `STEP: review → SKILL: orqestra:review-task` as the worked example. TASK-034's AC-3 has exactly one spelling available to it. `analyst` matches `step-diagnose.md:8`'s `ROLE: orqestra:analyst` (D-014) and `agents/analyst.md` exists | **pass** |
| AC-3 | **Both halves now pass.** *Every site agrees*: four independent enumerations checked by set-difference against the tree and against each other — §7.0 class table and §7.12 grid are **set-identical at 23**, with `diagnose` the sole spec-leads entry in each and **nothing on disk missing from either**; §5.1.1 and §7.7 both contain `diagnose` and are proper subsets with no orphans. Round 1's F2 (§7.0 omitted `diagnose`) is closed at :1081, and the `step` class is corroborated by `analyst.md`'s actual `tools:` line, not only by argument. Round 1's F3 (`init` absent from the grid) is closed at :1657 under the retitled `UTILITY / SETUP` column, so "the whole inventory" is now true rather than newly false. *No renumbering*: 108 headings, identical to `master`, diffed | **pass** |
| AC-4 | No skill count survives anywhere. Round 1's F1 is closed — §7.0:1072 now reads `Every skill has to be written consistently`, keeping what the sentence communicated and dropping the quantity. Re-swept this round by **quantity-near-noun** in three notations (digits, number-words `one`–`thirty`/`dozen`, and quantifiers `all`/`every`/`whole`/`none` within 25 chars of `skills?`): the only surviving hit near `skills` is §1.3:69 `nit has 21 skills`, a fact about a different, frozen project that orqestra adding a skill does not falsify — **read, not assumed**, and correctly kept, with §1.3's own orqestra-side clause now saying `a comparable number of skills` instead of `22`. §2:119 and §7.12:1660 assert no number. TASK-034 raising the tree to 23 falsifies nothing in the spec | **pass** |

## Issues

No defect against any acceptance criterion. Two items recorded, neither an AC failure.

**N1 — pre-existing, outside AC-4 as written: `§4.3:294` says "all twenty artifacts" and `§4.8:553`
says "Twenty-two artifacts", about the same catalogue.**

- **Where**: `REQUIREMENTS.md:294` and `:553`. Both **unmodified by this branch** — present verbatim in
  `master` at `:293`/`:552`, and the diff touches neither.
- **Observed**: §4.8.1 has exactly **22** rows. `:553`'s `Twenty-two` is therefore **correct**, and the
  prompt's question is answered: it is right, not stale. `:294`'s `twenty` is **wrong by two**, and the
  two sentences contradict each other 259 lines apart.
- **Expected**: one number, or none. This is the same decay class AC-4 names — a count in prose that the
  next catalogue row invalidates — and the same shape as the two skill counts this task removed, `22`
  asserted twice, far apart, with the tree disagreeing.
- **Why not a fail**: AC-4 is scoped to a *skill* count ("A number that every new **skill** invalidates"),
  and the TASK.md amendment note scopes it the same way. An artifact count is a different noun and a
  different task. Reporting it rather than widening the criterion, and rather than letting round 2 close
  without recording what it found. Companion to the already-recorded `§13:1917/1922 "all 20 templates"`
  against 21 conforming templates. **Recommend one task covering all three prose counts** — it is one
  edit and one defect class, and filing it now is cheaper than the next task tripping over it.

**N2 — no automated guard exists for what round 1 and round 2 both had to find by hand.**

- **Observed**: the enumeration agreement verified above — §7.0 ∆ §7.12 ∆ `ls skills/` — holds today
  because I ran it once, by hand, in a scratch script. Nothing in `scripts/` runs it. The next skill
  added reopens exactly the defect this task spent two rounds closing, silently, because no substring
  grep can see a missing table row.
- **Expected**: a `scripts/check-skill-tables.py` in the shape of the four existing checks, asserting
  set-equality between §7.0's class table, §7.12's grid, and `ls skills/` (allowing a spec-leads
  entry). **`scripts/` is the `plugin` module** — writing it here would cross a module boundary (D14),
  so this is a filing, not an omission. It is the cheapest possible check and it would have caught F2,
  F3, and both of round 2's cross-list questions before a human ever read the file.
