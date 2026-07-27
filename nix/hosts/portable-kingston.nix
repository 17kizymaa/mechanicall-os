# Portable Kingston host — Phase 2 lean image
# Operator daily: boot → login → ollama run personal-llm-full:v1
# Vault: `vault on` (passphrase once) — no keyfile paths
{ config, pkgs, lib, modulesPath, ... }:
{
  imports = [
    ./portable-kingston-hardware.nix
    ../modules/ollama-personal.nix
    ../modules/personal-llm-seed.nix
    ../modules/vault-prompt.nix
    ../modules/aether.nix
  ];

  networking.hostName = "mechanicall-portable";
  networking.networkmanager.enable = true;
  networking.firewall.enable = true;
  networking.firewall.allowedTCPPorts = [ ];

  time.timeZone = "Europe/London";

  boot.loader.systemd-boot.enable = true;
  boot.loader.efi.canTouchEfiVariables = false;
  boot.loader.efi.efiSysMountPoint = "/boot";

  mechanicall.ollama.useCuda = false;
  mechanicall.personal-llm-seed.enable = true;
  mechanicall.vault.enable = true;

  users.users.operator = {
    isNormalUser = true;
    extraGroups = [ "wheel" "networkmanager" "video" ];
    # password already set by operator on first boot; keep initial for reinstall only
    initialPassword = "operator";
  };
  users.users.root.initialPassword = "root";
  security.sudo.wheelNeedsPassword = true;

  systemd.tmpfiles.rules = [
    "d /vault 0755 root root -"
    "d /var/lib/ollama-seed 0755 root root -"
    "d /var/lib/ollama-seed/personal-llm-full-v1 0755 root root -"
    "d /opt/mechanicall-os 0755 root root -"
  ];

  environment.systemPackages = with pkgs; [
    vim
    curl
    htop
    pciutils
    usbutils
  ];

  # Fast path after seed service: just chat
  environment.shellAliases = {
    chat = "ollama run personal-llm-full:v1";
  };

  environment.etc."mechanicall/README.txt".text = ''
    Portable host — Phase 2
    Boot:  enter vault passphrase when asked (or skip; chat still works)
    Chat:  chat   OR   ollama run personal-llm-full:v1
    Vault: /vault after unlock · vault on|off|status if needed
    aether: AETHER_HOME=/opt/mechanicall-os
  '';

  system.stateVersion = "24.11";
}
