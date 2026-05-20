---
name: draft-pr
description: Create a draft PR for the current branch. Use when asked to draft, create, open, or prepare a PR, or to write a PR description.
---

# Draft PR

A PR description helps reviewers understand why the change exists and
why the solution is acceptable. The `tl;dr` line carries the
description; other sections are added only when they carry information
the `tl;dr` can't, never to restate it.

Optional sections, in heading order: `Abstract`, `Solution`, `Caveats`,
`Alternatives`, `Follow-up`, `Resolves`. See
[EXAMPLES.md](./EXAMPLES.md) for shapes.

Reader test: a senior engineer who doesn't work on this system should
be able to follow every paragraph and explain the change back in one
sentence after reading the `tl;dr` plus the first paragraph. Describe
the contract, not the mechanism -- internal function names, SDK
quirks, concurrency primitives, and process narrative ("X asked us to
split this up") belong in code or PR threads, not the description.

For PRs in a series, make the `tl;dr` self-locating ("publisher side
of ...", "infra prerequisite for ..."). When citing a sibling's merge
state, link the PR -- tickets can't be merged.

## Process

1. Identify the current branch and an appropriate base branch.
2. Read enough context to understand intent and implementation.
3. Draft an outcome-oriented title and body.
4. Create the PR as a draft. If creation fails, leave the user with
   the title, body, and command to run.

## Checks

- Body starts with `**tl;dr:**`.
- Reader test passes.
- PR is created with `--draft`.
