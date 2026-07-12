#!/usr/bin/env python3
"""Shared LLM plumbing for aether garden + rival editor.

Priority:
  1. XAI_API_KEY → https://api.x.ai/v1 (OpenAI-compatible chat)
  2. Local Ollama → http://127.0.0.1:11434
  3. None → callers handle

Doctrine: no hidden DBs; keys only from env; stdlib only.
Env:
  XAI_API_KEY, AETHER_MODEL (default grok-4.5)
  AETHER_OLLAMA_HOST (default http://127.0.0.1:11434)
  AETHER_OLLAMA_MODEL (default aetherOS-custom, then first tag)
  AETHER_LLM_TIMEOUT (seconds, default 120)
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Optional


@dataclass
class LLMBackend:
    name: str  # xai | ollama
    model: str
    base: str


def timeout() -> float:
    try:
        return float(os.environ.get("AETHER_LLM_TIMEOUT", "120"))
    except ValueError:
        return 120.0


def resolve_backend() -> Optional[LLMBackend]:
    key = os.environ.get("XAI_API_KEY", "").strip()
    if key:
        model = os.environ.get("AETHER_MODEL", "grok-4.5").strip() or "grok-4.5"
        return LLMBackend("xai", model, "https://api.x.ai/v1")

    host = os.environ.get("AETHER_OLLAMA_HOST", "http://127.0.0.1:11434").rstrip("/")
    model = os.environ.get("AETHER_OLLAMA_MODEL", "").strip()
    if not model:
        model = _ollama_pick_model(host) or "aetherOS-custom"
    if _ollama_up(host):
        return LLMBackend("ollama", model, host)
    return None


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
        prefer = ("aetherOS-custom", "anti-clown", "llama", "mistral", "qwen")
        for p in prefer:
            for n in names:
                if p in n:
                    return n
        return names[0] if names else None
    except Exception:
        return None


def chat(messages: list[dict[str, str]], *, temperature: float = 0.7) -> str:
    """messages: [{role, content}, ...] → assistant text."""
    backend = resolve_backend()
    if not backend:
        raise RuntimeError(
            "no LLM backend: set XAI_API_KEY (https://console.x.ai) "
            "or start Ollama (ollama serve) with a chat model"
        )
    if backend.name == "xai":
        return _openai_chat(backend, messages, temperature)
    return _ollama_chat(backend, messages, temperature)


def describe_backend() -> str:
    b = resolve_backend()
    if not b:
        return "none (set XAI_API_KEY or start ollama)"
    return f"{b.name}:{b.model}"


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
