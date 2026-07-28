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

## On the eMachine (after you plug the stick back in)

Boot Alpine (from this stick if it still boots, or another Alpine). As **root**:

```sh
mkdir -p /media/ALPINECFG
mount -L ALPINECFG /media/ALPINECFG
# if label fails:
# lsblk -f
# mount /dev/sdX1 /media/ALPINECFG

sh /media/ALPINECFG/wifi/apply-wifi.sh
ip -4 addr show wlan0
ping -c 2 192.168.1.241
```

Then you can `apk add openssh` and `service sshd start` for LAN SSH.

## Boot caveat

The stick’s **partition table was changed** so we could add a writable data volume after the ISO image. File probe still shows ISO9660 “bootable” at the start of the device; **if the eMachine no longer boots the stick**, re-flash alpine-standard 3.24.1 ISO and we re-create only ALPINECFG in free space (or use a second USB for config).

## Security

Anyone with the stick has the WiFi password. Treat the stick like a key. Do not commit `wpa_supplicant.conf` into mechanicall-os.
