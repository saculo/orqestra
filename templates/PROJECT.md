---
id: PROJECT
type: project
status: in-progress
updated:
stack:
---

<!-- ONE TEST DECIDES EVERY LINE IN THIS FILE:
     what does this fact cost to find at the moment an agent needs it?

     Cheap — visible in the code, in a config file, in the framework's own docs — leave it
     out. Expensive, or learned only by getting it wrong once, write it down. That is the
     whole editorial rule, and it is why this file is short.

     It loads on EVERY dispatch, in every workflow, for every module. A line restating what
     a competent engineer already assumes costs context forever and pushes out the line that
     would have saved a rework cycle. Keep the whole file under ~150 lines.

     Project-wide only. Anything true of one module and not the others belongs in that
     module's expertise skills (§5.3) — a module may name several, one per concern.

     Written by `design` during the first task and appended to as the project teaches you
     things. At init this is a stub: a half-inferred fact is worse than an absent one,
     because every downstream agent will trust it. -->

## Stack
<!-- Languages, frameworks, runtimes, and tools — WITH THE VERSIONS ACTUALLY IN USE, read
     from the lockfile or build file, not from memory. The version is the expensive half:
     an agent that assumes the current release writes code this project cannot compile.

     Name what is deliberately absent too, when its absence is surprising: no ORM, no DI
     container, no build step. -->

## Layout
<!-- Where work lands, and what to read first. Directories and their responsibility — a map
     for someone who has never opened this repo, not an inventory.

     Include the placements that are non-obvious: where tests live relative to source, where
     generated code goes and what regenerates it, which directories are off limits. -->

## Commands
<!-- Build, test, lint, run — the invocation that ACTUALLY WORKS, which is often not the one
     the README prints. Note anything an agent would otherwise discover the slow way: a suite
     that takes twenty minutes, a command needing a service running first, a flag that must
     be passed locally.

     Mark anything detected-but-not-run as unverified rather than presenting a guess as fact. -->

## Conventions
<!-- Where this project DEVIATES from what the ecosystem would do by default. That is the
     only kind of convention worth the space: the defaults are already known.

     State the rule, then the reason — a bare rule is followed until it is inconvenient, a
     rule with a reason survives the edge case.

     ✅  "Errors cross a module boundary as a result type, never as an exception."
     ❌  "Use meaningful names."  — universal, and already assumed. -->

## Testing
<!-- Framework, layout, and what a test here must do that the framework does not imply: what
     is mocked and what never is, which suite gates a merge, how fixtures and test data are
     obtained, what a flaky test means in this repo.

     Read by `qa` on every task, so be concrete. Module-specific testing goes in that module's
     expertise skills. -->

## Git and GitHub
<!-- The rules below hold in every orqestra project. KEEP THEM ALL — they are defaults, not
     placeholders — and add this repo's own underneath. -->

- **Never work on the base branch.** Every source change lands on the task branch. Nothing
  before the push step commits source, and the push step is the only thing that reaches the
  remote.
- **Never touch work you did not create.** No `stash`, no `reset --hard`, no
  `checkout -- <path>`, no `clean`. Uncommitted changes in the tree are a human's, and they
  are the one thing here that cannot be recreated. Stop and say so instead.
- **Stage explicit paths.** No `git add -A`, no `commit -a`. You commit what you changed, not
  whatever happened to be sitting next to it.
- **Never rewrite published history.** No amend, no rebase, no force-push once a commit is on
  the remote and under review — reviewers lose the lines their comments point at.
  `--force-with-lease`, on your own task branch, to finish a rebase you were told to do, is
  the single exception.
- **One task, one branch, one PR.** A branch or a PR that already exists for this task is
  adopted, never duplicated — a second one splits the review and strands the first.
- **Merging is a human's decision** unless the config says otherwise, and a conflict is always
  a human's. Never auto-resolve one.
- **`gh` is the only route to GitHub.** No raw API calls with a token scraped from the
  environment.
- **Never edit, close, or resolve another person's PR, issue, or comment.** Reply to it.
- **Never commit secrets, credentials, `.env` files, or build output.** If it is generated, it
  is regenerated.

<!-- Then this repo's own, which nothing can infer: the base branch if it is not `main`;
     protected paths and CODEOWNERS; the checks a PR must pass; whether commits must be
     signed; whether a PR must link an issue; squash versus merge commit; and anything a
     contributor already got wrong once. -->

## Traps
<!-- The mistakes made repeatedly here — the accumulated cost of past debugging, and the part
     no model can infer from reading the code. Usually the most valuable section in the file.

     Add to it when an agent gets something wrong; that is the evidence this section runs on.

- **Do not** …, because …
     -->
