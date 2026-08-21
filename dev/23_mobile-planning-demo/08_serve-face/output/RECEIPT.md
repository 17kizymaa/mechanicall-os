# Receipt — 08 serve face

**When:** 2026-08-18T06:44:02Z  
**Human:** `08_serve-face`  
**Preflight:** `mobile-planning-demo` ALLOW  
**Operator CURRENT:** still repair A. Not rewritten.  
**Sitting:** 2026-08-16 still cancelled. Face is up for rehearsal, not mum-in-the-room.

## Bind

| | |
|--|--|
| URL | http://192.168.0.51:8765/ |
| Listen | `192.168.0.51:8765` (not `0.0.0.0`, not `127.0.0.1`) |
| Twin | `~/mechanicall-pocket` |
| Start | `sh scripts/serve-pocket-face.sh` (left running) |

`curl http://127.0.0.1:8765/` failed to connect — LAN bind only.

## GET is not Yes

| Check | Result |
|-------|--------|
| `GET /` | HTTP 200, `Cache-Control: no-store` |
| Page says | `GET never Yes` |
| Yes control | `method="post" action="/yes"` + confirm dialog |
| Page Next | `name-the-outcome` |
| `GET /yes` | HTTP **404** |
| Twin sha256 before | `72acf60f04e23425faf77e9bcca3a02bb871f52932fa1a204b4cad6dd1d37cee` |
| Twin sha256 after GET | same |
| Twin Status / Approval | still REJECTED / REJECTED |
| POST `/yes` | **not sent** |

GET `/` tried phone pull (no flash error). Twin bytes unchanged — pull did not apply a Yes.

No browser tools in this session. Proof is `curl` + twin hash, not a click-through.

## Do not claim

- Live client sitting
- Play Store
- Operator approve
- Phone Yes

## Stop / next

**Stopped 2026-08-18T07:08:44Z** — serve process killed. `8765` not listening. Do not auto-restart.

Human Yes is still a POST you type, or `aether approve` on the twin.  
To bring the face back: say **serve the face** (do not assume).
