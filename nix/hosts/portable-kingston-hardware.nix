# Generated-style hardware config for Kingston Track B layout (2026-07-24).
# Device nodes (/dev/sdc*) may change — prefer UUID mounts.
# Import from portable-kingston.nix after install merge.
{ config, lib, pkgs, modulesPath, ... }:
{
  imports = [ (modulesPath + "/installer/scan/not-detected.nix") ];

  boot.initrd.availableKernelModules = [ "xhci_pci" "ahci" "usb_storage" "sd_mod" "uas" ];
  boot.initrd.kernelModules = [ ];
  boot.kernelModules = [ "kvm-intel" ];
  boot.extraModulePackages = [ ];

  # Root + ESP (always present for boot)
  fileSystems."/" = {
    device = "/dev/disk/by-label/nixos";
    fsType = "ext4";
  };

  fileSystems."/boot" = {
    device = "/dev/disk/by-label/ESP";
    fsType = "vfat";
    options = [ "fmask=0077" "dmask=0077" ];
  };

  # Vault is NOT auto-mounted. Open with /etc/mechanicall/unlock-vault.sh
  # LUKS UUID (partition): af6be1c7-27b3-42f8-91ca-fa3b07c3e98e
  # Mapper label after format: ARCHIVES

  swapDevices = [ ];

  networking.useDHCP = lib.mkDefault true;
  nixpkgs.hostPlatform = lib.mkDefault "x86_64-linux";
}
