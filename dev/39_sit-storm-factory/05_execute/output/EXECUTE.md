# EXECUTE — sit APK on storm-0

**Not Decide. Not Yes.** Live Next `sit-storm-factory` APPROVED (human). Preflight ALLOW. Models did not approve. Walkers did not tap Confirm. Serial `RZCW2038KHN` refused (app_verify exit 3).

## Device

| item | value |
|------|--------|
| serial | `emulator-5554` only |
| product | `sdk_gphone64_x86_64` (google API-34) |
| AVD | `storm-0` under `~/.mechanicall/storm` |
| package | `com.mechanicall.pocket.demo` |
| version | `0.15.0-vst` code 16 |
| pocket | `/sdcard/mechanicall-pocket` (demo client copy, **not** mechanicall-os) |

`adb devices` showed one serial. A33 was not attached. Sideload used `adb -s emulator-5554 install -r`, not `scripts/sideload-apk-via-edge.sh`.

## Commands (this turn)

1. `aether preflight sit-storm-factory` — ALLOW
2. `sh scripts/sync-pocket-engine.sh`
3. `cd android && JAVA_HOME=~/.jdk/temurin-17 ./gradlew :app:assembleDebug` — BUILD SUCCESSFUL in 38s
4. `adb -s emulator-5554 install -r android/app/build/outputs/apk/debug/app-debug.apk` — Success
5. `sh scripts/storm-walk.sh emulator-5554 dev/39_sit-storm-factory/output/storm-0` — unbound FOLDER dump
6. Grant `MANAGE_EXTERNAL_STORAGE` via appops (API-34 default had rejected; bind is not Yes)
7. Relaunch (KEYCODE_BACK once dropped to launcher — recovered with `am start`; never Confirm)
8. Bound walk: PLAN → DRAFT → DECIDE (no YES / Confirm tap) → RECEIPT → FILES
9. `python3 python/app_verify.py` and `--uidump-dir …/storm-0/verify` — **10/10**
10. `python3 python/app_verify.py --serial RZCW2038KHN` — refused exit 3

## Glass (honest)

- **Unbound:** title FOLDER; LCD “Name your folder. One project.”; GATE IDLE; Bind this folder / Choose your folder; no PLAN tabs; Confirm absent. See `home.png`.
- **PLAN:** bound name `mechanicall-pocket`; LCD `name-the-outcome · QUIET`; JOIN NOT-ON-NET; WAKE SLEEPING; SEND FOLDER depreciated not Yes; published CURRENT on cream. See `after-relaunch.png`.
- **DRAFT:** hunk workshop (PREAMBLE/OBJECTIVE… LIVE vs purple DRAFT); ACCEPT/REJECT HUNK; SEND stays SEND. See `draft.png`.
- **DECIDE:** first-arm YES / NOT YET pads. Confirm lives in the Why dialog. **Neither YES nor Confirm was tapped.** See `decide.png`.
- **RECEIPT:** “No sitting yet… Opening this page is not a Yes.” EVENTS empty. See `receipt.png`.
- **FILES:** OEM Files app on `mechanicall-pocket` (`CURRENT.md`, `PROPOSE-CURRENT.md`, `RECEIPT.md`). Not an in-app overlay. See `files.png`.

## Scores

- `/app-reviewer` mechanical: **10/10** source and glass (`output/VERIFICATION.md`)
- `/visual-reviewer`: no FAIL-closed (V2 letterbox / V5 `…` / V3 bubbles). FLAG: idle GATE lamps stay PurpleDim instead of 0/16 dark; DESK strip eats paper. (`output/VISUAL.md`)
- inbox tests 6 OK · storm tests 5 OK (A33 refuse covered)

## Gaps (named, not hidden)

- tsnet JNI still not in the APK. JOIN stays `NOT-ON-NET` until userspace Listen exists.
- API-34 emulator needs `MANAGE_EXTERNAL_STORAGE` allow (or SAF “Choose your folder”) to bind `/sdcard/…`.
- Headscale login-server / wol-pi is operator ops, not this execute.
- Inbox bytes stay local until mesh Listen.
- `aether current validate` WARNs Phase/Status/Approval all APPROVE(D). Human-owned CURRENT; models do not rewrite it.
- Live CURRENT / `.aether/events.jsonl` / `.context.md` / `DECISIONS.md` still dirty on purpose (no Go-git this turn).

Opening the emulator, installing, binding, and FILES are not Decide.
