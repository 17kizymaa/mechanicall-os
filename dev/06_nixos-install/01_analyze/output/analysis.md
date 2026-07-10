# 01_analyze: NixOS 300GB Partition Install on Apple HDD (via Current Alpine Bridge)

**User Query (Layer 4)**: "You have permission to perform the mounting bridge step to the rest of the operations; I want to install NixOS as a new 300GB partition (overwriting 300GB of the probably empty Alpine OS space...) on my device. Go!"

**Scope**: This analysis uses ONLY the declared inputs for the stage:
- Layer 1: ../CONTEXT.md (routing)
- Layer 3: ../../CORE_PRINCIPLES.md (and project rules)
- Layer 4: the query + verified disk facts from direct inspection in this session

No unrelated history loaded.

## Verified Current Disk Layout (Reality from lsblk, parted, blkid, df, mount)

Device: /dev/sda — 500GB ATA APPLE HDD HTS547 (sata, MacBook Pro hardware "mbp-edge")

Partition table: GPT

- /dev/sda1: 200MB vfat, label "EFI", mounted at /boot. Flags: boot, esp. **KEEP UNTOUCHED** (EFI for current boot).
- /dev/sda2: 150GB (139.7G reported), APFS "Macintosh HD". This is an Apple File System container. **HIGH RISK** — may contain macOS data or the primary Mac volume. Do not overwrite without explicit further confirmation.
- /dev/sda3: 350GB (325.9G/319.7G usable) ext4, label "alpine-root", mounted at / as current root. **Only ~3.8-3.9GB used**. This is the "Alpine OS space".

Free space on disk: Essentially none outside existing partitions. Tiny gaps (kB scale) at boundaries. The "empty" space the user refers to is inside the sda3 ext4 filesystem (~316GB free inside the 350GB allocation), not unpartitioned space.

Current Alpine: v3.24.1, root on sda3 (UUID 1315b2b2-18b1-41ee-accd-f9e6897ed1e4), /boot on sda1. Boot cmdline uses the ext4 root.

The 2GB USB (/dev/sdb1) is currently our GROK-PORTABLE-DE ext4 (from prior task), not an Alpine live.

No /nix directory or `nix` command present.

## Requirements Translation

- New 300GB partition for NixOS root.
- Overwrite ~300GB of the "empty Alpine OS space" → interpret as shrinking the sda3 allocation by ~300GB (Alpine keeps ~50GB for its 4GB usage + headroom).
- Use "current session as mounting bridge" → current Alpine can:
  - Install nix tools.
  - Prepare /mnt target (once partition exists).
  - Generate NixOS configuration.
  - Run nixos-install into the mounted target.
- Overwriting happens on the device (Apple HDD).

## Constraints from CORE_PRINCIPLES (Layer 3)

- **Filesystem single source of truth**: All plans, configs, and commands must be written as plain files/scripts (cat/grep/diff friendly). No magic state.
- **Markdown + Python only userland**: This analysis + generated scripts follow that.
- **High inspectability**: Every fact above came from direct `lsblk`, `parted`, `blkid`, `df`, `mount`. All future commands will be logged the same way.
- **Low overhead**: Use existing tools (parted, mkfs, nix when installed). No heavy frameworks.
- **Active sidecars**: After NixOS install, the awareness-agent repo (from our portable USB) should be copied in so the new system starts with .context.md etc.

## Risks (Explicit, Inspectable)

1. **Running system breakage**: sda3 is the live root. Resizing its partition or filesystem from here will corrupt or crash the current Alpine session.
2. **Data loss on sda2**: APFS Macintosh HD likely holds macOS or user data. Overwriting it would be catastrophic on Mac hardware.
3. **No free space**: Cannot create 300GB partition without shrinking sda3 (or touching sda2). Shrinking requires the filesystem first resized smaller (resize2fs), then the partition boundary moved (parted resizepart).
4. **Boot complexity**: Dual EFI boot on Mac (Apple HDD). NixOS bootloader (systemd-boot or grub) must be added to existing EFI without breaking current Alpine entry.
5. **NixOS on this hardware**: Apple-specific quirks (T2 chip if present on the MBP, WiFi, etc.) may require extra config.
6. **Current USB**: Our 2GB device is now data-only (Grok portable). Not usable as live installer without additional steps.

Shrinking a mounted root ext4 **cannot** be done safely. Requires booting external media.

## Proposed Path Using Current Session as Bridge (Non-Destructive Prep First)

The current Alpine session **can** safely act as bridge for preparation:

1. Install nix (single-user, no disk change).
2. Write a NixOS configuration.nix targeting a future /dev/sda4 (or whatever number after resize).
3. Generate a Python/shell behaviour script that documents the **exact** live-media sequence for the partition shrink + new partition + mkfs + mount + nixos-install.
4. Once user provides live media boot (or confirms), the bridge mounts the target and completes install.
5. Copy awareness-agent from the portable USB into the new NixOS for continuity.

## Concrete Outputs for Review (Layer 4)

- This analysis.md
- summary.md
- disk-analysis.py (the Python behaviour that produced the mechanical facts above — run it to re-verify)
- (Next stages will produce the actual config.nix and the full bridge script)

**Do not execute any partition or resize commands from the current running Alpine.**

All facts are directly from the filesystem and block devices. Review the numbers and risks before any "Go" on destructive steps.

Next gate: After human review of output/, instruct "proceed to 02_plan" (or provide edits/clarifications on which space exactly to overwrite and confirmation on sda2 safety).