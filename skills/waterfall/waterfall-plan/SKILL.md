---
name: waterfall-plan
description: Detail a chosen design approach into an implementation plan (objective, file manifest, execution order, test strategy), then auto-proceed to waterfall-challenge. Convergent phase of the waterfall flow.
disable-model-invocation: true
---

# Plan

Take the approach chosen in the `waterfall-design` skill and produce a
detailed implementation plan.

This is the convergent phase. The option space has already been exhausted
in design; do not reopen it here. Detail the chosen approach into files,
execution order, and tests. If detailing reveals the approach is wrong,
surface it (Step 2) rather than silently switching.

## Prerequisites

This skill expects an approach to have been selected via the
`waterfall-design` skill. If no chosen approach exists in the
conversation, ask the user what to plan.

## Step 1: Extract the chosen approach

Pull the selected approach from the conversation, including:

- What the approach does and why it was chosen.
- Which files are affected.
- Known trade-offs and risks.

## Step 2: Detail the plan

Expand the approach into a concrete implementation plan:

1. **Objective**: One sentence stating what the feature does.
2. **Approach**: How it will be built, at the level of "which modules
   change and why."
3. **File manifest**: Files to create, modify, or remove, with a one-line
   note per file describing what changes.
4. **Test strategy**: What tests to write and at which level (unit,
   integration, e2e).
5. **Open questions**: Anything unresolved that the challenge phase
   should examine.

If detailing the approach reveals problems not visible at the design
level (e.g. a dependency that makes the approach impractical), note them
clearly. Do not silently switch to a different approach — surface the
issue.

## Step 3: Slice into increments

Structure the plan into shippable increments. Each increment:

- Is a single commit that leaves the codebase in a working state.
- Has a clear purpose describable in a commit message.
- Is independently reviewable — a reviewer can understand it without
  reading the other increments.
- Includes the relevant tests for the behavior it introduces.

Order the increments so each one builds on the last. Prefer:

- Refactoring pre-work first (from the design phase's refactor analysis).
- Infrastructure and types before the code that uses them.
- Core logic before convenience features or edge case handling.
- Tests alongside the code they cover, not in a separate increment.

Present the increments as a numbered list. For each, note which files
change and what the commit message would be. If the whole feature is
small enough for a single commit, say so — do not split for the sake of
splitting.

## Step 4: Present and proceed to challenge

Present the plan to the user, then invoke the `waterfall-challenge` skill
to pressure-test it. Do not wait for approval — the challenge phase is
what validates the plan. The user will approve (or reject) after the
challenge.
