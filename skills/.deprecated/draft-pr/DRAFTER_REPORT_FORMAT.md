# Drafter Report Format

Return one `<report>` element. The main session reads it to relay the
PR and to check the claims it could not know you would make, so carry
only what it cannot read from GitHub or git.

The `status` attribute is `created` or `not-created`.

## Status: `created`

```xml
<report status="created">
  <url>https://github.com/owner/repo/pull/123</url>
  <inferred>
    <claim>A body sentence, and what it was deduced from.</claim>
  </inferred>
</report>
```

`inferred` holds every sentence in the body that rests on your reading
rather than on a source: a reason deduced from the diff, a consequence
expected but not observed. The main session verifies each one and
corrects the body where it is wrong. Return an empty element when
every sentence has a source.

## Status: `not-created`

`gh pr create` failed or could not run. Return what the main session
needs to create the PR itself.

```xml
<report status="not-created">
  <reason>The error, in one line.</reason>
  <title>...</title>
  <body>...</body>
  <command>The gh pr create command, --attach flags included.</command>
  <inferred>
    <claim>...</claim>
  </inferred>
</report>
```
