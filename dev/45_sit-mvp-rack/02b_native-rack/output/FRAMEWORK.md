# FRAMEWORK — SitRackView (native CBitmap host)

**Not Yes. Not assemble. Not Imagine-as-spec.** Preflight ALLOW `sit-mvp-rack`.  
**Halt.** Human Go on this file before any sit rewrite.

USB look 2026-08-25 `02_freeze/output/look-usb-sit.png`: millwork PNG matches `01_plates/output/plan.png`. Compose then draws `LAW · OBJECTIVE (none)` on the bezel and purple SEQ pits across OBJECTIVE. That is the shit. The plates were right. The host was wrong.

## Diagnosis (what 02_freeze actually shipped)

| Layer | Intended (M0b / VSTGUI 2.x) | What landed |
|-------|-----------------------------|-------------|
| Chassis | One `CBitmap` in `drawable-nodpi/` | `sit_skin.png` from `plan.png` — **keep** |
| Host | Blit + `CRect` hit-test | Compose `BoxWithConstraints` + `Image(FillBounds)` + `SkinHit` |
| LCD | Phosphor in the STATUS glass | `LcdViewer` Compose `Text` that escapes the glass |
| Zoom | `drawBitmap(skin, src=lcd, dst=lcd_zoom_dst)` | `SkinLayout.lcdZoom = (0.08, 0.12, 0.92, 0.52)` — a second rectangle covering the plates |
| Paper | Plan = painted fields; law in LCD pages | Plan empty; Draft `ChatHome` Column; Decide `DecideModule` Column + Dialog; Bind SAF under a paper hit |
| Hits | Integer pack pixels × the blit `Matrix` | Independent float fractions (`SkinLayout.kt`) that do not match `SKIN-LAYOUT.md` pack table |

Compose leftover on paper is **leftover-Compose-millwork-as-SOS** (CURRENT Reject). `app_verify.py` 10/10 scored semantics, not glass. NeuralBridge tree said “5 nodes”; the USB PNG says the overlay is still there.

## Decision (recommended)

**SitRackView** — one native `android.view.View` (a `CFrame`). Not Compose. Not a stack of `Image` + `Box`. Not WebView. Not Flutter.

Rejected hosts:

1. **Keep Compose, delete leftover modules only.** Still `FillBounds` + fraction hits + `LcdViewer` leak. The zoom bug is the host, not ChatHome.
2. **Recant plates / return to cream Compose millwork.** Forbidden (`leftover-compose-millwork-as-sos`).
3. **Multiple runtime-composited PNGs.** M2=1 is one editor bitmap with overlapping plates *painted in*.
4. **Imagine-as-spec.** FACE-SPEC stands. This file is the host contract; plates stay paint.

M2=1, M6=4, M7=1, M8=3 stand. Recant is **freeze host only**.

## Architecture

```
SitActivity  (ComponentActivity, NO setContent)
  SitRackView                    // CFrame: onDraw + onTouchEvent
    blit sit_skin via Matrix     // CBitmap
    draw LCD text clipped to glass
    (Draft) EditText children in field CRects, background=null
    (Bind)  paper CRect → SAF
    (Decide) paper CRect two-tap → FaceBridge.yes
```

Python still owns CURRENT / PROPOSE / Publish. The view never writes law.

### Plate swap (CBitmap frames, not Compose routes)

| Plate | drawable-nodpi | When |
|-------|----------------|------|
| `sit_splash` | from `splash.png` | first frames |
| `sit_bind` | from `bind.png` | unbound |
| `sit_plan` | from `plan.png` | PLAN |
| `sit_draft` | from `draft.png` | DRAFT |
| `sit_decide` | from `plan.png` until a decide plate exists | DECIDE (Yes is a CRect, not a form) |
| `sit_receipt` | from `plan.png` until a receipt plate exists | RECEIPT (text in LCD) |

One bitmap on screen. Swap the resource. Do not composite plates at runtime.

### Matrix (the whole point)

Pack size is **1080×2138**. Device window is **1080×2400** minus system bars.

```
dst = fit-center of pack into view  // FACE-SPEC: fill the activity, no painted 360×560 letterbox
matrix.setRectToRect(pack, dst, ScaleToFit.CENTER)
canvas.drawBitmap(skin, matrix, null)
hit = inverse.map(touch) → pack pixels → CRect contains
```

