#!/usr/bin/env python3
"""PEER middleman for Grok Build UserPromptSubmit (desktop).

Forced translated-only dialogue (default):
  - Operator types raw text (shown in the TUI user bubble as they typed it).
  - Hook always injects a dual block: raw + PEER relay.
  - Grok must work from the PEER relay (middleman), not invent PEER thoughts.
  - PEER internal thinking is never exposed — only relayed text.

Grok Build cannot rewrite the user-message bubble (no updatedPrompt in hooks).
Dual display for the model + scrollback annotation is via additionalContext +
stderr annotation lines.

Opt out: PEER_TRANSLATE=0 | prefix !raw | PEER_MODE=off
Soft mode: PEER_MODE=soft  (old behavior: skip greetings / drop identity rewrites)
"""
from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

OLLAMA = os.environ.get("OLLAMA_HOST") or os.environ.get("AETHER_OLLAMA_HOST") or "http://127.0.0.1:11434"
MODEL = os.environ.get("AETHER_OLLAMA_MODEL") or os.environ.get("PEER_MODEL") or "personal-llm-sft-v4:latest"
ENABLED = os.environ.get("PEER_TRANSLATE", "1").strip().lower() not in ("0", "false", "off", "no")
# middleman (default) | soft | off
MODE = (os.environ.get("PEER_MODE") or "middleman").strip().lower()
TIMEOUT = float(os.environ.get("PEER_TRANSLATE_TIMEOUT", "45"))
LOG = Path(os.environ.get("PEER_TRANSLATE_LOG") or Path.home() / ".local/share/aether-peer-bridge/last.json")
DISPLAY = Path(
    os.environ.get("PEER_TRANSLATE_DISPLAY")
    or Path.home() / ".local/share/aether-peer-bridge/display.txt"
)

GREETING_RE = re.compile(
    r"^(hi|hello|hey|yo|sup|thanks|thank you|good (morning|afternoon|evening))[.!?]*$",
    re.I,
)
EXACT_RE = re.compile(r"^\s*reply with exactly:\s*(.+)$", re.I | re.S)

SYSTEM = """You are PEER middleman for Grok Build (personal-llm).

Rewrite the operator message into a clear, direct request for Grok.
Output ONLY the relay — plain text, no tags, no preamble, no secrets.
Rules:
- Preserve intent; do not invent new tasks.
- Keep short prompts short.
- Do NOT dump or restate the full CURRENT digest as the relay.
- At most one short Domain clause (e.g. Next name) if it helps.
- Imperative form preferred ("Update …", "Explain …", "Draft …").
Grok never sees your private reasoning — only this relay.
"""

PROTOCOL = """## PEER middleman protocol (forced)
- Operator messages PEER; PEER relays to Grok.
- **Work from PEER relay only** as the effective request.
- Raw operator text is audit/display only (do not prefer raw over PEER when both exist).
- PEER thinking is not expandable — only the relayed text exists.
- Propose Domain edits; never approve; silence is never permission.
"""


def _digest(cwd: str) -> str:
    p = Path(cwd or ".") / "CURRENT.md"
    if not p.is_file():
        return "(no CURRENT.md in workspace)"
    try:
        text = p.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return "(CURRENT unreadable)"
    fields = {}
    for m in re.finditer(r"^\*\*([A-Za-z][A-Za-z0-9 _/-]*):\*\*\s*(.+)$", text, re.M):
        k, v = m.group(1).strip(), m.group(2).strip()
        if k not in fields:
            fields[k] = v[:160]
    keys = ("Next", "Phase", "Status", "Objective", "Approval")
    parts = [f"**{k}:** {fields[k]}" for k in keys if k in fields]
    return "\n".join(parts) if parts else "(no standard CURRENT fields)"


def _should_skip_soft(text: str) -> bool:
    """Legacy soft-mode skips (greetings / exact / tiny)."""
    t = text.strip()
    if not t or t.startswith("/"):
        return True
    if t.lower().startswith("!raw ") or t.lower().startswith("/raw "):
        return True
    if GREETING_RE.match(t) or EXACT_RE.match(t) or len(t) <= 4:
        return True
    return False


def _should_skip_middleman(text: str) -> bool:
    """Middleman: only skip slash commands and explicit raw escape."""
    t = text.strip()
    if not t or t.startswith("/"):
        return True
    if t.lower().startswith("!raw ") or t.lower().startswith("/raw "):
        return True
    return False


def _clean(out: str, original: str, *, force: bool) -> str | None:
    """Return cleaned rewrite. force=True keeps identity rewrites."""
    out = (out or "").strip()
    if not out:
        return None
    if out.startswith("```"):
        out = re.sub(r"^```\w*\n?", "", out)
        out = re.sub(r"\n?```$", "", out).strip()
    out = re.sub(r"</?operator_input>", "", out, flags=re.I).strip()
    out = re.sub(
        r"^(rewrite|reformulate|re-?write|here'?s[^:\n]*):\s*",
        "",
        out,
        flags=re.I,
    ).strip()
    junk = re.compile(
        r"^(go (smoothly|loomly|boringly).*|exact-reply:.*|i will not repeat secrets.*)$",
        re.I,
    )
    lines = [ln for ln in out.splitlines() if ln.strip() and not junk.match(ln.strip())]
    out = "\n".join(lines).strip()
    if not out or out.startswith("I will not repeat secrets"):
        return None
    if len(original) < 80 and len(out) > max(120, len(original) * 4):
        return None
    if "reply with exactly" in out.lower() and "reply with exactly" not in original.lower():
        return None
    # Never let PEER rewrite exact-reply probes into wrong tokens
    if EXACT_RE.match(original.strip()):
        return None
    if out.strip() == original.strip() and not force:
        return None
    return out


