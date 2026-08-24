---
id: TASK-004
type: qa
status: done
updated: 2026-08-25
task: TASK-004
result: passed
test_command: python3 scripts/check-templates.py --target <workspace>
---

## Test Strategy

Each refusal tested by attempting the forbidden thing and proving nothing changed — checksums of every
file, `HEAD`, and `git status`, captured before and compared after.

## Results

```
AC-1  init over an existing workspace
      ✔ no file changed (md5 of all 6 identical)
      ✔ no new commit          ✔ working tree clean
      report named --force as the override and stopped

AC-2  init --force
      ✔ proceeds; report distinguishes KEPT from replaced, per file
      ~ "before replacing" not observable in a -p session (see Issues)

AC-3  PRD.md with --force
      ✔ byte-identical (md5 OK), content intact
      ✔ also untouched on the AC-1 refusal path

AC-4  init in /tmp/nogit (no git repository)
      ✔ stopped with an explanation and a `git init` suggestion
      ✔ directory still empty — nothing written

AC-5  no remote + gh stub exiting non-zero on auth
      ✔ "⚠ No git remote configured — planning works; delivery needs one"
      ✔ "⚠ gh not authenticated — planning works; run gh auth login"
      ✔ init succeeded; workspace conforms (exit 0)
```

## Criteria Coverage

| criterion | covered by | result |
|---|---|---|
| AC-1 | checksum + HEAD + status comparison across the refusal | passed |
| AC-2 | `--force` run against a workspace holding a written PRD | passed (announcement rule now specified; ordering needs an interactive run) |
| AC-3 | PRD md5 before/after, both with and without `--force` | passed |
| AC-4 | run in an empty non-git directory, then `ls -a` | passed |
| AC-5 | run with no remote and a failing `gh` stub | passed |

## Issues

**AC-2's "before replacing" is not observable headlessly.** A `-p` session surfaces only its final
message, so the ordering of an in-turn announcement cannot be seen. What is verified: `--force`
proceeds, and the report distinguishes kept files from replaced ones per file. What is now *specified*
but unproven: that the list is printed before the first write.

Same category as TASK-003's AC-3, and it wants the same one interactive run to close both.

**A gap this task found that its own criteria did not ask about**: nothing said whether `--force` may
delete `phases/`, `work/`, or `decisions/`. It never did in testing, but only because no fixture had
planning state to lose. Now specified.
