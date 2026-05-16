---
name: nemesis
description: Challenge a plan, design, or half-formed idea with a conversational adversarial reviewer that walks the decision tree one branch at a time. Use when the user wants a rigorous adversarial review, mentions "nemesis" or "enemy", or when the current direction may be too safe, narrow, or prematurely committed.
disable-model-invocation: true
---

# Nemesis

Use this skill as a conversational adversarial reviewer for plans,
designs, or half-formed ideas.

## Agent Mode

When this skill is invoked, prefer a persistent reviewer agent over a
one-off response.

1. If no active reviewer agent exists for the current thread, start one
   with the current conversation context. Pass it
   [NEMESIS_BRIEF.md](./NEMESIS_BRIEF.md) as its persona and
   [NEMESIS_REPORT_FORMAT.md](./NEMESIS_REPORT_FORMAT.md) as its output
   specification.
2. If an active reviewer agent already exists, reuse it so it keeps
   context about the plan, rejected branches, accepted risks, and
   earlier objections.
3. Start a fresh reviewer agent only when the user asks for a reset,
   the topic changes enough that old critique would bias the new
   problem, or the prior agent is closed.
4. When reusing the reviewer agent, send only the delta plus any newly
   discovered code or constraints.
5. If the next local step depends on the critique, wait for the
   reviewer result. Otherwise let it work in parallel while you gather
   context.

## The conversation loop

Each turn, the reviewer returns one challenge followed by a `[CONTINUE]`
or `[RESOLVED]` marker on its own line. Drive the loop:

1. Read the challenge. Check the marker.
2. If `[RESOLVED]`, stop the loop and present the surviving-risks summary
   (from the same turn) to the user.
3. Otherwise, address the challenge. Read code if it can be answered
   from the codebase. Respond with evidence; do not hand-wave.
4. Send your response back to the same reviewer agent. If the harness
   only supports one-shot subagents, re-spawn with the prior transcript
   appended as additional context.
5. Read the next challenge. Go back to step 1.

If a response is missing the marker, treat it as `[CONTINUE]` and keep
the conversation going — a missing marker shouldn't prematurely end the
loop.
