# Exemplar: propose a CURRENT.md change (human applies)

Optional interface path for “development applications”: draft a proposed
authority update from a reflection. **Never auto-approves.**

## Without a model

Copy `PROPOSE-TEMPLATE.md`, fill sections by hand, then edit `CURRENT.md`
yourself or run `aether current` after applying.

## With optional local personal LLM

When Ollama + a personal tag is available (weights not shipped in this repo):

```bash
export AETHER_LLM_PROVIDER=ollama
export AETHER_PERSONAL_LLM_SYSTEM=1
# Use garden/rival or a future propose helper — output is draft only.
```

Required output fields (from DISTRIBUTE alpha guidance):

1. Observations  
2. Inferences  
3. Unknowns  
4. Proposed CURRENT change  
5. Conflicts with existing authority  
6. Human decision required  

Human then edits `CURRENT.md` and, when ready, runs `aether approve` themselves.

See [docs/PERSONAL-LLM-LAYER.md](../../docs/PERSONAL-LLM-LAYER.md).
