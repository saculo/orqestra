---
id:
type: review
status: done
updated:
task:
verdict: passed        # passed | changes-requested | failed
lenses: []             # correctness | design | security | performance | regression-risk | tests
required: []           # F-N ids the rework loop must address — every blocker and major, nothing else
review_round: 1        # 1 = first review · 2 = re-review of a disputed `failed`. There is no 3.
---

## Verdict
<!-- One paragraph. The verdict and the single reason for it. -->

## Findings
<!-- Table: id | severity | file:line | finding
     severity: blocker | major | minor | nit

     SEVERITY IS THE ONLY GRADE. There is no `required` column: every blocker and major
     goes in frontmatter `required`, no minor or nit may, and that list is what the
     rework loop consumes. Grading a finding twice is how `nit, required: yes` used to
     become expressible — and how the loop burned its three attempts.

     Every finding needs file:line. One a reader cannot locate cannot be fixed.
     A file outside the task's module paths is a `major` finding (D14).
     `_none_` if clean. -->

| id | severity | file:line | finding |
|---|---|---|---|

## What Would Change This Verdict
<!-- Required when `verdict: failed`, because a `failed` may be disputed and re-reviewed
     once (§8.1) — and a reviewer who cannot say what would reverse them is asserting a
     preference, not finding a defect. Name the evidence, design change, or criterion
     reading that would move you off it.
     `_n/a_` when the verdict is `passed` or `changes-requested`. -->

## Notes
<!-- Non-blocking observations, and anything outside the lenses you were given —
     including a simpler approach you would have preferred, which is a note and never a
     finding (§7.8.2). `_none_` if none. -->
