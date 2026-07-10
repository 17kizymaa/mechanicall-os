#!/usr/bin/env python3
"""
Python behaviour for 01_analyze: Disk layout facts and proposed partition plan.
Loads only from declared inputs (user query + CORE_PRINCIPLES + L1).
Produces concrete, verifiable commands and warnings.
Run with python3 this file to emit the plan.
"""

import subprocess
import sys

print("=== ICM 01_analyze: Disk Reality for NixOS 300GB Partition ===")
print("User request: Install NixOS as new 300GB partition overwriting ~300GB of 'empty Alpine OS space' on the device.")
print("Using current Alpine session as 'mounting bridge' where safe.")

def run(cmd):
    print(f"\n$ {cmd}")
    try:
        out = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, text=True)
        print(out.strip())
    except subprocess.CalledProcessError as e:
        print(e.output.strip())
        print(f"(exit {e.returncode})")

print("\n--- Current layout (verified) ---")
run("lsblk -o NAME,SIZE,TYPE,FSTYPE,MOUNTPOINT,LABEL /dev/sda")
run("parted -l /dev/sda")

print("\n--- Key facts ---")
print("sda1: 200MB EFI (vfat, mounted /boot) - KEEP")
print("sda2: 150GB APFS 'Macintosh HD' - APPLE FILESYSTEM. Likely macOS data or container. HIGH RISK to touch.")
print("sda3: 350GB ext4 'alpine-root' mounted as / . Only ~4GB used. This is the 'Alpine OS space'.")
print("Current / uses ~4GB of the 350GB allocation. ~346GB 'empty' inside FS but partition boundary is at end of disk.")

print("\n--- Constraints & Risks (per CORE_PRINCIPLES: inspectability, no hidden state) ---")
print("1. Running system is on sda3. Any change to sda3 partition table or aggressive shrink while mounted = immediate breakage of this session.")
print("2. No large unallocated space on disk (GPT fully allocated to 1+2+3).")
print("3. To free 300GB for new partition: MUST shrink sda3 filesystem + partition.")
print("   - Resize ext4 on sda3 to e.g. 50GB (leaves ~4GB used + headroom).")
print("   - Resize the sda3 partition to 50GB.")
print("   - Create new sda4 ~300GB in the freed space.")
print("4. Shrinking mounted root ext4 is NOT possible. Requires unmount or live boot.")
print("5. APFS (sda2) resize/delete risks destroying macOS if present on this MacBook Pro hardware.")
print("6. Nix not installed in current env. NixOS install will require nix + nixos-install after partitioning and mounting target.")

print("\n--- Proposed safe sequence (for review) ---")
print("This session (Alpine on sda3) can act as 'mounting bridge':")
print("  - Install nix (single-user)")
print("  - Prepare NixOS configuration.nix targeting future /dev/sda4")
print("  - But PARTITION CHANGES must be done from external live media (Alpine live USB or NixOS ISO).")
print("  - After creating partitions from live:")
print("    mount /dev/sda4 /mnt")
print("    nixos-generate-config --root /mnt")
print("    edit config, nixos-install --root /mnt")
print("    Then set up bootloader for dual-boot with existing EFI.")

print("\n--- Exact commands to consider (DANGEROUS - review before any run) ---")
print("From LIVE MEDIA ONLY (not this session):")
print("parted /dev/sda resizepart 3 50GB   # after shrinking FS")
print("parted /dev/sda mkpart primary ext4 50GB 350GB   # ~300GB")
print("mkfs.ext4 -L nixos /dev/sda4")

print("\n--- Recommended first non-destructive actions in current session (bridge) ---")
print("1. Install nix: curl -L https://nixos.org/nix/install | sh")
print("2. Source nix profile")
print("3. Generate a starter configuration for the future NixOS (manual since no target yet)")

print("\n--- Output for next stage ---")
print("See analysis.md and summary.md for full reviewable artifact.")
print("Do NOT run partition commands from this running Alpine root.")

if __name__ == "__main__":
    print("\n[Script complete - facts gathered, plan proposed. Human review required.]")
