# NOT IMPLEMENTED — Explicit Denial List

**Last updated:** 2026-08-04 (peer-review absorb: scope to **Mechanicall core**)

This file exists so no operator, investor, agent, or README can honestly claim
these components are part of **Mechanicall core** today.

If you find a claim that contradicts this file, the claim is wrong.

**Scope:** Unless a row says otherwise, denials apply to **Mechanicall repository
core** (local `aether` + CURRENT protocol). Adjacent surfaces must be labeled
explicitly in `PRODUCT.md`:

| Surface | How to talk about multi-user |
|---------|------------------------------|
| Mechanicall core | Not a multi-user collaboration platform |
| anphuni.com Session | Separate **capped hosted alpha** (≤5 seats) — **is** multi-seat hosted; **not** open SaaS |
| Club-cortex | Research only |

**Operator direction ≠ shipped core.** Product shape research (“club-cortex”,
multi-LoRA club scale) lives under `research/speculative/`. Those files do
**not** authorize open multi-tenant SaaS or auto-train claims.

## Product positioning (what *is* real)

**Mechanicall OS** (repo: `mechanicall-os`) is a **local-first authority
protocol** for human–agent work:

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
| Multi-user collaboration platform **as Mechanicall core** | **Not implemented** |
| Club multi-user backend (queues, multi-adapter host, retainers) | **Not implemented** — direction only: `research/speculative/CLUB-CORTEX-SHAPE.md` |
| Multi-tenant SaaS chat / infinite concurrent AI desktop | **Prohibited product claim** for core |
| anphuni Session (≤5 hosted seats + agent) | **Adjacent alpha lab** — not core release; document as hosted multi-seat, not “no multi-user at all” |
| Web dashboard / microservices / event bus **as core** | **Not implemented** |
| Branded product SaaS dashboard | **Not implemented** — optional local **Project Panel** TUI is `aether panel` |
| Always-on multi-tenant web control plane | **Not implemented** (Session is capped alpha, not a general control plane) |
| General-purpose DAG editor | **Not implemented** |
| “Hippocampus” summarisation subsystem | **Not implemented** |
| Authenticated human identity for approve/reject | **Not implemented** (protocol rule only) |
| Sandbox that blocks skip-preflight agents | **Not implemented** |
| **Sovereign operator TUI bound to Domain** | **Not implemented** — see below |
| Grok CLI (or any external AI TUI) as Domain-gated shell | **Not implemented** — third-party product |
| Force Grok / Cursor / etc. to preflight before edits | **Not implemented** |
| Single integrated “live in panel, talk to model” product surface | **Partial** — Panel/Session are cooperative CURRENT-visible UIs; not forced Domain enforcement |
| Enforced “Domain shell” that cannot skip preflight | **Not implemented** — use “CURRENT-visible cooperative agent shell” |
| **Single-app appliance distro default** (boot → only seat UX) | **Scaffold only** — `seat-kiosk` module + `docs/SINGLE-APP-DISTRIBUTION.md`; not default on Kingston |

## Operator TUI is not sovereign (logical gap)

**Operator fact (2026-07-30):** the TUI the operator *typically works from* is
**Grok** (xAI CLI / session UI), not `aether panel`.

**What the architecture implies vs what practice is**

| Claim / marketing | Reality |
|---|---|
| `CURRENT.md` + preflight are live authority | True **only when something actually consults them** |
| `aether panel` is the human plan / yes-no surface | Exists; often **not** the primary seat of attention |
| Grok is “the AI you talk to” beside the plan | In practice Grok **is** the operator’s main TUI |
| Dual-tool split is intentional and sufficient | Insufficient if the primary TUI never binds Domain |

**Why this is a flaw (not a taste preference)**

Domain sovereignty is not “a file exists.” It is “the control surface from which
work is directed cannot silently bypass Next / Prohibited / silence≠permission.”

If the primary operator TUI is **outside** Mechanicall (Grok, Cursor, raw shell
agent sessions, …), then:

1. **Technique and chat feel like the product** — they propose, edit, and
   sequence work without mandatory preflight.
2. **Panel becomes optional ceremony** — used after the fact or not at all.
3. **Filesystem authority is real but non-sovereign in practice** — it binds
   only when the human *chooses* to leave the external TUI and honour CURRENT.

That is a **control-surface gap**: architecture claims Domain sovereignty;
daily operation runs through a non-Domain TUI. Calling panel “the” authority UI
while living in Grok is self-contradictory until one of:

- the primary TUI is **panel** (or a Domain-bound shell), or  
- external TUIs (Grok, …) are **integrated or wrapped** so they read CURRENT,
  refuse outside Next, and never imply approve, or  
- docs **stop claiming** a sovereign in-product operator TUI and admit:
  “Domain is filesystem protocol; operator seat is external; honour is social.”

**What *is* implemented**

- `CURRENT.md`, `aether preflight` / `approve` / `reject`, events.jsonl  
- `aether panel` Project Panel TUI (files + shells to aether only)  
- Docs that **recommend** panel = plan, grok = talk (e.g. client-one GROK-INSTALL)

**What is *not* implemented**

- Making Grok (or any preferred external TUI) **Domain-sovereign**  
- Blocking consequential agent work that never opened CURRENT  
- A single product surface that is both “where I live” and “bound to Next”

**Fidelity gates (sft-v4 / personal technique — 2026-07-30)**

These remain binding for *models* and *docs*; they do **not** fix the TUI gap:

| Gate | Implication for this gap |
|------|---------------------------|
| CURRENT is authority | External TUI output is never authority |
| Propose only | Grok sessions must not be narrated as approve |
| Silence ≠ permission | Leaving CURRENT unchanged is not green-light |
| Technique ≠ Domain | Grok / personal-llm / sft-v4 are technique or foreign UI, not Domain |
| No secret echo / no vault unlock from model | Still required; external TUI is higher leak risk |
| Probes ≠ security certification | Passing taste tests does not make Grok Domain-safe |

sft-v4 consult note: model framed “TUI not sovereign” as mere UX; **operator
correction accepted** — if the primary seat of work is unbound, Domain is not
sovereign in the full architectural sense. Document honesty > marketing dual-tool
story.



**Research pointer (2026-07-30):** open-source fork/extract options for a Domain-bound
operator shell (MIT/Apache preferred) are catalogued in
`dev/14_client-one-and-technique/output/RESEARCH-OPEN-SOURCE-SOVEREIGN-TUI.md`.
Panel “Open Grok” is launch-and-return only — **not** a Domain wrap of Grok.

**Until this is closed, honest product language is:**

> Mechanicall provides a **filesystem Domain protocol** and an **optional**
> panel. It does **not** yet provide a **sovereign operator TUI**. If you
> operate from Grok (or similar), you are outside the product boundary unless
> you voluntarily honour CURRENT.

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
