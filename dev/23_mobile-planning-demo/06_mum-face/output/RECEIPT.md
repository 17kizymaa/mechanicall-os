# Receipt — mum LAN face

**2026-08-16** · demo · GET is not Yes

| | |
|--|--|
| URL | http://192.168.0.51:8765/ |
| Bind | 192.168.0.51:8765 (LAN, not 0.0.0.0) |
| Twin | `~/mechanicall-pocket` |
| Phone opener | `/sdcard/mechanicall-pocket/OPEN-SITTING.html` |
| A33 → face | `nc` to :8765 **ok** |
| CURRENT Next | still `name-the-outcome` (no approve) |
| Start | `sh scripts/serve-pocket-face.sh` |

Yes is POST + confirm dialog + `aether approve` on the twin, then push CURRENT/events back to the A33. I did not POST /yes.
