# Personal vault: LUKS passphrase at boot, RO mount at /vault.
# Passphrase never stored in the nix store.
{ lib, pkgs, config, ... }:
{
  options.mechanicall.vault = {
    enable = lib.mkEnableOption "vault LUKS + /vault mount" // { default = true; };
    uuid = lib.mkOption {
      type = lib.types.str;
      default = "af6be1c7-27b3-42f8-91ca-fa3b07c3e98e";
    };
    mountPoint = lib.mkOption {
      type = lib.types.str;
      default = "/vault";
    };
  };

  config = lib.mkIf config.mechanicall.vault.enable {
    environment.systemPackages = [
      pkgs.cryptsetup
      (pkgs.writeShellScriptBin "vault" ''
        set -euo pipefail
        MNT="${config.mechanicall.vault.mountPoint}"
        MAPPER=kingston-vault
        UUID="${config.mechanicall.vault.uuid}"
        case "''${1:-}" in
          on|open|start)
            if [[ ! -e /dev/mapper/$MAPPER ]]; then
              sudo cryptsetup open "UUID=$UUID" "$MAPPER"
            fi
            if ! mountpoint -q "$MNT"; then
              sudo mkdir -p "$MNT"
              sudo mount -o ro,nosuid,nodev,noexec "/dev/mapper/$MAPPER" "$MNT"
            fi
            echo "vault RO at $MNT"
            ;;
          off|close|stop)
            if mountpoint -q "$MNT"; then sudo umount "$MNT" || true; fi
            if [[ -e /dev/mapper/$MAPPER ]]; then sudo cryptsetup close "$MAPPER" || true; fi
            echo "vault closed"
            ;;
          status|st)
            cryptsetup status "$MAPPER" 2>/dev/null || echo "mapper closed"
            findmnt "$MNT" || echo "not mounted"
            ;;
          *)
            echo "usage: vault on|off|status"
            exit 1
            ;;
        esac
      '')
    ];

    # First-class encrypted filesystem: prompts for passphrase during boot
    fileSystems.${config.mechanicall.vault.mountPoint} = {
      device = "/dev/mapper/kingston-vault";
      fsType = "ext4";
      options = [ "ro" "nosuid" "nodev" "noexec" "nofail" ];
      encrypted = {
        enable = true;
        blkDev = "/dev/disk/by-uuid/${config.mechanicall.vault.uuid}";
        label = "kingston-vault";
      };
    };
  };
}
