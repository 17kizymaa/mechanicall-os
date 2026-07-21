# Mechanicall OS v0.2 — Ready for review

**Branch:** fix/gpt56-review-p0  
**Handoff:** research/speculative/mechanicall-os-v0.2.handoff.md  
**Tests:** `./tests/run.sh` — all pass

## Authorized mission delivered

Filesystem-native authority and approval layer. Not the PDF nervous system.

## New CLI

| Command | Role |
|---------|------|
| `aether current` / `current init` | Show / create CURRENT.md |
| `aether preflight <action>` | Gate consequential actions |
| `aether approve [reason]` | Human APPROVED |
| `aether reject [reason]` | Human REJECTED → SELECT |
| `aether event <msg>` | Freeform event log |
| `aether artifact <path>` | Register output metadata |

## Key files

- SPEC-v0.2.md, NOT-IMPLEMENTED.md, README.md
- aether (v0.2 commands)
- tests/run.sh (v0.2 cases)
- examples/reel-control/, examples/dev-task/

## Review checklist

1. Read SPEC-v0.2.md — semantics match intent?
2. Walk examples/reel-control/README.md sequence
3. Run `./tests/run.sh`
4. Confirm NOT-IMPLEMENTED.md matches your denial list
5. Decide: merge to master / ship alpha / more missions

## Explicitly NOT done (by design)

PostgreSQL, pgvector, LangGraph, Cortex/Ganglion, sandboxes, web dashboard,
autonomous video agent, industrial claims.
