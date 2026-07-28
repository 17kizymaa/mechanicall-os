#!/bin/sh
# Create a thin qcow2 disk for a *persistent* portable-kingston-vm install.
# Does not install NixOS by itself — use nixos-install / PHASE-2 host-build pattern next.
set -euo pipefail
SIZE="${1:-40G}"
DIR="${MECHANICALL_VM_DIR:-$HOME/vms}"
IMG="$DIR/portable-kingston.qcow2"

mkdir -p "$DIR"
if [ -f "$IMG" ]; then
  echo "exists: $IMG"
  qemu-img info "$IMG"
  exit 0
fi

if ! command -v qemu-img >/dev/null 2>&1; then
  echo "error: qemu-img not found (pacman -S qemu-img or qemu-base)" >&2
  exit 1
fi

qemu-img create -f qcow2 "$IMG" "$SIZE"
echo "created $IMG ($SIZE)"
qemu-img info "$IMG"
echo ""
echo "Next: install NixOS into this disk (UEFI), then apply flake #portable-kingston-vm"
echo "Or use scripts/vm/run-build-vm.sh for an ephemeral test without this qcow."
