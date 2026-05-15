---
name: waterfall-challenge
description: Run an adversarial review that rejects soft justifications ("it's simpler", "less scope") and demands explicit articulation of both the chosen approach and why dismissed alternatives were ruled out. Spawns a challenger subagent operating in structured rounds with the orchestrator until design-level branches resolve or are accepted as surviving risks. Strategic mode reviews approaches before commitment; tactical mode reviews a detailed plan. Use when a plan or design needs rigorous adversarial review, when the user mentions "challenge", or as part of the waterfall flow.
disable-model-invocation: true
---

# Challenge

Spawn an adversarial subagent and engage in structured rounds of challenge and
response until the plan's design-level branches are resolved.

## Prerequisites

This skill expects either approaches (from the `waterfall-design` skill) or a
detailed plan (from the `waterfall-plan` skill) in the conversation.

- **Strategic mode**: invoked during design to challenge the set of approaches
  before the user commits to one.
- **Tactical mode**: invoked after planning to challenge the detailed plan.

If neither is present, ask the user what to challenge.

## Step 1: Determine mode and prepare input

Detect the mode from the conversation:

- If approaches with trade-offs are present but no detailed file manifest and
  test strategy, run in **strategic** mode.
- If a detailed plan is present (objective, file manifest, test strategy), run
  in **tactical** mode.

If both exist, use the most recent.

Extract the relevant content:

- **Strategic**: the list of approaches with trade-offs, the recommendation,
  and the reasoning.
- **Tactical**: the objective, approach, file manifest and execution order,
  and any open questions the planning phase flagged.

## Step 2: Spawn the challenger subagent

Spawn a subagent. Pass it [CHALLENGER_BRIEF.md](./CHALLENGER_BRIEF.md) as its
persona and [CHALLENGER_REPORT_FORMAT.md](./CHALLENGER_REPORT_FORMAT.md) as
its output specification.

Send it as initial input:

- **Review level**:
  - Strategic: "Strategic — challenge the approaches, not implementation
    details."
  - Tactical: "Tactical — the approach is chosen. Challenge whether the plan
    will actually work."
- The input summary from Step 1 (approaches in strategic mode, plan in
  tactical mode).
- Enough codebase context for it to ground its challenges (key file paths,
  architecture notes). Do NOT do its exploration work for it — let it read
  code to verify its own claims.

The subagent will return its first batch of challenges.

## Step 3: Engage in rounds

The challenge phase works in rounds, not individual turns. Each round:

1. **Read the challenges.** The subagent returns a numbered list of concerns
   followed by a `[CONTINUE]` or `[RESOLVED]` marker on its own line.
2. **Check the marker.** If `[RESOLVED]`, stop the round loop and proceed to
   Step 5. If `[CONTINUE]`, proceed to step 3 below.
3. **Address each challenge.** For each:
   - If it can be answered by reading code, read the code and respond with
     evidence.
   - If it reveals a genuine weakness, acknowledge it and revise the plan.
   - If it is based on a misunderstanding, clarify with references to the
     code.
4. **Send all responses back to the same subagent.** Include the updated plan
   if you made revisions. If the harness only supports one-shot subagents,
   re-spawn with the prior transcript appended as additional context.
5. **Read the subagent's evaluation.** Go back to step 1.

If the response is missing the marker, or the marker is ambiguous, treat it
as `[RESOLVED]` and move on. Do not wait indefinitely on a silent or
malformed response — that is a subagent bug, not a signal to keep waiting.

Expect 2-4 rounds. Cap at 5. If the loop hits 5 rounds without converging,
stop and treat any unresolved challenges as surviving risks — present them to
the user rather than continuing to argue with the subagent.

Do NOT:

- Dismiss challenges without evidence.
- Agree with everything to end the loop faster.
- Propose changes without checking that they actually work in the codebase.

## Step 4: Termination

The challenge is done when:

1. All design-level branches are resolved or accepted as risks.
2. The remaining objections are implementation-level or too minor to change
   the design.
3. The user asks to stop.

## Step 5: Present results

In **strategic** mode, return to the caller (the `waterfall-design` skill)
with the revised approach list and the resolved/open branches. Do not prompt
the user here — `waterfall-design` handles the presentation and selection.

In **tactical** mode, summarize for the user:

1. **Plan revisions**: What changed in the plan as a result of the challenge.
   Show the updated plan if there were material changes.
2. **Resolved branches**: Key challenges that were addressed and how.
3. **Surviving risks**: Open risks that were explicitly accepted. For each,
   state what could go wrong and why the risk was accepted.
4. **Recommendation**: Whether the plan is ready for implementation.

Ask the user for approval. **Stop and wait for a response.** This skill ends
here. The next phase is the `waterfall-implement` skill, which the user will
invoke separately.
