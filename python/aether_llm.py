#!/usr/bin/env python3
"""Shared LLM plumbing for aether garden, rival, desk, and shell.

Priority (first available wins unless AETHER_LLM_PROVIDER forces one):
  0. grok_tui — Grok Build CLI (`grok -p`) with `grok login` session (preferred Grok compute)
  1. OPENROUTER_API_KEY → free-tier multi-provider (no card for free models)
  2. GROQ_API_KEY → free frontier-class open weights (fast)
  3. ANTHROPIC_API_KEY (or ~/.config/anthropic/api_key)
  4. XAI_API_KEY → api.x.ai (raw API compute; ranked below Grok TUI)
  5. Local Ollama → http://127.0.0.1:11434
  6. None → callers handle

Doctrine: no hidden DBs; keys only from env/files; stdlib only.
  Grok TUI session lives in ~/.grok/auth.json (from `grok login`) — not XAI_API_KEY.

Env:
  AETHER_LLM_PROVIDER=grok_tui|openrouter|groq|anthropic|xai|ollama|openai
  GROK_BIN                 # path to grok CLI (default: which grok)
  AETHER_GROK_TUI=0        # disable auto-detect of Grok TUI backend
  AETHER_MODEL             # model id (default grok-4.5 for grok_tui / xai)
  OPENROUTER_API_KEY, GROQ_API_KEY, ANTHROPIC_API_KEY, XAI_API_KEY
  AETHER_OLLAMA_HOST, AETHER_OLLAMA_MODEL
  AETHER_LLM_TIMEOUT (seconds, default 120; grok_tui default 300)
  AETHER_OPENAI_BASE_URL, OPENAI_API_KEY
  AETHER_PERSONAL_LLM_SYSTEM=1
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import tempfile
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
    # Claude 3.5 family (Anthropic direct or OpenRouter)
    "sonnet-3.5": "claude-3-5-sonnet-latest",
    "sonnet35": "claude-3-5-sonnet-latest",
    "claude-3.5-sonnet": "claude-3-5-sonnet-latest",
    "claude-3-5-sonnet": "claude-3-5-sonnet-latest",
    "sonnet-3.5-or": "anthropic/claude-3.5-sonnet",
    "coding": "openrouter/free",  # resolved further by preset
    "free": "openrouter/free",
}

# Toggleable compute presets (shell/panel cycle). Order = free coding → paid-ish → local.
# Each: (provider, default_model, short blurb)
# OpenRouter free slugs change; pin via AETHER_MODEL or /model after selecting preset.
LLM_PRESETS: dict[str, tuple[str, str, str]] = {
    "free": (
        "openrouter",
        "openrouter/free",
        "OpenRouter free router (any free model)",
    ),
    "coding": (
        "openrouter",
        "qwen/qwen3-coder:free",
        "OpenRouter free coding (Qwen3 Coder)",
    ),
    "coding_alt": (
        "openrouter",
        "agentica-org/deepcoder-14b-preview:free",
        "OpenRouter free coding alt (DeepCoder 14B)",
    ),
    "llama_free": (
        "openrouter",
        "meta-llama/llama-3.3-70b-instruct:free",
        "OpenRouter free Llama 3.3 70B",
    ),
    "groq": (
        "groq",
        "llama-3.3-70b-versatile",
        "Groq free-tier open weights (fast)",
    ),
    "sonnet35": (
        "openrouter",
        "anthropic/claude-3.5-sonnet",
        "Claude 3.5 Sonnet via OpenRouter (may need credits)",
    ),
    "sonnet35_direct": (
        "anthropic",
        "claude-3-5-sonnet-latest",
        "Claude 3.5 Sonnet via Anthropic API key",
    ),
    "sonnet": (
        "anthropic",
        "claude-sonnet-5",
        "Claude Sonnet 5 via Anthropic API key",
    ),
    "grok_tui": (
        "grok_tui",
        "grok-4.5",
        "Grok Build TUI session (preferred Grok compute)",
    ),
    "xai": (
        "xai",
        "grok-4.5",
        "Raw xAI API (XAI_API_KEY; below TUI)",
    ),
    "ollama": (
        "ollama",
        "",  # auto-pick personal-llm / first tag
        "Ollama personal-llm (this host or AETHER_OLLAMA_HOST LAN/Tailscale)",
    ),
}

# Cycle order for /provider next (free coding first → sonnet → ollama → grok)
PRESET_CYCLE: tuple[str, ...] = (
    "coding",
    "coding_alt",
    "free",
    "llama_free",
    "groq",
    "sonnet35",
    "sonnet35_direct",
    "sonnet",
    "ollama",
    "grok_tui",
    "xai",
)

# Alias names → canonical preset id
# Do NOT map real provider ids (openrouter, anthropic, ollama, …) here —
# resolve_backend would re-apply them and clobber a specific preset (e.g. coding).
PRESET_ALIASES: dict[str, str] = {
    "or": "free",
    "or-free": "free",
    "or_free": "free",
    "code": "coding",
    "coder": "coding",
    "qwen": "coding",
    "deepcoder": "coding_alt",
    "llama": "llama_free",
    "claude35": "sonnet35",
    "claude-3.5": "sonnet35",
    "claude-3.5-sonnet": "sonnet35",
    "3.5": "sonnet35",
    "sonnet-3.5": "sonnet35",
    "sonnet3.5": "sonnet35",
    "anthropic-35": "sonnet35_direct",
    "local": "ollama",
    "personal": "ollama",
    "personal-llm": "ollama",
    "grok": "grok_tui",
    "tui": "grok_tui",
    "api": "xai",
    "xai-api": "xai",
}

# Valid AETHER_LLM_PROVIDER values (not presets)
_PROVIDER_IDS = frozenset(
    {"grok_tui", "openrouter", "groq", "anthropic", "xai", "ollama", "openai"}
)

# Prefer personal Mechanicall propose layer when local Ollama has it.
# Order = pick preference (first match wins).
OLLAMA_PREFER = (
    "personal-llm-sft-v4",
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
    name: str  # grok_tui | openrouter | groq | anthropic | xai | ollama | openai
    model: str
    base: str
    api_key_env: str = ""  # env var name for OpenAI-compatible auth


def timeout() -> float:
    try:
        return float(os.environ.get("AETHER_LLM_TIMEOUT", "120"))
    except ValueError:
        return 120.0


def grok_tui_bin() -> Optional[str]:
    env = os.environ.get("GROK_BIN", "").strip()
    if env and Path(env).is_file():
        return env
    return shutil.which("grok")


def grok_tui_auth_path() -> Path:
    home = Path(os.environ.get("GROK_HOME", str(Path.home() / ".grok")))
    return home / "auth.json"



# Last headless Grok turn meta (thinking, usage) — for panel display
_LAST_CHAT_META: dict = {}


def last_chat_meta() -> dict:
    """Return meta from the most recent chat() call (thinking, model, usage)."""
    return dict(_LAST_CHAT_META)


def clear_chat_meta() -> None:
    _LAST_CHAT_META.clear()

def grok_tui_available() -> bool:
    """True when Grok CLI is installed and a TUI/session login is present.

    XAI_API_KEY alone does **not** count — that is raw API compute, ranked lower.
    """
    flag = os.environ.get("AETHER_GROK_TUI", "1").strip().lower()
    if flag in ("0", "false", "no", "off"):
        return False
    if not grok_tui_bin():
        return False
    auth = grok_tui_auth_path()
    try:
        return auth.is_file() and auth.stat().st_size > 32
    except OSError:
        return False


def _anthropic_key() -> str:
    key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if key:
        return key
    path = Path.home() / ".config" / "anthropic" / "api_key"
    if path.is_file():
        return path.read_text().strip()
    return ""


def _env_key(*names: str) -> str:
    for n in names:
        v = os.environ.get(n, "").strip()
        if v:
            return v
    return ""


def _resolve_model(default: str) -> str:
    raw = (
        os.environ.get("AETHER_MODEL")
        or os.environ.get("ANTHROPIC_MODEL")
        or default
    ).strip()
    return MODEL_ALIASES.get(raw.lower(), raw)


def normalize_preset_name(name: str) -> str:
    n = (name or "").strip().lower().replace(" ", "_").replace("-", "_")
    if n in LLM_PRESETS:
        return n
    # allow sonnet_3_5 style
    n2 = n.replace("__", "_")
    if n2 in LLM_PRESETS:
        return n2
    return PRESET_ALIASES.get(n) or PRESET_ALIASES.get(n.replace("_", "-")) or n


def list_presets() -> list[tuple[str, str, str, str]]:
    """Return (id, provider, model, blurb) in cycle order."""
    out: list[tuple[str, str, str, str]] = []
    for pid in PRESET_CYCLE:
        if pid not in LLM_PRESETS:
            continue
        prov, model, blurb = LLM_PRESETS[pid]
        out.append((pid, prov, model or "(auto)", blurb))
    return out


def format_presets_help(current: Optional[str] = None) -> str:
    cur = current or current_preset_name() or ""
    lines = ["LLM presets (toggle with /provider <id> or /provider next):", ""]
    for pid, prov, model, blurb in list_presets():
        mark = "▶" if pid == cur else " "
        lines.append(f"  {mark} {pid:16} {prov:12} {model}")
        lines.append(f"      {blurb}")
    lines.append("")
    lines.append("Aliases: code, free, sonnet35, ollama/local, grok/tui, xai/api")
    lines.append("Env: AETHER_LLM_PRESET | AETHER_LLM_PROVIDER + AETHER_MODEL")
    return "\n".join(lines)


def current_preset_name() -> Optional[str]:
    """Best-effort match of env to a known preset id."""
    explicit = os.environ.get("AETHER_LLM_PRESET", "").strip().lower()
    if explicit:
        n = normalize_preset_name(explicit)
        if n in LLM_PRESETS:
            return n
    prov = os.environ.get("AETHER_LLM_PROVIDER", "").strip().lower()
    model = (
        os.environ.get("AETHER_MODEL") or os.environ.get("AETHER_OLLAMA_MODEL") or ""
    ).strip()
    if prov in ("grok", "grok-cli", "grok_cli", "tui"):
        prov = "grok_tui"
    # Exact model match first (coding vs free vs sonnet35 all share openrouter)
    if model:
        for pid in PRESET_CYCLE:
            p, m, _b = LLM_PRESETS[pid]
            if p == prov and m and model.lower() == m.lower():
                return pid
        if prov == "openrouter":
            ml = model.lower()
            if "coder" in ml or "deepcoder" in ml:
                return "coding" if "deepcoder" not in ml else "coding_alt"
            if "3.5" in ml or "3-5" in ml:
                return "sonnet35"
            if "llama" in ml:
                return "llama_free"
            if model == "openrouter/free" or ml.endswith("/free"):
                return "free"
    if prov == "ollama":
        return "ollama"
    if prov == "grok_tui":
        return "grok_tui"
    if prov == "xai":
        return "xai"
    if prov == "groq":
        return "groq"
    if prov == "anthropic":
        if model and ("3-5" in model or "3.5" in model):
            return "sonnet35_direct"
        return "sonnet"
    if prov == "openrouter":
        return "free"
    return None


def apply_preset(name: str, *, lock: bool = True) -> str:
    """Set env for preset. Returns human status line. Does not call the network."""
    pid = normalize_preset_name(name)
    if pid not in LLM_PRESETS:
        known = ", ".join(PRESET_CYCLE)
        raise ValueError(f"unknown preset {name!r} — try: {known}")
    prov, model, blurb = LLM_PRESETS[pid]
    os.environ["AETHER_LLM_PRESET"] = pid
    os.environ["AETHER_LLM_PROVIDER"] = prov
    if lock:
        os.environ["AETHER_SHELL_PROVIDER_LOCK"] = "1"
    if prov == "ollama":
        # leave AETHER_MODEL empty for ollama auto; optional pin via AETHER_OLLAMA_MODEL
        os.environ.pop("AETHER_MODEL", None)
        if model:
            os.environ["AETHER_OLLAMA_MODEL"] = model
    else:
        if model:
            os.environ["AETHER_MODEL"] = model
        # openrouter coding should not force anthropic model leftovers
        if prov == "openrouter":
            os.environ.pop("ANTHROPIC_MODEL", None)
    return f"preset={pid} provider={prov} model={model or '(auto)'} — {blurb}"


def cycle_preset(direction: int = 1) -> str:
    """Move to next/prev preset in PRESET_CYCLE. direction: +1 or -1."""
    order = list(PRESET_CYCLE)
    cur = current_preset_name()
    if cur in order:
        idx = order.index(cur)
    else:
        idx = -1 if direction > 0 else 0
    nxt = order[(idx + direction) % len(order)]
    return apply_preset(nxt)


def load_preset_from_project(root: Optional[Path] = None) -> Optional[str]:
    """If project has .aether/llm-preset, apply it (no lock unless file says lock)."""
    if root is None:
        root = Path(os.getcwd())
    path = Path(root) / ".aether" / "llm-preset"
    if not path.is_file():
        return None
    try:
        raw = path.read_text(encoding="utf-8", errors="replace").strip().splitlines()
    except OSError:
        return None
    if not raw:
        return None
    name = raw[0].strip()
    lock = True
    for line in raw[1:]:
        if line.strip().lower() in ("nolock", "no-lock", "lock=0"):
            lock = False
    try:
        return apply_preset(name, lock=lock)
    except ValueError:
        return None


def save_preset_to_project(root: Path, name: Optional[str] = None) -> Path:
    """Persist current (or named) preset to .aether/llm-preset."""
    pid = normalize_preset_name(name or current_preset_name() or "coding")
    if pid not in LLM_PRESETS:
        pid = "coding"
    aether = Path(root) / ".aether"
    aether.mkdir(parents=True, exist_ok=True)
    path = aether / "llm-preset"
    path.write_text(pid + "\n", encoding="utf-8")
    return path


def resolve_backend() -> Optional[LLMBackend]:
    # Honor project/env preset before free-for-all resolution when only PRESET set
    preset_only = os.environ.get("AETHER_LLM_PRESET", "").strip()
    if preset_only and not os.environ.get("AETHER_LLM_PROVIDER", "").strip():
        try:
            apply_preset(preset_only, lock=False)
        except ValueError:
            pass

    force = os.environ.get("AETHER_LLM_PROVIDER", "").strip().lower()
    # aliases for Grok TUI
    if force in ("grok", "grok-cli", "grok_cli", "tui"):
        force = "grok_tui"
        os.environ["AETHER_LLM_PROVIDER"] = "grok_tui"
    # If user passed a *preset* id as provider (e.g. coding), expand it.
    # Never re-expand real provider ids (openrouter/anthropic/…) via aliases.
    if force and force not in _PROVIDER_IDS:
        if force in LLM_PRESETS or force in PRESET_ALIASES:
            try:
                apply_preset(
                    force,
                    lock=bool(os.environ.get("AETHER_SHELL_PROVIDER_LOCK")),
                )
                force = os.environ.get("AETHER_LLM_PROVIDER", "").strip().lower()
            except ValueError:
                pass

    def grok_tui() -> Optional[LLMBackend]:
        if not grok_tui_available():
            return None
        model = os.environ.get("AETHER_MODEL", "grok-4.5").strip() or "grok-4.5"
        if model.startswith("claude") or model in MODEL_ALIASES:
            model = "grok-4.5"
        if model.startswith("openrouter"):
            model = "grok-4.5"
        return LLMBackend("grok_tui", model, "grok-cli")

    def openrouter() -> Optional[LLMBackend]:
        key = _env_key("OPENROUTER_API_KEY")
        if not key:
            return None
        # openrouter/free routes to a free model; or pin AETHER_MODEL
        model = _resolve_model("openrouter/free")
        return LLMBackend(
            "openrouter",
            model,
            "https://openrouter.ai/api/v1",
            api_key_env="OPENROUTER_API_KEY",
        )

    def groq() -> Optional[LLMBackend]:
        key = _env_key("GROQ_API_KEY")
        if not key:
            return None
        model = _resolve_model("llama-3.3-70b-versatile")
        return LLMBackend(
            "groq", model, "https://api.groq.com/openai/v1", api_key_env="GROQ_API_KEY"
        )

    def anthropic() -> Optional[LLMBackend]:
        if not _anthropic_key():
            return None
        model = _resolve_model("claude-sonnet-5")
        return LLMBackend("anthropic", model, "https://api.anthropic.com")

    def xai() -> Optional[LLMBackend]:
        """Raw api.x.ai via XAI_API_KEY — below Grok TUI in preference."""
        if not os.environ.get("XAI_API_KEY", "").strip():
            return None
        model = os.environ.get("AETHER_MODEL", "grok-4.5").strip() or "grok-4.5"
        # if model is a claude alias while on xai, fall back
        if model.startswith("claude") or model in MODEL_ALIASES:
            model = "grok-4.5"
        return LLMBackend("xai", model, "https://api.x.ai/v1", api_key_env="XAI_API_KEY")

    def ollama() -> Optional[LLMBackend]:
        # Prefer explicit host; project pin; OLLAMA_HOST; probe local + Tailscale.
        root = None
        try:
            cwd = Path.cwd()
            if (cwd / ".aether").is_dir() or (cwd / "CURRENT.md").is_file():
                root = cwd
        except OSError:
            root = None
        host = resolve_ollama_host(root)
        model = (
            os.environ.get("AETHER_OLLAMA_MODEL", "").strip()
            or os.environ.get("AETHER_MODEL", "").strip()
        )
        if not model:
            model = _ollama_pick_model(host) or "personal-llm-sft-v4"
        if _ollama_up(host):
            return LLMBackend("ollama", model, host)
        return None

    def openai_compat() -> Optional[LLMBackend]:
        """Local/remote OpenAI-compatible (vLLM, TGI, remote Kimi day)."""
        base = os.environ.get("AETHER_OPENAI_BASE_URL", "").strip().rstrip("/")
        if not base:
            return None
        model = _resolve_model("default")
        # Allow unauthenticated local tunnels (vLLM often needs any non-empty Bearer)
        if not os.environ.get("OPENAI_API_KEY", "").strip():
            os.environ["OPENAI_API_KEY"] = "local"
        return LLMBackend("openai", model, base, api_key_env="OPENAI_API_KEY")

    table = {
        "grok_tui": grok_tui,
        "openrouter": openrouter,
        "groq": groq,
        "anthropic": anthropic,
        "xai": xai,
        "ollama": ollama,
        "openai": openai_compat,
    }
    if force in table:
        return table[force]()

    # Explicit remote OpenAI-compat before free cloud when URL is set
    if os.environ.get("AETHER_OPENAI_BASE_URL", "").strip():
        b = openai_compat()
        if b:
            return b

    # Grok TUI (session) first among Grok paths; raw XAI API later
    return (
        grok_tui()
        or openrouter()
        or groq()
        or anthropic()
        or xai()
        or ollama()
    )


def _normalize_ollama_host(host: str) -> str:
    """Accept host:port, bare IP, or full URL → http(s)://… without trailing slash."""
    h = (host or "").strip().rstrip("/")
    if not h:
        return "http://127.0.0.1:11434"
    if h.startswith("http://") or h.startswith("https://"):
        return h
    # Ollama often uses OLLAMA_HOST=0.0.0.0:11434 for the *server* bind; clients need 127.0.0.1
    if h.startswith("0.0.0.0"):
        h = "127.0.0.1" + h[len("0.0.0.0") :]
    return "http://" + h


