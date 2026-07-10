## Inputs
- Layer 0 doctrines: ../CORE_PRINCIPLES.md, ../AGENTS.md, ../ARCHITECTURE.md, ../SPEC-v0.1.md, .context.md (this project)
- Layer 4 from 02: ../02_test-code-review-command/output/code-review-design.md, verification-summary.md, low-friction-quick-test-research.md, code-review-enhanced
- Layer 4 from 01: ../01_research-grok-heavy-reviews/output/gauged-api-approach-examples.md, multi-agent-doctrine-review-strategy.md, verification-supergrok-free-rates.md
- User directive: Still want Grok Heavy (multi-agent). Make the entire "/codebase-review" process happen mechanically using skills and scripts. MCP only if true to repo (MD+Python, low overhead, sidecars, inspectable, no heavy frameworks). Progressive autonomy.

## Process
You are the single meta-agent.

Devise and implement (in this stage) a mechanical /codebase-review process using Grok Heavy.

Key constraints (locked by doctrines):
- Everything plain files: MD for skills/prompts/contracts, Python for behaviours/scripts.
- Use .context.md sidecars for target awareness.
- Low overhead: Use stdlib where possible (urllib for HTTP, no extra deps initially).
- Mechanical: A script or command that runs end-to-end: gather context from FS/sidecars + doctrines -> call Grok Heavy API -> receive review -> write as reviewable artifact (e.g. target/reviews/codebase-review-*.md or .memory/review.md).
- Grok Heavy: Use model="grok-4.20-multi-agent" with reasoning.effort="high" (16 agents) via xAI API (https://api.x.ai/v1/responses or chat). User provides XAI_API_KEY (from their SuperGrok/console account). Note: This uses API metering, not direct consumer chat rates (per previous verification).
- Progressive autonomy:
  - Base: Full context in one prompt (large but 1M window ok). Grok does the review.
  - Next level: Add tool calling support in the API call so Grok Heavy can request more files/context during the review (more autonomous).
  - MCP: Only introduce if it fits perfectly - e.g. a minimal stdio MCP-like tool server in Python providing codebase tools (read, grep, list) that the script can use for gathering or expose. Avoid if it adds complexity/heavy deps. Prefer native API tool use first.
- Skills: Create a skill as MD (skills/codebase-review/SKILL.md) containing the review constitution (doctrines injection + multi-agent instructions) and process description. Usable by scripts or future agents.
- Scripts: Python behaviour in scripts/codebase_review.py (or .sh wrapper) that implements the command. Make it invocable as `codebase-review <target>`.
- Output artifacts: Always write to target's FS as inspectable MD (e.g. in reviews/ or as sidecar). Update .awareness.json or similar if present.
- No Grok CLI/TUI dependency.
- Test/prototype in output/.

Use existing aether patterns where they fit (sidecars for input).

Write all to output/ for review. Keep self-contained.

## Outputs (to output/)
- mechanical-design.md : Detailed design for the mechanical process, API call, progressive levels, MCP decision.
- skills/codebase-review/SKILL.md : The skill definition (prompt template, rules, process). (Symlink or copy to main skills/ if appropriate.)
- scripts/codebase_review.py : Core Python script (behaviour) for mechanical execution. Minimal, uses stdlib.
- codebase-review : Thin wrapper script (sh or py entry) for easy invocation.
- example-review.md : Sample output artifact (or template).
- test-report.md : How to test (with example target), notes on API key setup, autonomy levels.
- summary.md : Stage summary + paths + next progressive steps.
