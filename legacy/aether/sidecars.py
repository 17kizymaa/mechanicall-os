"""Sidecar file handling.

All operations are direct FS reads/writes. No hidden state.
"""

from pathlib import Path
import json
from datetime import datetime, timezone
from typing import Dict, Any

SIDECAR_CONTEXT = ".context.md"
SIDECAR_AWARENESS = ".awareness.json"
SIDECAR_MEMORY_DIR = ".memory"
AETHER_DIR = ".aether"

def get_project_root(start: Path | None = None) -> Path:
    """Return the project root (directory containing sidecars or cwd)."""
    if start is None:
        start = Path.cwd()
    # For v0 we treat the current dir (or explicit) as the project root.
    # In future we may walk up looking for markers, but keep simple.
    return start.resolve()

def ensure_sidecars(root: Path) -> None:
    """Create minimal sidecar skeleton if missing."""
    root = root.resolve()
    root.mkdir(parents=True, exist_ok=True)

    awareness = root / SIDECAR_AWARENESS
    if not awareness.exists():
        data = {
            "created": datetime.now(timezone.utc).isoformat(),
            "last_updated": None,
            "file_count": 0,
            "notes": "Initialized by aether. Edit freely.",
        }
        awareness.write_text(json.dumps(data, indent=2) + "\n")

    context = root / SIDECAR_CONTEXT
    if not context.exists():
        context.write_text("""# Context

This is the living project context. It is the single source of truth for what this folder is about.

## Overview
(Write a short description here. aether can help keep it fresh.)

## Key Files
- (list important files or let aether summarize)

## Active Notes
- 

Generated/updated by aether. You can (and should) edit this file directly.
""")

    mem = root / SIDECAR_MEMORY_DIR
    mem.mkdir(exist_ok=True)

    (root / AETHER_DIR).mkdir(exist_ok=True)

def read_awareness(root: Path) -> Dict[str, Any]:
    path = root / SIDECAR_AWARENESS
    if not path.exists():
        return {}
    return json.loads(path.read_text())

def write_awareness(root: Path, data: Dict[str, Any]) -> None:
    path = root / SIDECAR_AWARENESS
    data = dict(data)  # copy
    data["last_updated"] = datetime.now(timezone.utc).isoformat()
    path.write_text(json.dumps(data, indent=2) + "\n")

def read_context(root: Path) -> str:
    path = root / SIDECAR_CONTEXT
    return path.read_text() if path.exists() else ""

def write_context(root: Path, content: str) -> None:
    (root / SIDECAR_CONTEXT).write_text(content.rstrip() + "\n")
