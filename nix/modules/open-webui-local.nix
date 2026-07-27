# Open WebUI bound to localhost only — browser UI over local Ollama.
{ lib, pkgs, config, ... }:
{
  options.mechanicall.open-webui = {
    enable = lib.mkEnableOption "local Open WebUI" // { default = true; };
    port = lib.mkOption {
      type = lib.types.port;
      default = 8080;
    };
  };

  config = lib.mkIf config.mechanicall.open-webui.enable {
    services.open-webui = {
      enable = true;
      host = "127.0.0.1";
      port = config.mechanicall.open-webui.port;
      environment = {
        # Prefer local Ollama; never expose as multi-tenant SaaS.
        OLLAMA_BASE_URL = "http://127.0.0.1:11434";
        # Reduce outbound surprise; package versions differ on exact keys.
        WEBUI_AUTH = "False"; # single-operator portable stick v1
      };
    };
  };
}
