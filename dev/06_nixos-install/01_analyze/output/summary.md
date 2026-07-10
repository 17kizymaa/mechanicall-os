# 01_analyze Summary — NixOS 300GB Partition (Alpine Bridge)

## Verified Layout
- /dev/sda (500GB Apple HDD, GPT)
  - sda1 200MB EFI vfat (/boot) — KEEP
  - sda2 150GB APFS "Macintosh HD" — HIGH RISK (possible macOS data)
  - sda3 350GB ext4 "alpine-root" (/ , ~4GB used) — the "Alpine space" user wants to carve from

No significant unallocated space on disk. "300GB empty" is inside the sda3 filesystem, not free partitions.

## Key Constraints
- Current session **runs from sda3**. Cannot safely shrink/resize sda3 partition or FS while mounted.
- Requires external live media (Alpine live or NixOS ISO) for any partition changes.
- Current 2GB USB is our data USB (GROK-PORTABLE-DE), not live.

## Requirements Met So Far
- User permission noted for "mounting bridge" (current Alpine used to prepare nix, config, mount target).
- Plan uses only plain files + Python behaviour.
- All facts inspectable via lsblk/parted/etc.

## Recommended Immediate Safe (Non-Destructive) Bridge Steps
1. Install nix on current Alpine: `curl -L https://nixos.org/nix/install | sh`
2. Prepare NixOS config targeting future partition.
3. Produce exact commands + script for live-media execution of the shrink + new 300GB partition + nixos-install.

**Do NOT run parted/resizepart/mkpart from here.**

Full details and generated commands in analysis.md + disk-analysis.py (run it to re-emit).

**Human gate**: Review output/. Edit or say "proceed to 02_plan" (with any clarifications on exact sizes or sda2 handling). 

This session can continue as the bridge for config generation and nix setup. Partitioning itself needs a reboot to live media.