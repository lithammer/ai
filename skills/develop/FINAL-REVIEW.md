# Final review

Spawn one fresh subagent per axis below, in parallel. Give each the pinned
review base, task file list, and commands or patches that include staged,
unstaged, and new files, plus its own axis's inputs and no others. Each
reviewer reads the surrounding code and returns findings without editing
files.

Start the reviewers without the implementation conversation, the
implementer's rationale, or each other's findings.

## Spec

Provide the original requirements, including accepted clarifications. When
present, read `GLOSSARY-MAP.md` to locate affected contexts and their
relationships. Include relevant `GLOSSARY.md` glossaries and ADRs, both
system-wide and context-specific. Use the glossaries for domain terms and
current ADRs for design constraints, following status and supersession.
Missing documents alone are not findings.

Trace the requested behavior through the implementation and check it against
applicable design decisions. Find missing or partial requirements, incorrect
execution paths, and behavior added outside the agreed scope. Walk every
stop, cancel, and error path as well: what each wait does when a signal,
cancel, or failure arrives part-way, and what the user is left with. Cite the
contract or decision and the code that contradicts it. For behavior findings,
give a concrete input or execution path that exposes the mismatch.

## Documented standards

Provide every file that documents how the repository's code should be
written or reviewed: the `AGENTS.md` instructions that govern the changed
files, and `CODING_STANDARDS.md`, `REVIEW.md`, and `CONTRIBUTING.md` when
present, with the documents they point to.

Check the change against every rule in those sources. Cite the source and
rule for each violation. Leave checks enforced by tools to those tools;
personal style preferences and generic code-smell lists are outside this
axis.

## Findings

Return each finding with its file and line, consequence, and supporting
evidence. Distinguish confirmed findings from questions that need an answer.
Report no findings when none are supported, and state any review limits.
The implementer owns edits and keeps each axis visible in the outcome.
