# 01_analyze: USB Installer + Grok IDE + awareness-agent Bootstrap Analysis

**Task**: Use the plugged-in 2GB USB (`/dev/sdb`) as an installer medium to bootstrap a "Grok IDE" environment together with the full awareness-agent repo, aether command, and active sidecars following Mechanicall OS principles.

Date: 2026-06-26
Device identified in this session: 1.9G USB Flash Disk (currently running as Alpine live media).

## Device Facts (gathered via lsblk, blkid, file, fdisk)

- Device: `/dev/sdb`
- Size: 1.9 GiB (2004877312 bytes, 3915776 sectors)
- Model: "Flash Disk", transport: usb
- Current layout (from fdisk + blkid):
  - /dev/sdb : ISO 9660 CD-ROM (bootable), LABEL="alpine-std 3.24.1 x86_64"
  - /dev/sdb1: 352 MiB, iso9660, bootable, contains full Alpine live (vmlinuz-lts, initramfs-lts, modloop-lts, apks/, boot/, efi/, syslinux + grub)
  - /dev/sdb2: 1.4 MiB, vfat (EFI FAT12), small boot support
- Used by ISO: ~351 MiB
- Free raw capacity on device: ~1.5+ GiB remaining if we add partitions or overlay.
- Current state: This USB is a standard Alpine standard live/installer. The sandbox environment itself appears to be derived from or compatible with this Alpine 3.24.1.

Important: `/dev/sda` (465.8G Apple HDD) is the system disk — **never target it**.

## USB Content Snapshot (read-only mount inspection)

Standard Alpine live ISO structure:
- `.alpine-release`
- `apks/` (package cache)
- `boot/` (kernel, initramfs, modloop, syslinux, grub configs)
- `efi/`
- Size on media: 351.3 MiB

Alpine live features relevant to bootstrap:
- Boots to a functional shell with root.
- Supports `apkovl` overlays for persistence/customization (can be placed on USB or separate media).
- Can run local scripts from `/etc/local.d/`.
- User can mount the original USB device from the live session for additional data.
- Can install additional packages with `apk`.

## Payload Size Analysis (mechanical, via Python + du)

Core awareness-agent components needed for a functional bootstrap:
- `aether` (the 11k POSIX sh script) — the heart of the system
- `bin/aether` (symlink)
- `scripts/emit_aether_snippet.py` + `scripts/setup.py`
- Top-level docs: `CORE_PRINCIPLES.md`, `AGENTS.md`, `SPEC-v0.1.md`, `README.md`, `ARCHITECTURE.md`
- `docs/` (getting-started + the nixos-transition we added)
- `flake.nix` + `shell.nix` (for users who later want Nix)
- Optional: the meta-agent skill files if we want full ICM on the target

Total size of minimal essential payload: **well under 200 KiB** (aether + scripts + key md files are tiny). Even the entire relevant non-dev/ tree is a few hundred KiB.

The 2GB USB has massive headroom. The limiting factor is not space but how to expose the payload on a mostly read-only live ISO + preserve bootability.

## Requirements (from user query + Layer 0/1 + previous context)

User exact request (Layer 4): "/meta-agent Let's use my plugged in 2GB USB as an installer - I want to boostrap Grok IDE with awareness-agent repo please!"

Combined with prior turns:
- Previous desire to move away from Alpine-centric development toward NixOS.
- But the physical USB the user plugged in is an **Alpine live USB**.
- Goal: the resulting USB, when used as installer/boot media, results in a system/environment where:
  - Grok (the Build TUI / CLI interaction) is usable.
  - awareness-agent repo is present and ready.
  - `aether` command works.
  - Sidecars (`.context.md`, `.aether/`) can be created and maintained.
  - Low friction for making projects self-aware.

Must obey (Layer 3):
- Filesystem = single source of truth (plain files only).
- Markdown + POSIX sh + optional tiny Python.
- Extremely low overhead, fully `cat`/`grep`/`git diff` inspectable.
- Active observable sidecars.
- No hidden state.

## Constraints

- 2GB total physical size.
- Current media is read-only ISO9660 (modifications require either repartition + new data area, overlay, or re-imaging the whole thing).
- Bootability must be preserved or enhanced (UEFI + BIOS via syslinux/grub already present).
- In this agent sandbox we can see `/dev/sdb` but any write operation is extremely dangerous and must be gated behind review + explicit user "yes".
- No assumption of large downloads during bootstrap (keep payload self-contained where possible).
- "Grok IDE" here interpreted as the full Grok CLI/TUI + awareness sidecar workflow.

