# Receipt — protocol-first re-centre

**Date:** 2026-08-04  
**Action id:** `protocol-first-current-schema`

## Why
- Peer wording pressure: product was drifting toward web Session / multi-seat.
- Client One: ~zero OpenRouter use after brief open — do not treat web as validated.
- Original direction: **CURRENT.md is the product** (local authority protocol).

## Landed
| Artifact | Role |
|----------|------|
| `docs/PROTOCOL.md` | Product core definition |
| `docs/READ-ORDER.md` | Peer/operator read path |
| `PRODUCT.md` / `START-HERE.md` | Reworded protocol-first |
| `NOT-IMPLEMENTED.md` | Website Session ≠ product definition |
| `python/aether_current.py` | Schema check/parse/template |
| `aether current check` | CLI entry |
| `tests/test_aether_current.py` + run.sh slice | Regression |

## Later (not this receipt)
- Intentional understanding-test web page (action facade over real protocol)
- Client One re-engage only after protocol story is clear

## Operator note
Do not confront client about unused OpenRouter key; use idle as market signal for protocol-first.
