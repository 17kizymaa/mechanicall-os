# STORM parallel test environments (myarch)

**Not CURRENT.** Research 2026-08-20. Opening is not a decision.

## Recommended path

**One local x86_64 API-34 `google_apis` AVD per STORM agent.** Unique `ANDROID_AVD_HOME`, adb serial `emulator-5554` / `5556`, isolated virtual `/sdcard`. Seed `examples/pocket-demo-client`. Walk with `uiautomator dump`. **Never Confirm. Never the A33.**

Cap: **2 AVDs** on this box (32 GiB, 0 swap).

## This host today

| Present | Missing |
|---------|---------|
| cmdline-tools, avdmanager, adb, platforms/android-34, build-tools 34 | **emulator package** |
| `/dev/kvm` + `kvm_amd` + CPU `svm` | **system-images;android-34;google_apis;x86_64** |
| APK already has `x86_64` Chaquopy | **no AVDs** |

Until emulator + image are installed, STORM is a **single flock on RZCW2038KHN**, not parallel.

## Install once (human factory — not done this turn)

```sh
export JAVA_HOME="$HOME/.jdk/temurin-17"
export ANDROID_SDK_ROOT="$HOME/.android-sdk-mechanicall"
sdkmanager --sdk_root="$ANDROID_SDK_ROOT" --install \
  "emulator" \
  "system-images;android-34;google_apis;x86_64"
emulator -accel-check
```

Play Store images: no. ARM images on this AMD box: no.

## Isolated pocket

Host: `/tmp/storm-env/<agent>/pocket/` copied from `examples/pocket-demo-client`.  
Device: that agent’s own AVD `/sdcard/mechanicall-pocket`.  
Refuse operator tree. Do not share live A33 pocket.

## Walker law

Parse uidump bounds (do not reuse A33 pixel taps). Force-stop, start, dump, Bind/Plan/Chat/Decide/Receipt, **Cancel** only. Never Confirm. Never `aether approve`. Chat may Send (desk now tries 127.0.0.1 first + `scripts/desk-through-a33.sh`).

## Not this

Public Ollama. Play Store. Sharing RZCW2038KHN. Compose-on-JVM as a sit. Copying operator CURRENT onto the phone.
