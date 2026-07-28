# RECONFIGURE: Alpine WLAN on eMachine E640

**Action id:** `reconfigure-wlan`  
**Authorized by:** `dev/10_client-one-emachine/CURRENT.md`  
**Goal:** `wlan0` UP, associated, DHCP address on LAN (`192.168.1.0/24` typical).  
**Not goal:** prefer USB tethering; do not make rndis/usb0 the primary route.

---

## Why setup-interfaces can “accept password” but leave you offline

Alpine’s `setup-interfaces` often writes config and may run `wpa_passphrase`, but association still fails if any of these are true:

1. Interface never brought **UP**
2. `wpa_supplicant` not running or wrong conf path
3. No DHCP client bound (`udhcpc`)
4. **rfkill** soft-block
5. Missing **firmware / kernel module** (common on older eMachines)
6. Conf written for `wlan0` but driver exposes another name (`wlp…` rare on Alpine; sometimes only after module load)

Treat “password accepted” as **config written**, not **link ready**.

---

## A. Console checklist (on the eMachine, as root)

Run in order. Copy outputs into a note if you want operator-side diagnosis.

### A1. Inventory

```sh
ip link
ls /sys/class/net/
rfkill list all 2>/dev/null || true
dmesg | grep -iE 'wlan|firmware|80211|brcm|rtl|ath|iwl' | tail -40
lsmod | grep -iE 'cfg80211|mac80211|brcm|rtl|ath|iwl'
which wpa_supplicant wpa_passphrase udhcpc iw iwconfig 2>/dev/null
apk info -e wpa_supplicant wireless-tools linux-firmware 2>/dev/null
```

### A2. Unblock and open the interface

```sh
rfkill unblock wifi 2>/dev/null || rfkill unblock all 2>/dev/null || true
ip link set wlan0 up
ip link show wlan0
```

If `wlan0` does not exist: load drivers / install firmware (section B), then re-check `ip link`.

### A3. Inspect what setup-interfaces wrote

```sh
cat /etc/network/interfaces
ls -la /etc/wpa_supplicant/ 2>/dev/null
# common locations:
cat /etc/wpa_supplicant/wpa_supplicant.conf 2>/dev/null
grep -r ssid /etc/wpa_supplicant/ 2>/dev/null | head
```

### A4. Manual associate (most reliable debug path)

Replace `YOUR_SSID` / use existing conf if present.

```sh
# If you need a fresh PSK file:
wpa_passphrase 'YOUR_SSID' 'YOUR_PASSWORD' > /etc/wpa_supplicant/wpa_supplicant.conf
chmod 600 /etc/wpa_supplicant/wpa_supplicant.conf

# Kill stale daemon, then start foreground once to see errors:
killall wpa_supplicant 2>/dev/null || true
wpa_supplicant -i wlan0 -c /etc/wpa_supplicant/wpa_supplicant.conf -d
# Ctrl-C after you see COMPLETED or a clear failure (WRONG_KEY, timeout, etc.)
```

Background once healthy:

```sh
wpa_supplicant -B -i wlan0 -c /etc/wpa_supplicant/wpa_supplicant.conf
udhcpc -i wlan0
ip -4 addr show wlan0
ip route
ping -c 2 192.168.1.254
ping -c 2 192.168.1.241    # operator Arch host on this LAN
```

### A5. Persist with Alpine interfaces (after manual proof)

Minimal `/etc/network/interfaces` pattern:

```
auto lo
iface lo inet loopback

auto wlan0
iface wlan0 inet dhcp
        hostname emachine-delroy
```

Ensure `wpa_supplicant` starts on boot (OpenRC):

```sh
apk add wpa_supplicant
rc-update add wpa_supplicant default
# Some setups use ifup hooks; if DHCP dies across reboot, re-test and pin:
rc-update add networking default
```

OpenRC note: on many Alpine images, wireless is “interfaces + wpa_supplicant service”. If `ifup wlan0` fails, stay with the manual A4 commands until stable, then lock conf.

### A6. SSH for transfer

```sh
apk add openssh
rc-update add sshd default
service sshd start
passwd    # ensure root or Delroy has a password you control
ip -4 addr show wlan0
```

Report to operator: **IPv4 address** and whether login is `root` or `Delroy`.

---

## B. Firmware / driver (when wlan0 missing or firmware errors in dmesg)

Internet chicken-and-egg: if Wi‑Fi is down you need **one temporary** path for `apk`:

| Temporary path | Use |
|----------------|-----|
| Ethernet USB dongle | Best if available |
| Phone USB tether **once** | Allowed only as bootstrap to fetch packages — **not** steady state |
| Pre-downloaded apk on USB stick | Offline install |

Then:

```sh
# Broad toolkit (pulls a lot of firmware — disk/heat cost on USB root)
apk update
apk add wpa_supplicant wireless-tools iw linux-firmware

# If dmesg names a family, prefer smaller sets when you know them, e.g.:
# apk add linux-firmware-brcm
# apk add linux-firmware-rtlwifi
# apk add linux-firmware-ath
```

Reload:

```sh
# example only — use the module name dmesg implies
modprobe -r <bad_module> 2>/dev/null
modprobe <wifi_module>
ip link
```

**eMachine-era hardware** often needs proprietary Broadcom firmware (`brcm`). If `dmesg` says `Direct firmware load … failed`, that is the smoking gun — not the password.

---

## C. Do not prefer USB tether as default route

If `usb0` / `rndis0` is up for emergency `apk`:

```sh
ip route
# After WLAN works, drop tether default so LAN path wins:
# ip route del default dev usb0   # only if you understand active routes
# Prefer: unplug tether; confirm default via wlan0
ip route
```

Operator preference: **WLAN to LAN**. Keep tether unplugged once `ping 192.168.1.241` works.

---

## D. Success criteria (RECONFIGURE done)

- [ ] `ip link` shows `wlan0` state UP
- [ ] `wpa_supplicant` associated (COMPLETED)
- [ ] `ip -4 addr` shows LAN address
- [ ] `ping` gateway and operator `192.168.1.241` succeed
- [ ] `sshd` listening (for session file transfer)
- [ ] Default route is **not** tether unless human re-opens emergency path

---

## E. Operator-side wait loop (this host)

Once client reports IP:

```bash
ping -c 2 "$CLIENT_IP"
ssh -v root@"$CLIENT_IP" 'uname -a; ip -4 addr; rc-status'
```

Then run the rsync block in `SESSION-TRANSFER-2026-07-28.md`.

---

## F. Heat while reconfiguring

- Stay on TTY; avoid browsers and heavy `apk upgrade`
- Prefer `apk add` of only `wpa_supplicant` / needed firmware first
- If thermal shutdown mid-associate, cool down and re-run A4 only (config should remain on USB)
