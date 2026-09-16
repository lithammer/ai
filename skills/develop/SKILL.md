---
name: develop
description: "Implement a feature or fix from agreed requirements, then test its contracts, refactor, and resolve independent reviews before committing. Use when carrying a defined change through implementation."
---

# Develop

Carry one agreed change through implementation, contract tests, refactoring,
and review. Use `simplify` and `self-review` from this collection for cleanup.

## 1. Establish the scope

Read the request, its spec or tickets, and the repository's instructions.
Resolve ambiguities that would change observable behavior. Work on a feature
branch; preserve unrelated changes.

Pin the review base before editing and record pre-existing changes. Carry the
same scope through cleanup and review: the task's branch changes, staged and
unstaged edits, and new files. A committed diff alone may omit the work.

## 2. Implement

Build a coherent implementation. Run existing checks and use temporary probes
when they answer an uncertainty. Let the task determine the order of edits
and checks; a bug reproducer may be useful before its fix.

Continue until the requested behavior is implemented through the agreed
interfaces and ready to test against its contracts.

## 3. Establish correctness

Write durable tests at the agreed seams. Derive expected results from the
requirements, reviewed examples, or a trusted reference. The implementation's
current output alone is not evidence of the right answer.

Exercise real behavior and choose cases that distinguish plausible mistakes.
Keep probes that protect a distinct contract or reproduce a defect; remove
temporary scaffolding. Fix defects the tests expose before refactoring.

Proceed when the contract tests pass. Identify pre-existing failures
separately from failures introduced by this change.

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
for fresh reviews of spec and correctness, test adequacy, and documented
standards. Keep the reviewed files unchanged while reviewers work.

Assess each finding against its evidence. Fix confirmed issues and record why
others do not apply. Send fixes back to the affected reviewers, including any
other axis whose assumptions the fix changes. Close findings on the final
state; a report about an earlier version is not final verification.

Run the repository's required checks on the final state. Commit only the
task's changes unless the user requested otherwise. Report the commit, checks
run, review outcomes, and any remaining limits. If a required check or review
cannot complete, report that gap and leave the task open.
