---
name: draft-pr
description: Create a draft PR for the current branch. Use when asked to draft, create, open, or prepare a PR, or to write a PR description.
---

# Draft PR

A PR description helps reviewers understand why the change exists and
why the solution is acceptable. Start with a bold `**tl;dr:**` line:
one sentence summarizing the outcome. Most PRs need nothing more.
Other sections are the exception, added one at a time only when they
carry something the diff doesn't already show -- never to restate it.
Write for a skimmer: a body that reads like an essay gets skipped,
not read. Keep every paragraph to three sentences or fewer, and
treat a body creeping past a dozen lines as a signal to cut.

Optional sections, in heading order: `Abstract`, `Solution`,
`Caveats`, `Alternatives`, `Follow-up`, `Resolves`.

Reader test: a senior engineer who doesn't work on this system should
be able to follow every paragraph and explain the change back in one
sentence after reading the `tl;dr` plus the first paragraph. Describe
what shipped, at the level of the contract -- not the mechanism behind
it. Reviewers see the diff; explain *why* and *consequences*, not
*what changed*. Internal function names, SDK quirks, concurrency
primitives, process narrative ("X asked us to split this up"), and
things you considered but didn't do (deferred refactors, dropped
scope) belong in code, PR threads, or follow-up issues, not the
description.

For PRs in a series, make the `tl;dr` self-locating ("publisher side
of ...", "infra prerequisite for ..."). When citing a sibling's merge
state, link the PR -- tickets can't be merged.

## Examples

Most PRs need nothing past the `tl;dr`:

```md
**tl;dr:** Bump `eslint-plugin-react` from 7.34 to 7.36 and accept the auto-fix output.
```

When a few load-bearing notes aren't visible in the diff (what didn't
get auto-fixed, what got skipped on purpose), add `Caveats` -- and
nothing else:

```md
**tl;dr:** Run `gofmt -s` across the tree to apply the new Go 1.24 simplifications, with two manual follow-ups where the rewrite would have changed behaviour.

### Caveats

- One `//nolint` retained where the rewrite would lose runtime type information.
- The simplifier is intentionally not run on generated files.
```

### Anti-pattern: mechanics ahead of mental model

Opening `Solution` with a one-line summary followed by a bulleted
enumeration of mechanics:

```
Move the cache layer out of the request hot path.

- decodes the incoming `X-Cache-Key` header against the new `cacheKeyV2` schema, falling back to legacy on mismatch;
- batches reads through `redisPipeliner.MGet` with a bounded errgroup (8 parallel, 200ms deadline);
- emits cache hits/misses to the existing `cache_v2_outcome` histogram with `tier=hot`;
- evicts entries that fail the `staleness_window` check before returning.
```

Even a reader on the same service has to chase four internal names and
a library function before they know what kind of change this is. The
plain-language paragraph that should have come first -- something like
"Cache lookups now run in parallel, and the request handler no longer
waits on misses to refresh" -- has been replaced by a bullet list.
Complete the plain-language `Solution` paragraph first; bullets and
internal names only after a reader could already summarize the change
without them.

## Process

1. Identify the current branch and an appropriate base branch.
2. Read enough context to understand intent and implementation.
3. Draft an outcome-oriented title. Draft the body in two passes:
   first cover the goal, then compress. For each paragraph in pass
   two, ask: does this tell the reviewer anything beyond the diff
   and `tl;dr`? If not, cut. Shorten any paragraph past three
   sentences. Simplify language as you go. Stop when further
   compression would lose load-bearing information.
4. Create the PR as a draft. If creation fails, leave the user with
   the title, body, and command to run.

## Checks

- Body starts with `**tl;dr:**`.
- No paragraph over three sentences.
- Reader test passes.
- PR is created with `--draft`.
