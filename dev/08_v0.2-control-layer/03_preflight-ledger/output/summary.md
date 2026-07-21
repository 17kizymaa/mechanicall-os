# Stage 03 — Preflight and event ledger (complete)

## Done
- `aether preflight <action>` — allow/refuse with readable reason (exit 0/1)
- Prohibited list + Next pin + blocked statuses
- `.aether/events.jsonl` append-only (flock when available; one JSON object per line)
- `aether approve` / `aether reject` — human only; reject → Phase SELECT, no auto-rebuild
- `aether artifact` — metadata under `.aether/artifacts/` + event
- `aether event` — freeform note
- `DECISIONS.md` trail on approve/reject

## Exit gate
`aether preflight rough-v6` refused while blocked; refusal logged in events.jsonl.
