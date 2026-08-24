# 01 — assemble debug APK

## Inputs
- Layer 1: `../CONTEXT.md`
- Layer 3: `../../../android/README.md`
- Layer 3: `../../../scripts/sync-pocket-engine.sh`
- Layer 3: `../../../python/aether_pocket.py`

## Process
You are the assembler.

1. `sh scripts/sync-pocket-engine.sh`
2. Ensure `android/gradlew` + wrapper jar exist (not committed last check).
3. Build with JDK 17 + `ANDROID_HOME` SDK 34. This Nix/Arch host default is JDK 26 and no SDK — use a local Temurin 17 + cmdline-tools install **outside the repo**.
4. Do not claim an APK exists if `app/build/outputs/apk/debug/app-debug.apk` is missing.
5. Do not start pocket-face.

## Outputs
- `output/CAPABILITY.md` — JDK/SDK/gradlew/ADB facts
- `output/RECEIPT.md` — assemble result (path or honest miss)
