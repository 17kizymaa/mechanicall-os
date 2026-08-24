# Sideload receipt — 2026-08-18

**Next:** `people-app-phone-seat` · did not tap Yes.

| | |
|--|--|
| USB host | mbp-edge `anphuni@100.70.86.90` (Alpine) |
| Device | `SM-A336B` / `RZCW2038KHN` / Android 14 |
| Command | `sh scripts/sideload-apk-via-edge.sh` |
| adb install | **Success** (streamed) |
| Package | `com.mechanicall.pocket.demo` `0.1.0-demo` |
| Path on phone | `/data/app/~~…/com.mechanicall.pocket.demo-…/base.apk` |
| Storage | `appops MANAGE_EXTERNAL_STORAGE: allow` |
| Pocket | `/sdcard/mechanicall-pocket` (**CURRENT not overwritten**) |
| Launch | `am start` Status ok; first frame drawn (Chaquopy + Compose; skipped frames on cold start) |

Already on the phone (left alone): `com.mechanicall.pocket.face` (different package).

## Bind smoke (Load, not Yes)

uiautomator after tapping **Load** only:

- Status: `bound /storage/emulated/0/mechanicall-pocket (demo)`
- Plan: phone pocket CURRENT (`Next: name-the-outcome`, **Status/Approval REJECTED**)
- Banner still: “You have not said yes yet” / “Opening this screen is not a yes.”

Phone `CURRENT.md` grep after Load: still REJECTED. Opening / Load ≠ Yes.
