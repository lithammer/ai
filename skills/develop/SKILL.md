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

**Make illegal states unrepresentable.** Put what callers would otherwise
need to remember into types and APIs: units, identities, valid states, and
permitted operations. Parse, don't validate: check external input once at
the boundary, into a type the rest of the code can trust.

**Shape the code for its production callers.** Make the change easy, then
make the easy change: when the existing structure fights the change,
reshape it first rather than patch around it. Choose the cleanest design
for the code that runs, then bring the tests to it. When that design breaks
a change-detector test, rewrite it against the contract. Reach behavior and
resolve uncertainty through real runs and throwaway probes; what a run
shows outranks what documentation says. Add a seam only tests use when
nothing else can reach it, and name it in the report.

## 3. Establish correctness

Prove each outcome with a real run through the change's entry point, the
way its users drive it: the command, request, page, or public API. Tests show
that logic meets a contract, not that the change works; they back a run, never
replace it. Take one scenario per outcome that a plausible mistake turns
red, with its expected result from the outcomes, reviewed examples, or a
trusted reference. For a fix, show it red on the base first. Fix defects
the runs expose, name each outcome no run could show and why, and delete
the throwaway code.

A new test encodes your reading of the outcomes, the same reading the
implementation encodes. Retain one only when the user asks for a test.

Continue until each outcome's run and the relevant tests pass after the
fixes.

## 4. Hand off

Leave the task's edits uncommitted and unstaged unless the user asks
otherwise. Report briefly; the reviews will change this code, and `close`
teaches it once they have. Give the outcomes, each with the run that
showed it as a step to repeat, and what no run could show and why. Then
the decisions only the user can make, each with your recommendation. End
with the next step: review the change with shape, then correctness, then
close it.
