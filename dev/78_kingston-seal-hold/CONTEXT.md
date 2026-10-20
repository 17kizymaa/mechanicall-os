# 78 — Kingston seal hold

**Layer 1 for this folder only.** Not CURRENT. Not a Yes.

A 2026-10-16 reading of one archive clock. The chat asked an agent to find a Kingston key, open the volume, and later remove that key after a training Next. The volume stayed sealed.

## Inputs
- `~/MODEL+RAG/rag-archive-manager/CURRENT.md` as read on 2026-10-16 after the parenthetical edit
- Applied backup `.aether/current-before/CURRENT-20261016T122019Z-2719349.md`
- `.aether/events.jsonl` from `2026-10-16T12:12:53Z` through `2026-10-16T13:08:46Z`
- `.aether/preflight.jsonl` rows on 2026-10-16
- `artifacts/EVENTS-LOG-SEQUENTIAL-IDS.md`
- Two `lsblk` readings the same day: Kingston by-id absent, no mapper, `/mnt/kingston-rag` not mounted

## Process
Write the data point. Leave both live CURRENT files alone. Leave the archive sealed.

## Outputs
- `output/CASE-STUDY.md`

## Halt
Do not `aether approve`, `reject`, `next`, or `apply`. Do not edit either `CURRENT.md`. Do not search for a key, open the volume, train, or delete key material. Do not put key material, a key path, or an unlock procedure in this folder.
