# Changes & Explorations — Re-focused from the Original Prompt

**Reference prompt (the "last prompt" to use for changes/exploration):**
> "I wanted Grok Heavy to do externally evaluated codebase reviews: I do not require the Grok CLI for this, just maybe let us use the codebase doctrines to create a /review-codebase command that lets Grok Heavy be queried through some sort of API, using official capability documents to gauge the right approach on this. Let us discuss this"

This file records adjustments to the stage 01 artifacts and new focused explorations, derived strictly by re-referring to the above.

## Changes Made (or Recommended) to Previous Work

1. **De-emphasize aether / this project's CLI integration**
   - Original prompt explicitly says "I do not require the Grok CLI for this".
   - Option 4 (aether extension) and heavy aether mentions in other files are now lower priority or secondary.
   - The `/review-codebase` command should stand alone as a thin tool for querying the external API. It can coexist with aether but does not depend on or extend it primarily.

2. **"Just maybe" for creating the command — keep exploratory**
   - Do not over-commit to a full implementation yet.
   - Focus remains on discussion + gauging the *right approach* via official docs.
   - The command is one possible surface; the real value is the doctrine-injected API query pattern for Grok Heavy reviews.

3. **Narrow the "command" scope**
   - Its sole purpose (per prompt): "lets Grok Heavy be queried through some sort of API".
   - Primary job = gather doctrines + target context from FS → assemble prompt → call xAI API (Grok Heavy model) → write clean report.
   - Keep it extremely thin. Prefer the spirit of SPEC-v0.1 (small sh + optional tiny py).

4. **Stronger emphasis on "using official capability documents to gauge the right approach"**
   - Previous research summary is good but can be extended with deeper dives into specific API features for *review workloads*.
   - This file + future edits will focus exploration here.

5. **"Let us discuss this" remains primary**
   - Artifacts should surface tradeoffs, concrete API examples, and prompt techniques rather than presenting a finished design.
   - All output/ files remain edit surfaces.

## Focused Explorations (Gauged from Official Documents + Original Intent)

### 1. Model Choice for "Grok Heavy" External Reviews (Updated per user)
**The model must be Grok Heavy: the multi-agent variant.**

- Official model: `grok-4.20-multi-agent`
- This is the Realtime Multi-agent Research model.
- Configure for **16 agents** (the "Heavy" setup) using `agent_count=16` or `reasoning.effort: "high"` / "xhigh".
- This matches the user's clarification: "The model should be Grok Heavy: it is multi-agent and the reason for my worthwhile effort anyway!"
- Why ideal for externally evaluated codebase reviews:
  - Multiple specialized agents collaborate in parallel (search/analyze/synthesize).
  - Can assign different doctrine lenses to different agents (e.g. one agent audits CORE_PRINCIPLES compliance, another AGENTS.md/ICM structure, another sidecar health + inspectability, another architecture fit).
  - Leader agent synthesizes into a coherent, evidence-based review.
  - Deeper, more thorough than single-model for complex, multi-faceted doctrine analysis.

From official docs:
- Use `grok-4.20-multi-agent` as the model.
- 16-agent setup for deep research on complex topics (perfect for full codebase + doctrines).
- Note: Full Heavy (16 agents) access/performance is associated with SuperGrok Heavy tier.

Update all prior recommendations that defaulted to grok-4.3. The multi-agent nature is the key differentiator and value.

### 2. API Surface: Responses API vs Chat Completions for Reviews
Official docs and examples favor the Responses API (`/v1/responses`) for newer capabilities.
- Better for structured state, tool use (if ever needed), and modern features.
- Chat Completions (`/v1/chat/completions`) still fully supported and simpler for pure text reviews.

**Gauged recommendation for /review-codebase**:
- Start with Responses API (matches recent examples for grok-build and grok-4.3).
- Or support both via a small abstraction.
- For a pure minimal sh version: use curl against whichever endpoint the prompt example shows.

Concrete curl skeleton (to explore and refine):
```bash
curl https://api.x.ai/v1/responses \
  -H "Authorization: Bearer $XAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "grok-4.3",
    "reasoning": {"effort": "high"},
    "input": [
      {"role": "system", "content": "You are ... doctrines here ..."},
      {"role": "user", "content": "Target context + code here..."}
    ]
  }'
```

### 3. Structured Outputs for Doctrine-Aligned Reviews
From official Structured Outputs doc:
- Use `response_format` with JSON schema.
- Guaranteed to match the schema.
- Perfect for forcing sections that map to doctrines (violations with evidence, principle-by-principle, etc.).

Exploration: The draft-review-prompt.md should evolve to include a schema when using the API feature. This makes the output machine-readable while staying principle-first.

### 4. Context Packing Strategy (Leveraging Official 1M Window)
- Doctrines are tiny → include full text.
- Target .context.md is the "distilled truth" → always include.
- Source files: use simple selection (git ls-files + size cap, or user-provided globs).
- With 1M tokens we can send a lot before needing heavy summarization or chunking.
- Exploration: Command should have a `--dry-run --tokens` mode that shows estimated size before calling (cost control + transparency).

### 5. Making the /review-codebase Command Itself Doctrine-Compliant
- It must itself follow the principles:
  - Output artifacts (the review .md) to the filesystem.
  - Be inspectable (source is small sh or py).
  - No hidden state.
  - Use Markdown for any templates/prompts (see draft-review-prompt.md).
- Thin client only; the intelligence (review) is external via Grok Heavy API.

### 6. "Command" Realization Options (Narrowed)
Given "just maybe" and "create a /review-codebase command":
- A. A small standalone script (`review-codebase` in PATH) — pure sh or tiny py.
- B. The command is effectively "the prompt template + a documented one-liner curl".
- C. A reusable Python function/behaviour that other tools can import (still tiny).

Prefer A or B for minimalism. Avoid tying it tightly to aether unless user requests.

## What This Means for Current Artifacts
- proposed-interface.md and options.md should be read with the de-emphasis on aether.
- discussion-points.md should be narrowed (see updated version or edit it).
- New focus: concrete API examples + prompt evolution as the main "right approach" exploration.

All of the above is for discussion. Edit this file or the others directly.
