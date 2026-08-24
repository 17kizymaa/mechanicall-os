## Inputs
- Layer 1: live `CURRENT.md` Next `sit-distro-gate` action (1)
- Layer 3: `.aether/proposals/13_FIRST_DISTRIBUTION_PR_GPT5.6.md` finding 1
- Layer 3: `python/aether_inbox.py` `_unzip_to`, `python/aether_drop.py` (do not start)
- Layer 4: `tests/test_aether_inbox.py`

## Process
Contain zip extraction. Reject absolute, backslash, drive, `..`, symlink/special members. Resolve each target under dest. Raise `PocketError` and do not stage a partial offer. Adversarial tests. Sync Chaquopy copy via `scripts/sync-pocket-engine.sh`. Do **not** restart drop.

## Outputs
- RECEIPT.md -> output/