def ollama_host_file(root: Optional[Path] = None) -> Path:
    base = root or Path.cwd()
    return base / ".aether" / "ollama-host"


def read_project_ollama_host(root: Optional[Path] = None) -> str:
    p = ollama_host_file(root)
    if not p.is_file():
        return ""
    try:
        return p.read_text(encoding="utf-8").strip().splitlines()[0].strip()
    except (OSError, IndexError):
        return ""


def write_project_ollama_host(root: Path, host: str) -> Path:
    h = _normalize_ollama_host(host)
    d = root / ".aether"
    d.mkdir(parents=True, exist_ok=True)
    path = d / "ollama-host"
    path.write_text(h + "\n", encoding="utf-8")
    return path


def _tailscale_ips() -> list[str]:
    ips: list[str] = []
    try:
        r = subprocess.run(
            ["tailscale", "ip", "-4"],
            capture_output=True,
            text=True,
            timeout=3,
        )
        if r.returncode == 0:
            for line in (r.stdout or "").splitlines():
                ip = line.strip()
                if ip:
                    ips.append(ip)
    except (OSError, subprocess.TimeoutExpired):
        pass
    return ips


def ollama_host_candidates(root: Optional[Path] = None) -> list[str]:
    """Ordered hosts to try for personal-llm (local + remote/LAN/Tailscale)."""
    out: list[str] = []
    seen: set[str] = set()

    def add(h: str) -> None:
        n = _normalize_ollama_host(h)
        if n and n not in seen:
            seen.add(n)
            out.append(n)

    add(os.environ.get("AETHER_OLLAMA_HOST", ""))
    add(os.environ.get("AETHER_OLLAMA_REMOTE", ""))
    pin = read_project_ollama_host(root)
    if pin:
        add(pin)
    add(os.environ.get("OLLAMA_HOST", ""))
    add("http://127.0.0.1:11434")
    for ip in _tailscale_ips():
        add(f"http://{ip}:11434")
    # common LAN env pin
    lan = os.environ.get("AETHER_OLLAMA_LAN", "").strip()
    if lan:
        add(lan)
    return out


