# BEHAVIOURS — what the sit must do

**Not CURRENT. Not Decide.** Scored by `python/app_verify.py` and `/app-reviewer`. Fail closed on missing evidence.

Pitch (people-app): *You decide. AI does the point-and-clicking — under a plan you can read and a yes only you can give.*

Walk: bind → show-plan → propose → gate → (do after Yes) → receipt.

| id | Need | Not | Evidence |
|----|------|-----|----------|
| B1 bind-first | Unbound: FOLDER is the only module. One path. Operator tree refused. | Auto-bind mechanicall-os or a hidden default pocket as the product | source + uidump |
| B2 plan-readable | CAPITALISED live fields. Objective and Next first. | Protocol dump as the only page | source + uidump |
| B3 plan-manual-edit | Human can edit plan fields on PLAN without chat. Writes PROPOSE or a draft, never live CURRENT until Decide | Read-only cards; chat as the only editor | source |
| B4 draft-is-workshop | Draft is a plan workshop: live vs proposed fields. Desk proposes. | Chat-app identity (composer+bubbles as the product) | source + uidump |
| B5 propose-not-current | Draft/Send writes PROPOSE only. CURRENT bytes unchanged until Yes | Model auto-write CURRENT | source + tests |
| B6 decide-only-yes | Two-tap + Why. Bind / Send / open / RETURN / DIR / FILES are not Yes | First tap is Yes; Confirm with empty Why | source |
| B7 gate-instrument | GATE IDLE/WARM/GATE/QUIET. Streamed thinking. Not typing dots, not the Send label | “…” / Send renamed GATE | source + uidump |
| B8 receipt-tomorrow | Receipt is what they already said. Empty is honest | Fake agree on open | source |
| B9 window-honest | `resizeableActivity`. No painted 92% card. OEM pop-up optional | Fake traffic-light VST filling the glass as “windowed” | source |
| B10 bind-not-repo | Phone bind ≠ this operator tree | Binding mechanicall-os | source + tests |

Walkers **never** tap Confirm. Models **never** `aether approve`.
