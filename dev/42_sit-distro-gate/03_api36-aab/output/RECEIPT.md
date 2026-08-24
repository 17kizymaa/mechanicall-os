# RECEIPT — 03_api36-aab

**Not Yes. Not Play upload.** Live Next `sit-distro-gate` action (3). Preflight allowed.

## Done

- `compileSdk` **36**, `targetSdk` **36** (merged manifest: `android:targetSdkVersion="36"`, min 26).
- `versionCode` **22**, `versionName` **0.17.1-api36**.
- AGP **8.9.1** (min for API 36), Gradle **8.11.1**, Chaquopy **16.1.0** (AGP 8.9–8.13).
- SDK platform `android-36` + build-tools `36.0.0` on `~/.android-sdk-mechanicall`.
- Signing: reads **off-git** `~/.mechanicall/play-upload.properties` if present. **Absent this sitting.** Do not mint a Play upload key here.
- Known limitations: `android/KNOWN-LIMITATIONS.md` (no LTE folder-send, not production, Data safety notes).

## Artifacts (not git)

| File | SHA-256 | Size |
|------|---------|------|
| `android/app/build/outputs/bundle/debug/app-debug.aab` | `03a1d4ed3405078b1db86e3488c761f4bf6c918beb4d4cecd9ae5312ac72e043` | 24M |
| `android/app/build/outputs/bundle/release/app-release.aab` | `40f284fc74538d7a92f1de2263c6f8dc855ab8be1fc7d9770ee8dbde119ff78f` | 23M |

Checksum file: `AAB.sha256`. AABs are gitignored.

Release bundle was `signReleaseBundle` **without** a Play upload keystore — treat as **debug-signed / not the first Console key**. Human creates `~/.mechanicall/play-upload.properties` then re-runs `bundleRelease` before upload.

## Honest leftover

- Host Python 3.14 cannot emit `.pyc` for Chaquopy 3.11 (warning only).
- Gradle TLS to Google Maven was flaky; second attempt succeeded.
- Action (4) LTE sideload still required. USB A33 ≠ LTE.
- Action (5) Play Console is **human**.

Walkers did not tap Confirm. Models did not approve. No Go-git.
