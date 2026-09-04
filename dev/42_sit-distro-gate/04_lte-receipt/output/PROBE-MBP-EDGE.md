# Probe — mbp-edge adb (not an LTE receipt)

**When:** 2026-08-25 (re-probe)  
**Not Yes.** USB is the adb pipe. LTE proof is radio, not the cable. Sharing RZCW2038KHN as STORM serial: Reject (USB-read/probe/sideload of the operator A33 is allowed; not STORM).

## Re-probe

| Field | Prior | Re-probe |
|-------|--------|----------|
| Wi-Fi | CONNECTED `Three_A475F1` `192.168.0.180` | **disabled** |
| Default internet | Wi-Fi primary | **MOBILE[LTE] extra: everywhere** `rmnet0` `10.99.50.23/24` defaultNetwork=true INTERNET |
| IMS LTE | rmnet1 | still present, not default |
| Serial / USB | RZCW2038KHN usb:3-2 | unchanged |

`aether preflight sit-distro-gate` allowed. Phase EXECUTE · Status BLOCKED-PENDING-HUMAN.

`aether preflight sit-distro-gate` allowed. Phase EXECUTE · Status BLOCKED-PENDING-HUMAN.

## Bus

| Field | Value |
|-------|--------|
| Host | `mbp-edge` (`100.70.86.90`) |
| Transport | **USB** `usb:3-2` |
| Serial | `RZCW2038KHN` |
| Model | SM-A336B (A33) |
| myarch `adb devices` | empty |

## Radio (dumpsys)

| Network | State |
|---------|--------|
| **WIFI** | **CONNECTED, TRANSPORT_PRIMARY.** SSID `Three_A475F1`. IPv4 `192.168.0.180/24`. Gateway `192.168.0.1`. This is LAN Wi-Fi, not cellular internet. |
| MOBILE[LTE] | Present as **IMS** (`extra: ims`, capabilities include IMS). Not the default INTERNET path. |
| Voice/data CS/PS | LTE **IN_SERVICE** (operator EE / 1p). Data connection used for internet is still Wi-Fi. |

## Why this is still BLOCKED

1. Install path would be **USB via mbp-edge** — CURRENT names that as **not** the LTE receipt.  
2. Default internet is **Wi-Fi** (`192.168.0.180`), not LTE.  
3. `scripts/sideload-apk-via-edge.sh` itself says it is not an LTE receipt.  
4. Sideload of a **debug APK** would not be the signed `0.17.1-api36` AAB path anyway (AAB is not `adb install`).

## What would make a real RECEIPT.md

On this A33 (or another phone): **Wi-Fi off**, dumpsys showing **CELLULAR INTERNET** as primary (not IMS-only, not `192.168.0.x` wlan), then sideload the **signed** API-36 artifact. USB may still be the adb pipe; the **proof** is radio state, not the cable. Until Wi-Fi is off, I will not write RECEIPT.md.

Did not `adb install`. Did not Console-upload. Did not `aether next sit-conjure-desk`.
