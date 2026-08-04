# Fallback for classic `nix-shell` (no flakes required)
{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.entr
    pkgs.python3
  ];

  shellHook = ''
    echo "mechanicall-os dev shell (via shell.nix)"
  '';
}
