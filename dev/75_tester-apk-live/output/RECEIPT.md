# RECEIPT — 75_tester-apk-live

**Action id:** `tester-apk-live`
**When:** 2026-10-07
**Preflight:** allowed (`tester-apk-live` matches Next, `Phase=APPROVE Status=APPROVED`)
**Instance:** tool (`mechanicall-os`). Closed-tester sit. Not production. Not Yes.

## Pin
`output/STABLE-LAYER.md`. Unchanged: `applicationId` `com.mechanicall.pocket.demo`, `versionName` `0.19.21-loop-from-20`, `versionCode` 46. HEAD `648987193ee237d4b59622bfb98448aadc1a7377` on `feat/aether-apply`. No version bump.

## JDK fix
`java` on `PATH` is OpenJDK `26.0.1`. Gradle `8.11.1` fails there while compiling the Kotlin DSL:

`java.lang.IllegalArgumentException: 26.0.1` at `org.jetbrains.kotlin.com.intellij.util.lang.JavaVersion.parse`.

Log of that run: `output/assembleDebug.log`. Exit 1. No task `:app:assembleDebug` ran.

The assemble was rerun with the JDK already on this machine:

```bash
export JAVA_HOME=/home/anphuni/.jdk/temurin-17
export PATH="$JAVA_HOME/bin:$PATH"
cd android && ./gradlew :app:assembleDebug --no-daemon --console=plain
```

`JAVA_HOME` `java -version` is Temurin `17.0.20` (2026-07-21). That matches the app's `jvmTarget` 17. Gradle was not upgraded. The system `java` on `PATH` was left at 26.

Result: `BUILD SUCCESSFUL in 12s`. 45 tasks: 1 executed (`:app:checkKotlinGradlePluginConfigurationErrors`), 44 up-to-date, including `:app:packageDebug` and `:app:assembleDebug`. Log: `output/assembleDebug-jdk17.log`.

No file under `android/` outside `build/` and `.gradle/` is newer than the debug APK. Gradle treated the existing package as the current debug output.

## Client download
Copied from `android/app/build/outputs/apk/debug/app-debug.apk`.

| | |
| --- | --- |
| Path | `dev/75_tester-apk-live/output/mechanicall-pocket-0.19.21-loop-from-20-vc46-debug.apk` |
| Bytes | 62526130 |
| sha256 | `44900cc0adc6b823a99bdca6a2992868e4017202d540b003dc31d31d66ac4d8f` |
| Source mtime | 2026-09-08 17:28:03 +0100 |
| `aapt dump badging` | `name='com.mechanicall.pocket.demo'` `versionCode='46'` `versionName='0.19.21-loop-from-20'` `compileSdkVersion='36'` `sdkVersion:'26'` `targetSdkVersion:'36'` `native-code: 'arm64-v8a' 'x86_64'` |

The copy is byte-identical to the Gradle output (`cmp`).

## Not done (by design)
No Play upload. No apex deploy. No recipient, website, or store. No sideload. No version bump. No `aether approve` / `apply` / `next`. No commit.

## Halt
The APK file above is the client download. The stable layer is the pin. Live development of a later tester build starts from that pin, with `JAVA_HOME` pointed at Temurin 17.
