#!/bin/sh
# Functional You Decide gauntlet on storm-0. Never Confirm. Never A33.
set -eu
ROOT="$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)"
exec python3 "$ROOT/python/you_decide_gauntlet.py" "$@"
