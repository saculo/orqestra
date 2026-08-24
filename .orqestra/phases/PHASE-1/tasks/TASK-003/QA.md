---
id: TASK-003
type: qa
status: done
updated: 2026-08-24
task: TASK-003
result: passed
test_command: python3 scripts/check-templates.py --target <workspace>
---

## Test Strategy

Three `init` runs in three fresh git repositories, each checked with the instance checker: a Java repo
before the fixes, the same after, and a TypeScript repo to confirm detection is not hard-coded.

## Results

```
run 1 (java, before fixes)     4 artifacts · ✘ 4 fail
                                 modules.md, PROJECT.md — no frontmatter (D16 violation)
                                 decisions/INDEX.md — 5 keys missing
                                 config.md — ## Routing missing
run 2 (java, after fixes)      4 artifacts · ✔ conform   exit 0
run 3 (typescript, after)      4 artifacts · ✔ conform   exit 0
```

Run 3 detected `typescript` / `npm test` from `package.json` — detection is genuinely reading the repo,
not defaulting.

## Criteria Coverage

| criterion | covered by | result |
|---|---|---|
| AC-1 | runs 2 and 3 — full tree, `phases/` and `work/` present (as `.gitkeep`) | passed |
| AC-2 | `--target` on runs 2 and 3 — every produced file conforms, exit 0 | passed |
| AC-3 | runs 1–3 — degrades honestly, marks values unconfirmed, names what to check | **partial** — see Issues |
| AC-4 | run 3 — `\| app \| src/ \| backend-engineer \| typescript \| typescript-expertise \|`, agent bare and real; report explains the registry | passed |
| AC-5 | runs 2 and 3 — one commit `chore(orqestra): initialize workspace`, zero files outside `.orqestra/` | passed |

## Issues

**AC-3 cannot be fully verified non-interactively.** It requires the stack to be "always confirmed via
`AskUserQuestion`", and that tool does not exist in a `-p` session. What is verified is the fallback:
`init` proceeds on detection, marks the values unconfirmed, and names exactly which to check — three
times out of three, unprompted.

**The remaining half needs one interactive run**: `claude --plugin-dir . ` then `/orqestra:init` in a
scratch repo, confirming the question is actually asked before anything is written.

**Deviation is `moderate`, not `minor`.** Two of the three deviations were unplanned repairs to *other*
files — the D15 citation drift and the plugin-root paths. Both were root causes rather than side
issues: fixing `init` alone would have left the first defect to recur in every other skill, and the
second breaks orqestra in every project but its own.
