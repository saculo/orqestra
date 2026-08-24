# Step — Reply

Commit, push, reply to every thread, resolve the ones you addressed.

## 1. Commit and push

Use `config.md`'s `commit_style`, onto the **task branch**. **Never force-push** to a branch under
review — it destroys the reviewers' view of what changed since they looked.

## 2. Reply to every thread

| verdict | Reply |
|---|---|
| `accept` | What changed and where — file and commit. Not "done" |
| `reject` | The drafted reasoning, in full |
| `discuss` | The question, addressed to the reviewer |

"Fixed" is not a reply. `Added a null guard in SessionStore.java:44 and a test covering the empty case — a3f21c8` is.

## 3. Resolve

Resolve the threads you addressed. **Never resolve a `discuss` thread** — it is waiting on a human, and
resolving it makes their question disappear.

## 4. Write `RESOLUTION.md`

Per comment: verdict, action taken, commit, whether the thread was resolved. Plus the reply text in
full under `## Replies Sent`, so a rejection's reasoning survives outside GitHub.

```
✓ reply · 4 fixed, 2 rejected with reasoning, 1 left open for discussion
```
