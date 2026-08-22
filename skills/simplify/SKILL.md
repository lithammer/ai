---
name: simplify
description: Clean up changed code without changing behavior — review it for reuse, simplification, efficiency, and altitude, then apply the fixes. Quality only; it does not hunt for correctness bugs.
argument-hint: "[target]"
---

# Simplify

Improve the quality of the changed code. Review it for reuse, simplification,
efficiency, and altitude issues, then fix what you find. Do not look for
correctness bugs — that is a dedicated review pass, not this one.

## Phase 0 — Gather the diff

Run `git diff @{upstream}...HEAD` to get the diff under review. Without an
upstream, diff against the merge-base with the default branch, detected
dynamically (e.g. `git symbolic-ref refs/remotes/origin/HEAD`), and fall back
to `git diff HEAD~1`. If that range is empty or there are uncommitted changes,
also run `git diff HEAD` and include the working tree — this often runs before
the commit. If the invocation names a target — a PR, a branch, a path — review
that instead. Treat this diff as the review scope.

## Phase 1 — Review (four cleanup angles)

Spawn one subagent per angle below, each given the diff and its own angle.
Run them in parallel if the harness supports it; otherwise serialize. If the
harness has no subagents, work through all four angles yourself in one pass —
do not drop an angle for lack of fan-out — and say so in the summary, so the
reader isn't misled about what ran.

Each angle returns its findings with `file`, `line`, a one-line `summary`, and
the concrete cost: what is duplicated, wasted, or made harder to maintain.

### Reuse

Flag new code that re-implements something the codebase already has — search
shared and utility modules and the files adjacent to the change, and name the
existing helper to call instead.

### Simplification

Flag unnecessary complexity the diff adds: redundant or derivable state,
copy-paste with slight variation, deep nesting, dead code left behind. Name
the simpler form that does the same job.

### Efficiency

Flag wasted work the diff introduces: redundant computation or repeated I/O,
independent operations run sequentially, blocking work added to startup or hot
paths. Also flag long-lived objects built from closures or captured
environments — they keep the entire enclosing scope alive for the object's
lifetime (a memory leak when that scope holds large values); prefer a class or
struct that copies only the fields it needs. Name the cheaper alternative.

### Altitude

Check that each change is implemented at the right depth, not as a fragile
bandaid. Special cases layered on shared infrastructure are a sign the fix
isn't deep enough — prefer generalizing the underlying mechanism over adding
special cases.

## Phase 2 — Apply the fixes

Wait for all four angles to report, dedup findings that point at the same line
or mechanism, and fix each remaining one directly. Skip any finding whose fix
would change intended behavior, require changes well outside the reviewed
diff, or that you judge to be a false positive — note the skip rather than
arguing with it. Run the relevant existing checks once the fixes are in.
Finish with a brief summary of what was fixed and what was skipped (or confirm
the code was already clean).
