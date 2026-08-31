---
id: TASK-037
type: qa
status: done
updated: 2026-08-31
task: TASK-037
result: failed
test_command: python3 scripts/check-templates.py && python3 scripts/test-check-envelopes.py && python3 scripts/check-envelopes.py
---

## Test Strategy

`docs` is `markdown`; the module's tests are `scripts/check-*.py`, which are `plugin` and outside this
module's `paths` (§5.2, D2) — so **no test files were added or edited**. Verification is (i) executing
every checker **directly**, because `config.md`'s `test_command` chains with `&&` and short-circuits at
the templates red, and (ii) a documented sweep of `REQUIREMENTS.md` with terms devised here rather than
reused from `IMPLEMENTATION.md`, since a check anchored on one surface form misses another.

Criteria were read from `TASK.md`'s HTML comment as amended by human decision (§8.2), resolution (a):
§5.5:957 and §5.1.1:795 become **true** and must not be softened, so "unchanged" was not accepted as
evidence — each was re-read against the new state and graded for accuracy.

**Sweep terms** (mine, deliberately different from the engineer's `carr* \`module:\``, which anchors on
one phrasing): `severity|BUG-NNN|BUG-001|bugfix intake|step-intake|if known|BUG\.md`; every `module`
line co-occurring with `bug|scope|derive|infer|touched|unknown|prose`; every
`carr(y|ies|ied)|frontmatter` line co-occurring with `module|scope unit|routing`; and
`task's \`module|from the task|routing key|look(s)? up`. **Set-difference**, two axes: §4.8.1's
frontmatter cells against `templates/*.md` (that *is* `check-templates.py`'s output), and the §5.5
scope-unit set `{TASK, PHASE, BUG, PROJECT}` against every clause that says where a `module` comes from.
The second axis is what produced Issue 1 — the engineer's grep could not reach §5.5:930, which says
"carry the row", never "carries `module:`".

## Results

Every command run directly from the repository root, at `9061ec5`.

| command | exit | outcome |
|---|---|---|
| `python3 scripts/check-templates.py` | **1** | **expected.** 21 templates checked; **exactly one** non-conforming template, **exactly one** finding line: `BUG.md — frontmatter missing: module`. No second finding behind it. |
| `python3 scripts/check-decisions.py` | 0 | 29 decisions conform. Was red before implement ("no row for D-029"); the INDEX row closed it. **Confirmed.** |
| `python3 scripts/check-envelopes.py` | 0 | 10 envelopes conform. Run **directly** — behind the `&&` it never executes. |
| `python3 scripts/test-check-envelopes.py` | 0 | 25 obligation cases |
| `python3 scripts/check-step-refs.py` | 0 | 42 step references resolve |
| `python3 scripts/test-check-step-refs.py` | 0 | 28 cases |
| `python3 scripts/test-check-templates.py` | **1** | 3 of 15 cases fail — **all three for the one expected reason** (see Issue 2). Not run by anyone before this step. |

The one red is the intended one and nothing is hiding inside it: every finding emitted by
`check-templates.py` names `BUG.md` and the missing key `module`, and the three `test-check-templates.py`
failures each quote that same output verbatim.

`README.md` is in this module's `paths` and **does not exist** in the repository. Any sweep over it is
vacuous — see AC-4's row: it does not weaken the coverage claim, because `REQUIREMENTS.md` is where
every asserted surface lives and AC-4 names `REQUIREMENTS.md` explicitly. It is worth one line in a
future task that `docs`'s `paths` names a file the repository has never had.

## Criteria Coverage

| criterion | covered by | result |
|---|---|---|
| AC-1 | `REQUIREMENTS.md:584` read directly: `` \| `BUG.md` \| `bugfix` intake \| `module` `bug` `severity` \| … ``. `check-templates.py` parses the cell and reports `module` as the delta against `templates/BUG.md`, which **proves the row is machine-readable**, not merely present. §5.5:957 and §5.1.1:795 re-read against the new state and confirmed **unedited in the diff** (`git diff master...HEAD -- REQUIREMENTS.md` touches only 584 and 1210-1211) **and now accurate**: "those units carry `module:` in their frontmatter" is true of `BUG` once §4.8.1 declares it; "a `BUG` carries `module:` too" is backed by a key rather than by convention. Neither was softened. | **pass** |
| AC-2 | `D-029-a-bug-carries-its-module.md` read in full; `check-decisions.py` exits 0 and counts it among 29 conforming, so all four required fields are present. `**Constrains:**` is **four forward obligations**, not a restatement of the Why: `templates/BUG.md` carries the key and `## Scope` stops carrying the module (TASK-040 AC-1, AC-3); intake may not create a bug without one nor fall back to prose, and blocks otherwise (TASK-040 AC-2); `step-diagnose.md`/`step-promote.md` **read** it and never re-derive, amending the frontmatter when diagnosis relocates the fix (TASK-040 AC-4); and a standing test for any future scope unit added to §5.5. Each is checkable against work not yet done — the field earns the file. | **pass** |
| AC-3 | Four surfaces read end to end as one workflow: §4.8.1:584 (amended), §5.5:957 (true unedited), §5.1.1:795 (true unedited), §7.3:1210 (promote now takes the module **carried from `BUG-NNN`'s frontmatter**) and §7.3.1:1221 (routing is *where the fix lands*, consistent — D-029 amends the frontmatter rather than composing a disagreeing `MODULE:`). The four named surfaces agree. **But §5.5 is not internally consistent with itself**: §5.5:930, twenty-seven lines above :957, is the only sentence defining where `MODULE`'s value comes from and names the task alone. See Issue 1. Graded against AC-3's own method clause — "read the workflow end to end rather than by grepping one phrase" — the end-to-end read is what surfaces it. | **fail** |
| AC-4 | Sweep terms above, plus both set-difference axes. Axis (i), §4.8.1 vs `templates/`: exactly one delta, the deliberate one. Axis (ii), scope units vs module-source clauses: `TASK` and `BUG` are both obliged by §5.5:957, only `TASK` has a stated source (§5.5:930) — **Issue 1**. Everything else checked clean: §5.1:739 ("Every **task** carries `module:`") is a baseline, not an exhaustive enumeration, and a bug carrying the key does not falsify it; §5.5:957's `PHASE`/`PROJECT` "must be omitted" clause is still correct (D-027) and `PHASE.md`'s catalogue row carries no `module`; §4.8.1's `## Scope` heading on `BUG.md` is the section, not the module's home, and TASK-040 AC-3 owns the prose; `REQUIREMENTS.md:404`'s tree comment ("report, repro, scope") describes sections and is neutral; "if known" has **zero** hits in `REQUIREMENTS.md` — it lives in `skills/bugfix/step-intake.md`, TASK-040's. `README.md` does not exist, so it contributes nothing to sweep, and nothing to the gap either. | **fail** |

## Issues

**Issue 1 — AC-4 (and AC-3): §5.5:930 states a source for `MODULE` that is wrong for one of the two
scope units §5.5:957 obliges it on.**

- **Criterion**: AC-4 — no other place in `REQUIREMENTS.md` contradicts the new state (graded per the
  amendment: resolution (a) made the warrant true, so the question is contradiction with the *new*
  state, not correction of an old error).
- **Observed**: `REQUIREMENTS.md:930` — *"**`MODULE` and `PATHS` carry the row the routing came from.**
  `MODULE` is the task's `module:` — the single key that resolved `ROLE`, `STACK`, `EXPERTISE`, and
  `PATHS` from one `modules.md` row"*. This is the **only** sentence in the specification that says
  where the envelope's `MODULE` value comes from, and it names the task exclusively. Twenty-seven lines
  later, §5.5:957 makes `MODULE` mandatory **iff the scope key is `TASK` or `BUG`**, and D-029's
  `**Constrains:**` requires `step-diagnose.md` to read the module **from `BUG-NNN/BUG.md`'s
  frontmatter**. A `BUG`-scoped dispatch is composed *before* promote, so there is no task to read:
  under :930 as written, a conformant `BUG` envelope's `MODULE` has no defined source.
- **Expected**: §5.5:930 names both units — `MODULE` is the scope unit's `module:`, the task's under
  `TASK:` and the bug's under `BUG:`, resolving the same `modules.md` row either way (§5.1, §5.1.1,
  D-004, D-029).
- **Why it is this task's**: `REQUIREMENTS.md:930` is in `docs`'s `paths`, and TASK-040's Out of Scope
  forbids it explicitly — *"`REQUIREMENTS.md` — TASK-037's, landed first (D-019). If this task finds the
  spec still wrong after it, that is a finding to report, not an edit to make."* No planned work will
  reach it. This is the task's own failure mode recurring one section over: an obligation whose warrant
  is stated in one place while the clause that would back it names only the narrower unit — which is
  precisely why the engineer's `carr* \`module:\`` sweep could not see it. :930 says "carry the row".
- **Cost**: one clause, one line, inside the module's `paths`.

**Issue 2 — observation, not a defect: the deliberate red also reds `scripts/test-check-templates.py`,
and that was not recorded.**

`python3 scripts/test-check-templates.py` exits **1**, with 3 of 15 cases failing — "clean tree exits 0",
"AC-1 no-headings row…", "AC-2 the decision row is reported as checked". All three assert against the
**real repository tree** and quote the same `BUG.md — frontmatter missing: module` output, so all three
are the same expected window and all three self-close the moment `templates/BUG.md` gains the key. It is
**not** a second failure hiding behind the familiar one. It is not in `config.md`'s `test_command`, so no
one ran it: `IMPLEMENTATION.md`'s verification table omits it, and TASK-040 AC-1 names only
`check-templates.py`. Worth a line on TASK-040 so the window is described completely — the exact hazard
`config.md`'s own stale comment already demonstrated (TASK-040 AC-5).

**Confirmed, not defects**: `check-decisions.py` exits 0 — the D-029 INDEX row closed the red the design
step could not. `check-templates.py`'s red is exactly one finding and is the intended one. `README.md`'s
non-existence does not weaken AC-4's coverage, because AC-4 scopes itself to `REQUIREMENTS.md`.
