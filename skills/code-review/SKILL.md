---
name: code-review
description: Review changed code for correctness bugs and instruction-file violations, verify each candidate, and report the survivors without editing. Use when asked to review a diff, branch, or PR for bugs. Not for cleanup; that is simplify.
argument-hint: "[target]"
---

# Code Review

You are reviewing for **recall**: catch every real bug. At this level,
catching real bugs matters more than avoiding false positives — a missed bug
ships. Err on the side of surfacing. Cleanup belongs to `simplify`; this
review reports findings and leaves the code as it is.

## Phase 0 — Gather the diff

Run `git diff @{upstream}...HEAD` to get the diff under review. Without an
upstream, diff against the merge-base with the default branch, detected
dynamically (e.g. `git symbolic-ref refs/remotes/origin/HEAD`), and fall back
to `git diff HEAD~1`. If that range is empty or there are uncommitted changes,
also run `git diff HEAD` and include the working tree — this often runs before
the commit. If the invocation names a target — a PR, a branch, a path — review
that instead. Treat this diff as the review scope.

## Phase 1 — Find candidates (5 correctness angles + 1 conventions angle, up to 8 each)

Spawn one subagent per angle below, each given the diff and its own angle.
Run them in parallel if the harness supports it; otherwise serialize. If the
harness has no subagents, perform each angle, verification, and the sweep
yourself, sequentially, in this context, and say so in the summary, so the
reader isn't misled about what ran.

Release each reviewer once its report is in, and every reviewer this run
started if the run stops or fails; leave other agents alone.

Each angle surfaces **up to 8 candidate findings** with `file`, `line`, a
one-line `summary`, and a concrete `failure_scenario`. Do NOT let one angle's
conclusions suppress another's — if two angles flag the same line for
different reasons, record both.

### Angle A — line-by-line diff scan

Read every hunk in the diff, line by line. Then read the enclosing function for
each hunk — bugs in unchanged lines of a touched function are in scope (the PR
re-exposes or fails to fix them). For every line ask: what input, state, timing,
or platform makes this line wrong? Look for inverted/wrong conditions,
off-by-one, null/undefined deref, missing `await`, falsy-zero checks,
wrong-variable copy-paste, error swallowed in catch, unescaped regex metachars.

### Angle B — removed-behavior auditor

For every line the diff DELETES or replaces, name the invariant or behavior it
enforced, then search the new code for where that invariant is re-established.
If you can't find it, that's a candidate: a removed guard, a dropped error
path, a narrowed validation, a deleted test that was covering a real case.

### Angle C — cross-file tracer

For each function the diff changes, find its callers (search for the symbol)
and check whether the change breaks any call site: a new precondition, a
changed return shape, a new exception, a timing/ordering dependency. Also check
callees: does a parallel change in the same PR make a call unsafe?

### Angle D — language-pitfall specialist

Scan for the classic pitfalls of the diff's language/framework — for example:
JS falsy-zero, `==` coercion, closure-captured loop var; Python mutable default
args, late-binding closures; Go nil-map write, range-var capture; SQL injection;
timezone/DST drift; float equality. Flag any instance the diff introduces.

### Angle E — wrapper/proxy correctness

When the PR adds or modifies a type that wraps another (cache, proxy, decorator,
adapter): check that every method routes to the wrapped instance and not back
through a registry/session/global — e.g. a caching provider holding a
`delegate` field that resolves IDs via `session.get(...)` instead of
`delegate.get(...)` will re-enter the cache or recurse. Also check that the
wrapper forwards all the methods the callers actually use.

### Conventions

Find the instruction files (`AGENTS.md`, `CLAUDE.md`) that govern the changed
code: user-level and repo-root, plus any in a directory that is an ancestor of
a changed file (a directory's file only applies to files at or below it). Read
each one that exists, then check the diff for clear violations of the rules
they state.

Only flag a violation when you can quote the exact rule and the exact line
that breaks it — no style preferences, no vague "spirit of the doc"
inferences. In the finding, name the file's path and quote the rule so the
report can cite it. If no instruction file applies, return nothing for this
angle.

Conventions candidates use the same `file`/`line`/`summary` shape; in
`failure_scenario`, name the instruction file and the rule that is broken
instead of a crash. Correctness bugs always outrank conventions findings when
the output cap forces a cut.

## Phase 2 — Verify (1-vote, 3-state)

Dedup candidates that point at the same line/mechanism, keeping the one with
the most concrete failure scenario. For each remaining candidate, spawn **one
verifier**: give it the diff, the relevant file(s), and the candidate, and have
it return exactly one of:

- **CONFIRMED** — can name the inputs/state that trigger it and the wrong
  output or crash. Quote the line.
- **PLAUSIBLE** — mechanism is real, trigger is uncertain (timing, env,
  config). State what would confirm it.
- **REFUTED** — factually wrong (code doesn't say that) or guarded elsewhere.
  Quote the line that proves it.

Keep candidates where the vote is CONFIRMED or PLAUSIBLE. This is recall mode —
a single non-REFUTED vote carries the finding. Do NOT drop on uncertainty.

## Phase 3 — Sweep for gaps

Spawn **one more finder** as a fresh reviewer who has the verified list.
Re-read the diff and enclosing functions looking ONLY for defects not already
listed. Do not re-derive or re-confirm anything already there — the job is
gaps. Focus on what the first pass tends to miss: moved/extracted code that
dropped a guard or anchor; second-tier footguns (dataclass default evaluated
once, `hash()` non-determinism, lock-scope shrink, predicate methods with side
effects); setup/teardown asymmetry in tests; config defaults flipped.

Surface **up to 8 additional candidates**, each naming a defect not already on
the list. If nothing new, return an empty sweep — do not pad.

## Output

Report at most 15 findings, ranked most-severe first. Give each its
`file:line`, a one-sentence `summary`, the `failure_scenario` (concrete
inputs/state → wrong output/crash), and its verdict. If more than 15 survive,
keep the 15 most severe. If nothing survives verification, say so.
