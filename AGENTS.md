# AGENTS.md — Development Philosophy (ICM Meta-Agent)

This project follows the **Interpretable Context Methodology (ICM)** from the paper:
https://arxiv.org/abs/2603.16021

**"Interpretable Context Methodology: Folder Structure as Agentic Architecture"**

## Mandatory at Every Repo Dev Session Startup

At the start of **any** development, research, implementation, or multi-step task (in this repo or when using this agent on other repos):

1. Activate and follow the **meta-agent** skill (`.grok/skills/meta-agent/SKILL.md` or `/meta-agent`).
2. Use **folder structure** as the primary orchestration mechanism.
3. Use **markdown files** as skills, stage contracts (CONTEXT.md), prompts and context.
4. Use **Python scripts** (in scripts/, bin/, or per-stage) as behaviours for all mechanical work.
5. Act as the **single orchestrating agent**. The filesystem (numbered stages + layered context) tells you the role, inputs, process, and outputs at every step.
6. Produce reviewable artifacts in `output/` directories. Wait for human review/edit before advancing stages.

## Context Layers (load only what you need)

- L0: Identity (this file, .grok/skills/meta-agent/SKILL.md, .context.md, CORE_PRINCIPLES.md)
- L1: Routing (top CONTEXT.md)
- L2: Per-stage contract (NN_stage/CONTEXT.md)
- L3: Stable reference/factory (references/, docs/, style rules)
- L4: Working artifacts (stage output/ + user input)

See the full protocol in `.grok/skills/meta-agent/SKILL.md`.

## Alignment with Core Principles

This is fully compatible with (and extends) the locked rules in CORE_PRINCIPLES.md:
- Filesystem is the single source of truth.
- Markdown + Python are the only userland.
- Active, observable sidecars and artifacts.
- Extremely low overhead, maximum inspectability (`cat`, `grep`, `git diff` everything).

## Practical Rules

- For trivial changes: edit directly but still produce a short readable summary artifact when it makes sense.
- For anything sequential or worth reviewing: create or reuse a numbered stage workspace (use the scaffolder behaviour when needed).
- Never load unrelated files or previous stages' full context unless explicitly listed in the current stage's Inputs.
- Every intermediate output is an edit surface.
- Prefer calling existing Python behaviours over ad-hoc logic.

## Quick Activation

- Explicit: `/meta-agent`
- Implicit: any prompt containing "start dev", "begin work", "implement", "dev session", "follow ICM", or "meta-agent".
- Startup: project rules (this AGENTS.md) + SessionStart hook + skill description ensure the philosophy is present from the first message.

Violations of this philosophy should be treated as bugs in the session.

---

See also:
- `.grok/skills/meta-agent/SKILL.md` (the detailed playbook)
- `CORE_PRINCIPLES.md`
- `ARCHITECTURE.md`
- `README.md`
- For codebase reviews: use the centralized `/codebase-review` command in the Grok CLI (skill at /root/.grok/skills/codebase-review/SKILL.md). It uses in-built parallel subagent swarms against the doctrines. Custom scripts deprecated.
