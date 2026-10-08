# Final review

Spawn one fresh subagent per axis below, in parallel within the harness's
capacity. Give each the pinned review base, task file list, and commands or
patches that include staged, unstaged, and new files. Reviewers may read the
surrounding code and run checks; they return findings without editing files.

Provide the original requirements and applicable repository rules, including
accepted clarifications. When present, read `GLOSSARY-MAP.md` to locate affected
contexts and their relationships. Include relevant `GLOSSARY.md` glossaries
and ADRs, both system-wide and context-specific. Use the glossaries for domain
terms and current ADRs for design constraints, following status and
supersession. Missing documents alone are not findings.

Start reviewers without the implementation conversation, the implementer's
rationale, or the other reviewers' findings.

## Spec and correctness

Trace the requested behavior through the implementation and check it against
applicable design decisions. Find missing or partial requirements, incorrect
execution paths, and behavior added outside the agreed scope. Cite the
contract or decision and the code that contradicts it. For behavior findings,
give a concrete input or execution path that exposes the mismatch.

## Test adequacy

Read the contracts and tests. Check what justifies the expected results,
whether the tests exercise the real behavior, and which plausible defects
would escape. Look for shared logic between implementation and expected
results, cases that cannot distinguish the suspected error, and assertions
that bind tests to internal structure.

Before reporting a gap, check whether the model already rules out the
failure, and cite the mechanism that enforces it. Report a gap as a concrete
case the current checks miss, for the implementer to verify once, not as a
request for a retained test. An untested path alone is not a finding.

## Test value

Read the added and changed tests beside the existing suite. For each, name
the contract it protects and the credible regression that turns it red.
Flag a new test the user did not ask for.
Flag a test whose failure existing coverage already catches: each contract
has one owner at the strongest boundary, and another layer needs a risk
that owner cannot reach. Flag a near-duplicate that fits as a case in an
existing test, a test that needs a production seam no production caller
uses, and a bug regression never shown red on the pre-fix code. For each
test you would remove, name the proof that remains or why one-off
verification suffices.

## Documented standards

Check applicable `AGENTS.md` instructions and the repository's documented
coding standards, including `CODING_STANDARDS.md` when present. Cite the source
and rule for each violation. Leave checks enforced by tools to those tools;
personal style preferences and generic code-smell lists are outside this axis.

## Findings

Return each finding with its file and line, consequence, and supporting
evidence. Distinguish confirmed findings from questions that need an answer.
Report no findings when none are supported, and state any review limits.
The implementer owns edits and keeps each axis visible in the outcome.
