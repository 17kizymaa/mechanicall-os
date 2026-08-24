# PROBE — zip / sharing / servers (2026-08-24)

**Not CURRENT. Not Yes. Not a drop start.** Verify-only. A33 was USB-read via mbp-edge, never a STORM serial.

## Live contract (forgotten)

| Field | Live `CURRENT.md` |
|-------|-------------------|
| Next | `sit-testers` |
| Approval | APPROVED |
| Objective | Testers sit this face; first-sit 7B PROPOSE template; off-LAN then Play **internal/closed**; not production; SOS parked |
| Play production | **Reject** / Prohibited `play-production-this-next` |
| Sharing | Depreciated inbox + lab drop; G4 mesh JNI named BLOCK; do not list LTE folder-send |

## Zip action (SEND FOLDER / drop)

| Check | Result |
|-------|--------|
| Code | `python/aether_inbox.py` `send_project` zips pocket, POST `/offer`, `poll_incoming` pulls zip, Accept copies and **skips live CURRENT.md** |
| Lab drop process | **Down.** No listener on `:8765`. No `aether_drop.py` process. |
| `http://127.0.0.1:8765/health` | connect refused |
| `http://192.168.0.51:8765/health` | connect refused |
| Twin `:7078` | down |
| Stale store | `.inbox/drop/offer.json` + `offer.zip` from **2026-08-23T10:18:17Z** `from=sitrae`, 5 files (`CURRENT.md` is *inside the zip*; Accept must still skip writing live CURRENT) |
| Auth | none (lab-only; `aether_drop.py` refuses bind `0.0.0.0`) |
| Containment | **Open.** `_unzip_to` skips `..` only. GPT-5.6: absolute/backslash/symlink members can escape `dest` **during poll, before Accept** |

**Sharing is not functional as a live service.** The protocol exists; the server is off; the extractor is unsafe for anything but a trusted lab zip.

## Other servers

| Service | Result |
|---------|--------|
| Ollama `personal-llm-sft-v4` | **Up** on `127.0.0.1:11434`, LAN `192.168.0.51:11434`, tailnet `100.90.85.68:11434`. Listener is `*:11434` (firewall not proven here). Public Ollama still Reject. |
| Local `adb devices` | empty (no STORM AVD) |
| mbp-edge `100.70.86.90` | ping OK; SSH OK; **A33 `RZCW2038KHN` device** on USB |

## Distro file on the phone

`/sdcard/mechanicall/sessions/13_FIRST_DISTRIBUTION_PR_GPT5.6.md`

Copy: `.aether/proposals/13_FIRST_DISTRIBUTION_PR_GPT5.6.md`

**Verdict in that file: NO — not yet.** Play internal upload today: No. Preserve product shape; fix ZIP containment + stock-phone Publish first.

Do not restart drop until `_unzip_to` is contained. Do not upload PR #7 as-is.
