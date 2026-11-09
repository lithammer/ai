---
name: shape
description: Review a working change for its shape (cause, ownership, states, names, size, reuse, cost), then apply what you accept.
disable-model-invocation: true
argument-hint: "[target]"
---

# Shape

## Run

1. Diff the review target: the current branch against its merge-base
   with the default branch, plus uncommitted changes, unless the
   invocation names another target.
2. Spawn one reviewer for both Where axes and wait for it.
3. If it reports findings, present each with its counter-draft and
   cost, and wait for the person to accept or decline it. Apply the
   accepted ones.
4. Spawn one reviewer per How axis, in parallel, on the code as it now
   stands, and give each the declined Where findings.
5. Apply each How finding whose counter-draft stays inside the diff and
   keeps to the ticket, then run the existing checks that cover the
   changed code. A fix that breaks a check goes back unapplied.
6. End with the findings by axis and which you applied, one combined
   counter-draft for the rest, and the decisions they leave the person.

Give every reviewer the Scope, Evidence, and Report sections and its own
axis sections, copied verbatim, plus the review target and the ticket.
Add nothing of your own reading.

## Scope

Review the axes your task names. Other reviewers cover the other axes,
and a correctness review runs on the result. When your task carries
declined Where findings, a person has ruled on them; leave them out.

## Evidence

For each candidate, write the counter-draft: the smallest correct change
that solves the same problem. A finding is the gap between the diff and
that draft, and the draft is its evidence. Show that the draft preserves
behavior against callers and tests, and name the concrete cost of the
gap: what a maintainer must hold in mind, keep in sync, or work around.
Line count alone is not a cost.

## Where

### Root cause

Does the change fix the mechanism that produces the problem, or apply a
band-aid downstream of it? A special case layered on shared code is the
usual sign. Trace the problem to its cause and name the change there. A
cause-level fix may overturn an approach the spec prescribed; report it
all the same, for a person to decide.

### Ownership

Does each responsibility the change adds or moves live in the module
that owns its data and rules? Find information leakage: knowledge of one
module's rules or internals spread into its callers. Verify the owner
against interfaces and callers, and keep the search tied to the changed
responsibility.

## How

### States

Does the code admit states the problem does not have? Find data shaped
to hold combinations the problem never produces or to store what could
be derived, and checks that guard states callers and types already rule
out. Make illegal states unrepresentable, and parse, don't validate:
input is checked once where it crosses a trust boundary, into a type the
rest of the code can trust. Show the reshaped data, or the proof from
callers and types, and the code it deletes.

### Precision

Do names, types, and comments say less than the code knows? Name the
precise replacement, in the ubiquitous language. When a comment explains
what a name could say, the name is the finding. When the code relies on
a constraint no name or type can show, the missing comment is the
finding.

### Proportion

Does the change carry accidental complexity: concepts its problem does
not need? A concept is anything a reader must hold in mind. Code the
change repeats or leaves dead counts; so does compatibility with
anything the base never shipped, and a comment that restates the code or
recounts how the change came about. Name each concept the counter-draft
removes.

### Reuse

Does something already do this, in the repository or in what it already
depends on? Name the existing symbol, check that its behavior and
dependency boundaries fit this caller, and weigh the reuse against the
cost of changing the caller.

### Efficiency

Does the change add work the result does not need, or put work where it
costs more: on a hot path, at startup, in sequence where it could run
concurrently, or in memory held longer than its use? Name the cheaper
alternative. Calibrate to where the code runs; work off the hot path
costs little.

## Report

Return each finding with its file and line, its axis, the counter-draft,
the cost, and whether the draft reaches outside the diff or departs from
the ticket.
