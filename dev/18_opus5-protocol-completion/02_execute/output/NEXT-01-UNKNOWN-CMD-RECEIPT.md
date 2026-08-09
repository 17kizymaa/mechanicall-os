# Receipt — next-01-unknown-cmd

**Date:** 2026-08-04  
**Action:** `next-01-unknown-cmd` · APPROVED  
**Peer:** Opus 5 🔴-1  

## Change

`aether` main dispatch fallback:

| Before | After |
|--------|--------|
| `*) cmd_status "$cmd"` → exit 0, status-shaped output | If `[ -d "$cmd" ]` → `cmd_status` (path shortcut). Else stderr `unknown command` + **exit 2** |

## Tests

`tests/run.sh`:

- `aether nexr` → exit 2, message contains `unknown command`, no CURRENT status report  
- Near-miss: `preflght`, `aprove`, `distil`, `nexxt` → exit 2  
- Path shortcut: `aether $tmpdir` → exit 0, status root line  

**Result:** ALL PASSED (`ok: unknown command dies (exit 2); path-as-cmd ok`)

## Manual smoke

```text
./aether nexr     → exit 2
./aether preflght → exit 2
./aether .        → exit 0 (status)
```

## Not in this Next

- Full exit-code table 0/1/2/3 in SPEC (NEXT-04)  
- `die` still exits 1 for other errors  
- shellcheck / negative.sh as separate file (NEXT-02/07) — negative cases live in `tests/run.sh` for this wave  

## Human gate

When satisfied:

```bash
aether next next-02-negative-tests   # or next-03-license / park
```
