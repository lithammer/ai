# Reviewer Report Format

If there are no findings, return an empty `<findings></findings>`.

## Schema

```xml
<findings>
  <finding>
    <file>path/to/file</file>
    <lines>42-48</lines>
    <severity>high</severity>
    <description>Short description of the issue.</description>
    <evidence>
      Why this is a real problem: triggering conditions, observed
      behavior, expected behavior. Optional but strongly preferred when
      the finding is non-obvious.
    </evidence>
    <suggestion>
      Concrete fix or actionable instruction. Code may sit here raw,
      no escaping:
      ```go
      if err != nil { return fmt.Errorf("failed: %w", err) }
      ```
    </suggestion>
    <!-- plus axis | category | rule where the reviewer's persona calls for it -->
  </finding>
</findings>
```

### Required elements

- `file` — path relative to the repo root.
- `lines` — single line (`42`) or range (`42-48`).
- `severity` — one of `critical`, `high`, `medium`, `low`.
- `description` — short, plain-language summary of the issue.
- `suggestion` — concrete fix the orchestrator can apply or quote to the
  user.

### Optional elements

- `evidence` — for findings where the description is not self-evidently
  serious: the attack scenario, the input that triggers the bug, the race
  window, the canonical replacement, etc. Strongly preferred for
  `runtime-bugs`, `security`, and `canonical-solutions`-axis findings.
- `axis` — merged reviewers only (`code-quality`, `runtime-bugs`): which
  sub-axis the finding belongs to. The reviewer's persona lists the valid
  values.
- `category` — `test-coverage` reviewer only: `missing-coverage` or
  `test-quality`.
- `rule` — `project-rules` reviewer only: the project rule being violated
  (quote or paraphrase from REVIEW.md / CLAUDE.md).

Omit an optional element entirely when it does not apply — do not emit an
empty tag.

## Merged reviewers: axis accountability

Merged reviewers (`code-quality`, `runtime-bugs`) review multiple
sub-axes in one pass. They must end every response, after the
`</findings>` block, with a one-line summary of what they considered on
each axis, even when no findings were produced. Example:

```
Axes reviewed: readability (2 findings), canonical-solutions (0),
style-and-hygiene (1).
```

If an axis was skipped because its preconditions don't hold (e.g., no
concurrent access patterns in the changed code), say so on the same
line. The orchestrator uses this summary to confirm every axis got
attention.

## Severity

Severity is per-dimension, not cross-dimension. A `high` correctness
finding and a `high` style finding both mean "the most serious thing my
dimension produces on this change" — they are not directly comparable. Use
the full range within your own scope; do not cap a dimension at `low`
because it can never produce a runtime crash.
