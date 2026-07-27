# First-boot: create personal-llm-full:v1 from on-root seed if missing.
# No vault unlock required for chat after seed files are on the root FS.
{ lib, pkgs, config, ... }:
{
  options.mechanicall.personal-llm-seed = {
    enable = lib.mkEnableOption "auto-seed personal-llm ollama model" // { default = true; };
    seedDir = lib.mkOption {
      type = lib.types.str;
      default = "/var/lib/ollama-seed/personal-llm-full-v1";
    };
    model = lib.mkOption {
      type = lib.types.str;
      default = "personal-llm-full:v1";
    };
  };

  config = lib.mkIf config.mechanicall.personal-llm-seed.enable {
    systemd.services.personal-llm-seed = {
      description = "Create personal-llm Ollama model from local GGUF seed";
      after = [ "network-online.target" "ollama.service" ];
      wants = [ "network-online.target" ];
      requires = [ "ollama.service" ];
      wantedBy = [ "multi-user.target" ];
      serviceConfig = {
        Type = "oneshot";
        RemainAfterExit = true;
        # Match ollama daemon identity when possible
        User = "ollama";
        Group = "ollama";
        Environment = [
          "HOME=/var/lib/ollama"
          "OLLAMA_HOST=127.0.0.1:11434"
        ];
      };
      path = [ config.services.ollama.package pkgs.coreutils pkgs.gnugrep ];
      script = ''
        set -euo pipefail
        SEED="${config.mechanicall.personal-llm-seed.seedDir}"
        MODEL="${config.mechanicall.personal-llm-seed.model}"
        # wait for daemon
        for i in $(seq 1 60); do
          if ollama list >/dev/null 2>&1; then break; fi
          sleep 2
        done
        if ollama list 2>/dev/null | grep -qF "$MODEL"; then
          echo "model $MODEL already present"
          exit 0
        fi
        if [[ ! -f "$SEED/Modelfile" ]] || [[ ! -f "$SEED/personal-llm-full-Q4_K_M.gguf" ]]; then
          echo "seed files missing under $SEED — skip"
          exit 0
        fi
        echo "creating $MODEL from $SEED ..."
        cd "$SEED"
        ollama create "$MODEL" -f Modelfile
        echo "seed complete"
      '';
    };
  };
}
