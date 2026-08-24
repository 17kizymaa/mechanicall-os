# MODULES — Mechanicall as a navigable space

**When:** 2026-08-19  
**Next:** `people-app-phone-seat` · SELECT / REJECTED  
Opening this file is not Yes. Splash is not Yes. Bind is not Yes. Client is not Yes.

## Identity

Launcher **Mechanicall** · package `com.mechanicall.pocket.demo` · version **0.4.0-space** · versionCode **3**

One application. Modules are rooms. The three-line menu (top-right) is the directory of the whole sitting.

## Modules

| Route | Name in menu | Job |
|-------|----------------|-----|
| `splash` | (not in menu) | Small logo loading screen, then Home. Not Yes. |
| `home` | Home | Bound folder, Next, last said, tiles into the other rooms. |
| `plan` | Plan | Schema fields, size by character count, labels CAPITALISED, dropdown for full CURRENT.md. |
| `draft` | Draft | Dual toggle: (1) locked schema-field editor (2) draft-on-draft chat → tailnet `personal-llm-sft-v4`. Chat writes PROPOSE only. |
| `decide` | Decide | Approve / Reject only. Each needs **two taps**, then dialog **Are you sure you want to X?** with **Why?** always visible (not hidden). Confirm calls `yes()` / `not_yet()`. |
| `receipt` | Receipt | Last RECEIPT.md or empty honesty. |
| `bind` | Bind | Name their folder. Refuse operator tree. |
| `client` | Client | Allowlisted **aether client**: current, brief, validate, events, drift, verbs, help, status. **Never** approve / reject / next from this room. |

Hamburger panel also lists **project shortcuts** (named files in the bound pocket): CURRENT.md, PROPOSE-CURRENT.md, RECEIPT.md, DECISIONS.md, events — tapping opens a read view, not Yes.

## Law

- GET / open / splash / bind / client / chat is never Yes.
- Silence is never Yes.
- Word **aether** may appear **only** in the Client module (operator asked for an aether client).
- Refuse mechanicall-os markers.
- Do not rewrite operator CURRENT. Do not rewrite pocket CURRENT except via `yes()`.
- No Funnel. No public Ollama. Default host stays a Tailscale placeholder the human fills.
- Approve/Reject on the face map to `yes()` / `not_yet()` (apply PROPOSE then `aether approve` / `aether reject` in the **bound** folder).

## File ownership (specialists must not cross)

### Engine (`python/aether_pocket.py` + `tests/test_aether_pocket.py` + bridge)

Add (keep existing `face_state`, `yes`, `not_yet`, refuse):

- `schema_fields(pocket) -> dict` live CURRENT fields (AUTHORITY_FIELDS)
- `read_schema_draft(pocket) -> dict` proposed field values (from PROPOSE, else live)
- `write_schema_draft(pocket, fields: dict) -> PocketResult` writes PROPOSE-CURRENT.md with **Field:** lines only; never CURRENT.md
- `project_shortcuts(pocket) -> list[{name, path, kind}]`
- `draft_chat(pocket, host, message, model="personal-llm-sft-v4:latest")` appends to `DRAFT-CHAT.jsonl`, writes only PROPOSE, returns JSON `{ok, reply, propose, history}`
- `chat_history(pocket) -> list`
- `face_state` gains `shortcuts` (list of names)

### Aether client (`python/aether_client.py` + tests + bridge)

New module, stdlib-only. Import from bridge.

- `CLIENT_ALLOW = ("current", "brief", "validate", "events", "drift", "verbs", "help", "status")`
- `client_run(pocket, verb) -> {ok, verb, text}`  
  Refuse `approve`, `reject`, `next`, `deinit`, and anything not in ALLOW.
- Prefer real `aether` via `aether_pocket.run_aether` when the binary exists; else read-only fallbacks from files (`CURRENT.md`, events.jsonl). Fallback must not approve.

### Face (Kotlin, package `com.mechanicall.pocket.demo`)

```
MainActivity.kt          splash → SeatApp
SeatTheme.kt             cream / navy
FaceBridge.kt            pyCall + JSON parse (shared)
SeatNav.kt               Scaffold + top bar + three-line menu (TOP RIGHT)
modules/SplashScreen.kt
modules/HomeModule.kt
modules/PlanModule.kt
modules/DraftModule.kt
modules/DecideModule.kt
modules/ReceiptModule.kt
modules/BindModule.kt
modules/ClientModule.kt
```

Plan: each field label CAPITALISED. Font size from `sp(28f - (len.coerceAtMost(80))/8f)` (short Next is large; long Objective shrinks). Dropdown “Detailed plan” shows markdown.

Draft: two toggle chips, **Fields** | **Chat**. Fields edit locked AUTHORITY_FIELDS. Chat list + compose box + Send to `ollama_host` (default `http://100.90.85.68:11434` as last known myarch Tailscale — human may change). Public bind refused in engine if host is 0.0.0.0.

Decide: two big buttons. Tap 1 arms (label “Tap again”). Tap 2 opens dialog. Dialog title `Are you sure you want to approve?` / `reject?`. **Why?** OutlinedTextField always shown. Confirm / Cancel.

Menu: `Icons.Default.Menu` top-right. Modal panel: module names then a divider **Project** then shortcuts.

Logo: `R.drawable.logo_mechanicall` (orchestrator installs PNG). Splash: small centered logo, 900ms, navigate Home.

## Colours

- Navy `#1F4E79`
- Cream `#F7F4EF`
- Surface `#FBF8F3`
- Ink `#1A1A1A`

## Tests the engine/client must add

- write_schema_draft does not touch CURRENT.md
- client_run("approve") refuses
- client_run("reject") refuses
- client_run("next") refuses
- client_run("current") ok on a toy pocket
- draft_chat writes PROPOSE not CURRENT (mock or skip network if no host)
- face_state open_is_yes is still false
- operator tree still refused

## Out of scope

Play Store. Funnel. Tapping Yes for them. `aether approve` as the model. Compose-as-a-new-product (stay this package). SeatMate branding.
