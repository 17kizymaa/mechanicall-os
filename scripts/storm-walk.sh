#!/bin/sh
# One STORM walker, one emulator serial, one pocket.
# Launch time is `am start -W`. A bank time runs from the tap until the
# content description changes. The UI dump and the screenshot come after
# that clock. Never Confirm. Never Yes. Never the A33.
set -eu
SERIAL="${1:?emulator-NNNN}"
OUT="${2:?/tmp/storm-env/<id>/out}"
PKG=com.mechanicall.pocket.demo
mkdir -p "$OUT"
TIMING="$OUT/timing.txt"
EVENTS="$OUT/events.log"
: > "$TIMING"
EVPID=

adb() { command adb -s "$SERIAL" "$@"; }

case "$SERIAL" in
  emulator-*) ;;
  *) echo "refused: not an emulator" >&2; exit 3 ;;
esac
got="$(adb get-serialno 2>/dev/null || true)"
case "$got" in
  "$SERIAL") ;;
  RZCW2038KHN) echo "refused: live A33" >&2; exit 3 ;;
  *) echo "refused: serial does not match" >&2; exit 3 ;;
esac

stop_events() {
  if [ -n "${EVPID:-}" ]; then
    kill "$EVPID" 2>/dev/null || true
    wait "$EVPID" 2>/dev/null || true
    EVPID=
  fi
  adb shell pkill uiautomator >/dev/null 2>&1 || true
}
trap stop_events EXIT

dump() {
  name="$1"
  adb shell uiautomator dump /sdcard/uidump.xml >/dev/null
  adb pull /sdcard/uidump.xml "$OUT/uidump-${name}.xml" >/dev/null
  adb exec-out screencap -p > "$OUT/${name}.png"
}

# Largest rack-sized node. Prints: left top right bottom desc
rack_of() {
  python3 - "$1" << 'PY'
import re, sys
xml = open(sys.argv[1], errors="replace").read()
best = None
for attrs in re.findall(r"<node ([^>]*?)(?:/>|>)", xml):
    def attr(name, attrs=attrs):
        m = re.search(rf'{name}="([^"]*)"', attrs)
        return m.group(1) if m else ""
    desc = attr("content-desc")
    bounds = attr("bounds")
    m = re.match(r"\[(\d+),(\d+)\]\[(\d+),(\d+)\]", bounds)
    if not m:
        continue
    l, t, r, b = (int(x) for x in m.groups())
    h = b - t
    if not (2000 <= h <= 2200):
        continue
    if not desc.startswith(("PLAN.", "DRAFT.", "DECIDE.", "RECEIPT.", "Choose your folder", "sit millwork")):
        continue
    area = (r - l) * h
    if best is None or area > best[0]:
        best = (area, l, t, r, b, desc)
if best is None:
    print("refused: rack bounds missing", file=sys.stderr)
    raise SystemExit(2)
print(best[1])
print(best[2])
print(best[3])
print(best[4])
print(best[5])
PY
}

new_desc() {
  python3 - "$EVENTS" "$@" << 'PY'
import sys
path, offset = sys.argv[1], int(sys.argv[2])
wanted = tuple(sys.argv[3:])
last = ""
with open(path, errors="replace") as handle:
    handle.seek(offset)
    data = handle.read()
for line in data.splitlines():
    key = "ContentDescription: "
    i = line.find(key)
    if i < 0:
        continue
    rest = line[i + len(key):].split(";", 1)[0].strip()
    if any(rest.startswith(prefix) for prefix in wanted):
        last = rest
print(last)
PY
}

# wait_desc MARK START_NS TIMEOUT_NS PREFIX...
wait_desc() {
  mark="$1"
  start="$2"
  timeout="$3"
  shift 3
  deadline=$((start + timeout))
  found=""
  while :; do
    found="$(new_desc "$mark" "$@")"
    if [ -n "$found" ]; then
      printf '%s' "$found"
      return 0
    fi
    now="$(date +%s%N)"
    if [ "$now" -ge "$deadline" ]; then
      return 0
    fi
    sleep 0.05
  done
}

