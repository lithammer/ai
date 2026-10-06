---
name: refactor
description: Find structural refactors that remove caller obligations, then implement the chosen change.
disable-model-invocation: true
argument-hint: "[scope or concern]"
---

# Refactor

Explore existing code for structural changes that remove obligations from
callers. No feature or diff is needed.

## 1. Scope

Read the repository's instructions and the requested scope or concern: a
path, subsystem, or goal such as making invalid checkout states
unrepresentable. With no target, map the repository's major subsystems and
choose promising areas to inspect.

## 2. Discover

Use a single agent by default. Apply these related questions in one pass;
they overlap and are not separate work queues. Split a large scope only
along genuinely independent subsystems.

- **Representation:** which units, identities, states, or operations rely
  on primitives, flags, naming, or caller discipline?
- **Derivability:** which stored or passed values could be derived from
  authoritative state instead of kept in sync?
- **Invariant ownership:** which rules do callers repeatedly enforce that
  one owning module or storage constraint could guarantee?
- **Lifecycle ownership:** which acquire/release or transaction protocols
  could a scoped operation own instead of each caller?
- **Least capability:** which callers receive authority they do not need?
- **Altitude:** which special cases compensate for limitations in the
  underlying mechanism? Where should the rule live?
- **Deep modules:** which repeated orchestration could sit behind an
  interface that hides knowledge callers currently need?

## 3. Substantiate

Read each promising implementation and its callers in full, with the tests
and contracts needed to judge the change. Trace the burden or possible
misuse to concrete code. A candidate needs a present cost or credible
failure mode; an observed bug is not required.

Describe the replacement and check which guarantees it actually enforces,
and which still need validation or tests. Distinguish tighter internal
representations from changes to accepted external behavior. Preserve
required boundary validation.

Merge candidates that address the same underlying mechanism.

## 4. Present and wait

Rank candidates by concrete benefit and migration risk. For each, give:

- Locations and evidence of the current burden or possible misuse.
- The proposed representation or owning module, and what callers stop doing.
- Expected size (small/medium/large), justified by the affected modules,
  callers, and migration work. State any uncertainty.
- Guarantees gained, affected contracts, migration risks, and verification
  needed.

State what you explored and what remains unread. Return no candidates when
none meet the evidence bar.

Wait for the user to select a candidate and approve any changes to accepted
behavior before editing.

## 5. Implement

Use the `develop` skill for the chosen change. Pass the selected candidate's
evidence, scope, accepted contracts, and risks as its requirements.
