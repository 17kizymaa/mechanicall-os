# BINARY-PIPELINE — SOS production quality from APK binaries

**Not Yes. Not Play Store. Not Camel Audio assets.** Live Next `sit-storm-factory`.

The pastiche was an **architecture** error: 0.15.1–0.15.2 painted millwork *live* (Compose `Color` / tiled `ImageShader` / 4-edge `drawBehind`). Camel Space never did that.

## 1. How the SOS original actually ships

Camel Space (Camel Audio, 2005) is a **bitmap-skinned VST editor**.

| Stage | Tool | What lands in the *binary* |
|-------|------|----------------------------|
| Paint | Photoshop (noise → motion blur → lighting). Later **SkinMan** (g200kg) for vector-with-lighting skins; **KnobMan** (2007+) for knob *filmstrips*. POV-Ray for photographed-looking knobs. | PNG/BMP of the **whole panel** plus per-widget frames |
| Toolkit | **VSTGUI 2.x** `CBitmap` / `CAnimKnob` / `CMovieBitmap` | One background bitmap; knobs are vertical filmstrips. Hit-tests are `CRect`s, not Layout. |
| Pack (Windows VST) | Win32 PE **resources** inside the `.dll` | `RT_BITMAP`, custom type `PNG` / `PICTURE` / `RCDATA`. Resource Hacker: save group → `.rc` + `.bin` that *are* PNGs (rename). Restorator 2018 batch-replaces hundreds of PNGs. FM8.dll is the well-known case (305 `PICTURE` entries). |
| Pack (Mac) | `.vst` bundle `Contents/Resources/` | Loose PNG, or the same bytes in the Mach-O. |
| Later (not Camel Space) | JUCE `BinaryData.cpp` | Array of bytes compiled in. Alchemy-era, not 2005. |

Production quality **is** that baked panel. Lighting, AO, overlapping plates, rivets, LCD glass — all decided in Photoshop, then **frozen into the binary**. The host (DAW) only draws a window; the plugin blits the editor bitmap.

Extracting Camel’s PNGs and putting them in Mechanicall is **copyright theft** and FACE-SPEC V7 FAIL. The *pipeline* is what we steal.

## 2. APK is the same machine as a VST DLL

| VST (2005) | Android APK |
|------------|-------------|
| PE `.rsrc` | `resources.arsc` + `res/` |
| `CBitmap` of the editor | `BitmapDrawable` / Compose `Image` |
| Resource Hacker | `aapt2` compile + `apktool` decode |
| `nodpi` analogue: raw pixels | **`res/drawable-nodpi/`** — system **must not** density-scale (else grain blurs). [Android densitites](https://developer.android.com/training/multiscreen/screendensities) |
| Optional 9-patch for *buttons* that stretch | `.9.png` + `npTc` PNG chunk. **Do not** 9-patch the full editor: millwork must not stretch. |
| Memory | 1080×2138 ARGB ≈ 9 MiB decoded. PNG on disk ~2–3 MiB. Acceptable for a demo APK. WebP lossless later. |

`aapt2` may palette-crush PNGs in `res/drawable/`. **nodpi** still crushes losslessly; grain survives better than a 256px tile upscaled by Compose.

Do **not** put the skin in `drawable/` without a density qualifier — xxhdpi devices will upsample a tiny tile and that *is* pastiche.

## 3. Implementation law (this stage)

```
Photoshop recipe  →  scripts/render-sit-skin.py
                  →  res/drawable-nodpi/sit_skin.png     # the CBitmap
                  →  PluginWindow Image(FillBounds)      # blit
                  →  Compose hit-targets, transparent    # CRect overlays
```

Yellow LCD text, purple STREAM bars, CURRENT.md paper — those **change**, so they stay live. Everything that does not change (chassis, plate overlap, wells, idle pits, rivets) belongs in the **binary skin**.

## 4. What we will not do

- Copy Camel Space / CamelPhat / Step FX bitmaps out of a purchased VST.
- JUCE in the APK.
- Imagine-as-spec.
- Tiled `ImageShader` as the product identity (that was 0.15.2).
- Play Store.

## 5. How to iterate like a VST shop

1. Edit `scripts/render-sit-skin.py` (the inspectable PSD).
2. Re-bake `sit_skin.png`.
3. `assembleDebug` — aapt2 packs it like Resource Hacker `-addoverwrite`.
4. Sideload storm-0. Never Confirm.

Optional later: separate `btn_up.png` / GATE filmstrip in the same `drawable-nodpi/` folder — that is KnobMan’s filmstrip, not a Compose Box.
