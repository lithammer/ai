# Implementor Report Format

Write the full report to a unique file in shared temporary storage; return only its absolute path and a one-line verdict (`complete` or `plan-gap`). The orchestrator reads the file with Read before acting on it.

Write one report per increment as a single `<report>` element. The
orchestrator reads it to decide what to commit and what to flag — so report
only what `git` cannot show. Do not list created/modified/deleted files or
describe the tests you added; the diff already does that.

The `status` attribute is `complete` or `plan-gap`.

## Status: `complete`

The increment was built, tested, and is ready for review and commit.

```xml
<report status="complete">
  <tests result="pass">
    The command you ran, and whether anything was skipped, flaky, or left
    uncovered.
  </tests>
  <plan-deviations>
    What you did that the increment scope did not specify, and why. The
    diff shows the change; only you can explain the reason. Empty element
    if none.
  </plan-deviations>
  <findings>
    <finding>
      <file>path/to/file</file>
      <lines>42</lines>
      <description>What you noticed and why it stood out.</description>
    </finding>
  </findings>
</report>
```

### Findings

Observations you have only because you just wrote this code — the kind the
diff cannot show and that would otherwise be lost once you move on. The
most valuable sit in code the reviewers never see: they review only this
increment's changed files, while you also read its callers and neighbors.
These are cheap passing notes, not a review: jot what caught your eye, do
not go hunting. Return an empty `<findings></findings>` if nothing stood
out.

Each `<finding>` carries:

- `file` — path relative to the repo root.
- `lines` — single line or range.
- `description` — the one-line observation and why it stood out.

Deliberately no `severity` and no fix: these are observations for the
orchestrator to route, not review findings to act on.

## Status: `plan-gap`

The increment's scope is missing something needed to proceed. Stop and
return the gap rather than improvising.

```xml
<report status="plan-gap">
  <gap>
    What the plan did not cover. Specific enough that the orchestrator can
    decide whether to expand scope, adjust the increment, or replan.
  </gap>
  <evidence>
    The code path, file, or failing test that exposed the gap.
  </evidence>
  <not-done>
    Anything you started but rolled back, so the orchestrator knows the
    working tree state.
  </not-done>
</report>
```

The orchestrator may re-dispatch after adjusting scope; the iteration cap
is 3 attempts per increment.
