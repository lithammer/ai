---
name: nemesis
description: Challenge a plan, design, or implementation one branch at a time.
disable-model-invocation: true
---

# Nemesis

Keep the same adversarial reviewer throughout the review loop, across all
challenge-and-response turns. Release it when the review ends.

## Pick the brief

The target picks the brief:

- A plan, design, or idea: [NEMESIS_BRIEF.md](./NEMESIS_BRIEF.md).
- An implementation, such as a diff, branch, or PR: two passes,
  [FIT_BRIEF.md](./FIT_BRIEF.md) then
  [ECONOMY_BRIEF.md](./ECONOMY_BRIEF.md). Fit goes first: trimming a change that turns out to be the wrong one
  wastes the pass.

Read the target from the request and the conversation; a working-tree
diff only supports that reading. An argument of `design` or
`implementation` decides it outright, and `fit` or `economy` runs that
one pass alone. When the target spans both, ask the user which. Name the
brief to the user before the first challenge.

## Start or resume

Start a fresh reviewer each time this skill is invoked. Within that run,
reuse it, sending only changes and new evidence. Start a replacement if it has
already closed. Otherwise, release it before starting a replacement when
the user asks for a reset, the brief changes, or the topic changes enough
that prior critique would bias the review. Give a fresh
reviewer the conversation context and these instructions:

- The picked brief: how to challenge and close branches.
- [NEMESIS_REPORT_FORMAT.md](./NEMESIS_REPORT_FORMAT.md): response format and
  status markers. Read this before driving the loop below.

If the harness supports only one-shot subagents, carry the prior transcript
into each new dispatch. Wait for critique before taking a step that depends
on it; gather independent context while the reviewer works.

## Drive the loop

1. Check the reviewer's status marker. If it is missing or invalid, ask the
   reviewer to restate the response with a valid marker before proceeding.
2. On `[CONTINUE]`, answer the challenge with evidence: defend the choice,
   or change it and show the result. Read the code when it can settle the
   point. Send the answer to the same reviewer and repeat.
3. On `[RESOLVED]` or `[STOPPED]`, end the loop and present the reviewer's
   closing summary, preserving the distinction between accepted risks and
   unreviewed or unresolved branches.
4. In a two-pass run, a `[RESOLVED]` fit pass starts the economy pass on
   the code as it now stands. A `[STOPPED]` fit pass ends the run.

If the user asks to stop, end the loop and summarize the current state.

## Release reviewers

When the review completes, the user stops it, or an error ends the run,
preserve the available findings and release every reviewer started by this
run before presenting the final summary. Leave unrelated agents alone.
Report cleanup failures in the summary.
