---
name: review-docs
description: Reviews doc, docstring, and comment diffs for AI-like prose and for comments that no longer have a job.
disable-model-invocation: true
---

# Review Docs

Review documentation changes for prose that sounds machine-written, generic,
salesy, padded, or unlike the surrounding project voice, and for comments that
no longer have a job.

## Workflow

1. Pick the target in this order: explicit PR, explicit base ref, current branch
   vs default-branch merge-base, otherwise staged/unstaged/untracked docs.
2. Review changed docs prose, docstrings, and every comment in the changed code,
   inline and test comments included; ignore generated files.
3. Follow prose references to files, symbols, constants, prompts, fixtures, or
   source-of-truth docs before judging terminology or cross-file claims.
4. Read nearby unchanged text and referenced artifacts to learn the local voice.
5. Name the rule behind each finding, then sweep every changed comment against
   that rule and report every instance it catches.
6. Report findings first, ordered by how much they hurt reader trust or clarity.

## What To Flag

Keep what the reader needs to act: run, configure, recover, or make a decision.
Link to recipes and configuration definitions instead of transcribing them.
Keep implementation constraints beside the code they constrain. Accurate
prose can still be a finding when deleting it loses no useful guidance.

Flag changed prose that adds no useful guidance or makes the text less clear:

- Generic AI filler: "seamless", "robust", "comprehensive", "streamlined",
  "leverages", "utilizes", "empowers", "enhances", "ensures".
- Throat-clearing: "It is important to note", "In today's landscape",
  "This document aims to", "Let's explore", "By following these steps".
- Inflated claims without evidence: "significantly improves", "best-in-class",
  "production-ready", "highly scalable", "secure by default".
- Over-balanced AI structure: every paragraph has the same rhythm, starts with
  an abstract benefit, or repeats "not only X but also Y".
- Abstract nouns where concrete actors would be clearer.
- Passive or agentless phrasing that hides who does the work or who benefits.
- Summary paragraphs that restate the heading instead of adding information.
- Tone mismatch with nearby docs: marketing voice in engineering docs,
  tutorial voice in a terse runbook, or corporate polish in personal notes.
- Cross-reference drift: a comment coins a term for something the referenced
  artifact already names differently, or asserts a sync rule the other side does
  not document.
- Test or guard comments that explain the mechanism but not what a maintainer
  should do when the test or guard fails.
- Docstrings that only echo the symbol name: `NewThing creates a new Thing`,
  `Thing represents a thing`, `processThing processes a thing`.
- Generic verb wrappers in comments: "handles", "manages", "orchestrates",
  "provides", "is used to", or "allows users to" when they hide the concrete
  behavior, constraint, or side effect.
- Section-marker comments or test comments that sound like generated outlines
  rather than useful explanation.
- Caller's-eye explanation: why the caller calls this rather than what this is.
  It goes stale the moment someone calls it for a second reason; keep only what
  the signature hides.
- Transient state of the world: true the day it was written, quietly false
  later. Prefixes naming a migration in flight, notes on what a live system
  answers today, open ticket numbers.
- Findings narration: what an investigation discovered rather than an invariant
  the code must hold. When the error message, the type, or the control flow
  already says it, the comment is a transcript.

Do not enforce a mechanical word ban. A word is only a finding when the local
sentence would be clearer, more specific, or more believable without it. Whether
a comment has a job is a judgement call too: a transient comment can be worth
keeping while the migration it names is live.

## Review Standard

Prefer prose that sounds like a competent human wrote it for a real reader:

- Concrete nouns and verbs over abstractions.
- Direct cause and effect.
- Specific trade-offs, constraints, and examples.
- Shorter sentences when the current sentence sounds padded.
- Reader-useful caveats instead of confident filler.
- Project terminology, especially vocabulary from referenced artifacts, over
  generic language, test jargon, or local synonyms.
- For test, guard, and assertion comments, explain the failure meaning or fix.
- When suggesting reciprocal notes, check host syntax so comments do not become
  prompt text, string content, or data.
- For docstrings, a first sentence that adds behavior beyond the function,
  type, or method name.

Keep a comment that has a job: it says what the code cannot say and a
foreseeable change will not falsify it. Ask of each one: a property of this
code, or of the world around it? Constraints, invariants, failure modes,
external effects, ordering, limits, and surprising trade-offs are properties of
this code and usually have a job. A fact about the world around it has one only
when the code cannot express it and it outlives the migration, deprecation, or
open question in flight.

## Output

Use a review format, not an essay:

1. Findings first. For each finding include `path:line`, the problem, why it
   reads as machine-written or no longer has a job, and either a suggested
   rewrite or the case for cutting it.
2. If a phrase is awkward but harmless, group it under "Nits" instead of making
   it a top-level finding.
3. If no problems are found, say that clearly and mention the docs surface that
   was checked.
4. Include the review basis: PR, branch comparison, base ref, or uncommitted
   changes.

Keep rewrites close to the author's likely intent. Do not introduce new facts,
new promises, or a more casual voice than the surrounding docs support.
Before returning "no findings", re-check any comment that looked accurate but
wordy: if a shorter, more actionable, or more on-vocabulary version is clearly
better, report it as a finding or nit.

## Editing Rule

This is a review skill by default. Do not edit the docs unless the user
explicitly asks for rewrites to be applied.
