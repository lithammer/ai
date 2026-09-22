# Challenger Report Format

Every round of the challenge produces one report following this structure.

Write the full report to a unique file in shared temporary storage; return only its absolute path and the one-line verdict `[CONTINUE]` or `[RESOLVED]`. The orchestrator reads the file with Read before responding or moving on.

## Structure

```md
## Challenges

1. [First challenge — specific, grounded in code where possible]
2. [Second challenge]
3. [Third challenge]
...

## Resolved (subsequent rounds only)

- [Challenge that was resolved this round, with one-line summary of the
  resolution]

## New concerns (subsequent rounds only, when applicable)

- [Concerns that surfaced from the main agent's responses]

[CONTINUE]  -- or --  [RESOLVED]
```

## Rules

- The numbered list of challenges is ordered by importance, most critical
  first.
- Aim for 3-7 challenges per round. Group related concerns together rather
  than padding the list. A round with nothing left to raise returns
  `[RESOLVED]` with no challenges; never invent one to reach the range.
- On subsequent rounds, repeat any still-open challenges with a follow-up,
  not just the original challenge. The main agent needs to know what its
  prior response failed to resolve.
- On the final round, replace the "Challenges" section with "Surviving open
  risks" — these are the concerns being accepted rather than addressed.

## Termination marker (required in every report)

End every report with exactly one of these two lines on its own line,
uppercase, no other text on the line:

- `[CONTINUE]` — open concerns remain; expect another round.
- `[RESOLVED]` — no more concerns; the surviving risks list above is final.

The orchestrator keys off this marker to decide whether to send another
round or move on. Do not omit it, paraphrase it, or bury it in prose.
