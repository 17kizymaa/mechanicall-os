# 01_analyze Summary — Grok IDE USB Bootstrap

## Key Facts Established

- **USB device**: `/dev/sdb` (1.9G USB Flash "Disk", usb transport) — currently a bootable **Alpine-std 3.24.1 x86_64 live ISO**.
  - sdb1: 352M iso9660 (full live environment with kernel, initramfs, apks, syslinux/grub).
  - sdb2: 1.4M vfat EFI.
  - ~1.5G+ raw space available on the physical device.
- **Payload size**: Core awareness-agent (aether sh script + emit script + key .md files + docs + flakes) is **< 200 KiB**. Extremely small.
- The sandbox can see the device, but writes are destructive and must be heavily guarded.

## Requirements
User wants the 2GB USB turned into an **installer** that bootstraps:
- Grok IDE / CLI environment
- awareness-agent repo
- Working `aether` + sidecars (`.context.md`, `.aether/`)

Must follow ICM + CORE_PRINCIPLES: plain files, sh + md + py only for userland, maximum inspectability, sidecars as truth.

## Analyzed Options (ranked)

1. **Augment existing Alpine live USB** (preferred for this hardware)
   - Add data partition using free space.
   - Place repo + `bootstrap-grok.sh` there.
   - Boot the USB (Alpine live), run the bootstrap script.
   - Keeps existing working installer media while adding Grok + awareness.

2. Minimal custom live (more work, very aligned with SPEC "FROM scratch" vision).

3. Data-only / manual copy (safest, least "installer" feeling).

4. Full NixOS re-image on the 2GB (tight fit + current media is Alpine).

## Risks
- Wrong device (sda = 465G system disk = disaster).
- Loss of current Alpine live content on repartition.
- Block writes from this session need explicit human approval.

## Deliverables from this stage
- `analysis.md` (detailed)
- `summary.md` (this file)

All facts, options, and safety considerations are now reviewable in `01_analyze/output/`.

**Human action required**: Review the analysis. Edit files if the direction or constraints are wrong. Then say e.g. "proceed to 02_plan" or give specific adjustments.
