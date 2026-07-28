# KVM/libvirt host role — run Arch (or other) guests *from* the portable NixOS stick.
# Nested virt not required: this system boots bare-metal on the Kingston.
{ lib, pkgs, config, ... }:
{
  options.mechanicall.virt-host = {
    enable = lib.mkEnableOption "KVM + libvirt host for integrated Arch dev guest" // {
      default = true;
    };
  };

  config = lib.mkIf config.mechanicall.virt-host.enable {
    virtualisation.libvirtd = {
      enable = true;
      qemu = {
        package = pkgs.qemu_kvm;
        runAsRoot = false;
        swtpm.enable = false;
        # Note: qemu.ovmf submodule was removed in recent nixpkgs;
        # OVMF is shipped with the QEMU package by default.
      };
    };

    # virbr0 appears when default network is started
    networking.firewall.trustedInterfaces = [ "virbr0" ];

    environment.systemPackages = with pkgs; [
      qemu_kvm
      qemu-utils
      virt-manager
      virt-viewer
      libvirt
      dnsmasq
      spice-gtk
      OVMF
    ];

    # operator can manage VMs without root (after re-login / newgrp)
    users.groups.libvirtd.members = [ "operator" ];
    users.users.operator.extraGroups = lib.mkAfter [ "libvirtd" "kvm" ];

    boot.extraModprobeConfig = ''
      options kvm_amd nested=1
      options kvm_intel nested=1
    '';

    environment.etc."mechanicall/README-virt-host.txt".text = ''
      Virt host (NixOS on Kingston hosts Mechanicall; Arch is the dev guest)

      Groups: operator ∈ libvirtd, kvm
      Check:  ls -l /dev/kvm && virsh list --all

      Arch guest helpers (after boot):
        /opt/mechanicall-os/scripts/vm/arch-guest-create.sh
        /opt/mechanicall-os/scripts/vm/arch-guest-start.sh

      Prefer large disks on internal SATA (myarch partition) for qcow:
        /mnt/myarch/home/anphuni/vms/myarch-dev.qcow2

      Mount Arch filesystem without full VM (quick file access):
        sudo /opt/mechanicall-os/scripts/vm/mount-myarch.sh
    '';
  };
}