def resolve_ollama_host(root: Optional[Path] = None) -> str:
    """Pick first reachable Ollama host; set AETHER_OLLAMA_HOST. Prefer local then remote."""
    for host in ollama_host_candidates(root):
        if _ollama_up(host):
            os.environ["AETHER_OLLAMA_HOST"] = host
            return host
    # Fallback: preferred pin even if down (caller sees error later)
    cands = ollama_host_candidates(root)
    host = cands[0] if cands else "http://127.0.0.1:11434"
    os.environ["AETHER_OLLAMA_HOST"] = host
    return host


def apply_peer_backend(root: Optional[Path] = None, *, model: str = "personal-llm-sft-v4:latest") -> str:
    """Wire shell for peer agent: ollama + sft-v4 + resolved local/remote host."""
    os.environ["AETHER_LLM_PROVIDER"] = "ollama"
    os.environ["AETHER_SHELL_PROVIDER_LOCK"] = "1"
    os.environ["AETHER_OLLAMA_MODEL"] = model
    os.environ["AETHER_MODEL"] = model
    host = resolve_ollama_host(root)
    up = _ollama_up(host)
    return f"peer backend: ollama:{model} @ {host}  ({'up' if up else 'DOWN'})"


def personal_llm_serve_hints() -> str:
    """How to run peer REPL on THIS hardware + how remotes reach it (LAN/Tailscale)."""
    lines = [
        "personal-llm peer REPL — runs ON this host",
        "",
        "Local REPL (this machine):",
        "  aether shell . --provider ollama --model personal-llm-sft-v4",
        "  /agent peer",
        "",
        "Ollama must listen beyond loopback for LAN/Tailscale clients:",
        "  OLLAMA_HOST=0.0.0.0:11434 ollama serve   # or nix mechanicall.ollama.host",
        "  # currently many installs still bind 127.0.0.1 only — rebuild/remount if needed",
        "",
    ]
    # Local tags
    local = "http://127.0.0.1:11434"
    if _ollama_up(local):
        model = _ollama_pick_model(local) or "(no personal-llm tag)"
        lines.append(f"local API: {local}  model≈{model}")
    else:
        lines.append(f"local API: {local}  DOWN")
    # Advertise addresses
    addrs: list[str] = []
    try:
        r = subprocess.run(
            ["tailscale", "ip", "-4"],
            capture_output=True,
            text=True,
            timeout=3,
        )
        if r.returncode == 0:
            for line in (r.stdout or "").splitlines():
                ip = line.strip()
                if ip:
                    addrs.append(ip)
                    lines.append(f"Tailscale: http://{ip}:11434")
    except (OSError, subprocess.TimeoutExpired):
        pass
    try:
        import socket

        hostname = socket.gethostname()
        for info in socket.getaddrinfo(hostname, None, socket.AF_INET):
            ip = info[4][0]
            if ip and not ip.startswith("127."):
                addrs.append(ip)
    except OSError:
        pass
    # dedupe
    seen = set()
    for ip in addrs:
        if ip in seen:
            continue
        seen.add(ip)
        if not any(ip in ln for ln in lines):
            lines.append(f"LAN/other: http://{ip}:11434")
    lines.extend(
        [
            "",
            "Remote machine → this host's model:",
            "  export AETHER_OLLAMA_HOST=http://<tailscale-or-lan-ip>:11434",
            "  export AETHER_OLLAMA_MODEL=personal-llm-sft-v4",
            "  aether shell . --provider ollama",
            "",
            "Remote TTY → REPL process on this host:",
            "  ssh user@<tailscale-ip> -t 'cd <domain> && aether shell . --provider ollama --model personal-llm-sft-v4'",
        ]
    )
    return "\n".join(lines)


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
            "no LLM backend: run `grok login` (preferred Grok TUI compute), "
            "or set OPENROUTER_API_KEY / GROQ_API_KEY / ANTHROPIC_API_KEY / "
            "XAI_API_KEY, or start Ollama — see docs/FREE-API.md + docs/AETHER-SHELL.md"
        )
    messages = maybe_inject_personal_system(messages)
    _LAST_CHAT_META.clear()
    if backend.name == "grok_tui":
        return _grok_tui_chat(backend, messages, temperature)
    if backend.name == "anthropic":
        return _anthropic_chat(backend, messages, temperature)
    if backend.name in ("xai", "openrouter", "groq", "openai"):
        return _openai_chat(backend, messages, temperature)
    return _ollama_chat(backend, messages, temperature)


