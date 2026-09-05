# sit-dest-preview send — 2026-09-05

**USB ≠ LTE. Not testers. Confirm not tapped.**

## Network profile (best path)

| Path | Result |
|------|--------|
| LAN `192.168.0.51` (myarch enp34s0) ↔ `192.168.1.88` (mbp-edge wlan0) | **dead** — different /24, 100% ping loss both ways |
| Tailscale `100.90.85.68` ↔ `100.70.86.90` | **only live path** — direct peer, IPv4 ping ~38 ms |
| SSH/SCP over TS | ~26 KiB/s (2 MiB in 77 s) |
| Raw TCP :9876 over TS | **best of the live paths** — ~0.03–0.04 MiB/s, 58 MiB in 1626 s |
| Taildrop `tailscale file` | denied on edge (needs `--operator`) |
| Funnel | Reject |

Chosen: **Tailscale IPv4 TCP myarch→edge:9876**, then **adb USB** `usb:3-2` on serial `RZCW2038KHN`. Last hop USB is fast; the bottleneck is TS bulk (~40 KiB/s).

## Send

- APK `0.19.4-dest-preview` vc **29**
- md5 `bd2bfbeeb60ebda4e68498dad4b6083c` local = edge
- `adb install -r -d` **Success**
- on-device `versionName=0.19.4-dest-preview` `versionCode=29`
- look: `look-after-send.png` (wake + screenshot; whatever was on the panel)

Live CURRENT at send time: Next `sit-dest-preview` **REJECTED** (human: merge toward first-sit-patching). This send is lab USB, not a recant of that reject.

Opening the app is not Yes.
