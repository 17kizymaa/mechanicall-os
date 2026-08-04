# AUTHORITY

**Product:** Mechanicall OS  
**Repo:** mechanicall-os  
**Version:** v1.2b  
**Status:** stable  
**Date:** 2026-08-01  

This file is **durable doctrine**. It does not replace `CURRENT.md`.  
`CURRENT.md` is the only live gate for Next / Prohibited / Approval.  
Personal LLM may propose under Domain; it never owns this file or CURRENT.

---

## 1. Local-first project control layer

- Authority is local-first: `CURRENT.md` + PERSONAL-LLM (as technique under Domain) are the control surface for agent work.
- Every operator has one authority node for this product context:
  - one `CURRENT.md` (live)
  - one `AUTHORITY.md` (durable doctrine)
- No Kingston unlock/write.
- No train on vault `raw/`.
- No logos source-pack rewrites.

## 2. Code vs context

- **Code:** applications direct the architecture. Produce first; fork distribution later. If code cannot be copied, prune with instability in mind.
- **Context:** everything else feeds `CURRENT.md` as the human-owned live authority — not chat transcripts, not model memory.

## 3. Security posture

- Secrets managed securely: rotate offline; do not echo keys in chat.
- Redact sensitive data in logs and shared notes.
- Preflight and human approve remain the consequential gate (`aether preflight`, `aether approve`).

## 4. Authority separation

| Artifact | Role | Overrides CURRENT? |
|----------|------|--------------------|
| `CURRENT.md` | Live Next / Prohibited / Phase | — (gate source) |
| `AUTHORITY.md` | Durable doctrine | **No** |
| `DECISIONS.md` | Append-only decision log | **No** |
| `.context.md` | Descriptive inventory | **No** |
| Personal LLM | Propose / taste only | **No** |
| Chat / session logs | Evidence | **No** |

## 5. Mode boundaries (do not merge)

### Mode A — Mechanicall OS work (this CURRENT)

Local-first project control layer for CURRENT + PERSONAL-LLM under Domain.  
Owned by repo-root `CURRENT.md` / this `AUTHORITY.md`.

### Mode B — TWS paper work (separate context)

Draft paper under a dedicated `TWS_PAPER/` (or other path) with its **own** CURRENT if authority is needed.  
Not part of this repo's live Next. Smoke tests: free API or sandbox only; log to that workspace.

### Mode C — Trading discipline

Trade ≤£200 max per session; hard stop at £200 loss.  
From this agent session: **write receipts only; do not execute trades.**

### Mode D — CURRENT hygiene (anti-clown)

Do not invent pack chrome: no `source:`, `filter:`, `keep-clean`, or `ai_score` headers.  
Keep CURRENT clean and boringly absolute on doctrine and Next.

## 6. Personal LLM (technique under Domain)

- Base LLM = substrate  
- Personal LLM = technique (voice, taste, doctrine-shaped refusals)  
- CURRENT / aether = Domain (binding Next + Prohibited)  
- Human approve = only actualisation of consequential change  

Personal LLM is never authority. See `docs/PERSONAL-LLM-DEFINITION.md`.

## 7. Non-goals (product)

See `NOT-IMPLEMENTED.md`. No PostgreSQL, pgvector, LangGraph “Cortex,” sandboxed multi-agent studio, or industrial autonomous OS claim as shipped product.

---

Silence is never permission. LLMs may propose; only humans approve.