`ScaleToFit.FILL` (today's `FillBounds`) stretches rivets. `CENTER` letterboxes with `SeatPalette.Host` (`#12100E`), not a painted fake plugin window. Cream chassis stays the PNG.

### CRects (pack pixels, one file)

`scripts/gen_crects.py` reads `01_plates/output/SKIN-LAYOUT.md` and writes `SitCRects.kt`. Do not hand-maintain a second fraction table (`SkinLayout.kt` dies).

Hits (from SKIN-LAYOUT; implementer re-measures against `plan.png` if paint disagrees with the table — **paint wins**, then the markdown is patched):

| id | pack `l t r b` | action |
|----|----------------|--------|
| `lcd` | preview-true on `plan.png`: `(135, 176, 504, 452)` at 576×1248 → scale × 1080/576, 2138/1248 | tap → zoom this glass |
| `title` | `(24, 24, 1056, 100)` | bound name overlay only if needed; prefer paint |
| `join` `send` `wake` | desk lamps | JOIN / SEND FOLDER / WAKE POST wol-pi |
| `tab_plan` … `tab_receipt` | banks | plate swap. **Not** the LCD pager |
| `field_objective` … `field_limits` | paper wells | Plan: open that LCD page. Draft: focus that `EditText` |
| `tbc` | Draft only | empty this MVP |
| `gate` | SEQ pits | LCD pager (ZOOM.md). Not Decide |
| `paper` | unbound | SAF picker |

**Paint wins.** USB look showed the STATUS glass is the large CRT, not the thin strip `(24,112,1056,200)` in the first SKIN-LAYOUT guess. Re-measure `lcd` from `plan.png` before coding hits.

### LCD (the only live chrome on Plan)

Idle: Next id · GATE phase, clipped to `lcd`. FACE-SPEC: not the whole Objective.

Zoom (ZOOM.md, already accepted):

1. Chassis blit stays identity.
2. `canvas.drawBitmap(skin, src=lcd, dst=lcd_zoom_dst)` — scale **this** glass. No second CRT (`zoom-bezel.png` still rejected).
3. CURRENT bytes (LawPages) drawn in `lcd_zoom_dst`. Clip. Do not draw on OBJECTIVE.
4. GATE SEQ (painted pits) pages Objective / Next / Keep / Reject / Limits / Receipt.
5. Inner left/right of the **glass** = prev/next. Outer millwork dismisses.
6. Glitch: 120–180ms amber flash + 2–6px tear + RGB split on the LCD overlay only.

No Compose `graphicsLayer`. No SEQ `Box` row on the paper (that is the USB failure).

### Draft

Same millwork. Field wells contain `EditText`:

- `background = null`
- `textColor = Ink`
- `typeface = MONOSPACE`
- no Material outline, no FlowRow chips, no hunk museum
- TBC well empty (`"(empty. No auto-draft.)"` as paint or one `TextView` in `tbc`)
- writes PROPOSE only

### Decide

Two-tap on the painted Publish region (paper CRect). Why is an LCD page, not a Dialog. `PluginDialogFrame` dies. `FaceBridge.yes` still Chaquopy-native. Models never tap it.

### Bind

Paper CRect → `OpenDocumentTree`. No essay. Unbound millwork is `sit_bind`.

### DESK

JOIN / SEND / WAKE are painted lamps. Hits only. No `OutlinedTextField` preauth well (M9=2 bake + M10=1 inject). JOIN `connected` only if tsnet Up (stage 03). Do not paint connected.

## Files to add / kill (after Go)

Add:

- `SitActivity.kt` — replaces Compose `MainActivity.setContent`
- `SitRackView.kt` — blit + hits + LCD
- `SitCRects.kt` — generated
- `SitLcd.kt` — LawPages draw
- `scripts/gen_crects.py`

Kill from the Plan/Draft/Decide path:

- `SkinLayout.kt` / `SkinHit`
- `LcdViewer.kt` as Compose
- `SeatNav.kt` Compose tree
- `ChatHome` / `DecideModule` / `ReceiptModule` / `PlanModule` on paper
- `PluginDialogFrame` / Material `OutlinedTextField` on the rack

Keep: `FaceBridge`, `LawPages` (parser), Chaquopy, Bind SAF contract, `app_verify.py` (rewrite asserts to resource-ids on SitRackView, not Compose semantics).

## Look pipe (lab, not product)

NeuralBridge companion is **not** the sit. USB `screencap` is the ground truth when MCP capture is down.

| Pipe | How | Status 2026-08-25 |
|------|-----|-------------------|
| `scripts/sit-look.sh` | ssh `mbp-edge` → `adb exec-out screencap -p` | **Works** (1080×2400 PNG). Not LTE. |
| NeuralBridge `android_screenshot` | a11y `takeScreenshot` | Failed: `SecurityException: Services don't have the capability of taking the screenshot` because XML lacked `canTakeScreenshot`. Patched in local clone `0.1.1-capture`. |
| MediaProjection GRANT | Setup tab, **foreground** `startActivityForResult` | Was: translucent activity from AccessibilityService (Samsung drops it). Now: MainActivity fires the system dialog. Human still taps **Start now**. |

Verify after Go:

```
scripts/sit-look.sh dev/45_sit-mvp-rack/02b_native-rack/output/look.png
# millwork pixels ≈ plan.png; LCD pixels ignored
```

Do not Funnel port 7474. Do not `adb reverse`. Forward on mbp-edge USB only.

## What this is not

- Not a new Next. Still `sit-mvp-rack`.
- Not mesh / doorbell / Play / LTE.
- Not permission to overwrite CURRENT.md (human applies the companion proposal if the host recant must be law).
- Not Camel bitmaps.
- Not Imagine-as-spec.

## Halt

Review this file + `look-usb-sit.png` vs `plan.png`.  
**Go** = implement SitRackView in 02b.  
Silence is not Go.
