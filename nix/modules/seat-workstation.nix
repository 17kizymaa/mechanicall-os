# Seat workstation foundation on portable Kingston (already-built Track B host).
#
# Domain product shape: pre-OS bootloader-class menu (EFI GOP preferred, UGA fallback).
# This module is the *userspace foundation* wired into nixosConfigurations.portable-kingston:
#   ESP (systemd-boot, EFI) → NixOS kernel → seat-menu as primary operator surface.
# A native UEFI GOP seat app (rEFInd-class binary) is a later Next — not claimed here.
#
# PEER profile (skill) remains exclusive to personal-llm-sft-v4 by Domain contract;
# this module only ships PATH/env hooks — it does not grant write-tools or approve.
{ lib, pkgs, config, ... }:
let
  cfg = config.mechanicall.seat;
  aetherHome = config.mechanicall.aether.home;
  seatMenu = pkgs.writeShellScriptBin "seat-menu" ''
    export AETHER_HOME="''${AETHER_HOME:-${aetherHome}}"
    export PATH="$AETHER_HOME:$AETHER_HOME/bin:$PATH"
    exec "$AETHER_HOME/scripts/seat-menu.sh" "$@"
  '';
in
{
  options.mechanicall.seat = {
    enable = lib.mkEnableOption "seat workstation (aether shell/panel as primary surface)" // {
      default = true;
    };
    autologin = lib.mkOption {
      type = lib.types.bool;
      default = false;
      description = ''
        Autologin operator on tty1 and drop into seat-menu.
        Off by default (password still required). Enable only on single-operator stick.
      '';
    };
    user = lib.mkOption {
      type = lib.types.str;
      default = "operator";
      description = "Seat operator account";
    };
    # Domain product model name — PEER profile only. Seed may still ship full:v1 for chat alias.
    peerModel = lib.mkOption {
      type = lib.types.str;
      default = "personal-llm-sft-v4";
      description = "Model id allowed to wear PEER profile/skill (Domain contract)";
    };
  };

  config = lib.mkIf cfg.enable {
    environment.systemPackages = [
      seatMenu
      pkgs.python3
      pkgs.ncurses
    ];

    environment.variables = {
      AETHER_HOME = aetherHome;
      # Peer contract hint for seats (agent code must still enforce exclusivity)
      AETHER_PEER_MODEL = cfg.peerModel;
      AETHER_SEAT_MODE = "kingston-foundation";
    };

    environment.shellAliases = {
      seat = "seat-menu";
      shell = "aether shell";
      panel = "aether panel";
    };

    environment.etc."mechanicall/SEAT.txt".text = ''
      Mechanicall seat workstation — Kingston foundation
      ==================================================
      Host flake:  nixosConfigurations.portable-kingston
      Rebuild:     /opt/mechanicall-os/scripts/rebuild-portable-kingston.sh
      Seat menu:   seat-menu   (or: seat)
      Domain seat: aether shell | aether panel
      PEER model:  ${cfg.peerModel}  (PEER profile/skill only — no other model)

      Boot chain (this stick):
        Firmware (EFI GOP/UGA) → systemd-boot on ESP → NixOS → login → seat-menu

      Product target (Domain): pre-OS bootloader-class menu rendered via EFI GOP
      (UGA fallback). Userspace seat-menu is the foundation surface until a native
      EFI seat binary lands under a later Next.

      Docs: /opt/mechanicall-os/docs/SEAT-NIXOS-EFI-FOUNDATION.md
      Verify: /opt/mechanicall-os/scripts/seat-verify-kingston.sh
    '';

    # Optional: tty1 autologin → seat-menu (not full desktop)
    services.getty.autologinUser = lib.mkIf cfg.autologin cfg.user;

    # Drop operator into seat-menu on interactive login when SEAT_AUTO is set
    # or when autologin is on (profile.d).
    environment.etc."profile.d/mechanicall-seat.sh".text =
      let
        autoFlag = if cfg.autologin then "1" else "0";
      in ''
        # Mechanicall seat — primary workstation surface (not a soft desktop chat)
        # Set MECHANICALL_SEAT_AUTO=1 or enable mechanicall.seat.autologin to enter menu on login.
        # MECHANICALL_SEAT_SKIP=1 disables.
        if [ -n "''${PS1-}" ] && [ -z "''${MECHANICALL_SEAT_SKIP-}" ]; then
          _m_seat_auto="''${MECHANICALL_SEAT_AUTO:-${autoFlag}}"
          if [ "$_m_seat_auto" = "1" ]; then
            case "$-" in
              *i*)
                if [ -z "''${MECHANICALL_SEAT_STARTED-}" ] && [ -t 0 ]; then
                  export MECHANICALL_SEAT_STARTED=1
                  command -v seat-menu >/dev/null 2>&1 && seat-menu || true
                fi
                ;;
            esac
          fi
        fi
      '';
  };
}
