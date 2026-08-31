---
id: TASK-034
type: qa
status: done
updated: 2026-08-31
task: TASK-034
result: passed
test_command: python3 scripts/check-templates.py && python3 scripts/test-check-envelopes.py && python3 scripts/check-envelopes.py
---

## Test Strategy

The `plugin` module has no test runner (§7.0). Verification is the two dev checkers plus behavioural
inspection of what a fresh agent actually receives — the module's own convention: "install the plugin,
run the command, inspect the artifacts against their schemas".

AC-3 is the weakest criterion in this task and was treated as such. `check-envelopes.py` goes green on
the `SKILL:` line alone, whatever the named file contains, because under D-025 the value is **invoked,
not inspected**. Exit 0 therefore proves the envelope conforms and proves nothing about the skill. So
**AC-1 was verified independently of AC-3**, by five checks a checker cannot make, and one behavioural
test nothing else in this pipeline has run:

- **Live load.** `orqestra:diagnose` is a registered skill in this session and was **invoked**. It
  returned its full body, resolved `${CLAUDE_PLUGIN_ROOT}` to
  `.claude/skills/orqestra/templates/DIAGNOSIS.md`, and left the prose reference
  `skills/bugfix/step-diagnose.md` plugin-relative and readable. This is AC-1 and AC-3 joined: the
  harness loads what the envelope names, and what it loads is a procedure.
- **Bash-freedom, re-tested with independent terms.** The orchestrator's earlier sweep anchored on the
  word `Bash`. This sweep did not: a 40-alternative pattern over execution verbs and their euphemisms
  (`re-run`, `execute`, `blame`, `bisect`, `instrument`, `breakpoint`, `benchmark`, `observe`,
  `step through`, `confirm it still fails`, `try it`, fenced `bash`/`sh` blocks, `$(`) hit **only** the
  two lines that state the prohibition. Every procedure step is a reading step: step 2 uses Grep, step 4
  "check it in the code", step 10 verifies against a schema.
- **Substitution test.** `TASK.md`, `acceptance criteri*`, `AC-`, `depends_on`: all absent. The skill was
  not assembled by analogy with `plan`.
- **Invariance test (TASK-037).** Three `module` mentions, all consumption: the `modules.md` input row,
  the §5.5 sentence saying the envelope supplies it, and rule 5's boundary. Nothing states where a bug's
  module comes from. If TASK-037 adds `module:` to `BUG.md`, no line here changes.
- **House shape.** Frontmatter is §7.0:1081's `step` row character-for-character
  (`Read, Write, Glob, Grep` / `Agent, Edit, NotebookEdit, Bash`); section order is the house one; 138
  lines, under the ~150 sharding threshold. `agents/analyst.md` grants `Skill, Read, Write, Glob, Grep`
  — the tool-set guarantee is real at the durable layer (D-024), not just declared.

## Results

| command | exit | output |
|---|---|---|
| `python3 scripts/check-envelopes.py` | **0** | `checked 10 dispatch envelopes against §5.5 · all envelopes conform` |
| `python3 scripts/check-step-refs.py` | **0** | `checked 41 step references against D-026 · every reference resolves` |
| `python3 scripts/check-step-refs.py --verbose` | 0 | lists `skills/diagnose/SKILL.md:57 → skills/bugfix/step-diagnose.md` ✔ — the new file's one reference exists and resolves |
| `Skill(orqestra:diagnose)` | loaded | full body returned; `${CLAUDE_PLUGIN_ROOT}` resolved, prose reference left literal |

No test files were added: this module has no runner, and the checkers are the acceptance instrument —
`scripts/` was deliberately not touched, since changing a checker to make a criterion pass inverts the
test.

## Criteria Coverage

| criterion | covered by | result |
|---|---|---|
| AC-1 | **Not** the checkers — deliberately. Live invocation of `orqestra:diagnose` returned a body with all six house sections, a 10-step falsification procedure, an outcome contract, a 9-line return, a blocked table and 6 rules. Plus the substitution, Bash-freedom, invariance and altitude checks above. 138 lines vs `plan`'s 86 | passed |
| AC-2 | First line inside the `## Return` fence is `SKILLS:` (`skills/diagnose/SKILL.md:94`). Cross-checked against the gate block at `skills/bugfix/step-diagnose.md:39-45`: all four rendered labels — `ROOT CAUSE`, `EVIDENCE`, `DIRECTION`, `RISK` — have a return line, name-for-name, plus `ROOT_CAUSE_FOUND` mirroring the frontmatter key. An orchestrator reading frontmatter only (§5.5.1) can render and gate without interpreting prose | passed |
| AC-3 | `check-envelopes.py` exit **0** over 10 envelopes. Placement verified by reading, not by exit code: `SKILL: orqestra:diagnose` sits at line 10, between `STEP:` and `BUG:`, per §5.5's scope-field rule. Diff is exactly +1 line — nothing else in that envelope changed | passed |
| AC-4 | `check-step-refs.py` exit **0** (41 references). The new file's single cross-skill reference is in prose, backticked, plugin-relative, no `${CLAUDE_PLUGIN_ROOT}` — D-026's shape for a prose citation; the template path in `## Output` correctly *does* carry the variable, being a `Read` argument. Confirmed live: both resolved as intended when the skill loaded | passed |
| AC-5 | Dispatch set derived independently, not trusted: `grep -rn -A1 '^ROLE: *orqestra:analyst' skills/` yields five and only five — `create-phases` (`greenfield/step-phases.md`), `create-phase` (`add-phase/step-define-phase.md`), `create-tasks` (`greenfield/step-tasks.md`), `plan` (`greenfield/step-plan-design.md`), `diagnose` (`bugfix/step-diagnose.md`). The new description names exactly that set, and no longer names `PLAN.md` as *the* artifact | passed |

**The design's central contract, verified against the file rather than IMPLEMENTATION.md's claim.**
`root_cause_found: false` is a **`done`** outcome: row two of the outcome contract
(`skills/diagnose/SKILL.md:81`) reads `done` / `false` / `done` / **yes**, bolded, with the reason stated
beside it at :85 — the gate's `[ Investigate further ]` branch is reachable only from an artifact that
reaches the gate. Procedure step 6 says the same in the place the mistake would be made. Both
`blocked_reason` values — `no-reproduction`, `contradictory-input` — are in §4.4.3's closed list, and
the skill says explicitly not to reach for a task-shaped reason. Nothing invented.

## Issues

No criterion fails. One inconsistency the new file **surfaces without causing**, recorded so it is a
decision rather than an oversight:

- **`skills/bugfix/SKILL.md:103` contradicts the outcome contract it is cited as the bar for.** It reads
  "Never diagnose past the first plausible cause. Evidence, **or block**." The new skill's rule 1 reads
  "Evidence, or `root_cause_found: false`" — and its outcome contract makes no-cause-found a `done`
  outcome that reaches the gate. `skills/bugfix/step-diagnose.md:31` agrees with the new skill
  ("`root_cause_found: false` is an honest and useful outcome"), so `bugfix/SKILL.md` is the lone
  outlier and predates this task. It matters because `skills/diagnose/SKILL.md:57` cites that rule as
  the bar it meets, importing a disagreement about the one disposition this task exists to get right.
  Observed: rule 3 says an unproven cause is a block. Expected: it is `root_cause_found: false`, `status:
  done`, and it reaches the gate. Out of this task's criteria and its stated scope — a one-word fix for
  a follow-up, alongside the `agents/architect.md` description already noted in TASK.md's amendment.
