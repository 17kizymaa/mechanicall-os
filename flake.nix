{
  description = "awareness-agent — Mechanicall OS dev shell (NixOS-first)";

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
      devShells = forAll (pkgs: {
        default = pkgs.mkShell {
          packages = with pkgs; [
            entr
            python3
            # git is typically already available in a dev context
          ];

          shellHook = ''
            echo "awareness-agent (Mechanicall OS) — Nix dev shell active"
            echo "Tools: entr (for aether watch), python3 (optional distill)"
            echo ""
            echo "Quick start in any project:"
            echo "  ./aether init"
            echo "  ./aether watch"
            echo ""
            echo "Or from this checkout (no PATH change needed for python path):"
            echo "  PYTHONPATH=. python3 -m aether status"
          '';
        };
      });
    };
}
