# FACE-WALK — people-app on the phone (one screen)

**When:** 2026-08-19  
**Next:** `people-app-phone-seat` · SELECT / REJECTED · opening this file is not Yes  
**Worth:** a person can sit *their* folder and still say they did not Yes.

## One sentence

You have not said yes yet. Opening this app is not a yes. Bind is not a yes. Only **Yes** is.

## One screen (the walk, not a wizard)

```
[ 1 Bind    — name their folder; refuse mechanicall-os ]
[ 2 Plan    — Objective, Next, decision; full file hidden ]
[ 3 Draft   — proposal; save does not change the plan   ]
[ 4 Decide  — Yes (two-tap) · Not yet                   ]
[ 5 Receipt — last decision, or none                    ]
```

| Face | People-app stage | Meaning |
|------|------------------|---------|
| **Bind** | `01_bind` | Their folder. Refuse operator tree. Default `/sdcard/mechanicall-pocket`. |
| **Plan** | `02_show-plan` | Objective + Next + Approval/Status. Not a monospace dump. Full plan on request. |
| **Draft** | `03_propose` | `PROPOSE-CURRENT.md`. Save ≠ Yes. |
| **Yes / Not yet** | `04_gate` | Two-tap Yes. Agent never taps. |
| *(engine)* | `05_do` | Only after Yes. Not a button. |
| **Receipt** | `06_receipt` | `RECEIPT.md` they can open tomorrow. |

No verb museum. No bubble chat. The word **aether** does not appear. No Invite / Wake this turn.

## Law the chrome must not break

- GET / open / Bind / expand plan is never Yes.
- Silence is never Yes.
- Agent may edit the draft only (under **More**, collapsed).
- Yes is a two-tap that calls the same `yes()` as the tests.
- Refuse if the bind path is the mechanicall-os operator tree.
- If the folder is missing or refused: show Bind only. Hide Plan / Draft / Decide.
- If CURRENT is missing: say so. Do not invent law.
- `open_is_yes` is always false in `face_state`.

## Engine (Python, one source)

`python/aether_pocket.py` → `face_state(path) -> dict`  
`android/app/src/main/python/aether_pocket.py` is a copy (`scripts/sync-pocket-engine.sh`).

Kotlin parses JSON. Kotlin does not parse CURRENT.

## Strings

- Launcher: **Mechanicall**
- Title: **You have not said yes yet**
- Sub: Opening this app is not a yes. Only **Yes** is.
- Bind label: **Your folder**
- Bind button: **Bind**
- Bound: This folder is bound. Opening is not a yes.
- Refused: That folder is the operator tree. Bind a different folder.
- Missing folder: This folder is not on this phone yet.
- Missing plan: This folder has no plan yet.
- Empty receipt: No decision recorded yet. The machine did not pretend you agreed.
- Yes confirm: Apply the draft and record that you said yes?
- Footer: Opening is not Yes. Silence is never permission.

## Not this face

Play Store. SeatMate branding. Compose-as-a-new-product. Funnel. Public Ollama. Operator CURRENT. Tapping Yes for them. Package id change.
