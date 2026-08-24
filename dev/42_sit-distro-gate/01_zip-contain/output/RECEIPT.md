# RECEIPT — 01_zip-contain

**Not Yes. Not drop-up.** Live Next `sit-distro-gate` action (1). Preflight allowed.

## Done

`python/aether_inbox.py` `_unzip_to`:

- Rejects absolute Unix paths, backslash paths, drive letters, `..` parts, NUL, symlink/special Unix modes.
- Resolves each member under `dest`; `PocketError` if it would escape.
- `poll_incoming` rmtree the offer dir if unzip refuses (no partial stage).
- Honest skip of `NOTICE.json` / SKIP names unchanged.

Chaquopy copy synced: `scripts/sync-pocket-engine.sh`.

## Tests

`python3 tests/test_aether_inbox.py` — 14 OK, including:

- nested file stays inside
- `../` slip
- absolute Unix
- backslash + `C:/`
- symlink member
- poll of a malicious lab zip does not notify and does not write outside

## Not done (this stage)

- Drop `:8765` still **down** (CURRENT: do not restart until this lands — landed in tree; **do not** start until you say storm-up/drop-up or Continue to a drop stage).
- Stock-phone Publish (action 2).
- API 36 / AAB (action 3).
- LTE receipt / Play Console (human).

Walkers did not tap Confirm. Models did not approve.
