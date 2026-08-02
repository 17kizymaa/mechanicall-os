# Seat NixOS EFI foundation — Kingston path (already built)

**Next:** `seat-nixos-efi-foundation` (APPROVED)  
**Host:** `nixosConfigurations.portable-kingston`  
**Stick:** Track B Kingston (~58G) — ESP + `nixos` + LUKS vault  
**Date:** 2026-08-02  

This document is the foundation contract for the **already-built** Kingston portable host.  
It does **not** reinstall the stick. It does **not** claim a finished native UEFI seat binary.

---

## 1. What “already built” means

| Piece | Status |
|-------|--------|
| Partition layout (ESP 1G + nixos 20G + LUKS vault ~37G) | Built (Track B) |
| Flake host `portable-kingston` | In repo |
| systemd-boot on ESP (`canTouchEfiVariables = false`) | Built |
| ollama + personal-llm seed + vault CLI + aether wrapper | Built |
| Userspace seats (`aether shell`, `aether panel` TUI) | Shipped (PR #2) |
| Seat module + `seat-menu` + this doc | **This Next** |
| Native pre-OS EFI GOP seat app (rEFInd-class binary) | **Later Next** |

**Operator path (no reinstall):**

1. Boot Kingston from firmware menu (USB / EFI entry).  
2. On stick: sync tree if needed, then `rebuild-portable-kingston.sh`.  
3. Login as `operator` → run `seat-menu` (or enable autologin later).

From Arch (dev host with stick mounted):

```sh
# Prefer stick mount
bash scripts/sync-to-kingston.sh
bash scripts/seat-verify-kingston.sh
# Rebuild only when *booted into* mechanicall-portable:
#   bash /opt/mechanicall-os/scripts/rebuild-portable-kingston.sh
```

---

## 2. Boot chain (EFI → seat)

```text
[ Firmware ]
    │  UEFI Simple Text / Console — uses EFI **GOP** when available
    │  (legacy **UGA** only on older firmware without GOP)
    ▼
[ ESP  label=ESP  /boot ]
    systemd-boot  (loader entries for NixOS generations)
    │
    ▼
[ Root  label=nixos ]
    NixOS  hostname mechanicall-portable
    │
    ▼
[ Login  operator ]
    seat-menu     ← userspace foundation (bootloader-class UX)
    aether panel | aether shell
```

### GOP vs UGA (Domain wording)

| Protocol | Role here |
|----------|-----------|
| **EFI GOP** | Preferred. Firmware and systemd-boot menu paint via Graphics Output Protocol. Product target for a future native seat EFI binary. |
| **UGA** | Compatibility fallback on old firmware only. Do not design new chrome around UGA. |

**Honest limit:** `aether panel` / `seat-menu` today run **after** the kernel. That is allowed as **foundation / development surface**. Domain product shape remains **pre-OS menu**; a native EFI app is a **later Next**, not redefined as “post-login optional TUI only.”

---

## 3. Package hooks (Nix)

| Path | Role |
|------|------|
| `nix/hosts/portable-kingston.nix` | Host; imports seat module |
| `nix/modules/seat-workstation.nix` | `seat-menu` on PATH, aliases, `SEAT.txt`, env |
| `nix/modules/aether.nix` | `aether` wrapper → `/opt/mechanicall-os` |
| `scripts/seat-menu.sh` | TTY workstation menu |
| `scripts/rebuild-portable-kingston.sh` | `nixos-rebuild switch` on stick |
| `scripts/sync-to-kingston.sh` | rsync from Arch → stick `/opt` |
| `scripts/seat-verify-kingston.sh` | Foundation checks |

**Options** (`mechanicall.seat.*`):

- `enable` (default true)  
- `autologin` (default **false**) — set true only on single-operator stick  
- `peerModel` (default `personal-llm-sft-v4`) — Domain PEER contract hint  

---

## 4. Domain constraints encoded (not lost)

| Constraint | Foundation handling |
|------------|---------------------|
| PEER profile/skill = **personal-llm-sft-v4 only** | Env `AETHER_PEER_MODEL`; docs; agent enforcement = later Next |
| CURRENT sole Domain law | seats always load project CURRENT; menu option “show CURRENT” |
| Editable CURRENT in UI | **Product target** — not shipped this Next |
| No PEER write-tools / auto-approve | Unchanged; not granted by seat module |
| No Electron / REST soft plane | seat-menu is sh + existing Python TUI |
| No vault unlock by agent | vault still human CLI |

---

## 5. Verification

### A. From Arch (stick plugged, nixos mounted)

```sh
bash scripts/seat-verify-kingston.sh
# expect RESULT: PASS
```

### B. On booted Kingston

```sh
bash /opt/mechanicall-os/scripts/rebuild-portable-kingston.sh
seat-menu
# 1 → panel · 2 → shell
cat /etc/mechanicall/SEAT.txt
```

### C. EFI fact (on UEFI machine)

```sh
test -d /sys/firmware/efi && echo UEFI_OK
# Bootloader paint is firmware GOP/UGA; do not claim native seat GOP app yet.
```

### D. VM (optional)

Existing flake VM path (`result-vm` if previously built) can smoke userspace seats;  
it does **not** replace bare-metal Kingston boot validation.

---

## 6. What this Next does / does not

**Does**

- Treat Kingston portable host as the deploy target (already built).  
- Wire seat foundation into the flake host.  
- Ship `seat-menu` + verify script + this contract.  
- Document EFI boot chain and GOP/UGA roles.

**Does not**

- Reinstall or repartition the stick.  
- Ship a UEFI `.efi` seat binary.  
- Finish PEER-profile exclusivity in agent code.  
- Finish in-UI CURRENT editor.  
- Touch vault unlock or TWS Domain.

---

## 7. Later Next candidates (after human re-pin)

1. `peer-exclusive-seats` — enforce PEER skill only on sft-v4 in shell/panel agents  
2. `panel-current-inline-edit` — editable CURRENT surface, human-confirm save  
3. `seat-efi-gop-app` — native pre-OS menu via GOP (rEFInd-class)  
4. `seat-autologin-operator` — enable `mechanicall.seat.autologin` on stick  

---

## 8. Related

- `scripts/rebuild-portable-kingston.sh`  
- `scripts/sync-to-kingston.sh`  
- `research/speculative/KINGSTON-NIXOS-STATE-REVIEW.md`  
- `dev/14_client-one-and-technique/output/KINGSTON-BOOT-NOW.md`  
- Root `CURRENT.md` — Next `seat-nixos-efi-foundation`
