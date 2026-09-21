---
name: create-pr
description: Create a draft or ready-for-review PR for the current branch. Use when asked to draft, create, open, or prepare a PR, or to write a PR description.
disable-model-invocation: true
---

# Create PR

A fresh subagent writes the description. It reads the branch cold; the main
session supplies only what the repository cannot say.

1. Identify the current branch and an appropriate base branch.
2. Write the context: what prompted the change (a ticket, a thread, a
   conversation, an incident), constraints agreed outside the
   repository, where the PR sits in a stack, and whether it opens as
   a draft or ready for review. Facts only, never a body: the drafter
   writes the prose.
3. Spawn a subagent. Pass it [DRAFTER_BRIEF.md](./DRAFTER_BRIEF.md) as its
   persona, along with the branch, base, and context.
4. Relay the URL, or the title, body, and blocker if creation failed.
