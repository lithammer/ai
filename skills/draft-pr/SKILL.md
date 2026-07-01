---
name: draft-pr
description: Create a draft PR for the current branch. Use when asked to draft, create, open, or prepare a PR, or to write a PR description.
---

# Draft PR

A PR description helps reviewers understand why the change exists and
why the solution is acceptable. Start with one sentence summarizing
the outcome. Most PRs need nothing more, and a one-sentence body
stands alone -- no heading, no prefix:

```md
Bump `eslint-plugin-react` from 7.34 to 7.36 and accept the auto-fix output.
```

Sections are the exception, added one at a time only when they carry
something the diff doesn't already show -- never to restate it. When
sections do follow, bold-prefix the opening sentence with
`**tl;dr:**` so a skimmer knows they can stop there, and name each
section for what the reader gains from it, not for a slot in a
template.

Reviewers see the diff: explain *why* and *consequences*, not *what
changed*, and complete the plain-language paragraph before any
bullets or internal names appear. Internal function names, SDK
quirks, concurrency primitives, process narrative, and things you
considered but didn't do belong in code, PR threads, or follow-up
issues, not the description. Write for a skimmer -- no paragraph
over three sentences, and a body creeping past a dozen lines of
prose is a signal to cut. Reader test: a senior engineer who doesn't
work on this system can explain the change back in one sentence
after the opening line and first paragraph.

Prefer showing over telling when an artifact reads faster than the
prose describing it: a before/after of output, a sample payload, a
screenshot for UI changes, a small table. The artifact replaces the
paragraph -- it never sits alongside one saying the same thing --
and observable behaviour is exactly what the diff can't show.

For PRs in a series, make the opening line self-locating ("publisher
side of ...", "infra prerequisite for ..."). When citing a sibling's
merge state, link the PR -- tickets can't be merged.

Process:

1. Identify the current branch and an appropriate base branch, and
   read enough context to understand intent and implementation.
2. Draft an outcome-oriented title and the body in two passes: first
   cover the goal, then compress -- cut every paragraph that tells
   the reviewer nothing beyond the diff and the opening line, and
   shorten any past three sentences. Stop when further compression
   would lose load-bearing information.
3. Create the PR with `--draft`. If creation fails, leave the user
   the title, body, and command to run.
