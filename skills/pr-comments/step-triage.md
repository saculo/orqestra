# Step — Triage

Write `COMMENTS.md`: one row per comment, fixed columns (§4.8.2), then gate per config.

| # | thread | file:line | summary | verdict | action |
|---|---|---|---|---|---|
| 1 | t_abc | `SessionStore.java:42` | null check missing | `accept` | add guard + test |
| 2 | t_def | `LoginForm.vue:11` | rename to `user` | `discuss` | conflicts with module convention |
| 3 | t_ghi | `Limiter.go:88` | use a map here | `reject` | n≤3; O(n) is correct here |

## Verdicts

| verdict | Meaning | Requires |
|---|---|---|
| `accept` | Valid — will be fixed | An action naming what changes |
| `reject` | Not correct here | **Drafted reasoning** for the human to send |
| `discuss` | Needs a human decision, not a code change | What the decision is |

**A `reject` without drafted reasoning is not allowed.** Rejecting silently, or with "won't fix", is how
review relationships break — the reviewer cannot tell whether they were wrong or ignored.

## Bots

CodeRabbit and similar are triaged like anyone else — but a bot thread of many low-signal comments may
be **batch-rejected with one drafted reply** rather than one reply per comment. Say in the row that it
is a batch.

## Judgement

You are allowed to reject. A reviewer suggesting something the module's conventions forbid, or an
optimization that does not apply at this scale, is wrong — and accepting it to be agreeable ships worse
code. Cite the convention or the reason.

When genuinely unsure: `discuss` (D11). That is what it is for.

## The gate (`semi` mode, default)

```
▸ GATE · triage · PR #142 · 7 comments

  accept   4   null guard, error message, missing test, doc typo
  reject   2   both suggest a map for n≤3 — reasoning drafted
  discuss  1   naming conflicts with the module convention

  [ Approve ]  [ Change a verdict ]  [ Reject with reason ]
```
