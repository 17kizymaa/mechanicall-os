# RECEIPT — 02_implement sit-join-workshop

**Not Decide. Not Yes.** Preflight ALLOW `sit-join-workshop`. Models did not approve. Walkers did not Confirm.

## Built

- **Hunk ICM** (`python/aether_pocket.py`): `list_hunks` / `apply_hunk` / `reject_hunk` / `accept_hunk` write PROPOSE only. `draft_chat(..., focus=)` sends one hunk, refuses whole CURRENT in the prompt, may merge schema onto PROPOSE.
- **JOIN** (`join_accept` / `join_status`): paste invite or auth key; fingerprint only in `.aether/tailnet.json`; never stores the secret; refuses `17kizymaa`; probe MagicDNS `myarch:11434`. Status not-on-net / invited / connected. Not Yes.
- **WAKE** (`wake_desk` + `scripts/wol-wake-listen.py`): POST `http://wol-pi:7077/wake` by default. Refuses `0.0.0.0`. MAC from `WOL_MAC` env on the Pi, not git.
- **Face:** paper palette; DESK strip after bind (JOIN well + WAKE); Plan shows published `CURRENT.md`; Draft is Suggesting (LIVE vs proposed hunk, Accept/Reject, SEND with focus); Decide copy “Publish the proposal.”
- Version `0.14.0-sit` (versionCode 15). Engine copied into Chaquopy via `scripts/sync-pocket-engine.sh`.

## Honest gap

- **libtailscale/tsnet JNI is not in this APK.** JOIN consumes paste, records fingerprint, and probes. “Connected” only if `myarch:11434` answers. Shipping gomobile tsnet is the remaining native link — do not claim the phone is a Tailscale node without that probe.
- STORM / APK install is **03_verify**. Go-git not run.

## Tests

- `python3 tests/test_aether_pocket.py` — 39 OK (hunk / join secret / wake public refuse / focus draft).
- `python3 python/app_verify.py` — B4 updated to accept hunk workshop (listHunks + LIVE/DRAFT).

## Never

- CURRENT bytes from JOIN/WAKE/hunk/Send
- Invite in git
- VpnService
- Confirm
