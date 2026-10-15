# Spec review

Spawn one fresh subagent. Give it the pinned review base, task file list, and
commands or patches that include staged, unstaged, and new files. The reviewer
reads the surrounding code and returns findings without editing files.

Provide the original requirements, including accepted clarifications. When
present, read `GLOSSARY-MAP.md` to locate affected contexts and their
relationships. Include relevant `GLOSSARY.md` glossaries
and ADRs, both system-wide and context-specific. Use the glossaries for domain
terms and current ADRs for design constraints, following status and
supersession. Missing documents alone are not findings.

Start the reviewer without the implementation conversation or the
implementer's rationale.

## Brief

Trace the requested behavior through the implementation and check it against
applicable design decisions. Find missing or partial requirements, incorrect
execution paths, and behavior added outside the agreed scope. Walk every
stop, cancel, and error path as well: what each wait does when a signal,
cancel, or failure arrives part-way, and what the user is left with. Cite the
contract or decision and the code that contradicts it. For behavior findings,
give a concrete input or execution path that exposes the mismatch.

## Findings

Return each finding with its file and line, consequence, and supporting
evidence. Distinguish confirmed findings from questions that need an answer.
Report no findings when none are supported, and state any review limits.
