# CURRENT

<!-- PROPOSAL ONLY — place under the future project path after INIT.
     Human must edit and own this file. Not active on the eMachine until copied
     and approved. Operator stage authority remains:
     dev/10_client-one-emachine/CURRENT.md -->

**Objective:** Run Mechanicall alpha on client-one (Delroy / eMachine) with TTY TUI and inspectable authority.
**Phase:** CAPTURE
**Status:** DRAFT
**Baseline:** session-transfer-2026-07-28
**Next:** unset
**Approval:** PENDING

## Keep
- Filesystem authority (`CURRENT.md` + events)
- TTY / `aether panel` TUI (no GUI required)
- User home `/home/Delroy`
- WLAN → LAN as primary network

## Reject
- USB tether as preferred network
- Hidden databases / vector stack
- Autonomous multi-agent studio claims

## Limits
- Thermal-limited hardware: avoid heavy builds and full desktop
- Alpine USB may be ephemeral — durable work needs an explicit disk decision later
- Operator may assist over SSH; human still owns approve/reject

## Next allowed action
(unset until human COMMITs after transfer — candidates: `create-unix-user-delroy`, `aether-onboard`, `mount-home-partition`)

## Approval condition
Human edits this file in the real project path, sets **Next**, and runs any needed `aether approve` from that path.

## Prohibited
- prefer-usb-tether
- wipe-disk
- install-gui-required
- skip-preflight
