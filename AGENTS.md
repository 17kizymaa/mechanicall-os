# AGENTS.md — Live authority first, then ICM

**Doc status:** **NORMATIVE** — agent operating rules (CURRENT-first; models never approve).  
**Conflict:** yields to live `CURRENT.md`; aligns with SPEC-v0.2 / PRODUCT.  
**Map:** `docs/DOC-AUTHORITY.md`

## Live authority — read first (non-negotiable)

Before ICM stages, tools, or model taste:

**Any agent cold start (no TUI):** [docs/AGENT-AGNOSTIC-COLD-START.md](./docs/AGENT-AGNOSTIC-COLD-START.md)

1. **Read root `CURRENT.md`** (or the project CURRENT that binds this work).  
2. **CURRENT outranks** chat, stages, sessions, skills, and model output.  

3. Perform **only** the declared **Next** (one action-id at a time).  
4. Run **`aether preflight <action>`** before consequential work.  
5. **Stop on refusal.**  
6. Agents **never** `approve`, `reject`, or rewrite authority as their own decision.  
7. **Silence is never permission.**

```bash
aether current
aether preflight <next-or-action>
# human only:
aether approve "…"
# after APPROVED, re-SELECT (never hand-edit **Next:**):
aether next <new-action-id>
```

Validate schema (protocol product):

```bash
aether current validate
```

---

## Development philosophy (ICM Meta-Agent)

This project follows the **Interpretable Context Methodology (ICM)** from:
https://arxiv.org/abs/2603.16021  
**"Interpretable Context Methodology: Folder Structure as Agentic Architecture"**

### When to use full ICM

| Situation | Load |
|-----------|------|
| Docs-only review / trivial patch | CURRENT + named files only; short receipt optional |
| Multi-step development / research | Full meta-agent + numbered stages |
| Consequential implement | CURRENT Next + preflight + stages as needed |

### Mandatory for multi-step work

1. Activate and follow the **meta-agent** skill (`.grok/skills/meta-agent/SKILL.md` or `/meta-agent`).  
2. Use **folder structure** as the primary orchestration mechanism.  
3. Use **markdown** as skills / stage contracts (`CONTEXT.md`).  
4. Use **Python or shell scripts** for mechanical work.  
5. Act as the **single orchestrating agent**.  
6. Produce reviewable artifacts in `output/`; wait for human review before advancing stages.

### Context layers (load only what you need)

- L0: Identity (this file, meta-agent skill, CORE_PRINCIPLES, PRODUCT)  
- L1: Routing (CURRENT + top CONTEXT.md)  
- L2: Stage contract (`NN_stage/CONTEXT.md`)  
- L3: Reference (docs/, SPEC, style)  
- L4: Working artifacts (`output/` + user input)

### Alignment with Core Principles

- Filesystem is the single source of truth.  
- Durable authority and user-owned state = plain Markdown/JSON.  
- Core automation = inspectable POSIX shell and/or Python.  
- Distribution UIs may use other languages but **must not** become a second authority store.  
- Extremely low overhead; `cat` / `grep` / `git diff` everything that matters.

### Practical rules

- Trivial changes: edit directly; short receipt when useful.  
- Sequential work: numbered stage workspace + human gate at `output/`.  
- Never load unrelated stages’ full history unless listed in Inputs.  
- Prefer existing scripts over ad-hoc logic.

### Quick activation

- Explicit: `/meta-agent`  
- Implicit: “start dev”, “implement”, “follow ICM”, “meta-agent”  
- Always: CURRENT + preflight before consequential work  

Violations of live authority or this philosophy are bugs in the session.

---

See also: `.grok/skills/meta-agent/SKILL.md` · `PRODUCT.md` · `CORE_PRINCIPLES.md` · `ARCHITECTURE.md` · `SPEC-v0.2.md` · `README.md`
