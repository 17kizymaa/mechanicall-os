# CLIENT-DONE

**When:** 2026-08-19  
**Specialist:** aether client (`python/aether_client.py`)  
**Next:** `people-app-phone-seat` — unchanged. Model did not approve / next / reject.  
Opening this file is not Yes.

## Done

- `python/aether_client.py` — stdlib-only; `CLIENT_ALLOW` = current, brief, validate, events, drift, verbs, help, status
- `CLIENT_DENY` includes approve, reject, next, deinit, init, onboard (and other mutating verbs)
- `client_run(pocket, verb) -> {ok, verb, text}`
  - `refuse_if_operator` first (operator tree never binds)
  - deny / unknown → `{ok: false, text: "refused: client cannot …"}` — never dispatched
  - CLI via `aether_pocket.run_aether` / helpers when `find_aether_bin` exists
  - read-only file fallback when CLI missing (CURRENT.md, parse_fields, events.jsonl)
  - fallback never implements approve / reject / next
- `android/app/src/main/python/aether_client.py` copied via `sh scripts/sync-pocket-engine.sh`
- `tests/test_aether_client.py` — 13 tests OK (`python3 tests/test_aether_client.py`)
  - approve / reject / next refused; CURRENT unchanged
  - current ok and contains Next / Objective
  - operator tree refused; CURRENT untouched
  - allowlisted `client_run` does not write CURRENT
  - CLI-missing fallback still refuses approve and does not write CURRENT

## Not

- No `aether approve` / `reject` / `next`
- No APK assemble / sideload
- No Kotlin (face owns ClientModule)
- Did not edit `python/aether_pocket.py` or root `CURRENT.md`

Silence is never permission.
