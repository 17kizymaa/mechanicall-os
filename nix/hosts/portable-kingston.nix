# Portable Kingston host — Phase 2 lean image + seat workstation foundation
# Already built Track B stick (ESP + nixos + LUKS vault). No reinstall for seats.
# Operator daily: EFI boot → login → seat-menu → aether panel|shell
# Vault: `vault on` (passphrase once) — no keyfile paths
{ config, pkgs, lib, modulesPath, ... }:
{
  imports = [
    ./portable-kingston-hardware.nix
    ../modules/ollama-personal.nix
    ../modules/personal-llm-seed.nix
    ../modules/vault-prompt.nix
    ../modules/aether.nix
    ../modules/seat-workstation.nix
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

  # Seat foundation on (enable + PEER model contract). Autologin stays off.
  mechanicall.seat.enable = true;
  mechanicall.seat.autologin = false;
  mechanicall.seat.peerModel = "personal-llm-sft-v4";

  # Fast path after seed service: chat seed (not PEER skill — PEER = sft-v4 only)
  environment.shellAliases = {
    chat = "ollama run personal-llm-full:v1";
  };

  environment.etc."mechanicall/README.txt".text = ''
    Portable host — Kingston path (already built) + seat foundation
    Boot:  Firmware EFI (GOP/UGA) → systemd-boot → NixOS → login
    Seat:  seat-menu   OR   seat   OR   aether panel / aether shell
    Chat:  chat   OR   ollama run personal-llm-full:v1
    PEER:  personal-llm-sft-v4 only (PEER profile/skill — Domain contract)
    Vault: /vault after unlock · vault on|off|status if needed
    aether: AETHER_HOME=/opt/mechanicall-os
    Docs:  /opt/mechanicall-os/docs/SEAT-NIXOS-EFI-FOUNDATION.md
    Rebuild on stick: bash /opt/mechanicall-os/scripts/rebuild-portable-kingston.sh
  '';

  system.stateVersion = "24.11";
}
