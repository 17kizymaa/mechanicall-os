# Interface-dev regressions — seat PANEL | SHELL

**Stream:** `dev/15_mbp-seat-gop-chat`  
**When:** 2026-08-02 (session continuation)  
**Surface:** `python/aether_panel_tui.py` (GOP dual-page under cage/foot)  
**Hosts:** mbp-edge Alpine seat · Kingston project FS · myarch Ollama  

Use this file when changing seat TUI, LLM routing, or seat env launchers.
Each row is a **regression that already bit production seat** — not hypothetical.

---

## Severity legend

| Tag | Meaning |
|-----|---------|
| **P0** | Chat/input completely broken on a page |
| **P1** | Wrong backend/model after page switch; silent wrong agent |
| **P2** | Layout/chrome discomfort; recoverable |
| **P3** | Boot/host ergonomics (outside TUI but same stream) |

---

## R-01 — Shell free-chat ImportError (`agent_mode_enabled`)

| | |
|--|--|
| **Severity** | P0 |
| **Pages** | SHELL (F2) |
| **Symptom** | Every free-chat line → `(import error: cannot import name 'agent_mode_enabled' from 'aether_shell_agent')` |
| **Root cause** | `shell_submit` imported `agent_mode_enabled` from `aether_shell_agent`. Symbol lives only in `aether_shell`. |
| **Fix** | Free-chat path: do **not** import or call `agent_mode_enabled`. Shell page = peer Ollama chat via `apply_peer_backend` + `chat` + `build_messages`. Optional agent loop is a separate, explicit mode later. |
| **Test** | F2, type `reply with exactly: pong` → line `peer   pong`, status `peer ready`. No import error. |
| **Guard** | `grep agent_mode_enabled python/aether_panel_tui.py` must not appear in **import** lines (comment OK). Prefer static check: import `shell_submit` source and assert no `from aether_shell_agent import … agent_mode_enabled`. |

---

## R-02 — Panel Grok inherits Ollama model id after F2 / seat env

| | |
|--|--|
| **Severity** | P0 / P1 |
| **Pages** | PANEL (F1), especially after SHELL or cold start from `mech-cage-session` |
| **Symptom** | Panel chat returns JSON error: `Couldn't set model 'personal-llm-sft-v4:latest': … unknown model id` |
| **Root cause** | Shared process env. Peer/shell sets `AETHER_MODEL=personal-llm-sft-v4:latest`. Panel used `os.environ.setdefault("AETHER_MODEL", "grok-4.5")` which **never overwrites**. Seat launcher (`mech-cage-session`) also pre-sets Ollama model as process default. `resolve_backend()` for `grok_tui` reads `AETHER_MODEL` as the CLI model id. |
| **Fix** | On every `panel_chat`: **force**  
  `AETHER_LLM_PROVIDER=grok_tui`  
  `AETHER_MODEL=grok-4.5`  
  `pop("AETHER_OLLAMA_MODEL", None)`  
  Never `setdefault` for the model after a peer hop. |
| **Test** | F2 peer chat once → F1 panel chat `reply with exactly: pong` → assistant `pong`, `backend: grok_tui/grok-4.5`, thinking optional but provider must be grok_tui. |
| **Guard** | Smoke: apply_peer_backend → force panel env → `resolve_backend().model == "grok-4.5"`. Ban `setdefault("AETHER_MODEL"` in panel chat path. |

---

## R-03 — Page switch leaves sticky backend (wrong agent)

| | |
|--|--|
| **Severity** | P1 |
| **Pages** | F1 ↔ F2 |
| **Symptom** | Shell talks to Grok, or panel talks to Ollama, after switching without full restart. |
| **Root cause** | Single process, module-global env in `aether_llm`. No per-page backend isolation. |
| **Contract** | | Page | Provider | Model | Role |
| |------|----------|-------|------|
| | PANEL | `grok_tui` | `grok-4.5` | `grok` |
| | SHELL | `ollama` | `personal-llm-sft-v4:latest` | `peer` |
| **Fix pattern** | Re-assert full env block at the **start of every submit**, not only on page enter. |
| **Test** | F1 message · F2 message · F1 message — each uses correct backend label in status/header. |

---

## R-04 — Dual-page must not replace process / kill cage

| | |
|--|--|
| **Severity** | P0 (session death) |
| **Pages** | F1 / F2 / QUIT semantics |
| **Symptom** | Escaping “shell” or Ctrl+D kills compositor; black screen; need seat restart. |
| **Root cause** | Earlier design `exec`’d external shell or replaced process under foot/cage. |
| **Fix** | PANEL and SHELL are **pages in one TUI** (`page = "panel"|"shell"`). `/panel`, F1, bye → `goto_panel()`, not process exit. Menu QUIT is the only intentional leave. |
| **Test** | F2 → F1 → F2 repeatedly; cage PID stable. `/panel` from shell does not drop compositor. |
| **Guard** | No `os.exec*`, no `subprocess` that replaces seat for page switch. |

