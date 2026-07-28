# Portable Kingston host — Phase 2 / primary Mechanicall host
#
# Role (2026-07-27):
#   THIS system boots bare-metal from the Kingston stick and hosts Mechanicall OS.
#   Arch (myarch) is the *virtual* or *mounted* dev environment under this host.
#
# Operator daily: boot stick → vault passphrase → login → aether panel / chat
# Vault: passphrase at boot (or skip) · `vault on|off|status`
# Virt:  libvirt/KVM for Arch guest (see mechanicall.virt-host)
{ config, pkgs, lib, modulesPath, ... }:
{
  imports = [
    ./portable-kingston-hardware.nix
    ../modules/ollama-personal.nix
    ../modules/personal-llm-seed.nix
    ../modules/vault-prompt.nix
    ../modules/aether.nix
    ../modules/virt-host.nix
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
  mechanicall.virt-host.enable = true;

  users.users.operator = {
    isNormalUser = true;
    extraGroups = [ "wheel" "networkmanager" "video" "kvm" "libvirtd" ];
    # First-boot default only; production stick password is operator-documented
    initialPassword = "operator";
  };
  users.users.root.initialPassword = "root";
  security.sudo.wheelNeedsPassword = true;

  systemd.tmpfiles.rules = [
    "d /vault 0755 root root -"
    "d /var/lib/ollama-seed 0755 root root -"
    "d /var/lib/ollama-seed/personal-llm-full-v1 0755 root root -"
    "d /opt/mechanicall-os 0755 root root -"
    "d /mnt/myarch 0755 root root -"
    "d /var/lib/libvirt/images 0755 root root -"
  ];

  environment.systemPackages = with pkgs; [
    vim
    curl
    htop
    pciutils
    usbutils
    git
    python3
    rsync
  ];

  environment.shellAliases = {
    chat = "ollama run personal-llm-full:v1";
    panel = "aether panel";
  };

  environment.etc."mechanicall/README.txt".text = ''
    Mechanicall host — Kingston NixOS (primary)

    Roles:
      NixOS (this stick)  = Mechanicall OS host (aether, CURRENT, panel, ollama)
      Arch (myarch)       = virtual/mounted dev environment under this host

    Boot:  vault passphrase when asked (or skip — chat still works)
    Login: operator  (password: see Phase-2 Nix install docs / your notes)
    Chat:  chat   OR   ollama run personal-llm-full:v1
    Panel: aether panel   OR   panel
    Vault: /vault after unlock · vault on|off|status
    aether: AETHER_HOME=/opt/mechanicall-os

    After first rebuild with virt-host:
      virsh list --all
      Mount Arch FS:  sudo mount /dev/disk/by-label/root /mnt/myarch
      Arch guest VM:  /opt/mechanicall-os/scripts/vm/arch-guest-start.sh

    Apply config updates (needs network first time):
      sudo nixos-rebuild switch --flake /opt/mechanicall-os#portable-kingston
  '';

  system.stateVersion = "24.11";
}
