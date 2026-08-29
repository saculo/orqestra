---
id: TASK-024
type: qa
status: done
updated: 2026-08-29
task: TASK-024
result: passed
test_command: python3 scripts/check-step-refs.py --verbose && python3 scripts/test-check-step-refs.py
---

## Test Strategy

The `plugin` module has no test runner; verification is behavioural — run the thing and read what it
does (claude-expert, `## Testing`). Everything below was executed, nothing was inferred from reading
the checker.

Four independent probes, because the claims in `IMPLEMENTATION.md` are the kind that a green run
cannot distinguish from a checker that sees nothing:

1. **The count, taken independently of the checker.** A `grep -rnoE` over `skills/*/*.md` with the
   pattern D-026 defines returns **40** backticked step references — the same total the checker
   prints. A fix that deleted a dangling reference rather than repairing it would also turn the
   check green, so the total holding at 40 across the fix is the load-bearing evidence, not the
   green tick. Both sides of the diff report 40.
2. **The pre-fix tree.** `git archive master skills` into a throwaway dir plus a copy of the
   checker, run there. Reproduced exactly: 40 references, **9 findings, exit 1**, all `missing`.
   The checker has been watched failing on a real tree, which is TASK-008's lesson.
3. **The inversion trap, adversarially.** Wrote a straw-man checker that globs `skills/*/step-*.md`
   and confirms each file exists — the implementation D-026's last constraint forbids — and ran the
   committed harness against it. It fails 10 of 23 cases, including all three direction cases. The
   design's most-weighted case is genuinely discriminating, not decorative.
4. **False positives beyond the six.** Probed the excluded categories on real content: indented
   fences (`skills/init/SKILL.md:33`, `skills/task/step-push.md:30`) are handled by `lstrip`; no
   `~~~` fences exist in `skills/`; no step reference exists anywhere in `agents/`, `templates/` or
   `.claude-plugin/`, so the scope limit recorded as tech debt is honest today. No false positive
   found.

**Tests added (3 new cases, 23 → 28).** `DESIGN.md`'s `## Test Strategy` names two rows the
committed harness did not carry: the exit-2 robustness pair, and a clean-tree case asserting the
reported total against a count taken independently *in the test*. Both were verified by hand and
both hold, but a hand check does not survive to the next rename, which is what AC-3 is for. Added to
`scripts/test-check-step-refs.py` — the only file edited. No existing case was weakened or removed;
no implementation file was touched.

## Results

```
python3 scripts/check-step-refs.py --verbose   → exit 0, 40 references, all ✔
python3 scripts/test-check-step-refs.py        → exit 0, 28 of 28 cases pass
```

Pre-fix tree (`git archive master skills`):

```
checked 40 step references against D-026
✘ 9 unresolved or misshapen        → exit 1
```

Exit contract, exercised directly rather than read: no `skills/` → **2**, no traceback; a `skills/`
holding zero references → **2**; a dangling reference → **1**; clean → **0**.

Whole `scripts/` suite: `check-templates.py` 0, `check-decisions.py` 0, `check-step-refs.py` 0,
`test-check-templates.py` 0, `test-check-envelopes.py` 0, `test-check-step-refs.py` 0.
`check-envelopes.py` exits 1 on two envelopes owned by TASK-030 — out of scope, unchanged by this
task, and confirmed unrelated to any file in this diff.

## Criteria Coverage

| criterion | covered by | result |
|---|---|---|
| AC-1 — every step file named in every SKILL.md index table resolves, verified across all 22 skills | `check-step-refs.py` walks `skills/*/*.md`; all 22 skill dirs present, no `.md` nested deeper than depth 1, so coverage is total. 40 references, 0 findings, exit 0. Widened per §8.2 to every cross-skill reference, not only index rows: prose is checked too and 4 of the 9 pre-fix findings were prose. Discrimination proven on the pre-fix tree (9 findings, exit 1) and against the inverted straw man (fails 10 of 23) | **pass** |
| AC-2 — sharing expressed in a way that works, chosen deliberately and consistently | D-026 fixes the shape by loading mechanism, and the checker enforces it as a `shape` finding, so "consistently" is machine-checked rather than a matter of taste. Four harness cases cover both rules in both directions. Verified live: `add-phase:29,30` and `bugfix:33` carry `${CLAUDE_PLUGIN_ROOT}/skills/greenfield/…` in their index cells; the seven prose sites carry the plugin-relative form; `task/step-preflight.md:59` is unqualified inside a step file | **pass** |
| AC-3 — the check is runnable and cheap enough to sit alongside `check-templates.py`, so a rename cannot reintroduce this silently | Runs standalone: `python3 scripts/check-step-refs.py`, CPython 3 stdlib only (`re`, `sys`, `pathlib`), `ROOT` from `__file__`, no plugin runtime dependency (D-001, D-015), sub-second on 22 skills. Exit 0/1/2 all exercised. The rename case is the direction case: deleting `greenfield/step-plan-design.md` from a copy exits 1 and names **both** `add-phase/SKILL.md` and `bugfix/SKILL.md`, which a glob-and-exist checker cannot do | **pass** |

Both recorded deviations were checked against the actual diff and are accurate. The second stale
ownership line (`skills/greenfield/SKILL.md:42`) is in the diff, is made false by the same change,
and is covered by no test — correctly, since it is a factual claim about sharing, not a reference.
The authorship deviation is honest and changes nothing about what shipped: the committed checker,
corrections and harness match the approved design.

## Issues

_none_

Two observations, neither a defect and neither blocking:

- **The count assertion added at `test-check-step-refs.py` is a consistency check, not an absolute
  one.** It compares the checker's total against a regex scan in the test that shares `preprocess`,
  so it catches the checker's matcher narrowing but could not catch both narrowing together. The
  companion `...and that total is not zero` assertion, plus the exit-2-on-zero contract, is what
  guards the silent-zero case.
- **`.orqestra/config.md:33` still names `check-templates.py` as the whole `test_command`,** so this
  check runs only when someone remembers. Already recorded as tech debt in `IMPLEMENTATION.md`;
  noted here because AC-3's "so a future rename cannot reintroduce this silently" is only fully
  earned once something runs it automatically. Out of this task's scope — `config.md` is outside
  `plugin`'s paths.
