---
id: TASK-019
type: qa
status: done
updated: 2026-08-29
task: PHASE-1/TASK-019
result: passed
test_command: python3 scripts/check-decisions.py && python3 scripts/check-templates.py && python3 scripts/test-check-envelopes.py && python3 scripts/check-envelopes.py
---

## Test Strategy

Round 3, after the rework commit `7a9febd`. Nothing from rounds 1 or 2 was carried forward on
trust — all four remaining criteria were re-run against the tree at `7a9febd`.

**Scope of the rework, confirmed first.** `git show --stat 7a9febd` touches exactly two files:
`.orqestra/decisions/D-025-agents-invoke-their-skills.md` (+14) and this task's
`IMPLEMENTATION.md` (+15/−2). Nothing under `agents/`, `skills/`, `templates/` or `scripts/`
moved, so the round-2 verifications of AC-2, AC-3 and AC-6 could not have been silently
invalidated — but each was re-run anyway rather than inferred from the diff.

**AC-2 and AC-4's grant half are again tested by this dispatch itself.** I am a subagent running
the branch's `agents/qa-engineer.md`, and I invoked `Skill` three times — `orqestra:qa`,
`claude-expert`, `orqestra-conventions` — all three returning their bodies. On `master` that
`tools:` line is `Read, Write, Edit, Glob, Grep`; under D-024 it is a true allowlist for the whole
subagent run, so those three invocations are behaviour that could not have occurred before this
task. AC-3 and AC-6 are absence criteria, checked by grep across all eight personas.

**AC-4's record half — judged on substance, not presence.** `check-decisions.py` only proves the
field exists. The criterion asks that the next agent added inherits *the reason*, so each of the
four appended constraints was read against that bar: is it a forward obligation on future work
with the failure it prevents, or a restatement of the decision above it?

| constraint | forward obligation | failure it names | verdict |
|---|---|---|---|
| names in `SKILL`/`EXPERTISE`, never paths, never via `READ` | yes — binds every future envelope | a step skill opened as a file arrives with every `TEMPLATE:` line a literal token | rule |
| every new `agents/*.md` holds `Skill` | yes — binds the ninth persona, the exact case AC-4 names | "silently reinstates the original defect — the artifacts still look fine" | rule |
| the grant is not evidence of a load; `SKILLS:` stays the **first** `## Return` line | yes — binds every future dispatch skill | cites §7.0.1 and D-024; names the detection layer | rule |
| the expertise list lives in the `modules.md` row and nowhere else | yes — forbids hardcoding into a persona or step skill | "makes expertise plugin-owned and static — the opposite of what the row buys" | rule |

None is a summary of the `**Why:**` above it: each states an action a future task must or must
not take, and each names the specific silent failure that follows from taking the other branch.
The second constraint in particular is AC-4's own sentence turned into an obligation. The field
carries the reason, not the line.

**The checker's green is not vacuous.** Negative control re-run on the current file: deleting the
`**Constrains:**` line from `D-025` makes `check-decisions.py` report exactly that finding and
exit 1; restoring it returns exit 0 with a clean `git diff`. The pass is therefore evidence, not
an artefact of a check that cannot fail.

## Results

| command | outcome |
|---|---|
| `python3 scripts/check-decisions.py` | 25 decisions, **0 findings, exit 0** — was 1 finding in round 2 |
| `python3 scripts/check-decisions.py` (negative control, `**Constrains:**` removed) | 1 finding, exit 1 — the check can fail |
| `python3 scripts/check-templates.py` | 20 templates conform, exit 0 |
| `python3 scripts/test-check-envelopes.py` | 19 obligation cases, 19 pass, exit 0 |
| `python3 scripts/check-envelopes.py` | 10 envelopes, 2 non-conformant, exit 1 — both **TASK-030**, out of scope here |
| live dispatch | `Skill` invoked 3×, all succeeded |

Tests added this round: none. `scripts/check-decisions.py`, added in round 2, is the test that
covers AC-4's record half and it now passes for the first time. No implementation file was
modified by this step. Working tree carries no modifications — only two untracked audit files
that predate this branch.

## Criteria Coverage

| criterion | covered by | result |
|---|---|---|
| AC-2 — a dispatched agent receives the step procedure rather than relying on its persona duplicating it | This dispatch. `criterion-unsatisfiable`, `no-reproduction` and `contradictory-input` each occur once in `skills/qa/SKILL.md` and **zero times** in `agents/qa-engineer.md`; this artifact's coverage map, template and return contract all come from the skill. The procedure reached me and was followed | **verified** |
| AC-3 — no persona instructs an action its `tools:` allowlist forbids, across all eight | All eight re-scanned against their own `tools:` line at `7a9febd`. `analyst`/`architect` hold neither `Edit` nor `Bash` and instruct neither — `analyst.md:12` and `reviewer.md:26` name their lack of `Edit` as structural rather than as restraint. The former unexecutable expertise-load bullet is gone from all eight, replaced by an identical `Invoke \`SKILL\` first` block (present in 8 of 8) whose only tool is `Skill`, which all eight now hold | **verified** |
| AC-4 — all eight hold `Skill` in `tools:`, **and** the choice is recorded as a `D-NNN` so the next agent added inherits the reason | Grant half: all eight `tools:` lines begin `Skill, …`, and `Skill` demonstrably worked in this run where it provably could not on `master`. Record half: `D-025` now carries `**Constrains:**` with four rules, judged above as forward obligations each naming its failure — not restatements; `check-decisions.py` 25/25 exit 0, with a negative control proving the check bites | **verified** |
| AC-6 — no persona instructs the agent to read a step skill as a file | `grep -rn CLAUDE_PLUGIN_ROOT agents/` → 0 hits; `grep -rniE 'read .*skill|skills/[a-z-]+/' agents/` → 0 hits. All eight instead carry *"skill names, not paths, and `Read` does not work on them"*. Behaviourally confirmed again this run: the `orqestra:qa` invocation returned its template path expanded, while the `TEMPLATE:` line in my envelope carried the literal token | **verified** |

Removed by the 2026-08-27 §8.2 amendment and re-filed, not graded here: **AC-1 → TASK-031**,
**AC-5 → TASK-030**.

## Issues

**I-1 · minor, unchanged from round 2, not a gate · `skills/design/SKILL.md`'s `## Return` block
is misaligned.** Observed: `SKILLS:` padded to 3 spaces, the eight lines below it to 5, making it
the only one of the nine dispatch skills whose return block does not align on a single column.
Expected: one column, as the other eight have. No behavioural effect — the orchestrator parses
the block, not the columns — and no criterion depends on it. Left for whoever next touches that
file.

**I-2 · observation, unchanged, owned by `docs` · the envelope's expansion premise still does not
hold for this dispatch.** §5.5 states the orchestrator composes the envelope from inside an
invoked skill *"so the value is already expanded by the time an agent reads it"*. My `TEMPLATE:`
line again carried the literal `${CLAUDE_PLUGIN_ROOT}` token. No harm — the `orqestra:qa`
invocation supplied the expanded path, which is precisely the redundancy D-025 bought — but §5.5
states as a guarantee something that behaves as a convention. Reproduced three times now, in
three separate dispatches. Not a TASK-019 criterion; §5.5 is the `docs` module (D-019).
