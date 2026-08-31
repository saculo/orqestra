---
id: TASK-040
type: qa
status: done
updated: 2026-08-31
task: TASK-040
result: passed
test_command: python3 scripts/check-templates.py && python3 scripts/test-check-envelopes.py && python3 scripts/check-envelopes.py
---

## Test Strategy

No test runner (`claude-expert`): verification is behavioural — run every check directly and read the
artifacts against their schemas. **Every checker was run standalone, not through the `&&` chain**, because
this task's headline claim is that seven checkers go green and a chained pass can be a result never
produced. The chain was then run separately as its own evidence.

Before/after was established with a `git worktree` on `master`, so "pre-existing" is an observation and
not a claim inherited from `IMPLEMENTATION.md`.

Two behavioural probes were run against `check-templates.py` in that throwaway worktree, to establish what
a green run **proves** rather than what it suggests:

- `templates/BUG.md` with `module:` **empty** → exit 0. With `module: plugin` → exit 0. So presence, not
  value, is what the checker sees (`line.startswith(f"{key}:")`), exactly as `## Decisions` states.
- `templates/BUG.md` with an extra key `foo:` → exit 1, `frontmatter not in catalogue: foo`. The over-fix
  guard the design claimed is real.

`scripts/` was not touched. No test files were added: this module has none to add — the harness is
`scripts/test-*.py`, which is `plugin` source the design put out of bounds, and widening it is what the
design deliberately did not do.

## Results

Every check run directly, from the repository root:

| check | exit | output |
|---|---|---|
| `python3 scripts/check-templates.py` | **0** | `checked 21 templates`, `✔ all templates conform` |
| `python3 scripts/test-check-templates.py` | **0** | `ran 15 cases`, `✔ all cases pass` |
| `python3 scripts/check-envelopes.py` | **0** | `checked 10 dispatch envelopes`, `✔ all envelopes conform` |
| `python3 scripts/test-check-envelopes.py` | **0** | `checked 25 §5.5 obligation cases` |
| `python3 scripts/check-step-refs.py` | **0** | `checked 43 step references`, all resolve |
| `python3 scripts/test-check-step-refs.py` | **0** | `ran 28 cases`, `✔ all cases pass` |
| `python3 scripts/check-decisions.py` | **0** | `checked 29 decisions`, `✔ all decisions conform` |
| `config.md:33` `test_command` chain | **0** | run separately from the seven above |

**On `master`, run in a worktree:** `check-templates.py` exit **1**, `test-check-templates.py` exit **1**
with `✘ 3 case(s) failed`. The three named in the failure output are exactly the three `PLAN.md` named —
read, not counted: `clean tree exits 0`, `AC-1 no-headings row: the heading comparison is skipped, not the
row`, `AC-2 the decision row is reported as checked`. The other twelve are asserted still-passing by the
same run reporting zero failures.

**`python3 scripts/check-templates.py --target .orqestra` exits 1** — the recorded deviation, confirmed
untouched rather than trusted. Master and HEAD output was diffed line by line: the **only** difference is
`checked 167 artifacts` → `checked 170`, the three artifacts this task adds, all conforming. Zero mentions
of `BUG`. It is pre-existing and this change neither caused nor widened it.

## Criteria Coverage

| criterion | covered by | result |
|---|---|---|
| AC-1 | `check-templates.py` exit 0 (21 templates) and `test-check-templates.py` exit 0 (15 cases, 0 failed), both run standalone; §4.8.1:584 read; empty-value and extra-key probes | **pass, with a stated limit** — see Issues I-1 |
| AC-2 | Read-through of `skills/bugfix/step-intake.md` as a fresh analyst, against `.orqestra/modules.md`'s `## Modules` table and `skills/bugfix/SKILL.md:5` (`AskUserQuestion` held); `grep -rn "if known" skills/` → 0 hits | pass |
| AC-3 | `grep -n module templates/BUG.md` → frontmatter key + a `## Scope` comment pointing *at* it; `grep -rn -i scope skills/bugfix/` → both hits say `## Scope` does **not** name the module; `## Scope` heading survives, proven by `check-templates.py`'s ordered heading comparison | pass |
| AC-4 | `check-envelopes.py` exit 0 (10 envelopes); chain exit 0; `MODULE:` traced `step-diagnose.md:7` → `templates/BUG.md:6` `module:` → §4.8.1:584 `module`; `step-reproduce.md:7` and `step-promote.md:22` read the key rather than re-derive | pass |
| AC-5 | `git diff master...HEAD -- .orqestra/config.md` → `0 7` (seven deletions, zero insertions); line 33 md5 identical to master's; `grep -ci "red\|fails\|by design" .orqestra/config.md` → 0 | pass |

