---
name: correctness
description: Review a working change for defects (logic, state, lifecycle, concurrency, regression) and for drift from its ticket, docs, and rules, then apply what you accept.
disable-model-invocation: true
argument-hint: "[target]"
---

# Correctness

## Run

1. Diff the review target: the current branch against its merge-base
   with the default branch, plus uncommitted changes, unless the
   invocation names another target.
2. Spawn five reviewers in parallel: one for Logic and Concurrency, one
   for State, one for Lifecycle, one for Regression, and one for the
   Contract axes, leaving out Spec when the change has no ticket.
3. Spawn one verifier with the Evidence and Verify sections copied
   verbatim, the review target, and every finding as its line, trigger,
   and failure, without the reviewer's reasoning.
4. Merge the confirmed and dependent findings that one fix resolves,
   keeping each one's trigger.
5. Present each merged finding with its triggers and failure, the fix
   you would apply, and any fact it depends on, and wait for the person
   to accept or decline it. List the refuted ones in a line each with
   the code the verifier cites, so the person can overrule it. Apply the
   accepted ones, then run the existing checks that cover the changed
   code. A fix that breaks a check goes back to the person.
6. End with the findings by axis, sorted by file and line, which you
   applied, and the decisions they leave the person.

Give every reviewer the Scope, Evidence, and Report sections and its own
axis sections, copied verbatim, plus the review target and the ticket.
Give each Behavior reviewer the paragraph under Behavior as well, and
the Contract reviewer the path of the user-level instruction file your
harness loads. Add nothing of your own reading.

## Scope

Review the axes your task names. Other reviewers cover the other axes;
leave their findings to them.

## Evidence

A finding names the input or state, the changed line, and the failure
that follows: a wrong result, a crash, lost data, or a broken contract.
Report a defect only when the change causes or worsens it, or when the
code fails an explicit requirement of the change, and cite the line
that does. Trace the trigger through callers, guards, types, and
configuration before you report it; a guard that rules it out refutes
it. A defect that another defect hides today still counts; it depends
on that fix.

## Behavior

Trace the change end to end on every Behavior axis: follow each changed
path from where its input enters to where its effects land, in storage,
events, responses, or another process, across files.

### Logic

What input makes a changed line compute the wrong answer? Apply boundary
value analysis to each condition, index, and range the change touches.
Treat input from across a trust boundary as tainted, and trace it to
every sink it reaches. Check that queries, units, and clocks mean what
the code takes them to mean. Find silent failures: an error swallowed,
or a fallback that reports success under a broken assumption.

### State

What invariant can the change leave broken? Name the invariants the
changed code relies on or maintains, then find every write that can
break one, outside the diff as well. An invariant can hold before and
after a multi-step update but not between its steps; find who reads it
there. Where data has a single source of truth, find the copies, caches,
and derived values the change lets drift from it.

### Lifecycle

What does the change start, hold, schedule, or store, and when does each
end? Check exception safety: on every exit, early returns and failures
halfway included, it is released or completed. Find what never ends or
expires and builds up. Ask what happens when its owner ends first, when
the process restarts and memory is lost, and when it runs twice: an
operation that can be retried must be idempotent. An effect that escapes
before its transaction commits outlives a rollback. What the change
stores may meet data written before it, or code from another version;
report that only when the repository shows them meeting: existing
records, a rolling deploy, or a published format.

### Concurrency

What runs at once on shared state? Establish the happens-before order
the changed code relies on, and find where nothing enforces it. A
check-then-act breaks when the state can change between the check and
the act. Report a race only when tasks that really run at once share
the state.

### Regression

What did the old code guarantee that the new code no longer does? Read
the old code beside the new: for each line the change deletes or
replaces, and each path it moves or rewrites, name what it enforced (a
guard, an order, a window, a side effect, a retry) and find where the
new code enforces it again. Respect Chesterton's fence: a guarantee
nobody wrote down still counts.

## Contract

### Spec

Does the change do what its ticket asks? Find requirements missing or
only partly met, requirements met wrongly, and changes to observable
behavior that the ticket did not ask for. Quote the requirement. A
ticket title is context, not a specification; without a usable spec,
say so and leave this axis.

### Contradictions

Does the change leave the code and its own claims disagreeing? Check the
comments, docstrings, and docs the change touches or makes stale against
what the code now does. Quote both claims with their locations and say
which is wrong.

### Conventions

Does a changed line break a rule from the instruction files that govern
it? Find them: the user-level file your task names, and each `AGENTS.md`
or `CLAUDE.md` at the repository root or in an ancestor directory of a
changed file, and the repository's `CODING_STANDARDS.md`, `REVIEW.md`,
and `CONTRIBUTING.md` when present, with the files they import or point
to. A directory's file binds only the files at or below it. Quote the
rule with its file and the line that breaks it; the spirit of a rule is
not evidence.

## Report

Return each finding with its file and line, its axis, the input or
state that triggers it, the failure that follows, and any fact it
depends on that the code does not show.

## Verify

Findings may repeat across reviewers; trace a shared mechanism once and
give each finding its own verdict. For each finding, read the cited line
and trace its trigger to its failure through callers, guards, types, and
configuration. Give one verdict:

- confirmed: the trace holds, and the change causes or worsens it.
- depends: it holds only if a fact the code does not show is true; name
  the fact.
- refuted: cite the code, at file and line, that rules it out, or the
  old code that had the same defect, or say that it names no failure.

Refute only by citing code. A finding you doubt but cannot rule out
depends on the fact you would need.
