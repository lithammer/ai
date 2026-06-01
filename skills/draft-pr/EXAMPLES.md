# Examples

Most PRs are just the `tl;dr`. Sections are the exception, added one at a time only when they carry something the line can't.

## Most PRs (`tl;dr` only)

When the whole story fits in one line, no other sections are needed:

```md
**tl;dr:** Bump `eslint-plugin-react` from 7.34 to 7.36 and accept the auto-fix output.
```

When a few load-bearing notes aren't visible in the diff (what didn't get auto-fixed, what got skipped on purpose), add `Caveats` -- and nothing else:

```md
**tl;dr:** Run `gofmt -s` across the tree to apply the new Go 1.24 simplifications, with two manual follow-ups where the rewrite would have changed behaviour.

### Caveats

- One `//nolint` retained where the rewrite would lose runtime type information.
- The simplifier is intentionally not run on generated files.
```

## Anti-pattern: mechanics ahead of mental model

Opening `Solution` with a one-line summary followed by a bulleted enumeration of mechanics:

```
Move the cache layer out of the request hot path.

- decodes the incoming `X-Cache-Key` header against the new `cacheKeyV2` schema, falling back to legacy on mismatch;
- batches reads through `redisPipeliner.MGet` with a bounded errgroup (8 parallel, 200ms deadline);
- emits cache hits/misses to the existing `cache_v2_outcome` histogram with `tier=hot`;
- evicts entries that fail the `staleness_window` check before returning.
```

Even a reader on the same service has to chase four internal names and a library function before they know what kind of change this is. The plain-language paragraph that should have come first -- something like "Cache lookups now run in parallel, and the request handler no longer waits on misses to refresh" -- has been replaced by a bullet list.

Rule: complete the plain-language `Solution` paragraph first. Bullets and internal names only after a reader could already summarize the change without them.
