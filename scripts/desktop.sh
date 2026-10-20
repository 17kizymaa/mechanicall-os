#!/bin/sh
# Mechanicall desktop: two apps (Trader, Serve). Paper only. Not Yes.
set -eu
ROOT=$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)
export WEBKIT_DISABLE_DMABUF_RENDERER="${WEBKIT_DISABLE_DMABUF_RENDERER:-1}"
export WEBKIT_DISABLE_COMPOSITING_MODE="${WEBKIT_DISABLE_COMPOSITING_MODE:-1}"
exec python "$ROOT/python/desktop_os.py" "$@"