start_events() {
  stop_events
  : > "$EVENTS"
  adb shell uiautomator events > "$EVENTS" 2>"$OUT/events.err" &
  EVPID=$!
  sleep 0.4
  if ! kill -0 "$EVPID" 2>/dev/null; then
    echo "refused: content description listener did not stay up" >&2
    exit 2
  fi
}

note() { printf '%s\n' "$1" >> "$TIMING"; }

note "launch_wait_ms is the system time to first frame"
note "home_page_ms is from issuing start until the plan or folder description"
note "a bank time is from issuing the tap until that page description"
note "dump and screenshot are after the clock"

adb shell am force-stop "$PKG"
start_events
mark="$(wc -c < "$EVENTS" | tr -d ' ')"
start="$(date +%s%N)"
adb shell am start -W -n "$PKG/.MainActivity" > "$OUT/launch.txt"
home_desc="$(wait_desc "$mark" "$start" 5000000000 "PLAN." "Choose your folder")"
end="$(date +%s%N)"
wait_ms="$(awk -F: '/^WaitTime:/{gsub(/ /,"",$2); print $2; exit}' "$OUT/launch.txt")"
total_ms="$(awk -F: '/^TotalTime:/{gsub(/ /,"",$2); print $2; exit}' "$OUT/launch.txt")"
note "launch_wait_ms ${wait_ms:-missing}"
note "launch_total_ms ${total_ms:-missing}"
if [ -n "$home_desc" ]; then
  note "home_page_ms $(( (end - start) / 1000000 ))"
else
  note "home_page_ms unchanged"
fi
note "home_desc ${home_desc:-unchanged}"
stop_events
dump home

t0="$(date +%s%N)"
adb shell true
t1="$(date +%s%N)"
note "adb_roundtrip_ms $(( (t1 - t0) / 1000000 ))"

rack_of "$OUT/uidump-home.xml" > "$OUT/rack.txt"
rack_l="$(sed -n '1p' "$OUT/rack.txt")"
rack_t="$(sed -n '2p' "$OUT/rack.txt")"
note "rack_origin ${rack_l},${rack_t}"

case "$home_desc" in
  PLAN.*) ;;
  *)
    note "banks skipped: home is not the plan"
    echo "opening is not Decide; Confirm was not tapped; Yes was not tapped"
    exit 0
    ;;
esac

# Pack centers of the four bank keys. View-local, added to the rack origin.
# Plan 243,1209  Draft 446,1209  Decide 649,1209  Receipt 851,1209
start_events

tap_bank() {
  name="$1"
  prefix="$2"
  cx="$3"
  cy="$4"
  sx=$((rack_l + cx))
  sy=$((rack_t + cy))
  mark="$(wc -c < "$EVENTS" | tr -d ' ')"
  start="$(date +%s%N)"
  adb shell input tap "$sx" "$sy"
  found="$(wait_desc "$mark" "$start" 2500000000 "$prefix")"
  end="$(date +%s%N)"
  ms=$(( (end - start) / 1000000 ))
  case "$found" in
    "$prefix"*) note "${name}_ms ${ms}" ;;
    "") note "${name}_ms unchanged" ;;
    *) note "${name}_ms unexpected" ;;
  esac
  note "${name}_desc ${found:-unchanged}"
  note "${name}_tap ${sx},${sy}"
  stop_events
  dump "$name"
  if [ "$name" != "plan" ]; then
    start_events
  fi
}

tap_bank draft "DRAFT." 446 1209
tap_bank decide "DECIDE." 649 1209
tap_bank receipt "RECEIPT." 851 1209
tap_bank plan "PLAN." 243 1209

echo "opening is not Decide; Confirm was not tapped; Yes was not tapped"
printf 'timing %s\n' "$TIMING"