def describe_backend() -> str:
    b = resolve_backend()
    preset = current_preset_name()
    prefix = f"[{preset}] " if preset else ""
    if not b:
        return prefix + "none (grok_tui | openrouter free/coding | sonnet35 | ollama | …)"
    if b.name == "grok_tui":
        return prefix + f"grok_tui:{b.model} (Grok CLI session — preferred over XAI_API_KEY)"
    if b.name == "xai":
        return prefix + f"xai:{b.model} (raw API — below Grok TUI)"
    if b.name == "openrouter":
        return prefix + f"openrouter:{b.model}"
    if b.name == "ollama":
        return prefix + f"ollama:{b.model} @ {b.base}"
    return prefix + f"{b.name}:{b.model}"


def _messages_to_prompt_parts(
    messages: list[dict[str, str]],
) -> tuple[str, str]:
    """Split system vs user/assistant transcript for CLI backends."""
    system_parts: list[str] = []
    turns: list[str] = []
    for m in messages:
        role = (m.get("role") or "user").strip().lower()
        content = (m.get("content") or "").strip()
        if not content:
            continue
        if role == "system":
            system_parts.append(content)
        elif role == "assistant":
            turns.append(f"Assistant: {content}")
        else:
            turns.append(f"User: {content}")
    system = "\n\n".join(system_parts).strip()
    if not turns:
        user_blob = "ping"
    elif len(turns) == 1 and turns[0].startswith("User: "):
        user_blob = turns[0][6:]
    else:
        user_blob = (
            "Continue this conversation. Reply as the assistant only.\n\n"
            + "\n\n".join(turns)
        )
    return system, user_blob


