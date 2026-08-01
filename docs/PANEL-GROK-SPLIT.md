# Panel · Grok-left · CURRENT-right

**Status:** implemented 2026-07-31 (v1 dual-pane)  
**Doctrine:** CURRENT sacred · panel projects + human gates · preflight lives in **shell agent**

---

## Research (locked product ask)

### What “steal Grok TUI” means

Grok Build TUI is a **chat-first** operator surface: transcript up, input down, tools/agent behind the conversation. Mechanicall steals that **layout language**, not the proprietary binary:

| Grok TUI | Mechanicall panel v1 |
|----------|----------------------|
| Full-width chat | **Left pane** — Domain chat (peer agent by default; Grok-shaped loop) |
| Project context implicit | **Right pane** — **CURRENT.md always visible** |
| Slash/tools in session | Full shell agent via “Fullscreen Domain shell” |
| Preflight N/A | **Not on main panel** — shell `/preflight` / agent |

### Why not embed raw `grok` binary in the left half

Embedding an interactive full-screen TUI inside a curses child window is fragile (PTY, alt-screen, resize). v1 **steals the UX**: left is chat-driven Domain agent (same tools/protocol as `aether shell`); right is always CURRENT. Advanced → “Fullscreen Grok TUI” still launches real `grok` when you want the full product.

### Why preflight left main board

Preflight is an **operator/agent** check, not a couch button. Putting it on the main panel recreated “ceremony chrome.” Shell agent owns Next checks (`/preflight`, agent loop). Panel main = **see CURRENT + chat + human approve/reject + open full seats**. Advanced keeps the full legacy action list (including preflight) for power operators.

### No hotkeys on main

Letter hotkeys made the board feel like a DOS menu, not Grok. v1 main: **Tab** focus · **arrows** · **Enter** · type to chat. Advanced list is pick-by-arrow only (no single-letter shortcuts required).

---

## Implementation map

| Piece | Location |
|-------|----------|
| Dual-pane draw | `python/aether_panel.py` `_draw_split` |
| Main menu (no preflight) | `MAIN_ACTIONS` |
| Legacy / power actions | `ADVANCED_ACTIONS` + Advanced… overlay |
| Left chat → peer/agent | `_panel_chat` → `aether_shell_agent.agent_chat_loop` |
| Right CURRENT | always from `load_state` / file re-read |
| Shell owns preflight | documented; still in Advanced for emergencies |

### Main actions (no hotkeys)

1. Refresh  
2. Approve (human only)  
3. Reject (human only)  
4. Advanced… (full list: preflight, switch project, presets, …)  
5. Fullscreen Domain shell  
6. Fullscreen Grok TUI  
7. Edit CURRENT  
8. Quit  

Chat is always available when focus is **chat** (default).

### Focus model

- **chat** — type message, Enter send  
- **menu** — ↑↓ select main action, Enter run  
- **current** — ↑↓ scroll CURRENT pane  
- **Tab** cycles focus  

---

## Operator story (post-desk)

1. `aether panel .`  
2. Right: read Next / Prohibited.  
3. Left: talk like Grok (peer synthesis default).  
4. Need code/tools deeply → Fullscreen Domain shell (agent) or Fullscreen Grok.  
5. Preflight in shell; Approve on panel when human is ready.  

---

## TUI vs CLI (important)

| Mode | Command | What you get |
|------|---------|----------------|
| **Fullscreen TUI** | `aether panel .` | Alt-screen dual-pane app (`aether_panel_tui.py`) |
| **Steal real Grok** | `aether panel --grok-split .` | **tmux**: left = `grok`, right = live `CURRENT.md` |
| Legacy CLI menu | `aether panel --simple` | Numbered menu (not TUI) |
| Text dump | `aether panel --dump` | Projection only |

Must run in a **real terminal** (TTY). Piping or non-interactive runners are not a TUI.

### Controls (fullscreen TUI)

| Input | Action |
|-------|--------|
| **Tab** | Focus: chat → menu → CURRENT |
| Type + **Enter** | Send Domain chat (left) |
| **←→↑↓** | Menu / scroll |
| Menu | Approve, Reject, Advanced, Domain shell, Grok fullscreen, … |
| No letter hotkeys on main | Preflight → shell or Advanced |

---

## Follow-ups

- Mouse hit-testing on panes  
- HTML projection matching dual-pane  
- Optional always-default `--grok-split` via env  

---

*Research + implementation contract for panel redesign.*
