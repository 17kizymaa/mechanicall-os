# Receipt — people-app-phone-seat (2026-08-18)

Operator Next `people-app-phone-seat` **APPROVED**. Agent did not `approve` / `next` / `reject`.

## Done this turn

1. Assembled debug APK on **myarch** with Temurin 17 + SDK 34 (mbp-edge has ADB only).
2. Sideloaded to Samsung A33 via mbp-edge USB.
3. Bound existing pocket `/sdcard/mechanicall-pocket` (not mechanicall-os).
4. Tapped **Load**. Did **not** tap Yes.

| Artifact | Where |
|----------|--------|
| APK | `android/app/build/outputs/apk/debug/app-debug.apk` (42 MB, gitignored) |
| Repeat assemble | `cd android && JAVA_HOME=~/.jdk/temurin-17 ANDROID_HOME=~/.android-sdk-mechanicall ./gradlew :app:assembleDebug` |
| Repeat sideload | `sh scripts/sideload-apk-via-edge.sh` |
| Stage trail | `dev/27_people-app-phone-seat/` |

## Pocket law (phone, separate tree)

Still the old demo sitting: Next `name-the-outcome`, **REJECTED**. That Yes is the human on the phone.

## Not done / not claimed

- Play Store
- URL / pocket-face as a second Next (sibling only)
- Human Yes on the A33 pocket
- Rewriting `~/people-app-stranger-sit` CURRENT
- Funnel / Compose / public Ollama

Silence is never permission.
