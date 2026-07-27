#!/usr/bin/env python3
"""Shared LLM plumbing for aether garden + rival editor.

Priority:
  1. ANTHROPIC_API_KEY (or ~/.config/anthropic/api_key) → Anthropic Messages API
  2. XAI_API_KEY → https://api.x.ai/v1 (OpenAI-compatible chat)
  3. Local Ollama → http://127.0.0.1:11434
  4. None → callers handle

Doctrine: no hidden DBs; keys only from env/files; stdlib only.
Env:
  ANTHROPIC_API_KEY, ANTHROPIC_MODEL / AETHER_MODEL (default claude-sonnet-5)
  XAI_API_KEY, AETHER_MODEL (default grok-4.5 when xai)
  AETHER_OLLAMA_HOST, AETHER_OLLAMA_MODEL
  AETHER_LLM_TIMEOUT (seconds, default 120)
  AETHER_LLM_PROVIDER=anthropic|xai|ollama  # force
  AETHER_PERSONAL_LLM_SYSTEM=1  # prepend references/personal-llm-system.txt if no system msg
"""
from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


# User-requested model set (aliases → API IDs)
MODEL_ALIASES = {
    "haiku": "claude-haiku-4-5",
    "haiku-4.5": "claude-haiku-4-5",
    "claude-haiku": "claude-haiku-4-5",
    "sonnet-4.6": "claude-sonnet-4-6",
    "sonnet4.6": "claude-sonnet-4-6",
    "claude-sonnet-4.6": "claude-sonnet-4-6",
    "sonnet-5": "claude-sonnet-5",
    "sonnet5": "claude-sonnet-5",
    "sonnet": "claude-sonnet-5",
}

# Prefer personal Mechanicall propose layer when local Ollama has it.
# Order = pick preference (first match wins).
OLLAMA_PREFER = (
    "personal-llm-sft-v2",
    "personal-llm-full:v1",
    "personal-llm-full",
    "personal-llm-pilot:v0",
    "personal-llm-pilot",
    "aetherOS-custom",
    "anti-clown",
    "llama",
    "mistral",
    "qwen",
)

# Soft outer guard: substrings that must never be auto-executed by callers.
# (Callers still own tool policy; this is a documentation helper + optional strip.)
UNSAFE_CMD_RE = re.compile(
    r"(?im)^\s*(?:aether\s+approve|cryptsetup\s+|sudo\s+cryptsetup)\b"
)
SECRET_LIKE_RE = re.compile(
    r"(?i)\b(sk-[a-z0-9_-]{10,}|sk-proj-[a-z0-9_-]{8,}|BEGIN (?:RSA |OPENSSH )?PRIVATE KEY)\b"
)


@dataclass
class LLMBackend:
    name: str  # anthropic | xai | ollama
    model: str
    base: str


def timeout() -> float:
    try:
        return float(os.environ.get("AETHER_LLM_TIMEOUT", "120"))
    except ValueError:
        return 120.0


def _anthropic_key() -> str:
    key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if key:
        return key
    path = Path.home() / ".config" / "anthropic" / "api_key"
    if path.is_file():
        return path.read_text().strip()
    return ""


def _resolve_model(default: str) -> str:
    raw = (
        os.environ.get("AETHER_MODEL")
        or os.environ.get("ANTHROPIC_MODEL")
        or default
    ).strip()
    return MODEL_ALIASES.get(raw.lower(), raw)


def resolve_backend() -> Optional[LLMBackend]:
    force = os.environ.get("AETHER_LLM_PROVIDER", "").strip().lower()

    def anthropic() -> Optional[LLMBackend]:
        if not _anthropic_key():
            return None
        model = _resolve_model("claude-sonnet-5")
        return LLMBackend("anthropic", model, "https://api.anthropic.com")

    def xai() -> Optional[LLMBackend]:
        if not os.environ.get("XAI_API_KEY", "").strip():
            return None
        model = os.environ.get("AETHER_MODEL", "grok-4.5").strip() or "grok-4.5"
        # if model is a claude alias while on xai, fall back
        if model.startswith("claude") or model in MODEL_ALIASES:
            model = "grok-4.5"
        return LLMBackend("xai", model, "https://api.x.ai/v1")

    def ollama() -> Optional[LLMBackend]:
        host = os.environ.get("AETHER_OLLAMA_HOST", "http://127.0.0.1:11434").rstrip("/")
        model = os.environ.get("AETHER_OLLAMA_MODEL", "").strip()
        if not model:
            model = _ollama_pick_model(host) or "aetherOS-custom"
        if _ollama_up(host):
            return LLMBackend("ollama", model, host)
        return None

    if force == "anthropic":
        return anthropic()
    if force == "xai":
        return xai()
    if force == "ollama":
        return ollama()

    return anthropic() or xai() or ollama()


def _ollama_up(host: str) -> bool:
    try:
        req = urllib.request.Request(f"{host}/api/tags", method="GET")
        with urllib.request.urlopen(req, timeout=2.0) as resp:
            return 200 <= resp.status < 300
    except Exception:
        return False


def _ollama_pick_model(host: str) -> Optional[str]:
    try:
        req = urllib.request.Request(f"{host}/api/tags", method="GET")
        with urllib.request.urlopen(req, timeout=2.0) as resp:
            data = json.loads(resp.read().decode())
        names = [m.get("name", "") for m in data.get("models", []) if m.get("name")]
        return pick_ollama_model(names)
    except Exception:
        return None


