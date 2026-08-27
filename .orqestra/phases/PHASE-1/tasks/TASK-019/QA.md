---
id: TASK-019
type: qa
status: done
updated: 2026-08-27
task: PHASE-1/TASK-019
result: failed
test_command: python3 scripts/test-check-envelopes.py && python3 scripts/check-decisions.py && python3 scripts/check-templates.py && python3 scripts/check-envelopes.py
---

## Test Strategy

Round 2, after rework and the §8.2 amendment. Nothing from round 1 was carried forward on
trust: the branch moved four commits, and every criterion below was re-run against the tree
at `e05fca9`.

**On the amendment — judged, not accepted.** The rescope is honest. Four tests:

1. **The blockers are structural, not effort.** Verified, not read: no `agents/*.md` `tools:`
   line contains `Agent` or `Task`, so no dispatched agent can dispatch AC-1's probe subject;
   and `check-envelopes.py`'s two findings are `skills/diagnose/` not existing and §5.5's
   always-class having no value a project-wide dispatch can supply. Neither is reachable from
   `plugin` without crossing D14 or inverting D-019.
2. **The criteria were carried, not softened.** TASK-031/AC-2 requires *both* directions of the
   probe and output that **honours** the convention — strictly stronger than the removed AC-1,
   which round 1 had already found could be satisfied by quoting. TASK-030/AC-1 requires
   `check-envelopes.py` to exit 0 "with nothing invented", and its `## Out of Scope` forbids
   fabricating a value to green the check. A laundering rescope weakens the criterion; this one
   sharpened both.
3. **The dependencies are real.** `TASK-030` carries `depends_on: [TASK-024, TASK-029]` — the
   two blockers named. The work cannot be quietly skipped; it is ordered behind its causes.
4. **The process gap was filed against itself.** TASK-032 exists because `step-qa.md` had no
   route for this failure and would have burned three attempts then blocked with
   `max-attempts` — the wrong cause. Its `## Out of Scope` explicitly refuses the softer
   grade: "the fix is a route for the failure, not a softer grade." A dishonest split would
   have taken that exit.

All four re-filed tasks exist on disk with full criteria and are registered in `TASKS.md`.

**Method for the four remaining criteria.** This dispatch is again the experiment for AC-2 and
AC-4: I am a subagent running the branch's `agents/qa-engineer.md` and I invoked `Skill` three
times (`orqestra:qa`, `claude-expert`, `orqestra-conventions`). On `master` that `tools:` line
is `Read, Write, Edit, Glob, Grep` — under D-024 a true allowlist for the whole run, so the
invocations could not have happened there. AC-3 and AC-6 are absence criteria, checked by grep
across all eight personas. AC-4's second half is checked by a new script, below.

**Test added: `scripts/check-decisions.py`** (new, stdlib only). `check-templates.py` cannot
see this class of defect — a decision file's schema lives in **bold field lines**, not `##`
headings, so its heading check passes a decision missing every one of them. The new check
derives the required fields from `templates/DECISION.md` itself and asserts every `D-NNN`
carries them, plus index row/`count`/`next_id` agreement. Proven in both directions: it reports
exactly one finding against the repo (positive control: 24 of 25 conform), and deleting a
`**Why:**` line from a conformant fixture is caught (negative control).

## Results

| command | outcome |
|---|---|
| `python3 scripts/test-check-envelopes.py` | 19 obligation cases, 19 pass, **exit 0** |
| `python3 scripts/check-decisions.py` | 25 decisions, **1 finding, exit 1** — new, added by this step |
| `python3 scripts/check-templates.py` | 20 templates conform, **exit 0** |
| `python3 scripts/check-envelopes.py` | 10 envelopes, 2 non-conformant, exit 1 — **both now TASK-030**, out of scope here |
| live dispatch | `Skill` invoked 3×, all succeeded; `${CLAUDE_PLUGIN_ROOT}` expanded on invocation |

The rework commit `6631d38` regressed nothing: it touches three files, two of them two-line
moves in `## Return` blocks, and `check-templates.py` and `test-check-envelopes.py` are both
still green.

Tests added: 1 file (`scripts/check-decisions.py`). No implementation file was modified.

## Criteria Coverage

