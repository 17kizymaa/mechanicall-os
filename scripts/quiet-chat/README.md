# Quiet chat on eMachine — why reboot showed nothing

## What went wrong

1. **Alpine live USB = RAM root.**  
   Everything we put in `/opt/chat`, `/etc/hostname`, `/etc/profile.d` lived in memory.  
   **Reboot wiped it.** That is normal for live media, not a mystery bug.

2. **Even before reboot, console may not use `profile.d`.**  
   BusyBox getty → login → shell does not always look like an interactive login the way we assumed.  
   So privacy/chat never appeared on the physical screen.

## What we do now

| Piece | Purpose |
|--------|---------|
| `install-quiet-chat.sh` | Install chat + **tty1 → chat-console** (no login dance) |
| `aether_desk.py` | Privacy banner → Hello → chat only |
| **ALPINECFG persist** | USB data partition keeps scripts/keys across reboots |
| `ALPINECFG/auto/start` | **One command after every live boot** to re-install into RAM |

## After each live boot (until disk install)

As root on eMachine:

```sh
modprobe vfat
mkdir -p /media/ALPINECFG
# find 1.5G FAT labeled ALPINECFG, then:
mount -t vfat /dev/sdX1 /media/ALPINECFG
sh /media/ALPINECFG/auto/start
reboot
```

After that reboot (still live), if install ran, **tty1 should open chat**.  
If you only run `auto/start` without reboot: type `chat`.

## Permanent fix

Install Alpine to the internal disk (not live USB). Then one install sticks.

## Keys

Never commit keys. On operator machine, Desktop `.env` has raw `sk-or-…`.  
Installer copies into `/root/.chat.env` and optional `ALPINECFG/chat.env`.
