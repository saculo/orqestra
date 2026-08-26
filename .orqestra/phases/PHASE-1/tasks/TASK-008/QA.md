---
id: TASK-008
type: qa
status: done
updated: 2026-08-26
task: TASK-008
result: passed
test_command: python3 scripts/check-templates.py
---

## Test Strategy

The file under test is also the test command, so every criterion was proved by **inducing the failure**
it claims to catch, on throwaway copies of the tree (`scripts/` + `templates/` + `REQUIREMENTS.md` +
`.orqestra/`) under the scratchpad. The script resolves `ROOT` from `__file__.parent.parent`, so a copied
tree is a faithful subject; the repo working tree was never modified (`git status --short` empty at start
and at finish).

Every induced failure was also run against the **pre-fix script** (`git show master:scripts/check-templates.py`)
on the identical broken tree. A probe that fails both ways proves nothing, so each one had to pass before
the change and fail after it (or the reverse for AC-3's traceback).

AC-4 was not checked by reading the diff for a missing constant. The exemption was **moved in the
catalogue**: `PRD.md`'s Required-headings cell was given a real heading and `QA.md`'s cell was replaced
with `none`, then the checker was run to see which row it exempted. A script that still knew the name
`PRD.md` would have exempted the wrong one.

Both modes were exercised — default (`templates/`) and `--target` — because `## Deviations` records the
same fix applied to `check_instance()`, and an unverified deviation is an unverified change.

## Results

| run | outcome |
|---|---|
| `python3 scripts/check-templates.py` (repo, unmodified) | `checked 21 templates`, `✔ all templates conform`, exit 0 |
| same, pre-fix script, same tree | `checked 20 templates`, exit 0 — the row was silently absent |
| `--target .orqestra` (repo) | `checked 79 artifacts`, 19 pre-existing non-conformances, exit 1 |
| same, pre-fix script | `checked 55 artifacts` — 24 `decisions/D-*.md` never examined |
| `templates/DECISION.md` with `area:` deleted | exit 1, `decisions/D-NNN-*.md → frontmatter missing: area` |
| same break, pre-fix script | exit 0, `✔ all templates conform` — the defect, reproduced |
| `templates/DECISION.md` + `bogus_key:` | exit 1, `frontmatter not in catalogue: bogus_key` |
| `templates/DECISION.md` + stray `## Bogus Heading` | exit 0 — heading comparison correctly skipped |
| `REQUIREMENTS.md` deleted | exit 2, `✘ cannot read the catalogue at <path>: No such file or directory` |
| `REQUIREMENTS.md` `chmod 000` | exit 2, `… Permission denied` |
| `REQUIREMENTS.md` replaced by a directory | exit 2, `… Is a directory` |
| all three, with `--target` as well | exit 2, same message — the guard runs before either mode |
| `REQUIREMENTS.md` deleted, pre-fix script | exit 1 with `FileNotFoundError` traceback |
| §4.8.1 heading renumbered to §4.8.9 | exit 2, `✘ could not locate §4.8.1 in REQUIREMENTS.md` |
| catalogue probe: `none` moved from `PRD.md` to `QA.md` | `· QA.md: catalogue declares no schema — skipped`, and `PRD.md` newly checked and failing `headings missing: ## Zebra` |
| `.orqestra/decisions/D-001-*.md` with `area:` deleted, `--target` | exit 1, names the file; pre-fix script does not report it |

The 19 `--target` failures are the pre-existing schema drift `## Tech Debt` already records (ten `TASK.md`
missing `bug`, eight `DESIGN.md` missing `## Structure`, one `REVIEW.md`); none is new. The artifact count
is 79 rather than the 78 in `## IMPLEMENTATION` because `TASK-008/IMPLEMENTATION.md` itself landed since.

## Criteria Coverage

| criterion | covered by | result |
|---|---|---|
| AC-1 | `decisions/D-NNN-*.md` — the one row with no `##` headings — verbose-listed as `✓` checked; deleting `area:` fails, adding `bogus_key:` fails, adding a stray `## Bogus Heading` passes | pass |
| AC-2 | count 20 → 21 against the pre-fix script on an identical tree; `area:` deleted from `templates/DECISION.md` gives exit 1 naming `decisions/D-NNN-*.md`, where pre-fix gave exit 0 | pass |
| AC-3 | four unreadable-catalogue shapes (missing, `chmod 000`, a directory, renumbered heading) each exit 2 with a message and no traceback, in both modes; pre-fix exits 1 with `FileNotFoundError` | pass |
| AC-4 | catalogue probe: the `none` exemption moved from `PRD.md` to `QA.md` and the checker followed it, exempting `QA.md` and newly failing `PRD.md`. `FREEFORM` is gone; the surviving literals (`ALIASES`, `INSTANCE_PATHS`) are on-disk path mappings the catalogue does not state, not exemptions | pass |
| deviation (`check_instance`) | `--target` count 55 → 79; a `D-*.md` with `area:` deleted is reported post-fix and invisible pre-fix | pass |

## Issues

No criterion fails. One observation, below the bar for rework:

- **`none` in the Required-headings column exempts the frontmatter too, not just the headings.**
  Observed: with `QA.md`'s headings cell set to `none`, the row is skipped entirely — its frontmatter
  additions (`task`, `result`, `test_command`) are no longer checked. AC-1's rule as written ("only the
  heading comparison is skipped") holds for `decisions/D-NNN-*.md` but not for a row that writes the word
  `none`. Not a defect today: the only such row is `PRD.md`, which §4.8.1 calls "the one free-form input"
  and whose template deliberately carries no frontmatter, so checking it would produce a false failure —
  and the two-tier reading is exactly what `## Decisions` in `DESIGN.md` specifies. The latent cost is
  that a future catalogue edit writing `none` in that column silently drops that row's frontmatter from
  the checked count, which is the same class of defect this task closed. `docs` module if it is ever
  worth a distinct marker; noted, not raised.
