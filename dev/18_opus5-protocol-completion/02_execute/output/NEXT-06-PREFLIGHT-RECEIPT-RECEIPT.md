# Receipt — next-06-preflight-receipt

**Date:** 2026-08-04  
**Action:** `next-06-preflight-receipt` · APPROVED  
**Peer:** Opus 5 🟠-2 / NEXT-06  

## Behaviour

| Step | Effect |
|------|--------|
| `aether preflight …` | Writes `.aether/preflight-last` + appends `.aether/preflight.jsonl` |
| `aether approve …` | Prints `preflight: PASS \| STALE \| ABSENT` then continues (non-blocking) |

### Fingerprint

- **Git tree:** `git:<HEAD>:d0|d1` (dirty bit from `status --porcelain`)  
- **Non-git:** `tree:<cksum>` over all files except `.aether/*`

### Line format (`preflight-last`)

```text
ts=…|action=…|result=allowed|ec=0|fp=git:abc:d1
```

## Also fixed

`aether approve <reason> <path>` peels trailing directory (was only sole-arg path).

## Tests

`ok: preflight receipt PASS/STALE/ABSENT` in `tests/run.sh` · suite **ALL PASSED**

## Spec

SPEC-v0.2 preflight rule 7: gate may be human; gate must leave a trace.

## Human gate

```bash
aether next next-07-shellcheck
# or park-protocol-alpha
```
