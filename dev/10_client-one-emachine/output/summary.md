# Summary — 10_client-one-emachine (2026-07-28)

## Done on operator host

- Branch: `session/client-one-delroy-reconfigure` (from `master` @ `b7dc96d`)
- Stage authority: `CURRENT.md` with **Next:** `reconfigure-wlan`
- Transfer package written under `output/`
- Project INIT and `/home/Delroy` product tree **deferred**
- USB tether marked **not preferred**; WLAN reconfigure runbook is the active path

## Blocked on client hardware/console

- `wlan0` association + DHCP + `sshd`
- Unknown IP on LAN (eMachine not yet in operator neighbor table as a known host)
- Disk layout choice deferred to decision tree (no mounts performed from here)

## Your immediate console work (client)

1. Follow `RECONFIGURE-WLAN-ALPINE.md` sections A → success criteria  
2. Paste `ip -4 addr show wlan0` (and `lsblk` if easy) back to operator  
3. Operator runs rsync from `TRANSFER-MANIFEST.md` / session handoff  

## After transfer

- Human review gate before any `aether init` under Delroy  
- Proposed client authority: `PROPOSED-CLIENT-CURRENT.md` (draft only)
