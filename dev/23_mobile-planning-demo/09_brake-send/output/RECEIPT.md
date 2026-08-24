# Receipt — 09 brake send

**When:** 2026-08-18  
**Human:** plan approved — URL first, then sideload APK  
**Preflight:** `mobile-planning-demo` ALLOW  
**Operator CURRENT:** not rewritten  

## Sendable now (URL)

```bash
# copy template off-repo, then:
export POCKET_HOST_TWIN="$HOME/mechanicall-pocket"
# optional: export POCKET_FACE_HOST=<tailscale-ip>
sh scripts/send-brake.sh
# paste the printed URL — GET is not Yes
```

| Check | Result |
|-------|--------|
| Operator bind via `send-brake.sh` | refuse exit 3 |
| `GET /` | 200, title **You have not said yes yet**, `Cache-Control: no-store` |
| `GET /yes` | **404** |
| `POST /not-yet` | 303 + `RECEIPT.md` “You said Not yet” |
| Phone `adb` sync | off unless `POCKET_SYNC=1` |
| Pocket unit + serve HTTP + rehearse | OK |

Contract: `../output/BRAKE.md`  
Walk: `examples/pocket-demo-client/HOW-TO-SIT.md`

## APK second (chrome done, assemble blocked here)

- Label / MainActivity / bridge show the same brake table + confirm-Yes
- Engine synced: `android/app/src/main/python/aether_pocket.py`
- **No APK file on this host:** no `gradlew`, no wrapper jar, no Android SDK
- Sideload steps: `android/README.md` (needs JDK 17 + SDK 34 on another machine)

Same `yes()` / `not_yet()` as the URL. Not Play Store.

## Do not claim

- A friend has tapped
- Play Store
- Assembled `app-debug.apk` on this Nix shell
- Operator approve

## Stop / next

Face is **not** left listening. Start it with `send-brake.sh` when you send a URL.

A person who is not you still has to tap, or this Next is decoration.
