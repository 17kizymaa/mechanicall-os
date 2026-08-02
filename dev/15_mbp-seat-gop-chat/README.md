# 15 — MBP seat GOP chat continuous integration

Live Alpine seat + Kingston project FS.  
Primary artifact: operator can chat **panel (Grok)** and **shell (PEER sft-v4)** about CURRENT without killing cage.

## Docs (start here for UI work)

| File | Use when |
|------|----------|
| **`INTERFACE-REGRESSIONS.md`** | Changing seat TUI / LLM routing — **known P0–P3 regressions** |
| **`UI-DATA.md`** | Layout tokens, action lists, chat payload shapes, env contracts |
| `SESSION-LOG.md` | What landed this stream + validation |
| `BOOT-AUTO-PICKER.md` | Auto multi-OS picker (rEFInd) vs Apple Option hold |
| `ROLE-GROK-SEAT-INJECT.md` | Role / system inject analysis |

## Code

- `python/aether_panel_tui.py` — dual-page GOP TUI  
- `python/aether_llm.py` — backends, peer apply, chat  
- `/usr/local/bin/mech-cage-session` — seat process env (on MBP)

## Parent CURRENT

Next: `seat-chat-comfort-loop` (see repo `CURRENT.md`).
