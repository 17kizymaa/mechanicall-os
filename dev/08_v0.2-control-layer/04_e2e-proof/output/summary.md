# Stage 04 — End-to-end proof (complete for review)

## Done
- `examples/reel-control/` — reel stop-before-spiral fixture + operator README
- `examples/dev-task/` — non-reel authority model (proves not video-hardcoded)
- Integration tests in `tests/run.sh`:
  - prohibited refused
  - next allowed
  - non-next refused while blocked
  - reject → SELECT, no auto rebuild
  - approve events
  - seeds cannot unlock prohibited actions
  - no CURRENT → refuse all
  - non-reel project model

## Operator proof path
See `examples/reel-control/README.md`.

## Exit gate
New agent can enter the directory, read CURRENT.md, and correctly state what it may/may not do.
