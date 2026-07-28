# Stage: 10_client-one-emachine — session transfer + RECONFIGURE

## Role
Operator-side execution stage for **client one** (eMachine E640, Alpine USB live, thermal-limited).  
Agent session remains on the mechanicall-os source host; product is a transfer package + network reconfigure runbook.

## Inputs
- Layer 0: `AGENTS.md`, `CORE_PRINCIPLES.md`, meta-agent skill
- Layer 1: this folder’s `CURRENT.md` (authority)
- Layer 3: `SPEC-v0.2.md`, `docs/getting-started.md`, `examples/dev-task/CURRENT.md`
- Layer 4: operator answers (Delroy home, INIT deferred, Next=RECONFIGURE, WLAN not tether)

## Process
1. Bind authority in `CURRENT.md` (Next: `reconfigure-wlan`).
2. Produce transfer docs in `output/` (handoff, WLAN runbook, disk decision, proposed client CURRENT, manifest).
3. Do **not** create `/home/Delroy` project or run client `aether init` until SSH + later auth.
4. After human brings WLAN up (console on device), SSH from operator host and copy `output/` + selected repo paths.
5. Halt for human review before INIT.

## Outputs
- `output/SESSION-TRANSFER-2026-07-28.md`
- `output/RECONFIGURE-WLAN-ALPINE.md`
- `output/DISK-PARTITION-DECISION.md`
- `output/PROPOSED-CLIENT-CURRENT.md`
- `output/TRANSFER-MANIFEST.md`
- `output/THERMAL-TUI-NOTES.md`
- `output/summary.md`

## Deferred (not this stage)
- `aether init` / `aether current init` under `/home/Delroy`
- Permanent install off Alpine USB
- GUI desktop
