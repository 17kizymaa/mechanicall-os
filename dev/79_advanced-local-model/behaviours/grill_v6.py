#!/usr/bin/env python3
"""One local Ollama grill of personal-llm-sft-v6:latest. Writes V6-GRILL.md. Not Yes."""
from __future__ import annotations

import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

MODEL = "personal-llm-sft-v6:latest"
HOST = "http://127.0.0.1:11434"
OUT = Path(__file__).resolve().parent.parent / "output" / "V6-GRILL.md"

PROMPT = """You are personal-llm-sft-v6:latest. Propose only. Never approve. Never claim current permission. Do not name a password, key, token, or root command. Do not unlock anything.

Write a complete, advanced, standardised local-model framework the operator could later approve. Host tag is personal-llm-sft-v6:latest. Weight stays outside the APK and outside git.

Cover these as named sections:
1. What the local model is allowed to write
2. What it must never write or run
3. How a call is pinned (tag, host, SYSTEM)
4. How propose files sit next to CURRENT, preflight, apply, approve
5. Doctor's Note (stuck-gate record; not Yes; not the grant)
6. Bookmark (snapshot of CURRENT bytes; parked; not Yes; not apply)
7. aether run (parked; ollama-shaped type-then-approve-or-reject)
8. When rented GPU is the hardcore path (operator Yes; not this halt)
9. Failure modes
10. A short standard call recipe

Then grill your own draft: list holes, stale pins, and anything that would become a Yes by accident.

Clock: DRAFT_DESK_MODEL is already personal-llm-sft-v6:latest. OLLAMA_PREFER starts with personal-llm-sft-v6. A host call writes PROPOSE-CURRENT.md only. aether bookmark is not in AETHER_VERBS. Onyx is parked. Models never approve. Silence is never permission.
"""


def main() -> None:
    body = json.dumps(
        {
            "model": MODEL,
            "prompt": PROMPT,
            "stream": False,
            "system": Path(
                "/mnt/kingston-nixos-sync/opt/mechanicall-os/references/personal-llm-system.txt"
            ).read_text(encoding="utf-8"),
            "options": {"temperature": 0.2},
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
        f"# V6 grill — not CURRENT, not Yes\n\n"
        f"**Model:** `{MODEL}`\n"
        f"**Host:** `{HOST}`\n"
        f"**When:** {ts}\n"
        f"**Prompt tokens / eval:** {raw.get('prompt_eval_count')} / {raw.get('eval_count')}\n\n"
        f"This file is the model's draft. It is not a framework until FRAMEWORK.md. "
        f"It does not approve.\n\n"
        f"## Model prose\n\n{text}\n",
        encoding="utf-8",
    )
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
