## Inputs
- Layer 1: `../CONTEXT.md`
- Layer 1: root `CURRENT.md` Next `leftover-compose-delete`
- Layer 3: `python/app_verify.py`, `android/app/build.gradle.kts`
- Layer 4: leftover Compose sources listed in REVIEW packing list

## Process
You are the **delete** stage.

Remove Compose millwork so HEAD matches PR #8’s host claim. Do not assemble overlay-Compose. Do not sideload. Verify with `python3 python/app_verify.py` and, if the SDK is present, `:app:assembleDebug` of the **native** host only.

## Outputs
- `DELETE.md` — files removed
- `summary.md`
