# Stage: 10_client-one-emachine

## Role
Operator-side stage for **client one** (eMachine E640). Code and docs stay on this host.  
Two tools for teaching: **aether panel** (plan + human yes/no) and **grok** (AI). Same TTY is ops only.

## Inputs
- Layer 0: `AGENTS.md`, `CORE_PRINCIPLES.md`
- Layer 1: this folder’s `CURRENT.md`
- Layer 3: `SPEC-v0.2.md`, approved plan (plain panel + tether + Grok install)
- Layer 4: educational sprint notes (labels, tether first, no chat facade)

## Process
1. Keep a normal single-**Next** CURRENT (no pending-until-STOP dual-agent mode).
2. Plain-language panel labels + short help in `python/aether_panel.py`.
3. Client-facing runbooks: tether SSH, brightness, Grok install, same-TTY layout.
4. Optional panel action: open Grok in this folder (leave and return) — not a product merge.
5. Halt for human review before client INIT under Delroy.

## Outputs
- `output/SSH-TO-TETHERED.md`
- `output/DEVICE-OPS.md`
- `output/GROK-INSTALL.md`
- `output/SAME-TTY.md`
- `output/summary.md`
- (older transfer/WLAN notes retained but demoted)

## Deferred
- `/home/Delroy` project INIT
- WLAN-first
- Package transfer P0
- Chat facade inside panel
