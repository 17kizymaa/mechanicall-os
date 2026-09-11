#!/bin/sh
# Mum-class benchmark statements. Never Confirm. Never A33.
set -eu
ROOT="$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)"
exec python3 "$ROOT/python/mum_verify.py" "$@"
