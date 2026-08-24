## Inputs
- Live CURRENT.md Next `sit-storm-factory` (preflight ALLOW)
- SOS reference: `../13_camel-sos-check/references/camel-space-sos.jpg`
- Failed architecture: `../14_sos-luminance/` tiled ImageShader + Compose boxes (still pastiche)
- Layer 3: VSTGUI CBitmap, Win32 PE resources, Android drawable-nodpi / aapt2

## Process
Research **how SOS-quality GUIs live in binaries**, then implement the analogue in the APK.

1. Document the VST path: Photoshop/SkinMan/KnobMan → PNG/BMP → PE `RT_BITMAP` / custom `PNG` / `PICTURE` resources (Resource Hacker, Restorator) → VSTGUI `CBitmap` of the **whole editor**.
2. Document the APK path: same PNGs → `res/drawable-nodpi/` (no density scale) → `resources.arsc` → Compose `Image` **under** hit-targets.
3. Do **not** extract or ship Camel Audio bitmaps (copyright + V7).
4. Bake **our** full-bleed `sit_skin.png`. Recant tiled millwork as the identity.
5. Sideload storm-0 only. Never Confirm.

## Outputs
- BINARY-PIPELINE.md, RECEIPT.md, VISUAL.md → output/
- sit_skin.png → android `drawable-nodpi/`
- storm-0 glass → output/storm-0/
