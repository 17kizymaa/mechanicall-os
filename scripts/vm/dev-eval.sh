#!/bin/sh
# Fast check: does the VM system evaluate? (no full image build)
set -euo pipefail
ROOT="$(CDPATH= cd -- "$(dirname "$0")/../.." && pwd)"
export NIX_CONFIG="experimental-features = nix-command flakes
"
echo "eval #portable-kingston-vm hostName:"
nix eval --raw "$ROOT#nixosConfigurations.portable-kingston-vm.config.networking.hostName"
echo ""
echo "eval system.build.vm type:"
nix eval --raw "$ROOT#nixosConfigurations.portable-kingston-vm.config.system.build.vm" >/dev/null
echo "OK — VM config evaluates. Run: sh scripts/vm/dev-up.sh"
