# CURRENT

**Objective:** Land preflight CLI tests without expanding scope.
**Phase:** EXECUTE
**Status:** BLOCKED-PENDING-HUMAN
**Baseline:** plan-v1
**Next:** write-tests
**Approval:** PENDING

## Keep
- shell-only preflight
- filesystem events.jsonl

## Reject
- rewrite in another language
- database-backed state

## Limits
- no new dependencies
- no web dashboard

## Next allowed action
Add integration tests for preflight (action id: `write-tests`).

## Approval condition
Human runs: `aether approve "tests green"`.

## Prohibited
- rewrite-in-rust
- add-postgres
- add-vector-db
- expand-to-dag-engine
