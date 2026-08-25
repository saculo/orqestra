---
name: claude-expert
description: "Expertise for authoring Claude Code plugin components — skills, subagents, slash commands, and plugin manifests. Covers the file formats, frontmatter fields, loading model, tool permissions, and the writing discipline that makes instructions hold up for an agent with no prior context. Use when writing or reviewing anything under skills/, agents/, commands/, or .claude-plugin/."
---

# Claude Code Plugin Authoring

The `plugin` module is Claude Code plugin components. What ships is instructions, not code — so the
craft is in what a fresh agent will do when it reads them, not in what they say to a person who already
knows.

## Structure

```
.claude-plugin/plugin.json   name, description, version, author — `name` is the skill namespace
skills/<name>/SKILL.md       skill; the FOLDER NAME is the invocation name → /<plugin>:<name>
skills/<name>/step-*.md      orchestrator shards, loaded only when that step runs
agents/<name>.md             subagent — frontmatter: name, description, tools
templates/<NAME>.md          artifact schemas, copied literally by the skill that writes them
```

**Never create a `commands/` directory.** It is the legacy flat form; plugin skills already *are* the
slash commands, namespaced automatically from `plugin.json`'s `name`. A parallel command file per skill
describes the same invocation twice (D-012). Arguments come from `$ARGUMENTS`, with `argument-hint` in
the skill's frontmatter.

**Never put `skills/`, `agents/`, or `hooks/` inside `.claude-plugin/`.** Only `plugin.json` goes there;
everything else sits at the plugin root. This is the single most common structural mistake.

## Development loop

```bash
claude --plugin-dir .        # load the plugin from the working tree — no install
/reload-plugins              # pick up edits without restarting
claude plugin validate .     # structural validation; --strict treats warnings as errors
```

`--plugin-dir` takes precedence over an installed plugin of the same name for that session, so a local
copy can be tested without uninstalling anything.

## The loading model — the thing to design around

Three levels, and getting them wrong is the most common failure:

1. **`description` is always in context** for every installed skill. It is the *only* thing the model
   sees when deciding whether to load the skill.
2. **The `SKILL.md` body loads only after the skill triggers.**
3. **Bundled files load only when the body points at them.**

Two consequences that decide how you write:

- **Put every trigger phrase in the `description`.** A "When to use this skill" section in the body is
  invisible at the moment the decision is made. Name what it does, what it produces, and the literal
  phrases a user would type.
- **Shard anything long.** A step file that loads only when its step runs costs nothing the rest of the
  time. This is the main context-economy lever in the whole plugin.

## Conventions

- **`allowed-tools` does NOT enforce.** It pre-approves: the listed tools run without a permission
  prompt, and *every unlisted tool stays callable*. An orchestrator without `Write` in `allowed-tools`
  can still write — it just gets asked first. The restricting field is **`disallowed-tools`**, and it
  clears at the user's next message.
- **Durable enforcement lives in `agents/<name>.md`.** Its `tools:` field is a true allowlist and
  `disallowedTools:` a true denylist, both for the whole subagent run. Note the casing — the agent
  fields are camelCase, the skill field is kebab-case, and a camelCase key in a `SKILL.md` is silently
  ignored. Put a guarantee in the agent when the work is dispatched; a skill can only hold it for a
  turn.
- **Still prefer a structural constraint over an instruction asking for restraint** — the instruction
  degrades under pressure. Just verify the constraint is real before you rely on it, and say plainly
  which layer holds it (§7.0.1).
- **Write for a reader with no context you have not given them.** An instruction that reads clearly to
  someone holding this conversation may be genuinely ambiguous to a fresh subagent — and that is the
  only reader it will ever have.
- **Put the negative rule where the mistake would be made.** "Do not commit — push owns git" placed in
  the implement skill prevents more than a paragraph about ownership placed anywhere else.
- **State the reason with the rule.** A rule with a reason survives edge cases the bare rule does not,
  because the agent can tell whether the current case is one of them.
- **Imperative voice.** "Read the design first", not "the design should be read first".

## Patterns

Fixed section order in every skill, so a reader knows where to look:

```markdown
---
name: "orqestra:thing"
description: "What it does, what it produces, when to use it — with trigger phrases."
allowed-tools: Read, Write, Glob, Grep
---

> **Invocation**: how it is reached · **Class**: which class

# Title
One paragraph: what you are, and the boundary — what you must NOT do.

## Inputs      table of paths, with why each is read
## Output      the ONE artifact, and its template
## Procedure   numbered, imperative, one action per step
## Return      the ≤10-line block handed back
## When you cannot proceed    conditions → blocked_reason
## Rules       the non-obvious constraints, numbered
```

## Testing

There is no test runner. Verification is behavioural: install the plugin, run the command, inspect the
artifacts it produced against their schemas.

Write criteria that way too — "running `/orqestra:init` in an empty repo produces a valid workspace" is
checkable; "the init skill is written" is not.

## Traps

- **Do not** describe when to use a skill in its body — put it in `description`, the only part read
  before triggering.
- **Do not** give an orchestrator `Write` "just for convenience". The whole separation collapses, and it
  collapses quietly.
- **Do not** number step files. Order lives in the SKILL.md index table; a numeric prefix means
  inserting a step renames every file after it.
- **Do not** restate a rule that lives elsewhere. Cite it by number. A rule written twice is a rule that
  will disagree with itself.
- **Do not** write a template's guidance as prose the skill must interpret. Put it in HTML comments the
  skill strips — the template *is* the schema, in executable form.
- **Do not** let a skill exceed ~150 lines without sharding. Long skills get skimmed, and the part that
  gets skipped is the Rules section at the bottom.
