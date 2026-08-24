# 05_execute — sideload sit APK onto storm-0

**Not Yes. Not Decide.** Live Next `sit-storm-factory` APPROVED. Models never approve. Walkers never Confirm. Serial `RZCW2038KHN` refused.

## Inputs
- Layer 1: `../CONTEXT.md`
- Layer 4: `../output/HANDOFF-EXECUTE.md`
- Layer 3: `python/app_verify.py`, `scripts/storm-walk.sh`, FACE-SPEC v2, BEHAVIOURS.md
- Device: **emulator-5554** only (storm-0)

## Process
You are the execute walker.

1. `aether preflight sit-storm-factory` — stop on refuse.
2. `sh scripts/sync-pocket-engine.sh`
3. `cd android && ./gradlew :app:assembleDebug` (JDK 17 + SDK 34).
4. Verify `adb get-serialno` is `emulator-5554` and not `RZCW2038KHN`.
5. `adb -s emulator-5554 install -r app/build/outputs/apk/debug/app-debug.apk`
6. `sh scripts/storm-walk.sh emulator-5554 ../output/storm-0`
7. `python3 python/app_verify.py --uidump-dir ../output/storm-0`
8. Visual score vs FACE-SPEC v2 from uidump + screenshots.
9. Write artifacts. Do not tap Confirm. Do not bind mechanicall-os. Do not write CURRENT.

## Outputs
- `EXECUTE.md` — what ran, serial, honest gaps
- `VERIFICATION.md` — B1–B10 with glass
- `VISUAL.md` — V1–V7 with glass
- uidump + png under `../output/storm-0/`
