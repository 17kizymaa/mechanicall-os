#!/usr/bin/env python3
"""
E2E Transfer Generator for awareness-agent project to future NixOS environment.

This Python behaviour (per meta-agent) generates all files needed to:
- Partition using recommended numbers (sda3 shrink to 50GB, sda4 300GB NixOS).
- Install NixOS with rEFInd compatible setup.
- Transfer the full project (awareness-agent, aether, meta-agent skill) to the new NixOS.
- Bootstrap sidecars, aether, and dev environment on first NixOS boot.

Run this to populate the USB (mounted at /mnt/usb) and stage output.

User clarifications applied:
- sdb = USB (transfer medium)
- sda2 = MacOS (Catalina, do not touch)
- sda3 = Alpine (archive/shrink)
- Use rEFInd for booting the new NixOS
- Exact numbers: sda3 to 200GB end, sda4 300GB
"""

import os
import subprocess

USB_MOUNT = "/mnt/usb"
STAGE_OUT = "dev/06_nixos-install/01_analyze/output"  # or 03 later
TARGET_DIR = os.path.join(USB_MOUNT, "nixos-transfer")

def sh(cmd):
    print(f"[GEN] {cmd}")
    subprocess.check_call(cmd, shell=True)

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)
    os.chmod(path, 0o755 if path.endswith('.sh') else 0o644)
    print(f"[GEN] wrote {path}")

