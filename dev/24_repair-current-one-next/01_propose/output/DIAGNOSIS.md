# Diagnosis — one file, three Nexts

**Date:** 2026-08-18  
**Read-only check:** `aether current .` · `aether current validate .`

| Pin | Value | Source |
|-----|--------|--------|
| Header `**Next:**` | `mobile-planning-demo` | live `CURRENT.md` |
| Body `**Action id:**` | `casual-core-interface` | live `CURRENT.md` |
| Last `next_selected` | `casual-core-interface` (2026-08-11T19:13:33Z) | `.aether/events.jsonl` |
| `next_selected` → `mobile-planning-demo` | **none** | events |
| `aether current validate` | OK with warnings (APPROVE lifecycle) | does **not** fail this split |
| Preflight 2026-08-17T16:53:41Z | `mobile-planning-demo` allowed; `casual-core-interface` refused | events |
| Claimed contract | `docs/CASUAL-CORE-INTERFACE.md` | **file missing** |
| Demo sitting | cancelled 2026-08-16 | `dev/23_mobile-planning-demo/PARKED.md` |

`aether next mobile-planning-demo` will **refuse** (`next unchanged`) because the header already has that id. A missing events row cannot be created that way.

`aether next casual-core-interface` **will** run: header ≠ that id. It also resets Phase/Status/Approval to SELECT / ACTIVE / PENDING.

## What each repair makes true

| Option | After apply, the one Next is | Honest because | Residual |
|--------|------------------------------|----------------|----------|
| **A** | `mobile-planning-demo` | Matches the header `aether` already pins | No `next_selected` row unless you later bounce Next (do not bounce just to fake a receipt) |
| **B** | `casual-core-interface` | Matches last real `next_selected` + body | Mobile demo stays parked lab; do not also implement it here |
| **C** | `hold-one-next` | Sitting cancelled; contract file missing; do not implement either | You must re-SELECT a real Next later (Play Store would be a **new** propose, not this file) |
