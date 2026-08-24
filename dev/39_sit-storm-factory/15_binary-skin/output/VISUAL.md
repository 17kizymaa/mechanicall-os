# VISUAL — 0.15.3-skin (binary CBitmap analogue)

**Not Yes.** storm-0 `emulator-5554`. Never Confirm. Never A33.

Glass: `storm-0/after.png`. Spec: `BINARY-PIPELINE.md`. Skin: `sit_skin.png`.

| id | Verdict | Note |
|----|---------|------|
| V1 rack | PASS (FLAG) | Full-bleed baked plates, LCD well, GATE pits, cream score. FLAG: Compose labels are not yet CRect-aligned to the skin (LCD text sits *under* the well; GATE caption in the pit). |
| V2 host | PASS | fillMaxSize + resizeableActivity. No letterbox. |
| V3 paper | PASS | Cream inset is pixels in the skin. Bind copy is low-contrast — FLAG. |
| V4 LCD | PASS (FLAG) | Yellow live text. Well is baked. Alignment FLAG. |
| V5 gate | PASS | Idle pits are **skin pixels**, not Compose boxes. LOAD/STREAM overlay when lit. |
| V6 desk | PASS | JOIN/WAKE are overlays on a baked plate. |
| V7 genuine | PASS | Our PNG from `render-sit-skin.py`. No Camel bitmap. nodpi pack. |

FAIL-closed none. 10/10 app_verify is not visual Yes.

## Why this is not 0.15.2

0.15.2 tiled a 256px metal and drew millwork in Compose. That is a pastiche of “plugin-ish”. 0.15.3 ships the **editor bitmap in the APK binary**, which is what Camel Space did with VSTGUI `CBitmap` in the DLL.
