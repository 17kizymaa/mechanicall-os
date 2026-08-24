# Assemble receipt — 2026-08-18

**Next:** `people-app-phone-seat` · preflight allowed · human APPROVED.

| | |
|--|--|
| Engine sync | `sh scripts/sync-pocket-engine.sh` → `android/app/src/main/python/aether_pocket.py` |
| Command | `./gradlew --no-daemon :app:assembleDebug` (JAVA_HOME Temurin 17, ANDROID_HOME local SDK 34) |
| Result | **BUILD SUCCESSFUL** in 1m 24s |
| APK | `android/app/build/outputs/apk/debug/app-debug.apk` (42 262 156 bytes) |
| Package | `com.mechanicall.pocket.demo` |
| Notes | Chaquopy warning: host Python 3.14 cannot emit `.pyc` (runtime still 3.11). Not Play Store. |

Did not start URL / pocket-face. Did not tap Yes.
