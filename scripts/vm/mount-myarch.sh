#!/bin/sh
# Mount the internal Arch root (myarch) for file-level integrated dev
# without starting a full VM. Run on Kingston NixOS host.
set -euo pipefail
MNT="${1:-/mnt/myarch}"
# Arch root was labeled "root" on the internal disk during prior probes
DEV="${MYARCH_ROOT_DEV:-/dev/disk/by-label/root}"

if [ ! -b "$DEV" ] && [ ! -e "$DEV" ]; then
  echo "error: device not found: $DEV" >&2
  echo "lsblk and set MYARCH_ROOT_DEV=" >&2
  lsblk -o NAME,SIZE,LABEL,FSTYPE,MOUNTPOINT
  exit 1
fi

sudo mkdir -p "$MNT"
if mountpoint -q "$MNT"; then
  echo "already mounted: $MNT"
  findmnt "$MNT"
  exit 0
fi

sudo mount -o rw "$DEV" "$MNT"
echo "mounted $DEV → $MNT"
echo "home: $MNT/home/anphuni"
echo "unmount: sudo umount $MNT"
