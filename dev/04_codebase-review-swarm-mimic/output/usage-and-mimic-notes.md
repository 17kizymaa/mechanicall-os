# /codebase-review - Decent Swarm-Mimicked Version

## Quick Start
```bash
export XAI_API_KEY=...   # for real Grok Heavy calls (grok-4.20-multi-agent + high)
./scripts/codebase-review /path/to/target
```

This will:
- Load doctrines + target's .context.md
- "Spawn" 4-5 specialized agents (filesystem sidecars in target/.swarm/)
- Each agent gets a semantically-structured persona + shared context
- Calls Grok Heavy (multi-agent) for each specialist perspective
- Victor (synthesis leader) reads the .swarm/ bus and produces final review
- Writes reviews/codebase-review-*.md + leaves full inspectable swarm state

Without key: Generates everything as prompts you can paste into grok.com Grok Heavy manually.

## How it Mimics Grok Heavy's Framework (research-backed)
See references/grok-heavy-swarm-mimic.md for full research.

Short version:
- **Semantically-structured**: Each agent has a dedicated .md persona with exact output schema (Findings / Violations / Recommendations / Confidence). This forces structured, composable contributions.
- **Parallel specialists**: Agents run "in parallel" (concurrent in Python, or sequential for determinism). Each focuses on one doctrine slice (Principles, ICM, Sidecars, Architecture).
- **Coordination layer**: The `.swarm/` directory is the filesystem equivalent of the model's internal bus. Orchestrator writes shared context; agents write outputs; leader reads everything.
- **Leader synthesis (Victor)**: Final step does "adversarial consensus" — notes agreements/disagreements between agents and produces one coherent review.
- **Progressive autonomy**: Currently orchestration is in one script. Future: agents could write "I need more X" files, orchestrator fulfills from FS, re-runs. Hookable via aether.
- **True to this repo**: 100% MD (personas, sidecars, reviews) + Python (behaviours). No hidden state. Everything cat/grep/git diffable. Low overhead. Uses existing .context.md as the "shared memory".

This gives you the power of a structured swarm without leaving the filesystem-only, Markdown+Python world.

## Files Involved
- references/swarm-agents/*.md : The semantic agent definitions (edit these to change the swarm).
- scripts/codebase_review.py + codebase-review : The decent script.
- target/.swarm/ : Live swarm artifacts (inspect after run).
- target/reviews/codebase-review-*.md : Final output.

## Why This is "Actually Decent"
- Respects every locked principle.
- Uses Grok Heavy where it matters (the actual thinking).
- Full transparency of the "swarm" via filesystem (you can debug any agent).
- Easy to evolve (add new agent persona = new .md file).
- Mechanical: one command.

Run it, inspect the .swarm/ dir, and iterate.
