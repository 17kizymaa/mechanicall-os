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
    in {
      # Portable Kingston single-stick host (Track B). Install only after backup.
      #   nixos-install --flake /path/to/mechanicall-os#portable-kingston
      # At install, merge generated hardware-configuration.nix into the host module.
      nixosConfigurations.portable-kingston = nixpkgs.lib.nixosSystem {
        system = "x86_64-linux";
        modules = [
          ./nix/hosts/portable-kingston.nix
        ];
      };

      packages = forAll (pkgs: {
        # Thin wrapper so portable hosts / other flakes can depend on aether path tools.
        aether = pkgs.writeShellScriptBin "aether" ''
          set -euo pipefail
          ROOT="''${AETHER_HOME:-${self}}"
          exec "$ROOT/aether" "$@"
        '';
      });

      devShells = forAll (pkgs: {
        default = pkgs.mkShell {
          packages = with pkgs; [
            entr
            python3
          ];

          shellHook = ''
            echo "Mechanicall OS — Nix dev shell active"
            echo "Tools: entr (for aether watch), python3 (optional distill)"
            echo "Portable host flake: nixosConfigurations.portable-kingston"
            echo ""
            echo "Quick start in any project:"
            echo "  ./aether init"
            echo "  ./aether watch"
            echo ""
            echo "  PYTHONPATH=. python3 -m aether status"
          '';
        };
      });
    };
}
