# Stage 03 Summary — Mechanical /codebase-review with Grok Heavy

**User directive addressed**: Still want Grok Heavy (multi-agent). Make the entire /codebase-review process mechanical via skills and scripts. MCP only if true to repo. Progressive autonomy.

**Verification from prior stages incorporated**: Direct API for mechanical execution (API billing separate from consumer SuperGrok rates). Level 0 prompt mode remains available for rates if preferred.

**What was created**:
- dev/03_mechanical-codebase-review/CONTEXT.md (stage contract)
- output/mechanical-design.md (full design, progressive levels, MCP decision)
- skills/codebase-review/SKILL.md (invocable skill with constitution and process)
- scripts/codebase_review.py (core mechanical behaviour — stdlib, calls Grok Heavy API)
- scripts/codebase-review (thin wrapper for easy `codebase-review <target>`)
- output/test-report.md
- This summary

**How it works (mechanical)**:
- One command gathers doctrines + target sidecars/context.
- Calls grok-4.20-multi-agent + high reasoning (Grok Heavy 16 agents).
- Saves structured review as FS artifact in target.
- Progressive: Start with snapshot prompt (Level 1). Add tool-calling for model-driven exploration (Level 2). MCP server only if it stays minimal/Python/sidecar-based.

**Grok Heavy usage**: Via official xAI API (your account's key). This enables full mechanical autonomy with the multi-agent power.

**True to repo**: Pure MD (skills/prompts) + Python (script). Sidecars for input/output. Low overhead. Inspectable.

**To run**:
See test-report.md. Start with Level 1.

This gives progressive autonomy: from assisted prompt gen → full mechanical review with Grok Heavy.

All artifacts ready for review/edit. Next: test, then implement Level 2 (tools) or MCP if approved.
