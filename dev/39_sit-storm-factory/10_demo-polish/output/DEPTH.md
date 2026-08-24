# DEPTH — Camel Space SOS Test grammar vs sit APK

**Not Yes. Not Play Store.** Live Next `sit-storm-factory`. Grammar only — no Camel bitmaps or trademarks in the APK.

Reference photo: Sound on Sound Nov 2005 *Camel Space* plugin *inside* a DAW host (`Guitar 2: Ins. 1 - CamelSpace` title bar, SOS Test preset). FACE-SPEC v2 + VENDOR-NOTES already named this steal.

## 1. Framework of depth (what SOS Test actually does)

| Optical move | How Camel Space does it | Honest sit mapping |
|--------------|-------------------------|--------------------|
| Host vs editor | Windows DAW chrome around the plugin | Android OEM is the host (`resizeableActivity`). Do **not** paint traffic lights or a 360×560 card. |
| Panel as millwork | Brushed metal *body*; every module is a raised island or a pit | Compact rack: stacked lips around cream **paper** (the score). Chrome darker on title + LCD + GATE only. |
| Lighting | Light from **top-left**: highlight on top/left edges, shadow on bottom/right | Asymmetric pad (extra start/top) + dark outer / lite / inner dark rabbet. Gaps between strokes. |
| Recessed LCD | Centre display is a **cutout well** with a thick bevel, dark glass, glowing content | `LcdStrip`: Title surround, extra top/left pad, LcdBg cutout, hairline. Next + GATE only. |
| Lamp pits | Trance-gate = dark well of **vertical step bars** (the product word GATE) | 16 GATE cells as pits (dark lip, fill). LOAD amber / STREAM purple / idle 0/16 dark. |
| Banks | Module labels sit in carved recesses | PLAN / DRAFT / DECIDE / RECEIPT tabs. Paper inside. |

**Do not steal:** knobs, X-Y pad, 128-step editor as a page, Camel wordmark, DAW window buttons, painted letterbox.

## 2. Why 08 glass looked flat

08 `plan.png`: cream-on-cream, 1.dp strokes, LCD a filled black slab, GATE 8.dp schematic cells. Chained `.border` on **one** node collapses to a hairline at Pixel density. Decide was two posters (YES black slab / NOT YET cream) with a lerp label swap.

That is not SOS millwork. Structure (OEM host, paper score, no letterbox) was already right (V2/V3). Millwork was missing.

## 3. APK map after this pass (`SeatTheme.kt` / `DecideModule.kt`)

- `PluginWindow`: Host cream → 3.dp BevelDark → gap → 2.dp BevelLite → gap → 1.dp BevelDark → Panel. Lighting top-left via order, not a bitmap.
- `LcdStrip`: 36.dp well, `padding(start=3, top=3, end=1, bottom=1)`, LcdBg cutout, `#4A4030` hairline.
- `GateStrip` lamps: 14.dp pits, asymmetric 1.dp lip, idle `LcdBg`.
- `DecidePad`: 16 GATE cells filling from the bottom in 40ms steps; label **relays** YES→AGAIN only at 16/16. Not `tween` crossfade. Two-tap + Why unchanged. Confirm not auto.
- Logo: `scripts/render-sit-logo.py` from SeatPalette hex (not Imagine). Cream full-bleed so Android 12’s circle is Host, not white. Title + gold LCD + paper + 8 GATE pits.

## 4. Logo (before / after)

**Before:** `logo_mechanicall.png` = `ic_launcher.png` = debug-window **slab + purple disc** on gunmetal. Sit chrome is cream rack. Splash 96.dp showed the cartoon. Bevels on that PNG were a fake 3D squircle — cheap because they were Imagine-era mark, not millwork.

**After:** miniaturized PluginWindow. OEM splash theme cream (`Theme.Mechanicall.Sit`). Compose splash 112.dp glyph on Host.

## 5. Decide animation

Crossfade (stacked Text alpha / 0.2 threshold) was a dissolve. Instrument steal = the pad **is** a trance-gate: 16 pits fill, then the word flips like a relay. Drain in reverse if they do not tap AGAIN. AGAIN still only arms; Confirm + Why is still the Yes.

FLAG: armed pad reads as a gold shutter (16 fat bars). Rest pits are the grammar. Iterate later if the shutter is too loud — not a second Next.

## 6. Rubric (visual-reviewer) on this glass

| id | Verdict | Note |
|----|---------|------|
| V1 rack | PASS (FLAG) | Title + LCD well + GATE pits + stacked lips. Paper is the score. FLAG: DESK still eats height. |
| V2 host | PASS | `fillMaxSize` + `resizeableActivity`. No letterbox. |
| V3 paper | PASS | Cream + ink CURRENT on PLAN. |
| V4 LCD | PASS | Next + GATE phase only. |
| V5 gate | PASS | Idle dark pits. SEND stays SEND. |
| V6 desk | PASS | JOIN/WAKE strip verbs. Decide is its own bank. |
| V7 genuine | PASS | Grammar from SOS Test / FACE-SPEC. No Camel bitmap. Logo from palette script. |

FAIL-closed none. PASS is not human Yes.

## 7. Analyst addendum (stricter — after 10 shipped)

Read-only reviewer vs SOS Test. **FLAG, not FAIL.** Structure of the rack is right. Millwork is still a **stamp** relative to SOS:

- Proud rim is **lite N/W + dark S/E**. Uniform `Modifier.border()` cannot say that. Four-edge `drawBehind` is the remaining cheap patch.
- Pixel 5 density 2.75: 1.dp ≈ 0.16 mm. FACE-SPEC’s 1+2 token is below a chamfer.
- `BevelLite` `#C8C4BC` on cream is a dusty neighbour, not a highlight — lite stroke + gap collapse into one rule on glass.
- 16-step Decide clock is the right *kind*; flooding the pad gold and flipping YES→AGAIN at 16 is still a dissolve of the well. Steal: GATE **row**, relay of two legends, well stays a well.
- V2/V3/V4/V6 PASS. V1 / V5-glass / V7 FLAG. FAIL-closed none.

Shipped 10 (concentric 3/2/1, LCD NW pad, GATE pits, palette logo) is **better than 08 hairline**. It is not yet SOS lighting. Four-edge drawBehind + quieter Decide well = another leftover under this **same** Next if you want it before you leave — not a second action-id.
