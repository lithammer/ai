---
name: waterfall-implement
description: Implement a planned and challenged feature by delegating each increment to a subagent, then running a review-fix loop until the code is clean. The orchestrator stays in oversight mode; building happens in fresh subagent contexts. Use after a plan has been designed, planned, challenged, and approved; or when the user says "implement the plan" / mentions waterfall-implement.
disable-model-invocation: true
---

# Implement

The plan has been drafted, challenged, and approved. Delegate implementation
to a subagent, then orchestrate a review-fix loop until the code is clean.

## Prerequisites

This skill expects a plan that has been:

1. Designed via the `waterfall-design` skill and detailed via the
   `waterfall-plan` skill.
2. Challenged via the `waterfall-challenge` skill.
3. Approved by the user.

If no approved plan exists in the conversation, ask the user what to
implement.

It also expects a clean working tree. Run `git status` before Step 3; if
uncommitted changes exist, stop and ask the user to commit, stash, or
discard them. Per-increment commits assume the tree is clean so unrelated
changes do not get swept into the increment's commit.

## Step 1: Extract the plan

Pull the final, approved plan from the conversation, including any
revisions made during the challenge phase. Identify:

- The execution order (which changes to make, in what sequence).
- The file manifest (what to create, what to modify).
- The test strategy.
- Any surviving risks to keep in mind.

## Step 2: Identify refactoring opportunities

Run the `waterfall-refactor` skill at the **tactical** level. This
identifies code that should be cleaned up before or during implementation
to give the feature a better foundation.

Pass any **pre-work** refactors to the subagent as a first step before the
planned changes. Pass **incorporated** refactors alongside the relevant
plan steps.

## Step 3: Delegate implementation

Build the feature one increment at a time, following the plan's increment
list. For each increment, spawn a subagent. Pass it
[IMPLEMENTOR_BRIEF.md](./IMPLEMENTOR_BRIEF.md) as its persona and
[IMPLEMENTOR_REPORT_FORMAT.md](./IMPLEMENTOR_REPORT_FORMAT.md) as its
output specification.

Send it as initial input:

- The increment's scope (which files change, what behavior to add, the
  commit message it will ship under).
- Any pre-work refactors from Step 2 that apply to this increment.
- Key codebase context: relevant file paths, patterns, conventions.

The orchestrator delegates rather than building directly so it can retain
broader context — the plan, surviving risks from challenge, the
operating-context summary — for the review-fix loop that follows. The
implementor's narrow context keeps it focused on the increment without
scope creep; the orchestrator keeps the bigger picture for triage and
oversight. This separation holds regardless of model choice.

If the harness supports per-subagent model selection, also prefer a
cheaper model for the implementor (e.g., Sonnet) and keep the
orchestrator on a stronger one (e.g., Opus): implementation is execution;
the strategic work already happened in design, plan, and challenge.

The subagent makes the changes, writes tests, runs the suite, and returns
a structured report. After it returns and tests pass, **commit the
increment** using the planned commit message. Then move to the next
increment.

If the plan is a single increment, treat it as one commit.

### Iteration cap

The implementor may return a plan gap (status `plan-gap`) instead of a
completed increment. If you re-dispatch after adjusting scope or context,
cap at 3 attempts per increment. After 3 returns with gaps, stop and
surface the issue to the user — do not keep re-dispatching in an attempt
to bridge the gap without their input.

## Step 4: Review

After the subagent returns, follow the `waterfall-review` skill on the
files changed during this increment:

1. Determine what to review (the changed files).
2. Determine the operating context.
3. Select and dispatch relevant reviewers in parallel.
4. Triage findings: Fix / Judgement call / Dismiss.
5. Deduplicate.

Do NOT present findings to the user yet. First, handle fixes.

## Step 5: Fix confirmed issues

For findings classified as **Fix** (verified, clearly correct):

- Apply the fix yourself. These are issues the reviewers confirmed with
  evidence — bugs, leaked secrets, dead code, wrong boundary checks.
- After applying all fixes, run the test suite again to confirm nothing
  broke.

For findings classified as **Judgement call**:

- Collect them for the user. Do not apply or dismiss these on your own.

## Step 6: Re-review if needed

If you applied any fixes in Step 5, re-run Step 4 on the affected files
only. Repeat Steps 4-6 until a review round produces no new Fix findings.

Cap at 3 review rounds. If issues persist after 3 rounds, include the
remaining findings in the report for the user.

## Step 7: Present results

Summarize for the user:

1. **What was built**: Files created/modified, tests written, plan
   deviations.
2. **Review findings**: What was found, what was auto-fixed, what was
   dismissed.
3. **Judgement calls**: Present each one with the reviewer's reasoning,
   the relevant code, and why you are unsure. Ask the user "Fix it",
   "Ignore", or let them provide direction. Batch related calls (2-4 at a
   time).
4. **Remaining issues**: Anything that persisted after 3 review rounds.

End with a one-line count: "N findings across M files (K auto-fixed, J
dismissed, L for user review)."
