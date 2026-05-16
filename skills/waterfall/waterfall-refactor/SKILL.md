---
name: waterfall-refactor
description: Identify refactoring opportunities in code that a feature will touch. Runs at strategic level during design (looking for structural moves that could change which approach is chosen) or tactical level before implementation (looking for pre-work that gives the feature a better foundation). Primarily invoked by waterfall-design or waterfall-implement; avoid auto-triggering on casual mentions of "refactor".
---

# Refactor

Analyze the codebase for refactoring opportunities relevant to the feature
being built. This is not a general cleanup pass — it focuses on code the
feature touches and asks what changes would give it a better foundation.

The analysis adapts to when it runs. The caller provides a **review
level**:

- **Strategic**: Run during design, before approaches are generated.
  Surface structural opportunities that could influence which approach to
  take. "This service is tangled enough that a rewrite might be the
  better approach" or "these two modules could be merged, which opens up
  a simpler design."
- **Tactical**: Run before implementation, after the plan is approved.
  Surface pre-work and incorporated refactors that make the
  implementation cleaner.

## Step 1: Determine scope

Extract from the conversation:

- The feature being built.
- Which areas of the codebase are involved.
- The review level (strategic or tactical).

If running at the strategic level, the scope is broader — look at the
modules and services the feature touches, not just individual files. If
tactical, focus on the specific files in the plan's manifest.

## Step 2: Analyze

Read the affected code with the feature in mind. The question is not
"what is wrong with this code?" but "will this code give the feature a
good foundation?"

At the **strategic** level, be willing to consider larger moves —
rewrites, merges, eliminations. A refactor that turns the feature from
complex to trivial is worth naming, even if the user ultimately decides
not to take it.

At the **tactical** level, look for smaller moves: pre-work that keeps
the implementation diff clean, or cleanups that fold naturally into the
planned changes.

## Step 3: Classify

For each opportunity:

- **Strategic** level:
  - **Enables new approach**: A refactor that opens up a design option
    that would otherwise be impractical. Note what approach it enables.
  - **Simplifies all approaches**: A refactor that benefits the feature
    regardless of which approach is chosen.
  - **Unrelated**: Not relevant to this feature. Do not include.

- **Tactical** level:
  - **Pre-work**: Do before implementation starts.
  - **Incorporate**: Fold into the implementation alongside planned
    changes.
  - **Skip**: Not relevant to the planned changes. Do not include.

## Step 4: Present

Return the opportunities with file paths, descriptions, and why each
matters for the feature. At the strategic level, explicitly note how
opportunities connect to potential approaches.