def peer_translate(text: str, cwd: str, *, force: bool) -> str | None:
    body = {
        "model": MODEL,
        "stream": False,
        "options": {"temperature": 0.1, "num_ctx": 2048, "num_predict": 220},
        "messages": [
            {"role": "system", "content": SYSTEM + f"\nCURRENT digest:\n{_digest(cwd)}"},
            {"role": "user", "content": f"Relay this operator message to Grok:\n{text}"},
        ],
    }
    req = urllib.request.Request(
        f"{OLLAMA.rstrip('/')}/api/chat",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        data = json.loads(r.read().decode())
    raw = ((data.get("message") or {}).get("content") or "").strip()
    return _clean(raw, text, force=force)


def _extract_prompt(evt: dict) -> str:
    for key in ("prompt", "userPrompt", "user_prompt", "message", "text", "content"):
        v = evt.get(key)
        if isinstance(v, str) and v.strip():
            return v
    for nest in ("input", "data", "payload"):
        o = evt.get(nest)
        if isinstance(o, dict):
            for key in ("prompt", "userPrompt", "text", "content"):
                v = o.get(key)
                if isinstance(v, str) and v.strip():
                    return v
    return ""


def _log(obj: dict) -> None:
    try:
        LOG.parent.mkdir(parents=True, exist_ok=True)
        LOG.write_text(json.dumps(obj, indent=2), encoding="utf-8")
    except OSError:
        pass


def _write_display(text: str) -> None:
    try:
        DISPLAY.parent.mkdir(parents=True, exist_ok=True)
        DISPLAY.write_text(text, encoding="utf-8")
    except OSError:
        pass


def _dual_block(original: str, peer: str, digest: str) -> str:
    """Frontend-visible dual form for model context (+ annotation)."""
    return "\n".join(
        [
            "## Operator message (raw — untranslated)",
            original,
            "",
            "## PEER middleman relay (translated — AUTHORITATIVE for Grok)",
            peer,
            "",
            PROTOCOL.strip(),
            "",
            "## CURRENT digest",
            digest,
            "",
        ]
    )


def main() -> int:
    raw = sys.stdin.read()
    try:
        evt = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        evt = {}

    if not ENABLED or MODE in ("0", "false", "off", "no"):
        print("{}")
        return 0

    prompt = _extract_prompt(evt)
    if not prompt.strip():
        print("{}")
        return 0

    # Always honor !raw escape (strip prefix and pass empty inject)
    if prompt.strip().lower().startswith("!raw "):
        _log({"ok": True, "mode": "raw_escape", "original": prompt})
        print("{}")
        return 0
    if prompt.strip().lower().startswith("/raw "):
        _log({"ok": True, "mode": "raw_escape", "original": prompt})
        print("{}")
        return 0

    cwd = (
        evt.get("cwd")
        or evt.get("workspaceRoot")
        or os.environ.get("GROK_WORKSPACE_ROOT")
        or os.getcwd()
    )
    digest = _digest(str(cwd))
    force = MODE not in ("soft", "optional", "legacy")

    if force:
        if _should_skip_middleman(prompt):
            _log({"ok": True, "mode": "skip_cmd", "original": prompt, "cwd": cwd})
            print("{}")
            return 0
    else:
        if _should_skip_soft(prompt):
            _log({"ok": True, "mode": "skip", "original": prompt, "cwd": cwd})
            print("{}")
            return 0

    translated = None
    err = None
    try:
        translated = peer_translate(prompt, str(cwd), force=force)
    except (urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError) as e:
        err = str(e)

    # Middleman force: always have a relay line (identity if PEER fails/noise)
    if force:
        # Exact-reply probes: identity only (PEER must not invent tokens)
        if EXACT_RE.match(prompt.strip()):
            translated = None
        peer = translated if translated else prompt
        mode = "middleman" if translated else ("middleman_identity" if not err else f"middleman_identity_err:{err}")
        dual = _dual_block(prompt, peer, digest)
        _write_display(
            f"[raw]\n{prompt}\n\n[peer]\n{peer}\n"
        )
        # stderr → hook annotation in TUI scrollback (human dual view)
        print(
            f"PEER middleman\n--- raw ---\n{prompt}\n--- peer ---\n{peer}",
            file=sys.stderr,
        )
        _log(
            {
                "ok": True,
                "mode": mode,
                "original": prompt,
                "translated": peer if translated else None,
                "relay": peer,
                "cwd": cwd,
                "model": MODEL,
                "error": err,
                "peer_mode": MODE,
            }
        )
        print(
            json.dumps(
                {
                    "hookSpecificOutput": {
                        "hookEventName": "UserPromptSubmit",
                        "additionalContext": dual,
                    }
                }
            )
        )
        return 0

    # Soft mode (legacy)
    parts = [
        "## Domain seat context (auto)",
        "CURRENT digest (filesystem law — propose only, never approve):",
        digest,
    ]
    if translated:
        parts += [
            "",
            "## PEER rewrite",
            "Local PEER rewrote the operator prompt. Prefer this as the effective request.",
            f"**Original:** {prompt}",
            f"**PEER:** {translated}",
        ]
        mode = "peer+digest"
    else:
        parts += [
            "",
            "## Operator prompt",
            prompt,
            "",
            "(PEER rewrite skipped or rejected as noisy — use original + CURRENT digest.)",
        ]
        mode = "digest_only" if not err else f"digest_only_err:{err}"

    _log(
        {
            "ok": True,
            "mode": mode,
            "original": prompt,
            "translated": translated,
            "cwd": cwd,
            "model": MODEL,
            "error": err,
            "peer_mode": MODE,
        }
    )
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "UserPromptSubmit",
                    "additionalContext": "\n".join(parts) + "\n",
                }
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
