#!/usr/bin/env python3
"""Play a You Decide room in chromium. Stills + walk log.

Never Send. Never BUY. Never Yes. Never write CURRENT. Never deploy.
Website analogue of sit-sitter / storm-walk.
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "site_play.cjs"
DEFAULT_URL = (
    "http://127.0.0.1:8788/you-decide/t/e9b16791a12ac1ef521891b6eac3bf68"
)
NODE_PATH = os.environ.get("NODE_PATH", "/usr/lib/node_modules")
CHROMIUM = os.environ.get("SITE_PLAY_CHROMIUM", "/usr/bin/chromium")


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--url", default=DEFAULT_URL)
    p.add_argument(
        "--out",
        default=str(ROOT / "dev" / "64_site-play" / "02_play" / "output"),
    )
    p.add_argument("--width", type=int, default=1440)
    p.add_argument("--height", type=int, default=900)
    args = p.parse_args()
    if not SCRIPT.is_file():
        print(f"missing walker: {SCRIPT}", file=sys.stderr)
        return 2
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env["NODE_PATH"] = NODE_PATH
    env["SITE_PLAY_CHROMIUM"] = CHROMIUM
    env["SITE_PLAY_VIEWPORT"] = f"{args.width}x{args.height}"
    cmd = ["node", str(SCRIPT), args.url, str(out)]
    print(" ".join(cmd), flush=True)
    return subprocess.call(cmd, env=env, cwd=str(ROOT))


if __name__ == "__main__":
    raise SystemExit(main())
