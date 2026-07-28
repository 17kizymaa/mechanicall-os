# Client-one learning: Android TV exists, GRUB steals every boot

**Device:** eMachine-class client (internal OS = Android TV / Android-x86 entertainment intent)  
**Symptom:** Power-on always lands in **GRUB** (or GRUB menu); internal Android TV (and other internal partitions) do not become the default useful environment.  
**Goal:** Make **Android TV the daily boot** — entertainment + light dev surface — and capture the workflow for the next client.

This is a **boot-priority / bootloader ownership** problem, not “Android is missing.”

---

## Why this happens (pattern to reuse)

| Layer | What often went wrong |
|--------|------------------------|
| **Boot order (firmware)** | USB / “ubuntu” / Alpine / “grub” EFI entry sorts **above** Android |
| **Shared ESP** | Linux GRUB wrote `EFI/BOOT/BOOTX64.EFI` or `grubx64.efi` as default |
| **MBR/BIOS** | GRUB in MBR; Android expects its own chain or different partition active |
| **Live USB residue** | Installing Alpine/GRUB tools while “just testing” rewrites the only boot path |
| **Multi-boot leftovers** | Win7 archive + failed Android + Linux GRUB = three claims, GRUB wins |

**Client lesson:** Any “temporary” Linux USB work is **not temporary** if it touches the ESP or MBR. Treat bootloader changes as **product-critical**.

---

## Non-goals (until human says wipe)

- Do **not** reformat Android `system` / `data` “to fix boot”
- Do **not** delete Windows archive without explicit backup intent
- Do **not** install another full Linux as the “easy fix” without recording boot impact

---

## Phase A — Inventory (boot Alpine live USB **without** running `grub-install`)

From live shell (**read-only mindset**):

```sh
# 1) What does firmware see?
# UEFI:
apk add efibootmgr 2>/dev/null; efibootmgr -v
# BIOS-only machines: skip efibootmgr; use disk layout instead

# 2) Disk map
lsblk -o NAME,SIZE,TYPE,FSTYPE,LABEL,UUID,MOUNTPOINTS,PARTTYPE
blkid
fdisk -l   # or: sfdisk -l

# 3) Find Android-ish partitions
blkid | grep -iE 'android|system|vendor|userdata|super|boot|ESP|EFI|vfat|ext4'
# Android-x86 often: system (ext4/squash), data, and EFI with android or boot

# 4) Mount ESP read-only and list loaders
mkdir -p /mnt/esp
# replace with real EFI partition, often vfat ~100–500M
mount -o ro /dev/sdXY /mnt/esp
find /mnt/esp/EFI -type f 2>/dev/null
ls -la /mnt/esp/EFI/*/ 2>/dev/null
umount /mnt/esp
```

**Record a table (paste into session notes):**

| Part | Size | FS | Label | Role guess | Boot files? |
|------|------|----|-------|------------|-------------|
| … | | | | Android system? | |
| … | | | | EFI/ESP | `EFI/…` |
| … | | | | GRUB / Linux | |
| … | | | | Win7 archive | |

---

## Phase B — Decide boot path (pick one)

### B1. UEFI machine (most common fix)

**Preferred:** set Android’s EFI entry **first**, leave GRUB installed but not default.

```sh
efibootmgr -v
# Identify Android / android-x86 / BootXXXX
efibootmgr -o XXXX,YYYY   # Android first, GRUB later
# Optional: remove broken entries only after listing
# efibootmgr -B -b ZZZZ
```

If Android has no EFI entry but files exist under `EFI/Android` or similar:

```sh
# example names vary — use what find showed
efibootmgr -c -d /dev/sdX -p N -L "Android TV" -l '\\EFI\\Android\\grubx64.efi'
# path must match real file on ESP
```

### B2. BIOS / legacy (no efibootmgr)

- Set **active** partition to Android boot partition if it uses a classic bootloader, **or**
- Repair Android-x86 GRUB config so **default entry is Android**, not Alpine/memtest, **or**
- Use firmware boot menu (F10/F12/Esc) once → select Android disk → then fix default in setup

### B3. GRUB is the only loader (chainload Android)

If only GRUB is installed, edit GRUB (from live, mount the GRUB config partition) to:

```text
set default="Android"
# or: set default=0 after reordering menu entries
```

and ensure `grub.cfg` has a `menuentry` that boots Android kernel/initrd or chainloads the Android partition.

**Do not** `grub-install` again unless inventory proves GRUB is required and Android EFI is gone.

---

## Phase C — “Migrate anyway” (workflow, not panic wipe)

“Migrate” here means **move the intended environment into first place**, not necessarily copy partitions over Ethernet.

| Step | Action | Success |
|------|--------|---------|
| C1 | Inventory (Phase A) over live USB | Table filled |
| C2 | Fix boot order (Phase B) | Cold boot → Android TV UI without picking GRUB |
| C3 | Confirm entertainment basics | Launcher, Wi‑Fi, remote/keyboard |
| C4 | Light “dev” surface | ADB over Wi‑Fi/USB, sideload one chat/browser app if desired |
| C5 | Document for next client | This file + `lsblk` + `efibootmgr -v` snapshot |

**Ethernet role (when cable works):**

- Live Alpine ↔ operator/MBP: `ssh`, copy inventory logs, push APKs later  
- **Not** required to rewrite partitions if only boot order is wrong  
- Useful for `adb connect` once Android is up on LAN  

**If Android system partition is actually corrupt** (mount fails, missing kernel):

1. Still **do not** wipe Win7 archive first  
2. Recover Android from backup image / reinstall Android-x86 **to the same slot** after snapshot  
3. That is a **separate authorized Next** (`reinstall-android-tv-slot`)

---

## Phase D — Client playbook (next client template)

Name: **“Entertainment device / dual-OS boot discipline”**

1. **Before any Linux USB “test”:** photograph `efibootmgr -v` + `lsblk`  
2. **Rule:** live USB work uses `nomodeset` / data mounts only; **ban** `grub-install` unless CURRENT says so  
3. **Default product boot** written in CURRENT: e.g. `**Next:** boot-android-tv`  
4. **Recovery card** (one page): “If GRUB appears → live USB → Phase A → B1”  
5. **Dev add-on only after entertainment boots:** ADB, one sideload path (see `firestick-sideloading` patterns)  

---

## Mechanicall alignment

| Principle | Application |
|-----------|-------------|
| Filesystem is truth | Boot state = ESP files + partition table + firmware order (`cat`/`efibootmgr`) |
| One Next | e.g. `inventory-boot` → then `set-android-default` |
| Silence ≠ permission | Do not wipe because GRUB is annoying |
| Learn for next client | This doc **is** the reusable stage output |

---

## Suggested CURRENT fields (edit by hand when ready)

```markdown
**Objective:** Android TV is the default power-on experience on client-one.
**Next:** inventory-boot
**Keep:** existing Android system/data if mountable; Win7 archive until copied
**Reject:** blind grub-install; wipe to “just use Alpine”
**Prohibited:** wipe-win7-archive; reformat-android-data
```

---

## Immediate operator checklist (today)

1. Boot **Alpine live only** (or any live USB that will not auto-run grub-install).  
2. Run Phase A; paste `efibootmgr -v` + `lsblk` + `blkid` into chat or `output/`.  
3. Together pick B1/B2/B3.  
4. One change → full power cycle test → only then persist further tooling (ADB/chat).  

Ethernet/SSH is optional sugar for pasting logs; the critical path is **firmware + ESP**, not partition migration over the wire.
