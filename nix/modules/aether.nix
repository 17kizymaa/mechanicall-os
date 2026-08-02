# Ship aether CLI + env defaults for personal-llm. Model never gains approve.
{ lib, pkgs, config, ... }:
let
  aetherPkg = pkgs.writeShellScriptBin "aether" ''
    set -euo pipefail
    export AETHER_HOME="''${AETHER_HOME:-/opt/mechanicall-os}"
    exec "$AETHER_HOME/aether" "$@"
  '';
in
{
  options.mechanicall.aether = {
    enable = lib.mkEnableOption "aether CLI wrapper" // { default = true; };
    home = lib.mkOption {
      type = lib.types.str;
      default = "/opt/mechanicall-os";
      description = "Checkout or installed tree containing ./aether";
    };
    defaultOllamaModel = lib.mkOption {
      type = lib.types.str;
      default = "personal-llm-full:v1";
    };
  };

  config = lib.mkIf config.mechanicall.aether.enable {
    environment.systemPackages = [ aetherPkg pkgs.git pkgs.jq pkgs.cryptsetup ];

    environment.variables = {
      AETHER_HOME = config.mechanicall.aether.home;
      AETHER_LLM_PROVIDER = "ollama";
      AETHER_OLLAMA_MODEL = config.mechanicall.aether.defaultOllamaModel;
      AETHER_OLLAMA_HOST = "http://127.0.0.1:11434";
    };

    # Prefer: vault on  (see vault-prompt.nix)
    environment.etc."mechanicall/README-vault.txt".text = ''
      Vault: vault on | vault off | vault status
      Chat:  ollama run personal-llm-full:v1  (or: chat)
      Seat:  seat-menu | aether panel | aether shell
      aether approve is human-only. PEER profile = personal-llm-sft-v4 only.
    '';
  };
}
