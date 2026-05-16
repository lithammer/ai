---
name: waterfall-design
description: Generate a range of approaches for a feature — from incremental to structural — with adversarial review before presenting. Divergent phase of the waterfall flow.
disable-model-invocation: true
---

# Design

Given a feature request, deeply explore the codebase, critically evaluate
the existing structure, and generate a range of approaches — from
incremental to structural. The challenger reviews the approaches before
they are presented to the user.

This is the divergent phase. Do not converge on a solution yet. The goal is
to exhaust the option space so the user can make an informed choice.

Detailed planning is the comfortable escape — it feels productive and
sidesteps the harder strategic question of whether the structure is even
right. That question belongs here, not in `waterfall-plan`. If you find
yourself sketching the implementation, stop and go back to the option
space.

## Step 1: Understand the feature

Read the feature description provided by the user. If critical details are
missing, ask the user — but prefer answering questions yourself by
exploring the codebase. Do not ask about things you can discover by
reading code.

## Step 2: Explore and evaluate

Explore the codebase to understand:

- Where the feature would live (existing modules, packages, directories).
- What existing code it touches or depends on.
- What patterns and conventions the codebase follows.
- What constraints exist (APIs, data models, config, tests).

Spend real effort here. A design built on assumptions about code you did
not read is worthless.

**Do not just map the code — evaluate it.** As you explore, ask:

- Is the existing structure the right foundation for this feature, or is
  it working around a previous limitation?
- Are there services, layers, or abstractions that exist for historical
  reasons but no longer earn their complexity?
- Would a different structure make this feature (and future work)
  simpler?
- What would you build if you were starting from scratch with today's
  requirements? How far is the current code from that?

The existing code is not sacred. It was written by someone making their
best decision at the time, possibly under different constraints than you
have now.

## Step 3: Identify refactoring opportunities

Invoke the `waterfall-refactor` skill at the **strategic** level. Send it
the feature description and the areas of the codebase involved.

This surfaces structural opportunities — rewrites, merges, eliminations —
that could influence which approach to take. Feed the results into
approach generation: if a refactor enables a cleaner design, it should
appear as part of an approach, not as a footnote.

## Step 4: Generate approaches

Generate a range of approaches. For each, describe:

- The approach in 2-3 sentences.
- Which files to create, modify, or remove.
- Trade-offs: what it makes easy, what it makes hard, what risks it
  carries.
- Scope: rough sense of how much changes (small/medium/large).

When naming approaches, identify the algorithmic class (graph traversal,
dynamic programming, bipartite matching, etc.), pattern family (event
sourcing, state machine, finite automaton, etc.), or domain-modeling
concept (aggregate, bounded context, anti-corruption layer, etc.) when
one applies. Domain-modeling concepts apply most when the codebase has
rich domain logic, not CRUD or infrastructure glue. If an approach is
bespoke for a problem class that has known solutions, justify the bespoke
choice. Do not force a pattern where none fits, but do not reinvent one
either.

**The approaches must span the spectrum:**

- **Incremental**: Fit the feature into the existing structure with
  minimal changes. Describe what compromises this requires and what debt
  it adds.
- **Refactor-first**: Restructure the relevant code to properly
  accommodate the feature, then build it on the improved foundation.
  Describe what the refactor unlocks beyond this feature.
- **Structural** (when applicable): Challenge whether the existing
  components are the right ones. Could services be merged, split, or
  replaced? Could a layer be eliminated? Describe what this makes
  possible that the other approaches cannot.

Do not pad with straw-man alternatives. Each approach must be genuinely
viable. If a structural approach does not apply (the existing code is
well-suited), say so explicitly and explain why — do not skip the
question.

Bigger scope is not automatically worse. A rewrite that simplifies three
future features may be cheaper than three incremental hacks. Present
scope as a trade-off, not a disqualification.

## Step 5: Challenge the approaches

Invoke the `waterfall-challenge` skill. It will detect strategic mode from
the conversation (approaches present, no detailed plan) and run the
adversarial review against the approach list, returning revised approaches
and resolved or open branches.

When the challenge flow returns, incorporate any revisions into the
approach list before Step 6.

## Step 6: Present and recommend

Present all approaches (including any added or revised during the
challenge) with a clear recommendation. State which approach you
recommend and why, but make the case for the others too — the user may
have context you do not.

Ask the user to pick an approach (or propose their own). **Stop and wait
for a response.** Do not proceed to detailed planning until the user has
chosen.

The next phase is the `waterfall-plan` skill, which will detail the
chosen approach into an implementation plan.
