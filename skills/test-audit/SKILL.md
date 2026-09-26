---
name: test-audit
description: "Audit tests for redundant or implementation-coupled coverage, and check the value of new or changed tests. Use for test reviews, test-pruning sweeps, and subsystem-wide test audits."
disable-model-invocation: true
---

# Test Audit

Three modes, one value bar. Authoring mode checks each new or changed test at
write time. Audit mode examines tests that re-assert source, duplicate stronger
proof, couple behavior to implementation, or keep test-only production seams
alive. For broad audits, work in coherent batches; optimize for confidence, not
deletion count. Campaign mode covers one whole subsystem's test surface. Before
starting a campaign, read [CAMPAIGN.md](CAMPAIGN.md).

## Authoring gate

Before adding any test, answer four questions; a missing answer means do not
add it yet:

1. What observable behavior, invariant, or independent contract does it protect?
2. What credible regression makes it fail?
3. Why does existing coverage not already catch that failure? Each contract has
   one primary test owner at the strongest boundary; another layer needs its
   own distinct risk, such as a transport or lifecycle failure the owner cannot
   reach. Prefer extending a table-driven case or shared fixture over a
   near-duplicate test; consolidate duplicated setup in the same change.
4. Does it need a production seam (export, flag, wrapper, injection hook) that no
   production caller needs? If yes, move the test to the real boundary instead.

Then check the test against every [junk pattern](#junk-patterns); a match fails
the gate unless the [retention bar](#retention-bar) names the contract it
independently guards. A test that would break under behavior-preserving
refactoring is asserting implementation, not behavior; rewrite it at the
owning boundary before landing it.

Bug regression tests must fail on the pre-fix code for the intended reason and
pass after the owner-boundary repair. A regression test that never demonstrably
failed proves the mock, not the fix. One regression at the owner boundary
covers the bug; do not replay the same scenario at every layer it crosses.

## Junk patterns

The shared checklist for authoring and audit modes: the authoring gate rejects a
new test that matches one, and audits hunt for existing tests that do.

- assertion-free coverage probes;
- self-comparisons and identity copiers;
- copied fixtures, inventories, manifests, or export lists;
- exact source, import, or string greps;
- private predicate or call-shape tests duplicated at real boundaries;
- duplicate invocations of the same contract;
- provider-local replays of shared helpers;
- tests whose only purpose is preserving test-only exports, globals, or wrappers;
- dead production code whose only callers are tests;
- expected values produced by the helper or renderer under test;
- mocks that implement the asserted behavior, or one identical mock standing in
  for different APIs;
- fixtures that supply outcomes or event ordering the owner should produce, or
  persistence asserted against a store the path never writes;
- capability tests that restate declared flags instead of exercising the
  delivery or acknowledgement the flag promises;
- negative controls that pass for an unrelated reason, such as a denial from a
  different guard or a rejection the production path never reaches;
- names or fixtures that promise more than the input and assertions exercise.

## Value bar

Tests justify their maintenance cost by protecting behavior, a credible
regression, or an independently meaningful contract. In an audit, an existing
test that must change for behavior-preserving source reorganization is suspect,
not automatically deletable; the authoring gate still rejects new ones.

Before judging a candidate, read the complete test and production owner, its
entry point, callers, callees, sibling implementations, overlapping tests, test
execution setup, and relevant history. Read the repository's applicable
instructions first. When the test claims dependency-backed behavior, inspect
the dependency source or types directly.

## Discovery

Keep discovery read-only and report evidence before editing. For broad scope,
split discovery along the repository's production owner boundaries and include
a cross-cutting pattern sweep. Parallelize independent lanes when available.

Outside campaign mode, prefer a few high-confidence candidates over a large
speculative inventory. Hunt for the [junk patterns](#junk-patterns).

## Retention bar

Keep a test when it independently enforces an API, protocol, configuration,
migration, storage, security, platform, generated artifact, release, or
architecture contract. Also keep:

- call ordering when order is observable behavior;
- regressions with a credible failure mode;
- source inspection when it is the cheapest independent guard: it fails when
  the contract changes (the user-facing key, byte, or path) and survives an
  identifier-only refactor;
- a retained test that fails on the baseline: treat it as a possible product
  bug, reproduce it, and repair the owner rather than deleting it.

Static or slow is not a deletion reason. A test that resembles implementation
may still be the independent contract; prove otherwise before removing it.

## Candidate evidence

Record every field below before editing. A missing field means the candidate is
not ready for deletion:

- exact test name and location;
- what failure it can actually detect;
- non-test callers of the covered production or support seam;
- stronger remaining owner-boundary proof, or why no proof is needed;
- relevant history and the reason the test or seam exists;
- production or test-support deletion unlocked;
- risk and the focused validation command.

## Edit shape

Choose one coherent owner-boundary batch. Delete obsolete test-only exports,
globals, wrappers, and dead production paths instead of preserving aliases.
Move retained regressions to their canonical owners. Consolidate repeated
package or dependency assertions into one generic contract.

Prefer net-negative production LOC. Do not add replacement tests that restate
the same implementation, and do not convert uncertain candidates into cleanup
to increase deletion counts.

## Validation

Use the repository's test runner and validation policy. Do not edit files while
a test run is reading them in the same workspace.

1. Run the smallest owner and sibling tests that exercise the changed contracts.
2. For removed source greps or plan assertions, run the executable script or
   dry-run that owns the real contract.
3. Run applicable formatting and changed-file checks. Inspect the changes for
   whitespace errors.
4. Run any broader suite or gate required by the repository, and name checks
   that could not run.
5. Compare the before and after change size; report production/tooling
   separately from tests and test support.
6. Review the final diff for lost contracts and vacuous assertions.

## Landing and continuation

Follow the user's and repository's delivery instructions. If the audit
continues after a batch is accepted, refresh the baseline and rerun read-only
discovery for the next high-confidence batch.

## Handoff

Report:

- root cause and removed low-value categories;
- production owner simplifications;
- retained false positives and why they remain valuable;
- focused and full proof actually run;
- production versus test LOC;
- delivery state when applicable;
- named follow-ups.