## Analysis of Options

**Option 1: Augment the existing Alpine USB (recommended starting point)**
- Add a new partition (e.g. sdb3, ~1.4 GiB vfat or ext4) using the free space.
- Copy the awareness-agent tree (or a tarball of the core) + a `bootstrap-grok.sh` script onto the new partition.
- On boot (Alpine live), the user mounts the new partition (or we auto-detect) and runs the bootstrap script.
- The script:
  - Copies aether to /usr/local/bin or ~/bin
  - Runs the emit snippet into ~/.profile or similar
  - Runs `aether init` on a default projects location or the live root
  - Creates example sidecars
  - Prints "Grok + awareness ready"
- Pros: Preserves the working Alpine live the user already has. Tiny changes. Fully aligned with repo minimalism.
- Cons: Still Alpine base (we can document the Nix path inside the bootstrap for later switch).

**Option 2: Full re-image with custom minimal live**
- Use the existing Alpine bits + custom initramfs or apkovl that bakes in the repo at build time.
- Or generate a very small custom live using the SPEC vision (busybox + entr + aether + python + the repo).
- Pros: Clean "Mechanicall OS live" feel.
- Cons: More complex to build in this environment; larger engineering surface for 2GB USB.

**Option 3: Data-only payload + instructions (least destructive)**
- Do not repartition.
- Create a tarball or directory of the repo on the user's host.
- User manually copies it onto the USB's EFI partition (if space) or uses tools after boot.
- Or document: "boot the USB, then from another machine or after boot use `cp -a` from the host repo".
- Pros: Zero risk to the USB structure.
- Cons: Not automatic "installer" experience.

**Option 4: NixOS-focused on this USB**
- Attempt to put a minimal NixOS netinstall or custom on the 2GB.
- Then layer our flake + repo.
- Reality check: NixOS minimal ISOs are often close to or over 1GB; combined with repo + overhead may be tight or impossible without netboot. Current USB being Alpine makes this a full wipe.
- We can still ship the `flake.nix` and instructions for "once you have Nix, use it".

**Preferred direction from analysis**: Start with Option 1 (augment the live Alpine USB the user already owns). It matches the physical reality, keeps things minimal, and can include a "later switch to NixOS" path. All artifacts remain plain text + sh + py.

## Risks & Safety Requirements

- Catastrophic data loss if we target the wrong block device (sda vs sdb).
- Any preparation script **must**:
  - Hard-require explicit confirmation.
  - Show `lsblk` output with sizes and models.
  - Only proceed if the device exactly matches "1.9G" + "Flash Disk" + usb.
  - Preferably be a reviewed Python behaviour.
- The sandbox has block device access; the generated behaviour must be runnable by the user on their real host.
- Live USBs are often used for rescue — do not brick the user's rescue media without clear "this will destroy current content" messaging.

## Proposed Artifacts for Later Stages (preview for routing)

- A `scripts/prepare-grok-usb.py` (or per-stage) behaviour that safely prepares `/dev/sdb` (or user-specified) by optionally adding a data partition + copying payload + writing a bootstrap script.
- A `bootstrap-grok.sh` that is self-contained and can run on the live Alpine or a fresh install.
- Updated docs (e.g. in the transition guide or new "portable-installer.md").
- A small README or .md on the data partition explaining usage.
- Possibly an apkovl or local.d script for more seamless first-boot experience.

## Alignment with Previous Work

- Respects the NixOS pivot: the USB can contain `flake.nix` + instructions to `nix develop` once the user has Nix on a target system. The immediate media will be Alpine because that's what the physical USB currently carries.
- Uses the existing `aether` script and `emit_aether_snippet.py` as the behaviours.
- Everything will be `cat`-able and sidecar-based.

## Open Questions for User / Next Stage

- Do you want to **preserve** the current Alpine live content or are you OK with a full wipe + re-partition of the 2GB USB?
- Should the bootstrap target the live session itself (temporary) or prepare for installation to disk?
- Prefer pure Alpine + aether, or also bundle steps to install the Nix package manager inside the live session?
- Any specific "Grok IDE" customizations (e.g. aliases, a default project dir with .context.md already initialized)?

This analysis was produced by reading only the declared inputs for the stage (L1 routing CONTEXT, CORE_PRINCIPLES, user query context) plus mechanical device + size facts gathered via terminal and Python list generation. All outputs are in this `output/` directory for human review.

Next gate: Review these files, edit if needed, then instruct to proceed (e.g. "proceed to 02_plan" or "create the prepare script now").
