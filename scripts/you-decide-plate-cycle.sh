#!/bin/sh
# Mechanical You Decide plate cycle. Never Confirm. Never A33.
# FLAG is iterate. PASS is not Yes. USB ≠ LTE.
set -eu
ROOT="$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)"
exec python3 "$ROOT/python/you_decide_plate_cycle.py" "$@"
