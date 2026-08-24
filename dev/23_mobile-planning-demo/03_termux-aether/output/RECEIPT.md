# Receipt — aether on A33 (Android sh, not Termux)

**2026-08-16** · demo · no approve

Termux is installed but **not debuggable** (`run-as` refused). Android `/system/bin/sh` + toybox (`grep` `sed` `awk` `flock` `cksum`) ran the real `aether` script.

| | |
|--|--|
| CLI | `/sdcard/mechanicall-aether/aether` (slim copy — no PRODUCT.md) |
| Pocket | `/sdcard/mechanicall-pocket` |
| `current` | OK — Next `name-the-outcome` |
| `current validate` | VALIDATE: OK |
| `brief` | preflight would ALLOW |
| `probe name-the-outcome` | ALLOW |
| Repeat CLI | `sh scripts/aether-on-a33.sh current` |
| Re-push CLI | `sh scripts/push-aether-via-edge.sh` |

Not done: Termux prefix install; human Yes (`approve`); live Ollama.

Wrapper on device: `/sdcard/mechanicall-pocket/aether.sh` (appends pocket path).
