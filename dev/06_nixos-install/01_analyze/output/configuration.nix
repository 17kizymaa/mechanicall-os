# configuration.nix
# Prepared for your MacBook (Catalina, rEFInd)
# ~330GB maxed NixOS on sda4 (20GB archived Alpine)
# EFI managed by rEFInd (canTouchEfiVariables = false)
# Headless terminal-only / TTY dev environment (no GUI)

{ config, pkgs, ... }:

{
  imports = [ ];

  boot.loader.systemd-boot.enable = true;
  boot.loader.efi.canTouchEfiVariables = false;
  # rEFInd will discover the NixOS EFI stub or you can add a manual entry
  # pointing to /EFI/systemd/systemd-bootx64.efi or the kernel on this partition.

  networking.hostName = "mbp-nix";
  networking.useDHCP = true;  # Ethernet for fast setup/reinstalls

  time.timeZone = "GMT";

  users.users.awareness = {
    isNormalUser = true;
    extraGroups = [ "wheel" ];
    initialPassword = "change-me";
  };

  # Minimal packages for terminal-only dev + project transfer
  environment.systemPackages = with pkgs; [
    git
    vim
    python3
    curl
    wget
    # For Ethernet fast reinstalls of Grok Build CLI / tools
  ];

  # Headless TTY/console only (no X11/Wayland/GUI)
  # Use TTY or ssh over Ethernet for dev sessions
  # Basic for dev work like the original Alpine env
  programs.bash.shellAliases = {
    ae = "aether";
  };

  # After first boot, run the bootstrap from the USB to set up aether + project
  # See nixos-bootstrap.sh on the USB. Use Ethernet for fast setup.

  system.stateVersion = "24.05";  # or current
}
