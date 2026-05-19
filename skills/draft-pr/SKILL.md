---
name: draft-pr
description: Create a draft PR for the current branch.
disable-model-invocation: true
---

# Draft PR

## Intent

Create a draft PR for the current branch. The PR description should help
reviewers understand why the change exists and why the solution is acceptable.
It is not a changelog.

## Process

1. Identify the current branch, an appropriate base branch, and the branch delta.
2. Read enough touched code, tests, docs, commits, and conversation context to understand intent and implementation.
3. Draft an outcome-oriented title.
4. Draft the body using [PR_FORMAT.md](./PR_FORMAT.md).
5. Create the PR as a draft. If PR creation cannot be completed, leave the user with the title, body, and exact command to run.

## Writing rules

- Keep the body short and reviewer-useful.
- Use reviewer-oriented language: concrete, direct, and easy to skim.
- Start with a bold `**tl;dr:**` line: one sentence summarizing the outcome for skim readers.
- `Abstract`: describe the bug, failure mode, feature, capability, or user outcome. Include only the smallest useful log output or traceback.
- `Solution`: explain why and how the implementation solves the problem or enables the feature. Prefer design-level explanation over file-by-file detail.
- The first paragraph of `Solution` is plain-language mental model only -- no bullets, unexplained internal API names, library function names, or dense infra mechanics. Use only the system names needed to explain the shape of the change. Bullets and specifics come after the reader has that shape.
- `Caveats`: include meaningful limitations, risks, constraints, or trade-offs.
- `Alternatives`: include discarded approaches only when they help reviewers understand the chosen solution.
- `Follow-up`: include planned or expected next PRs only. Omit speculative wishlist or rainy-day ideas.
- `Resolves`: include only issue tracker IDs or links that reviewers can access. Omit local-only references such as Beads tasks or private tracker IDs. Do not invent references.
- When the PR is one in a series fulfilling a larger epic, make `tl;dr` self-locating by naming the role this PR plays in the chain ("the publisher side of ...", "the infra prerequisite for ...", "the scaffold-flag removal for ...").
- Avoid timing claims about sibling PRs ("now that X is provisioned") -- siblings in a series often sit open in parallel, and a state claim can be wrong by the time a reviewer reads it.
- Lead `Abstract` with the user-visible problem or change, not a ticket or peer-PR reference. Cross-references belong in `Abstract` only when they carry load-bearing context (e.g. "SS-XXX added the flag we're now removing"). Pure positioning ("part of epic Y") goes in `Resolves` or `Follow-up`.
- Omit optional sections when there is nothing meaningful to say.
- Within a section, use prose for one point and bullets for multiple distinct points. `Resolves` is always a bullet list.
- Do not hard-wrap paragraphs; rely on the PR UI's soft wrapping. Keep bullets on one line unless they become unreadable.
- Avoid detailed inventories, commit summaries, and file-by-file lists such as "this changed X, Y, and Z."
- Match description weight to change weight. For PRs that are mostly mechanical -- dependency bumps, code-mod sweeps, lint auto-fixes, generated-file regeneration -- name the bulk operation in one sentence and reserve narrative density for the small set of sites that required judgment (manual cleanups, suppressions kept, places the auto-fix wasn't safe). A "ran the new auto-fixes plus three manual follow-ups" PR should read like that, not like an architectural change. For purely mechanical PRs with no judgment calls worth narrating, the `tl;dr` alone may be the whole description -- `Abstract` and `Solution` are not required (see [PR_FORMAT.md](./PR_FORMAT.md)).

## Language tricks

- **Mental model before mechanics**
  - Avoid: "Issues N per-file pre-signed PUT URLs in parallel via a bounded errgroup."
  - Prefer: "The API hands out short-lived upload permissions, and the client uploads files directly to object storage."
- **Before / now / why**
  - Prefer: "Before, file bytes were POSTed through the API, which forwarded them to object storage. Now, the client uploads directly using a pre-signed URL. This avoids paying for bandwidth twice and frees the API worker for the duration of the transfer."
- **Impact before mechanism**
  - Avoid: "This PR introduces enhanced token handling."
  - Prefer: "Invalid tokens now stop the sync retry loop and send the account through re-auth."
- **Concrete nouns over vague abstractions**
  - Avoid: "Improves reliability."
  - Prefer: "Prevents the account from staying stuck in pending sync."
- **Concrete example for abstract problems**
  - Prefer: "The old request looked like `POST /uploads  Content-Type: multipart/form-data  [file bytes]`, so even small uploads pinned an API worker for the full transfer duration."
- **Cause/effect sentences**
  - Prefer: "When the server rejects the token, sync treats it as an auth failure instead of a retryable network failure."
- **No sales pitch words**
  - Avoid: "seamless," "robust," "comprehensive," "leverages," and "streamlined" unless they are technically precise.
- **Assume reviewer competence**
  - Avoid explaining basic concepts; explain why this change took this shape.

## Checks

Before creating the PR, verify:

- The current branch is not the base branch.
- The base branch is correct.
- The PR body follows [PR_FORMAT.md](./PR_FORMAT.md), including the required `**tl;dr:**` line.
- **Reader test:** reread `tl;dr` plus the first paragraph of `Solution`. A senior engineer who doesn't work on this system should be able to explain the change back in one sentence after reading just those two. If not, rewrite before adding mechanics. Dense bullets, internal names, and acronyms before the mental model are the failure mode this catches.
- The PR is created with `--draft`.
