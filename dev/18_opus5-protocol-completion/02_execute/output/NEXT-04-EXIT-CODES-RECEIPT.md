# Receipt — next-04-exit-codes

**Date:** 2026-08-04  
**Action:** `next-04-exit-codes` · APPROVED  
**Peer:** Opus 5 🟠-3 / NEXT-04  

## Normative table

| Code | Meaning |
|------|---------|
| **0** | Success / allowed |
| **1** | Internal error · also `drift` when dirty (report) |
| **2** | Usage (unknown verb, bad args, invalid flags) |
| **3** | Protocol refusal (`preflight` / `probe` / `next` gate) |

## Code

- `die` → exit **1** (internal)  
- `die_usage` → exit **2** (new)  
- Unknown verb → **2** (unchanged)  
- `cmd_preflight` refuse → **3** (was 1)  
- `cmd_probe` refuse → **3** (was 2)  
- `cmd_next` refuse → **3** (was 2)  
- Help line documents the table  

## Docs

- `SPEC-v0.2.md` — exit codes section + preflight rule 6  
- `docs/PROTOCOL-TEST-SURFACE.md` — claim map  

## Tests

- `tests/run.sh` — next refuse / probe refuse expect **3**  
- `tests/negative.sh` — usage **2**, no-CURRENT preflight **3**  
- **ALL PASSED**

## Smoke

```text
aether nexr           → 2
aether preflight      → 2
aether preflight bad  → 3
aether probe bad      → 3
```

## Human gate

```bash
aether next next-05-loc-decision
# or next-06-preflight-receipt / park
```
