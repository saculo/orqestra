---
id: TASK-004
type: plan
status: done
updated: 2026-08-25
task: TASK-004
---

## Approach

Adversarial, not confirmatory. Every criterion here is a **refusal**, and a refusal is only proven by
attempting the thing and showing that nothing happened — so each test captures state before, runs
`init`, and diffs.

Checksums rather than eyeballing. "It said it refused" is not evidence it refused.

## Affected Areas

`skills/init/SKILL.md`, and fixtures in `/tmp`. Read the skill's refusal rules before testing to see
which criteria it actually instructs.

## Risks

- **`--force` is genuinely destructive.** Testing it means running it, so the fixture must contain
  planning state worth protecting or the test proves nothing.
- **Ordering claims are hard to verify headlessly.** AC-2 says "before replacing"; a `-p` run reports
  only its final message, so the sequence is not observable.

## Open Questions

_none_
