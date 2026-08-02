# Auto boot picker (no hold-Option)

## What you want
- Multi-OS **picker on every power-on**, without holding Option/Alt
- Option screen is fine as a concept; **rEFInd after/as that picker is OK**

## Hard limit (Apple firmware)
The grey **Startup Manager** (hold Option) **cannot** be set to auto-show.
There is no NVRAM switch for "always show Startup Manager" on Intel Macs.

## What *can* auto-show
**rEFInd** (already on internal ESP `/boot` = `/dev/sda1`):
- `timeout 20` → menu sits ~20s (Alpine + macOS entries)
- Loaded when firmware default = rEFInd / EFI Boot

## Why cold boot skips the picker today
Apple uses protected `efi-boot-device` NVRAM → **macOS** (`Boot0080`), not UEFI `BootOrder`.
From Alpine we can set `BootOrder: 0002,0003,0080` (rEFInd first) but **cannot write** `efi-boot-device` (EPERM).
So power-on still follows blessed macOS unless you re-bless once.

## One-time fix (recommended — permanent)
1. Reboot and **hold Option** (you already know this path).
2. Highlight the **EFI** / **rEFInd** / orange drive entry (not "Macintosh HD").
3. Hold **Control**, then click the up-arrow (or press Control+Enter).
   - Cursor becomes a circle → **sets that volume as default** for future boots.
4. Next power-ons: **rEFInd menu appears automatically** (no Option). Pick Alpine or macOS.

### Optional from macOS (if Control-click fails)
Mount EFI, then:
```bash
sudo mkdir -p /Volumes/ESP
sudo mount -t msdos /dev/disk0s1 /Volumes/ESP   # diskN s1 = EFI; check diskutil
sudo bless --mount /Volumes/ESP --setBoot --file /Volumes/ESP/EFI/refind/refind_x64.efi --shortform
```

## After it works
- rEFInd = your automatic picker (same role as Option screen, always-on)
- Option still available anytime as emergency picker
- macOS System Preferences → Startup Disk can re-steal the default; re-do Control-click if that happens

## Current EFI (Alpine)
- `Boot0002` rEFInd `\EFI\refind\refind_x64.efi`
- `Boot0003` EFI Boot `\EFI\BOOT\bootx64.efi` (same binary as rEFInd)
- `Boot0080` Mac OS X
- `BootOrder` 0002,0003,0080
- Fallback file `EFI/BOOT/bootx64.efi` == rEFInd
