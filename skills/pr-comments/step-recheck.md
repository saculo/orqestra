# Step — Recheck

Re-fetch. Reviewers comment while you work, and a pass that ignores what arrived mid-run leaves threads
unhandled with no record of why.

| Result | Do |
|---|---|
| New comments since the run started | Loop to triage — **with only the new ones** |
| Only `discuss` threads remain | Done. Report them; they need a human, not another pass |
| Nothing unresolved | Done |

## Termination

The loop ends when a full pass adds no new threads.

**Three passes without converging → block.** A PR generating comments faster than they are resolved
needs a conversation, not a fourth pass — and the loop will otherwise run until someone notices the token
bill. Report what is still open and who is adding to it.

## Report

```
✓ pr-comments · PR #142 · 7 comments · 4 fixed, 2 rejected, 1 open for discussion

  ← thread t_def needs your decision: naming conflicts with the module convention
```

Then hand back to the task pipeline, which continues to the merge gate.
