# Step — Verify

Run the full test suite from `PROJECT.md`. **Nothing regressed** is the bar.

Not "the fix works" — the fix working is necessary and not sufficient. PR-comment fixes are small,
scattered, and applied under the assumption they are safe, which is exactly the profile of a change that
breaks something two files away.

## On failure

Back to resolve, with the failure named. If the same fix fails twice, **block** — a comment whose fix
cannot be made to pass is a `discuss`, not a retry.

## Do not reply before this passes

A reply announcing a fix that broke the build is worse than no reply: the reviewer re-reviews, finds it
red, and now distrusts every other reply in the thread.

```
✓ verify · mvn test · 214 passed, 0 failed
```
