# FACE-DONE — modular Mechanicall seat (Kotlin)

**When:** 2026-08-19  
**Next:** `people-app-phone-seat` · SELECT / REJECTED  
Opening this file is not Yes. Splash is not Yes. Bind is not Yes. Client is not Yes.

Face specialist only. Did not run `aether approve`, `aether reject`, or `aether next`. Did not rewrite CURRENT.md. Did not tap Yes. Did not sideload.

## Tree

Package `com.mechanicall.pocket.demo` · versionName already `0.4.0-space`.

```
android/app/src/main/java/com/mechanicall/pocket/demo/
  MainActivity.kt          Python start; setContent { SeatApp() }
  SeatTheme.kt             cream #F7F4EF / navy #1F4E79 / surface #FBF8F3 / ink #1A1A1A
  FaceBridge.kt            pyCall + JSON helpers
  SeatNav.kt               Scaffold title + three-line menu TOP-RIGHT
  modules/SplashScreen.kt
  modules/HomeModule.kt
  modules/PlanModule.kt
  modules/DraftModule.kt
  modules/DecideModule.kt
  modules/ReceiptModule.kt
  modules/BindModule.kt
  modules/ClientModule.kt
```

The old one-screen walk in `MainActivity.kt` is gone.

## Rooms

| Route | Menu | Behaviour |
|-------|------|-----------|
| splash | no | Small `R.drawable.logo_mechanicall` (~96.dp), cream, 900ms, then Home |
| home | Home | Logo, Mechanicall, bound path, Next, last said / empty honesty, tiles |
| plan | Plan | AUTHORITY fields, labels CAPITALISED, body size from length, Detailed plan |
| draft | Draft | Independent Fields / Chat toggles. Save → `write_schema_draft` (not Yes). Chat → `draft_chat` |
| decide | Decide | Approve / Reject only. Two taps, then dialog with Why? always visible. Confirm → `yes` / `not_yet` |
| receipt | Receipt | RECEIPT.md or empty honesty |
| bind | Bind | Your folder + Bind. Refuse operator tree. Bind is not Yes |
| client | Client | Allowlisted verbs. Run → `client_run`. Subtitle: This is not Yes. Never approve/reject/next |

Menu panel (full-height Dialog): Home, Plan, Draft, Decide, Receipt, Bind, Client, divider **PROJECT**, then `face_state.shortcuts` / `project_shortcuts`. Module tap navigates. Project file tap opens a read-only sheet. Not Yes.

Navigation: sealed `SeatRoute` + `currentRoute` in `SeatNav`. After splash, Home.

## Bridge

`FaceBridge.pyCall` is resilient (`ERROR: …` if a function is missing). Calls:

- `face_state`, `schema_fields`, `read_schema_draft`, `write_schema_draft`
- `project_shortcuts`, `chat_history`, `draft_chat`, `client_run`
- `yes`, `not_yet` (Decide confirm only)
- `plan_text`, `receipt_text` still used for Plan / Receipt / shortcut sheet

Default desk host in Draft: `http://100.90.85.68:11434`, labelled **Desk model (private network)**.

`yes()` is invoked from `DecideModule` after arm + confirm only.

## Word law

The string `aether` does not appear on Home / Plan / Draft / Decide / Receipt / Bind.

It appears as:

- `aether_bridge` module name in `FaceBridge` (required Chaquopy import)
- **Aether client** copy in `ClientModule` only

Gradle: no new deps. `Icons.Default.Menu` comes from material-icons-core (Material3). Package id unchanged.

## Compile check

`JAVA_HOME=$HOME/.jdk/temurin-17 ANDROID_HOME=$HOME/.android-sdk-mechanicall ./gradlew :app:assembleDebug --offline` from `android/` — **BUILD SUCCESSFUL**. Compile check only. Not sideloaded. Not Yes.

Chaquopy still warns that host Python 3.14 cannot emit 3.11 `.pyc`. Pre-existing. Not a face change.

## Not done by this specialist

Engine (`schema_fields`, `draft_chat`, `client_run`, …) — other specialist. Face degrades to honesty if those calls are missing.

Human still must sideload and bind a folder that is not mechanicall-os. Opening the APK is not Yes.
