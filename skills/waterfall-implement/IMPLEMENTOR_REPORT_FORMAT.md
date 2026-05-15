# Implementor Report Format

Return one report per increment. Two possible statuses:

## Status: `complete`

The increment was built, tested, and is ready for review and commit.

```md
## Status
complete

## Files
- Created: path/to/new_file.go, path/to/another.go
- Modified: path/to/existing.go
- Deleted: (none, or list paths)

## Tests
- Added: short description per new test or test file.
- Existing test suite result: pass | fail (and which suite/command).

## Plan deviations
- Anything you did that wasn't in the increment scope, and why. Empty if
  none.

## Notes
- Anything the orchestrator should know before committing (e.g. "ran
  `gofmt`", "vendored dependency added"). Empty if none.
```

## Status: `plan-gap`

The increment's scope is missing something needed to proceed. Stop and
return the gap rather than improvising.

```md
## Status
plan-gap

## Gap
What the plan did not cover. Specific enough that the orchestrator can
decide whether to expand scope, adjust the increment, or replan.

## Evidence
The code path, file, or failing test that exposed the gap.

## What I did not do
List anything you started but rolled back, so the orchestrator knows the
working tree state.
```

The orchestrator may re-dispatch after adjusting scope; the iteration cap
is 3 attempts per increment.
