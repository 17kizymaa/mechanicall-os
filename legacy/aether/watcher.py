"""Minimal filesystem watcher.

v0 design:
- Pure stdlib polling loop (no extra packages)
- Extremely simple and inspectable
- On any relevant change: trigger distill (update sidecars)
- All activity is visible: prints + sidecar updates

Future: can swap the polling engine for Linux inotify (still no heavy deps)
while keeping exactly the same sidecar contract.
"""

from pathlib import Path
import time
from typing import Callable, Set

from .sidecars import get_project_root
from .distill import run_distill, collect_files


def relevant_change(root: Path, last_snapshot: Set[str]) -> bool:
    """Return True if the set of relevant files changed."""
    try:
        current = {str(p) for p in collect_files(root)}
    except Exception:
        return True
    return current != last_snapshot


def poll_loop(root: Path, interval: float = 5.0, on_change: Callable[[Path], None] | None = None) -> None:
    """Simple polling loop. Calls on_change (or distill) when the file set mutates."""
    root = root.resolve()
    print(f"  poll interval: {interval}s")
    last: Set[str] = set()
    try:
        last = {str(p) for p in collect_files(root)}
    except Exception:
        pass

    while True:
        time.sleep(interval)
        if relevant_change(root, last):
            print(f"[{time.strftime('%H:%M:%S')}] change detected → updating sidecars")
            if on_change:
                on_change(root)
            else:
                run_distill(root)
            try:
                last = {str(p) for p in collect_files(root)}
            except Exception:
                last = set()
