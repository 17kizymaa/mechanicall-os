#!/bin/sh
# Wake the A33 over USB adb (mbp-edge). Not LTE. Not Funnel.
# Keeps the panel on while USB-powered so sit-look is not a black PNG.
set -eu
host=${SIT_LOOK_HOST:-${POCKET_EDGE:-mbp-edge}}
serial=${SIT_LOOK_SERIAL:-${POCKET_SERIAL:-RZCW2038KHN}}
ssh -o BatchMode=yes -o ConnectTimeout=8 "$host" \
  "adb -s $serial shell input keyevent KEYCODE_WAKEUP
   adb -s $serial shell wm dismiss-keyguard >/dev/null 2>&1 || true
   adb -s $serial shell settings put global stay_on_while_plugged_in 7 >/dev/null 2>&1 || true
   adb -s $serial shell dumpsys power | grep mWakefulness | head -1"