def _grok_tui_chat(
    backend: LLMBackend, messages: list[dict[str, str]], temperature: float
) -> str:
    """Headless Grok Build CLI — same session compute as interactive Grok TUI.

    Uses `grok login` auth (not raw XAI_API_KEY). Emits thinking + answer via
    `--output-format streaming-json` (Grok session infrastructure).
    """
    _ = temperature
    binary = grok_tui_bin()
    if not binary:
        raise RuntimeError("grok CLI not found on PATH (set GROK_BIN)")
    system, user_blob = _messages_to_prompt_parts(messages)

    try:
        t_out = float(os.environ.get("AETHER_LLM_TIMEOUT", "300"))
    except ValueError:
        t_out = 300.0
    try:
        max_turns = int(os.environ.get("AETHER_GROK_MAX_TURNS", "4"))
    except ValueError:
        max_turns = 4
    effort = (
        os.environ.get("AETHER_REASONING_EFFORT")
        or os.environ.get("GROK_REASONING_EFFORT")
        or "high"
    ).strip() or "high"
    # Domain seat: no write/exec tools; allow research tools like Grok session
    deny_tools = os.environ.get(
        "AETHER_GROK_DENY_TOOLS",
        "run_terminal_cmd,run_terminal_command,search_replace,Write,Edit,Bash,write",
    ).strip()

    with tempfile.TemporaryDirectory(prefix="aether-grok-tui-") as td:
        td_path = Path(td)
        body = user_blob
        if system and len(system) >= 12000:
            body = system[:20000] + "\n\n---\n\n" + user_blob
            system_for_flag = ""
        else:
            system_for_flag = system

        prompt_path = td_path / "prompt.txt"
        prompt_path.write_text(body, encoding="utf-8")

        out_fmt = (
            os.environ.get("AETHER_GROK_OUTPUT_FORMAT", "streaming-json").strip()
            or "streaming-json"
        )
        cmd = [
            binary,
            "--prompt-file",
            str(prompt_path),
            "--output-format",
            out_fmt,
            "--max-turns",
            str(max(1, max_turns)),
            "-m",
            backend.model,
            "--reasoning-effort",
            effort,
        ]
        if deny_tools:
            cmd.extend(["--disallowed-tools", deny_tools])
        if system_for_flag:
            cmd.extend(["--system-prompt-override", system_for_flag])

        env = {**os.environ}
        keep_api = os.environ.get("AETHER_GROK_TUI_KEEP_API_KEY", "").strip().lower()
        if keep_api not in ("1", "true", "yes", "on"):
            env.pop("XAI_API_KEY", None)
            env.pop("GROK_CODE_XAI_API_KEY", None)
        # ensure GROK_HOME points at session auth
        if not env.get("GROK_HOME") and Path.home().joinpath(".grok").is_dir():
            env["GROK_HOME"] = str(Path.home() / ".grok")

        try:
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=t_out,
                env=env,
            )
        except subprocess.TimeoutExpired as e:
            raise RuntimeError(f"grok_tui timed out after {t_out}s") from e
        except FileNotFoundError as e:
            raise RuntimeError(f"grok CLI not executable: {binary}") from e

    out = (proc.stdout or "").strip()
    err = (proc.stderr or "").strip()
    if proc.returncode != 0 and not out:
        raise RuntimeError(
            f"grok_tui exit {proc.returncode}: {(err or 'no stderr')[:500]}"
        )
    if not out:
        raise RuntimeError(
            f"grok_tui empty response (exit {proc.returncode}): {(err or '')[:300]}"
        )

    thinking, text, meta = _parse_grok_stream(out)
    _LAST_CHAT_META.clear()
    _LAST_CHAT_META.update(
        {
            "provider": "grok_tui",
            "model": backend.model,
            "thinking": thinking,
            "reasoning_effort": effort,
            **meta,
        }
    )
    # Prefer structured text; fall back to raw stdout if plain format
    if text.strip():
        return text.strip()
    if out_fmt == "plain" or not thinking:
        # strip accidental JSON lines if mixed
        lines = []
        for line in out.splitlines():
            s = line.strip()
            if s.startswith("{") and '"type"' in s:
                continue
            lines.append(line)
        cleaned = "\n".join(lines).strip()
        return cleaned or out
    return thinking.strip() or out


