# Discussion Points — Narrowed Using the Original Prompt

**Re-referenced prompt**: "I wanted Grok Heavy to do externally evaluated codebase reviews: I do not require the Grok CLI for this, just maybe let us use the codebase doctrines to create a /review-codebase command that lets Grok Heavy be queried through some sort of API, using official capability documents to gauge the right approach on this. Let us discuss this"

This version has been narrowed. Broad questions about aether integration have been deprioritized.

## Focused Questions (directly from re-reading the original intent + latest clarification)
1. **Grok Heavy = multi-agent model** (user clarification):
   - Use `grok-4.20-multi-agent` with 16-agent configuration (Heavy) as the default.
   - How to best prompt the multi-agent system so different agents specialize on different doctrines (CORE_PRINCIPLES, AGENTS/ICM, sidecars, inspectability, etc.)?

2. **Exact API mechanism**:
   - Responses API with `reasoning.effort: "high"` (maps to 16 agents) + optional `agent_count`.
   - How to request verbose/encrypted sub-agent traces if we want to surface the multi-agent collaboration in the review report?
   - Concrete examples for the thin `/review-codebase` caller.

3. **How the /review-codebase command (or pattern) should work**:
   - Standalone thin script (sh or tiny py) whose job is "gather from FS + doctrines → query API"?
   - Or primarily the prompt template in Markdown + a documented one-liner?
   - "Just maybe" — should we produce a working minimal prototype script as an artifact now, or keep purely discussion + examples?

4. **Doctrines injection for external evaluation**:
   - Full verbatim inclusion (doctrines are small)?
   - Or curated excerpts + reference to the .md files?
   - How to handle the *target* project's .context.md and any local AGENTS.md?

5. **"Gauge the right approach" using official docs** — what else should we explore?
   - Context management for large codebases given the 1M window.
   - Dry-run / token estimation / cost visibility before the call.
   - Output formats (Markdown report + optional structured JSON).

6. **Keeping the command itself doctrine-compliant**:
   - Must output to filesystem as reviewable artifacts.
   - Source must be tiny and inspectable.
   - Prompt logic should live in Markdown where possible.

## Updated Recommendations (tighter to original prompt)
- Use **grok-4.3 + high reasoning effort** as the default for externally evaluated principle-based reviews.
- The `/review-codebase` thing is a thin API query enabler. Primary exploration = how to call the official API correctly with doctrines injected.
- Produce concrete API usage examples (curl + minimal code) + evolve the draft-review-prompt.md.
- Provide a minimal standalone caller (sh or py) only if it stays extremely small. The real "command" can start as the documented pattern.
- Leverage target `.context.md` + full doctrine files.

## Next Steps for Discussion
- Edit any file in output/ (especially the new changes-and-explorations-from-original-prompt.md and this file).
- Ask me to produce a specific concrete example (e.g. a full curl command with sample prompt, or a 50-line review_codebase.py sketch in output/).
- Say "narrow further to X" or "explore the Responses API + structured outputs in more depth".
- When ready: "create a minimal working sketch as a new artifact" or "advance to 02 once we lock the API approach".

All files here are the discussion surface. Let's use the original prompt as the north star for what to change and explore.

