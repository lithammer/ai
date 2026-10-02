---
name: develop
description: "Implement a feature or fix from agreed requirements, then test its contracts, refactor, and resolve independent reviews. Use when carrying a defined change through implementation."
---

# Develop

Carry one agreed change through implementation, verification, refactoring,
and review. Use `simplify` and `self-review` from this collection for cleanup.

## 1. Establish the scope

Read the request, its spec or tickets, and the repository's instructions.
Resolve ambiguities that would change observable behavior. Stay on the current
branch unless the user asks otherwise; preserve unrelated changes and existing
staging.

Pin the review base before editing and record pre-existing changes. Carry the
same scope through cleanup and review: the task's branch changes, staged and
unstaged edits, and new files. A committed diff alone may omit the work.

## 2. Implement

Build a coherent implementation. Run existing tests and checks, and use
throwaway probes to resolve uncertainty. Leave new regression and contract
tests for step 3. A bug reproducer may start as a probe before its fix.

Continue until the requested behavior is implemented through the agreed
interfaces and ready to test against its contracts.

## 3. Establish correctness

Choose existing coverage, one-off verification, or a retained test before
designing fixtures. For integration setup, prefer one real run and coverage
through the workflows that use it. A retained setup test needs a project-owned
failure worth its fixtures and upkeep; a conceivable failure alone is not enough.

Derive expected results from the requirements, reviewed examples, or a trusted
reference, rather than the implementation's current output.

Exercise real behavior and choose cases that distinguish plausible mistakes.
Keep probes as regression tests only when they pass the retention decision;
otherwise record the verification result and remove temporary scaffolding.
Fix defects the checks expose before refactoring.

Run the relevant existing and new tests after correctness fixes. Resolve
failures introduced by this change before refactoring; record pre-existing
failures separately.

## 4. Refactor

Use `simplify` with the pinned scope. Include the **Word choice in code and
comments** guidance from `self-review` in this pass; its structural checks
overlap with `simplify` and need no separate pass.

Apply changes that remove a concrete cost while preserving the accepted
contracts. Keep expected behavior fixed during cleanup. If cleanup exposes a
behavior defect or contract ambiguity, resolve it in step 3 before continuing.
Run the relevant checks after edits. An unchanged implementation is a valid
outcome when no useful simplification remains.

## 5. Review and finish

Once cleanup is complete and its checks pass, follow [REVIEW.md](REVIEW.md)
for fresh reviews of spec and correctness, test adequacy, test value, and
documented standards. Keep the reviewed files unchanged while reviewers work.

Assess each finding against its evidence. Fix confirmed issues and record why
others do not apply. When test findings conflict, remove the test unless its
regression is credible, worth the test's upkeep, and missed by the existing
suite. Send fixes back to the affected reviewers, including any other axis
whose assumptions the fix changes. Close findings on the final state; a report
about an earlier version is not final verification.

Run the repository's required checks on the final state. Leave the task's edits
uncommitted and unstaged unless the user asks otherwise. Report the changes,
checks run, review outcomes, and any remaining limits. If a required check or
review cannot complete, report that gap and leave the task open.
