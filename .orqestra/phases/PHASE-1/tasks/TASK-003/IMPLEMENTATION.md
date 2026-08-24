---
id: TASK-003
type: implementation
status: done
updated: 2026-08-24
task: TASK-003
deviation: moderate
files_changed: 24
---

## Changes

**Four defects found by running `init`, none of them findable by reading:**

1. **`D15` citation drift.** Eight skills cited `D15` meaning "copy templates literally". Inserting D14
   (one task, one module) renumbered the charter, so `D15` became *No parallelism*. `init` was reading
   an instruction whose own citation contradicted it — and resolved that by composing files from
   scratch instead of copying templates. The first run produced `modules.md` and `PROJECT.md` with **no
   frontmatter at all**: correct-looking to a reader, invisible to `status`, which derives every task
   stage from frontmatter. Repointed to `D16`.

2. **`${CLAUDE_PLUGIN_ROOT}` missing from every template path.** All 22 skills referenced
   `templates/X.md` bare. Inside orqestra's own repo that happens to resolve; in **any user's project it
   does not** — it points at their directory. The run surfaced it as a reported deviation ("the repo
   only ships two templates"). Every skill now uses `${CLAUDE_PLUGIN_ROOT}/templates/X.md`.

3. **`init` wrote namespaced agent names** into `modules.md` (`orqestra:backend-engineer`), contradicting
   D-014, which puts the namespace at dispatch and keeps the registry bare. The skill now says so
   explicitly, with the reason.

4. **The checker validated templates, not artifacts.** AC-2 is about produced files, and nothing checked
   those — which is exactly how defect 1 shipped. Added `--target`.

Plus: `init` now states what to do when `AskUserQuestion` is unavailable — proceed on detection, mark it
unconfirmed, say which values need checking. A guess presented as a decision is the failure; a guess
labelled as a guess is fine.

## Deviations

| severity | from design | what | why |
|---|---|---|---|
| moderate | not planned | Repointed `D15`→`D16` across 6 files | Root cause of defect 1. Leaving it would have made the fix to `init` cosmetic |
| moderate | not planned | `${CLAUDE_PLUGIN_ROOT}` across all 22 skills | Defect 2 breaks orqestra in every project except its own. Too severe to defer |
| minor | not planned | Conditional-key (`` `name?` ``) support | The instance check on our own workspace flagged `bug` missing on 7 feature tasks; `bug` is only meaningful when `origin: bug` |

## Tech Debt

**Two docs-module follow-ups**, out of reach here (D14):

1. **`§4.8.1` must mark `bug` as `` `bug?` ``** — the mechanism now exists; the catalogue does not use
   it, so our own workspace still fails the instance check on 7 task files.
2. **`§4.8.3` should document `${CLAUDE_PLUGIN_ROOT}`**, and the charter should carry a warning that
   renumbering it silently repoints every citation. Defect 1 was invisible to the citation check written
   in TASK-007, because that check verifies citations *resolve* — not that they still mean what they
   meant.
