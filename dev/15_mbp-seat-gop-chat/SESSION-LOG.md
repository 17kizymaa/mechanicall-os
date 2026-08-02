# Session log — 15_mbp-seat-gop-chat

**When:** 2026-08-02  
**Hosts:** myarch (desktop, Ollama) · mbp-edge Alpine (seat) · Kingston nixos+vault  
**Operator:** continuous integration until comfortable chatting on MBP seat  

## Goals this stream
- Connect MBP over ethernet/WiFi; Alpine co-host online
- Install cage + seat OpenRC dual chooser (VNC kiosk | aether panel)
- Mount Kingston with vault key; project = `/mnt/kingston-nixos/opt/mechanicall-os`
- Wire CURRENT.md + chat logs from Kingston
- GOP-style panel TUI; F1 PANEL / F2 SHELL as **pages** (same header, same compositor)
- Grok session chatter on panel (thinking via streaming-json)
- Shell default = personal-llm-sft-v4 on myarch Ollama for CURRENT propose drafts
- Fix shell↔panel so Ctrl+D does not kill cage

## Role inject
See `ROLE-GROK-SEAT-INJECT.md` (copied into `references/` and this folder).

## CURRENT rewrite
Rewritten for **seat-chat-comfort-loop** (INTEGRATE / ACTIVE). Prior Next `seat-nixos-efi-foundation` deferred until chat comfort APPROVED.

## Validation snapshots
- Grok headless: thinking + answer OK
- Ollama `personal-llm-sft-v4` from MBP → myarch:11434 OK
- `aether shell --smoke` OK after project chown
- Panel dual-page TUI deployed on Kingston python/

## Open risks
- Ollama must stay up on myarch for shell PEER
- Grok auth expiry → `grok login --device-auth`
- Kingston unplug unmounts project path
