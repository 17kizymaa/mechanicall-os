#!/bin/sh
# Create a qcow2 for the Arch *dev guest* (myarch virtual environment).
# Run on Kingston NixOS host (or Arch while preparing the image).
#
# Prefer disk space on the internal SATA volume (myarch root), not the 20G stick.
set -euo pipefail

SIZE="${1:-80G}"
# Prefer existing Arch home if mounted; else libvirt images on current root
if [ -d /mnt/myarch/home/anphuni ]; then
  DIR="/mnt/myarch/home/anphuni/vms"
elif [ -d /home/anphuni ]; then
  DIR="/home/anphuni/vms"
else
  DIR="/var/lib/libvirt/images"
fi
IMG="${MECHANICALL_ARCH_QCOW:-$DIR/myarch-dev.qcow2}"

mkdir -p "$(dirname "$IMG")"
if [ -f "$IMG" ]; then
  echo "exists: $IMG"
  qemu-img info "$IMG" 2>/dev/null || true
  exit 0
fi

if ! command -v qemu-img >/dev/null 2>&1; then
  echo "error: qemu-img missing — enable mechanicall.virt-host and nixos-rebuild" >&2
  exit 1
fi

qemu-img create -f qcow2 "$IMG" "$SIZE"
echo "created $IMG ($SIZE)"
echo ""
echo "Install Arch into this disk (UEFI + virtio), or convert a backup later."
echo "Then: MECHANICALL_ARCH_QCOW=$IMG $0  # no-op once exists"
echo "Start: scripts/vm/arch-guest-start.sh"
