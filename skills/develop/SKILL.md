---
name: develop
description: "Implement an agreed feature or fix and prove each requirement with real runs. Use when carrying a defined change through implementation."
---

# Develop

## 1. Establish the scope

Read the request, its spec or tickets, and the documented standards the
review will hold the change to. Resolve ambiguities that would change
observable behavior. Stay on the current branch unless the user asks
otherwise; preserve unrelated changes and existing staging. Pin the review
base before editing and record pre-existing changes.

When the change is larger than a reviewer can understand in one pass,
propose slices before implementing: each lands on its own, leaves the code
working, and has requirements a run can show, with shared interfaces first.
Implement the slice the user picks.

## 2. Implement

**Encode meaning and invariants in the model.** Use types, APIs, and
enforced constraints to express distinctions callers would otherwise need to
remember: units, identities, valid states, and permitted operations. Prefer
representations that prevent misuse over conventions, repeated checks, or
tests that merely detect it. Validate external inputs at the boundary.

**Shape the code for its production callers.** Choose the cleanest design
for the code that runs, then bring the tests to it. When that design breaks
an existing test that pins internal structure rather than a contract,
rewrite the test against the contract. Reach behavior and resolve
uncertainty through real runs and throwaway probes; add a seam only tests use
when nothing else can reach it, and name it in the report.

**Keep evidence as you go.** In a record outside the task's changes, note
each run or probe that settles how something behaves: the step as you took
it and its unedited output or screenshot, beside the claim it backs. What a
run shows outranks what documentation says.

Continue until the requested behavior is implemented through the agreed
interfaces.

## 3. Establish correctness

Prove each requirement with a real run through the change's entry point, the
way its users drive it: the command, request, page, or public API. Tests show
that logic meets a contract, not that the change works; they back a run, never
replace it. Take one scenario per requirement from the requirements, not the
code, in a case a plausible mistake would fail, and run against the base where
the difference is the point. Derive expected results from the requirements,
reviewed examples, or a trusted reference, rather than the implementation's
current output. Add the runs to the evidence record, each beside the
requirement it shows. Fix defects the runs expose, name each requirement no
run could show and why, and delete the throwaway code; its output stays in
the record.

A new test encodes your reading of the requirements, the same reading the
implementation encodes. Retain one only when the user asks for a test.
Propose a test only where a regression would go unnoticed by types, existing
tests, or a quick real run, and an incidental edit, made while changing
nearby code for another reason, could bring it back. Propose every test that
meets this, each on its own line: the contract, the incidental edit that
would break it, and how you verified it now.

Continue until the requirement runs and the relevant tests pass after the
fixes; record pre-existing failures separately.

## 4. Finish

Leave the task's edits uncommitted and unstaged unless the user asks
otherwise. Report for a user who must own the change without reading every
line. Lead with the evidence: where the record lives, what each requirement's
final run showed, and the probe results the change rests on. Then the
decisions the requirements left open: where the code commits to one, what it
chose, and what it passed over. Name the hunks that carry the behavior, in
reading order, and what is mechanical. Then fixes beyond the request, test
proposals, and remaining limits. If a requirement run cannot complete, report
that gap and leave the task open. End with the next step: review the change
with shape, then correctness.
