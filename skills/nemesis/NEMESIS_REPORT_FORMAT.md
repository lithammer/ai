# Nemesis Report Format

Use this format for each reviewer response. The orchestrator uses the
final marker to decide whether to continue the conversation.

## Continuing

```md
## Current branch
[Short branch label.]

## Challenge
[Challenge or resolution check grounded in the plan, code, or prior reply.
When moving from a closed branch, first state why that branch closed.]

[CONTINUE]
```

## Closing

Report only risks and branches identified during the conversation. State
"None" for an empty section.

```md
## Review status
[All identified branches closed, or who requested an early stop. Include
the basis for any branch closure since the previous response.]

## Surviving risks
- [What could go wrong, who accepted the risk, and why.]

## Outstanding branches
- [Unreviewed or unresolved branch and what remains open.]

[RESOLVED]
```

## Status markers

End every response with exactly one marker on its own line:

- `[CONTINUE]`: another challenge or resolution check remains.
- `[RESOLVED]`: every identified branch meets the closure criteria in
  [NEMESIS_BRIEF.md](./NEMESIS_BRIEF.md#close-branches).
- `[STOPPED]`: the main agent or user ended the review before all branches
  closed. Use the closing format with this marker in place of `[RESOLVED]`.

An early stop leaves outstanding branches open; it does not accept their
risks.
