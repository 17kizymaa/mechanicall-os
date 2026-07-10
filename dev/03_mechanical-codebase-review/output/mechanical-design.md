# Mechanical /codebase-review Design (Grok Heavy + Progressive Autonomy)

## Goal
Make the full /codebase-review process mechanical (script-driven, end-to-end) while using Grok Heavy (grok-4.20-multi-agent, 16-agent mode) for the external evaluation against this repo's doctrines.

## Core Flow (Mechanical)
1. **Input Gathering** (local, FS/sidecars, Python):
   - Target dir (default .).
   - Ensure/load target's .context.md (call aether distill if available via subprocess, else note it).
   - Load doctrines: CORE_PRINCIPLES.md, AGENTS.md, ARCHITECTURE.md, SPEC-v0.1.md (from known paths or repo root).
   - Gather limited source context (git ls-files or find, truncated for size, focus on key files like AGENTS.md, .py, etc. in target).
   - Optional: .memory/ or other sidecars.

2. **Prompt Assembly** (MD + Python):
   - Use skill-defined template (see skills/codebase-review/SKILL.md).
   - Inject full doctrines + target context + instructions for multi-agent collaboration.
   - Instruct Grok Heavy to act as 16 specialized agents (Principles, ICM, Sidecars, Architecture, etc.) + leader.

3. **Call to Grok Heavy** (mechanical via API):
   - Model: "grok-4.20-multi-agent"
   - reasoning: {"effort": "high"} for 16 agents.
   - Endpoint: https://api.x.ai/v1/responses (or /chat/completions for compatibility).
   - Auth: XAI_API_KEY env (obtain from console.x.ai using your SuperGrok account).
   - Send the assembled messages.
   - Note on rates: This uses xAI API billing/quotas associated with the key. Consumer SuperGrok chat rates are for grok.com manual use (see prior verification). For full mechanical, API is required.

4. **Receive & Persist** (local):
   - Parse response (text or structured if using response_format).
   - Write review to target/reviews/codebase-review-$(date +%Y-%m-%d).md (or configurable).
   - Optionally update target's .awareness.json or create .memory/codebase-review.md sidecar.
   - Make it git-friendly, cat/grep-able.

5. **Autonomy**:
   - The Grok Heavy multi-agent does the "intelligence" autonomously.
   - Local script handles mechanical parts (gather, call, persist).

## Progressive Autonomy Levels
- **Level 0 (Current from stage 02)**: Generate prompt → manual paste to grok.com (uses SuperGrok consumer rates + Heavy if logged in).
- **Level 1 (This stage base)**: Script does full gather + API call + save. One-command mechanical review. Grok gets all context upfront.
- **Level 2 (Next)**: Add tool calling to the API request. Define tools (read_file, grep_codebase, list_dir) in the call. Script implements the tool loop: when Grok calls a tool, local Python executes it (using sidecars/FS), feeds result back, continues until final answer. This gives Grok Heavy runtime autonomy to explore the codebase.
- **Level 3 (Future)**: Integrate sidecar updates more deeply (aether hooks on review). Perhaps MCP server for standardized tool exposure (see below).

## MCP Integration Decision
MCP (Model Context Protocol) is used in the Grok ecosystem for providing tools/servers to LLM clients (stdio or HTTP JSON-RPC style).

**Decision**: Introduce only minimally and if truly fits doctrines.
- **Fits if**: Pure Python (stdlib or tiny), observable (logs to MD/JSON sidecars), no heavy frameworks, enhances autonomy without violating low overhead/inspectability.
- **Plan**: For Level 2 tool calling, implement a simple internal tool provider in the script (no full MCP server initially).
- If needed later: Add a minimal `mcp_codebase_server.py` that speaks basic MCP over stdio for tools like "grep", "read", "context". The review script could launch it or use equivalent. But only if user confirms — it must stay "cat-able" and sidecar-based.
- Current: Skip full MCP for v1. Use native xAI API tool calling (supported). This is truer to "Python as behaviours".

Rationale: Keeps repo minimal. MCP would be useful for making the review agent composable with other Grok tools, but not required for mechanical process.

## Scripts & Skills
- `scripts/codebase_review.py`: Main behaviour. Handles levels 1+.
- Thin wrapper: `bin/codebase-review` or `scripts/codebase-review` for CLI.
- Skill: `skills/codebase-review/SKILL.md` — contains the constitution (doctrines + agent instructions), frontmatter for invocability if used in meta-agent contexts.
- Prompt is versioned in the skill MD (easy to edit, grep).

## Billing & Grok Heavy Notes
- API key from your SuperGrok/console account.
- Heavy multi-agent: Confirmed via model + high effort.
- If wanting consumer rates: Fall back to Level 0 prompt mode (enhanced script can support both).

## Output Artifacts
Reviews live in the target's filesystem as first-class MD (git trackable, sidecar-like).

This enables full mechanical /codebase-review while staying true to doctrines and giving Grok Heavy the multi-agent power.
