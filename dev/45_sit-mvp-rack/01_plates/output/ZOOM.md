# ZOOM — in-frame LCD viewer (not a second terminal)

**Not Yes. Not assemble. Not Imagine-as-spec.**  
The extra CRT overlay (`zoom-bezel.png`) is a **rejected fork**. It is the previous failure mode: a nested window.

## Think

The imagined device already has a terminal: the amber **STATUS** glass under TRANCEFORM. That CRect *is* the viewer. Plan field plates stay the original view. Zoom does not invent glass.

### Failure modes we do not repeat

| Fail | Why it failed | This zoom |
|------|----------------|-----------|
| Nested `verticalScroll` in `SeatCard` (`PlanModule.kt`) | millwork-inside-millwork; “ugly scroll window” | **No** nested scroll window. Pages, not a document scroller |
| Material `OutlinedTextField` / Dialog | Compose window on a plugin | **No** dialog. Same Activity, same skin |
| Second CRT painted on the paper | extra terminal; overprogrammed | **One** LCD CRect. Reject `zoom-bezel.png` |
| Imagine the law text | garbled CURRENT; Imagine-as-spec | Compose/Canvas **blits bytes** of CURRENT.md |
| New Activity / WebView | second product | `graphicsLayer` / `drawBitmap` src→dst on the LCD **patch of the same PNG** |

### APK-friendly zoom

Idle: full `sit_skin` blit; live text in `lcd` CRect (Next · GATE only — FACE-SPEC).

Zoom: still **one** bitmap.

1. Draw `sit_skin` at identity (chassis, lamps, plates, GATE stay).
2. Clip the **same** PNG to `lcd` (the existing glass) and draw that patch scaled into `lcd_zoom_dst` — a larger rect centred on the STATUS well, **below title, above GATE SEQ**, cream chassis still visible as padding.
3. Draw CURRENT lines in that dest glass (monospace, gold on dark). Not a second texture of a terminal.

That is `Canvas.drawBitmap(skin, src=lcd, dst=lcd_zoom_dst)` plus one text overlay. GPU, no extra asset, no Dialog. Exit = hit test **outside** `lcd_zoom_dst` (title, rivets, lamps, field plates, GATE body).

Enter zoom: tap `lcd`, or tap a field plate (OBJECTIVE / NEXT / KEEP / …) to open that essential already selected.

### Where the user clicks to cycle essentials

**Do not** steal ABCD. Idle ABCD = PLAN / DRAFT / DECIDE / RECEIPT (banks). Two jobs on one pad is the chip museum again.

**GATE SEQ** (already on the millwork, stays in the padding if the LCD patch grows downward but not over the gate) is the pager. It is already a step sequencer. Each step is one essential page:

| step | page | bytes |
|------|------|--------|
| 1 | Objective | `**Objective:**` line + following prose until next `**` |
| 2 | Next | `**Next:**` |
| 3 | Keep | `## Keep` block |
| 4 | Reject | `## Reject` block |
| 5 | Limits | `## Limits` block |
| 6 | Receipt | bound `RECEIPT.md` if present, else honest empty |

Left / right **inner edge** of the *same* LCD glass = prev / next step (backup if a finger misses the gate).

No nested scroll. Long Keep/Reject = **that GATE page**, then MORE as the next step if a block overflows the glass — still paging, still not a Compose millwork window.

### Glitch (crisp, not a crossfade)

Crossfade is Material. This glass is phosphor.

On step change or zoom in/out, **120–180ms**, LCD overlay only:

1. 1 frame full-well amber flash (`Lcd` `#E6C14A` at ~0.35 alpha).
2. 2–3 frames **horizontal tear**: copy the text layer with 2–6px `translationX` and a 1px RGB split (three draws, R/G/B tints, cheap).
3. GATE LED for the new step strobes.
4. Snap to the new lines. No easing soup.

Not a video. Not `RenderEffect` as identity. `Animatable` + `drawWithContent`.

### Law

Zoom is a **view**. CURRENT bytes on disk do not change. Dismiss is not Yes. GATE pager is not Decide.
