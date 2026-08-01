# `aether shell` — Domain-bound operator REPL

**Status:** implemented 2026-07-30 (MVP); compute ranking fixed 2026-07-31  
**Inspired by:** Aider’s thin terminal loop — **not** a full Aider fork  
**Does not:** replace Grok CLI product; uses **Grok TUI compute** as the preferred backend  

## Why

Panel “Open Grok” is launch-and-return. Operating *from* Grok leaves Domain.  
`aether shell` keeps you in a **Mechanicall seat** while still using Grok compute.

## Compute ranking (important)

| Rank | Backend | Credential | How |
|------|---------|------------|-----|
| **1 (preferred)** | **Grok TUI** | `grok login` → `~/.grok/auth.json` | `grok -p` / headless CLI |
| 2 | Free APIs / Anthropic / Ollama | various | direct HTTP |
| **3 (lower)** | **Raw xAI API** | `XAI_API_KEY` → `api.x.ai` | OpenAI-compat HTTP |

**API compute &lt; Grok TUI compute.**  
Raw `XAI_API_KEY` is *not* the same as your SuperGrok / Grok.com session.  
Shell and `aether_llm` prefer `grok_tui` whenever the CLI is installed and you are logged in.

## Use

```bash
export AETHER_HOME=/path/to/mechanicall-os
export PATH="$AETHER_HOME:$PATH"

# Preferred: Grok TUI session (same compute path as interactive Grok Build)
grok login                    # once; stores ~/.grok/auth.json
# optional pin:
# export AETHER_MODEL=grok-4.5

cd /path/to/project           # should have CURRENT.md
aether shell
# or from panel: Open Domain shell [s]

# force provider if needed:
# aether shell . --provider grok_tui --model grok-4.5
# aether shell . --provider xai       # raw API (explicit; lower rank)
# aether shell . --provider ollama
```

### Credential notes

| Method | What it is |
|--------|------------|
| `grok login` | Grok Build / Grok.com **session** (preferred TUI compute) |
| `XAI_API_KEY` | Console API key → **api.x.ai** (fallback only; different quota) |

Disable TUI prefer: `AETHER_SHELL_PREFER_GROK_TUI=0`  
Disable TUI backend entirely: `AETHER_GROK_TUI=0`  
Keep API key visible to `grok` subprocess: `AETHER_GROK_TUI_KEEP_API_KEY=1` (default: stripped so session wins)

## Slash commands

| Cmd | Effect |
|-----|--------|
| `/status` | one-line Objective / Next |
| `/current` | full CURRENT.md |
| `/next` | Next id + Next allowed action section |
| `/events [n]` | last n lines of `.aether/events.jsonl` |
| `/decisions` | `DECISIONS.md` if present |
| `/preflight <id>` | run aether preflight |
| `/backend` | which LLM + active preset |
| `/provider list\|next\|coding\|sonnet35\|ollama\|…` | **toggle compute presets** |
| `/model <id>` | pin model slug (keep provider) |
| `/preset-save` | write `.aether/llm-preset` |
| `/smoke` | offline smoke of standard slash behaviours (no LLM) |
| `/run <cmd> [args]` | **human** allowlisted tools (`cat` `grep` `ls` `touch` `mkdir` …) |
| `!<cmd> [args]` | same as `/run` |
| `/tools` | print allowlist |
| `/clear` | drop chat history |
| `/quit` | leave |

Empty line waits (never yes).

### Allowlisted local tools

Human-only. **Model chat never auto-executes.** cwd = project root. No `shell=True`, no pipes/`;`/`&`.

`cat` `head` `tail` `grep` `rg` `ls` `pwd` `touch` `mkdir` `stat` `wc` `find` `echo` `date` `file` `diff` `which` `basename` `dirname` `realpath` `printf` `tee` `sort` `uniq` `cut` `tr` `sed` `awk` `tree` `du` `df` `id` `uname` `env` `test` `true` `false`

**Denied:** `rm` `mv` `cp` `sudo` `bash`/`sh` `curl` `python` `aether` (use `/preflight`) `cryptsetup` …

```bash
shell> /run touch notes.md
shell> ! grep -n Next CURRENT.md
shell> /tools
```

Non-interactive smoke:

```bash
aether shell /path/to/project --smoke
# exit 0 if SMOKE OK
```

### Preset ladder (free coding → Sonnet → local)

`coding` → `coding_alt` → `free` → `llama_free` → `groq` → `sonnet35` →
`sonnet35_direct` → `sonnet` → `ollama` → `grok_tui` → `xai`

See `docs/FREE-API.md` for keys and OpenRouter free slugs.

## Vs other surfaces

| Surface | Seat | Domain-bound | Compute |
|---------|------|--------------|---------|
| `grok` interactive TUI | External TUI | No | TUI session |
| panel → Open Grok | Launch external | No | TUI session |
| panel → Open Domain shell | Suspend → shell → return | **Yes** | peer default / grok real |
| **`aether shell`** | Operator REPL | **Hard** | peer (ollama) default |
| `aether desk` / desk-serve | **Removed** | — | unsacred soft-chat |

## Two agents (actual shape)

| Role | Profile | Compute | Tools | Job |
|------|---------|---------|-------|-----|
| **peer** (default) | `references/aether-shell-agent-peer.md` | Ollama `personal-llm-sft-v4` (local or remote) | **read-only** | Proposals + synthesis |
| **grok** (real) | `references/aether-shell-agent-grok.md` | Grok TUI preferred | full tools | Implement under Domain |

**Default on shell start:** `/agent peer` + Ollama host probe (loopback → `.aether/ollama-host` → Tailscale self IP).

```bash
aether shell .                    # peer by default
/agent peer                       # explicit
/ollama-host http://100.x.y.z:11434   # pin remote personal-llm host (project)
/ollama-host local                # back to 127.0.0.1
/peer-serve                       # LAN/Tailscale URLs for THIS host as server
/agent grok                       # opt-in real coding agent
```

Env: `AETHER_SHELL_AGENT_ROLE=peer|grok` · `AETHER_OLLAMA_HOST` · `AETHER_OLLAMA_REMOTE` · project pin `.aether/ollama-host`

### Grok-shaped DEFINITION (shared)

1. Agent profile (YAML tools + body)  
2. `AGENTS.md` project rules  
3. Tool loop (`<tool_call>…</tool_call>`)  
4. **CURRENT** sacred — never auto-approve  

**Strip-alpha:** no web tools, no subagents/MCP, no auto-approve.  
Shell-side tools run between model turns (remote `grok -p` still tool-stripped; **real edits** happen via shell tool loop).

```bash
aether shell . --provider grok_tui          # tends to /agent grok
aether shell . --provider ollama --model personal-llm-sft-v4   # peer
```

## Implementation

- Backend id: `grok_tui` in `python/aether_llm.py` (`grok --prompt-file … -p` headless; remote tools denied)
- Agent loop: `python/aether_shell_agent.py` + profile `references/aether-shell-agent.md`
- Shell prefer: `prefer_grok_tui_for_shell()` in `python/aether_shell.py`
- Panel: **Open Domain shell [s]** preferred over **Open Grok [g]**

See also: `NOT-IMPLEMENTED.md` (operator TUI sovereignty),  
`dev/14_…/output/RESEARCH-OPEN-SOURCE-SOVEREIGN-TUI.md`.
