# GOAL — one sit, four pages, Bind as a slot

**Not CURRENT.** This is the phone-seat contract for `0.8.0-vst`.

## Pages (the product)

| # | Page | Role |
|---|------|------|
| 01 | Plan | CAPITALISED fields |
| 02 | Chat | slim desk through **myarch** |
| 03 | Decide | the only decision surface; buttons fill the window |
| 04 | Receipt | trail + events |

## Outside the pages

**Bind** is a folder slot on the plugin title bar (and a first-run overlay if unbound/refused). It is not a tab. Path persists.

**PROJECT** lists files in the bound folder (read).

## Desk (this machine)

myarch *is* the desk. Chat tries, in order:

1. `http://127.0.0.1:11434` (USB `adb reverse` via edge)
2. `http://192.168.0.51:11434` (LAN)
3. `http://100.90.85.68:11434` (Tailscale)

Short timeout per hop. Fail visible. No public bind. `scripts/desk-through-a33.sh` wires USB reverse through mbp-edge.

## Copy

Preach only on Decide. Other pages do not repeat the decision word.

## Image

00s VST: grey plugin window on a dark host, does not maximise, fake window buttons, LCD for Next.

## STORM

Parallel sits need isolated pockets + (research) emulator/SDK — see `03_storm-research/`. Do not share the live A33 across agents. Walkers never Confirm.
