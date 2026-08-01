# PROPOSE — control-layer seats (harden-control-layer-seats)

**Status:** proposal (not auto-approved)  
**Domain Next:** `harden-control-layer-seats`  
**Date:** 2026-07-31  
**Authority:** CURRENT.md only · personal-llm is technique only  

---

## Intent

Make **local-first project control** the daily path for Mechanicall OS:

| Seat | Role | Default |
|------|------|---------|
| **CURRENT.md** | Sole Domain law | Always |
| **`aether panel`** | Human gates + CURRENT always (right) + Domain chat (left) | Fullscreen TUI |
| **`aether shell`** | Domain-bound agent REPL | **peer** = personal-llm-sft-v4 |
| **personal-llm** | Propose / synthesis peer | Not co-authority |
| **Grok agent** | Real implementer (`/agent grok`) | Opt-in |

TWS / trading stays **out** of this Domain (own CURRENT root later).

---

## Already shipped (PR #2)

- `feat/domain-shell-panel-tui` → https://github.com/17kizymaa/mechanicall-os/pull/2  
- Shell dual agents + remote Ollama path  
- Panel dual-pane TUI (scroll fix)  
- Desk removed from product surface  
- Ollama nix LAN bind for serving weights on this host  

---

## Proposed completion checklist (Next)

1. **Dogfood seats daily**
   - `aether panel .` (TTY) for Approve / CURRENT rail / chat  
   - `aether shell .` for peer synthesis + preflight  
   - `/agent grok` only when implementing under Next  

2. **Land product branch**
   - Merge PR #2 to `master` after review  
   - Keep session/* branches out of this merge  

3. **Document one-page operator path**
   - README pointer: panel + shell + CURRENT (no desk)  
   - Link `docs/PANEL-GROK-SPLIT.md`, `docs/AETHER-SHELL.md`, `docs/PERSONAL-LLM-PEER-REPL.md`  

4. **Collaborator fork (later Next)**
   - Re-pin Next to `collaborator-fork-review` after merge  
   - Not concurrent with trade modes  

5. **Explicit non-goals this Next**
   - No TWS / live trades in this Domain  
   - No AUTHORITY.md co-truth  
   - No peer write tools  

---

## Acceptance (human)

- [ ] Panel TUI usable on a real terminal (not CLI-only)  
- [ ] Shell peer answers under CURRENT; preflight works  
- [ ] PR #2 merged or explicitly parked with reason  
- [ ] Root CURRENT Next still single pin  

**Approve when done:**  
`aether approve "harden-control-layer-seats"`

---

## Publicise note

This proposal + CURRENT snapshot are for GitHub product branch public review — **no secrets** in tree.
