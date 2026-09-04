# sit-module-panels — implement receipt

**Not Yes. Not Play. USB ≠ LTE.**

## Done

- CRT tap → `IsolatedMode.CRT` maximised dark panel, no millwork overlay
- Send-folder → `sendOverlay` panel (`offerStatus` / preview). Not `sendProject`. Not Yes. Not FILES
- Draft bank → `IsolatedMode.DRAFT` live vs proposed. `writeSchemaDraft` only
- RECEIPT → `FaceBridge.receiptText`; empty stays `(empty receipt)`
- B11–B15 in BEHAVIOURS.md; `app_verify.py` **15/15**
- `scripts/sit-send-smoke.sh` source PASS; A33 look skipped (adb down)

## Halt

Sideload + stranger walk on device. Opening the app is not Yes.

## Sideload (2026-09-04)

USB via mbp-edge, **not LTE**. Tailscale `100.70.86.90` direct. A33 `RZCW2038KHN` `adb device usb:3-1`. Phone usb0 tethering `10.14.187.0/24` is not a testers receipt.

| | |
|--|--|
| Before (archived) | `0.19.0-sit-rack` vc 25 |
| Installed | **`0.19.2-module-panels` vc 27** |
| LAST.apk | `mechanicall-0.19.2-module-panels-vc27.apk` |
| Look | `after-sideload.png` (lab; not Yes) |
