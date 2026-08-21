# Proposed CURRENT update (draft — not authority)

**Project:** mechanicall-os  
**Date:** 2026-08-18  
**Author:** human asked “how is this useful for people?” + start from the actual app (Docker, OpenHands)

`APPLY:` human must reject or re-SELECT, then merge — model must not overwrite CURRENT without human gate.

## Summary

Close `mobile-planning-demo` as the live Next. The phone/LAN face stays lab. New Next: **one runnable app** — Docker Compose boots OpenHands (does the work) + aether law (one plan, human Yes). Not Play Store first. Not a swarm dashboard first.

Full replacement: `dev/24_repair-current-one-next/01_propose/output/CURRENT-D-app-first-openhands.md` (written with this propose).

## Observations

- Live Next is `mobile-planning-demo` (repair A). Face is up at `http://192.168.0.51:8765/`. Twin still `name-the-outcome` / REJECTED. Sitting 2026-08-16 cancelled.
- PRODUCT pitch: “You decide. AI does the point-and-clicking — under a plan you can read and a yes only you can give.”
- `docs/SINGLE-APP-DISTRIBUTION.md`: casual users will not run `aether` in a terminal; one app is the product shape; that UX is **incomplete**.
- Closed `decision-tree.md` said this phone spike is **not** Play Store / not product. That still holds for the *spike*. This propose is a **new** Next, not a rewrite of that grill.
- Live Reject includes “Play Store / app-first product claim **on this Next**.”

## Inferences

- People do not need a protocol demo. They need: install or `compose up` → agent works on *their* folder → they can read the plan → they tap Yes on the consequential bit → they can leave and resume.
- OpenHands is a reasonable **agent host** (does the pointing-and-clicking). Docker is **packaging**. Neither is law. `CURRENT.md` + `aether` stay law.
- Swarm-capable is a later Next. First useful app is **one** agent, **one** project, **one** Yes. Dual-concurrent-next stays rejected.

## Unknowns

- Which OpenHands image/tag you already trust on this host.
- Whether the first face is the existing LAN HTML, a Compose-published web UI, or OpenHands’ own UI with a Mechanicall Yes strip.
- Whether phone/Play Store is week-1 or after a desktop compose path works.

## Proposed CURRENT change

See `CURRENT-D-app-first-openhands.md`. One Next: `app-first-openhands-compose`.

## Conflicts with existing authority

- Replaces `mobile-planning-demo` (demo / not productize / not Play Store *this Next*).
- Parks the A33 sitting and `:8765` as lab, not the people-facing app.
- PRODUCT core table stays: protocol is core; OpenHands/Docker are the **distribution + agent host**, not a second authority store.
- Does not authorize model-auto-write-current or OpenHands approving itself.

## Fidelity checklist

- [x] Still one Next
- [x] Models never approve
- [x] No secrets
- [x] Silence ≠ permission
- [x] No `model-auto-write-current`
- [x] Header and body match inside the D file

## Human decision required

- [ ] Apply D: `aether next app-first-openhands-compose --reason "people-facing app: compose + OpenHands + aether Yes"` then `cp` the D file over `CURRENT.md`
- [ ] Reject and leave `mobile-planning-demo`
- [ ] Revise and re-propose

**Do not** run `aether approve` from a model or agent.
