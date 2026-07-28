# VERIFICATION — House TV Desk (stages 01–07)

**Date:** 2026-07-28  
**Host:** myarch  
**Domain:** `domains/house-tv-desk`  
**Runner:** `scripts/tv/desk-smoke.sh --live`

## Automated results

| Check | Result | Notes |
|-------|--------|-------|
| Desk unit tests | **PASS** | 7 tests |
| Desk API unit tests | **PASS** | 7 tests |
| `/health` | **PASS** | `openrouter:openrouter/free` |
| Empty message rejected | **PASS** | `error: empty` (silence ≠ permission) |
| HTML privacy | **PASS** | page contains privacy |
| Live movie-suggest | **PASS** | Model replied `**Big Buck Bunny (2008)**` from library index |
| ADB movies sync | **SKIP** | no device attached at run time |
| Kodi launch from desk | **SKIP** | needs eME640 ADB |
| Desk on TV VIEW intent | **SKIP** | needs eME640 ADB |
| Leanback APK build | **PENDING** | needs ANDROID_HOME / SDK |

## Parent UAT checklist (human)

| # | Step | Pass? |
|---|------|-------|
| 1 | `aether desk-serve --lan --port 8788 domains/house-tv-desk` | |
| 2 | Phone/laptop opens Desk; privacy visible | |
| 3 | Ask for a funny short film on disk → title makes sense | |
| 4 | Empty send does nothing harmful | |
| 5 | House Remote → **Desk chat** opens Desk | |
| 6 | **Open Kodi** still starts Kodi (device on) | |
| 7 | Optional: `open-desk-on-tv.sh` or Desk APK tile | |

## Doctrine checks

| Rule | Status |
|------|--------|
| Model never writes CURRENT | OK (no code path) |
| Keys not in HTML/APK/seed | OK |
| No local heavy LLM on eME640 | OK (OpenRouter on myarch) |
| Kodi remains entertainment king | OK (propose only) |

## Gaps / next human actions

1. Power eME640 on LAN → re-run `desk-smoke.sh --live` + ADB index sync  
2. Parent couch session with checklist above  
3. Build APK when Android SDK available (`scripts/tv/build-house-desk-apk.sh`)