def main():
    print("=== E2E NixOS Transfer Generator ===")
    print("Populating USB and stage with partition script, NixOS config, and bootstrap for awareness-agent project.")

    # Ensure dirs
    sh(f"mkdir -p {TARGET_DIR}")

    # 1. Partition script with ghost verification and exact numbers
    partition_sh = '''#!/bin/sh
# partition-nixos.sh
# Generated E2E for user's Mac (Catalina + rEFInd)
# sda2 = MacOS (DO NOT TOUCH)
# Shrink sda3 (Alpine archive) to 50GB
# New sda4 = 300GB for NixOS

set -e

echo "=== GHOST-USER VERIFIED PARTITION FOR NIXOS ==="
echo "This will shrink Alpine (sda3) and create 300GB NixOS partition."
echo "sda2 must remain MacOS APFS."

lsblk -o NAME,SIZE,TYPE,FSTYPE,LABEL /dev/sda
blkid /dev/sda2

echo "Confirm sda2 is your MacOS (Catalina). Type YES to proceed:"
read confirm
if [ "$confirm" != "YES" ]; then
  echo "Aborted."
  exit 1
fi

echo "Current layout:"
parted /dev/sda print

echo "Resizing sda3 to end at 200GB (50GB for archived Alpine)..."
parted /dev/sda --script resizepart 3 200GB

echo "Creating new 300GB partition sda4 for NixOS..."
parted /dev/sda --script mkpart primary ext4 200GB 500GB
parted /dev/sda --script name 4 nixos
parted /dev/sda --script set 4 boot on || true

echo "Final layout:"
parted /dev/sda print

echo "Formatting NixOS partition..."
mkfs.ext4 -L nixos /dev/sda4

echo "=== Partitioning complete ==="
echo "Next: Boot live media if needed, then:"
echo "  mount /dev/sda4 /mnt"
echo "  mount /dev/sda1 /mnt/boot   # if using the EFI"
echo "  Then run nixos-install with the prepared config."
echo "The USB has the full awareness-agent project ready to transfer."
'''

    write_file(os.path.join(TARGET_DIR, "partition-nixos.sh"), partition_sh)
    write_file(os.path.join(STAGE_OUT, "partition-nixos.sh"), partition_sh)

    # 2. NixOS configuration.nix (rEFInd friendly, minimal + awareness prep)
    config_nix = '''# configuration.nix
# Prepared for your MacBook (Catalina, rEFInd)
# 300GB NixOS on sda4
# EFI managed by rEFInd (canTouchEfiVariables = false)

{ config, pkgs, ... }:

{
  imports = [ ];

  boot.loader.systemd-boot.enable = true;
  boot.loader.efi.canTouchEfiVariables = false;
  # rEFInd will discover the NixOS EFI stub or you can add a manual entry
  # pointing to /EFI/systemd/systemd-bootx64.efi or the kernel on this partition.

  networking.hostName = "nixos-mac";
  networking.useDHCP = false;  # or true for simple

  time.timeZone = "America/Los_Angeles";  # adjust

  users.users.awareness = {
    isNormalUser = true;
    extraGroups = [ "wheel" "networkmanager" ];
    initialPassword = "change-me";
  };

  environment.systemPackages = with pkgs; [
    git
    vim
    python3
    curl
    wget
    # entr can be added via nixpkgs or built
  ];

  # Basic for dev work like the original Alpine env
  programs.bash.shellAliases = {
    ae = "aether";
  };

  # After first boot, run the bootstrap from the USB to set up aether + project
  # See nixos-bootstrap.sh on the USB.

  system.stateVersion = "24.05";  # or current
}
'''

    write_file(os.path.join(TARGET_DIR, "configuration.nix"), config_nix)
    write_file(os.path.join(STAGE_OUT, "configuration.nix"), config_nix)

    # 3. Post NixOS bootstrap script (transfers the project, sets up aether and sidecars)
    bootstrap_sh = '''#!/bin/sh
# nixos-bootstrap.sh
# Run this on first boot of the new NixOS (as root or with sudo)
# It transfers "this project" (awareness-agent) from the USB and bootstraps
# the full environment (aether, meta-agent, sidecars) E2E.

set -e

USB_MOUNT="/media/usb"   # adjust if different, e.g. /mnt/usb when mounted
REPO_SRC="$USB_MOUNT/awareness-agent"
TARGET_REPO="/opt/awareness-agent"

echo "=== Transferring awareness-agent project to new NixOS environment ==="

if [ ! -d "$REPO_SRC" ]; then
  echo "USB not mounted or awareness-agent not found at $REPO_SRC"
  echo "Mount your USB (the sdb one with GROK-PORTABLE-DE) and rerun."
  exit 1
fi

mkdir -p /opt
cp -a "$REPO_SRC" "$TARGET_REPO"
echo "Repo copied to $TARGET_REPO"

# Install aether globally
cp "$TARGET_REPO/aether" /usr/local/bin/aether
chmod +x /usr/local/bin/aether
echo "aether installed to /usr/local/bin"

# Shell integration (for the awareness user)
USER_HOME="/home/awareness"
mkdir -p "$USER_HOME"
python3 "$TARGET_REPO/scripts/emit_aether_snippet.py" >> "$USER_HOME/.bashrc" || true
echo 'export PATH="/usr/local/bin:$PATH"' >> "$USER_HOME/.bashrc" || true

# Initialize the project sidecars (E2E transfer)
cd "$TARGET_REPO"
./aether init || true
./aether distill || true

# Example project to make "alive" immediately
mkdir -p /home/awareness/projects/example
cd /home/awareness/projects/example
"$TARGET_REPO/aether" init || true
echo "# New NixOS project" > README.md
"$TARGET_REPO/aether" distill || true

echo ""
echo "=== E2E Complete ==="
echo "awareness-agent is now in $TARGET_REPO"
echo "Run: aether status"
echo "Edit .context.md files. The meta-agent skill is at $TARGET_REPO/.grok/skills/meta-agent/"
echo "Your Grok sessions on this new NixOS will have full filesystem awareness."
echo ""
echo "To continue development: cd $TARGET_REPO && source the shell integration."
echo "rEFInd should detect the NixOS install. Add manual entry if needed for /dev/sda4."
'''

    write_file(os.path.join(TARGET_DIR, "nixos-bootstrap.sh"), bootstrap_sh)
    write_file(os.path.join(STAGE_OUT, "nixos-bootstrap.sh"), bootstrap_sh)

    # 4. Updated README on USB for this transfer
    readme = '''NIXOS TRANSFER - awareness-agent Project (E2E)

This USB (sdb, GROK-PORTABLE-DE) now carries the complete setup to move the project
from the current Alpine to your new NixOS 300GB partition.

User setup:
- sda2: MacOS Catalina (do not touch)
- sda3: Alpine (archiving / shrinking to 50GB)
- New sda4: 300GB NixOS
- Boot: rEFInd (already installed)

Files in nixos-transfer/ on this USB:
- partition-nixos.sh : Exact commands with verification (run from live media or current before archiving)
- configuration.nix : Ready-to-use NixOS config (rEFInd friendly)
- nixos-bootstrap.sh : Post-install script to transfer the awareness-agent project, install aether, init sidecars, and make the environment "alive" E2E.

Recommended exact partition numbers (as analyzed and accepted):
- sda3 resized to 200GB end (50GB for archived Alpine)
- sda4 from 200GB to 500GB (300GB, ext4, label nixos)

Steps for E2E:
1. (From live or current Alpine with care) Run partition-nixos.sh on the USB.
2. Boot NixOS installer (or use the prepared config if doing from bridge).
3. During/after install, use the generated configuration.nix .
4. On first NixOS boot (via rEFInd):
   - Mount this USB.
   - Run the nixos-bootstrap.sh from the USB.
5. aether will be available, sidecars initialized, meta-agent skill present.
6. The project (awareness-agent) is now in the new environment.

All state is in the filesystem. cat .context.md to see.

Generated in ghost-user verified mode using ICM.
'''

    # Append/update on USB root
    with open(os.path.join(USB_MOUNT, "README-NIXOS-TRANSFER.txt"), "w") as f:
        f.write(readme)

    print("\n=== E2E files generated and placed on USB and in stage output ===")
    print("Mount point:", USB_MOUNT)
    print("nixos-transfer/ contents will include the three key scripts + existing awareness-agent/.")
    sh(f"ls -l {TARGET_DIR}/")
    sh(f"ls -l {USB_MOUNT}/ | head -10")

if __name__ == "__main__":
    main()
