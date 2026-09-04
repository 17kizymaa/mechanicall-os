# RECEIPT — LTE sideload (radio proof; USB was the adb pipe)

**Not Yes. Not Confirm. Not Play Console. Not `sit-conjure-desk`.**  
**Live Next:** `sit-distro-gate` clause 1. Preflight allowed. Phase EXECUTE.

## LTE proof (dumpsys — not the cable)

| Check | Result |
|-------|--------|
| Wi-Fi | **disabled** (was `Three_A475F1` / `192.168.0.180`) |
| Default internet | **MOBILE[LTE] extra: everywhere** · `rmnet0` `10.99.50.23/24` · `defaultNetwork=true` · INTERNET |
| IMS | `rmnet1` still up; not the default path |
| Host | `mbp-edge` USB `usb:3-2` serial `RZCW2038KHN` SM-A336B |

USB-on-mbp-edge is **not** the LTE proof (CURRENT Reject). It was only how `adb` reached the phone. The proof is Wi-Fi off + `rmnet0` default.

Not a STORM serial. USB-read/sideload of the operator A33 is allowed. Never Confirm.

## Sideload

| Field | Value |
|-------|--------|
| Artifact | `android/app/build/outputs/apk/release/app-release.apk` (gitignored) |
| SHA-256 | `c27fa706fc10476fa88974b657cfd85e22b109a6d0e0e926ba894a1090709b4f` |
| apksigner | Verifies (v2). Signer CN=Mechanicall closed testers, O=Mechanicall, C=GB. Cert SHA-256 `51ae5df0…c465a858` |
| Before | `0.15.0-vst` versionCode **16** targetSdk **34** (signature mismatch → uninstall) |
| After | `0.17.1-api36` versionCode **22** targetSdk **36** · `com.mechanicall.pocket.demo` |
| AAB (Play upload, not this install) | `app-release.aab` still at `android/app/build/outputs/bundle/release/` |

Did not `adb install` the debug APK. Did not open the app (opening is not Yes). Did not Console-login.

## Still this Next (not done)

2. Human Play **internal** upload of the signed **AAB** (after this receipt). Not production.  
3. Dirty git last (human Go-git).

Then stop. Human `aether next sit-conjure-desk` only after this Next closes.

Walkers did not tap Confirm. Models did not approve.