---

## R-05 — Chat density / actions dock (comfort loop)

| | |
|--|--|
| **Severity** | P2 |
| **Pages** | Both |
| **Symptom** | Inbox felt cramped; action strip always open; actions not right-aligned; “Grok padding” mismatch. |
| **Desired** | Sparse inbox (`msg_gap=2`, wider air, `max_thoughts_width=72`); **F3** toggles actions (default **hidden**); open strip **right-aligned**. |
| **Implementation notes** | `GrokPad` dataclass; `show_actions`; `_bot_rows()` shrinks when closed; `_draw_menu_dock` right-aligns labels. |
| **Test** | Visual: empty chat shows airy placeholder; F3 shows actions on the right; F3 again hides; more body height when closed. |
| **Regression risk** | Hard-coding `menu_rows=2` always steals vertical space even when actions hidden. |

---

## R-06 — Ollama context / model tag

| | |
|--|--|
| **Severity** | P1 |
| **Pages** | SHELL |
| **Symptom** | Ollama `400` context length (e.g. 2048) or model not found. |
| **Root cause** | Missing `AETHER_OLLAMA_NUM_CTX` / wrong model string without `:latest`. |
| **Fix** | Shell path sets `AETHER_OLLAMA_NUM_CTX=8192`, model `personal-llm-sft-v4:latest`, host from `.aether/ollama-host` or `OLLAMA_HOST=http://192.168.1.241:11434`. |
| **Test** | From MBP: `curl -m3 $OLLAMA_HOST/api/tags` lists model; shell chat returns non-error. |

---

## R-07 — Apple Option picker vs rEFInd auto (boot UX)

| | |
|--|--|
| **Severity** | P3 |
| **Surface** | Firmware / rEFInd, not TUI |
| **Operator intent** | “I like the Option-only screen; I want it automatic.” |
| **Truth** | Apple Startup Manager (hold Option) **cannot** auto-show. **rEFInd** is the automatic multi-OS picker (`timeout 20`, Alpine + macOS). |
| **Blocker** | Protected `efi-boot-device` → macOS; Linux cannot rewrite (EPERM). UEFI `BootOrder` alone often ignored on Apple firmware. |
| **One-time human fix** | Hold Option → select EFI/rEFInd → **Control+click** up-arrow to bless default. See `BOOT-AUTO-PICKER.md`. |
| **Do not** | Confuse “fix Option screen auto” with “install rEFInd again” without bless. |

---

## Quick smoke (copy/paste on MBP)

```bash
cd /mnt/kingston-nixos/opt/mechanicall-os
export PYTHONPATH=python AETHER_HOME=$PWD MECH_PROJECT=$PWD
python3 - <<'PY'
import os, sys
from pathlib import Path
sys.path.insert(0, "python")
root = Path(".").resolve()
from aether_llm import apply_peer_backend, chat, resolve_backend, last_chat_meta
from aether_shell_agent import set_agent_role

# R-01 / R-06 shell
set_agent_role("peer")
print(apply_peer_backend(root, model="personal-llm-sft-v4:latest"))
os.environ.update({
    "AETHER_LLM_PROVIDER": "ollama",
    "AETHER_OLLAMA_MODEL": "personal-llm-sft-v4:latest",
    "AETHER_MODEL": "personal-llm-sft-v4:latest",
    "AETHER_OLLAMA_NUM_CTX": "8192",
})
assert resolve_backend().name == "ollama"
assert chat([{"role":"user","content":"reply with exactly: pong"}], temperature=0.1).strip().lower().startswith("pong")

# R-02 panel after peer
os.environ["AETHER_LLM_PROVIDER"] = "grok_tui"
os.environ["AETHER_MODEL"] = "grok-4.5"
os.environ.pop("AETHER_OLLAMA_MODEL", None)
set_agent_role("grok")
b = resolve_backend()
assert b.name == "grok_tui" and b.model == "grok-4.5", b
assert chat([{"role":"user","content":"reply with exactly: pong"}], temperature=0.1).strip().lower().startswith("pong")
print("smoke OK", last_chat_meta().get("provider"), last_chat_meta().get("model"))
PY
```

---

## Files that own these contracts

| File | Role |
|------|------|
| `python/aether_panel_tui.py` | Pages, padding, F3, submit paths |
| `python/aether_llm.py` | `resolve_backend`, `apply_peer_backend`, `chat`, env |
| `python/aether_shell.py` | `build_messages`, `agent_mode_enabled` (shell CLI only) |
| `python/aether_shell_agent.py` | Roles `peer` / `grok`; **no** `agent_mode_enabled` |
| `/usr/local/bin/mech-cage-session` | Seat process env defaults (peer/ollama) |
| `dev/15_mbp-seat-gop-chat/UI-DATA.md` | Layout numbers + chat payload shapes |

When you fix a new seat UI bug, **add a row here first**, then code.
