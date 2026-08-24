# 31 — Sequential live walk (STORM)

**Layer 1.** Operator: *Let subagents walk the app sequentially.*  
Live Next remains `people-app-phone-seat` (SELECT / REJECTED). Model does not approve / next / reject. Do not tap Confirm.

**Preflight:** probe ALLOW.

## Definition the walk is scored against

1. App deploys and queries the local AI model for **structured support**
2. App **opens on a selected directory**
3. App follows **standard chat-app frameworks**
4. App is a **bridge** from the person to the workspace

Be harsh. Rooms are not a defence.

## Pipeline (one walker at a time)

1. `01_home` — splash, home, hamburger
2. `02_plan` — plan fields, detailed markdown, bind
3. `03_draft` — schema fields + chat to local model
4. `04_gate-client` — decide (no Confirm), receipt, aether client, STORM verdict

Each stage writes `output/WALK.md` + screenshots if the A33 is `device`.

**Live (2026-08-19 re-walk):** `adb devices` on the edge shows `RZCW2038KHN device` (SM-A336B). Walkers must use the device, not fallback glass, unless get-state is not `device`.
