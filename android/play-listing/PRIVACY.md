# Privacy — Mechanicall sit (closed testers)

**Not a production privacy policy URL until you host it.** This is the honest text for Play Data safety and for testers.

Mechanicall is a **local-first** folder sit. The app binds a folder **you** choose on the device. It does not create a Mechanicall account. It does not show ads. It does not sell data.

## What stays on the phone

- Your bound folder (`CURRENT.md`, `PROPOSE-CURRENT.md`, receipts, notes).
- App prefs (last bound path). `allowBackup` is false.

## What may leave the phone (only if you use those buttons)

- **Desk / 7B:** if you Send a draft while a desk URL is reachable, the sitting text goes to **your** operator host (Ollama on LAN or tailnet). Not a Mechanicall cloud.
- **SEND FOLDER:** a zip of the bound folder may go to a **lab drop** on the operator desk (`127.0.0.1` / LAN). Unauthenticated last-offer slot. Not a public Drive. Incoming zips are staged until **you** Accept; Accept skips live `CURRENT.md`.

## What we do not do

- No Google/Facebook login inside the sit.
- No analytics SDK.
- No Funnel / public Ollama as product.
- Opening the app is not consent to write your plan. Only **you** Publish (two-tap + Why).

## Delete

Uninstall `com.mechanicall.pocket.demo`. Bound folders on disk remain yours; the app does not wipe them.
