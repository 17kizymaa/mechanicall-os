#!/usr/bin/env python3
"""aether — CLI for awareness-agent (Mechanicall OS v0)

Usage examples:
  python -m aether init
  python -m aether status
  python -m aether update
  python -m aether watch

This is plain Python. No magic.
"""

import argparse
import sys
from pathlib import Path

from .sidecars import (
    get_project_root, ensure_sidecars, read_awareness, read_context,
    SIDECAR_CONTEXT, SIDECAR_AWARENESS, SIDECAR_MEMORY_DIR
)
from .distill import run_distill


def cmd_init(args: argparse.Namespace) -> None:
    root = get_project_root(Path(args.path) if args.path else None)
    ensure_sidecars(root)
    print(f"Initialized sidecars in {root}")
    print(f"  {root / SIDECAR_CONTEXT}")
    print(f"  {root / SIDECAR_AWARENESS}")
    print(f"  {root / SIDECAR_MEMORY_DIR}/")


def cmd_status(args: argparse.Namespace) -> None:
    root = get_project_root(Path(args.path) if args.path else None)
    awareness = read_awareness(root)
    context = read_context(root)
    mem_dir = root / SIDECAR_MEMORY_DIR

    print(f"Project root: {root}")
    print("")
    print("Sidecars:")
    print(f"  {SIDECAR_AWARENESS}: {'present' if awareness else 'MISSING'}")
    if awareness:
        print(f"    last_updated: {awareness.get('last_updated')}")
        print(f"    file_count:   {awareness.get('file_count')}")
    print(f"  {SIDECAR_CONTEXT}: {'present' if context else 'MISSING'} ({len(context)} chars)")
    print(f"  {SIDECAR_MEMORY_DIR}/: {'present' if mem_dir.exists() else 'MISSING'} "
          f"({len(list(mem_dir.glob('*'))) if mem_dir.exists() else 0} items)")
    print("")
    if not awareness:
        print("Tip: run `aether init` (or python -m aether init)")


def cmd_update(args: argparse.Namespace) -> None:
    root = get_project_root(Path(args.path) if args.path else None)
    run_distill(root)


def cmd_watch(args: argparse.Namespace) -> None:
    root = get_project_root(Path(args.path) if args.path else None)
    print(f"Watching {root} (Ctrl-C to stop)")
    print("Note: v0 watcher uses simple polling. Real events coming soon.")
    # Minimal stub — a real implementation will live in watcher.py
    import time
    from .watcher import poll_loop

    try:
        poll_loop(root, interval=args.interval)
    except KeyboardInterrupt:
        print("\nWatch stopped.")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="aether",
        description="Awareness sidecar manager. Filesystem is truth. Markdown + Python only."
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("init", help="Create sidecar files in a project folder")
    p.add_argument("path", nargs="?", help="Project path (default: cwd)")
    p.set_defaults(func=cmd_init)

    p = sub.add_parser("status", help="Show sidecar state for a project")
    p.add_argument("path", nargs="?", help="Project path (default: cwd)")
    p.set_defaults(func=cmd_status)

    p = sub.add_parser("update", help="Distill fresh context into sidecars")
    p.add_argument("path", nargs="?", help="Project path (default: cwd)")
    p.set_defaults(func=cmd_update)

    p = sub.add_parser("watch", help="Observe filesystem and keep sidecars fresh")
    p.add_argument("path", nargs="?", help="Project path (default: cwd)")
    p.add_argument("--interval", type=float, default=5.0, help="Poll seconds (default 5)")
    p.set_defaults(func=cmd_watch)

    args = parser.parse_args(argv)
    try:
        args.func(args)
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
