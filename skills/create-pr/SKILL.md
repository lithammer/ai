---
name: create-pr
description: Create a draft or ready-for-review PR for the current branch. Use when asked to draft, create, open, or prepare a PR, or to write a PR description.
---

# Create PR

1. Identify the current branch and an appropriate base branch. Inspect the
   intended changes, including uncommitted work, and use the conversation context
   already available. Check claims against the actual branch rather than relying
   on memory.
2. Write the title and description using the guidance below.
3. Read the description as a teammate about to review the diff. Keep the
   outcome, the visual, the evidence, and what the review must settle; cut
   prose that narrates the implementation or explains what the changed code or
   documents already say.
4. If asked only for a description, return the title and body without changing
   Git state or creating a PR. Otherwise, prepare the PR branch locally, creating
   one if needed. Commit only the intended changes if needed, then push that
   branch. Preserve file contents, unrelated changes, and unrelated staging.
   Keep the local checkout on the PR branch.
5. Create the PR as a draft unless explicitly requested ready for review.
   Confirm the published body matches the intended text. Return the URL and
   the author's remaining steps, or the title, body, and blocker if preparation
   or creation fails.

## Description

Write from the PR author's perspective, not as an assistant reporting on their
work.

Tell a teammate what this makes possible, and why now if they'd ask. Assume
they'll read the diff. Most PRs need only a short sentence of prose describing
the outcome.

Follow the outcome with a visual of the change's shape, so the reviewer knows
what the PR is about before they open the diff. A person cannot build that
picture from the diff at a glance; it shows the change only in pieces. Use a
call tree, a file tree, pseudocode, or a Mermaid diagram for parts that talk
to each other, and draw it as a `diff` block when the surrounding shape
already exists. Pick the smallest view that gives the overview, and keep only
the calls, files, and states it needs. Leave it out when the change has no
shape to show, such as a one-line fix.

Then name any decision the review must settle, such as a change that cannot
be rolled back.

Answer what a reviewer, or someone tracing this change later, would ask
first: how do you know it works? Show what you would show a teammate at
your desk, beside the claim it backs, and let it replace the explanation
where possible. For a fix or a behaviour change, show before and after.
Reuse it from the session or capture it now; `gh pr create --help` covers
`--attach`. Tests and CI show that logic meets a contract, not that the
change works in practice; leave out that they pass.

Fold what someone tracing this change later would want, such as a limit of
the evidence or a path not taken, into one `<details>` block after the
evidence, with a `<summary>` that says what it holds and a blank line after
`</summary>`. How the change rolls out and what the author still has to do,
such as deploy steps and pending checks, go in your reply to them.

End the body with a line for each issue the PR references that a reviewer
can open; a ticket that lives only on this machine, such as a `tk` id, is not
one. Read its open acceptance criteria: write `Closes #N` when this PR meets
the last of them, and `Refs #N` otherwise. Add `Refs #N` for each related PR
outside this PR's stack; GitHub already shows the stack.
