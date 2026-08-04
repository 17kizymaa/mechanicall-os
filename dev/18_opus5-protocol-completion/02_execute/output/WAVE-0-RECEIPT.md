# Wave 0 receipt — Opus 5 lead + host execute

**Date:** 2026-08-04  
**Lead:** `anthropic/claude-opus-5` (OpenRouter, Desktop/.env **line 2** sk-or key)  
**Host:** Grok Build (tools)

## Key

- Line 1 sk-or: models list only / chat 401  
- Line 2 sk-or: chat OK (`pong` + full lead brief)  
- `opus_lead.py` prefers last raw `sk-or-` line when env unset  

## Opus lead artifact

`01_lead/output/WAVE-LEAD-2026-08-04.md` — waves 0–5, proposed Next `proto-lifecycle-reselect`

## Implemented (Wave 0 core)

| Item | Status |
|------|--------|
| `aether next <id> [path] [--reason]` | Done — refuse unapproved / unchanged; re-SELECT |
| Help text | Done |
| Tests in `tests/run.sh` | Done — validate + next cycle |
| AGENTS.md never hand-edit Next | Done |
| PROTOCOL-TEST-SURFACE claim map | Updated |
| AETHER_ROOT project override | **Skipped** — already install-root; use path arg for sandbox |

## Tests

`sh tests/run.sh` → **ALL PASSED**

## Human gate (Opus)

Proposed Next action-id (not applied by models):

```
proto-lifecycle-reselect
```

After human re-SELECT of live CURRENT:

```sh
# only if Approval APPROVED (already is):
aether next proto-lifecycle-reselect
# or hand-edit thin gate then approve as you prefer
```

## Note on AETHER_ROOT

In this codebase `AETHER_ROOT` = **aether install root** (python/, docs). Project Domain path is the optional path argument to commands. Sandbox isolation = `aether next foo /tmp/proj` style, not env rename.
