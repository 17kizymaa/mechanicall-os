# Session log — 15_mbp-seat-gop-chat

**When:** 2026-08-02 (stream + continuation)  
**Hosts:** myarch (desktop, Ollama `personal-llm-sft-v4:latest`) · mbp-edge Alpine (cage/foot seat) · Kingston nixos+vault  
**Branch:** `feat/domain-shell-panel-tui`  
**Operator goal:** continuous integration until comfortable chatting on MBP seat  

---

## Goals this stream

- Connect MBP over ethernet/WiFi; Alpine co-host online  
- Install cage + seat OpenRC dual chooser (VNC kiosk | aether panel)  
- Mount Kingston with vault key; project = `/mnt/kingston-nixos/opt/mechanicall-os`  
- Wire CURRENT.md + chat logs from Kingston  
- GOP-style panel TUI; F1 PANEL / F2 SHELL as **pages** (same header, same compositor)  
- Grok session chatter on panel (thinking via streaming-json)  
- Shell default = personal-llm-sft-v4 on myarch Ollama for CURRENT propose drafts  
- Fix shell↔panel so page switch / Esc does not kill cage  
- Chat comfort: sparse inbox, F3 toggle actions (right-aligned), shared chrome  
- Document interface-dev regressions + UI data for future work  
- Boot: clarify Option Startup Manager vs auto rEFInd  

---

## Timeline / what landed

### Infrastructure

- Alpine seat + `mbp-seat` OpenRC chooser; `mech-cage-session` / `mech-cage`  
- Kingston mounts: nixos, ESP, vault key  
- Peer Ollama host pin: `.aether/ollama-host` → `http://192.168.1.241:11434`  
- Seat env defaults peer/ollama; panel forces Grok per message  

### TUI (GOP dual-page)

- `python/aether_panel_tui.py` rewritten around `GrokPad`  
- F1 PANEL (chat + CURRENT) · F2 SHELL (peer transcript) · F3 actions  
- Actions default **hidden**, **right-aligned** when open  
- Sparse chat: `msg_gap=2`, `max_thoughts_width=72`, thinking strip  

### Chat routing (critical)

| Page | Backend | Model |
|------|---------|-------|
| PANEL | `grok_tui` | `grok-4.5` |
| SHELL | `ollama` | `personal-llm-sft-v4:latest` |

### Fixes this continuation (interface regressions)

See **`INTERFACE-REGRESSIONS.md`** for full rows. Short form:

| ID | Failure | Fix |
|----|---------|-----|
| R-01 | Shell import `agent_mode_enabled` from wrong module | Free-chat only; no that import |
| R-02 | Panel kept Ollama model after F2 / seat env (`setdefault`) | **Force** `AETHER_MODEL=grok-4.5` every panel submit |
| R-03 | Sticky backend across pages | Re-assert full env on every submit |
| R-04 | Page switch killed cage | Pages only; no process replace |
| R-05 | Dense inbox / always-on actions | Sparse pad + F3 toggle |
| R-06 | Ollama ctx / model tag | `num_ctx=8192`, `:latest` |
| R-07 | “Auto Option boot screen” | Impossible; rEFInd is auto picker + Control-click bless |

### Boot (out of TUI, same stream)

- Documented in `BOOT-AUTO-PICKER.md`  
- Apple Option screen cannot auto-show  
- rEFInd timeout 20; BootOrder 0002/0003 first; `efi-boot-device` still macOS until human bless  
- One-time: Option → EFI/rEFInd → Control+click to set default  

### Validation (post-fix, MBP)

```
shell submit "reply with exactly: pong" → peer pong · status peer ready
panel after shell → assistant pong · thinking True · backend grok_tui/grok-4.5
cage restarted with new aether_panel_tui.py (838 lines)
```

---

## Role inject

See `ROLE-GROK-SEAT-INJECT.md`.

---

## CURRENT

Next: **seat-chat-comfort-loop** (INTEGRATE / ACTIVE).  
Prior Next `seat-nixos-efi-foundation` deferred until chat comfort APPROVED.

---

## Artifacts in this folder

| File | Role |
|------|------|
| `README.md` | Index |
| `SESSION-LOG.md` | This log |
| `INTERFACE-REGRESSIONS.md` | **Regression catalog for interface-dev** |
| `UI-DATA.md` | **Layout tokens, chat shapes, env contracts** |
| `BOOT-AUTO-PICKER.md` | Option vs rEFInd auto |
| `ROLE-GROK-SEAT-INJECT.md` | Role system notes |

---

## Open risks

- Ollama must stay up on myarch for shell PEER  
- Grok auth expiry → `grok login --device-auth` on seat user  
- Kingston unplug unmounts project path  
- macOS Startup Disk / bless can re-steal boot default (R-07)  
- Any new `setdefault(AETHER_MODEL)` on panel path reintroduces R-02  
- Importing shell-only symbols from `aether_shell_agent` reintroduces R-01  

---

## Handoff for next interface-dev

1. Read `INTERFACE-REGRESSIONS.md` before editing seat TUI or LLM env.  
2. Read `UI-DATA.md` before changing padding, chrome, or chat payload shapes.  
3. After changes: run smoke block in INTERFACE-REGRESSIONS (shell then panel).  
4. On new production bug: add regression row **first**, then patch.  
5. Optional: implement `.aether/ui-events.jsonl` hook from UI-DATA §10.  