def _parse_grok_stream(raw: str) -> tuple[str, str, dict]:
    """Parse Grok CLI streaming-json / json lines into thinking + answer text."""
    import json

    thoughts: list[str] = []
    texts: list[str] = []
    meta: dict = {}
    for line in (raw or "").splitlines():
        s = line.strip()
        if not s.startswith("{"):
            # plain leftover
            if s:
                texts.append(s)
            continue
        try:
            ev = json.loads(s)
        except json.JSONDecodeError:
            texts.append(line)
            continue
        if not isinstance(ev, dict):
            continue
        typ = ev.get("type") or ""
        if typ == "thought":
            d = ev.get("data")
            if d is None and "text" in ev:
                d = ev.get("text")
            if d is not None:
                thoughts.append(str(d))
        elif typ == "text":
            d = ev.get("data")
            if d is None and "text" in ev:
                d = ev.get("text")
            if d is not None:
                texts.append(str(d))
        elif typ in ("assistant", "message", "content"):
            # alternate shapes
            d = ev.get("data") or ev.get("content") or ev.get("text") or ""
            if isinstance(d, list):
                for part in d:
                    if isinstance(part, dict) and part.get("type") == "text":
                        texts.append(str(part.get("text") or part.get("data") or ""))
                    elif isinstance(part, str):
                        texts.append(part)
            elif d:
                texts.append(str(d))
        elif typ == "end":
            if "sessionId" in ev:
                meta["session_id"] = ev.get("sessionId")
            if "usage" in ev:
                meta["usage"] = ev.get("usage")
            if "modelUsage" in ev:
                meta["model_usage"] = ev.get("modelUsage")
        elif typ == "usage" and "usage" in ev:
            meta["usage"] = ev.get("usage")
        elif typ == "tool_call":
            title = ev.get("title") or ev.get("toolName") or "tool"
            meta.setdefault("tools", []).append(str(title))
    thinking = "".join(thoughts).strip()
    # If thought tokens are word-pieces, join without extra spaces when already spaced
    text = "".join(texts).strip()
    return thinking, text, meta




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
    env_name = backend.api_key_env or "XAI_API_KEY"
    key = os.environ.get(env_name, "").strip()
    if not key and backend.name == "xai":
        key = os.environ.get("XAI_API_KEY", "").strip()
    if not key and backend.name == "openai":
        key = "local"
    if not key:
        raise RuntimeError(f"missing API key env {env_name}")
    body_obj: dict = {
        "model": backend.model,
        "messages": messages,
        "temperature": temperature,
    }
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }
    # OpenRouter optional attribution headers (improves free-tier routing)
    if backend.name == "openrouter":
        headers["HTTP-Referer"] = os.environ.get(
            "OPENROUTER_REFERER", "https://github.com/mechanicall-os"
        )
        headers["X-Title"] = os.environ.get("OPENROUTER_TITLE", "Mechanicall desk")
    body = json.dumps(body_obj).encode()
    req = urllib.request.Request(
        f"{backend.base}/chat/completions",
        data=body,
        headers=headers,
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout()) as resp:
            data = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        err = e.read().decode(errors="replace")[:400]
        raise RuntimeError(f"{backend.name} HTTP {e.code}: {err}") from e
    choices = data.get("choices") or []
    if not choices:
        raise RuntimeError(f"{backend.name} empty response: {data!r}"[:300])
    return (choices[0].get("message") or {}).get("content", "").strip()


