# Final review

Spawn one fresh subagent per axis below, in parallel within the harness's
capacity. Give each the pinned review base, task file list, and commands or
patches that include staged, unstaged, and new files. Reviewers may read the
surrounding code and run checks; they return findings without editing files.

Provide the original requirements and applicable repository rules, including
accepted clarifications. When present, read `CONTEXT-MAP.md` to locate affected
contexts and their relationships. Include relevant `CONTEXT.md` glossaries
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

Request a test only when it protects meaningful behavior or catches a
specific defect. Give a concrete case and explain what the current tests
miss; test counts and coverage percentages alone do not establish adequacy.

## Documented standards

Check applicable `AGENTS.md` instructions and the repository's documented
coding standards, including `CODING_STANDARDS.md` when present. Cite the source
and rule for each violation. Leave checks enforced by tools to those tools;
personal style preferences and generic code-smell lists are outside this axis.

## Findings

Return each finding with its file and line, consequence, and supporting
evidence. Distinguish confirmed findings from questions that need an answer.
Report no findings when none are supported, and state any review limits.
The implementer owns edits and keeps the three axes visible in the outcome.
