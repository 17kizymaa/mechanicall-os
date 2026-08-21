# Implement 0.5.0-sit (not Yes)

**When:** 2026-08-20  
**CURRENT:** people-app-phone-seat APPROVED. Model did not approve / next.

## Shipped in tree

- Chat is home (`ChatHome.kt`): thread + composer. Desk Tailscale default `http://100.90.85.68:11434`.
- `draft_chat` timeout **25s**; fail appends “Desk did not answer. This is not Yes.”
- Kotlin Send uses 26s `withTimeoutOrNull` so the thread does not hang.
- Default pocket `/sdcard/mechanicall-pocket`.
- Support: Bind string + **Choose folder (support)** (`OpenDocumentTree`).
- Menu **Sit**: Chat, Plan, Decide, Receipt, Support, Client. Draft room removed.
- Decide Confirm requires Why.
- APK `0.5.0-sit` versionCode 4 assembled.
- Sideload this turn: **blocked** (A33 USB missing). Retry when device is `device`.

Opening is not Yes.
