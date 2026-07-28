# Free frontier APIs for Mechanicall desk

**Product is still `CURRENT.md`.** These keys only feed **propose** (`aether desk` → `g`). Models never approve.

## Recommended (no credit card for free models)

### 1. OpenRouter (best default)

- Sign up: https://openrouter.ai — free models, one key, multi-provider.
- Create an API key; no card required for free-tier models.

```bash
export OPENROUTER_API_KEY="sk-or-..."
# optional pin:
export AETHER_MODEL="openrouter/free"
# or a specific free slug from openrouter.ai/models?q=free
export AETHER_LLM_PROVIDER=openrouter   # optional force

aether desk
# type to chat (default). /e edits CURRENT. /w saves last proposal.
```

### 2. Groq (fast open weights)

- https://console.groq.com — free tier, no card for standard free limits.

```bash
export GROQ_API_KEY="gsk_..."
export AETHER_MODEL="llama-3.3-70b-versatile"
# or: export AETHER_LLM_PROVIDER=groq
```

### 3. Already supported (paid / local)

| Env | Notes |
|-----|--------|
| `XAI_API_KEY` | Grok (paid) |
| `ANTHROPIC_API_KEY` | Claude (paid) |
| Ollama local | No key; `AETHER_OLLAMA_MODEL=...` |

Priority in `python/aether_llm.py`: **OpenRouter → Groq → Anthropic → xAI → Ollama**.

## Check

```bash
python3 python/aether_llm.py
# e.g. openrouter:openrouter/free
```

## Doctrine

- Output of `g` is **not** authority.
- Press `e` to edit `CURRENT.md` yourself.
- Optional: `w` writes `.aether/propose-CURRENT.md` for review.
- Do not put API keys in git.
