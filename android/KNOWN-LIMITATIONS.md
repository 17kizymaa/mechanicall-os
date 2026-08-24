# Mechanicall sit — known limitations (closed testers)

**Not production. Not Funnel. Not Yes.** Store listing and testers must read this as-is.

## What this APK/AAB is

A **closed-tester** phone sit of Mechanicall OS: bind one folder, read CURRENT, draft a PROPOSE, Publish with Why. Demo seat.

## Do not claim

- **LTE folder-send / mesh Drive.** Headscale/tsnet JNI is a named gap (G4). SEND FOLDER is a lab drop (`127.0.0.1`), unauthenticated, last-offer slot. Sharing is not “online” unless that drop is up on the desk.
- **Production Play listing.** Internal/closed testing only.
- **JOIN connected** without tsnet Up.
- **Opening the app / Bind / Send / FILES / Accept** as Yes. Only Decide → Publish (two-tap + Why) writes CURRENT.

## Stock phone

Decide → Publish is **native** in the APK (`pocket_approve`). No Termux and no `bin/aether` on PATH required for Yes/Not yet. Desk 7B is optional: first sit can write a static PROPOSE template when the desk is quiet.

## Play Console declarations (human)

- `MANAGE_EXTERNAL_STORAGE` (bind a user-chosen folder). Restricted permission — justify All files access or switch to SAF; this Next does not silently pass policy.
- `usesCleartextTraffic` (lab desk URLs). Declare in Data safety; do not ship as production.
- Target API **36** (required for new/update uploads from 2026-08-31).
- Signing: upload keystore lives **off git** (`~/.mechanicall/play-upload.jks` + `play-upload.properties`). This tree never contains `.jks`. Backup that directory before first Console upload.

## Privacy / data safety (honest)

- No cloud account. No ads. No third-party analytics.
- Bound folder stays on device. Lab drop, if used, posts a zip to the operator desk on LAN — not a public server.
- Ollama/desk is the operator’s host, not a Mechanicall SaaS.

## Upgrade / uninstall

Uninstall the package `com.mechanicall.pocket.demo`. Bound folders on disk are the user’s; the app does not delete them.
