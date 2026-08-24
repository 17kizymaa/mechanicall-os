#!/bin/sh
# Boot storm-0 in the isolated AVD home. Never Confirm. Never A33.
set -eu
ROOT="$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)"
NAME="${1:-storm-0}"
export ANDROID_SDK_ROOT="${ANDROID_SDK_ROOT:-$HOME/.android-sdk-mechanicall}"
export JAVA_HOME="${JAVA_HOME:-$HOME/.jdk/temurin-17}"
export MECHANICALL_STORM_HOME="${MECHANICALL_STORM_HOME:-$HOME/.mechanicall/storm}"
export ANDROID_AVD_HOME="$MECHANICALL_STORM_HOME/avd"
EMU="$ANDROID_SDK_ROOT/emulator/emulator"

python3 "$ROOT/python/aether_storm.py" create --name "$NAME"
case "$NAME" in
  storm-*) ;;
  *) echo "refused: name must be storm-N" >&2; exit 2 ;;
esac
if [ ! -x "$EMU" ]; then
  echo "refused: emulator binary missing" >&2
  exit 2
fi
exec "$EMU" -avd "$NAME" -no-snapshot -gpu swiftshader_indirect
