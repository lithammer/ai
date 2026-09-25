---
name: create-pr
description: Create a draft or ready-for-review PR for the current branch. Use when asked to draft, create, open, or prepare a PR, or to write a PR description.
disable-model-invocation: true
---

# Create PR

A fresh subagent writes the description. It reads the branch cold; the main
session supplies only what the repository cannot say.

1. Identify the current branch and an appropriate base branch.
2. Supply only relevant facts the drafter cannot discover from the repository:
   what prompted the change, decisions made outside the repository, and stack
   context when needed. Include whether the PR opens as draft or ready for
   review. Context is evidence, not an outline for the description; omit
   implementation details and unrelated follow-up work. The drafter checks
   supplied claims against the repository and corrects any that conflict.
3. Spawn a subagent. Pass it [DRAFTER_BRIEF.md](./DRAFTER_BRIEF.md) as its
   persona, along with the branch, base, and context.
4. If creation succeeded, read the published body directly from GitHub and
   check it against the drafter brief. The body introduces the diff; cut
   explanations already present in changed code or documents, implementation
   narration, and context the reviewer does not need to understand the outcome.
   Apply any corrections to the PR and confirm the published body matches the
   intended text.
5. Relay the URL, or the title, body, and blocker if creation failed.
