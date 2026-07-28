# Virtualization options — develop portable host + mechanicall on Arch

**Date:** 2026-07-27 (updated: role inversion)  
**Operator choice (current):** **Boot Kingston NixOS as Mechanicall host**; **Arch (myarch) is the virtual/mounted dev environment**.

**Earlier experiment (superseded for daily use):** Arch as host + `#portable-kingston-vm` guest — still available for flake testing on Arch, but not the operator’s preferred topology.

**Host facts (when on Arch):** Ryzen 5 2600 · AMD-V · kvm · ~40G free.  
**Doctrine:** Kingston NixOS = production presence for Mechanicall. Arch = integrated dev. Protocol alpha can still run bare-metal anywhere.

---

## Problem split

| Pain | Fix |
|------|-----|
| Forgot stick login | Offline recovery / password in Phase-2 Nix install docs (operator file) |
| Reboot loop for flake edits | KVM guest `#portable-kingston-vm` |
| Integrate with developing | virtiofs/9p share of `~/mechanicall-os` |

## Options verdict

| Option | Verdict |
|--------|---------|
| QEMU/KVM + qcow2 from flake | **Chosen** |
| libvirt + virt-manager | Recommended UX layer |
| Raw `/dev/sdc` passthrough | Reject for daily |
| Clone stick root only | Optional debug later |
| Docker “NixOS” | Reject for host fidelity |
| VirtualBox | Inferior on this host |

## Target architecture

```text
Arch (myarch)
├── ~/mechanicall-os
├── host Ollama / Open WebUI
└── KVM guest: mechanicall-portable-vm
      disk: ~/vms/portable-kingston.qcow2
      share: host repo → /mnt/host/mechanicall-os
      vault: disabled in VM profile
```

## Flake targets

| Attr | Role |
|------|------|
| `portable-kingston` | Real USB stick |
| `portable-kingston-vm` | Dev VM (no LUKS UUID, virtio, shared tree) |

## Resource policy

- Thin qcow ~40G; do not duplicate GGUFs into guest by default  
- 8G RAM guest v1; host Ollama for chat  
- GPU passthrough deferred  

## Non-goals

Multi-tenant desktops; virt required for alpha users; daily USB passthrough.
