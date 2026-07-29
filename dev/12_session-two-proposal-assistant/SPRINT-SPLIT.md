# Session two — human / proposer / executor split (ACTIVE)

**Accepted:** 2026-07-29  
**Branch (SOT):** `session/client-one-s2-proposal-assistant` @ mechanicall-os  

## Roles

| Role | Project CURRENT | Next (now) |
|------|-----------------|------------|
| **Human** | all | approve / reject / panel authority |
| **Proposer** | `MODEL+RAG/personal-llm` | `retrain-sft-v3-data-freeze` (retrain authorized) |
| **Executor / host panel** | `MODEL+RAG/rag-archive-manager` | **PARKED** (`none-parked`) — huge Domain program later: rebase projects + low-overhead **VM human UI** |
| **Client surface** | `domains/house-tv-desk` | `desk-p0-verify-ci` / Desk product |

## rag-archive-manager — PARKED (2026-07-29)

Human park: overhead clear for now.  

**When resumed, this is a large Domain project**, not a panel spike:

1. **Rebase / realign** projects under the archive-host Domain story  
2. Design **low-overhead human UI** that **launches inside a VM**  
3. Host = agent IDE; VM = human Domain interface  

Pre-spike notes remain: `PRESPIKE-KINGSTON-VM-HOST.md`, `PANEL-V0-CHALLENGE.md`.  
Do **not** continue `implement-operator-panel-v0` until CURRENT is unparked.

## Active tracks while park holds

- **personal-llm:** retrain path (`retrain-sft-v3-data-freeze` …)  
- **house-tv-desk / Desk:** P0 verify CI + product honesty  
- **Human:** approve / client sessions  

## Authority files
- `personal-llm/CURRENT.md` — active  
- `rag-archive-manager/CURRENT.md` — **PARKED**  
- `domains/house-tv-desk/CURRENT.md` — Desk product

## Staged from personal-llm (not merged)

- Deploy ops / session-boot **menu** (review only): `MODEL+RAG/personal-llm/ready-to-move_dev.md/`
- Destination when human moves: this folder (`dev/12_session-two-proposal-assistant/`), branch `session/client-one-s2-proposal-assistant`
- Exact session boot logic: **not decided** in that pack
