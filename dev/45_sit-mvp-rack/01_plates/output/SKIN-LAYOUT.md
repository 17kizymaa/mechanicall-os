# SKIN-LAYOUT — sit-mvp-rack plates

**Not Yes. Not assemble.** Pack target `1080×2138` (`drawable-nodpi/sit_skin.png` after Go).  
Imagine previews in this folder are **576×1248** (9:19.5). Freeze stage scales the chosen millwork; CRects below are pack pixels.

VSTGUI analogue: one CBitmap. Compose overlays **live text and hits** on these CRects. Millwork (bevels, AO, wells, idle lamps) stays in the PNG.

Scale preview → pack: `x * 1080/576`, `y * 2138/1248`.

## Chassis (FACE-SPEC rack; GATE at bottom)

| plate | pack CRect `l t r b` | live overlay |
|-------|----------------------|--------------|
| title | (24, 24, 1056, 100) | MECHANICALL + bound folder name |
| lcd | (24, 112, 1056, 200) pack; **preview** on `plan.png` `(72, 176, 504, 452)` | **The only terminal.** Idle: Next · GATE. Zoom: same glass, CURRENT essential page. See `ZOOM.md`. |
| desk | (24, 212, 1056, 360) | — |
| join_lamp | (64, 228, 248, 344) | filmstrip: idle / invited / connected / refused. Hit = JOIN (preauth RAM from baked inject, not a Material field) |
| send_lamp | (432, 228, 616, 344) | filmstrip: idle / staging / offer. Hit = SEND FOLDER |
| wake_lamp | (800, 228, 984, 344) | filmstrip: sleeping / waking / up. Hit = POST wol-pi (not Yes) |
| tabs | (24, 372, 1056, 468) | — |
| tab_plan | (40, 380, 280, 460) | PLAN |
| tab_draft | (300, 380, 540, 460) | DRAFT |
| tab_decide | (560, 380, 800, 460) | DECIDE |
| tab_receipt | (820, 380, 1040, 460) | RECEIPT |
| paper | (24, 480, 1056, 1920) | score |
| field_objective | (48, 508, 1032, 700) | typeset Objective (Plan read-only; Draft editable) |
| field_next | (48, 716, 1032, 860) | typeset Next |
| field_keep | (48, 876, 1032, 1100) | typeset Keep; MORE plate if overflow |
| field_reject | (48, 1116, 1032, 1340) | typeset Reject |
| field_limits | (48, 1356, 1032, 1680) | typeset Limits |
| tbc | (48, 1700, 1032, 1896) | Draft only. Empty this MVP. No 7B. |
| gate | (24, 1932, 1056, 2114) | LOAD/STREAM pits. Not Send. |

Bind overlay: FOLDER plate uses `paper`. Unbound: only that hit.  
Splash: mark uses `paper`; no hits.

## Zoom (same terminal — `ZOOM.md`)

| hit | does |
|-----|------|
| tap `lcd` | enter zoom (scale **this** glass patch; no second CRT) |
| tap field plate | enter zoom on that essential |
| GATE SEQ step | cycle Objective / Next / Keep / Reject / Limits / Receipt |
| inner left/right of `lcd` | prev/next page |
| outside `lcd_zoom_dst` (title, lamps, plates, gate body) | dismiss — original view |
| ABCD | **banks** PLAN/DRAFT/DECIDE/RECEIPT only — not pager |

`lcd_zoom_dst` (pack, after title, before GATE): (48, 120, 1032, 1888) — implement-time lerp from `lcd`. Skin PNG stays identity; only the LCD **patch** + text overlay scale.

Glitch: 120–180ms amber flash + horizontal tear + RGB split on the overlay, then snap. Not a crossfade.

**Rejected:** `zoom-bezel.png` (second terminal). Do not pack it.

## Law

- No Changes chip row. No Proposal-on-PLAN. No `**markdown**` glyphs on Plan.
- Overflow = GATE pages / MORE, not a nested millwork window.
- JOIN `connected` only if tsnet Up (later stage). Do not paint connected.
- Imagine PNGs are millwork **paint**, not FACE-SPEC. CRects + CURRENT **bytes** are law (blitted, not imagined).
- Not Camel Audio pixels.

## Files

| file | role |
|------|------|
| `rack.png` | canonical millwork (empty paper) |
| `plan.png` | paper as published field plates |
| `draft.png` | paper as workshop + TBC well |
| `bind.png` | unbound FOLDER plate |
| `splash.png` | splash mark |
| `lcd-idle.png` | same `plan.png`; STATUS glass = Next · GATE |
| `lcd-objective.png` `lcd-next.png` `lcd-keep.png` | same glass, verbatim essentials |
| `zoom-bezel.png` | **REJECTED** second CRT |
| `ZOOM.md` | in-frame zoom contract |
