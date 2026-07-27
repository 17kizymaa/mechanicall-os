# Personal LLM layer (optional propose substrate)

**Status:** shipped as **optional local layer** for Mechanicall OS · 2026-07-22  
**Authority:** still **CURRENT.md + human `aether approve` only** — the model never advances phase.

## Why it exists

Day-1 MODEL+RAG work produced a local personal assistant (QLoRA → GGUF/Ollama) trained on **filtered user/operator/rubric** text with Mechanicall doctrine in SYSTEM:

| Tag (local Ollama) | Role |
|--------------------|------|
| `personal-llm-full:v1` | Full-corpus QLoRA (richer; use with outer guards) |
| `personal-llm-sft-v2` | Filter-v2 clean corpus (preferred when import works) |
| `personal-llm-pilot:v0` | SYSTEM-hardened Llama fallback |

Weights and private train JSONL **do not live in this git repo**. This document + `python/aether_llm.py` wire **how Mechanicall uses** the layer when present.

## Placement in the architecture

```text
human
  └─ Interface (Markdown, shell, Grok/Claude)
       ├─ aether (Awareness / Control) — CURRENT, preflight, approve
       ├─ Filesystem substrate — truth
       └─ Personal LLM (optional Propose) ← this layer
            · drafts garden / rival / CURRENT seeds
            · refusal-shaped answers
            · never executes tools or aether approve
```

This is **not** a fourth authority layer. It is a **propose-only interface plugin** under the Interface Layer, same as garden/rival LLM helpers.

## Wiring

| Env | Effect |
|-----|--------|
| `AETHER_LLM_PROVIDER=ollama` | Force local Ollama |
| `AETHER_OLLAMA_MODEL=personal-llm-full:v1` | Pin tag |
| `AETHER_OLLAMA_HOST` | Default `http://127.0.0.1:11434` |
| `AETHER_PERSONAL_LLM_SYSTEM=1` | Prepend `references/personal-llm-system.txt` when no system message |

`aether_llm._ollama_pick_model` prefers, in order:

1. `personal-llm-sft-v2`  
2. `personal-llm-full:v1`  
3. `personal-llm-pilot:v0`  
4. `aetherOS-custom` / `anti-clown` / other  

Consumers: `aether garden`, `aether rival` (via `python/aether_llm.py`).

## Hard rules (from taste profile)

1. **Outer tool policy** — model text is never shell; never run suggested `aether approve` / `cryptsetup`.  
2. **Secret post-filter** — refuse/echo paths for `sk-` / PEM-like strings at the orchestrator when needed.  
3. **Facts from files** — finance, project state, RAG answers: inject from `CURRENT` / ledgers / archives; do not trust weights for ledger truth.  
4. **Dual control** — human or aether gate on any filesystem write.  
5. **Silence ≠ permission** — model agreement is not approval.

## What stays out of git

- GGUF / PEFT adapters / HF caches  
- Train JSONL with personal content  
- Kingston vault paths / unlock material  
- API keys  

Operator keeps those under `~/MODEL+RAG/personal-llm/` (or private disk).

## Install model locally (operator)

```bash
# when a GGUF is available and Ollama accepts it:
ollama create personal-llm-full:v1 -f /path/to/Modelfile.personal-llm-full-v1

export AETHER_LLM_PROVIDER=ollama
export AETHER_OLLAMA_MODEL=personal-llm-full:v1
aether garden status   # should show ollama:personal-llm-…
```

## Provenance (private ops, not required to clone)

- logos `source-packs/20260722-filter-v2/` — filter-first SFT candidates  
- personal-llm `artifacts/derived/models/qlora-*` — train/merge reports  
- finance `logs/2026-07-22-personal-llm-taste-profile.md` — behavioral map  

## Non-goals

- Replacing `aether` authority  
- Multi-tenant hosted personal models  
- Shipping weights in GitHub releases  
- Auto-approve or tool execution from model output  
