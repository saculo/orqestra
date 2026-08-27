---
id: TASK-019
type: qa
status: done
updated: 2026-08-27
task: PHASE-1/TASK-019
result: failed
test_command: python3 scripts/check-envelopes.py && python3 scripts/test-check-envelopes.py && python3 scripts/check-templates.py
---

## Test Strategy

This module has no test framework; scripts are the checks and criteria are behavioural
(`PROJECT.md` `## Testing`). Three sources of evidence were used, in descending strength:

**1. This dispatch is itself the experiment.** AC-1, AC-2 and AC-4 are claims about what a
dispatched agent receives, and I am a dispatched agent running against the branch under test —
`.claude/skills/orqestra/agents` is a symlink to the working tree's `agents/`, so the definition
loaded is the one this diff changed. Three facts make that decisive rather than assumed:

- My system prompt contains, verbatim, *"Invoke `SKILL` first, then every skill in `EXPERTISE`,
  before you do anything else"*. `git show master:agents/qa-engineer.md | grep -c Invoke` returns
  `0`. The persona I received exists only on this branch.
- On `master` and on `feat/TASK-015`, `agents/qa-engineer.md` reads
  `tools: Read, Write, Edit, Glob, Grep, Bash` — no `Skill`. I invoked `Skill` three times
  successfully (`orqestra:qa`, `claude-expert`, `orqestra-conventions`). Under D-024 the `tools:`
  list is a true allowlist for the whole subagent run, so this could not have happened on either
  other branch.
- `skills/qa/SKILL.md:36` reads ``${CLAUDE_PLUGIN_ROOT}/templates/QA.md``. The invocation returned
  it already expanded, to `/home/lgrula/Projects/orqestra/.claude/skills/orqestra/templates/QA.md`.
  A `Read` of that file returns the literal token. This is direct behavioural confirmation of the
  premise D-025 and §5.5 rest on — invoke expands, read does not — verified rather than argued.

**2. A new behavioural test of the envelope checker**, `scripts/test-check-envelopes.py` (added by
this step, 19 cases, stdlib only). Running `check-envelopes.py` over the repo proves only what
today's ten envelopes happen to be; it does not prove the checker would *notice* a violation not
currently present, which is the only thing a conformance check is for. The new test drives
`check()` directly over every §5.5 obligation class in both directions — always, scope
(exactly-one), conditional (all-or-nothing), step-specific (`LENSES`/`ROUND` required on `review`
and permitted on no other), the closed list, and duplicates. All 19 pass, so the checker is a
faithful encoding of §5.5 and its two findings against the repo can be trusted.

**3. Static checks across all eight personas** for AC-3 and AC-6, where the criterion is itself an
absence.

## Results

| command | outcome |
|---|---|
| `python3 scripts/test-check-envelopes.py` | 19 obligation cases, 19 pass, **exit 0** — new, added by this step |
| `python3 scripts/check-envelopes.py` | 10 envelopes, **2 non-conformant, exit 1** |
| `python3 scripts/check-templates.py` | 20 templates, all conform, exit 0 |
| live dispatch | `Skill` invoked 3×, all succeeded; plugin-root token expanded on invocation |

`check-envelopes.py` reproduces `IMPLEMENTATION.md`'s reported failures exactly:

```
skills/bugfix/step-diagnose.md:8   [diagnose]        missing SKILL — always class
skills/greenfield/step-phases.md:13 [create-phases]  0 scope fields; exactly one of TASK/PHASE/BUG required
```

Tests added: 1 file, 19 cases. No implementation file was modified.

## Criteria Coverage

