#!/bin/sh
# Run aether against the A33 pocket via mbp-edge USB adb.
# Usage: sh scripts/aether-on-a33.sh current
#        sh scripts/aether-on-a33.sh current validate
#        sh scripts/aether-on-a33.sh brief
# Does not approve. Demo only.
set -e
EDGE="${POCKET_EDGE:-anphuni@100.70.86.90}"
SERIAL="${POCKET_SERIAL:-RZCW2038KHN}"
POCKET="${POCKET_PHONE_PATH:-/sdcard/mechanicall-pocket}"
HOME_A="${POCKET_AETHER_HOME:-/sdcard/mechanicall-aether}"
if [ $# -eq 0 ]; then
  set -- current
fi
# Args are verb tokens (letters, digits, ._-). Pocket path is last.
ssh -o BatchMode=yes -o ConnectTimeout=8 "$EDGE" \
  "adb -s $SERIAL shell 'export AETHER_HOME=$HOME_A; sh $HOME_A/aether $* $POCKET'"
