# Implement — people-app phone face

**When:** 2026-08-19  
**Next:** `people-app-phone-seat` · SELECT / REJECTED  
Model did not `approve` / `next` / `reject`. Opening / Bind is not Yes.

## Chrome

- `android/app/src/main/java/com/mechanicall/pocket/demo/MainActivity.kt`
- One screen walk: **1 Bind · 2 Plan · 3 Draft · 4 Yes / Not yet · 5 Receipt**
- Plan is Objective / Next / Decision. Full file only if they ask.
- Bind refuses operator tree. Missing folder does not invent a plan.
- Word **aether** is not on the face (bridge module name only).
- `versionName` **0.3.0-walk** · `versionCode` 2 · package still `com.mechanicall.pocket.demo`

## Engine

- `python/aether_pocket.py` `face_state` / `face_state_json`
- `open_is_yes` is always false
- Operator tree returns a refused dict (no crash)
- Copy synced: `sh scripts/sync-pocket-engine.sh`
- `android/app/src/main/python/aether_bridge.py` exposes `face_state`

## Tests

`python3 tests/test_aether_pocket.py` — 15 passed (includes face_state bind / refuse / missing / open-is-not-yes).
