#!/bin/sh
# Persist STORM SDK packages. Developer infra only. Not Yes. Never A33.
set -eu
ROOT="$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)"
SDK="${ANDROID_SDK_ROOT:-$HOME/.android-sdk-mechanicall}"
JAVA_HOME="${JAVA_HOME:-$HOME/.jdk/temurin-17}"
export JAVA_HOME ANDROID_SDK_ROOT="$SDK" ANDROID_HOME="$SDK"
PATH="$SDK/cmdline-tools/latest/bin:$SDK/emulator:$SDK/platform-tools:$JAVA_HOME/bin:$PATH"
export PATH

SM="$SDK/cmdline-tools/latest/bin/sdkmanager"
if [ ! -x "$SM" ]; then
  echo "refused: sdkmanager missing under $SDK" >&2
  exit 2
fi

"$SM" --sdk_root="$SDK" --install \
  "emulator" \
  "platform-tools" \
  "platforms;android-34" \
  "system-images;android-34;google_apis;x86_64"

python3 "$ROOT/python/aether_storm.py" setup --name storm-0
python3 "$ROOT/python/aether_storm.py" status
echo "STORM factory ready. Do not share RZCW2038KHN. Confirm was not tapped."
