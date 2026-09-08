# Chassis concept — not that PNG

**Not Yes. Not CURRENT.** Research dump for compact. The freeze photo (`sit_chassis.png`) is **inspiration**, not the chassis.

## What the repo already named

| Source | Chassis **is** | Chassis **is not** |
|--------|----------------|-------------------|
| `decision-tree.md` **M0b** | VSTGUI 2.x **pipeline**: Photoshop-frozen panel, `CBitmap` blit, `CRect` hits. Overlapping brushed-metal plates, LCD well, GATE pits. Host = DAW / Android OEM. Steal **pipeline**, never Camel Audio bitmaps. | Live Compose rectangles; Camel PNGs; a photo of a synth on a desk as law |
| `FACE-SPEC.md` | **Rack around paper**: title, LCD (Next+GATE), DESK, banks PLAN/DRAFT/DECIDE/RECEIPT, cream **score**, GATE row. Fill the activity. | Chat; yellow LCD as the document; 360×560 fake plugin window |
| `02b_native-rack/FRAMEWORK.md` | **SitRackView**: one native view, pack 1080×2138, blit `Matrix`, integer CRects. Plates in `drawable-nodpi/`. Paint wins, then patch the CRect table. | Compose `FillBounds`; fraction hits; LcdViewer leak; **multiple runtime-composited PNGs** (M2=1: overlapping plates *painted into* one editor bitmap) |
| `scripts/render-sit-skin.py` | Inspectable millwork **generator** — OUR cream / gold / purple. `sit_skin.png` = CBitmap. | Imagine-as-spec; Camel clones |
| `15_binary-skin` → `16_revert-skin` | Pipeline was named, then undone | Live glass after revert was Compose again; later SitRackView re-landed blit with a **photograph** as the CBitmap |
| G1=2\* / G2=1+3 / farm-paint recant | C owns first sit. Millwork **augmented**. Chassis = **concept**. New plates + re-lay. | Dim/cover; freeze the oak photo; Pillow glyph boxes as the design method |

**Live APK (0.19.16-layers):** SitRackView blits **many** nodpi files (field, face, send, banks, well, gate). That is already a recant of FRAMEWORK “one CBitmap.” The **face** is still the freeze photograph with wood knocked out. That photo is the thing that is **not** the chassis.

## Inspiration (keep looking at it)

- Camel Space SOS Test grammar: overlapping plates, LCD, GATE, rivets, fills the host window.
- Freeze millwork PNG: cream faceplate, phosphor hole, three lamps, four banks, well, gate — **as a mood board**.
- Splash composition: instrument as an object (you liked this), minus oak.

## Standard for today (APK)

Law already: bind → plan → NOT ACTIVE draft → Why → Yes → One Next → I did it → receipt ↔ send. `app_verify` 15/15. Confirm never.

Look standard: **instrument that speaks C**, VSTGUI-grammar blit, not an oak-desk photo, not farm-paint scars as the face.

## Grill next (G3) — how we **paint** the real chassis this sitting

Facts are in this file. Decision:

| id | Produce the face how | Today? |
|----|----------------------|--------|
| **G3=1** | Re-land `render-sit-skin.py` → one (or few) CBitmap of overlapping plates, OUR palette, C rooms. Photo = reference only. | Inspectable. Hours–day. **Recommended if “today” means a real millwork panel.** |
| **G3=2** | Imagine = Photoshop: generate plates into `output/`, you stamp, freeze nodpi. Same CRects. | Faster pretty; Imagine ≠ spec until you stamp. |
| **G3=3** | Grill more / no paint today. Compact only. | Honest if G3 isn’t pinned. |
| **G3=4** | Keep the photo as face; only field/layers. | Contradicts “the chassis isn’t that image.” |

**Pinned:** **G3=1** (generator preview → Imagine paint → human stamp). **F3=3** (chassis Send LED + Decide ritual). Next pin: **L** + **S** in `LAYOUT-OPTIONS.md`.

**Fact (2026-09-08 resume):** `sit_skin.png` in nodpi is **byte-identical to** `sit_plan.png` (freeze photo). It is **not** a live bake of `scripts/render-sit-skin.py`. G3=1 means re-land that generator, not “the file named sit_skin is already the chassis.”
