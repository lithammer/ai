---
name: create-pr
description: Create a draft or ready-for-review PR for the current branch. Use when asked to draft, create, open, or prepare a PR, or to write a PR description.
---

# Create PR

1. Identify the current branch and an appropriate base branch. Inspect the diff
   and use the conversation context already available. Check claims against the
   actual branch rather than relying on memory. Leave the working tree unchanged.
2. Write the title and description in the current session using the guidance
   below.
3. Read the description as a teammate about to review the diff. Keep the outcome
   and useful heads-ups; cut implementation narration and explanations already
   present in the changed code or documents.
4. Create the PR as a draft unless explicitly requested ready for review.
   Confirm the published body matches the intended text. Return the URL, or the
   title, body, and blocker if creation fails.

## Description

Tell a teammate what this makes possible, then mention anything they'd otherwise
be surprised by or need to decide. Assume they'll read the diff. Most PRs need
only a short sentence describing the outcome.

A heads-up might explain why the change matters now, a surprising consequence,
a deliberate omission, a decision for reviewers, or a merge dependency. These
are reasons to add context, not a checklist to fill out. Keep discussion tied to
a particular line in an inline comment rather than the description.

Add an example, before/after benchmark table, log excerpt, traceback, or other
illustration only when it makes the outcome clearer than prose alone. Let it
replace the explanation where possible. Omit validation summaries.
