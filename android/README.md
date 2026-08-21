# Brake APK (demo sideload)

**LAB. Not core. Not Play Store.** Same law as the URL face: pocket folder outside this repo, Yes is `yes()`, GET-equivalent (opening the app) is not Yes.

Face contract: `dev/23_mobile-planning-demo/output/BRAKE.md`

This Next (`people-app-phone-seat`): **APK first**. URL / pocket-face is the sibling fallback — not a second Next.

```bash
sh scripts/sync-pocket-engine.sh
# JDK 17 + SDK 34 + ./gradlew  (this Nix host used ~/.jdk/temurin-17 + ~/.android-sdk-mechanicall)
cd android && ./gradlew :app:assembleDebug
sh scripts/sideload-apk-via-edge.sh   # A33 via mbp-edge ADB
```

## What this chrome is

Android Compose + Chaquopy calling `aether_pocket.py`, which execs the same `bin/aether` when a POSIX `aether` is on PATH / `AETHER_HOME`.

On a stock phone there is no bash `aether`. For a sitting either:

1. Sideload the APK **and** provide `AETHER_HOME` via a copied `aether` + toybox/Termux (same law), or  
2. Use the **URL face** (host already has `aether`) and treat the APK as optional chrome.

## Build (needs Android SDK — not in the default Nix shell)

```bash
sh scripts/sync-pocket-engine.sh
cd android
# need: JDK 17, Android SDK 34, gradle wrapper jar
./gradlew :app:assembleDebug
# APK: app/build/outputs/apk/debug/app-debug.apk
```

Sideload: `sh scripts/sideload-apk-via-edge.sh` (USB / `adb install -r` via mbp-edge). Bind `/sdcard/mechanicall-pocket` (already on the A33, or a copy of `examples/pocket-demo-client`), never this repo. Opening the app is not Yes.

Refuse bind: operator tree (`PRODUCT.md` + `bin/aether` + `CORE_PRINCIPLES.md` + `AGENTS.md`).
