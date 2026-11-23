---
name: close
description: Prove a reviewed change on its final code, teach it, and decide its tests.
disable-model-invocation: true
argument-hint: "[target]"
---

# Close

The reviews changed the code after its last run. Close proves and teaches
the code as it now stands.

## 1. Recover the outcomes

Diff the target: the current branch against its merge-base with the
default branch, plus uncommitted changes, unless the invocation names
another target. List the outcomes, each as something a run can show, from
the ticket or request; an outcome is behavior a user, caller, or peer
observes. Where the session holds a hand-off from `develop`, take its
outcomes and their runs, and check each still matches the ticket.

## 2. Prove

Prove each outcome with a real run through the change's entry point, the
way its users drive it: the command, request, page, or public API. Repeat
the runs the session holds. For an outcome without one, take one scenario
that a plausible mistake turns red, with its expected result from the
outcomes, reviewed examples, or a trusted reference. For a fix, show it
red on the base first. Where the fix rests on several guards, show each
one red in place: remove it, run that test alone, and put it back,
checking the diff matches what it was before.

A run that fails now shows a defect the reviews let in or left. Fix it,
rerun every outcome the fix could touch, and keep the failure for the
report. Delete the throwaway code.

Done when each outcome has a passing run on the final code, or is named
with the reason no run could show it.

## 3. Decide tests

Propose a test only where a regression would go unnoticed by types,
existing tests, or a quick real run, and an incidental edit, made while
changing nearby code for another reason, could bring it back. A defect
the reviews or these runs found is a mistake already made once; weigh
each first. Prefer a form that does not share your reading of the
outcomes: a walk of every reachable state, generated inputs, or the base
as the oracle. Propose every test that meets this, each on its own line:
the contract, the incidental edit that would break it, and how you
verified it now.

A shim, code that bridges data or callers about to age out, such as a
fill-in for records saved before a recent format change, gets a
throwaway run in place of a test: its regression ends when the old data
does. Name in the report when the shim can go.

## 4. Teach

Report for a user who must own the change without reading every line:
teach it, in the report itself.

- **A feature:** teach how it works as a whole. Open with where it sits
  among what was already there, as a diagram or before and after; for a
  feature that moves between states, a statechart in the user's words.
  Then walk it the way its user drives it, from entry point to result:
  each outcome's run as you took it, with the output that shows it. Name
  code only where the user must know it to own the feature.
- **A fix:** teach the cause. Show the path the failing input took, where it
  went wrong, and how the fix changes that path, with the run failing on the
  base and passing now.

Then what a run broke after the reviews and how you fixed it. Then what no
run could show and why, which leaves the task open. Then the test
proposals; write the ones the user picks.
