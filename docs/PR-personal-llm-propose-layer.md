# PR draft — feat/personal-llm-propose-layer

**Branch:** `feat/personal-llm-propose-layer` → `master`  
**Open:** https://github.com/17kizymaa/mechanicall-os/pull/new/feat/personal-llm-propose-layer  

(Paste the body below into the GitHub PR form if `gh` is not authenticated.)

---

## Summary

Adds Mechanicall OS integration for the **local personal LLM** as an optional **propose-only** interface plugin (not an authority layer).

Day-1 MODEL+RAG work produced filtered train packs and Ollama tags. This PR wires how **aether garden/rival** pick and doctrine-inject that layer when present, and documents hard rules from the taste profile.

### Statement of changes

| Area | Change |
|------|--------|
| Architecture | Document optional personal-llm under Interface Layer (propose only; CURRENT + human approve remain sole authority) |
| `python/aether_llm.py` | Prefer personal-llm-sft-v2 → full:v1 → pilot over legacy customs; optional `AETHER_PERSONAL_LLM_SYSTEM`; soft flags for unsafe cmd / secret-like output |
| `references/personal-llm-system.txt` | Mechanicall doctrine SYSTEM (public, no weights) |
| `docs/PERSONAL-LLM-LAYER.md` | Placement, env, hard rules, what stays off-git |
| README / NOT-IMPLEMENTED | Operator quick env; explicit denial that weights are not in repo |
| Tests | `tests/test_aether_llm_personal.py` + hook in `tests/run.sh` |

### Explicitly not in this PR

- GGUF / PEFT / train JSONL / personal corpus
- Auto-approve or tool execution from model output
- Changing aether preflight/approve semantics

## Test plan

- [x] `python3 tests/test_aether_llm_personal.py`
- [x] `sh tests/run.sh` (full aether suite)
- [ ] Operator with Ollama: `AETHER_LLM_PROVIDER=ollama` + `AETHER_OLLAMA_MODEL=personal-llm-full:v1` → `aether garden status`
- [ ] Confirm `aether approve` still human-only (unchanged)
