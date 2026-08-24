<!--
  orqestra — module expertise skill template
  ==========================================
  These are YOUR skills, not orqestra's. One per module whose conventions differ from
  the defaults a competent engineer in that stack would assume.

  Copy to  .claude/skills/<name>/SKILL.md  in your project, then name it in the
  `expertise` column of that module's row in .orqestra/modules.md:

      | worker | services/worker | backend | python | python-expertise, celery-conventions |
                                                                       ^^^^^^^^^^^^^^^^^^^

  Loaded by EVERY step of a task in that module — plan, design, implement, qa, review —
  so write it for all five readers, not just the engineer.

  ─────────────────────────────────────────────────────────────────────────────
  THE ONE RULE THAT DECIDES WHAT GOES IN HERE

  Write only what a competent engineer in this stack would get WRONG without being told.

    ✅  "Controllers return ResponseEntity, never raw DTOs. Errors go through
         GlobalExceptionHandler — never try/catch in a controller."
    ✅  "Celery tasks must be idempotent and take only JSON-serializable args.
         We replay from the DLQ, so a task that runs twice must be safe."
    ✅  "Vue components are <script setup> with the Composition API.
         No Options API in new code, even when editing an Options API file."
    ✅  "Argo Applications are generated from charts/. Never edit deploy/*.yaml
         by hand — it is regenerated and your change disappears."

    ❌  "Java is statically typed."                    the model knows
    ❌  "Use meaningful variable names."               not module-specific
    ❌  "Celery is a distributed task queue."          background, not a convention
    ❌  A tutorial on Spring Boot.                     it knows the framework; it
                                                      does not know YOUR choices

  Every line that fails this test costs context on every dispatch for this module,
  forever, and pushes out a line that would have mattered.
  ─────────────────────────────────────────────────────────────────────────────
-->

---
name: "▢module-conventions"
description: "▢What this covers and which module it belongs to — e.g. 'Spring Boot conventions for the api module: layering, error handling, transactions, and testing patterns.' Loaded by orqestra for every task in that module; also usable directly when working in those paths."
---

# ▢Module — ▢Stack Conventions

▢One or two sentences: which module, which stack, and what someone must know before
▢touching it that they would not assume.

## Structure

▢How code is organised in this module. Where things go, and what must not go where.
▢Name real paths — an agent will follow them literally.

## Conventions

▢The rules that differ from the stack's defaults. Be specific and prescriptive:
▢state the rule, then the reason, because a rule with a reason survives edge cases
▢that a bare rule does not.

- ▢**Rule.** Why.
- ▢**Rule.** Why.

## Patterns

▢The shapes to follow. A short real example beats a paragraph of description —
▢prefer code from this actual module over invented illustrations.

```▢lang
▢
```

## Testing

▢How this module is tested: framework, layout, what a test must assert, what is
▢mocked and what never is. Read by `qa` on every task here, so be concrete.

## Traps

▢The mistakes that are made repeatedly in this module. This section is usually the
▢most valuable one in the file — it is the accumulated cost of past debugging, and
▢it is the part no model can infer from the code.

- ▢**Do not** ▢…, because ▢…

<!--
  Keep this under ~150 lines. It loads on every dispatch for this module.
  When it grows past that, split by concern (api-conventions, api-testing) and
  name both in the modules.md row.
-->
