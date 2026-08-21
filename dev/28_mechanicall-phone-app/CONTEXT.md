# 28 — Mechanicall phone app (A33)

**Layer 1.** Operator ordered: install a real **app** on the phone; they will `aether approve` only after they can open it. Model **does not** approve / next / reject.

**Preflight:** `people-app-phone-seat` ALLOW (2026-08-19) · Phase SELECT · Status REJECTED.

## Product of this folder

Sideload **Mechanicall** (not “Brake (demo)”) on Samsung A33. One screen: Plan, Draft, Yes, Not yet, Receipt. Opening is not Yes. Bind `/sdcard/mechanicall-pocket` (not mechanicall-os). Play Store off.

## Pipeline (human skipped halt-until-install)

1. `01_analyze` — contract from BRAKE.md + research conclusion (seat window)
2. `03_implement` — **two specialists** (CONTEXT below authorizes spawn_subagent):
   - **face:** Kotlin chrome only (`MainActivity.kt`, manifest label)
   - **engine:** `aether_pocket` + Chaquopy copies + tests
3. `04_verify` — assemble debug APK (JDK 17 + SDK 34)
4. `05_review` — sideload via `scripts/sideload-apk-via-edge.sh`; receipt; **do not tap Yes**

## Law

- Same `aether_pocket` / refuse operator tree
- Word **aether** not on the face
- Do not rewrite operator `CURRENT.md`
- Do not rewrite bind CURRENT on the pocket
- No Funnel / public Ollama / Compose-as-Docker
