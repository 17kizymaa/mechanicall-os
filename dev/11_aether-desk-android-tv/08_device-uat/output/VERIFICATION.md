# VERIFICATION — device UAT (stage 08) · live install 2026-07-28

**Device:** eME640 `192.168.1.235:5555` · Android 8.1 · abi x86  
**Host:** myarch `192.168.1.241`  
**Desk:** `:8788` · **Remote:** `:8787`

## Automated / operator checks

| Check | Result |
|-------|--------|
| ADB device online | **PASS** |
| Movies on `/sdcard/Movies` | **PASS** (Big Buck Bunny full + sample) |
| Index sync (video only) | **PASS** (2 titles) |
| Seed `/sdcard/Mechanicall/` | **PASS** (CURRENT, library, bridge.url, helpers) |
| Device → myarch `/health` | **PASS** (wget from device) |
| Open Desk on TV (WebView shell) | **PASS** (focus WebViewBrowserActivity) |
| Launch Kodi via ADB | **PASS** |
| Live chat movie suggest | **PASS** → `Big Buck Bunny` |
| Home row `/home` | **PASS** (HTTP 200 + opened on TV) |
| Keys on device | **PASS** (none pushed) |

## Parent demo checklist (client-one)

| # | Step | Notes |
|---|------|-------|
| 1 | HDMI shows Desk or Home row | `launch-home-row.sh` if blank |
| 2 | Privacy visible on Desk | |
| 3 | Ask funny film on disk | Expect Bunny |
| 4 | Open Kodi → play Bunny | Entertainment king |
| 5 | Empty send does nothing | silence ≠ yes |

Demo card: `~/one-off-TV-box-OS/docs/CLIENT-ONE-DEMO.md`
