#!/usr/bin/env python3
"""Unit tests for personal-llm Ollama preference (no network)."""
from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "python"))

from aether_llm import (  # noqa: E402
    flag_unsafe_model_output,
    maybe_inject_personal_system,
    personal_llm_system_text,
    pick_ollama_model,
    resolve_backend,
)


def test_prefer_sft_v4():
    names = [
        "llama3:latest",
        "personal-llm-sft-v2:latest",
        "personal-llm-sft-v4:latest",
        "aetherOS-custom:latest",
    ]
    assert pick_ollama_model(names).startswith("personal-llm-sft-v4")


def test_prefer_sft_v2_when_no_v4():
    names = ["llama3:latest", "personal-llm-sft-v2:latest", "aetherOS-custom:latest"]
    assert pick_ollama_model(names).startswith("personal-llm-sft-v2")


def test_prefer_full_v1_over_custom():
    names = ["aetherOS-custom:latest", "personal-llm-full:v1"]
    assert pick_ollama_model(names) == "personal-llm-full:v1"


def test_prefer_pilot_over_generic():
    names = ["mistral:latest", "personal-llm-pilot:v0"]
    assert pick_ollama_model(names) == "personal-llm-pilot:v0"


def test_fallback_first_name():
    names = ["foo:latest", "bar:latest"]
    assert pick_ollama_model(names) == "foo:latest"


def test_empty():
    assert pick_ollama_model([]) is None


def test_system_file_exists():
    text = personal_llm_system_text()
    assert "aether approve" in text
    assert "Silence is never permission" in text


def test_inject_system():
    os.environ["AETHER_PERSONAL_LLM_SYSTEM"] = "1"
    try:
        out = maybe_inject_personal_system([{"role": "user", "content": "hi"}])
        assert out[0]["role"] == "system"
        assert "CURRENT.md" in out[0]["content"]
        # do not double-inject
        out2 = maybe_inject_personal_system(out)
        assert sum(1 for m in out2 if m["role"] == "system") == 1
    finally:
        os.environ.pop("AETHER_PERSONAL_LLM_SYSTEM", None)


def test_flag_unsafe():
    flags = flag_unsafe_model_output("run:\naether approve keep\n")
    assert "unsafe_cmd_suggest" in flags
    flags2 = flag_unsafe_model_output("here is sk-proj-ABCDEFGHIJKL")
    assert "secret_like" in flags2


def test_openai_compat_from_base_url():
    prev = {k: os.environ.get(k) for k in (
        "AETHER_LLM_PROVIDER", "AETHER_OPENAI_BASE_URL", "AETHER_MODEL", "OPENAI_API_KEY",
        "OPENROUTER_API_KEY", "GROQ_API_KEY", "ANTHROPIC_API_KEY", "XAI_API_KEY",
    )}
    try:
        for k in prev:
            os.environ.pop(k, None)
        os.environ["AETHER_LLM_PROVIDER"] = "openai"
        os.environ["AETHER_OPENAI_BASE_URL"] = "http://127.0.0.1:8000/v1"
        os.environ["AETHER_MODEL"] = "moonshotai/Kimi-K2-Instruct-0905"
        b = resolve_backend()
        assert b is not None
        assert b.name == "openai"
        assert b.base.endswith("/v1")
        assert "Kimi" in b.model
    finally:
        for k, v in prev.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v


def main() -> int:
    tests = [
        test_prefer_sft_v4,
        test_prefer_sft_v2_when_no_v4,
        test_prefer_full_v1_over_custom,
        test_prefer_pilot_over_generic,
        test_fallback_first_name,
        test_empty,
        test_system_file_exists,
        test_inject_system,
        test_flag_unsafe,
        test_openai_compat_from_base_url,
    ]
    for t in tests:
        t()
        print(f"ok: {t.__name__}")
    print("all personal-llm unit tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
