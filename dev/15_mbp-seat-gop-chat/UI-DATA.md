# UI data — Aether seat (PANEL | SHELL)

**Purpose:** Freeze **layout numbers, chrome semantics, chat payloads, and env contracts** so future interface-dev does not re-derive from screenshots or chat memory.

**Canonical code:** `python/aether_panel_tui.py` (`GrokPad`, `PanelApp`)  
**Stream:** `dev/15_mbp-seat-gop-chat` · 2026-08-02  

---

## 1. Page model

```
┌─────────────────────────────────────────────────────────┐
│ header row 0  MECHANICALL SEAT · GOP · F3 actions       │  color pair 6
│ header row 1  [F1 PANEL] [F2 SHELL]  proj · next · be   │  pair 8/9 active tab
├──────────────────────────┬──────────────────────────────┤
│                          │                              │
│  PANEL only:             │  PANEL only:                 │
│  chat pane (~58% width)  │  CURRENT pane                │
│                          │                              │
│  SHELL: full-width shell log                            │
│                          │                              │
├──────────────────────────┴──────────────────────────────┤
│  [optional] right-aligned action strip  (F3, show_actions) │
│  status foot: MODE │ F3 … │ status                      │
│  input: ›  or  shell>                                   │
└─────────────────────────────────────────────────────────┘
```

| Key | Action |
|-----|--------|
| F1 | `page = panel`, focus chat |
| F2 | `page = shell`, focus input, `ensure_shell_boot` |
| F3 | toggle `show_actions`; focus menu when open |
| Tab | cycle focus (menu only if actions open) |
| Esc | close advanced → hide actions → shell→panel |
| Enter | submit chat / shell line / menu action |

**Invariant:** one process, two pages. No compositor kill on page change.

---

## 2. Layout tokens (`GrokPad`)

Aligned to Grok Build TUI theming (outer / block / message gap).

| Token | Value | Notes |
|-------|------:|-------|
| `outer_vpad` | 1 | Below header before body |
| `outer_hpad_left` | 3 | |
| `outer_hpad_right` | 3 | |
| `block_pad_left` | 3 | Inside chat/CURRENT boxes |
| `block_pad_right` | 3 | |
| `msg_gap` | 2 | Blank lines between message blocks |
| `header_rows` | 2 | Fixed |
| `menu_rows` | 1 | Actions **closed** (status only) |
| `menu_rows_open` | 2 | Actions **open** (strip + status) |
| `input_rows` | 2 | Status foot + input line (when closed: status uses one of these) |
| `max_thoughts_width` | 72 | Soft wrap for chat text |
| `max_history_turns` | 10 | Display window |
| `max_thinking_chars` | 220 | Truncate thinking strip |
| `min_cols` | 56 | Below → “need ≥…” |
| `min_rows` | 16 | |

**Panel split:** chat width ≈ `0.58 * usable_w`, CURRENT gets remainder (min ~16 cols).

**Body height:**  
`body_h = h - header_rows - outer_vpad - bot_rows`  
`bot_rows = (menu_rows_open if show_actions else menu_rows) + input_rows`

---

## 3. Actions dock data

Default: `show_actions = False` (more vertical air for inbox).

When open, actions are **right-aligned** in the strip:

### PANEL main

```
APPROVE | REJECT | REFRESH | SHELL | ADVANCED | EDIT CURRENT | QUIT
```

### PANEL advanced

```
Preflight Next | Preflight step… | Switch project… | Open PROPOSE… |
Events | Write PANEL files | Create CURRENT | Playbook | ← Back
```

### SHELL

```
PANEL | PREFLIGHT NEXT | STATUS | HELP | CLEAR | QUIT
```

Keys are internal action ids (`approve`, `open_shell`, `goto_panel`, …) consumed by `run_menu_action` / host `_run_action`.

---

## 4. Chat display data (PANEL)

### History item shape

```json
{
  "role": "user" | "assistant",
  "content": "string",
  "thinking": "string (assistant only, optional)",
  "provider": "grok_tui (optional meta)"
}
```

### Render prefixes (fixed column labels)

| Role | First line prefix | Continuation |
|------|-------------------|--------------|
| user | `  you    ` | `         ` |
| thinking | `  think  ` | `         ` |
| assistant | `  grok   ` | `         ` |

Empty history placeholder lines:

```
  chat
  type below
  F3 · actions
```

### Colors (curses pairs, when available)

