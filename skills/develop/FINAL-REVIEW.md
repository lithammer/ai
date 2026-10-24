# Final review

Spawn one fresh subagent per axis below, in parallel. Give each the pinned
review base, the task file list, commands or patches that include staged,
unstaged, and new files, its own axis's section, and the Findings section.
Withhold the implementation conversation, your rationale, and the other
axis's inputs. Reviewers read code and return findings; the implementer runs
checks and edits.

## Spec

Provide the original requirements, including accepted clarifications. When
present, use `GLOSSARY-MAP.md` to find the affected contexts, and provide
their `GLOSSARY.md` glossaries and ADRs, system-wide and context-specific.
Glossaries define domain terms; current ADRs, by status and supersession,
constrain the design. A missing document alone is not a finding.

Trace the requested behavior through the implementation and check it against
applicable design decisions. Find missing or partial requirements, incorrect
execution paths, and behavior added outside the agreed scope. Walk every
stop, cancel, and error path as well: what each wait does when a signal,
cancel, or failure arrives part-way, and what the user is left with.

## Documented standards

Provide every file that documents how the repository's code should be
written or reviewed: the `AGENTS.md` instructions that govern the changed
files, and `CODING_STANDARDS.md`, `REVIEW.md`, and `CONTRIBUTING.md` when
present, with the documents they point to.

Report violations of the rules in those sources that tools do not already
enforce.

## Findings

Return each finding with its file and line, its consequence, and its
evidence: the contract, decision, or rule it breaks and where that is
stated, and for a behavior finding, a concrete input or execution path that
exposes it. Distinguish confirmed findings from questions that need an
answer. Report no findings when none are supported, and state any review
limits.
