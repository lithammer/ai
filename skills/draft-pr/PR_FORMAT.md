# PR Format

Start with a one-sentence `**tl;dr:**` line, then use this heading order for the PR body. `tl;dr`, `Abstract`, and `Solution` are required. The other sections are optional; omit empty sections. Do not hard-wrap paragraphs; rely on the PR UI's soft wrapping.

## Template

```md
**tl;dr:**

### Abstract

### Solution

### Caveats

### Alternatives

### Follow-up

### Resolves
```

## Examples

### Bug fix

```md
**tl;dr:** Invalid tokens now stop the sync retry loop and send the account through re-auth.

### Abstract

Before, sync treated an invalid token like a retryable network failure. A 401 could leave the account stuck in pending sync, because the UI kept showing progress while background retries kept failing.

### Solution

Now, token rejection is treated as an auth failure. Sync stops retrying that account and routes it through the existing re-auth path, while transient transport failures still use the normal retry path.

### Caveats

This makes invalid-token failures visible sooner instead of hiding them behind background retries.

### Follow-up

A follow-up PR will add a richer account-health message once the settings page has a shared error-state component.

### Resolves

- GH-123
- [AB-1337](https://jira.example.com/browse/AB-1337)
```

### Data-flow change

```md
**tl;dr:** Large file uploads no longer pass through the API; clients upload directly to object storage using short-lived pre-signed URLs.

### Abstract

Before, uploading a file meant POSTing it to the API, which then forwarded the bytes to object storage. A typical request looked like `POST /uploads  Content-Type: multipart/form-data  [file bytes]`. The API worker stayed pinned for the full upload duration, and the service paid bandwidth twice -- once on ingress from the client, once on egress to storage.

### Solution

Now, the API hands out short-lived pre-signed PUT URLs and the client uploads each file directly to object storage. File bytes no longer pass through the API. The API still authorizes the request, allocates the object keys, and records the upload in the database once the client confirms completion.

### Caveats

Because uploads go client -> object storage, the API no longer sees per-file upload latency or content length in real time. Pre-sign metrics and storage access logs remain available.

### Alternatives

Keeping a multipart upload route on the API would preserve upload telemetry, but it would add bandwidth cost, worker occupancy, and another data path to operate.
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

Even a reader on the same service has to chase four internal names and a library function before they know what kind of change this is. The plain-language paragraph that should have come first -- something like "Cache lookups now run in parallel with a tight deadline, and the request handler no longer waits on misses to refresh" -- has been replaced by a bullet list.

Rule: complete the plain-language `Solution` paragraph first. Bullets and internal names only after a reader could already summarize the change without them.
