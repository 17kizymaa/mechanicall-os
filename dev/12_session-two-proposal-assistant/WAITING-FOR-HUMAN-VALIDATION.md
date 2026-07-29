# Waiting for human validation — do **not** rewrite CURRENT yet

**Status:** PARKED pending operator think-through  
**Date:** 2026-07-29  
**Branch:** `session/client-one-s2-proposal-assistant`  
**Rule this turn:** **No edits** to any project `CURRENT.md` until human validates in chat.

---

## Ready checklist (agent)

| Item | State |
|------|--------|
| Session-two branch exists + pushed | yes · `origin/session/client-one-s2-proposal-assistant` |
| Propose file for personal-llm written | yes · `MODEL+RAG/personal-llm/artifacts/PROPOSE-CURRENT-SESSION-TWO.md` |
| CURRENT files left untouched this turn | **yes** (gate) |
| Plan below for human alignment | this file |
| First spike scoped as non-main | sampling quality validation only |

**Ready for your validation.** Next turn after you approve the *shape*: rewrite the respective CURRENT.md files only as you specify.

---

## Intended three-way split (your aether panel / workflow)

Clean separation so panel stays usable sprint-long:

```text
┌─────────────────────────────────────────────────────────────┐
│ HUMAN  (Domain actualisation)                               │
│  · owns CURRENT.md edits + aether approve / reject          │
│  · aether panel actions that mutate authority               │
│  · client-facing yes/no on proposals                        │
└─────────────────────────────────────────────────────────────┘
          ▲                              ▲
          │ review                       │ review
┌─────────┴──────────┐        ┌─────────┴──────────────────────┐
│ PROPOSER           │        │ EXECUTOR                       │
│ (innate technique) │        │ (implementation agent)         │
│ · personal-llm     │        │ · grok / session agent         │
│   sft-v2 / full    │        │ · code, scripts, mounts        │
│ · garden / desk    │        │ · never aether approve         │
│ · PROPOSE-*.md     │        │ · preflight + CURRENT Next     │
│ · interjections    │        │ · emits artifacts for review   │
│ · never approve    │        │                                │
└────────────────────┘        └────────────────────────────────┘
          │                              │
          └──────────► filesystem ◄──────┘
                 mechanicall-os = source of truth build
                 MODEL+RAG projects = domain CURRENTs
```

| Role | Primary cwd / project | Panel use |
|------|----------------------|-----------|
| **Human** | any · panel for approve | `aether panel` · approve/reject only as human |
| **Proposer** | `MODEL+RAG/personal-llm` (+ client domains for language) | propose CURRENT / garden; optional Desk |
| **Executor** | `~/mechanicall-os` on session branch | implement Next only; write PROPOSE or output/ for human |

**Awareness:** `aether watch` / events = observe FS; interjections = **propose files**, not auto-Next.

---

## Host / source-of-truth assumption

| Layer | Path | Role |
|-------|------|------|
| **Core SOT build** | `/home/anphuni/mechanicall-os` | aether, desk, panel, nix flake — **checkout latest session branch here** |
| **Personal technique project** | `/home/anphuni/MODEL+RAG/personal-llm` | CURRENT for technique + Kingston-related propose |
| **Archive / RAG project** | `/home/anphuni/MODEL+RAG/rag-archive-manager` | CURRENT for archive policy + **Kingston boot validation ownership** (planned) |
| **Client surface** | `mechanicall-os/domains/house-tv-desk` | Client-one CURRENT-as-product Desk |

**Planned:** Kingston **boot validation** lives under **rag-archive-manager** CURRENT (vault/archive host narrative), not only personal-llm — so personal-llm can move to proposal-assistant Next without dual-wielding boot ceremony.

*(Environment was set up for portable host + seed; formal CURRENT reassignment waits on your validation.)*

---

## Draft CURRENT rewrites (NOT APPLIED — for alignment only)

### A. `personal-llm/CURRENT.md` (after you say go)

- Objective: innate technique ON · sft-v2 propose assistant · client CURRENT-as-product  
- Park or drop sole ownership of Kingston boot validation  
- Next: e.g. `wire-sft-v2-proposal-assistant` or your refined spike list  
- See full draft: `artifacts/PROPOSE-CURRENT-SESSION-TWO.md` (may still revise)

### B. `rag-archive-manager/CURRENT.md` (after you say go)

- **Add / own:** Kingston portable host **boot validation** (OPERATOR-BOOT, PHASE-2-VALIDATION)  
- Keep archive/RAG pipeline duties  
- Next: e.g. `human-operator-boot-validation` **or** `host-sot-mechanicall-checkout` then validation  
- Explicit: mechanicall-os on stick/host is SOT for aether binary; this project validates *use* of host + vault/archive access  

### C. Client-one `house-tv-desk/CURRENT.md`

- Only if you want session-two client Next aligned; otherwise leave promo CURRENT until client spike  

---

## Early spikes (align before CURRENT freeze)

Order is **proposal for discussion** — not authority.

| # | Spike | Owner role | Main run of session? |
|---|--------|------------|----------------------|
| **S0** | Human validates CURRENT rewrite shape | Human | gate |
| **S1** | **Sample training data for quality validation** (logos sampler / filter reports; small N; write SAMPLE-QUALITY note) | Proposer + light Executor | **NO — warm-up only**, not the main session responsibility |
| **S2** | Checkout latest `session/client-one-s2-proposal-assistant` (or agreed tip) on mechanicall-os; `aether panel` smoke on a clean project | Executor | setup |
| **S3** | Apply accepted CURRENTs (personal-llm + rag-archive-manager) | Human | authority |
| **S4** | Wire sft-v2 env + document propose-interjection path (PROPOSE-*.md only) | Executor | core sprint candidate |
| **S5** | Kingston boot validation under rag-archive-manager Next (if still open) | Human + Executor docs | parallel |
| **S6** | Client-one CURRENT-as-product loop (Desk) steered by journaled client goals | Human + Proposer | client-facing |

### S1 detail (first spike, **not** the main run)

- **What:** Pull a **small sample** from training-data sampler manifests / existing filter reports; score or spot-check quality dimensions (PII risk, junk, voice fit).  
- **Output:** e.g. `personal-llm/artifacts/SPIKE-SAMPLE-QUALITY.md` (or sampler artifacts).  
- **Not responsible for:** full retrain, full corpus rebuild, shipping weights, client delivery.  
- **Why first:** proves proposer+executor file loop without touching Domain approve.

---

## What we will **not** do until you validate

- Rewrite any `CURRENT.md`  
- Run `aether approve`  
- Start S1–S6 execution as if Next already moved  
- Merge experimental disclaimers into authority without your word  

---

## What you can do next (human)

1. Think through objectives / which spikes are sprint-main vs warm-up.  
2. Reply with validation notes (e.g. “S1 ok as warm-up; Kingston → rag-archive-manager; personal-llm → propose assistant”).  
3. **Next agent turn:** rewrite the respective CURRENT.md files **only then**.  

---

## One-line readiness

**Ready.** Holding authority files. Plan includes Kingston validation under rag-archive-manager, mechanicall-os as SOT, human/proposer/executor split, and sample-quality as a **non-main** first spike. Your think-time is the gate.
