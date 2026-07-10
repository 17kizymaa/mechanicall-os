# Research: Mimicking Grok Heavy's Semantically-Structured Swarm Framework

## What is Grok Heavy's Swarm (from official + community sources)
- **Model**: grok-4.20-multi-agent (API), Grok 4.20 Heavy in consumer (16 agents).
- **Core Architecture**:
  - Shared backbone (not fully separate models).
  - Specialized agents operating in **parallel**.
  - Task decomposition by leader (Grok/Captain or Victor the orchestrator).
  - Agents contribute perspectives, reasoning, findings.
  - Coordination layer for inter-agent "communication" (e.g., one agent's output feeds another, cross-verification, "adversarial consensus").
  - Leader synthesizes into coherent final response.
- **4-agent base** (Grok 4.20):
  - Examples from analysis: Grok (Captain/coordinator, strategy, synthesis), others specialized (research, code, etc.).
  - "Adversarial consensus": Agents debate internally.
- **16-agent Heavy**:
  - Domain specialists: Lucas (software engineering/coding), Benjamin (finance), Elizabeth (legal), Victor (orchestration/synthesis), Aria (scientific), Nathan (cybersecurity), etc.
  - Not all activated for every query; orchestration routes to relevant subset.
  - Parallel processing for multi-domain complexity.
  - Scales cognitive "effort".
- **How it works semantically**:
  - Structured task allocation.
  - Agents have defined roles/domains.
  - Outputs are synthesized, not just concatenated.
  - "Swarm intelligence": Distributed specialized reasoning > single generalist.
- API usage: model="grok-4.20-multi-agent", reasoning.effort="high" or agent_count=16 for Heavy.
- Benefits for code review: Parallel deep dives into different aspects (principles, structure, sidecars, code), then consensus synthesis.

Sources synthesized from x.ai/docs, community breakdowns (aitoolland, verdent.ai, Reddit, Medium analyses as of 2026).

## Mimicking with This Filesystem's Limitations
This repo's constraints (from CORE_PRINCIPLES, AGENTS, SPEC, ICM):
- No hidden state/DBs – everything plain files (MD, JSON sidecars).
- Markdown + Python only.
- Active sidecars (.context.md for distilled context, .memory/ for fragments, .awareness.json).
- Low overhead, inspectable (cat/grep/git).
- Folder structure as orchestration (numbered stages, agents as subdirs?).
- No heavy frameworks, no external LLM orchestration libs beyond what's mechanical.
- Python behaviours for logic.
- Use existing aether patterns for context gathering if possible.
- Progressive: Start simple, add autonomy (e.g., parallel Python processes writing sidecars).

**Mimic Strategy**:
- **Semantically-structured**: Define agents via dedicated .md "personas" with clear roles, input/output schemas (structured MD sections or JSON blocks for easy parsing).
- **Swarm**:
  - Orchestrator (main script, like Victor): Decomposes task using doctrines, prepares shared context from .context.md + target files.
  - Specialized agents: Small number (4-5) tailored to *this* project's doctrines (not general 16 domains).
    - Principles Agent (Lucas-like for code + CORE_PRINCIPLES).
    - ICM/Meta Agent (AGENTS.md, stages, CONTEXT.md).
    - Sidecar/Context Agent (.context.md, .awareness, memory health).
    - Architecture/Minimalism Agent (ARCHITECTURE + SPEC).
    - Synthesis Leader (Victor): Collects, applies "adversarial consensus" (notes conflicts), produces final.
  - Parallelism: Python concurrent.futures or simple multiprocessing – each agent "runs" independently, writing to its sidecar dir (e.g., .swarm/principles-agent/output.md).
  - Communication/Coordination: Shared context files in .swarm/ (orchestrator writes common context; agents can "read" previous agents' outputs if sequential or via shared).
  - "Adversarial consensus": In synthesis prompt or post-processing, have leader critique/cross-reference agent outputs.
- **Mechanical execution**:
  - Script: `codebase-review <target>` (Python + thin sh wrapper).
  - Gathers using existing patterns (subprocess for grep if needed, or pure Python; respect .gitignore).
  - For "Grok Heavy" intelligence: Multiple API calls to grok-4.20-multi-agent (high effort) – one per agent + final synthesis. This approximates the swarm by giving each "specialist" its own Heavy reasoning pass, then synthesis.
  - If no API key: Fallback to generating structured prompts for manual paste into Grok Heavy (consumer).
  - Outputs: All intermediates in target's `.swarm/` (inspectable MD/JSON), final review in `reviews/codebase-review-*.md` or sidecar.
- **Filesystem as the swarm bus**:
  - .swarm/ dir as coordination layer (like the model's internal).
  - Each agent dir: persona.md (role), input.md (specialized context), output.md (structured findings), thoughts.md (if verbose).
  - Orchestrator reads/writes these, "spawns" agents.
  - .context.md as persistent shared memory.
  - .memory/ for fragments.
  - Fully cat/grep/git friendly, low overhead (no daemons).
- **Progressive autonomy** (as per previous):
  - v1: Sequential agent "runs" + synthesis (current script base).
  - v2: Parallel execution + structured JSON outputs for easy merge.
  - v3: Agents can "request" more info by writing needs.md (orchestrator fulfills from FS).
  - v4: Hook into aether for auto-trigger on code changes.
  - v5: If MCP allowed later, expose .swarm/ as tool server, but only if fits (Python stdio, no heavy).

This keeps everything true to the repo: The "swarm" *is* the filesystem + lightweight Python orchestration. No external state.

Limitations acknowledged:
- Can't do true real-time inter-agent debate without multiple roundtrips or local simulation.
- Relies on Grok (Heavy) for the "thinking" (as intended).
- For full 16 agents, we'd overkill for codebase review – tailor to doctrines (4-5 is sweet spot for ICM).
- API costs vs consumer: Use multi-agent model where possible.

This research directly informs the decent script below.
