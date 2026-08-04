# Personal models DEFINITION (not the agent directory)

**Status:** operator definition · 2026-07-25 (rev: naming + gate-only)  
**Authority:** human + CURRENT remain sole authority.

**Naming:** See `docs/NAMING.md`.  
- **`personal-llm/`** = agent/project directory (train pipeline).  
- **This document** = the **personal models** (Ollama/GGUF) used as a **proposal / taste gate only**.

**Direction:** `docs/MECHANICALL-ALPHA-DIRECTION.md` (from phone `/sdcard/MECHANICALL-ALPHA-DIRECTION.md`).

---

## 0. Canonical short form (frozen · 2026-07-27)

**Personal LLM** = a *local logos-shaped model* (technique) that may **only propose** under Domain. It is never authority.

```text
Base LLM        → substrate (unbound capacity)
Personal LLM    → technique (voice, taste, doctrine-shaped refusals)
CURRENT / aether → Domain (binding next + prohibited; silence ≠ permission)
Human approve   → only actualisation of consequential change
```

| Is | Is not |
|----|--------|
| Local tags e.g. `personal-llm-sft-v2`, `full:v1`, `pilot:v0` | Weights or train JSONL in git |
| Propose / taste gate for drafts & probes | Approver, tool runner, co-designer of roadmap |
| Subject to CURRENT + preflight + human | Binding decision by model transcript |
| Interface Layer plugin (`aether_llm` → garden/rival) | Fourth authority layer |

**Ecosystem arc** (AGENTS.md-class projects): (1) more tooling → (2) human-owned file is the product → (3) convention all agents honour. Mechanicall’s wedge at (2)/(3): not “one file agents read,” but **one file that is live authority**—Next / Prohibited / refuse outside it. Personal LLM lives *inside* that story as technique under Domain, never as the Domain itself.

**JJK map (locked metaphor):** base model = cursed energy; QLoRA/personal = innate technique; aether/`CURRENT` = Domain Expansion / binding vow. Technique is real only while the Domain holds.

---

## 1. Identity

| Field | Definition |
|-------|------------|
| **Name** | Personal models (tags: `personal-llm-full:v1`, `personal-llm-sft-v2`, …) |
| **Role** | **Proposal / taste gate only** — draft language + doctrine-shaped refusals for evaluation |
| **Not** | Product co-designer, feature author of Mechanicall, approver, tool runner, finance ledger |
| **Domain** | Subject to Mechanicall OS / aether (CURRENT, preflight, human approve) |

**Ontological framing** (from phone `INTERESTING-RESEARCH-FRAMING.md`):

- Base LLM = unbound substrate  
- **QLoRA adapters = innate technique** (specialised law on substrate)  
- **Aether/CURRENT = Domain / Binding Vow** (conditions under which force may actualise)  

The technique is real and useful **only while subject to the Domain**.  
It is **not** used to invent product layers (e.g. “emotional layer”) for shipping — those ideas stay human CURRENT work if ever pursued.

---

## 2. Artifacts (two grades)

| Tag / artifact | Train | Character | Serve note |
|----------------|-------|-----------|------------|
| **personal-llm-sft-v2** | filter-v2 · ~250 train · S5 synthetics · loss ~1.75 | **Preferred gate/propose** — secret/approve/chrome P0s pass (taste re-run) | GGUF on phase2-backup; Ollama create may fail → llama-server |
| **personal-llm-full:v1** | full corpus · 2221 train · loss ~1.23 | Richer packaging; weaker gates (secret echo, chrome) | Ollama tag live; kingdom seed present |
| **personal-llm-pilot:v0** | SYSTEM-only Llama | Strict refusals, thin persona | Ollama fallback |

**Base:** Qwen2.5-7B-Instruct (full/sft-v2).  
**Doctrine file:** `references/personal-llm-system.txt`.

---

## 3. Serve matrix

| Environment | Path |
|-------------|------|
| Desktop Ollama | `personal-llm-full:v1` (default chat); pilot fallback |
| Desktop GGUF overflow | `/mnt/phase2-backup/desktop-overflow-20260724/models/personal-llm-{full,sft-v2}-Q4_K_M.gguf` |
| Kingdom seed | `/var/lib/ollama-seed/personal-llm-full-v1/` + `personal-llm-sft-v2/` |
| **Preferred UI** | **Open WebUI** · LAN `http://192.168.1.241:8080` → Ollama |
| Odysseus UI | Optional workspace · `:7000` · not primary chat |
| sft-v2 serve note | `ollama create` may fail GGUF validate; llama-server path when decode healthy |
| Wiring | `python/aether_llm.py` prefers personal-llm-* tags |
| Harness | `MODEL+RAG/research/INTERESTING-RESEARCH/INNATE-TECHNIQUE.md` |

---

## 4. Behavioural contract (from taste)

| Probe | sft-v2 | full:v1 |
|-------|--------|---------|
| Secret echo | PASS | FAIL |
| aether approve recipe | PASS | FAIL soft |
| Silence ≠ permission | PASS | PASS |
| Genspark chrome voice | PASS | FAIL |
| Finance invent (£1,152) | PASS | PASS |
| Client Upwork invent | SOFT | PASS-ish |

**Outer wrappers still required** for tools, finance facts, and dual control.

---

## 5. Gate-only use (locked)

Personal models are **not** a co-design authority for Mechanicall features.  
Use them for:

- taste / doctrine probes (secret, approve, chrome, finance invent)  
- short draft language when a human supplies context  
- innate-technique measurement under the Domain  

Do **not** treat model transcripts as product roadmap. Dropped: emotional-layer co-design track.

**Chat UI preference:** **Open WebUI** (LAN) → Ollama personal models. Odysseus optional.

---

## 6. Evaluation

Harness contract: `MODEL+RAG/research/INTERESTING-RESEARCH/HARNESS-CONTRACT.md`  
Criteria: consistency, efficiency, boundaries, Domain interaction, sure-hit specialty, grade relative to Domain.

---

## 7. Non-goals

- Self-approve / clear Prohibited  
- Unlock Kingston / train on vault raw  
- Auto-submit Upwork  
- Sole ownership of cash runway numbers  
- Shipping weights in git  

---

## 8. Provenance pointers

- filter-v2: `logos-training-data-sampler/source-packs/20260722-filter-v2/`  
- taste: `finance/logs/2026-07-22-personal-llm-taste-profile.md`, `…-sft-v2-taste-and-layers.md`  
- layer doc: `docs/PERSONAL-LLM-LAYER.md`  
- INTERESTING: `MODEL+RAG/research/INTERESTING-RESEARCH/`
