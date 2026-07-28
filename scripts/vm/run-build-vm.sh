#!/bin/sh
# Build and run the ephemeral NixOS VM for portable-kingston-vm (dev).
# Requires: nix, KVM (/dev/kvm), ~several GB free for the build.
set -euo pipefail
ROOT="$(CDPATH= cd -- "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"

if [ ! -e /dev/kvm ]; then
  echo "error: /dev/kvm missing — enable AMD-V/SVM and load kvm_amd" >&2
  exit 1
fi

echo "Building nixosConfigurations.portable-kingston-vm (build-vm)…"
echo "Repo share for guest 9p: $ROOT (baked as /home/anphuni/mechanicall-os in vmVariant — ensure path matches)"
echo ""

# Prefer nixos-rebuild if available; else nix build the vm attribute
if command -v nixos-rebuild >/dev/null 2>&1; then
  nixos-rebuild build-vm --flake "$ROOT#portable-kingston-vm"
  RUNNER=$(find "$ROOT/result/bin" -type f -name 'run-*-vm' 2>/dev/null | head -1)
  if [ -z "${RUNNER:-}" ]; then
    RUNNER=$(ls "$ROOT/result/bin"/run-* 2>/dev/null | head -1 || true)
  fi
else
  nix build "$ROOT#nixosConfigurations.portable-kingston-vm.config.system.build.vm" -o "$ROOT/result-vm"
  RUNNER=$(find "$ROOT/result-vm/bin" -type f 2>/dev/null | head -1)
fi

if [ -z "${RUNNER:-}" ] || [ ! -x "$RUNNER" ]; then
  echo "error: could not find VM runner script under result*/bin" >&2
  echo "try: nixos-rebuild build-vm --flake $ROOT#portable-kingston-vm" >&2
  exit 1
fi

echo "Starting: $RUNNER"
echo "Login: operator / operator"
echo "Shared tree (if 9p ok): /mnt/host/mechanicall-os"
echo ""
exec "$RUNNER" "$@"
