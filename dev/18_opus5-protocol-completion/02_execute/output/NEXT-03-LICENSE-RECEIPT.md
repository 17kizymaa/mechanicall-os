# Receipt — next-03-license

**Date:** 2026-08-04  
**Action:** `next-03-license` · APPROVED  
**Peer:** Opus 5 🔴-2 / NEXT-03  

## Finding

`LICENSE` was **already present** on the tree (Apache License 2.0, tracked since `12f6429 docs(alpha): Apache-2.0 license…`). README already linked it. Opus peer “no LICENSE” was **stale relative to this host/master**.

## Choice

**Keep Apache-2.0** (not switch to MIT). Matches existing LICENSE, README Status line, and copyright appendix (2026 anphuni / Mechanicall OS contributors).

## Work done this Next

| File | Change |
|------|--------|
| `LICENSE` | Unchanged (already complete Apache-2.0 + copyright notice) |
| `PRODUCT.md` | New **License** section: repo vs packaged distro vs Session lab |
| `README.md` | License line expanded (vendor under Apache-2.0; Session ≠ open SaaS) |
| `START-HERE.md` | Read-order item 5b → LICENSE |
| `docs/SINGLE-APP-DISTRIBUTION.md` | Inherit Apache-2.0 for packages; Session pointer |

## Acceptance (Opus NEXT-03)

| Criterion | Status |
|-----------|--------|
| License file present | **Yes** (pre-existing) |
| Stated in README | **Yes** (strengthened) |
| Session-lab terms explicit | **Yes** (PRODUCT + README + SINGLE-APP) |
| Third party can vendor `aether` without asking | **Yes** under Apache-2.0 |

## Human gate

```bash
aether next next-04-exit-codes
# or next-05-loc-decision / park-protocol-alpha
```
