# 27 — people-app-phone-seat (APK chrome on A33)

**Layer 1 routing.** Operator Next `people-app-phone-seat` (APPROVED 2026-08-18).  
Phone: Samsung A33 (`SM-A336B` / `RZCW2038KHN`) on USB ADB via mbp-edge (`anphuni@100.70.86.90`).

## Inputs
- Layer 1: `../../CURRENT.md` (Next + Action id = `people-app-phone-seat`)
- Layer 3: `../../android/README.md`, `../../examples/pocket-demo-client/`
- Layer 3: `scripts/push-pocket-via-edge.sh`, `scripts/push-aether-via-edge.sh`, `scripts/aether-on-a33.sh`, `scripts/sync-pocket-engine.sh`
- Layer 3: `dev/23_mobile-planning-demo/output/BRAKE.md`
- Layer 4: existing phone pocket `/sdcard/mechanicall-pocket` (do not overwrite CURRENT)

## Process
Assemble debug APK on a host with JDK 17 + SDK 34. Sideload via edge ADB. Bind pocket folder that is **not** mechanicall-os. Opening the app is not Yes.

URL / pocket-face is a sibling idea — do not start it as a second Next.

## Pipeline
1. `01_assemble/` — sync engine, wrapper, assemble `app-debug.apk`
2. `02_sideload/` — `adb install` on A33 via edge; bind existing pocket
3. `03_receipt/` — honest receipt (have APK / missing APK)

## Non-goals
- Play Store
- Funnel / public Ollama / Compose
- Bind mechanicall-os
- `aether approve` / `next` / `reject` as the model
- POST Yes for them
- Rewrite bind CURRENT (`~/people-app-stranger-sit`)
