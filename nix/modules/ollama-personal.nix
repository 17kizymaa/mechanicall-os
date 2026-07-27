# Local-only Ollama for portable personal-llm host.
# Seed models offline via `ollama create` from GGUF — do not rely on cloud pull.
{ lib, pkgs, config, ... }:
{
  options.mechanicall.ollama = {
    enable = lib.mkEnableOption "local Ollama for personal-llm" // { default = true; };
    # Prefer ollama-cuda when available; fall back to pkgs.ollama.
    useCuda = lib.mkOption {
      type = lib.types.bool;
      default = true;
      description = "Use pkgs.ollama-cuda when true; else pkgs.ollama (CPU).";
    };
  };

  config = lib.mkIf config.mechanicall.ollama.enable {
    services.ollama = {
      enable = true;
      host = "127.0.0.1";
      port = 11434;
      package =
        if config.mechanicall.ollama.useCuda
        then (pkgs.ollama-cuda or pkgs.ollama)
        else pkgs.ollama;
    };

    environment.systemPackages = [
      config.services.ollama.package
    ];
  };
}
