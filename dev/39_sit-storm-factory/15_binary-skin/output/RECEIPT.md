# RECEIPT — 15_binary-skin

**Not Decide. Not Yes.** Preflight ALLOW `sit-storm-factory`. Confirm not tapped. Serial `emulator-5554`.

## Research

`BINARY-PIPELINE.md` — VST PE `PNG`/`PICTURE` resources (Resource Hacker / Restorator) map to APK `res/drawable-nodpi/` + aapt2. Production quality is a **baked editor bitmap**, not live rectangles.

Do **not** extract Camel Space assets.

## Built

- `scripts/render-sit-skin.py` → `android/app/src/main/res/drawable-nodpi/sit_skin.png` (1080×2138)
- `PluginWindow` blits that PNG; chrome is overlay text/clicks
- Version **0.15.3-skin** (versionCode 19)
- APK: `mechanicall-0.15.3-skin.apk`

## Verify

`python3 python/app_verify.py --serial emulator-5554` → 10/10. Not Yes.

## Leftover (same Next)

CRect alignment: live labels vs baked wells. Next cheap patch: layout JSON from the renderer driving Compose weights — that is VSTGUI `CRect`, not a new action-id.
