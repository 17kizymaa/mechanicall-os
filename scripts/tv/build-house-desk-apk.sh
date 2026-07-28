#!/usr/bin/env bash
# Build House Desk WebView APK if Android SDK + Gradle wrapper available.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
APP="$ROOT/android/house-desk"
cd "$APP"

if [ -z "${ANDROID_HOME:-}${ANDROID_SDK_ROOT:-}" ]; then
  if [ -d "$HOME/Android/Sdk" ]; then
    export ANDROID_HOME="$HOME/Android/Sdk"
  fi
fi

if [ -z "${ANDROID_HOME:-}${ANDROID_SDK_ROOT:-}" ]; then
  echo "ANDROID_HOME not set — cannot build APK."
  echo "Zero-APK alternative: $ROOT/scripts/tv/open-desk-on-tv.sh"
  exit 2
fi

if [ ! -f ./gradlew ]; then
  echo "No gradle wrapper. Generating with system gradle if present..."
  if command -v gradle >/dev/null 2>&1; then
    gradle wrapper --gradle-version 8.2
  else
    echo "Install Android Studio or gradle wrapper, then re-run."
    echo "Or use: open-desk-on-tv.sh"
    exit 2
  fi
fi

./gradlew :app:assembleDebug
echo "APK: $APP/app/build/outputs/apk/debug/app-debug.apk"
