---
name: waterfall-review
description: Review a code change by dispatching specialized review subagents in parallel — each focused on a single dimension (correctness, security, architecture, etc.) — then triaging their findings into a unified report. Works standalone on a branch or as part of the waterfall flow after implementation. Use when reviewing changed code, when the user mentions "review the branch" or "review the diff", or as a step inside the waterfall-implement skill.
disable-model-invocation: true
---

# Review

Dispatch specialized review subagents, each focused on a single dimension.
Collect their findings, triage, deduplicate, and present a unified report.

## Step 1: Determine what to review

If this skill has been run earlier in the same conversation, prior triage
decisions (dismissals, user-ignored judgement calls) are already in the
conversation history. Honor them during triage in Step 3 — skip findings
that match a previous decision unless the relevant code has changed since.

Figure out what to review. Pick the first that applies:

1. If this follows an implementation in the same conversation, review the
   files that were created or modified during implementation.
2. If the user gave a base ref, diff against it.
3. If on a branch other than the default branch, diff against the merge-base
   with the default branch. Detect the default branch dynamically (e.g.
   `git symbolic-ref refs/remotes/origin/HEAD`), falling back to
   `origin/main` then `origin/master`.
4. Otherwise, review uncommitted changes (`git diff HEAD`).

Also include any untracked files (`git ls-files --others --exclude-standard`)
so new files get reviewed too.

Collect:

- The list of changed files.
- A **change-summary**: one line per file indicating status (added /
  modified / deleted) and rough magnitude. The command depends on the
  case above:
  - Case 1 (post-implementation): you already know the changes from the
    implementation phase; format them.
  - Case 2 (base ref provided): `git diff --stat <base>..HEAD`.
  - Case 3 (branch): `git diff --stat <merge-base>..HEAD`.
  - Case 4 (uncommitted): `git status --short` plus
    `git diff --stat HEAD`.

  Filter out untracked files unrelated to the current change (editor
  scratch, OS metadata like `.DS_Store`, unrelated experiments left in
  the worktree). Use judgment — if a file's path makes no sense for the
  feature being reviewed, drop it.

  Reviewers use this summary to triage attention (heavily-modified files
  first, new files vs. modified differently) without needing to run git
  themselves.
- A context summary: what feature was planned, what was implemented, any
  known surviving risks from the challenge phase. If this follows the full
  waterfall flow, this context is already in the conversation. If running
  standalone, derive context from the branch name, recent commit messages,
  or by skimming the diff.

Do NOT pass the raw diff to reviewers. They will read the changed files
themselves, which forces them to understand the code in its full context
rather than reviewing a narrow patch in isolation.

## Step 1b: Determine operating context

Describe the code's operating context so reviewers can calibrate what matters
in practice vs. what is theoretical. Cover:

- Who runs this code (end users, internal employees, developers, automated
  jobs).
- Where it runs (public internet, office network, CI, local dev machine).
- What data or systems it touches (PII, credentials, trusted internal data,
  source code only).
- What failure modes matter (availability, correctness, confidentiality).

Use whatever signals are available: repo name, README, package metadata,
directory structure, CLAUDE.md, the nature of the changed files. If you
cannot confidently infer the operating context, ask the user before
proceeding.

Express it as a short paragraph reviewers can interpret for their own
dimension, e.g.: "Internal CLI tool, run by developers on their own laptops,
no network exposure, handles only source code in this repo. Correctness and
convention adherence matter; confidentiality and availability do not."

## Step 2: Select and dispatch reviewers

Before dispatching, skim the diff and changed file list to decide which
reviewers are relevant. For each reviewer below, ask: "based on what
changed, is there anything for this reviewer to examine?" Skip reviewers
where the answer is clearly no.

Available reviewers (each lives at `reviewers/<name>.md`):

- **runtime-bugs** — merged: correctness (sequential bugs, wrong results,
  crashes, data loss) + concurrency (races, synchronization, leaks)
- **code-quality** — merged: readability (complexity, unclear naming) +
  canonical-solutions (bespoke code where a stdlib / idiom / already-
  imported pattern fits) + style-and-hygiene (conventions, leftover
  debris)
- **security** — vulnerabilities, data exposure
- **architecture** — module boundaries, layering, cross-module
  duplication
