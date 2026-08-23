---
name: waterfall-challenge
description: Run an adversarial review that rejects soft justifications ("it's simpler", "less scope") and demands explicit articulation of both the chosen approach and why dismissed alternatives were ruled out. Spawns a challenger subagent operating in structured rounds with the orchestrator until design-level branches resolve or are accepted as surviving risks. Strategic mode reviews approaches before commitment; tactical mode reviews a detailed plan; retrospective mode reviews an implemented change against the plan that survived. Primarily invoked by waterfall-design, waterfall-plan, or waterfall-implement; avoid auto-triggering on casual mentions of "challenge".
---

# Challenge

Spawn an adversarial subagent and engage in structured rounds of challenge and
response until the design-level branches under review are resolved.

## Prerequisites

This skill expects approaches (from the `waterfall-design` skill), a detailed
plan (from the `waterfall-plan` skill), or an implemented change.

- **Strategic mode**: invoked during design to challenge the set of approaches
  before the user commits to one.
- **Tactical mode**: invoked after planning to challenge the detailed plan.
- **Retrospective mode**: invoked after implementation to challenge whether
  what got built is the change that should have been made.

If none of the three is present, ask the user what to challenge.

## Step 1: Determine mode and prepare input

Take the mode from the caller if it named one. Otherwise detect it, in this
order:

- If the change has already been implemented, run in **retrospective** mode.
- If a detailed plan is present (objective, file manifest, test strategy), run
  in **tactical** mode.
- If approaches with trade-offs are present but no detailed file manifest and
  test strategy, run in **strategic** mode.

Where several could apply, the later phase wins — a plan that has been built
is challenged as built, not as a plan.

Extract the relevant content:

- **Strategic**: the list of approaches with trade-offs, the recommendation,
  and the reasoning.
- **Tactical**: the objective, approach, file manifest and execution order,
  and any open questions the planning phase flagged.
- **Retrospective**: the base ref the change diffs against, the changed-file
  list, and the intent the change was meant to serve — the approved plan and
  the risks the earlier challenge accepted. Running standalone, with no plan
  in the conversation, derive the intent from the branch name, the commit
  messages, or the user, and say which you used. Include any items a previous
  retrospective already dispositioned, so they are not raised again.

## Step 2: Spawn the challenger subagent

Spawn a subagent. Pass it [CHALLENGER_BRIEF.md](./CHALLENGER_BRIEF.md) as its
persona and [CHALLENGER_REPORT_FORMAT.md](./CHALLENGER_REPORT_FORMAT.md) as
its output specification.

The challenger is judgment work, not execution. If the harness supports
per-subagent model or profile selection, use the same reasoning-capable
model/profile as the orchestrator when spawning the challenger. Do not
downgrade the challenger for cost or throughput. If model selection is
unavailable, or subagents already inherit the caller's model, use the
harness default.

Send it as initial input:

- **Review level**:
  - Strategic: "Strategic — challenge the approaches, not implementation
    details."
  - Tactical: "Tactical — the approach is chosen. Challenge whether the plan
    will actually work."
  - Retrospective: "Retrospective — the code exists. Challenge whether it is
    the change that should have been made."
- The input summary from Step 1 (approaches in strategic mode, the plan in
  tactical mode, the change and the intent it is measured against in
  retrospective mode).
- Enough codebase context for it to ground its challenges (key file paths,
  architecture notes). Do NOT do its exploration work for it — let it read
  code to verify its own claims. In retrospective mode this includes the diff:
  give it the base ref, not the patch.

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

   In retrospective mode the code is already committed, so a challenge that
   lands is a decision for the user, not an edit you make mid-loop. Answer it
   with evidence and carry it to Step 5. Do not rework the code here.
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

In retrospective mode, read (2) as objections too minor to change the code
that shipped. A change that matches what survived the earlier challenge should
resolve in a single round — that is the expected outcome, not a failure to
find anything.

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

Ask the user for approval. **Stop and wait for a response.** Tactical mode
ends here; the next phase is the `waterfall-implement` skill, which the user
invokes separately.

In **retrospective** mode, report:

1. **Drift**: where the built change departs from the intent it was measured
   against, and whether the departure is justified.
2. **Resolved branches**: challenges the code answered, and how.
3. **Surviving risks**: what is being accepted as built, and why.

Attach one of three dispositions to every open item — accept as built, fix
now, or record as a backlog item — and let the user pick. Do not apply fixes
here; this mode reports on a change that already exists. When another skill
invoked this one, return the items to it rather than prompting the user, the
way strategic mode returns to `waterfall-design`.
