# CURRENT proposal — 2026-08-24 sit-distro-gate

**Not law. Model must not overwrite live `CURRENT.md`.**

**APPLY: human must approve then merge — model must not overwrite CURRENT without human gate.**

After apply:

```bash
cp examples/propose-current/CURRENT-sit-distro-gate.md CURRENT.md
aether next sit-distro-gate
aether approve "closed-tester distro gate: contain zip, stock-phone Publish, API 36, then Play internal"
aether current validate
```

Live file to replace: root `CURRENT.md` (Next `sit-testers` APPROVED). Dual-Next stays Reject — this is a **replacement** Next, not a second one.

---

## You forgot this (live contract, now)

| | Live |
|---|------|
| **Next** | `sit-testers` |
| **Approval** | APPROVED |
| **Objective** | Testers sit this face. First sit = 7B PROPOSE template. Off-LAN then Play **internal/closed**. Not production. SOS parked. |
| **Still open under that Next** | LTE sideload (cellular AVD done). Play Console upload (no keystore in git). |
| **Reject** | Play **production**, Funnel, public Ollama, dual-Next, model Yes, A33-as-STORM |

That Next got you a face and PR #7. It did **not** get a Play-uploadable artifact. The phone’s own distro bar (`13_FIRST_DISTRIBUTION_PR_GPT5.6.md`) says **NO**.

---

## Summary of proposed change

New action-id **`sit-distro-gate`**. Close the GPT-5.6 distribution gates so Play **internal/closed** upload is possible. Keep production Reject.

Grounded in:

- Live `CURRENT.md` (sit-testers APPROVED)
- Probe `.aether/proposals/PROBE-20260824-zip-servers.md`
- Phone file `.aether/proposals/13_FIRST_DISTRIBUTION_PR_GPT5.6.md` (pulled via mbp-edge adb from `/sdcard/mechanicall/sessions/13_FIRST_DISTRIBUTION_PR_GPT5.6.md`)

Full apply-ready body: `examples/propose-current/CURRENT-sit-distro-gate.md`

---

## Zip / sharing / servers (verified 2026-08-24)

**Sharing is not online.**

- Drop `:8765` **down** (127.0.0.1 and 192.168.0.51 refused). Twin `:7078` down.
- Stale lab zip from 2026-08-23 (`sitrae`, 5 files) still in `.inbox/drop/`.
- Ollama 7B **up** (`*:11434` / LAN / tailnet). Public Ollama still Reject.
- Zip extractor **unsafe** (absolute paths can escape dest **on poll**, before Accept). Required before any drop restart.
- Do **not** call SEND FOLDER a store feature on LTE. G4 JNI still BLOCK.

## Play prep vs 13_* bar

| 13_* gate | Now | This Next |
|-----------|-----|-----------|
| 1 ZIP containment | FAIL | first action |
| 2 stock-phone Publish (`run_aether(["approve"])` needs POSIX aether) | FAIL (`android/README.md` already says so) | second action |
| 3 Android CI assemble/AAB | FAIL (`tests/run.sh` only) | with API 36 |
| 4 emulator first-sit→Decide smoke | source-string 10/10 only | named |
| 5 targetSdk 36 | **34**; Play new/update apps need API 36 from **2026-08-31** (7 days) | required |
| 6 off-LAN/LTE | cellular AVD receipt exists; LTE does not; USB A33 ≠ LTE | LTE receipt before Console |
| 7 human CURRENT apply | this proposal | human |
| 8 narrow release artifact | PR #7 is 645 files | signed AAB + checksum + limitations |
| 9 call it closed testers | PR claims testers | keep; **not production** |

13_* : merge now **No**. Play internal **today** **No**. Worth finishing **Yes**.

---

## Before / after (header fields)

| Field | Live | Proposed |
|-------|------|----------|
| Next | `sit-testers` | `sit-distro-gate` |
| Approval | APPROVED | PENDING (until you apply + `aether next` + `aether approve`) |
| Objective | testers sit this face; Play internal after off-LAN | closed-tester **Play-uploadable** distro: zip safe, stock Publish, API 36, signed AAB |
| Play production | Reject | **still Reject** |
| Drop | lab, assumed | **down until zip contained**; then 127.0.0.1 only |

Keep / Reject / Limits: inherit sit-testers, add `restart-uncontained-drop` and `play-upload-pr7-as-is` to Prohibited. Park C-series notepad. Park SOS. Park Funnel.

---

## Fidelity checklist

- [x] Still **one** Next (`sit-distro-gate`)
- [x] Models never approve / never `aether next`
- [x] No secrets in git (keystore stays off-tree)
- [x] Silence ≠ permission
- [x] Bind / Send / drop / Play upload are **not** Decide
- [x] Phone bind ≠ this repo
- [x] A33 not used as STORM (USB read of the 13_* file only)
- [x] This file does **not** write live `CURRENT.md`

---

## What I did not do

- Did not overwrite `CURRENT.md`
- Did not `aether next` / `approve` / `reject`
- Did not start `aether_drop.py` (unsafe unzip)
- Did not tap Confirm
- Did not open Play Console
- Did not mint a keystore
