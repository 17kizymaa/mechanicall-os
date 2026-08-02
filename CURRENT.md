# CURRENT

**Objective:** Continuously integrate MBP Alpine seat features (panel + shell as one GOP-chrome app, Grok session chatter, personal-llm-sft-v4 peer on shell, Kingston project + CURRENT) until the operator is comfortable **chatting live on the seat** to draft/propose CURRENT edits — then lock the next Domain foundation Next.
**Phase:** INTEGRATE
**Status:** ACTIVE
**Baseline:** 2026-08-02 · MBP seat live on Alpine · Kingston nixos mounted · dual-page TUI · Grok TUI chat · Ollama sft-v4 on myarch LAN
**Next:** seat-chat-comfort-loop
**Approval:** PENDING

## Keep
- CURRENT.md sole Domain authority (filesystem truth); silence is never permission
- **Shell default model = personal-llm-sft-v4 (PEER)** via Ollama on the desktop (`OLLAMA_HOST`); propose-only — never write Domain itself
- **Panel default chatter = Grok Build session** (`grok login` + streaming-json **thinking** → answer) for operator conversation infrastructure
- Panel + shell are **one seat application** (shared GOP header; F1 PANEL / F2 SHELL pages — not separate processes that kill the compositor)
- Project root on Kingston: `/mnt/kingston-nixos/opt/mechanicall-os` when the stick is mounted on MBP
- PEER profile exclusivity: only personal-llm-sft-v4 wears PEER; Grok is technique/chatter outside PEER skill
- PEER drafts / proposes CURRENT edits; **human only** APPROVE/REJECT actualises Domain
- Seat development may proceed on Alpine MBP as the live integration host while NixOS portable stick remains the durable project FS
- Session logs under `dev/15_*` (and subsequent stage folders) for continuous integration memory

## Reject
- Soft Electron/REST seat as product workstation
- Model auto-writing CURRENT or automatic-approve
- Non-sft-v4 claiming PEER
- Killing cage/compositor when switching shell ↔ panel
- Dual concurrent Next
- Treating “not yet on pure NixOS seat host” as a hard stop on **chat comfort** work (foundation Next follows comfort)

## Limits
- One Next at a time
- Shell PEER must reach Ollama on myarch (`192.168.1.241:11434` / Tailscale later); if DOWN, surface clear error + recovery (`/ollama-host`, desktop `ollama serve`)
- Grok panel chatter needs valid `~/.grok/auth.json` (`grok login --device-auth` if expired)
- PEER never gets write-tools; propose text only
- Continuous integration ends when operator says chat workflow is comfortable — then pin next foundation Next

## Next allowed action
**Action id:** `seat-chat-comfort-loop`

Make the MBP seat **usable for daily Domain chat**:
1. Shell page talks to **personal-llm-sft-v4** by default (no error path when Ollama is up).
2. Operator can discuss **this CURRENT.md** with the peer model and receive **draft / PROPOSE edit text** (not auto-applied).
3. Panel remains Grok-session chat (thinking visible) for operator/Grok technique talk.
4. F1/F2 page switch stays one TTY/one compositor.
5. Log this integration stream under `dev/15_mbp-seat-gop-chat/` (SESSION + ROLE inject).

When operator is comfortable chatting here, human: `aether approve "seat-chat-comfort-loop"` and pin the following foundation Next (likely return to / advance `seat-nixos-efi-foundation`).

## Approval condition
Human: `aether approve "seat-chat-comfort-loop"` when:
1. Shell default peer chat works end-to-end (sft-v4 on desktop Ollama), and
2. Operator can run a short CURRENT discussion and get usable draft/propose text, and
3. Panel/shell page switch does not drop the seat compositor, and
4. This stage’s session log exists under `dev/15_mbp-seat-gop-chat/`.

Silence is never permission.

## Prohibited
- automatic-approve
- commit-secrets
- tws-in-this-domain
- personal-llm-as-authority
- invent-authority-md
- dual-concurrent-next
- peer-write-tools
- k8s-as-product-core
- electron-rest-seat-gui
- non-sft-v4-peer-profile
- model-auto-write-current