| criterion | covered by | result |
|---|---|---|
| AC-2 — a dispatched agent receives the step procedure rather than relying on its persona duplicating it | This dispatch. `criterion-unsatisfiable`, `no-reproduction`, `SCHEMA:` and `## Criteria Coverage` each occur once in `skills/qa/SKILL.md` and **zero times** in `agents/qa-engineer.md`; this artifact carries all four. The procedure reached me and was followed | **verified** |
| AC-3 — no persona instructs an action its `tools:` allowlist forbids, across all eight | All eight re-scanned against their own `tools:` line. `analyst`/`architect` hold neither `Edit` nor `Bash` and instruct neither; `analyst.md:12` and `reviewer.md:26` name their lack of `Edit` as structural. The former unexecutable expertise-load bullet is gone from all eight, replaced by an `Invoke \`SKILL\` first` block whose only tool is `Skill`, which all eight now hold | **verified** |
| AC-4 — all eight hold `Skill` in `tools:`, **and** the choice is recorded as a `D-NNN` so the next agent added inherits the reason | Grant half: all eight `tools:` lines begin `Skill, …`; `Skill` demonstrably worked in this run and provably would not have on `master`. **Record half: `scripts/check-decisions.py` — D-025 is the only one of 25 decisions missing `**Constrains:**`** | **failed** — see I-1 |
| AC-6 — no persona instructs the agent to read a step skill as a file | `grep -rn CLAUDE_PLUGIN_ROOT agents/` → 0 hits; `grep -rniE 'read .*skill\|skills/[a-z-]+/' agents/` → 0 hits. All eight instead carry *"skill names, not paths, and `Read` does not work on them"*. The premise is behaviourally confirmed: the invocation returned the template path expanded, a `Read` of `skills/qa/SKILL.md` returns the literal token | **verified** |

Removed by the 2026-08-27 §8.2 amendment and re-filed, not graded here: **AC-1 → TASK-031**,
**AC-5 → TASK-030**. Round 1's findings I-1 and I-2 stand as the reasons those tasks exist.

## Issues

**I-1 · AC-4 · `D-025` omits `**Constrains:**`, the one field AC-4's own reasoning asks for.**
Observed: `python3 scripts/check-decisions.py` → `D-025-agents-invoke-their-skills.md: missing
**Constrains:**`, alone among 25 decisions. Expected: the field present, as
`templates/DECISION.md` requires of every decision and as D-001 through D-024 all carry.

This is not pedantry about a heading. AC-4 reads *"recorded as a `D-NNN` — the durable
allowlist changed, so **the next agent added inherits the reason, not just the line**"*, and
`templates/DECISION.md` defines `**Constrains:**` as *"what a FUTURE task must now do… the
field that earns this file. If you cannot write this line, the decision is a note, not a
decision."* AC-4's stated purpose and the missing field are the same sentence. D-025 has the
substance — every agent holds `Skill`, every step skill's `RETURN` opens with `SKILLS:` — but
a fresh agent adding the ninth persona reads the index row and the field lines, not 50 lines of
rationale, and the field it would read is absent.

Round 1 graded this half "verified", hedging it as *"`**Constrains:**`-grade content"*. That
hedge was the miss: the content is Constrains-grade, the line is not there. Recorded so the
error is visible rather than quietly corrected.

**Owner: implement.** In scope and fixable here — implement already writes `D-025` under AC-4's
mandate and recorded doing so as a deliberate minor deviation. This is one line, not a rework
spiral, and does not need TASK-032's escape route: it is an ordinary defect that implement can
satisfy.

**I-2 · minor · `skills/design/SKILL.md`'s `## Return` block is misaligned.** Observed:
`SKILLS:` is padded to 3 spaces, `STATUS:`/`OUTCOME:` to 5 — the only one of the nine dispatch
skills whose return block does not align on a single column. Introduced by `6631d38`'s sibling
edits leaving this file's pre-existing padding untouched. No behavioural effect; the
orchestrator parses the block, not the columns. Noted, not a gate.

**I-3 · observation, unchanged from round 1, owned by `docs` · the envelope's expansion premise
still did not hold for this dispatch.** §5.5 states the orchestrator composes the envelope from
inside an invoked skill *"so the value is already expanded by the time an agent reads it"*. My
`TEMPLATE:` line again carried the literal `${CLAUDE_PLUGIN_ROOT}` token. No harm — the
`orqestra:qa` invocation supplied the expanded path, which is exactly the redundancy D-025
bought — but §5.5 states as a guarantee something that behaves as a convention. Reproduced
twice now, in two separate dispatches.
