#!/bin/sh
# Exit 3 if PATH is the mechanicall-os operator tree (demo bind guard).
set -e
target="${1:-}"
[ -n "$target" ] || { echo "usage: pocket-refuse-root.sh <path>" >&2; exit 2; }
ROOT="$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)"
export PYTHONPATH="$ROOT/python${PYTHONPATH:+:$PYTHONPATH}"
python3 - "$target" <<'PY'
import sys
from aether_pocket import PocketError, refuse_if_operator
try:
    print(refuse_if_operator(sys.argv[1]))
except PocketError as e:
    print(e, file=sys.stderr)
    sys.exit(3)
PY