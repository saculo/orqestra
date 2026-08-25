---
id:
type: design
status: done
updated:
task:
decisions: []          # D-NNN ids recorded by this design
---

<!-- ALTITUDE. This is architectural advice, not a work order. You say what should exist,
     what it is responsible for, and what must not cross which boundary. The engineer
     chooses the files — they are reading the code while they type, and you read it once.

     A design that names paths is a design that goes stale the moment anything else merges,
     and it invites an engineer to satisfy the list instead of the criteria. -->

## Components
<!-- What should exist when this is done, and what each piece is RESPONSIBLE for — one
     capability per component, stated as a responsibility rather than an implementation.

     Each one names the AC-N it serves. A component serving none is scope you invented.
     Delete it. -->

## Interfaces
<!-- The contracts between those components and the code around them: signatures, types,
     error shapes, the data that crosses each seam.

     These must match the real code you read, not code you assume exists — an invented
     interface is the most common cause of a `design-invalid` block at implement. -->

## Structure
<!-- WHERE the work lands and HOW it is shaped — never a list of files to touch.

     Name the areas and layers each component belongs to, in the vocabulary this project's
     layout already uses. Say what must not reach into what. Say the order the pieces have
     to come together when one depends on another. A path appears here only as an existing
     thing you are extending, never as a file to create.

     The whole change stays inside the task's module (§5.2, D2); a design needing a second
     module is two tasks.

     ❌  "Create src/main/java/com/acme/auth/TokenStore.java"
     ✅  "The token store belongs in the persistence layer beside the session repository,
          and nothing above the service layer may hold a reference to it. It has to exist
          before the refresh endpoint, which reads through it." -->

## Decisions
<!-- Choices made here, each with the reason that makes it survive an edge case. One that
     constrains FUTURE tasks also gets a decisions/D-NNN-*.md file and is cited by id.
     Local ones live only here. -->

## Test Strategy
<!-- What proves each criterion. Not "add unit tests" — which behaviour, verified how. -->
