# 75_tester-apk-live

**Action id:** `tester-apk-live`
**Law:** root `CURRENT.md`. One Next. Preflight allowed before this stage wrote anything.

## Inputs
- `CURRENT.md` section "Next allowed action"
- `android/app/build.gradle.kts` `defaultConfig` (read only; do not bump)
- `git rev-parse HEAD` and `git status --porcelain` at pin time
- `android/KNOWN-LIMITATIONS.md` (closed-tester sit)

## Process
1. Write `output/STABLE-LAYER.md`. Pin `applicationId`, `versionName`, `versionCode`, HEAD, and the dirty bit. Do not change the version.
2. From `android/`, run `./gradlew :app:assembleDebug`.
3. If that JDK cannot assemble, write the failure in `output/RECEIPT.md` and halt. Do not copy a binary this halt did not just build.
4. If assemble succeeds, copy the debug APK into `output/`. Record path, byte size, and sha256.
5. Receipt. The file, when present, is the client download. No Play upload, no apex deploy, no recipient.

## Outputs
- `output/STABLE-LAYER.md`
- `output/RECEIPT.md`
- `output/` debug APK only when step 2 succeeds
