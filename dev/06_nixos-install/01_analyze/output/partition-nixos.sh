#!/bin/sh
# partition-nixos.sh
# Generated E2E for user's Mac (Catalina + rEFInd)
# sda2 = MacOS (DO NOT TOUCH)
# Shrink sda3 (Alpine archive) to 20GB (max out for NixOS)
# New sda4 = ~330GB for NixOS (maxed remaining space after MacOS + minimal archive)

set -e

echo "=== GHOST-USER VERIFIED PARTITION FOR NIXOS ==="
echo "This will shrink Alpine (sda3) to 20GB archive and create maxed ~330GB NixOS partition."
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

echo "Resizing sda3 to end at 170GB (20GB for archived Alpine - maxed cut)..."
parted /dev/sda --script resizepart 3 170GB

echo "Creating new maxed ~330GB partition sda4 for NixOS..."
parted /dev/sda --script mkpart primary ext4 170GB 100%
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
