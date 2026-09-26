# Test-pruning campaign

Campaign mode audits one subsystem's whole test surface in one coherent change.
The value bar, retention bar, candidate evidence, and validation in
[SKILL.md](SKILL.md) apply to every lane. This file adds the order of work.
Each step ends on its completion criterion; do not start the next step early.

## 1. Baseline

Before editing, record the subsystem's test and support line counts and every
test file's pass/fail state. Keep baseline failures in their own list and
investigate them as possible product bugs.

Done when every in-scope test file has a recorded baseline result.

## 2. Lanes and inventory

Split the surface into **lanes** along production owner boundaries, not file
prefixes. Include the subsystem's cases at shared boundaries, integration
tests, and any manual or automated QA scenarios it owns.

Done when every test file and QA scenario the subsystem owns belongs to exactly
one lane.

## 3. Read-only ledger per lane

Read each lane in a separate read-only pass. Read every assigned test in full,
including parameter tables. Also read the production owners and their entry
points, callers, history, and test execution setup. Each test declaration goes
into a written **ledger** with one mark. A parameterized test is one declaration
unless its cases need different marks; then mark each case.

- `R`: retain, naming the contract and the bug it catches; a retained test that
  only moves to a better-named file stays `R` with the move noted;
- `F`: retain the contract but repair the assertion, such as a vacuous negative
  that passes when only one of several items is missing;
- `C`: consolidate, naming the owner that absorbs the assertion first: a sibling
  table case, a stronger boundary suite, or the shared owner in another package;
- `D`: delete, naming the proof that remains, or why no contract exists.

Judge a test by its assertions, not its name.

Done when every declaration in the lane has a mark and an evidence line.

## 4. Layer plan per lane

Treat the per-test ledger as input, not as the edit list. A second read-only
pass, starting from the ledger, looks for the redundant **layer**. Name the
**keeper** suite for each contract. Prefer a real boundary with a controlled
external dependency over a mocked internal collaborator. Correct any ledger
errors this pass finds.

Done when each lane plan names its retired files, its keeper per contract, the
assertions to carry into keepers, and the test-only production seams unlocked.

## 5. Cutover

Edit lane by lane. Serialize changes to shared test support files through one
owner. With each lane, remove the test-only production seams it unlocks:
injection parameters, getters, reset exports, and indirection layers. Register
moved suites in test discovery and execution config. Update any test line-count
baselines. Record durable test-ownership rules in repository guidance when the
campaign uncovers a recurring mistake.

Done when every lane plan is applied and each lane's keepers pass.

## 6. Preservation review

Before claiming completion, compare deleted coverage against the keepers in a
separate review pass for each boundary group. Look for contracts that lost
their only proof and new assertions that cannot fail, such as a rejection case
the production code never reaches. Use independent reviewers when available.

For each restored contract, make one deliberate **mutation** of the production
owner and confirm the keeper goes red. Then restore the source byte for byte.

Done when every reported gap is restored or rejected with source evidence, and
every restored contract has a caught mutation.

## 7. Product defects

A baseline failure that survives into a keeper may be a product bug. Reproduce
it before fixing it at its owner. Prove the fix through the real behavior path,
with a **control** run that shows the old behavior. Record unrelated product
discrepancies as follow-ups.

Done when each repaired defect has a failing control and a passing candidate
in the same test environment.

## 8. Reconcile and hand off

If the baseline moves during the campaign, reconcile new or changed tests with
the keeper suites. Confirm each new regression still has a home. Rerun the whole
subsystem suite and repeat any relevant end-to-end proof on the final revision.

Hand off with the [SKILL.md](SKILL.md) report, plus:

- baseline and final test/support line counts, with production counted separately;
- lanes, retired layers, and keepers;
- preservation gaps found and their mutations;
- product defects with control and candidate proof.
