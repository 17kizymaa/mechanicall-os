# Receipt — smoke-verify

**Action id:** `smoke-verify`  
**Date:** 2026-08-04  
**Host:** myarch (desktop)  
**Authority:** Next=smoke-verify · Phase/Status/Approval=APPROVE/APPROVED/APPROVED  
**Preflight:** ALLOW  

## Scope

Re-prove protocol-complete alpha without publish/tag and without mutating authority Next (except what human already did). Sandbox demo never touches live CURRENT body beyond header fields already set by human.

## Commands run

| Step | Command | Result |
|------|---------|--------|
| 1 | `aether preflight smoke-verify` | ALLOW |
| 2 | `aether demo` | **DEMO OK** (exit 0) — refuse → allow → no silent pass → approve → re-SELECT → ledger |
| 3 | `aether demo --quiet` | **DEMO OK** (exit 0) |
| 4 | `aether current validate` | **VALIDATE: OK** (warn: all APPROVE(D) — expected until human re-SELECT) |
| 5 | `aether brief` | Next=smoke-verify; preflight would ALLOW; drift noted |
| 6 | `aether probe smoke-verify` | ALLOW (exit 0) |
| 7 | `aether probe not-the-next` | REFUSE (exit 2) |
| 8 | `aether drift` | exit 1 — ~103 dirty paths (report only) |
| 9 | `sh tests/run.sh` | **ALL PASSED** (pytest 41 + full aether integration + ci-control-layer-gates) |

## Claim-surface files present

- `docs/PROTOCOL-TEST-SURFACE.md`
- `docs/GROK-SEAT.md`
- `docs/PROTOCOL-LAB.md`
- `docs/RELEASE-NOTES-ALPHA.md`
- `scripts/protocol-demo.sh`
- `scripts/grok-aether-brief.sh`

## Demo chain observed (sandbox)

1. REFUSE — preflight outside Next  
2. ALLOW — preflight Next  
3. NO SILENT PASS — Approval stays PENDING without human  
4. APPROVE — human-labelled  
5. RE-SELECT — `aether next` demo-one → demo-two  
6. LEDGER — events chain intact  

## Not done (by design)

- Publish / tag release  
- Blocking Grok hooks  
- Cleaning the dirty tree / committing  
- Human re-SELECT off `smoke-verify` after this receipt  

## Note: stale CURRENT prose

Header fields are correct (`**Next:** smoke-verify`). Body section **“Next allowed action”** still describes `implement-remaining-waves` (left from prior cycle). Models must not hand-rewrite CURRENT; human may refresh prose after re-SELECT or via a dedicated doc edit you authorize.

## Verdict

**SMOKE PASS** — protocol demo, validate, probe, brief, drift, and full test suite green.

## Human gate (suggested)

When satisfied:

```bash
# pick the next objective, e.g. park / freeze / commit-hygiene
aether next <new-action-id>
```

Or leave Next as `smoke-verify` until you choose.
