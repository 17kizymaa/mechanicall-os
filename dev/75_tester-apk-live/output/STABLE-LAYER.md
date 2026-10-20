# Stable layer — tester-apk-live

**When:** 2026-10-07
**Action id:** `tester-apk-live`
**This halt does not move the pin.** Later tester builds start from these values. Nothing below was edited to produce this note.

## Pin

| Field | Value | Source |
| --- | --- | --- |
| applicationId | `com.mechanicall.pocket.demo` | `android/app/build.gradle.kts` `defaultConfig` |
| namespace | `com.mechanicall.pocket.demo` | same file, `android.namespace` |
| versionName | `0.19.21-loop-from-20` | same `defaultConfig` |
| versionCode | `46` | same `defaultConfig` |
| minSdk | `26` | same `defaultConfig` |
| compileSdk / targetSdk | `36` / `36` | same file |
| abiFilters | `arm64-v8a`, `x86_64` | same `ndk` block |
| HEAD | `648987193ee237d4b59622bfb98448aadc1a7377` | `git rev-parse HEAD` |
| Branch | `feat/aether-apply` | `git rev-parse --abbrev-ref HEAD` |
| Worktree | dirty | `git status --porcelain` = **411** paths, counted before this stage folder existed |

Version was not bumped.

The host line in `CURRENT.md` still names branch `feat/share-urls-readiness`. The pin records the branch `git` reported.

## JDK

- `java` on `PATH` at pin time: OpenJDK `26.0.1`. `JAVA_HOME` was unset. `/usr/lib/jvm` has `java-26-openjdk` only.
- App compile target is Java 17. Wrapper is Gradle `8.11.1`.
- The assemble that succeeded used the JDK already at `/home/anphuni/.jdk/temurin-17` (Temurin `17.0.20`). That choice does not change the pin above.

## What this pin is not

- Not a new `versionCode` or `versionName`.
- Not a Play upload, an apex deploy, or a named recipient.
- The debug APK Gradle accepted is recorded in `output/RECEIPT.md`, including path, size, and sha256.
