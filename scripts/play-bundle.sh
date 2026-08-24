#!/bin/sh
# Sign a Play-internal AAB using the off-git upload keystore.
# Does not log into Play Console. Does not write CURRENT. Not Yes.
set -e
ROOT="$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)"
PROPS="${PLAY_UPLOAD_PROPS:-$HOME/.mechanicall/play-upload.properties}"
[ -f "$PROPS" ] || {
  echo "missing $PROPS — create the off-git upload keystore first" >&2
  exit 2
}
export ANDROID_HOME="${ANDROID_HOME:-$HOME/.android-sdk-mechanicall}"
export ANDROID_SDK_ROOT="$ANDROID_HOME"
export JAVA_HOME="${JAVA_HOME:-$HOME/.jdk/temurin-17}"
cd "$ROOT/android"
if [ -n "${GRADLE_BIN:-}" ] && [ -x "$GRADLE_BIN" ]; then
  WRAPPER="$GRADLE_BIN"
elif [ -x /tmp/gradle-8.11.1/bin/gradle ]; then
  WRAPPER=/tmp/gradle-8.11.1/bin/gradle
else
  WRAPPER="./gradlew"
fi
"$WRAPPER" --no-daemon -Dhttps.protocols=TLSv1.2,TLSv1.3 :app:bundleRelease
AAB="$ROOT/android/app/build/outputs/bundle/release/app-release.aab"
[ -f "$AAB" ] || { echo "missing $AAB" >&2; exit 1; }
sha256sum "$AAB"
echo "Play Console upload is still a human step. Not production."
