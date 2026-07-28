# CURRENT

**Objective:** Transfer this operator session to client-one (eMachine E640 / Alpine) and reconfigure host WLAN so the device is reachable on LAN without preferring USB tethering.
**Phase:** EXECUTE
**Status:** READY-FOR-REVIEW
**Baseline:** session/client-one-delroy-reconfigure@b7dc96d
**Next:** reconfigure-wlan
**Approval:** PENDING

## Keep
- Agent + git branch stay on operator Arch host (`myarch` / mechanicall-os source)
- Plain Markdown transfer package under `dev/10_client-one-emachine/`
- TTY / TUI-first on thermal-limited eMachine (no GUI required for alpha demo)
- Future INIT target: `/home/Delroy` on the client (user name Delroy)
- Prefer WLAN → LAN for client reachability

## Reject
- Preferring USB tethering as steady-state networking
- Creating the client project folder or running `aether init` before SSH + WLAN work
- Destructive repartition / wipe of Windows 7 archive or unknown AndroidOS without explicit later auth
- Installing a full GUI on the eMachine as a prerequisite
- Treating silence or chat as permission beyond this CURRENT

## Limits
- This stage authorizes **RECONFIGURE** (network + session transfer prep) only
- No project-root INIT on client until a later CURRENT Next unlocks it
- No forced disk mount until a human picks a partition from the decision tree
- Do not commit large binaries (qcow2, result links) into the session branch

## Next allowed action
Reconfigure Alpine WLAN on the eMachine so `wlan0` associates and gets a LAN address; keep the operator-side transfer package ready for `scp`/`rsync` after SSH. Action id: `reconfigure-wlan`.

## Approval condition
Human confirms WLAN is up (or accepts documented fallback), reviews `output/` package, then either:
- `aether approve "wlan up; transfer ready"` from this stage directory, or
- explicit chat: proceed to SSH transfer / INIT under `/home/Delroy`.

## Prohibited
- prefer-usb-tether
- client-project-init-now
- wipe-disk
- install-gui-required
- expand-to-club-cortex
- autonomous-repartition
