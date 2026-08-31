---
id: TASK-037
type: qa
status: done
updated: 2026-08-31
task: TASK-037
result: passed
test_command: python3 scripts/check-templates.py && python3 scripts/test-check-envelopes.py && python3 scripts/check-envelopes.py
---

## Test Strategy

Round 2, scoped to the rework at `3209fbf` (`REQUIREMENTS.md` only) and to the two criteria that failed.
`docs` is `markdown`; its tests are `scripts/check-*.py`, which are `plugin` and outside this module's
`paths` (§5.2, D2) — **no test files added or edited**, as in round 1.

Three things were verified, in this order.

**(i) The one-line change is a resolution, not a relocation.** `:930`, `§5.5:957`, `§7.3:1213`, `§5.1.1:795`
and `D-029`'s `**Constrains:**` were each re-read in full and checked pairwise, not by grep.

**(ii) The sentence kept its point.** AC-3 is satisfiable by an edit that is accurate and useless — the
grading question was whether the bold lead and the "boundary rather than a hint" clause survived, since a
sentence that becomes true by losing "MODULE and PATHS come from the routing row, never from the agent's
judgement" would pass a narrow reading and fail the criterion.

**(iii) A third sweep, deliberately unlike both earlier ones.** Round 1 anchored on `carr.* \`module:\``;
the rework anchored on `MODULE`, "the task's", "the row", `re-deriv|infer`. Both are **rule-shaped**
searches, so both would still miss a constraint stated in a **narrative or an example** and one that
constrains `MODULE` **without naming it**. So round 2 read, in full and not grepped: **§5's opening
example** (`:707`), the **§5.5 envelope example** (`:877`), the **§4 frontmatter example** (`:239`), the
**§7.3 bugfix narrative and §7.3.1** (`:1210-1247`), **§5.5.1**, the **step I/O table** (`:1466`), the
**status/report examples** (`:1598`), the **`work/BUG-001/` tree** (`:403`), and **§9 Worked example**
(`:1767`) — chosen because a contradiction survives in prose that constrains the value while naming only
`modules.md`, "the row", or "routing".

## Results

Every checker run **directly** from the repository root at `3209fbf`, never through `config.md`'s
`test_command`, whose `&&` short-circuits at the templates red — behind it, the remaining four never
execute and a "pass" would be a result that was never produced.

| command | exit | outcome |
|---|---|---|
| `python3 scripts/check-templates.py` | **1** | **expected.** 21 templates checked; `✘ 1 template(s) do not conform`; **exactly one** finding line, `BUG.md — frontmatter missing: module`. Re-confirmed by reading the full output, not by trusting the rework's claim — **nothing is hiding behind it** |
| `python3 scripts/check-decisions.py` | 0 | 29 decisions conform |
| `python3 scripts/check-envelopes.py` | 0 | 10 envelopes conform |
| `python3 scripts/check-step-refs.py` | 0 | 42 step references resolve — including `:930`'s new `§5.1.1`/`§7.3` citations |
| `python3 scripts/test-check-envelopes.py` | 0 | 25 obligation cases |
| `python3 scripts/test-check-step-refs.py` | 0 | 28 cases |
| `python3 scripts/test-check-templates.py` | **1** | 3 of 15 — `clean tree exits 0`, `AC-1 no-headings row…`, `AC-2 the decision row is reported as checked`. All three quote `BUG.md frontmatter missing: module` verbatim; **same window, self-closing**, now recorded as tech debt against TASK-040 |

Both reds are the expected ones and the same one. `check-templates.py`'s single finding closes when
TASK-040 adds `module` to `templates/BUG.md`; the three `test-check-templates.py` cases close with it.

## Criteria Coverage

