# Device ops — brightness (eMachine)

**Goal:** Screen as bright as the hardware allows (easier for teaching).

## Try this first

```sh
ls /sys/class/backlight/
```

If you see a folder (example name `intel_backlight` or `acpi_video0`):

```sh
# see current and max
cat /sys/class/backlight/*/brightness
cat /sys/class/backlight/*/max_brightness

# set to max (use the max number you just saw)
echo 9999 | tee /sys/class/backlight/*/brightness
```

Replace `9999` with the real max value from `max_brightness`.

## If that fails

- Some machines only dim under a desktop; text-only mode may have no backlight sysfs entry.
- Function keys: try **Fn + brightness up** on the keyboard.
- Record what worked below after you try it on the real device.

## Record (fill in on the device)

| Tried | Result |
|-------|--------|
| sysfs backlight | |
| Fn keys | |
| Other | **2026-07-28: brightness successfully set to MAX** (operator confirmed). |

See also `DEV-LOG-2026-07-28.md` for LAN/phone scan notes.
