# Grok Heavy (Multi-Agent) Strategy for Doctrine-Driven Codebase Reviews

**User directive**: "The model should be Grok Heavy: it is multi-agent and the reason for my worthwhile effort anyway!"

This artifact explores how to harness the native multi-agent architecture (`grok-4.20-multi-agent` + 16 agents / Heavy) specifically when the review criteria are the locked doctrines from this project.

## Why Multi-Agent Fits Perfectly
The doctrines are multi-faceted and somewhat orthogonal:
- CORE_PRINCIPLES (FS as truth, Markdown+Python only, active sidecars, low overhead/inspectability)
- AGENTS.md + ICM (numbered stages, CONTEXT.md contracts, output/ gates, single orchestrating agent, human review)
- ARCHITECTURE (three layers)
- SPEC-v0.1 (brutalist minimal sidecar layout, aether command, no hidden state)

A single model might reason sequentially and miss interactions. Grok Heavy launches multiple agents that can specialize, debate, cross-reference, and have a leader synthesize.

## Recommended Prompting Approach for Heavy Reviews
In the system message or initial user content, explicitly instruct role specialization:

```
You are Grok Heavy operating in 16-agent mode.

You must launch and coordinate specialized sub-agents. Assign agents to the following doctrine domains and have them work in parallel:

- Principles Auditor: Focus exclusively on CORE_PRINCIPLES.md. Check filesystem truth, absence of hidden state, Markdown + Python/sh purity, sidecar activity, overhead/inspectability.
- ICM / Meta-Agent Auditor: Focus on AGENTS.md and ICM protocol. Verify numbered stages, CONTEXT.md usage, Layer 0/1/2/3/4 separation, human review gates, output/ artifacts.
- Architecture & Layers Auditor: Analyze against ARCHITECTURE.md three-layer model.
- Minimalism & Sidecar Auditor: Deep dive on SPEC-v0.1 and actual .context.md / .aether/ usage.
- Cross-Cutting & Synthesis Leader: You (leader) collect findings, look for interactions between principles, score overall alignment, and produce the final report with verbatim quotes and precise file evidence.

All agents must quote the doctrines directly. Be ruthless but evidence-based. The final output must be from the leader after collaboration.
```

Then feed the full doctrine texts + target .context.md + codebase excerpts.

## Benefits for This Use Case
- Parallel depth on each principle instead of shallow coverage.
- Agents can "debate" findings (e.g. one agent finds a Python framework violation, another checks if a sidecar mitigates it).
- Leader produces higher-quality synthesis.
- Matches the "externally evaluated" goal — the heavy lifting is collaborative multi-agent work on the cloud.

## API Configuration for True Heavy (16 Agents)
From official docs:
- Model: `"grok-4.20-multi-agent"`
- For 16 agents / Heavy: `"reasoning": {"effort": "high"}` (or "xhigh") + optionally `agent_count: 16` in the xAI SDK.
- Use the Responses API.

Example fragment:
```json
{
  "model": "grok-4.20-multi-agent",
  "reasoning": {"effort": "high"},
  ...
}
```

## Open Exploration Points
- Should the thin `/review-codebase` command support `--agents 4|16` (map low/high)?
- Can we ask for encrypted sub-agent traces (`use_encrypted_content`) to optionally show the collaboration process in verbose review reports?
- How to tune the specialization prompt without making it too long (doctrines are small, but we still have to send them).
- Opportunity: Produce a reusable "doctrine roles" Markdown fragment that the command can inject.

This is the core reason the effort is worthwhile. Edit and discuss.
