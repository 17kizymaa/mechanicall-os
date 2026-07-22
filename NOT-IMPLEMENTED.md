# NOT IMPLEMENTED — Explicit Denial List

**Last updated:** 2026-07-22 (personal-llm propose layer docs; weights still off-repo)

This file exists so no operator, investor, agent, or README can honestly claim
these components are part of Mechanicall OS today.

If you find a claim that contradicts this file, the claim is wrong.

## Product positioning (what *is* real)

**Mechanicall OS** (repo: `mechanicall-os`) is a **local-first project control
layer** for human–agent work:

- filesystem substrate (plain folders + Markdown/JSON sidecars);
- POSIX `aether` shell CLI;
- capture (`seed` / `session`), optional LLM helpers (`garden`, `rival`);
- v0.2 authority layer: `CURRENT.md`, preflight gates, approval/reject events,
  append-only `.aether/events.jsonl`, artifact registration.

It is **not** an industrial autonomous agent platform.

## Invented / absent components

| Claimed component | Status |
|---|---|
| Private `17kizymaa/mechanicallOS` monorepo as described in external PDFs | **Not this repo** (public `mechanicall-os`) |
| `src/` tree / `src/os_layer/graph.py` | **Does not exist** |
| LangGraph orchestration | **Not implemented** |
| PostgreSQL + pgvector | **Prohibited by architecture; not implemented** |
| `WORKSPACE` / `EXECUTION_DAG` / `NODE_CHECKPOINT` / `AGENT_STATE` tables | **Do not exist** |
| `SEMANTIC_MEMORY` vectors | **Not implemented** |
| “Cortex” central orchestrator | **Not implemented** |
| “Ganglion” agent runtime | **Not implemented** |
| Sandboxed tool execution platform | **Not implemented** |
| Shipping personal-llm **weights** / GGUF / train JSONL in this repo | **Not in git** — optional local Ollama only; see `docs/PERSONAL-LLM-LAYER.md` |
| Model self-approve / auto `aether approve` | **Prohibited forever** |
| Mandatory Critic validation on every action | **Not implemented** |
| Sliding-window anchor retrieval | **Not implemented** |
| Holographic state | **Not implemented** |
| Synaptic pruning | **Not implemented** |
| Reflex-arc routing | **Not implemented** |
| Autonomous video-editing agent | **Not implemented** |
| Deterministic ACID workflow engine | **Not implemented** |
| Industrial-grade fault tolerance claims | **Unsupported** |
| Multi-user collaboration platform | **Not implemented** |
| Web dashboard / microservices / event bus | **Not implemented** |
| General-purpose DAG editor | **Not implemented** |
| “Hippocampus” summarisation subsystem | **Not implemented** |

## Architecture non-goals (still locked)

From `ARCHITECTURE.md` and `CORE_PRINCIPLES.md`:

- No special workspace databases.
- No persistent hidden stores.
- No vector databases or embedded search indexes as core truth.
- No FastAPI / SQLAlchemy / LangChain in core.
- Durable truth is the filesystem (`cat`, `grep`, `git diff`).

## Biological vocabulary

Terms like cortex, ganglion, synapse, hippocampus remain **metaphor only** until
each name points at an implemented, testable mechanism. Do not use them in
README product claims.

## Speculative archive

External PDFs and speculative write-ups, if retained, belong under
`research/speculative/` with a prominent **FICTIONAL / NOT IMPLEMENTED** header.
They are concept material, not acceptance criteria.

## Condition that must remain true

> The product must prove that it can **stop one wrong action** before it adds
> machinery for performing more actions.
