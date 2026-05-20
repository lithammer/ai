---
name: draft-pr
description: Create a draft PR for the current branch. Use when asked to draft, create, open, or prepare a PR, or to write a PR description.
---

# Draft PR

## Intent

Create a draft PR for the current branch. The PR description should help
reviewers understand why the change exists and why the solution is
acceptable. It is not a changelog.

## Process

1. Identify the current branch, an appropriate base branch, and the
   branch delta.
2. Read enough touched code, tests, docs, commits, and conversation
   context to understand intent and implementation.
3. Draft an outcome-oriented title.
4. Draft the body following the writing rules below; see
   [EXAMPLES.md](./EXAMPLES.md) for shapes.
5. Create the PR as a draft. If PR creation cannot be completed, leave
   the user with the title, body, and exact command to run.

## Writing rules

- Start with a bold `**tl;dr:**` line: one sentence summarizing the
  outcome for skim readers. The `tl;dr` is the description; every other
  section is optional, added only when it carries information the
  `tl;dr` can't. If you'd be restating the `tl;dr` in different words,
  drop the section.
- Heading order when sections are present: `tl;dr`, `Abstract`,
  `Solution`, `Caveats`, `Alternatives`, `Follow-up`, `Resolves`.
- `Abstract`: add when the reviewer needs problem context that doesn't
  fit in `tl;dr` (a non-obvious bug, a chain of events that produced a
  failure). Describe the bug, failure mode, or user outcome; include
  only the smallest useful log output or traceback.
- `Solution`: add when the *how* is genuinely load-bearing for review
  (a data-flow shift, an architectural pivot, a surprising design
  choice). Explain why and how the implementation solves the problem
  or enables the feature; prefer design-level explanation over
  file-by-file detail.
- First paragraph of `Solution` is plain-language mental model. Bullets
  and specifics come after.
- `Caveats`: include meaningful limitations, risks, constraints, or
  trade-offs.
- `Alternatives`: include discarded approaches only when they help
  reviewers understand the chosen solution.
- `Follow-up`: include planned or expected next PRs only. Omit
  speculative wishlist or rainy-day ideas.
- `Resolves`: include only issue tracker IDs or links that reviewers
  can access. Omit local-only references such as Beads tasks or private
  tracker IDs. Do not invent references.
- For PRs in a series, make `tl;dr` self-locating by naming the role
  this PR plays in the chain ("the publisher side of ...", "the infra
  prerequisite for ..."). Avoid timing claims about siblings ("now that
  X is provisioned") -- siblings often sit open in parallel.
- Lead `Abstract` with the user-visible problem or change, not a
  ticket or peer-PR reference. Cross-references must carry
  load-bearing context (e.g. "#NNN added the flag we're now
  removing"); link the PR rather than the tracking ticket when the
  claim is about merge state -- tickets can't be merged.
- Pure positioning ("part of epic Y") goes in `Resolves` or
  `Follow-up`, not `Abstract`.
- Skip process narrative ("X asked us to split this up", "discussed in
  Slack on Tuesday") -- who requested the PR or why work was split goes
  in PR comments or chat, not the description.
- Within a section, use prose for one point and bullets for multiple
  distinct points. `Resolves` is always a bullet list.
- Do not hard-wrap paragraphs; rely on the PR UI's soft wrapping. Keep
  bullets on one line unless they become unreadable.
- Avoid detailed inventories, commit summaries, and file-by-file lists
  such as "this changed X, Y, and Z."
- Match description weight to change weight. For mostly-mechanical PRs
  (dependency bumps, code-mod sweeps, lint auto-fix runs), name the
  bulk operation in the `tl;dr` and reserve any body for the sites
  that took judgment (manual cleanups, suppressions kept, places the
  auto-fix wasn't safe).

## Language tricks

- **Before / now / why**
  - Prefer: "Before, file bytes were POSTed through the API, which
    forwarded them to object storage. Now, the client uploads directly
    using a pre-signed URL. This avoids paying for bandwidth twice and
    frees the API worker for the duration of the transfer."
- **Impact before mechanism**
  - Avoid: "This PR introduces enhanced token handling."
  - Prefer: "Invalid tokens now stop the sync retry loop and send the
    account through re-auth."
- **Concrete example for abstract problems**
  - Prefer: "The old request looked like `POST /uploads  Content-Type:
    multipart/form-data  [file bytes]`, so even small uploads pinned
    an API worker for the full transfer duration."
- **No sales pitch words**
  - Avoid: "seamless," "robust," "comprehensive," "leverages," and
    "streamlined" unless they are technically precise.

## Checks

Before creating the PR, verify:

- The current branch is not the base branch.
- The base branch is correct.
- The PR body starts with a `**tl;dr:**` line and follows the writing
  rules above.
- **Reader test:** at every paragraph, a senior engineer who doesn't
  work on this system should be able to follow what's being said.
  Internal function names, jargon for code paths, and implementation
  details (goroutines, timeouts, locking primitives) are red flags --
  describe the contract that's now exposed, not the mechanism behind
  it. The opening (`tl;dr` plus the first paragraph of `Solution`) is
  the strictest case: the outsider should be able to explain the whole
  change back in one sentence after reading just those.
- The PR is created with `--draft`.
