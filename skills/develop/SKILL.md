---
name: develop
description: "Implement an agreed feature or fix and prove each outcome with real runs."
---

# Develop

## 1. Establish the scope

Read the request, its spec or tickets, and the documented standards the
review will hold the change to. A ticket's outcomes bind; its plan is a
first sketch, written before anyone dug in, so depart from it when the
code shows a better way. Resolve ambiguities that would change
observable behavior, then list the outcomes, each as something a run can
show. Stay on the current branch unless the user asks otherwise; preserve
unrelated changes and existing staging. Pin the base before editing.

When the change is larger than a reviewer can understand in one pass,
propose slices before implementing: each lands on its own, leaves the code
working, and has outcomes a run can show, with shared interfaces first.
A restructure that makes the change easy is the first slice. Implement the
slice the user picks.

## 2. Implement

**Encode meaning and invariants in the model.** Use types, APIs, and
enforced constraints to express distinctions callers would otherwise need to
remember: units, identities, valid states, and permitted operations. Prefer
representations that prevent misuse over conventions, repeated checks, or
tests that merely detect it. Validate external inputs at the boundary.

**Shape the code for its production callers.** Make the change easy, then
make the easy change: when the existing structure fights the change,
reshape it first rather than patch around it. Choose the cleanest design
for the code that runs, then bring the tests to it. When that design breaks
an existing test that pins internal structure rather than a contract,
rewrite the test against the contract. Reach behavior and resolve
uncertainty through real runs and throwaway probes; what a run shows
outranks what documentation says. Add a seam only tests use when nothing
else can reach it, and name it in the report.

## 3. Establish correctness

Prove each outcome with a real run through the change's entry point, the
way its users drive it: the command, request, page, or public API. Tests show
that logic meets a contract, not that the change works; they back a run, never
replace it. Take one scenario per outcome, in a case a plausible mistake
would fail, with its expected result from the outcomes, reviewed examples,
or a trusted reference. Run against the base where the difference is the
point. Fix defects the runs expose, name each outcome no run could show and
why, and delete the throwaway code.

A new test encodes your reading of the outcomes, the same reading the
implementation encodes. Retain one only when the user asks for a test.
Propose a test only where a regression would go unnoticed by types, existing
tests, or a quick real run, and an incidental edit, made while changing
nearby code for another reason, could bring it back. Propose every test that
meets this, each on its own line: the contract, the incidental edit that
would break it, and how you verified it now.

Continue until each outcome's run and the relevant tests pass after the
fixes.

## 4. Finish

Leave the task's edits uncommitted and unstaged unless the user asks
otherwise. Report for a user who must own the change without reading every
line: teach it, in the report itself.

- **A feature:** teach how it works as a whole. Open with where it sits
  among what was already there, as a diagram or before and after. Then walk
  it the way its user drives it, from entry point to result: each outcome's
  run as you took it, with the output that shows it. Name code only where
  the user must know it to own the feature.
- **A fix:** teach the cause. Show the path the failing input took, where it
  went wrong, and how the fix changes that path, with the run failing on the
  base and passing now.

Then the decisions only the user can make, each with your recommendation.
Then what no run could show and why, which leaves the task open, and test
proposals, a line each. End with the next step: review the change with
shape, then correctness.
