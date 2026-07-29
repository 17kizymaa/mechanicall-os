# Desk product merge gate (P0)

From phone `28-7-26` session-1 review. Architecture GO; merge NO-GO until checked.

## P0 before merge to master

- [ ] CI green (`sh tests/run.sh`)
- [ ] POST /chat **never** accepts client `root`
- [ ] No wildcard CORS on Desk API
- [ ] Request body size limit
- [ ] `/health` does not leak absolute host path
- [ ] Honest history policy (browser + optional server log + transmission)
- [ ] Kingston/VM work **not** required in Desk product branch

## P1 after

- [ ] Test: CURRENT re-read between turns
- [ ] Test: root cannot be selected by client
- [ ] Test: transcript body persistence policy
- [ ] Proposal artifact against authority revision
- [ ] Second unguided Client-one Desk session

## Extract recipe

See later `EXTRACT-DESK-PRODUCT-BRANCH.md` — cherry-pick only desk python, tests, domain, tv scripts, concise docs.
