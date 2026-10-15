---
name: develop
description: "Implement a feature or fix from agreed requirements, then verify it and resolve an independent spec review. Use when carrying a defined change through implementation."
---

# Develop

Carry one agreed change through implementation, verification, and a review
against its spec.

## 1. Establish the scope

Read the request, its spec or tickets, and the repository's instructions.
Resolve ambiguities that would change observable behavior. Stay on the current
branch unless the user asks otherwise; preserve unrelated changes and existing
staging.

Pin the review base before editing and record pre-existing changes. Carry the
same scope through review: the task's branch changes, staged and unstaged
edits, and new files. A committed diff alone may omit the work.

## 2. Implement

**Encode meaning and invariants in the model.** Use types, APIs, and enforced
constraints to express distinctions callers would otherwise need to remember:
units, identities, valid states, and permitted operations. Prefer representations
that prevent misuse over conventions, repeated checks, or tests that merely
detect it. Validate external inputs at the boundary.

Build a coherent implementation. Run existing tests and checks, and use
throwaway probes to resolve uncertainty. A bug reproducer may start as a
probe before its fix.

Continue until the requested behavior is implemented through the agreed
interfaces and ready to verify.

## 3. Establish correctness

Verify the change against real behavior with existing tests, a real run, or
throwaway tests and probes. Derive expected results from the requirements,
reviewed examples, or a trusted reference, rather than the implementation's
current output. Choose cases that distinguish plausible mistakes. Fix defects
the checks expose, record what each check showed, and delete the throwaway
code.

A new test encodes your reading of the requirements, the same reading the
implementation encodes. Retain one only when the user asks for a test.
Update existing tests the change invalidates. Propose a test only where a
regression would go unnoticed by types, existing tests, or a quick real run,
and a natural edit could bring it back. Propose every test that meets this,
each on its own line: the contract, the edit that would break it, and how
you verified it now.

Run the relevant existing and new tests after correctness fixes. Resolve
failures introduced by this change before review; record pre-existing
failures separately.

## 4. Review and finish

Once the checks pass, follow [REVIEW.md](REVIEW.md) for a fresh review against
the spec. Keep the reviewed files unchanged while the reviewer works.

Assess each finding against its evidence. Fix confirmed issues and record why
others do not apply. Send fixes back to the reviewer. Close findings on the
final state; a report about an earlier version is not final verification.

Run the repository's required checks on the final state. Leave the task's edits
uncommitted and unstaged unless the user asks otherwise. Report the changes,
including fixes beyond the request, what each check showed, the review outcome,
test proposals, and any remaining limits. If a required check or the review
cannot complete, report that gap and leave the task open.
