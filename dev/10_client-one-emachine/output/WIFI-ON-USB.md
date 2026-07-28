# WiFi on the eMachine Alpine USB (ALPINECFG)

**Done on:** mbp-edge, stick `/dev/sdb`  
**SSID used:** same home network as MBP (`EE-P97C9F`) — credentials taken from iwd on MBP, **not** stored in git.

## What was written on the stick

| Piece | Role |
|-------|------|
| Partition **ALPINECFG** | ~1.5 G FAT32 at `/dev/sdb1` (data) |
| `wifi/apply-wifi.sh` | Run as root on eMachine to bring `wlan0` up |
| `wifi/wpa_supplicant.conf` | Network secret (on stick only) |
| `wifi/interfaces` | Alpine `/etc/network/interfaces` template |
| `emachine.apkovl.tar.gz` | Optional Alpine overlay bundle |
| `README-WIFI.txt` | Same instructions on the stick |

## On the eMachine (BusyBox — **no lsblk**, no `mount -L`)

`Invalid argument` on mount usually means **fat/vfat modules not loaded**.  
`No such file or directory` usually means **mount by label** (BusyBox) or missing mkdir.

As **root**, after the stick is plugged in:

```sh
modprobe fat
modprobe vfat
modprobe nls_cp437
modprobe nls_iso8859-1
mdev -s
mkdir -p /media/ALPINECFG
cat /proc/partitions
blkid
# find LABEL="ALPINECFG" (~1.5G) → e.g. /dev/sda1 or /dev/sdb1
mount -t vfat /dev/XXXX /media/ALPINECFG
ls /media/ALPINECFG/wifi
sh /media/ALPINECFG/wifi/apply-wifi.sh
```

Same text lives on the stick: `EMACHINE-HANDCOPY.txt`.  
Helper: `wifi/mount-this.sh` (once you can run anything from a mounted path — chicken/egg, so hand-copy first).

## “Resource busy” + empty folder (eMachine)

**Meaning:** the filesystem did **not** attach to that folder. `ls` of an empty mountpoint is normal after a failed/busy mount. Running `sh …/apply-wifi.sh` then fails with “not found”.

**Typical causes**

1. Partition **already mounted** somewhere else (check `mount` / `cat /proc/mounts`).
2. You booted **from this same stick** — ISO half is busy; use the **other** partition (ALPINECFG), or a **different mountpoint** (`/mnt/cfg`).
3. Stale busy state — `umount` then remount.
4. Shell still **cwd inside** the mountpoint — `cd /` first.

**Recovery (hand-copy, no lsblk):**

```sh
cd /
umount /media/ALPINECFG 2>/dev/null
umount -l /media/ALPINECFG 2>/dev/null
cat /proc/mounts
# if you see ALPINECFG or a vfat on /dev/sdXN already, ls THAT path

mkdir -p /mnt/cfg
modprobe fat; modprobe vfat
modprobe nls_cp437; modprobe nls_iso8859-1
blkid
# LABEL="ALPINECFG" device only:
mount -t vfat /dev/XXXX /mnt/cfg
ls /mnt/cfg/wifi
# must show: apply-wifi.sh  interfaces  wpa_supplicant.conf
sh /mnt/cfg/wifi/apply-wifi.sh
```

If `ls /mnt/cfg/wifi` is still empty, the wrong device is mounted (or mount failed again) — paste `cat /proc/mounts` and `blkid`.

## Operator debug (MBP)

Stick may appear as `/dev/sdb` or `/dev/sdc`. Always **umount before unplug** (we hit a ghost `/media/ALPINECFG` after yank). Prefer:

```sh
findfs LABEL=ALPINECFG
mount -t vfat /dev/sdX1 /media/ALPINECFG
# when done:
umount /media/ALPINECFG
```

Then you can `apk add openssh` and `service sshd start` for LAN SSH.

## Boot caveat

The stick’s **partition table was changed** so we could add a writable data volume after the ISO image. File probe still shows ISO9660 “bootable” at the start of the device; **if the eMachine no longer boots the stick**, re-flash alpine-standard 3.24.1 ISO and we re-create only ALPINECFG in free space (or use a second USB for config).

## Security

Anyone with the stick has the WiFi password. Treat the stick like a key. Do not commit `wpa_supplicant.conf` into mechanicall-os.
