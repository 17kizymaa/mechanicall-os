# Free frontier APIs for Mechanicall shell / garden / rival

**Product is still `CURRENT.md`.** These keys only feed **propose** surfaces
(`aether shell`, garden/rival; desk removed). Models never approve.

## Toggleable presets

Named presets live in `python/aether_llm.py` (`LLM_PRESETS` / `PRESET_CYCLE`).

| Preset | Provider | Default model | Notes |
|--------|----------|---------------|--------|
| **`coding`** | openrouter | `qwen/qwen3-coder:free` | Free coding compute (default free path) |
| `coding_alt` | openrouter | `agentica-org/deepcoder-14b-preview:free` | Free coding alt |
| `free` | openrouter | `openrouter/free` | Free model router |
| `llama_free` | openrouter | `meta-llama/llama-3.3-70b-instruct:free` | Free Llama 70B |
| `groq` | groq | `llama-3.3-70b-versatile` | Groq free tier (own key) |
| **`sonnet35`** | openrouter | `anthropic/claude-3.5-sonnet` | Via OpenRouter (credits may apply) |
| `sonnet35_direct` | anthropic | `claude-3-5-sonnet-latest` | Anthropic API key |
| `sonnet` | anthropic | `claude-sonnet-5` | Newer Sonnet |
| **`ollama`** | ollama | auto (personal-llm preferred) | Local |
| `grok_tui` | grok_tui | `grok-4.5` | `grok login` session (preferred Grok) |
| `xai` | xai | `grok-4.5` | Raw `XAI_API_KEY` (below TUI) |

### Shell

```bash
aether shell
/provider list                 # show all
/provider next                 # cycle coding → … → sonnet35 → ollama → …
/provider coding               # free OpenRouter coder
/provider sonnet35             # Claude 3.5 via OpenRouter
/provider ollama               # local
/model <openrouter-slug>       # pin model, keep provider
/preset-save                   # write .aether/llm-preset
```

CLI:

```bash
aether shell . --preset coding
aether shell . --provider sonnet35
python3 python/aether_llm.py presets
python3 python/aether_llm.py preset coding
```

### Panel

- **[m] Toggle LLM preset (next)** — cycles and saves `.aether/llm-preset`
- **[u] Pick LLM preset…** — type `coding`, `sonnet35`, `ollama`, …

### Project pin

```
.aether/llm-preset    # one line: coding | sonnet35 | ollama | …
```

Loaded automatically when `aether shell` starts in that project.

## Keys

### 1. OpenRouter (best free multi-model)

- https://openrouter.ai — free models, one key.

```bash
export OPENROUTER_API_KEY="sk-or-..."
export AETHER_LLM_PRESET=coding          # or free / coding_alt / llama_free
# optional pin over preset default:
# export AETHER_MODEL="qwen/qwen3-coder:free"
```

Free slugs change; if a `:free` model 404s, `/model` to another free slug from
https://openrouter.ai/models?q=free or cycle `/provider free`.

### 2. Groq

```bash
export GROQ_API_KEY="gsk_..."
/provider groq
```

### 3. Anthropic (Sonnet 3.5 / 5)

```bash
export ANTHROPIC_API_KEY="..."
/provider sonnet35_direct   # 3.5
/provider sonnet            # sonnet 5
```

### 4. Ollama (local)

```bash
# ollama serve + pull personal-llm or any tag
/provider ollama
# or: export AETHER_OLLAMA_MODEL=personal-llm-sft-v4
```

### 5. Grok

| Path | How |
|------|-----|
| **TUI (preferred)** | `grok login` → preset `grok_tui` |
| Raw API | `XAI_API_KEY` → preset `xai` |

**API compute &lt; Grok TUI compute.**

## Auto resolution order (no preset)

When nothing is forced: **grok_tui → openrouter → groq → anthropic → xai → ollama**.

## Check

```bash
python3 python/aether_llm.py
# e.g. [coding] openrouter:qwen/qwen3-coder:free
```

## Doctrine

- Model output is **not** authority.
- Do not put API keys in git.
- Silence is never permission.
