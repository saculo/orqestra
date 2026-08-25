---
id: D-013
type: decision
status: active
updated: 2026-08-25
amended: 2026-08-25          # skills-dir plugin is now primary — see **Amendment**
area: runtime
supersedes: —
superseded_by: —
---

# D-013 — `--plugin-dir` is the development and dogfooding mechanism

**When:** 2026-08-24 · bootstrap · dogfooding bootstrap
**Decision:** `claude --plugin-dir .` loads orqestra from its own working tree; `/reload-plugins` picks up edits in-session; `claude plugin validate .` checks structure. Marketplace packaging is deferred to PHASE-5.
**Why:** Dogfooding requires orqestra to be runnable in its own repository, but it cannot install itself from a marketplace before the marketplace work exists — a bootstrap deadlock. `--plugin-dir` dissolves it: the working tree is live, so a skill edited in a session is testable in that same session. It also removes marketplace packaging from PHASE-1, where it was scope nothing needed yet.
**Constrains:** Development and every dogfooding run use `--plugin-dir`, never an install. Do not add `marketplace.json` before PHASE-5 — no earlier phase needs it.

## Amendment — 2026-08-25

**A third mechanism exists, and it is better for dogfooding than either option this decision weighed.**
A directory under `.claude/skills/` containing `.claude-plugin/plugin.json` loads automatically as
`<name>@skills-dir` — no marketplace, no install, no flag. This decision framed the choice as
*`--plugin-dir` versus marketplace install* because that was the whole option space as understood at
the time. It was not.

`.claude/skills/orqestra/` now holds the manifest, with its component directories **symlinked to the
plugin at the repo root** so there is exactly one copy of every file (§2.1). Opening this repo in
Claude Code makes `/orqestra:*` available with no flag, which is what "develop orqestra using orqestra"
actually requires: a run that forgets the flag is a run that silently has no orqestra in it.

**Both original constraints survive intact**, which is why this is an amendment and not a reversal:

- *Never an install* — a skills-dir plugin is not installed; nothing is fetched and there is no
  `uninstall`, only deleting the folder.
- *No `marketplace.json` before PHASE-5* — reinforced, not weakened. The mechanism that made the
  marketplace tempting is gone, so the packaging work stays in PHASE-5 where it belongs.

`--plugin-dir .` is retained as the fallback: it is how the tree is loaded from **outside** this repo,
and how a checkout on a filesystem without symlink support runs at all.

**Constrains, added:** the three project-scope conditions in §2.1 are load-bearing and easy to violate
silently. **Trust the workspace** (a parent folder does not count, `-p` does not count); **launch from
the repo root** (skills-dir plugins do not walk up, so a session started in a subdirectory has no
orqestra and says nothing about it); and **do not also pass `--plugin-dir .`**, which loads the same
plugin twice under two names. Symlinks stay symlinks — copying the tree into `.claude/` would create a
second source of truth for ~90 files.
