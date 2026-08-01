# Desk removed (unsacred)

**When:** 2026-07-31  
**Why:** Desk was soft chat with CURRENT as ambient context — not Domain sovereignty. Sacred seats are **panel** (human gates) and **shell** (Domain-bound agent).

## Removed

| Former | Replacement |
|--------|-------------|
| `aether desk` | `aether shell` (default agent=peer) |
| `aether desk-serve` | `aether shell` · `aether panel` |
| `python/aether_desk.py` | Shared helpers → `python/aether_fs.py` |
| `python/aether_desk_api.py` | deleted |
| desk unit tests | shell unit tests in `tests/run.sh` |

CLI still accepts `desk` / `desk-serve` only to **die** with a redirect message.

## Still present (not the desk product)

- Domain folder name `domains/house-tv-desk/` (House TV Domain — rename later if desired)
- Historical notes under `dev/11_aether-desk-android-tv/`
- Android `android/house-desk/` scaffold (needs new host path if revived)

## Sacred path

```bash
aether panel .     # human approve / preflight
aether shell .     # Domain REPL · peer / grok agents
```
