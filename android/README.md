# Brake APK (demo sideload)

**LAB. Not core. Not Play Store.** Same law as the URL face: pocket folder outside this repo, Yes is `yes()`, GET-equivalent (opening the app) is not Yes.

Face contract: `dev/23_mobile-planning-demo/output/BRAKE.md`

This Next (`people-app-phone-seat`): **APK first**. URL / pocket-face is the sibling fallback — not a second Next.

```bash
sh scripts/sync-pocket-engine.sh
# JDK 17 + SDK 36 + Gradle 8.11.1  (this Nix host: ~/.jdk/temurin-17 + ~/.android-sdk-mechanicall)
cd android && ./gradlew :app:assembleDebug   # or :app:bundleRelease
# Play upload keystore is off git: ~/.mechanicall/play-upload.properties
sh scripts/sideload-apk-via-edge.sh   # A33 via mbp-edge ADB — not an LTE receipt
```

## What this chrome is

Android Compose + Chaquopy calling `aether_pocket.py`. **Decide → Publish** is native (`pocket_approve` / `pocket_reject`): apply PROPOSE, then Status/Approval + events + DECISIONS + RECEIPT. No POSIX `bin/aether` on the phone.

Desktop `aether current` / `validate` still use the CLI when present. Opening the app is not Yes. Why is required.

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
