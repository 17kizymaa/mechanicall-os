# RECEIPT — 02_freeze

**Not Decide.** Preflight ALLOW `sit-mvp-rack`. Human Continue after ZOOM.md = Go on plates.

## Done

- `android/app/src/main/res/drawable-nodpi/sit_skin.png` — 1080×2138 from `01_plates/output/plan.png`
- `PluginWindow` millwork stack replaced by skin blit + CRect hits (`SkinLayout.kt`, `LcdViewer.kt`, `LawPages.kt`)
- LCD zoom uses the **existing STATUS glass**. GATE SEQ pits page Objective/Next/Keep/Reject/Limits/Receipt. Outer pad dismisses. Glitch = amber flash + RGB tear.
- PLAN: no Changes, no Proposal-on-PLAN, no nested scroll window
- Draft: TBC well empty (no 7B auto-draft)
- Desk: Material preauth field removed
- BEHAVIOURS B2 + `app_verify.py` recanted to LCD law pages
- `zoom-bezel.png` still rejected (not packed)

## Not this stage

- tsnet AAR / AuthKey inject / zip carry (03)
- wol-pi deploy / S3 (04)
- Sideload: `adb devices` empty this sitting — no fake USB-as-LTE
- Git last is human

## Look-only sideload (2026-08-25)

- Device: `RZCW2038KHN` SM-A336B via **mbp-edge USB** (`adb` on myarch still empty).
- Artifact: `android/app/build/outputs/apk/debug/app-debug.apk` (43M). SHA-256 `00c57c36ace52cd858b9001ba4373652e378237db5231d40822ea99d8a132d14`.
- `adb install -r` → `INSTALL_FAILED_UPDATE_INCOMPATIBLE` (Play-signed vs debug). Uninstall then install **Success**. Launched `MainActivity`.
- USB is **not** LTE. This is freeze look, not distro-gate.
- `screencap` from this SSH pipe returned empty (device awake; app pid present). Look is on the phone.

## Halt after assemble attempt

Look-only APK if gradle succeeds. Mesh and doorbell are later actions.