| Pair | Use |
|-----:|-----|
| 1 | frames / grok bold |
| 2 | you / input bold |
| 3 | CURRENT text |
| 4 | think / status foot |
| 6 | header bar |
| 7 | reverse menu select |
| 8 | inactive tab strip |
| 9 | active tab |

---

## 5. Shell display data

### Transcript lines (`shell_lines: list[str]`)

Free-form; convention:

```
  shell  ·  peer sft-v4
  <status_line>
  <peer backend line>
  <describe_backend>

  you    <user text>

  peer   <first reply line>
         <continuation>
```

### Shell history for LLM (`shell_hist`)

Same role/content dicts as panel history (no thinking required for peer).

### Slash / tools

| Input | Behavior |
|-------|----------|
| `/panel`, `/back`, `/p`, `panel` | `goto_panel` |
| `bye` / `quit` / … | `goto_panel` (does not kill seat) |
| `!cmd …` | allowlisted tool via `run_allowlisted` |
| `/…` | `handle_slash` |
| free text | peer chat |

---

## 6. Backend env contract (per submit)

### PANEL `panel_chat` (force every time)

```
AETHER_LLM_PROVIDER=grok_tui
AETHER_SHELL_AGENT_ROLE=grok
AETHER_MODEL=grok-4.5
# AETHER_OLLAMA_MODEL removed
AETHER_REASONING_EFFORT=high          # setdefault OK
AETHER_GROK_OUTPUT_FORMAT=streaming-json
set_agent_role("grok")
```

### SHELL free chat (force every time)

```
AETHER_LLM_PROVIDER=ollama
AETHER_OLLAMA_MODEL=personal-llm-sft-v4:latest
AETHER_MODEL=personal-llm-sft-v4:latest
AETHER_OLLAMA_NUM_CTX=8192
OLLAMA_HOST=http://192.168.1.241:11434   # or .aether/ollama-host
set_agent_role("peer")
apply_peer_backend(root, model="personal-llm-sft-v4:latest")
```

### Seat launcher defaults (`mech-cage-session`)

Process starts **peer/ollama**-biased so shell works immediately; panel **must** override on each message (see INTERFACE-REGRESSIONS R-02).

---

## 7. LLM message build

Both pages: `aether_shell.build_messages(root, history)` injects CURRENT / role system context.

Panel display truncates thinking to `max_thinking_chars`; full thinking may still sit in `last_chat_meta()["thinking"]`.

---

## 8. Status / header backend label

`_backend_label()` → `backend: {name}/{model}` from `resolve_backend()`.

| Page after successful chat | Expected label fragment |
|----------------------------|-------------------------|
| PANEL | `grok_tui/grok-4.5` |
| SHELL | `ollama/personal-llm-sft-v4:latest` |

---

## 9. Logs & persistence

| Path | Content |
|------|---------|
| `.aether/shell.jsonl` | shell user/assistant via `append_log` |
| `.aether/chat.jsonl` | older desk chat (may be stale) |
| `.aether/events.jsonl` | panel events |
| `.aether/ollama-host` | pinned Ollama URL |
| `.aether/agent-role` | last role file |
| `.aether/llm-preset` | preset name |
| `dev/15_mbp-seat-gop-chat/*` | operator session + UI contracts |

Do **not** commit secrets. Grok auth is under `~/.grok` on seat user.

---

## 10. Future UI data hooks (not built yet)

When interface-dev adds richer UI, prefer these shapes so regressions stay testable:

```json
{
  "ui_event": "chat_submit|page_switch|actions_toggle|scroll",
  "page": "panel|shell",
  "ts": "ISO-8601",
  "backend": {"name": "…", "model": "…"},
  "layout": {
    "show_actions": false,
    "focus": "chat|input|menu|current|log",
    "cols": 120,
    "rows": 40,
    "body_h": 28
  },
  "payload": {
    "user_chars": 0,
    "reply_chars": 0,
    "thinking_chars": 0,
    "error": null
  }
}
```

Append to `.aether/ui-events.jsonl` (optional) without blocking the draw loop.

---

## 11. Visual regression checklist (manual)

1. Cold seat: panel open, actions **hidden**, airy empty chat.  
2. Type short message → `you` / `think` / `grok` with gaps.  
3. F3 → actions on **right**; body shrinks one row.  
4. F2 → full-width shell; peer boot banner; chat works.  
5. F1 → panel chat still Grok (not Ollama model error).  
6. Esc from shell → panel; cage still alive.  
7. Header tab highlight tracks page.

Record failures as new rows in `INTERFACE-REGRESSIONS.md`.
