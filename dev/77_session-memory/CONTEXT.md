# 77_session-memory

**Action id:** `session-memory`
**Law:** root CURRENT.md. One Next. Not this halt until selected.

## Goal
Agent-agnostic session memory as a .memory/ sidecar: append-only capture,
deferred structure, human-reviewed via git. Grok Build memory as the study;
no Grok dependency.

## Inputs
- CORE_PRINCIPLES.md (sidecars; capture sacred / structure deferred)
- docs/RHIZOME.md
- .memory/principles-reminder.md (existing; stays)
- .aether/events.jsonl, DECISIONS.md (what memory must NOT duplicate)

## Process
1. Scaffold .memory/ (README, TAIL, ledger.jsonl, topics/, rollup/)
2. Add one row to docs/AGENT-AGNOSTIC-COLD-START.md step 2 table
3. Receipt

## Outputs
- .memory/README.md
- .memory/TAIL
- .memory/ledger.jsonl
- .memory/topics/.keep
- .memory/rollup/.keep
- docs/AGENT-AGNOSTIC-COLD-START.md (modified)
- output/RECEIPT.md

## Not this stage
- Scripts or an aether subcommand (three repeats first)
- Any write to CURRENT.md, DECISIONS.md, .aether/
- Restating law into topics
