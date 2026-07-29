# Session two — human / proposer / executor split (ACTIVE)

**Accepted:** 2026-07-29  
**Branch (SOT):** `session/client-one-s2-proposal-assistant` @ mechanicall-os  

## Roles

| Role | Project CURRENT | Next (now) |
|------|-----------------|------------|
| **Human** | all | approve / reject / panel authority |
| **Proposer** | `MODEL+RAG/personal-llm` | `spike-sample-quality-validation` (warm-up, not main) |
| **Executor / host panel** | `MODEL+RAG/rag-archive-manager` | `prespike-kingston-vm-host-investigation` |
| **Client surface** | `domains/house-tv-desk` | unchanged until client Next |

## Pre-spike (Kingston) — main operator tooling path

1. Investigate Kingston as **VM instance inside host OS**  
2. Host = IDE + agents; guest/panel = bare Mechanicall  
3. Build toward **hardcore TUI operator actually uses** (not final product)  
4. Artifact: `rag-archive-manager/artifacts/PRESPIKE-KINGSTON-VM-HOST.md`  

## Warm-up spike (personal-llm) — not main run

- Sample train-data quality → `personal-llm/artifacts/SPIKE-SAMPLE-QUALITY.md`  
- Model serve already proven; agents may run ollama without ceremony  

## Authority files applied
- `personal-llm/CURRENT.md`  
- `rag-archive-manager/CURRENT.md`  
- Matching `PROMPT.md` in each project  
