# CURRENT proposal — 2026-08-25T21:14Z

**Not law. Not Yes.** Live Next stays `sit-mvp-rack`.  
**APPLY: human must approve then merge — model must not overwrite CURRENT without human gate.**

Recant is the **freeze host**, not the plates, not the action-id.

## Observations

- `02_freeze` packed `sit_skin.png` from `plan.png`. USB look and NeuralBridge screenshot (now working) show the millwork is the imagined plate. Compose then draws `LAW · OBJECTIVE (none)` on the bezel and purple SEQ pits across OBJECTIVE (`SkinLayout.lcdZoom` covers the paper).
- That host is leftover-Compose on millwork (Reject) even if the PNG is a CBitmap.
- Proposed CURRENT body still says “Compose overlays live text/hits only.” That sentence is the failed method.
- NeuralBridge capture is lab, not product. Companion `0.1.1-capture` on the A33 now has `canTakeScreenshot` (a11y capabilities=169). MCP `android_screenshot` returns JPEG without MediaProjection GRANT.

## Proposed change (summary)

1. Keep **Next `sit-mvp-rack`**.  
2. Recant freeze host: native **SitRackView** (one `View`, one `CBitmap`, integer CRects through the blit `Matrix`, LCD clipped to glass). Compose is forbidden on millwork **and** paper.  
3. Insert stage `02b_native-rack/` — halt on `FRAMEWORK.md`. No assemble until Go. Mesh/doorbell stay later.  
4. Do not recant M2=1 / M7=1 / Imagine-as-paint / Funnel / Camel / dual-Next.

## Before → after (This Next item 1)

| Field | Live (inner CURRENT) | Proposed |
|-------|----------------------|----------|
| Freeze host | Compose overlays live text/hits only | Native `SitRackView`: blit `drawable-nodpi/` via `Matrix`; hits = pack CRects; LCD text clipped to STATUS glass; Draft = transparent `EditText` in wells; Decide = CRect two-tap. No Compose on paper. |
| Stage 2 | freeze overlay + sideload look | freeze PNG kept; **02b** recants host after Go on `FRAMEWORK.md` |

## Fidelity checklist

- [x] Still **one** Next (`sit-mvp-rack`)
- [x] Models never approve / never auto-write CURRENT
- [x] No secrets in git
- [x] Silence ≠ permission
- [x] Halt at `02b_native-rack/output/FRAMEWORK.md`
- [x] Imagine = paint, not spec
- [x] leftover-Compose-millwork-as-SOS still Reject

## Human decision required

- [ ] Go on `dev/45_sit-mvp-rack/02b_native-rack/output/FRAMEWORK.md` (implement SitRackView)
- [ ] Apply this recant into CURRENT body (host sentence) then `aether approve` with a real reason
- [ ] Reject SitRackView and name a different host

**Do not** run `aether approve` from a model. **Do not** assemble sit until Go.
