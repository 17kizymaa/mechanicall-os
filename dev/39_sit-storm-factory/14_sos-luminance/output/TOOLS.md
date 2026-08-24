# TOOLS — how Camel Space was actually drawn, and what we can ship in an APK

**Not Yes. Not Play Store.** Live Next `sit-storm-factory`. Grammar + *our* bitmaps. **No Camel Audio assets in the APK.**

Reference photo: Sound on Sound Nov 2005, Camel Space *SOS Test* (`dev/39_sit-storm-factory/13_camel-sos-check/references/camel-space-sos.jpg`).

## What 2005 plugin GUIs actually were

Camel Space (Camel Audio, 2005) is a **bitmap-skinned VST editor**, not a vector Compose theme and not JUCE.

| Layer | Tool (era) | What it did |
|-------|------------|-------------|
| Panel art | **Photoshop** | Filter → Noise → **Motion Blur** (horizontal) → Lighting (top-left). High-key brushed aluminum. Overlapping plates, inner shadows, rivets. |
| Knobs | 3D (Cinema 4D / 3ds Max) or photographed, later **KnobMan** (2007+) | Filmstrips (`CAnimKnob`). Lighting stays fixed while the metal rotates. |
| Host compositing | **VSTGUI 2.x** (Steinberg) | One background PNG + CMovieBitmap / CAnimKnob. The DAW draws the *window*; the plugin draws the *editor*. |
| Not this era | JUCE LookAndFeel | Camel **Alchemy** (2010, Apple later) is JUCE. Camel Space is not. |
| Not this era | Figma / VST GUI Pro | 2020s filmstrip exporters. |

The SOS photo is high **luminance** silver (almost cream-white), deep **AO** in plate joints, **recessed** LCD/sequencer wells, vertical trance-gate bars in a dark pit. It is **not** four 2px Compose strokes on `#9AA1A9`.

## Can that be recreated in an APK?

**Yes, as a skin.** That is how the original worked: bitmaps + a host. Compose `ImageShader` is our VSTGUI. Android OEM (`resizeableActivity`) is our DAW chrome.

**No, as a pixel clone.** Copying Camel plates, the camel wordmark, or their knob filmstrips is theft and CURRENT Reject (V7). We re-run the *recipe* (noise + motion blur + lighting + cream colorize) in `scripts/render-sos-metal.py`.

**No, as JUCE-in-the-APK.** FACE-SPEC: Compose stays. Knobs stay out (verb museum).

## What 13_camel-sos-check got wrong

`0.15.1-sos` stole **cool grey + cyan** and 4-edge `drawBehind` millwork. That is a generic 2000s pastiche. It **lost** the sit palette (yellow LCD, purple GATE, cream paper) that `now.png` already had. The SOS photo is *bright metal + dark wells*, not *dead grey + teal text*.

## What 0.15.2 ships

| SOS optical | Our mapping (keep yellow / purple / cream) |
|-------------|--------------------------------------------|
| High-key brushed plate | `metal_light.png` tile, cream-silver |
| Dark module islands | `metal_dark.png` chocolate-warm, not teal |
| Recessed LCD / gate well | inverted lighting + `lcd_glass.png` + yellow text |
| Trance-gate bars | 16 pits; LOAD amber; STREAM purple; idle `LcdBg` |
| Paper score | cream + `paper_grain.png` (the document, not the rack) |
| Rivets | 9.dp drawn circles on the title — not Camel’s camel |

Python is the inspectable Photoshop stand-in. Imagine is not the spec.