- **error-handling** — error context, observability, silent failures
- **performance** — obvious, easy-to-fix performance issues
- **test-coverage** — missing tests, brittle tests
- **project-rules** — rules in REVIEW.md and CLAUDE.md (skip if no
  REVIEW.md)

Examples of when to skip:

- Config/documentation-only changes: skip most reviewers, keep
  code-quality (it'll cover style-and-hygiene as one of its axes).
- Pure test refactor: skip security, performance.
- No user input, network, or auth in the changed code: skip security.
- No code that could realistically have runtime bugs (config files, pure
  data): skip runtime-bugs.

For the merged reviewers (`runtime-bugs`, `code-quality`), do not skip
the *reviewer* because only one of its axes might apply — the merged
reviewer handles per-axis applicability internally via its
axis-summary line.

When in doubt, dispatch the reviewer — the triage step will filter false
positives.

Keep a note of which reviewers were skipped and why (one line each) — include
it in the final report under a "Skipped reviewers" heading.

For each selected reviewer, spawn a subagent. Pass it
`reviewers/<name>.md` as its persona and
[REVIEWER_REPORT_FORMAT.md](./REVIEWER_REPORT_FORMAT.md) as its output
specification. Run them in parallel if the harness supports it; otherwise
serialize.

Give each reviewer:

- The list of changed files (paths only).
- The change-summary from Step 1.
- The context summary (feature plan, what was implemented, surviving
  risks).
- The operating context paragraph from Step 1b.

Do not include the diff, do not explain the implementation approach, and do
not share what other reviewers are looking for. Each reviewer arrives at its
conclusions independently.

## Step 3: Triage

Reviewers operate without full context, so not every finding is valid.
Before presenting results, review each finding against the actual code and
the full context summary. Classify:

- **Fix**: Verified against the actual code and clearly correct. Examples:
  a real bug, a leaked secret, dead code, a provably wrong boundary check.
  No user input needed.
- **Judgement call**: Plausible but involves a trade-off, a design
  preference, or context you cannot fully verify yourself (e.g. a "missing
  test" for code that might be covered by an integration test elsewhere, a
  "wrong layer" flag for code that may be intentionally colocated for a
  known follow-up). Reserve this category for findings where a reasonable
  reviewer could go either way — do not use it as a hedge when you are
  simply unsure. If you can verify it by reading more code, do that instead
  of asking the user.
- **Dismiss**: Wrong because the reviewer lacked context, or you verified
  it does not apply. Drop it silently — do not waste the user's attention.

Read the relevant code yourself before classifying. Do not rubber-stamp
findings just because a reviewer reported them.

For merged reviewers (`runtime-bugs`, `code-quality`), verify the
axis-summary line is present in the response. If a reviewer skipped the
axis-summary entirely, treat the dimensions it should have covered as
unreviewed — note them in the final report under "Skipped reviewers"
rather than silently accepting partial coverage.

## Step 4: Deduplicate

After triage, for the remaining findings:

1. Deduplicate: if two reviewers flagged the same line for overlapping
   reasons, keep one entry and note which dimensions flagged it.
2. Sort by file, then by line number.

## Step 5: Resolve judgement calls

For each judgement call, ask the user for a decision and **wait for their
response** before proceeding — do not continue or assume an answer. Present
the finding with enough context to decide: the reviewer's reasoning, the
relevant code, and why you are unsure. Offer options like "Fix it",
"Ignore", or let them provide their own direction.

Batch related judgement calls when they concern the same file or trade-off,
but don't overload a single prompt — keep it to 2-4 questions at a time.

## Step 6: Present results

Print a summary of all findings: what was found, what the user chose to
ignore, and what was dismissed during triage (briefly, by dimension).

For each confirmed fix (both the "Fix" findings from triage and the
judgement calls the user approved), show:

```
[Dimension or Dimension/axis] file:line-range
Description of the issue.
Suggested fix (concrete diff or actionable instruction).
```

For merged-reviewer findings, include the axis tag (e.g.,
`[code-quality/readability]`, `[runtime-bugs/concurrency]`) so the
dimension that flagged it is visible.

If there are no findings for a dimension, say so briefly — don't pad with
filler praise. For merged reviewers, pass through the axis-summary line
verbatim so the user can see what each axis covered.

End with a one-line count: "N findings across M files (K fixed, J
dismissed, L deferred by user)."

Do not apply fixes automatically. Present them for the user to review and
apply.
