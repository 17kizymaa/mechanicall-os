# 02 — sideload to A33 via mbp-edge

## Inputs
- Layer 4: `../01_assemble/output/RECEIPT.md` (must name an APK path)
- Layer 3: `../../../scripts/push-aether-via-edge.sh` (CLI already on device)
- Defaults: `POCKET_EDGE=anphuni@100.70.86.90` `POCKET_SERIAL=RZCW2038KHN`

## Process
You are the sideloader.

1. Confirm A33 `device` on edge ADB.
2. `adb -s $SERIAL install -r` the debug APK. Package `com.mechanicall.pocket.demo`.
3. Bind `/sdcard/mechanicall-pocket` (already there). **Do not overwrite** phone `CURRENT.md` unless the human asked.
4. Opening the app is not Yes. Do not tap Yes.
5. Do not push mechanicall-os.

## Outputs
- `output/RECEIPT.md` — serial, package, install result, pocket path