| criterion | covered by | result |
|---|---|---|
| AC-1 — dispatched agent demonstrably receives expertise content, via a probe planted **only** in an expertise skill whose output **honours** it | This dispatch: `claude-expert` and `orqestra-conventions` both invoked; the string *"stopped listing required headings"* appears in exactly one file in the repo (`.claude/skills/orqestra-conventions/SKILL.md`), which I never opened, yet received. Honoured, not merely quoted: `claude-expert`'s two-layer rule (`allowed-tools` pre-approves, `agents/` `tools:` binds) is what made the branch-vs-master `tools:` comparison above a valid experiment | **not verified as written** — see I-1 |
| AC-2 — receives the step procedure rather than relying on the persona duplicating it | `criterion-unsatisfiable`, `no-reproduction`, `SCHEMA:`, `CRITERIA:` and `## Criteria Coverage` each occur in `skills/qa/SKILL.md` and **zero times** in `agents/qa-engineer.md`. This artifact carries all five. The procedure reached me and was followed | **verified** |
| AC-3 — no persona instructs an action its `tools:` allowlist forbids, across all eight | All eight scanned against their own `tools:` line. `analyst` and `architect` hold neither `Edit` nor `Bash` and instruct neither; `analyst.md:12` states *"you hold no `Edit`"*; `reviewer.md:26` names its lack of `Edit` as structural. The formerly unexecutable expertise-load bullet is gone from all eight | **verified** |
| AC-4 — all eight hold `Skill` in `tools:`, and the choice is recorded as a `D-NNN` | Grant: all eight `tools:` lines begin `Skill, …`. Behaviour: `Skill` worked in this run and provably would not have on `master`. Decision: `D-025` exists with `**Constrains:**`-grade content and its `INDEX.md` row; index frontmatter `count: 25` matches 25 table rows | **verified** |
| AC-5 — every envelope in `skills/` carries the fields §5.5 declares mandatory | `check-envelopes.py`, itself validated by the 19-case test. 8 of 10 conform; 2 do not | **failed** — see I-2 |
| AC-6 — no persona instructs reading a step skill as a file | `grep -rn CLAUDE_PLUGIN_ROOT agents/` → none. `grep -rniE 'read (the )?(step \|expertise )?skill\|skills/.*\.md' agents/` → none. All eight instead carry *"skill names, not paths, and `Read` does not work on them"*. The premise is behaviourally confirmed by the expansion evidence above | **verified** |

## Issues

**I-1 · AC-1 · the specified probe was not run, and cannot be run by this pipeline step.**
Observed: no convention was planted in an expertise skill and no fresh agent was dispatched to
check the output honours it. Expected: exactly that. Two structural obstacles, neither the
engineer's to remove — the expertise skills live in `.claude/skills/`, outside the `plugin`
module's `PATHS` (D14), and no agent in `agents/` holds the subagent tool (`Agent`; `Task` is its
former name and grants nothing, per `PROJECT.md`), so neither implement nor qa can dispatch a
probe. Rework to implement will not fix this. What *was* proved is receipt of expertise content
unique to an expertise skill, on a live dispatch — stronger than the earlier quote-only probe
`IMPLEMENTATION.md` records, weaker than the criterion. **A human must either accept this
evidence as satisfying AC-1's intent, or move the probe to the eval harness (PHASE-1 SC-5), which
is the layer that can dispatch.** Grading it "met in substance" without that ruling would be qa
grading its own coverage, which D-023 exists to prevent.

**I-2 · AC-5 · two of ten envelopes are non-conformant; `check-envelopes.py` exits 1.**
Observed: `skills/bugfix/step-diagnose.md:8` has no `SKILL` (always class); `skills/greenfield/step-phases.md:13`
has no scope field (always class). Expected: all ten conform. `IMPLEMENTATION.md` grades both as
owned elsewhere and I concur on ownership — `skills/diagnose/` does not exist (TASK-024), and
`create-phases` operates on the whole project so it genuinely has no scope unit, which is a gap in
§5.5's always class and therefore a `docs` change (D-019). **But ownership elsewhere does not make
AC-5 met.** The criterion is observably false today. It cannot be closed inside this module, so
this is a sequencing decision for a human, not a rework loop: either AC-5 narrows to the eight
envelopes this task can reach, or TASK-019 waits on TASK-024 and the §5.5 amendment.

**I-3 · AC-4 / D-025 · three artifacts disagree on where `SKILLS:` sits, and this one *is*
fixable here.** Observed: `skills/implement/SKILL.md` and `skills/review-phase/SKILL.md` put
`SKILLS:` on the **second** return line, after `STATUS:`; the other seven put it first. All eight
personas say *"Your first `RETURN` line names what you loaded"*, and D-025 says every step skill's
return *"opens with"* it. Expected: one of the three changes so they agree. `IMPLEMENTATION.md`
grades this `minor`/"cosmetic in effect" and the effect is indeed nil — the orchestrator reads the
block, not the ordinal. But both files are inside this module's `PATHS`, the fix is a two-line
move, and an instruction that contradicts the file it describes is exactly the silent-drift shape
D-025 was written to end. Correctly graded as minor; **not correctly left open.**

**I-4 · observation, not a defect of this diff · the envelope's expansion premise did not hold
for this dispatch.** §5.5 states the orchestrator composes the envelope from inside an invoked
skill, *"so the value is already expanded by the time an agent reads it"*. The `TEMPLATE:` line I
received carried the literal `${CLAUDE_PLUGIN_ROOT}` token, unexpanded. No harm resulted — the
`orqestra:qa` invocation supplied the expanded path, which is precisely the redundancy D-025
bought — but §5.5's claim is stated as a guarantee and behaved as a convention. Owned by `docs`;
recorded here because this run is the only place it is observable.
