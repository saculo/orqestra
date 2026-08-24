# Step — Fetch

Collect every thread on the PR. Human and bot, resolved and unresolved.

```bash
gh pr view <n> --json reviews,comments,reviewThreads,state
gh api repos/{owner}/{repo}/pulls/<n>/comments --paginate
```

`gh auth status` failing → **block** `gh-auth`.

**Fetch everything, including already-resolved threads.** They are recorded and skipped, not
re-litigated — but a thread you never fetched is a thread you cannot prove you handled, and the next
recheck pass will treat it as new.

Note each thread's id, file and line, author, whether it is a bot, and its resolved state. Thread ids
are how replies are addressed later; losing them means replying in the wrong place.

## No comments

A PR with no review comments passes straight through to merge. Expected case, not a suspicious one — do
not wait for comments to appear, and do not prompt for them.

```
✓ fetch · 7 comments across 5 threads (2 already resolved)
```
