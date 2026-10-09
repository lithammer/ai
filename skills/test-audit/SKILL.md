---
name: test-audit
description: Find tests that do not earn their upkeep and silent regressions nothing guards, then apply the chosen changes.
disable-model-invocation: true
argument-hint: "[scope or concern]"
---

# Test Audit

Audit existing tests with one question: if the behavior a test guards broke,
what would notice first? A test earns its upkeep only when nothing else
would: the regression is silent, and a natural edit could cause it. No diff
is needed.

## 1. Scope

Read the repository's instructions and the requested scope or concern: a
path, subsystem, or kind of test. With no target, map the repository's major
subsystems and choose promising areas to inspect.

Run the in-scope tests and static checks. A test that is already red may
guard a product bug; report it and leave its value unjudged. The proofs in
step 3 need a green baseline.

## 2. Discover

Use a single agent by default. Split a large scope only along genuinely
independent subsystems.

Read each test beside the production code it guards. For each guarded
behavior, ask what would notice a regression first: types, another test, a
crash, a visible failure in normal use, or nothing. Collect candidates in
both directions:

- **Removal:** a test whose regression something else would catch, or that
  goes red when behavior stays the same.
- **Addition:** behavior whose regression nothing would catch, where a
  natural edit could cause it.

## 3. Prove

Record `git status --short` and `git diff` before the first mutation. Prove
each candidate with a **mutation** of the production code, then run the
owner's tests, static checks, and, where the claim is normal use, a real run.
Undo each mutation before the next.

- Break the guarded behavior and something other than the test goes red:
  the test is redundant.
- Change the code without changing behavior and the test goes red: the test
  is a change detector.
- Break the behavior and nothing goes red: propose a test.

Record each mutation and what caught it. A claim the environment cannot run
stays unproven; drop it with the candidates the proof does not support.

Done when every remaining candidate has a mutation record and the working
tree matches the record taken before the first mutation.

## 4. Present and wait

Rank candidates by upkeep removed or risk guarded. For each, give:

- The test or production location and the behavior it concerns.
- The mutation, and what caught it or that nothing did.
- For a removal, the lines it removes, including production code that only
  the test uses.
- For an addition, the contract and the edit that would break it.

State what you explored and what remains unread. Return no candidates when
none hold.

Wait for the user to select candidates before editing.

## 5. Implement

Use the `develop` skill for the selected candidates. Pass each candidate's
mutation record as its requirements; a selected addition is the user asking
for that test.
