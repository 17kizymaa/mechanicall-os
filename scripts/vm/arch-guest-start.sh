#!/bin/sh
# Start the Arch dev guest under KVM from the Kingston NixOS host.
# Shares host mechanicall-os into the guest at /mnt/host/mechanicall-os (9p).
set -euo pipefail

ROOT="${AETHER_HOME:-/opt/mechanicall-os}"
if [ -d /mnt/myarch/home/anphuni/vms ]; then
  DEFAULT_IMG="/mnt/myarch/home/anphuni/vms/myarch-dev.qcow2"
elif [ -d /home/anphuni/vms ]; then
  DEFAULT_IMG="/home/anphuni/vms/myarch-dev.qcow2"
else
  DEFAULT_IMG="/var/lib/libvirt/images/myarch-dev.qcow2"
fi
IMG="${MECHANICALL_ARCH_QCOW:-$DEFAULT_IMG}"
MEM="${MECHANICALL_ARCH_MEM:-8192}"
CPUS="${MECHANICALL_ARCH_CPUS:-4}"
SHARE="${MECHANICALL_SHARE:-$ROOT}"

if [ ! -f "$IMG" ]; then
  echo "error: disk missing: $IMG" >&2
  echo "run: scripts/vm/arch-guest-create.sh" >&2
  exit 1
fi
if [ ! -e /dev/kvm ]; then
  echo "error: /dev/kvm missing" >&2
  exit 1
fi
if ! command -v qemu-system-x86_64 >/dev/null 2>&1; then
  echo "error: qemu-system-x86_64 missing — nixos-rebuild with virt-host" >&2
  exit 1
fi

echo "Arch guest disk: $IMG"
echo "Share (9p tag mechanicall): $SHARE"
echo "RAM=${MEM}M CPUs=$CPUS"
echo "Login depends on what you installed into the qcow."
echo ""

# UEFI if OVMF present
OVMF_CODE=""
for c in \
  /run/libvirt/nix-ovmf/OVMF_CODE.fd \
  /run/libvirt/nix-ovmf/FV/OVMF_CODE.fd \
  /usr/share/edk2/x64/OVMF_CODE.fd \
  /usr/share/OVMF/OVMF_CODE.fd
do
  if [ -f "$c" ]; then OVMF_CODE="$c"; break; fi
done

set -- \
  -enable-kvm \
  -machine q35,accel=kvm \
  -cpu host \
  -smp "$CPUS" \
  -m "$MEM" \
  -drive "file=$IMG,if=virtio,format=qcow2,cache=writeback" \
  -netdev user,id=net0,hostfwd=tcp::2222-:22 \
  -device virtio-net-pci,netdev=net0 \
  -fsdev "local,id=fs0,path=$SHARE,security_model=none" \
  -device virtio-9p-pci,fsdev=fs0,mount_tag=mechanicall \
  -nographic

if [ -n "$OVMF_CODE" ]; then
  set -- "$@" -drive "if=pflash,format=raw,readonly=on,file=$OVMF_CODE"
fi

exec qemu-system-x86_64 "$@"
