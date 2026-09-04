---
name: draft-pr
description: Create a draft PR for the current branch. Use when asked to draft, create, open, or prepare a PR, or to write a PR description.
---

# Draft PR

A fresh subagent writes the description. It reads the branch cold,
which is what keeps the body short; the main session supplies only
what the repository cannot say.

1. Identify the current branch and an appropriate base branch.
2. Write the context: what prompted the change (a ticket, a thread, a
   conversation, an incident), constraints agreed outside the
   repository, where the PR sits in a stack, and whether it opens as
   a draft or ready for review. Facts only, never a body: the drafter
   writes the prose.
3. Spawn a subagent. Pass it [DRAFTER_BRIEF.md](./DRAFTER_BRIEF.md)
   as its persona and
   [DRAFTER_REPORT_FORMAT.md](./DRAFTER_REPORT_FORMAT.md) as its
   output specification, with the branch, the base, and the context
   as its input.
4. Relay the URL. Verify each claim the report marks as inferred and
   correct a wrong one with `gh pr edit`, that sentence only. If the
   report says the PR was not created, hand the user its title, body,
   and command.
