#!/usr/bin/env python3
"""Call Claude Opus 5 (OpenRouter) as sprint lead. No secrets in output files."""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.request
from pathlib import Path

DEFAULT_MODEL = "anthropic/claude-opus-5"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

SYSTEM = """You are Claude Opus 5, authorized sprint LEAD collaborator for Mechanicall OS.

You plan and prioritize. The host agent (Grok Build) executes tools. You never claim to run aether approve.
Human is sole approver. Silence is never permission.

Product: local-first authority protocol (CURRENT.md + aether preflight + human yes).
Not core: multi-tenant SaaS, Session-as-product, live Outlook OAuth.
Session = capped hosted lab only. Operator primary TUI = Grok Build.

Output STRICT markdown:
1. Executive lead brief (≤15 lines)
2. Ordered waves (Wave 0..N) each with: goal, files, commands, acceptance
3. Immediate Wave 0 tasks for the host agent (checklist)
4. Risks / anti-patterns
5. Proposed thin CURRENT Next (action-id only) for human — do not claim applied

Be concrete. Prefer completing protocol over new chrome. No secrets."""


def load_key() -> str:
    """Prefer OPENROUTER_API_KEY env; else Desktop/.env raw sk-or lines.

    Operator note: line 1 may be a stale/list-only key; line 2 is often the
    active chat key. Prefer the *last* sk-or- raw line unless env is set.
    """
    if os.environ.get("OPENROUTER_API_KEY"):
        return os.environ["OPENROUTER_API_KEY"].strip()
    env = Path.home() / "Desktop" / ".env"
    if env.is_file():
        raw_sk: list[str] = []
        named = None
        for line in env.read_text().splitlines():
            s = line.strip()
            if not s or s.startswith("#"):
                continue
            if s.startswith("OPENROUTER_API_KEY="):
                named = s.split("=", 1)[1].strip().strip('"').strip("'")
            elif s.startswith("sk-or-"):
                raw_sk.append(s)
        # Prefer last raw sk-or (newer key often appended as line 2+)
        if raw_sk:
            return raw_sk[-1] if len(raw_sk) == 1 else raw_sk[-1]
        if named:
            return named
    raise SystemExit("OPENROUTER_API_KEY not found")


def chat(model: str, user: str, max_tokens: int = 6000) -> str:
    key = load_key()
    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": user},
        ],
        "temperature": 0.35,
        "max_tokens": max_tokens,
    }
    req = urllib.request.Request(
        OPENROUTER_URL,
        data=json.dumps(body).encode(),
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/17kizymaa/mechanicall-os",
            "X-Title": "mechanicall-os opus5 sprint lead",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        data = json.loads(resp.read().decode())
    if data.get("error"):
        raise SystemExit(f"OpenRouter error: {data['error']}")
    content = data["choices"][0]["message"]["content"]
    return content


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--brief", required=True, help="Path to brief markdown")
    ap.add_argument("--out", required=True, help="Write lead output here")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--max-tokens", type=int, default=6000)
    args = ap.parse_args()
    brief = Path(args.brief).read_text()
    user = (
        "Lead the sprint to completion from scaffolding present.\n\n"
        "=== BRIEF ===\n" + brief + "\n=== END BRIEF ===\n"
    )
    print(f"Calling {args.model}…", file=sys.stderr)
    out = chat(args.model, user, max_tokens=args.max_tokens)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    header = (
        f"# Opus 5 lead output\n\n"
        f"**Model:** `{args.model}`  \n"
        f"**Role:** sprint lead  \n"
        f"**Human:** ACCEPTED collaborator  \n\n---\n\n"
    )
    out_path.write_text(header + out + "\n")
    print(f"Wrote {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
