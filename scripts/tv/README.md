# TV / House Desk scripts

| Script | Purpose |
|--------|---------|
| `sync-movies-index.py` | Build `library/movies-index.md` from ADB or local Movies |
| `push-mechanicall-seed.sh` | Push domain seed to `/sdcard/Mechanicall/` (no keys) |
| `desk-smoke.sh` | Unit tests + health/empty/HTML smoke (`--live` for LLM turn) |
| `open-desk-on-tv.sh` | ADB VIEW intent → desk URL (no APK) |
| `build-house-desk-apk.sh` | Build Leanback WebView APK if SDK present |
| `install-house-desk-apk.sh` | `adb install` Desk tile |
| `install-desk-on-device.sh` | Full live install: index + seed + open Desk on TV |
| `launch-home-row.sh` | Open Kodi · Desk · Remote HTML home on TV |

## Operator flow

```bash
cd /home/anphuni/mechanicall-os
./scripts/tv/desk-smoke.sh --live
python3 scripts/tv/sync-movies-index.py --root domains/house-tv-desk --adb
./scripts/tv/push-mechanicall-seed.sh
aether desk-serve --lan --port 8788 domains/house-tv-desk
# phone/laptop on LAN → http://<myarch-ip>:8788/
# or: ./scripts/tv/open-desk-on-tv.sh
```

House remote (D-pad / Kodi / **Desk chat** / **Desk on TV**):  
`python3 ~/one-off-TV-box-OS/scripts/house-remote.py` → `:8787`
