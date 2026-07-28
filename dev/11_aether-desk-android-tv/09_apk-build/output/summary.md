# 09_apk-build — runtime path shipped; binary APK deferred

## Shipped (installable without SDK)

| Path | Status |
|------|--------|
| WebView shell VIEW intent | **Installed live** as Desk surface |
| `install-desk-on-device.sh` | **Green** on eME640 |
| `open-desk-on-tv.sh` / `launch-home-row.sh` | **Green** |
| Scaffold `android/house-desk/` | Present for future SDK build |

## Not produced this session

- Signed/debug `.apk` binary (no `ANDROID_HOME`; Docker Android image not cached / pull aborted)
- When SDK available: `scripts/tv/build-house-desk-apk.sh` + `install-house-desk-apk.sh`

## Product decision

For client-one demo, **WebView browser + bridge.url** is the Desk “app.”  
Custom Leanback APK remains optional polish, not demo-blocking.
