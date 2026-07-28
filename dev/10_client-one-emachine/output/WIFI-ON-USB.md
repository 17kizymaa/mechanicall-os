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

## Operator debug (MBP)

Stick may appear as `/dev/sdb` or `/dev/sdc`. Prefer:

```sh
findfs LABEL=ALPINECFG
mount -t vfat /dev/sdX1 /media/ALPINECFG
```

Then you can `apk add openssh` and `service sshd start` for LAN SSH.

## Boot caveat

The stick’s **partition table was changed** so we could add a writable data volume after the ISO image. File probe still shows ISO9660 “bootable” at the start of the device; **if the eMachine no longer boots the stick**, re-flash alpine-standard 3.24.1 ISO and we re-create only ALPINECFG in free space (or use a second USB for config).

## Security

Anyone with the stick has the WiFi password. Treat the stick like a key. Do not commit `wpa_supplicant.conf` into mechanicall-os.
