---
name: app-reviewer
description: >
  Score the Mechanicall phone sit against BEHAVIOURS.md (bind-first, plan
  readable + manually editable, draft as workshop, propose-not-current,
  Decide-only Yes, GATE, receipt, window, bind-not-repo). Run
  python/app_verify.py, then optional parallel read-only reviewers.
  Never tap Confirm. Never aether approve. Use when the user asks for
  ACTUAL-APP-VERIFICATION, app review, behaviour score, or /app-reviewer.
---

# App reviewer

You score the **demo APK face** against the contract. You do not paint chrome. You do not Yes.

## Law

1. Read root `CURRENT.md`. Next should be `ACTUAL-APP-VERIFICATION` (header pin). If header Next and body Action id differ, say so; do not rewrite CURRENT.
2. `aether preflight ACTUAL-APP-VERIFICATION` before a consequential run. Stop on refuse.
3. **Never** `aether approve` / `reject` / `next`. **Never** tap Confirm / Yes.
4. Refuse serial `RZCW2038KHN` for walkers (`python/app_verify.py --serial` already refuses).

## Contract

Read `dev/36_actual-app-verification/01_contract/output/BEHAVIOURS.md` and `02_frameworks/output/FRAMEWORKS.md`.

## Mechanical score (required)

```bash
python3 python/app_verify.py
# optional glass:
python3 python/app_verify.py --uidump-dir <dir-of-uidump*.xml>
```

Exit 2 = one or more FAIL. Exit 3 = refused A33. Exit 0 = all PASS (not a human Yes).

Write the printed markdown to the current stage `output/VERIFICATION.md` (or refresh `dev/36_actual-app-verification/04_first-run/output/VERIFICATION.md`).

## Judgment layer (optional, parallel)

If the user asked for a swarm, spawn **read-only** explore agents, one per failed (or all ten) behaviour ids. Each must read the named Kotlin/Python files and quote evidence. Synthesize; do not let a swarm PASS a mechanical FAIL.

## Not this skill

- Implementing the plan editor or replacing Draft (that's a later Next after this report).
- Maestro/Appium install (FRAMEWORKS.md: optional later).
- Play Store, public Ollama, model-auto-write-current.
