# Opus 5 peer-review call — FAILED

**Date:** 2026-08-04  
**Intended model:** `anthropic/claude-opus-5` via OpenRouter  
**Status:** **not obtained**  

## Error

Both Desktop `.env` raw `sk-or-…` lines (inventory lines 1–2):

- `GET /api/v1/models` → 200 (list returns)  
- `POST /api/v1/chat/completions` → **401** `{"error":{"message":"User not found.","code":401}}`

No chat completion available. Keys appear invalid/orphaned for completions despite models listing.

## Artifacts prepared for re-run

| File | Role |
|------|------|
| `PEER-INPUT-AWARENESS-SCAFFOLD-CRITIQUE-LEGACY.md` | Archived user paste |
| `PEER-BRIEF-OPUS5-2026-08-04.md` | Ground-truth brief + required output schema |
| `PEER-REVIEW-HOST-ADJUDICATION-2026-08-04.md` | Host interim peer doc (not Opus) |

## Re-run when key works

```bash
# set working OPENROUTER_API_KEY first
python3 - <<'PY'
# same call as session, or:
# extend opus_lead.py with --role peer
PY
```

Or:

```bash
export OPENROUTER_API_KEY='…'   # working key
# host will re-invoke peer call against PEER-BRIEF + PEER-INPUT
```

## Human

Replace/refresh OpenRouter keys in Desktop `.env`. Do not commit keys.
