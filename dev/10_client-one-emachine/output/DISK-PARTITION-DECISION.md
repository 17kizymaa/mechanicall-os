# Disk / partition decision tree — eMachine E640

**Status:** advisory only. **Not authorized:** wipe, reformat, or install OS.  
**Context:** failed AndroidOS · archived Windows 7 · short-term Alpine USB.

---

## Principle

Mount **read-only** first. Write only to media you intend to treat as disposable or explicitly chosen for Delroy’s home. Alpine USB is fine for a test-operation session; it is a poor sole home for durable research unless you accept loss on reimage.

---

## Inventory commands (on client, as root)

```sh
lsblk -o NAME,SIZE,FSTYPE,LABEL,UUID,MOUNTPOINTS
blkid
fdisk -l 2>/dev/null || sfdisk -l
cat /proc/mounts
df -h
```

Record a table:

| Device | Size | Fstype | Label | Current role (guess) | Safe action now |
|--------|------|--------|-------|----------------------|-----------------|

---

## Branching decisions

### 1) Alpine USB (live / install medium)

| Question | If yes |
|----------|--------|
| Is this the running root (`/`) | Expect changes (apk, users) to live here until reboot/reimage policy is clear |
| Enough free space for docs + thin aether surface? | OK for transfer package + TUI demo |
| Want Delroy home only on USB? | Possible for **short-term**; document as ephemeral |

**Recommended near-term:** keep OS on Alpine USB; put session transfer under `/home/Delroy/incoming/…` on that same root **or** on an internal data partition once identified.

### 2) Archived Windows 7 partition (NTFS/HFSish rare; usually NTFS)

| Action | When |
|--------|------|
| `mkdir -p /mnt/win7 && mount -t ntfs-3g -o ro /dev/sdXN /mnt/win7` | Need old files; **ro** first |
| Do **not** install Alpine here without a full backup plan | Archive means preserve |
| Do **not** use as primary Linux `/home` without backup | Hibernation/Windows dirty flags risk |

If `ntfs-3g` missing: `apk add ntfs-3g` (needs network once).

### 3) Failed AndroidOS partition (ext4 / userdata / weird hybrid)

| Action | When |
|--------|------|
| Identify with `blkid` / labels (`userdata`, `system`, etc.) | Always before mount |
| Mount **ro** if you need to scavenge files | `mount -o ro` |
| Assume unclean journal | `fsck` only with explicit later auth |
| Prefer **not** reusing as Delroy home until fsck + wipe plan approved | Failed OS ≈ untrusted metadata |

### 4) Empty or spare internal partition

Best candidate for persistent `/home/Delroy` **later**:

1. Confirm empty / expendable with human.
2. Still requires a **future** CURRENT Next (e.g. `prepare-home-partition`) — **not** this stage.
3. Then: mkfs only after approval, mount at `/home/Delroy` or `/home`.

---

## Suggested default for *this* week (no repartition)

```text
Alpine USB  →  running system + /home/Delroy (unix user) + incoming session docs
Internal disks →  leave unmounted or mount ro for forensics only
Project INIT →  deferred under /home/Delroy when test-operation session starts
```

Rationale: matches “short-term Alpine USB”, thermal limits (no long install), and deferred project folder.

---

## Mount cheatsheet (non-destructive)

```sh
mkdir -p /mnt/ro-inspect
mount -o ro /dev/sdXN /mnt/ro-inspect
ls /mnt/ro-inspect
# when done:
umount /mnt/ro-inspect
```

---

## What to send back to operator

Paste:

1. `lsblk -o NAME,SIZE,FSTYPE,LABEL,MOUNTPOINTS`
2. Which device is USB Alpine root
3. Any mount you performed (ro/rw)
4. Free space on `/` (`df -h /`)
