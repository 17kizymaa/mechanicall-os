#!/usr/bin/env python3
"""Build library/movies-index.md from device /sdcard/Movies (ADB) or a local dir.

Usage:
  python3 scripts/tv/sync-movies-index.py --root domains/house-tv-desk
  python3 scripts/tv/sync-movies-index.py --root domains/house-tv-desk --local /path/to/Movies
  EME640_IP=192.168.1.235 python3 scripts/tv/sync-movies-index.py --root domains/house-tv-desk --adb
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

VIDEO_EXT = {".mp4", ".mkv", ".avi", ".mov", ".m4v", ".webm", ".ts"}


def list_local(path: Path) -> list[str]:
    if not path.is_dir():
        return []
    names = []
    for p in sorted(path.rglob("*")):
        if p.is_file() and p.suffix.lower() in VIDEO_EXT:
            names.append(p.name)
    return names


def list_adb(serial: str, remote: str = "/sdcard/Movies") -> list[str]:
    cmd = ["adb", "-s", serial, "shell", "ls", "-1", remote]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip() or r.stdout.strip() or "adb ls failed")
    names = []
    for line in r.stdout.splitlines():
        line = line.strip()
        if not line or line.startswith("ls:"):
            continue
        base = Path(line).name
        if Path(base).suffix.lower() in VIDEO_EXT:
            names.append(base)
    return sorted(set(names))


def write_index(root: Path, titles: list[str], source: str) -> Path:
    lib = root / "library"
    lib.mkdir(parents=True, exist_ok=True)
    out = lib / "movies-index.md"
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
    lines = [
        "# Movies on disk (index)",
        "",
        f"Generated {ts} from **{source}**.",
        "Desk uses this only to *propose* titles — it does not start playback.",
        "",
        "## Titles",
        "",
    ]
    if not titles:
        lines.append("- *(none found — push a film or fix the path)*")
    else:
        for t in titles:
            lines.append(f"- {t}")
    lines.append("")
    out.write_text("\n".join(lines), encoding="utf-8")
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Sync movies index for House Desk")
    ap.add_argument("--root", default=".", help="project root (domain with library/)")
    ap.add_argument("--local", help="local Movies directory")
    ap.add_argument("--adb", action="store_true", help="list via adb /sdcard/Movies")
    ap.add_argument(
        "--serial",
        default=os.environ.get(
            "EME640_SERIAL",
            f"{os.environ.get('EME640_IP', '192.168.1.235')}:{os.environ.get('EME640_ADB_PORT', '5555')}",
        ),
    )
    args = ap.parse_args()
    root = Path(args.root).resolve()

    if args.local:
        titles = list_local(Path(args.local))
        source = args.local
    elif args.adb:
        try:
            subprocess.run(
                ["adb", "connect", args.serial],
                capture_output=True,
                text=True,
                timeout=15,
            )
            titles = list_adb(args.serial)
            source = f"adb:{args.serial}:/sdcard/Movies"
        except Exception as e:
            print(f"error: {e}", file=sys.stderr)
            return 1
    else:
        # keep existing seed titles if no source — rewrite stamp only if file missing
        existing = root / "library" / "movies-index.md"
        if existing.is_file():
            print(f"kept {existing} (pass --adb or --local to refresh)")
            return 0
        titles = ["Big Buck Bunny (2008) — placeholder until --adb/--local"]
        source = "placeholder"

    path = write_index(root, titles, source)
    print(f"wrote {path} ({len(titles)} titles)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
