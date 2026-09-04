---
name: draft-pr
description: Create a draft PR for the current branch. Use when asked to draft, create, open, or prepare a PR, or to write a PR description.
---

# Draft PR

A PR description helps reviewers understand why the change exists and
why the solution is acceptable. Start with one sentence summarizing
the outcome. Most PRs need nothing more, and the sentence is the
whole body:

```md
Bump `eslint-plugin-react` from 7.34 to 7.36 and accept the auto-fix output.
```

Sections are the exception, added one at a time only when they carry
something the diff and the CI checks don't already show. Name each
section for what the reader gains from it. Headings are `###`: a
section label should not outshout the body it introduces.

Reviewers see the diff: explain *why* and *consequences*, not *what
changed*, and complete the plain-language paragraph before any
bullets or internal names appear. Describe what shipped, at the level
of the contract; the rest belongs in code, PR threads, or follow-up
issues. Use the repository's normal technical vocabulary with
ASD-STE100 sentence discipline and typewriter punctuation. Write for
a skimmer -- no paragraph over three sentences, and a body creeping
past a dozen lines of prose is a signal to cut. Meet those bounds by
deleting whole sentences; what survives stays as written. The bounds
are ceilings; the floor is the reader test: a senior engineer who
doesn't work on this system can explain the change back in one
sentence after the opening line and first paragraph. A line only an
insider can parse is broken, and the repair is a plainer sentence.

Observable behaviour is exactly what the diff can't show, so show it,
before and after. The artifact replaces the paragraph; a caption
saying what to look at is all that accompanies it. A sentence
claiming something was verified is telling; attach what was seen.

For a PR in a stack, the opening line says where it sits. When citing
a sibling's merge state, link the PR -- tickets can't be merged.

Process:

1. Identify the current branch and an appropriate base branch, and
   read enough context to say why the change exists and what it
   makes observable.
2. Before writing a word, capture the before and after of what the
   change makes observable, as a file to attach or a block to paste.
3. Draft an outcome-oriented title and the body in two passes: first
   write the why and the consequences around the artifact, then
   compress -- cut every paragraph that tells the reviewer nothing
   beyond the diff and the opening line, and shorten any past three
   sentences. Stop before the cut that would fail the reader test.
4. Create the PR with `--draft`, passing screenshots with `--attach`
   (`gh pr create --help` shows how to place one inside the body).
   If creation fails, leave the user the title, body, and command to
   run.