| criterion | covered by | result |
|---|---|---|
| AC-1 | **Spot check, not re-derived** — `git diff fac06bf..HEAD` touches only `REQUIREMENTS.md` and `IMPLEMENTATION.md`, and within `REQUIREMENTS.md` only `:930-936`. `:584` re-read verbatim: `` \| `BUG.md` \| `bugfix` intake \| `module` `bug` `severity` \| … ``. `check-templates.py` still parses the cell and reports `module` as the delta, so the row remains **machine-readable**, not merely present. Passed firmly in round 1; unchanged and re-observed. | **pass** |
| AC-2 | **Spot check** — `D-029-a-bug-carries-its-module.md` last touched at `74f788c` (design), untouched this round; `check-decisions.py` exits 0 and counts it among 29 conforming, so all four required fields are present. Its `**Constrains:**` still carries four forward obligations rather than a restatement of the Why. Passed firmly in round 1; unchanged and re-observed. | **pass** |
| AC-3 | **Resolved, and it resolves rather than relocates.** `:930` now reads "`MODULE` is the **scope unit's** `module:` — the task's under `TASK:`, the bug's under `BUG:`", and adds the clause the contradiction actually needed: "**read from the unit's frontmatter, never derived by the dispatching agent** — a `BUG` dispatch is composed before promote, so there is no task to read from, and `step-diagnose` takes `BUG-NNN/BUG.md`'s own `module:` (§7.3, D-029)". Checked pairwise: `:957`'s "those units carry `module:` in their frontmatter" now has a stated source for **both** units it obliges; `§7.3:1213` ("module carried from BUG-NNN's frontmatter") is the same mechanism named from the promote side; `D-029`'s third constraint ("read the module from the BUG's frontmatter and never re-derive it from the symptom") is now backed by a spec sentence rather than by a decision file alone; `§7.3.1`'s "routing comes from where the fix lands" stays consistent because D-029 amends the frontmatter and recomposes rather than composing a disagreeing `MODULE:`. **It generalises rather than special-cases** — no `BUG`-only exception was bolted on, so the next scope unit inherits the rule (D-027, and D-029's fourth constraint). **The sentence kept its point**, checked against the diff rather than the result. The bold lead is **verbatim unchanged**: "**`MODULE` and `PATHS` carry the row the routing came from.**" `PATHS` is still "a boundary rather than a hint", `review-task` still flags an outside file as `major` (§5.2, §7.8.1, D2), and both still "travel in the envelope because that check has to be mechanical". The added "never derived by the dispatching agent" **strengthens** the anti-judgement point the criterion is protecting rather than trading it away for accuracy. | **pass** |
| AC-4 | **Sweep (iii) above, on surfaces neither earlier sweep could reach — nil result, recorded as a search.** §5's opening example (`:707`, `TASK-007, module: api`) and the §5.5 envelope example (`:877`, `MODULE: api`) are `TASK`-scoped illustrations that assert no source, so neither is falsified by a `BUG` carrying the key. §7.3's narrative and §7.3.1 name the frontmatter explicitly. §5.5.1 enumerates what the orchestrator reads on **return** (`status`, `verdict`, `result`, `deviation`) — a different direction from envelope composition, and its "frontmatter only, never the body" rule **corroborates** resolution (a): sourcing the module from `## Scope` prose is what would have contradicted it. `:1466`'s step I/O table has `diagnose` reading `BUG.md`, which is now exactly where the key lives. `:1389` ("routed by the task's module") is `pr-comments`, genuinely task-scoped. `:1413` ("Assigns exactly one `module`") is `create-tasks`, and promote reaches it carrying the bug's value (§7.3:1213). `:403`'s tree comment ("report, repro, scope") names sections. §9's Worked example contains **no bugfix run at all**, so it asserts nothing here. Set-difference re-run on both axes: §4.8.1 vs `templates/` gives exactly one delta, the deliberate one; scope units `{TASK, PHASE, BUG, PROJECT}` vs module-source clauses now gives **zero** gaps — `TASK` and `BUG` both sourced at `:930`, `PHASE`/`PROJECT` both excluded at `:957` (D-027). `:739`'s "Every **task** carries `module:`" remains a baseline over tasks, not an enumeration of carriers, and `:930` now generalises above it. `README.md` is in this module's `paths` and does not exist; AC-4 scopes itself to `REQUIREMENTS.md`, so this contributes nothing to the sweep and nothing to a gap. | **pass** |

## Issues

_none_ — no defect against any acceptance criterion. Two observations, neither a finding:

**Observation 1 — pre-existing and unrelated: §5:717 names the wrong file as the routing table.**
`:717` says the orchestrator "reads the routing table in `config.md`", while `:209`, `:727` and `:930`
all make `.orqestra/modules.md` the registry the row comes from. Reported rather than edited because it
fails no criterion here: `git log -L 717,717` puts it in `a660327`, the initial workspace commit, so it
predates this task's claim and is untouched by it — the wrong version AC-4 hunts is "a bug does not carry
`module:`", not "the registry lives in `config.md`". It is one clause inside `docs`'s `paths` and worth a
task of its own; it is **not** grounds to fail this one.

**Observation 2 — the expected red is wider than the one command anyone runs.**
`scripts/test-check-templates.py` also exits 1 (3 of 15), for the same missing `module` key and closing
with it. The rework now records this under Tech Debt against TASK-040, which is the right disposition —
noted here only so the window is described completely, since the file is in no `test_command` and would
otherwise be discovered by whoever next runs it cold.

**Confirmed rather than assumed:** `check-templates.py`'s red is **exactly one** finding with nothing
behind it (round 1 caught a second red hiding; this round there is none); `check-decisions.py`,
`check-envelopes.py`, `check-step-refs.py` and both remaining test files are green when run **directly**,
which is the only way they run at all while the templates check is red.
