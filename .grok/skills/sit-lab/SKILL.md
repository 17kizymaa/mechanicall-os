---
name: sit-lab
description: >
  Lab factory for the Mechanicall sit APK on the A33 via mbp-edge USB.
  Archive every sideload, rollback a previous APK, wake the panel, capture
  a honest look PNG. Use when assembling, sideloading, looking, restoring,
  or rolling back the sit. Never Confirm. Never aether approve. USB ≠ LTE.
---

# Sit lab

You move **binaries and pixels**, not law. CURRENT still wins. Opening the app is not Yes.

## Law

1. Read the pocket that owns this sitting (`sit-ui-sprint` CURRENT or mechanicall-os CURRENT). One Next.
2. Never `aether approve` / `next`. Never Confirm.
3. USB on `mbp-edge` is not LTE. Serial `RZCW2038KHN` is the A33.
4. Do not overwrite the phone until the **currently installed** APK is in `~/.mechanicall/apk-archive/`.

## Commands (repo `scripts/`)

```bash
# keep what's on the A33 (run before a new sideload)
scripts/sit-apk-from-device.sh

# archive a local APK as mechanicall-<versionName>-vc<versionCode>.apk
scripts/sit-apk-archive.sh android/app/build/outputs/apk/debug/app-debug.apk

scripts/sit-apk-list.sh
scripts/sit-apk-rollback.sh LAST
scripts/sit-apk-rollback.sh 0.18.1-storage

scripts/sit-wake.sh
scripts/sit-look.sh /tmp/sit-look.png

POCKET_EDGE=mbp-edge scripts/sideload-apk-via-edge.sh
```

`sideload-apk-via-edge.sh` now: archives on-device APK → `install -r -d` → archives the new APK.

## Look failures

| Symptom | Cause | Tool |
|---------|-------|------|
| `not a PNG` | `adb exec-out` mixed a warning into stdout | `sit-look.sh` pulls a device file |
| tiny / near-black PNG | doze, panel off | `sit-wake.sh` then look again |
| no previous APK | never archived | `sit-apk-from-device.sh` **before** install |

## Not this skill

- Imagine plates, CURRENT recants, mesh, Funnel, Play Console.
- Treating a look PNG as Yes.