def pick_ollama_model(names: list[str]) -> Optional[str]:
    """Pure pick: prefer personal-llm tags, then legacy aether customs.

    Exported for unit tests (no network).
    """
    if not names:
        return None
    lower_map = {n.lower(): n for n in names}
    # exact / prefix prefer list
    for p in OLLAMA_PREFER:
        pl = p.lower()
        for n in names:
            nl = n.lower()
            if nl == pl or nl.startswith(pl + ":") or pl in nl:
                return n
        # also try bare match against lower_map keys
        if pl in lower_map:
            return lower_map[pl]
    return names[0]


def personal_llm_system_text() -> str:
    """Load repo doctrine SYSTEM for the personal propose layer."""
    # aether_llm.py lives in python/ → repo root is parent
    root = Path(__file__).resolve().parent.parent
    path = root / "references" / "personal-llm-system.txt"
    if path.is_file():
        return path.read_text(encoding="utf-8").strip()
    return (
        "You propose only. Never run aether approve. Silence is never permission. "
        "Filesystem is truth. CURRENT.md is authority."
    )


def maybe_inject_personal_system(messages: list[dict[str, str]]) -> list[dict[str, str]]:
    """If AETHER_PERSONAL_LLM_SYSTEM is set and no system msg, prepend doctrine."""
    flag = os.environ.get("AETHER_PERSONAL_LLM_SYSTEM", "").strip().lower()
    if flag not in ("1", "true", "yes", "on"):
        return messages
    if any(m.get("role") == "system" for m in messages):
        return messages
    return [{"role": "system", "content": personal_llm_system_text()}, *messages]


def flag_unsafe_model_output(text: str) -> list[str]:
    """Return human-readable flags for outer tool policy (never auto-exec)."""
    flags: list[str] = []
    if UNSAFE_CMD_RE.search(text or ""):
        flags.append("unsafe_cmd_suggest")
    if SECRET_LIKE_RE.search(text or ""):
        flags.append("secret_like")
    return flags


def chat(messages: list[dict[str, str]], *, temperature: float = 0.7) -> str:
    """messages: [{role, content}, ...] → assistant text."""
    backend = resolve_backend()
    if not backend:
        raise RuntimeError(
            "no LLM backend: set ANTHROPIC_API_KEY (or import via "
            "~/exports/import-anthropic-key.sh), XAI_API_KEY, or start Ollama"
        )
    messages = maybe_inject_personal_system(messages)
    if backend.name == "anthropic":
        return _anthropic_chat(backend, messages, temperature)
    if backend.name == "xai":
        return _openai_chat(backend, messages, temperature)
    return _ollama_chat(backend, messages, temperature)


def describe_backend() -> str:
    b = resolve_backend()
    if not b:
        return "none (ANTHROPIC_API_KEY / XAI_API_KEY / ollama)"
    return f"{b.name}:{b.model}"


def _anthropic_chat(backend: LLMBackend, messages: list[dict[str, str]], temperature: float) -> str:
    key = _anthropic_key()
    system = ""
    chat_msgs = []
    for m in messages:
        role = m.get("role", "user")
        content = m.get("content", "")
        if role == "system":
            system = (system + "\n" + content).strip() if system else content
        else:
            chat_msgs.append({"role": role if role in ("user", "assistant") else "user", "content": content})
    if not chat_msgs:
        chat_msgs = [{"role": "user", "content": "ping"}]
    body_obj: dict = {
        "model": backend.model,
        "max_tokens": 2048,
        "messages": chat_msgs,
    }
    # Newer Claude models (Sonnet 5+) reject temperature; omit for all Anthropic.
    # (temperature param kept in signature for xai/ollama callers.)
    _ = temperature
    if system:
        body_obj["system"] = system
    body = json.dumps(body_obj).encode()
    req = urllib.request.Request(
        f"{backend.base}/v1/messages",
        data=body,
        headers={
            "x-api-key": key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout()) as resp:
            data = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        err = e.read().decode(errors="replace")[:400]
        raise RuntimeError(f"Anthropic HTTP {e.code}: {err}") from e
    parts = data.get("content") or []
    texts = [p.get("text", "") for p in parts if p.get("type") == "text"]
    out = "\n".join(t for t in texts if t).strip()
    if not out:
        raise RuntimeError(f"Anthropic empty response: {str(data)[:300]}")
    return out


def _openai_chat(backend: LLMBackend, messages: list[dict[str, str]], temperature: float) -> str:
    key = os.environ["XAI_API_KEY"].strip()
    body = json.dumps(
        {
            "model": backend.model,
            "messages": messages,
            "temperature": temperature,
        }
    ).encode()
    req = urllib.request.Request(
        f"{backend.base}/chat/completions",
        data=body,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout()) as resp:
            data = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        err = e.read().decode(errors="replace")[:400]
        raise RuntimeError(f"xAI HTTP {e.code}: {err}") from e
    choices = data.get("choices") or []
    if not choices:
        raise RuntimeError(f"xAI empty response: {data!r}"[:300])
    return (choices[0].get("message") or {}).get("content", "").strip()


def _ollama_chat(backend: LLMBackend, messages: list[dict[str, str]], temperature: float) -> str:
    body = json.dumps(
        {
            "model": backend.model,
            "messages": messages,
            "stream": False,
            "options": {"temperature": temperature},
        }
    ).encode()
    req = urllib.request.Request(
        f"{backend.base}/api/chat",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout()) as resp:
            data = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        err = e.read().decode(errors="replace")[:400]
        raise RuntimeError(f"ollama HTTP {e.code}: {err}") from e
    msg = data.get("message") or {}
    text = (msg.get("content") or data.get("response") or "").strip()
    if not text:
        raise RuntimeError(f"ollama empty response from {backend.model}")
    return text


if __name__ == "__main__":
    print(describe_backend())
