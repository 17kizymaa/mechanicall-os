# CONTEXT — aether desk on Android TV ecosystem

## Goal
Ship propose-only aether desk as House TV’s AI surface: Python core + myarch bridge + couch HTML; Kodi stays primary.

## Defaults (approved 2026-07-28)
- HTML desk first (not APK)
- Keys on myarch only
- Domain: `domains/house-tv-desk/`
- LAN bind explicit for couch browser
- Offline myarch: not required for v1

## Stages
| Stage | Purpose |
|-------|---------|
| 01_contract | Domain CURRENT + plan copy |
| 02_core-extract | Pure desk_turn helpers |
| 03_bridge | desk-serve HTTP |
| 04_surface | Couch HTML UI |
| 05_ecosystem-hooks | remote↔desk links, ADB Kodi/TV open |
| 06_verify-uat | desk-smoke + VERIFICATION.md |
| 07_leanback-webview | WebView APK scaffold + open-desk-on-tv |
| 08_device-uat | Live ADB install + VERIFICATION |
| 09_apk-build | Runtime WebView install; APK binary when SDK |
| 10_launcher-row | `/home` tiles Kodi · Desk · Remote |

## Inputs
- `python/aether_desk.py`, `python/aether_llm.py`
- `~/one-off-TV-box-OS` house-remote + Kodi ops

## Outputs
- Working `aether desk-serve` + domain CURRENT
- Tests green
