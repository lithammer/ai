---
name: nemesis
description: Challenge a plan, design, or idea one decision branch at a time.
disable-model-invocation: true
---

# Nemesis

Drive a conversation with a persistent adversarial reviewer.

## Start or resume

Reuse the current thread's reviewer, sending only changes and new evidence.
Start a fresh reviewer when none exists, the prior agent is closed, the
user asks for a reset, or the topic changes enough that prior critique
would bias the review. Give a fresh reviewer the conversation context and
these instructions:

- [NEMESIS_BRIEF.md](./NEMESIS_BRIEF.md): how to challenge and close branches.
- [NEMESIS_REPORT_FORMAT.md](./NEMESIS_REPORT_FORMAT.md): response format and
  status markers. Read this before driving the loop below.

If the harness supports only one-shot subagents, carry the prior transcript
into each new dispatch. Wait for critique before taking a step that depends
on it; gather independent context while the reviewer works.

## Drive the loop

1. Check the reviewer's status marker. If it is missing or invalid, ask the
   reviewer to restate the response with a valid marker before proceeding.
2. On `[CONTINUE]`, answer the challenge with evidence. Read the code when
   it can settle the point. Send the answer to the same reviewer and repeat.
3. On `[RESOLVED]` or `[STOPPED]`, end the loop and present the reviewer's
   closing summary, preserving the distinction between accepted risks and
   unreviewed or unresolved branches.

If the user asks to stop, end the loop and summarize the current state.
