---
name: research
description: "Research technical, academic, or open-source topics by grounding claims in primary evidence: docs, papers, standards, code, issues, releases."
disable-model-invocation: true
---

# Research

## Quick start

1. Frame the research question, constraints, and decision the answer should support.
2. Write a brief plan using [PLAN_FORMAT.md](./PLAN_FORMAT.md) before deep search.
3. Gather primary evidence first; use secondary sources as leads, not proof.
4. Inspect papers, standards, repos, code, issues, releases, and benchmarks deeply enough to support claims.
5. Use sub-agents for independent research branches when available; require concise reports.
6. Synthesize into a Markdown file in the repository: evidence ledger, negative pass, recommendation, and open questions.

## Workflow

### 1. Frame the research

- Identify the user's actual decision, constraints, and evaluation criteria.
- Ask clarifying questions only when missing context would change the recommendation.
- Capture key terminology, aliases, and related problems so searches do not miss canonical sources.
- Produce a short research plan with search terms, source classes, repo filters, budget, and deliverable.

### 2. Find sources

- Prefer primary, current, inspectable sources: official docs, standards, papers/surveys, repository code, issues, releases, and reproducible benchmarks.
- Use blog posts, package registries, forums, citations, backlinks, and comparison pages for discovery; corroborate before relying on them.
- Treat stars, citation counts, old posts, opaque benchmarks, and unsourced claims as weak evidence unless supported by stronger sources.

### 3. Delegate when useful

If sub-agent/delegation support is available, split independent branches to keep the main context small. Good branches include literature, repositories, ecosystem/adoption, and risks.

Tell each sub-agent to return a concise report, not raw browsing logs. Use [SUBAGENT_REPORT_FORMAT.md](./SUBAGENT_REPORT_FORMAT.md) for the report format.

### 4. Inspect evidence

For academic or well-defined problem domains, verify:

- Definitions, assumptions, inputs/outputs, variants, and canonical terminology.
- Correctness and complexity claims, including edge cases and implementation constraints.
- Benchmark methodology, reproducibility, contested results, applicability, limitations, and common misuses.

For repositories, verify:

- Purpose, boundaries, adoption, maintenance, release cadence, and license/security posture.
- README/docs against actual code, examples, tests, architecture, and extension points.
- Issues and PRs for recurring bugs, design tensions, migration pain, performance complaints, and maintainer direction.
- For deep evaluation, cache or update a local checkout and read code rather than relying on GitHub summaries.

### 5. Synthesize

- Maintain an evidence ledger of inspected sources, what was checked, and confidence.
- Separate facts from interpretation; cite specific URLs, paper IDs, issue numbers, or local paths.
- Call out uncertainty, stale signals, and conflicts between sources.
- Run a negative pass: what evidence argues against the likely recommendation?
- Explain the recommendation, trade-offs, and remaining questions for the user's context.

## Deliverable

Write the findings to a single Markdown file, following [DELIVERABLE_FORMAT.md](./DELIVERABLE_FORMAT.md) unless the user asks otherwise. Always include a summary, evidence ledger, negative evidence, recommendation, and open questions.

Save it where the repository already keeps research notes and match that convention; when there is none, choose a sensible location and say where. Reply with the summary and a link to the file: the file is the deliverable, the reply is the pointer.

## Guardrails

- Do not claim to have checked sources that were not opened or inspected.
- Do not over-weight stars, citations, benchmark wins, or marketing claims.
- Do not ignore negative evidence from issues, PRs, changelogs, errata, or failed replications.
- If online access is unavailable, say so and provide an offline plan or inspect already-cached sources.
- Keep notes concise while preserving enough links for verification.
