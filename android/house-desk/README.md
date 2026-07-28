# House Desk — Android TV WebView shell (Leanback launcher tile)

Thin APK that loads the myarch desk URL from `/sdcard/Mechanicall/bridge.url`  
(or `http://192.168.1.241:8788/` fallback). **No API keys in the app.**

## Requirements

- Android SDK with build-tools; JDK 11+
- Target: **API 26–27**, `abiFilters 'x86'` (ATV8 32-bit / eME640)
- Device with desk bridge reachable on LAN

## Configure URL on device

```bash
# from mechanicall-os
./scripts/tv/push-mechanicall-seed.sh
# writes /sdcard/Mechanicall/bridge.url
```

## Build & install

```bash
export ANDROID_HOME=~/Android/Sdk   # or your SDK path
cd android/house-desk
./gradlew :app:assembleDebug
adb connect 192.168.1.235:5555
adb install -r app/build/outputs/apk/debug/app-debug.apk
```

Or:

```bash
../../scripts/tv/build-house-desk-apk.sh
../../scripts/tv/install-house-desk-apk.sh
```

## Without SDK

Use the zero-APK path (opens system browser):

```bash
./scripts/tv/open-desk-on-tv.sh
```

## Product doctrine

- Propose-only chat lives on **myarch** (`aether desk-serve`)
- This APK is a **view**, not an authority layer
- Kodi remains the movie player
