#!/bin/sh
# Primary dev loop: build + run portable-kingston-vm FROM ARCH (KVM).
# Do not use the physical Kingston stick for flake troubleshooting.
set -euo pipefail
ROOT="$(CDPATH= cd -- "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
export NIX_CONFIG="experimental-features = nix-command flakes
"

if [ ! -e /dev/kvm ]; then
  echo "error: /dev/kvm missing" >&2
  exit 1
fi

# Submodule .git is fine on Arch (points at real gitdir). Flakes work from host.
echo "==> Building NixOS QEMU runner for #portable-kingston-vm"
echo "    host repo share → guest /mnt/host/mechanicall-os"
echo "    (first build can take a long time / several GB)"
echo ""

OUT="${MECHANICALL_VM_OUT:-$ROOT/result-vm}"
nix build \
  "$ROOT#nixosConfigurations.portable-kingston-vm.config.system.build.vm" \
  -o "$OUT"

RUNNER="$(find "$OUT/bin" -type f -name 'run-*' 2>/dev/null | head -1 || true)"
if [ -z "$RUNNER" ] || [ ! -x "$RUNNER" ]; then
  echo "error: no run-* script in $OUT/bin" >&2
  ls -la "$OUT" "$OUT/bin" 2>/dev/null || true
  exit 1
fi

echo ""
echo "==> Starting $RUNNER"
echo "    Login: operator / operator"
echo "    Then:  aether panel --dump"
echo "    Exit:  poweroff  (or close qemu)"
echo ""
exec "$RUNNER" "$@"
