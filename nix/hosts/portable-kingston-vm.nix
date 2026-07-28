# Portable host — KVM *dev* guest (run from Arch — do NOT use the physical stick for rebuild debug)
#
# Primary workflow (on Arch):
#   sh scripts/vm/dev-up.sh
# Login: operator / operator
# Shared repo: /mnt/host/mechanicall-os  (9p from host ~/mechanicall-os)
#
# Physical Kingston is deploy-only after the VM proves a generation.
{ config, pkgs, lib, modulesPath, ... }:
{
  imports = [
    ./portable-kingston-vm-hardware.nix
    ../modules/ollama-personal.nix
    ../modules/personal-llm-seed.nix
    ../modules/aether.nix
  ];

  options.mechanicall.vm = {
    enableGuestOllama = lib.mkOption {
      type = lib.types.bool;
      default = false;
      description = "Run Ollama inside the guest (default false — use host Arch Ollama)";
    };
  };

  config = {
    networking.hostName = "mechanicall-portable-vm";
    networking.networkmanager.enable = true;
    networking.firewall.enable = true;

    time.timeZone = "Europe/London";

    # build-vm / qemu-vm supplies its own boot disk; keep systemd-boot for persistent qcow installs
    boot.loader.systemd-boot.enable = true;
    boot.loader.efi.canTouchEfiVariables = true;
    boot.loader.efi.efiSysMountPoint = "/boot";

    services.qemuGuest.enable = true;

    # No LUKS vault, no personal-llm seed by default
    mechanicall.ollama.enable = config.mechanicall.vm.enableGuestOllama;
    mechanicall.ollama.useCuda = false;
    mechanicall.personal-llm-seed.enable = false;

    mechanicall.aether.enable = true;
    # Prefer shared host tree (mounted by vmVariant 9p); fallback /opt
    mechanicall.aether.home = "/mnt/host/mechanicall-os";

    users.users.operator = {
      isNormalUser = true;
      extraGroups = [ "wheel" "networkmanager" "video" ];
      initialPassword = "operator";
    };
    users.users.root.initialPassword = "root";
    security.sudo.wheelNeedsPassword = false;

    # Placeholder dirs; real share comes from virtualisation.sharedDirectories in vmVariant
    systemd.tmpfiles.rules = [
      "d /mnt/host 0755 root root -"
      "d /mnt/host/mechanicall-os 0755 root root -"
      "d /opt/mechanicall-os 0755 root root -"
    ];

    environment.systemPackages = with pkgs; [
      vim
      curl
      htop
      git
      python3
    ];

    environment.variables.AETHER_HOME = "/mnt/host/mechanicall-os";

    environment.shellAliases = {
      panel = "aether panel";
      chat = "echo 'Use host Arch Ollama: ollama run personal-llm-full:v1' >&2; false";
    };

    environment.etc."mechanicall/README-vm.txt".text = ''
      Mechanicall DEV VM — rebuild/test here, not on the Kingston stick.

      Login:  operator / operator
      Share:  /mnt/host/mechanicall-os  (host repo via 9p)
      Panel:  aether panel
      Dump:   aether panel --dump

      Edit files on Arch; they appear in the share. Re-run scripts/vm/dev-up.sh after flake/NixOS module changes.
      Deploy to physical stick only when the VM generation is known-good.
    '';

    # --- Ephemeral QEMU via: nix build .#nixosConfigurations.portable-kingston-vm.config.system.build.vm
    virtualisation.vmVariant = {
      # qemu-vm module options
      virtualisation = {
        memorySize = 8192;
        cores = 4;
        graphics = false;
        diskSize = 10240; # MB for the ephemeral disk
        # target must be an *absolute* guest path (this was the eval failure)
        sharedDirectories = {
          mechanicall = {
            source = "/home/anphuni/mechanicall-os";
            target = "/mnt/host/mechanicall-os";
          };
        };
      };

      # No virtiofs in ephemeral VM — 9p is wired by sharedDirectories
      mechanicall.aether.home = lib.mkForce "/mnt/host/mechanicall-os";
      environment.variables.AETHER_HOME = lib.mkForce "/mnt/host/mechanicall-os";
    };

    system.stateVersion = "24.11";
  };
}
