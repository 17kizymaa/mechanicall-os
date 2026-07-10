# Gauged API Approach for /review-codebase (Grok Heavy via Official API)

**Derived from original prompt + official docs** (https://docs.x.ai , models page, reasoning doc, structured outputs doc, quickstart).

This is the current best "right approach" for letting Grok Heavy do externally evaluated reviews. Everything is for discussion and editing.

## Recommended Defaults (Gauged) — Grok Heavy Multi-Agent
**Model**: `grok-4.20-multi-agent` (this is Grok Heavy in the multi-agent sense)

- **Agent count for Heavy**: 16 agents (use `agent_count=16` in xAI SDK or `reasoning.effort: "high"` / "xhigh" in compatible SDKs / REST).
- **Endpoint**: `/v1/responses` (official examples use this for multi-agent).
- **Structured output**: Use `response_format` JSON schema for doctrine-mapped reviews.
- **Auth**: `XAI_API_KEY`
- **Why multi-agent is the point**: Parallel specialized agents can each deeply audit different doctrines or codebase facets, then synthesize. This is the core reason for the worthwhile effort.

## Example 1: Minimal curl for Grok Heavy (16-agent multi-agent)

```bash
#!/bin/sh
# review-codebase-curl.sh — thin caller for Grok Heavy multi-agent

TARGET="${1:-.}"
DOCTRINES_DIR="${DOCTRINES_DIR:-/path/to/this/awareness-agent}"

CONTEXT=$(cat "$TARGET/.context.md" 2>/dev/null || echo "(no .context.md)")
DOCTRINES=$(cat "$DOCTRINES_DIR/CORE_PRINCIPLES.md" "$DOCTRINES_DIR/AGENTS.md" "$DOCTRINES_DIR/ARCHITECTURE.md" "$DOCTRINES_DIR/SPEC-v0.1.md" 2>/dev/null | head -c 25000)

PROMPT="You are a team of specialized agents (Grok Heavy / 16-agent mode). Collaboratively and rigorously evaluate the target ONLY against the injected doctrines. Different agents should focus on different doctrine areas in parallel (filesystem truth & sidecars, ICM/AGENTS protocol, architecture layers, Markdown+Python purity + inspectability). The leader synthesizes. Quote doctrines verbatim and cite exact evidence."

curl -s https://api.x.ai/v1/responses \
  -H "Authorization: Bearer $XAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d @- <<JSON | jq -r '.output[0].content[0].text // .'
{
  "model": "grok-4.20-multi-agent",
  "reasoning": {"effort": "high"},
  "input": [
    {"role": "system", "content": "You are Grok Heavy (16-agent multi-agent system). Evaluate strictly against the provided doctrines using collaborative reasoning."},
    {"role": "user", "content": "=== DOCTRINES ===\n$DOCTRINES\n=== END ===\n\nTarget .context.md:\n$CONTEXT\n\n[Insert selected source files or full codebase excerpts here]"}
  ]
}
JSON
```

**Notes**: This is deliberately simple. Real version would handle file selection, token estimation, and writing the result to a review artifact in the target.

## Example 2: Grok Heavy Multi-Agent + Structured Outputs + 16 Agents

```json
{
  "model": "grok-4.20-multi-agent",
  "reasoning": { "effort": "high" },
  "response_format": {
    "type": "json_schema",
    "json_schema": {
      "name": "doctrine_aligned_codebase_review",
      "schema": {
        "type": "object",
        "properties": {
          "overall_alignment": { "type": "integer", "minimum": 0, "maximum": 100 },
          "agent_perspectives": {
            "type": "array",
            "description": "Summary of key contributions from different specialized agents (e.g. Principles agent, ICM agent, Sidecar agent, Architecture agent)",
            "items": { "type": "string" }
          },
          "principle_violations": { ... same as before ... },
          "synthesized_recommendations": { ... }
        }
      }
    }
  },
  "input": [ ... full doctrines + target .context.md + code ... ]
}
```

The multi-agent system (leader + sub-agents) produces deeper cross-referenced analysis. Use 16-agent Heavy mode for the most worthwhile reviews.

## Exploration Questions Specific to API Approach
- Should the thin command default to Responses API?
- How do we expose `reasoning.effort` cleanly in the command flags?
- For very large targets, should we first use a cheap pass (or local distill) to select the most relevant files before the heavy review call?
- Is there value in sending source as separate "file" style messages if the API supports it, or one big user message?

## Relation Back to Original Prompt
This file exists because the prompt said "lets Grok Heavy be queried through some sort of API, using official capability documents to gauge the right approach".

The above is the current gauged approach. Edit it, tell me what to add/remove, or ask for a working minimal Python version of the caller as the next exploration artifact.

All still within stage 01. No new stages yet.
