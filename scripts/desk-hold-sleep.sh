#!/bin/sh
# HOLD then S3 (CONJURE W11). Not Yes. Not Funnel.
# If a local graphical/ssh session is active, do nothing.
# Does not run unless MECHANICALL_ALLOW_SUSPEND=1 (never from an agent by default).
set -e
HOLD_SEC="${MECHANICALL_HOLD_SEC:-900}"
STAMP="${MECHANICALL_HOLD_STAMP:-$HOME/.mechanicall/desk-hold.stamp}"

active_session() {
  if command -v loginctl >/dev/null 2>&1; then
    loginctl list-sessions --no-legend 2>/dev/null | grep -q '[^[:space:]]'
    return $?
  fi
  return 1
}

if active_session; then
  echo "desk-hold: local session — skip S3"
  exit 0
fi

now=$(date +%s)
if [ -f "$STAMP" ]; then
  then_ts=$(cat "$STAMP")
  age=$((now - then_ts))
  if [ "$age" -lt "$HOLD_SEC" ]; then
    echo "desk-hold: HOLD ${age}s < ${HOLD_SEC}s"
    exit 0
  fi
fi

if [ "${MECHANICALL_ALLOW_SUSPEND:-}" != "1" ]; then
  echo "desk-hold: would S3 (set MECHANICALL_ALLOW_SUSPEND=1 to actually suspend)"
  exit 0
fi

echo "desk-hold: systemctl suspend"
exec systemctl suspend