### What each green run does and does not prove

**AC-1.** A green `check-templates.py` proves the `BUG.md` frontmatter key **set** now equals §4.8.1's row
in both directions — `module` was added and nothing else was. It proves **nothing about a value**: the
probe confirms an empty `module:` passes. That is acceptable here only because the key is a *template*
placeholder, and every key in `templates/` is deliberately empty. What carries meaning is the comment
beside it (`templates/BUG.md:6-7`: *"THE routing key (D-029) … Established at intake, never 'if known' — a
bug without one is not creatable"*), which is instruction to the writer, not data a checker reads. The key
is not merely present; it is present with the rule that governs how it is filled.

**AC-2.** No schema and no checker enforces this. `check_instance` never globs `work/*/BUG.md`, so no real
bug is checked at all. Read as the analyst who will follow it, `step-intake.md:16-37` is a **procedure**,
not an assertion of one: the question is a closed choice over a **named table with named columns** that
exists (`.orqestra/modules.md`, `module` and `paths`, two rows); the fallback is a **derivation** against a
named column from named evidence; a derived candidate is **offered back**, with the one-match and
zero-or-many branches each given a different next action; and the loop terminates. Every branch ends in
either a `BUG.md` with a non-empty `module:` or a workflow that wrote nothing and said so. **No branch
ends in `blocked`**, per the §8.2 amendment, and the reason travels with the rule at :32-35. Intake holds
`AskUserQuestion` (`skills/bugfix/SKILL.md:5`), so step 1 is executable and not aspirational.

**AC-3.** D-029's second obligation is flat, and it is met flatly. Neither the template nor any of the four
step files carries the module in prose anywhere: the only two `## Scope` mentions in `skills/bugfix/` both
say it does **not** name the module, and `templates/BUG.md:25` says the same. This is silence, not merely
the absence of contradiction.

**AC-4.** `check-envelopes.py` exiting 0 is a **no-regression signal only** — it keys on the scope key and
never reads frontmatter, so it is not evidence that `MODULE:` has a key behind it. The evidence is the
trace, and the trace closes: `step-diagnose.md:7` names `work/BUG-NNN/BUG.md`'s `module:`; that key exists
in `templates/BUG.md:6`; §4.8.1:584 lists it as required. Before this change the same `MODULE:` resolved to
`## Scope` prose with no key anywhere.

## Issues

**I-1 — AC-1's green run cannot catch an empty `module:`.** Not a defect in this change; a stated limit on
what its evidence covers. Observed: `templates/BUG.md` with `module:` empty exits 0; with `module: plugin`
exits 0. Expected, for a schema that means anything: an instance with a blank routing key is rejected.
Already recorded as tech debt by `IMPLEMENTATION.md` with the three layers that would close it, and the
design named it before it was built. No action for this task — `scripts/` widening is explicitly out of
scope, and inventing it here is the speculative work the design forbids.

**I-2 — the recorded deviation understates the pre-existing failure it describes, though its material
claim holds.** `IMPLEMENTATION.md`'s Deviations row says the `--target .orqestra` failures are
`TASK-001/REVIEW.md` and `TASK-009/DESIGN.md`. Observed: **19** artifacts fail, across
`TASK-001`…`TASK-010` — eight `DESIGN.md` (`headings missing: ## Structure`), ten `TASK.md`, and one
`REVIEW.md`. The two named are a sample, not the set. This does **not** change the verdict: the claim that
matters — pre-existing, untouched by this change — was verified independently by worktree diff and is
true. Reported so the "two artifacts" figure does not get carried into a follow-up task as a scope
estimate.

**I-3 — intake's abandonment branch has no report shape.** `step-intake.md:34-35` says the workflow "ends
having written **nothing** and says so", but `## Report` shows only the success line. A fresh agent
reaching that branch has no prescribed output. Cosmetic, within AC-2's requirement (which asks that intake
not block, and it does not), and not grounds to fail — recorded because the next reader of this step will
hit it.

**I-4 — D-029's `Constrains` still reads "or intake blocks (D11)"**, which the §8.2 human decision on
`TASK.md` made dead prose. Confirmed still present in `.orqestra/decisions/D-029-a-bug-carries-its-module.md`.
A `docs` amendment (D14, D9), correctly not made here; already filed as tech debt.
