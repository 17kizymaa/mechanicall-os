## Inputs
- Layer 1: live `CURRENT.md` Next `sit-distro-gate` action (3)
- Layer 3: Play API-36 gate 2026-08-31; AGP min 8.9.1; Chaquopy 16.1 for AGP 8.9+
- Layer 3: `android/app/build.gradle.kts`, `android/build.gradle.kts`
- Layer 4: `../02_stock-publish/output/RECEIPT.md`

## Process
Raise compileSdk/targetSdk to 36. Bump AGP/Gradle/Chaquopy only as needed. Produce an AAB and SHA-256. Signing keystore stays **off git** (`~/.mechanicall/play-upload.properties`). Do not mint a Play upload key. Known-limitations page: no LTE folder-send, not production. Do not open Play Console. Do not Go-git.

## Outputs
- RECEIPT.md -> output/
- LIMITATIONS.md (or android/KNOWN-LIMITATIONS.md)
- checksum of the AAB built this sitting