def _ollama_chat(backend: LLMBackend, messages: list[dict[str, str]], temperature: float) -> str:
    # personal-llm / Modelfile often ships with small n_ctx; raise for CURRENT inject
    try:
        num_ctx = int(os.environ.get("AETHER_OLLAMA_NUM_CTX", "8192"))
    except ValueError:
        num_ctx = 8192
    model = backend.model
    # Prefer :latest if bare name fails later — normalize sft tags
    if model in ("personal-llm-sft-v4", "personal-llm-sft-v2", "personal-llm-full:v1"):
        if ":" not in model.replace("personal-llm-full:v1", "x"):  # keep full:v1
            pass
    if model == "personal-llm-sft-v4":
        model = "personal-llm-sft-v4:latest"
    elif model == "personal-llm-sft-v2":
        model = "personal-llm-sft-v2:latest"
    # Truncate huge system messages to fit small local models if still oversized
    safe_msgs = []
    for m in messages:
        role = m.get("role") or "user"
        content = m.get("content") or ""
        if role == "system" and len(content) > 6000:
            content = content[:2500] + "\n\n…[truncated for n_ctx]…\n\n" + content[-2500:]
        safe_msgs.append({"role": role, "content": content})
    body = json.dumps(
        {
            "model": model,
            "messages": safe_msgs,
            "stream": False,
            "options": {"temperature": temperature, "num_ctx": num_ctx},
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
    import sys

    if len(sys.argv) > 1 and sys.argv[1] in ("presets", "list", "--presets"):
        print(format_presets_help())
    elif len(sys.argv) > 2 and sys.argv[1] in ("preset", "use"):
        print(apply_preset(sys.argv[2], lock=False))
        print(describe_backend())
    else:
        print(describe_backend())

