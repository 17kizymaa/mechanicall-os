# Receipt — next-02-negative-tests

**Date:** 2026-08-04  
**Action:** `next-02-negative-tests` · APPROVED  
**Peer:** Opus 5 NEXT-02  

## Deliverable

| Path | Role |
|------|------|
| `tests/negative.sh` | Dedicated negative-path suite |
| `tests/run.sh` | Calls `sh tests/negative.sh` (replaces inline next-01 block) |

## Coverage

1. **Garbage verbs** — `nexr`, `xyzzy`, `notacommand` → exit **2**, `unknown command`  
2. **Authority near-misses** — single-char drop + first-two swap for:  
   `preflight approve reject next current probe demo brief drift`  
   plus explicit `preflght aprove distil nexxt preflghtt`  
3. **Missing required args** — `preflight` / `next` / `probe` / `event` → nonzero  
4. **No CURRENT** — preflight refuses (nonzero + refuse text)  
5. **Regressions** — path-as-cmd status still exit 0; `help` still works  

## Result

```text
sh tests/negative.sh  → ok: negative path suite (next-02)
sh tests/run.sh       → ALL PASSED
```

## Not in this Next

- shellcheck gate (NEXT-07)  
- full exit-code table 0/1/2/3 in SPEC (NEXT-04)  
- LICENSE (NEXT-03)  

## Human gate

```bash
aether next next-03-license
# or next-04-exit-codes / park
```
