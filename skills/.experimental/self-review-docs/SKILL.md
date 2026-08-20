---
name: self-review-docs
description: Use when drafting or editing project prose — README, ADR, guide, runbook, changelog — so the result reads like a human wrote it for a reader arriving cold.
---

Review the prose you just wrote, in the scope the user specified. Fix what you
find and touch nothing outside it. Code comments and docstrings are covered
elsewhere; this skill is for prose files.

## Word choice

Headings and sentences are the same material. Apply Orwell's rules to both:

> Never use a long word where a short one will do.
>
> If it is possible to cut a word out, always cut it out.
>
> Never use the passive where you can use the active.
>
> Never use a foreign phrase, a scientific word, or a jargon word if you can
> think of an everyday English equivalent.

Latinate vocabulary sounds abstract; Anglo-Saxon words are short and physical.
Prefer the Saxon word.

## Claims

Every claim carries its evidence or leaves. "Significantly faster" needs a
number. "Production-ready", "best-in-class", and "secure by default" need a
definition nobody has written. A caveat the reader can act on beats a confident
summary.

## Voice

Match the documents around it: a runbook stays terse, a personal note stays
personal, an engineering doc stays clear of marketing. Name the actor who does
the work rather than hiding them behind the passive. Prefer the concrete noun
to the abstraction.

## Structure

**Inverted pyramid.** Lead with what the reader came for and push background
beneath it. A section adds information its heading did not. When every
paragraph opens on an abstract benefit and closes on a promise, the shape is
generated rather than written.

## Vocabulary

Use the project's own terms, taken from the artifact that defines them. Follow
a reference before asserting what it says: a document that coins its own name
for something the code already names will drift from it.

## Standing alone

The reader arrives with no history of this change. A document that only makes
sense to someone who watched it happen is overfitted — cut the narration of
what this session discovered and keep what the reader needs. A note that names
a migration in flight or an open question goes stale on its own schedule; put
it where it will be found when it resolves, or leave it out.
