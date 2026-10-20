#!/usr/bin/env python3
"""One local Ollama grill of aether bookmark. Writes V6-GRILL.md. Not Yes."""
from __future__ import annotations

import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

MODEL = "personal-llm-sft-v6:latest"
HOST = "http://127.0.0.1:11434"
OUT = Path(__file__).resolve().parent.parent / "output" / "V6-GRILL.md"
SYSTEM = Path(
    "/mnt/kingston-nixos-sync/opt/mechanicall-os/references/personal-llm-system.txt"
).read_text(encoding="utf-8")

PROMPT = """You are personal-llm-sft-v6:latest. Propose only. Never approve. Do not name a password, key, token, or root command. Write once. Do not repeat the same sections.

Propose a complete spec for one new aether verb: bookmark.

Live facts (do not invent other verbs or files):
- aether is one POSIX script. Verbs include current, preflight, apply, approve, reject, next, probe, event, artifact. bookmark is NOT in AETHER_VERBS.
- aether apply copies a fenced # CURRENT body onto CURRENT.md and backs up the old file to .aether/current-before/. That backup is not a bookmark.
- aether approve is Yes. Bookmark is not Yes.
- aether event appends one JSONL line. Bookmark copies CURRENT.md bytes.
- A manual snapshot already exists: .aether/bookmarks/CURRENT-20261016T162428Z-this-current.md cksum 3532677481.
- Restore is NOT in this first verb. Restore would be a later human hand like apply.
- Models may snapshot. Models never approve, apply, next, or restore.
- Do not invent aether snapshot, aether run --gpu-yes, preflight.md, apply.md, approve.md, or aether/01-PIN.md.

Write these sections once:
1. What aether bookmark is
2. Difference from apply, approve, event, and current-before
3. Usage: aether bookmark [label] [path] and aether bookmark list [path]
4. What it writes (path shape, event kind)
5. What it must never do
6. Failure modes
7. Tests that would prove it
8. Grill your own draft: holes that would become a Yes by accident
"""


def main() -> None:
    body = json.dumps(
        {
            "model": MODEL,
            "prompt": PROMPT,
            "stream": False,
            "system": SYSTEM,
            "options": {"temperature": 0.2, "num_predict": 1200},
        }
    ).encode("utf-8")
    req = urllib.request.Request(
        HOST.rstrip("/") + "/api/generate",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        raw = json.loads(resp.read().decode("utf-8"))
    text = (raw.get("response") or "").strip()
    if not text:
        raise SystemExit("ollama returned empty grill")
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        f"# V6 grill — aether bookmark — not CURRENT, not Yes\n\n"
        f"**Model:** `{MODEL}`\n"
        f"**Host:** `{HOST}`\n"
        f"**When:** {ts}\n"
        f"**Prompt tokens / eval:** {raw.get('prompt_eval_count')} / {raw.get('eval_count')}\n\n"
        f"This file is the model's draft. SPEC.md is the spec. The CURRENT proposal is what you apply.\n\n"
        f"## Model prose\n\n{text}\n",
        encoding="utf-8",
    )
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
