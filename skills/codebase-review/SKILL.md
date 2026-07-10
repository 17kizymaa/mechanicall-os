---
name: codebase-review
description: Mechanical externally-evaluated codebase review using Grok Heavy (multi-agent) against this project's locked doctrines.
user-invocable: true
version: 0.1
---

# codebase-review Skill

## Constitution (injected into every review)
You are Grok Heavy in 16-agent multi-agent mode.

Evaluate the target codebase **strictly and exclusively** against the doctrines below. Quote them verbatim. Use parallel specialized agents + leader synthesis.

### Core Doctrines (always include full or key excerpts)
[Full text of CORE_PRINCIPLES.md, AGENTS.md, ARCHITECTURE.md, SPEC-v0.1.md will be injected by the script]

### Agent Roles (for multi-agent)
- Principles Auditor: FS as truth, Markdown+Python only, active sidecars, low overhead/inspectability.
- ICM/Meta-Agent Auditor: Numbered stages, CONTEXT.md, Layered context, output/ review gates, single orchestrator.
- Architecture Auditor: Three layers (FS Substrate, Awareness, Interface).
- Minimalism & Sidecar Auditor: Brutalist .context.md, .aether/, no hidden state.
- Cross-Cutting Leader: Synthesize, score alignment (0-100), evidence from specific files/sidecars, recommendations tied to doctrines.

## Process
1. Receive target .context.md + limited source excerpts + full doctrines.
2. (Level 2+) Use tools if provided (read_file, grep, list_dir) to gather more evidence autonomously.
3. Produce structured review:
   - Overall alignment score
   - Per-doctrine assessments with quotes
   - Violations (file:line + evidence + severity)
   - Strengths
   - Recommendations (doctrine-tied)
   - Multi-agent notes (if visible)
   - Final verdict

## Invocation (via script)
codebase-review <target-dir>

The supporting script (scripts/codebase_review.py) handles mechanical gathering, API call to grok-4.20-multi-agent (high), and artifact writing.

## Outputs
Review written to target's filesystem (reviews/codebase-review-*.md or .memory/).

This skill makes the review repeatable and mechanical while leveraging Grok Heavy's multi-agent power.
