# RECEIPT — 14_sos-luminance

**Not Decide. Not Yes.** Preflight ALLOW `sit-storm-factory`. Walkers did not Confirm. Serial was `emulator-5554` (storm-0), never RZCW2038KHN.

## Why

Live `0.15.1-sos` on storm-0 was cool grey + cyan millwork — a generic pastiche that lost yellow / purple / cream. Human: match Camel Space SOS **texture, depth, luminance**; keep those three colours; research the actual 2005 tools; publish a **sideload demo**.

## Built

- `scripts/render-sos-metal.py` — tileable cream-metal / dark-metal / paper grain / LCD glass (Photoshop 2005 chain, not Camel PNG).
- `SeatTheme.kt` — `ImageShader` chassis, raised islands, recessed wells, yellow LCD, purple STREAM, cream paper.
- Version **0.15.2-luminance** (versionCode 18).
- Demo APK: `output/mechanicall-0.15.2-luminance.apk`.

## Verify

- `python3 python/app_verify.py --serial emulator-5554` → **10/10**. Not Yes.
- storm-0 screenshots in `output/storm-0/`. Confirm not tapped.

## Demo install (not Play Store)

```bash
adb -s emulator-5554 install -r dev/39_sit-storm-factory/14_sos-luminance/output/mechanicall-0.15.2-luminance.apk
# or any device that is NOT RZCW2038KHN for walkers
```

Bind a folder **outside** mechanicall-os (e.g. `/sdcard/mechanicall-pocket`). Do **not** bind `/sdcard/mechanicall` (sessions tree) or this git repo. Opening is not Yes.

## Never

- CURRENT rewrite
- Go-git (not said)
- Camel bitmaps / camel wordmark
- Play Store
- Confirm
