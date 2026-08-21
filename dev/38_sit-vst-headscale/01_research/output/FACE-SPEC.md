# FACE-SPEC v2 — rack around paper

**Not CURRENT. Not Yes.** Implements T2 (genuine instrument frame, paper inside) on top of sit-join FACE-SPEC v1. Identity is **rack + score**, not chat, not a painted plugin window.

v1 (paper Plan/Draft, DESK strip, hunk Accept/Reject) still holds. This file only changes chrome and GATE.

## Walk (unchanged)

Unbound: **FOLDER** only (B1). Operator tree refused (B10).  
After bind: compact **rack** (title + LCD + DESK strip) around the document.  
Then: **PLAN** (published) · **DRAFT** (Suggesting) · **DECIDE** (Publish) · **RECEIPT**.

Gray outside a module overlay still closes that module. Strip stays.

## Rack (the VST *frame*)

Steal: Camel Space / generic 2000s plugin *editor* hosted by a DAW. We fill the activity. Android OEM is the host.

```
┌─────────────────────────────────────────────┐  bevel: lite inner + dark outer
│ MECHANICALL  <bound name>     DIR   FILES   │  title bar (dark, LCD gold name)
│ LCD  NEXT sit-vst-headscale · LOAD 9/16     │  amber LCD — Next + GATE only
│ JOIN invited   WAKE sleeping                │  DESK strip (after bind)
│ [paste preauth · login-server if needed]    │
├─────────────────────────────────────────────┤
│ PLAN  DRAFT  DECIDE  RECEIPT                │  banks (tabs)
│                                             │
│   cream paper document (score)              │  Plan/Draft/Decide/Receipt
│                                             │
├─────────────────────────────────────────────┤
│ GATE LOAD ▓▓▓▓▓░░░░░░░░░░░   DESK           │  trance-gate row
└─────────────────────────────────────────────┘
```

| Rule | Do | Do not |
|------|----|--------|
| Size | `fillMaxSize` + `resizeableActivity` | Painted 360×560 letterbox; fake 92% |
| Window buttons | none | Traffic-light WinDots |
| LCD | Next id + GATE phase/count | Chat log; whole Objective |
| Bevel | 6.dp pad, 1.dp lite + 2.dp dark | Gradient soup, Imagine mock as law |
| Paper | cream/ink inside the rack | Yellow LCD as the document |
| Knobs | none this Next | Verb museum |

`PluginWindow` already fills the activity and documents the letterbox fail. Keep that comment. Restyle title/LCD/GATE to read as a rack; keep paper body.

Palette: keep sit-join cream paper (`Host`/`Panel`/`Ink`/`Suggest`). Rack chrome may go **darker on title + LCD + GATE only** (already `Title`/`LcdBg`). Do not flood the score with yellow.

## DESK strip (after bind)

Same verbs as v1. JOIN well now prefers **Headscale preauth**. WAKE still wol-pi.

| Control | States | Not |
|---------|--------|-----|
| JOIN | not-on-net / invited / connected / refused | Yes |
| well | paste preauth (+ login-server URL if unset) | secret store |
| WAKE | sleeping / waking / up | Yes; disabled until connected **or** lab USB/LAN |
| lamp | GATE table in GATE-CONTRACT.md | typing dots |

Connected = tsnet Up, not “LAN Ollama answered.”

## PLAN / DRAFT / DECIDE / RECEIPT

Unchanged from v1:

- PLAN = published `CURRENT.md`. Read-only as law.
- DRAFT = Suggesting on `PROPOSE-CURRENT.md`. Hunk Accept/Reject. SEND = focused hunk. Last desk say one line.
- DECIDE = two-tap + Why. Copy: **Publish the proposal.**
- RECEIPT = what they already published. Empty is honest.

## GATE face

See `GATE-CONTRACT.md`. Strip labels **LOAD** (amber fill) then **STREAM** (purple steps). QUEUE n if a Send is waiting. Quiet after. Not `…`.

## Bind (grey, not Limits)

T8c: do **not** require a pre-existing CURRENT.md to bind. Many folders allowed. Operator tree still refused. Location *may* be the APK install dir — **not this FACE-SPEC unless 02 has a cheap fence**; default stays: bind a user-picked folder, refuse operator markers.

## Never

- Hunk accept / schema / JOIN / WAKE / LOAD / STREAM / twin-pull as Yes
- Dump whole CURRENT into the 7B
- Invite/preauth in git or APK
- Painted maximise / fake window
- Chat-app chrome as identity
- Imagine-mocks as the spec
