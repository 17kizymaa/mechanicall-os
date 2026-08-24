# SPIKE — mobile-planning-demo (demo APK only)

**Status:** resumed 2026-08-18 · host rehearsal green · **not** product · **not** casual-core · sitting still cancelled  
**Calendar:** 4–8 weeks (weeks 1–6 host-done; week 7 host rehearsal done)  
**Authority:** operator Next **and** Action id are `mobile-planning-demo` (human applied repair A).  
**Decisions:** `decision-tree.md` (interview closed 2026-08-16)

This is a **sideload demo** on *your* Android phone so a client can plan live: proposal-doc editor + visible CURRENT + Yes/Not yet + receipts. Remote Ollama on myarch via Tailscale. Same `aether` as desktop.

**Not this spike:** Play Store, iOS, Flutter, Kotlin protocol clone, Session/anphuni.com, second CURRENT on the desk, bubble-chat product, full `AETHER_VERBS` keypad, attach-picker UX, OT/CRDT.

---

## One-screen contract

```
[ Live CURRENT — read-only projection of pocket CURRENT.md ]
[ Receipts — brief / last events / drift                       ]
[ Yes ]  [ Not yet ]     optional: Next (re-SELECT, not main Yes)

[ Proposal editor — the session                               ]
  Agent and client type here.
  File: <pocket>/PROPOSE-CURRENT.md  (or examples/propose-current shape)
  Agent never writes CURRENT.md.
```

Yes = apply visible PROPOSE fields into pocket CURRENT + `aether approve`.  
Not yet = reject / leave CURRENT.  
Editor save = PROPOSE only.

---

## Bind (law)

| Piece | Where |
|--------|--------|
| Operator law | `mechanicall-os/CURRENT.md` — this Next. Do not bind the app here. |
| Pocket Domain | Client project **outside this repo**, on **phone storage** |
| Engine | Chaquopy ships `bin/aether` + needed `python/` |
| Chrome | Kotlin/Compose |
| Model | myarch Ollama over Tailscale (`:11434`). **Whole pocket tree** each editor turn (D9=3, demo-only) |
| Network | Tailscale. No public bind. |

Refuse to open if bind path is this repo root.

---

## Weeks (demo, not polish)

| Week | Done when |
|------|-----------|
| 1 | **Host done** — `aether_pocket.current` / `validate` on a temp pocket via real `bin/aether`. APK assemble = SDK leftover |
| 2 | **Host done** — `projection()` + brief/events/drift. Compose panes exist |
| 3 | **Host done** — `write_propose` does not touch CURRENT (tested) |
| 4 | **Host done** — `yes` / `not_yet` contract tests (10/10). CLI events + DECISIONS |
| 5 | **Wired, not live-called** — `agent_edit_propose` + whole-tree packer |
| 6 | **Face scaffolded** — Compose Yes / editor / receipts. Mum pass needs a sideload + POSIX `aether` on device |
| 7 | **Host done 2026-08-18** — `scripts/rehearse-pocket-spike.sh` + suite hooks. No live sitting. |
| 8 | **Face up 2026-08-18** — `08_serve-face` · http://192.168.0.51:8765/ · GET ≠ Yes. Sitting still cancelled. No new surface. |

Ship week 6 if 7–8 are idle. Interaction polish is **after** this sprint.

---

## Verb map (main face)

| Face | `aether` |
|------|----------|
| CURRENT pane | `current` (display) |
| Receipts | `brief`, events tail, `drift` |
| Yes | apply PROPOSE + `approve` |
| Not yet | `reject` |
| Next (secondary) | `next <id>` after APPROVED |
| Editor agent | Ollama; writes PROPOSE only |
| Hidden / not built | full verb list, garden, rival, shell, panel TUI |

---

## Honest limits (say these in the sitting)

- Demo build on your phone. Not Mechanicall-as-an-app-store-product.
- The model on your desk sees **the whole pocket folder**. Put only what they may send.
- Chat is ephemeral except PROPOSE + CURRENT + events.
- Models never approve. Silence ≠ permission.

---

## Brake face (2026-08-18)

Contract: `BRAKE.md` (same folder). Sendable sitting = URL first (`scripts/send-brake.sh`), APK second (sideload lab). GET is never Yes. `RECEIPT.md` is what they keep tomorrow.

## First implement step (operator body is aligned as of 2026-08-18)

1. Create/pick the pocket folder **on the phone**, outside this repo.  
2. `aether current init` / seed a real client CURRENT there.  
3. Scaffold the Android module as **lab** (do not claim `android/` as core).  
4. Chaquopy: invoke `aether current` and show it. That is week 1.

Do not start week 5 before week 4’s contract test exists.

---

## Human gates on *this* repo

I do not run `aether approve` / `next`.  
Operator CURRENT body aligned via repair A (2026-08-18). Do not silent-rewrite it.
