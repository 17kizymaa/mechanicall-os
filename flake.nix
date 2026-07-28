{
  description = "Mechanicall OS — aether control plane + portable personal-llm host";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }:
    let
      systems = [ "x86_64-linux" "aarch64-linux" ];
      forAll = f: nixpkgs.lib.genAttrs systems (system:
        f nixpkgs.legacyPackages.${system}
      );

      # Shared system configs so aliases are identical
      portableKingston = nixpkgs.lib.nixosSystem {
        system = "x86_64-linux";
        modules = [
          ./nix/hosts/portable-kingston.nix
        ];
      };

      portableKingstonVm = nixpkgs.lib.nixosSystem {
        system = "x86_64-linux";
        modules = [
          ./nix/hosts/portable-kingston-vm.nix
        ];
      };
    in {
      # Rebuild on stick (prefer explicit attr; bare flake path uses hostName):
      #   sudo nixos-rebuild switch --flake /opt/mechanicall-os#portable-kingston
      #   sudo nixos-rebuild switch --flake /opt/mechanicall-os#mechanicall-portable
      #   sudo /opt/mechanicall-os/scripts/rebuild-portable-kingston.sh
      nixosConfigurations = {
        portable-kingston = portableKingston;
        # Must match networking.hostName — else bare --flake /path looks up
        # packages.x86_64-linux.mechanicall-portable and fails.
        mechanicall-portable = portableKingston;

        portable-kingston-vm = portableKingstonVm;
        mechanicall-portable-vm = portableKingstonVm;
      };

      packages = forAll (pkgs: rec {
        aether = pkgs.writeShellScriptBin "aether" ''
          set -euo pipefail
          ROOT="''${AETHER_HOME:-${self}}"
          exec "$ROOT/aether" "$@"
        '';
        default = aether;
      });

      devShells = forAll (pkgs: {
        default = pkgs.mkShell {
          packages = with pkgs; [
            entr
            python3
          ];

          shellHook = ''
            echo "Mechanicall OS — Nix dev shell active"
            echo "Portable host: #portable-kingston (alias #mechanicall-portable)"
            echo "Dev VM:        #portable-kingston-vm"
            echo "  ./aether init && ./aether panel"
          '';
        };
      });
    };
}
