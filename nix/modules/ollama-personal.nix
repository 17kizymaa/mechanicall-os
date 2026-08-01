# Ollama for personal-llm — inference RUNS ON THIS HOST.
# Default bind 0.0.0.0 so LAN / Tailscale clients can reach this hardware.
# Seed models offline via `ollama create` from GGUF — do not rely on cloud pull.
#
# Local peer REPL (on this machine):
#   aether shell . --provider ollama --model personal-llm-sft-v4
#   /agent peer
#
# Remote peer (other machine → THIS host's model):
#   export AETHER_OLLAMA_HOST=http://<tailscale-ip>:11434
#   aether shell . --provider ollama --model personal-llm-sft-v4
#
# Remote TTY to REPL on this host:
#   ssh user@<tailscale-ip> -t 'cd /path && aether shell . --provider ollama --model personal-llm-sft-v4'
{ lib, pkgs, config, ... }:
{
  options.mechanicall.ollama = {
    enable = lib.mkEnableOption "Ollama for personal-llm on this host" // { default = true; };
    useCuda = lib.mkOption {
      type = lib.types.bool;
      default = true;
      description = "Use pkgs.ollama-cuda when true; else pkgs.ollama (CPU).";
    };
    host = lib.mkOption {
      type = lib.types.str;
      # Not 127.0.0.1 — REPL/model on this hardware must be LAN/Tailscale reachable.
      default = "0.0.0.0";
      description = ''
        Bind address for Ollama on THIS host. Default 0.0.0.0 (LAN + Tailscale).
        Set 127.0.0.1 for loopback-only.
      '';
    };
    port = lib.mkOption {
      type = lib.types.port;
      default = 11434;
    };
    openFirewall = lib.mkOption {
      type = lib.types.bool;
      default = true;
      description = "Open TCP port when binding beyond loopback.";
    };
  };

  config = lib.mkIf config.mechanicall.ollama.enable {
    services.ollama = {
      enable = true;
      host = config.mechanicall.ollama.host;
      port = config.mechanicall.ollama.port;
      package =
        if config.mechanicall.ollama.useCuda
        then (pkgs.ollama-cuda or pkgs.ollama)
        else pkgs.ollama;
    };

    networking.firewall.allowedTCPPorts = lib.mkIf (
      config.mechanicall.ollama.openFirewall
      && config.mechanicall.ollama.host != "127.0.0.1"
    ) [ config.mechanicall.ollama.port ];

    environment.systemPackages = [
      config.services.ollama.package
    ];

    # Local aether peer always talks to THIS host's loopback (same machine as serve).
    environment.sessionVariables = {
      AETHER_OLLAMA_HOST = "http://127.0.0.1:${toString config.mechanicall.ollama.port}";
      AETHER_OLLAMA_MODEL = "personal-llm-sft-v4";
    };
  };
}
