# Proposed CURRENT update (draft — not authority)

**Project:** mechanicall-os (operator tree)  
**Date:** 2026-08-16  
**Author:** grill + spike (propose only)

## Observations

- Live `**Next:**` field is already `mobile-planning-demo`.
- CURRENT body (This Next, Action id, Brief, Limits, Approval condition) still describes `casual-core-interface`.
- `.aether/events.jsonl` has 2026-08-16 human APPROVED rows and no `next_selected` to `mobile-planning-demo`.
- Closed decision tree: `decision-tree.md`. Executable spike: `dev/23_mobile-planning-demo/output/SPIKE.md`.
- App projection is a **demo build only** (sideload, your phone, live client planning).

## Inferences

- Human intended this Next to be the demo APK spike, not continued casual-core contract writing.
- Body drift will confuse preflight (`casual-core-interface` vs `mobile-planning-demo`).
- Casual-core is paused, not cancelled.

## Unknowns

- Concrete pocket-folder path on the phone (client project; outside this repo).
- Whether events should gain a late `next_selected` row (human / `aether next` only).

## Proposed CURRENT change

```markdown
**Objective:** Ship a **demo-only** Android app projection for live client planning on the operator’s phone: pocket Domain + proposal-doc editor + human Yes/Not yet + receipts, talking to remote Ollama on myarch over Tailscale, using the same `aether` (Chaquopy). Not a product. Not casual-core. Not Play Store.
**Phase:** IMPLEMENT
**Status:** APPROVED
**Next:** mobile-planning-demo
**Approval:** APPROVED

## This Next
- Sideload demo APK. Client is the planner. Bind a client folder **on the phone**, outside this repo.
- Face: live CURRENT + receipts + Yes/Not yet + PROPOSE editor (agent/client edit draft only).
- Yes = apply PROPOSE + `aether approve`. Agent never writes CURRENT.
- Ollama context = whole pocket tree (demo shortcut). Tailscale to myarch:11434.

## Next allowed action
**Action id:** `mobile-planning-demo`

Brief: `dev/23_mobile-planning-demo/output/SPIKE.md`

1. Week 1: Chaquopy + `aether current` on a pocket path.  
2. Weeks 2–4: CURRENT/receipts panes; PROPOSE editor; Yes/Not yet via real `aether`.  
3. Weeks 5–6: Ollama + mum sitting.  
4. Weeks 7–8: buffer only. No new surface.

## Limits
- Demo build only — do not productize, do not fold into casual-core this Next
- One law: ship `bin/aether`; no Kotlin protocol clone
- Do not bind the app to this repo’s CURRENT
- Do not commit secrets; do not public-bind Ollama
- Interaction polish after this sprint

## Approval condition
Human already selected this Next. Apply this body so Action id matches `**Next:**`. Then preflight `mobile-planning-demo` only.
```

## Conflicts with existing authority

- Action id / Brief / Limits / Approval condition still name `casual-core-interface` and forbid multi-surface implement.
- Keep still says casual path / no child Domain as *operator* session authority — pocket bind is a **different folder**, not a sub-CURRENT on this tree.
- Done still claims `docs/CASUAL-CORE-INTERFACE.md` (file missing). Leave that as inventory; do not pretend this spike is that contract.

## Human decision required

- [ ] Apply proposed fields to CURRENT.md  
- [ ] Reject and leave CURRENT unchanged  
- [ ] Revise and re-propose  

**Do not** run `aether approve` from a model or agent.
