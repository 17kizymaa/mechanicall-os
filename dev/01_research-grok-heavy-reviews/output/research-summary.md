# Research Summary: Grok Heavy (xAI API) for Externally Evaluated Codebase Reviews

**Date**: 2026-06-25
**Stage**: 01_research-grok-heavy-reviews
**Inputs used**: Official xAI docs (models, quickstart, api page), project doctrines (CORE_PRINCIPLES.md et al.), user request.

## Official Capabilities Relevant to This Use Case (gauged directly from docs)

### Primary Model for Grok Heavy Reviews
**`grok-4.20-multi-agent`** (this *is* Grok Heavy)

- The official Realtime Multi-agent Research model.
- Supports configuration for **4 agents** or **16 agents** ("Heavy").
- 16-agent mode (Heavy) is the multi-agent collaborative system the user wants: specialized agents work in parallel on different aspects, with a leader synthesizing.
- Large context (aligns with other Grok 4.x models; excellent for doctrines + .context.md + codebase).
- Best for deep, multi-perspective analysis — exactly suited to externally evaluating a codebase against multiple interlocking doctrines (principles, ICM stages, sidecars, architecture, purity, inspectability).

**Access note**: Full 16-agent Heavy experience/performance is strongly associated with SuperGrok Heavy subscription. Via API, specify the multi-agent model + high reasoning effort / agent_count=16.

### Why Multi-Agent is the Core Value
The user stated: "The model should be Grok Heavy: it is multi-agent and the reason for my worthwhile effort anyway!"

Instead of one model reasoning sequentially, multiple agents can simultaneously audit:
- Filesystem truth + active sidecars
- Strict Markdown + Python (or sh) userland
- ICM / numbered stages / CONTEXT.md / output/ gates
- Low overhead + inspectability
- Etc.

The leader then produces a synthesized, high-signal review. This is why the investment makes sense.

### API Access (official, no Grok CLI involved)
- Fully compatible with OpenAI SDK (`base_url="https://api.x.ai/v1"`) or official `xai-sdk`.
- Raw curl example provided in docs.
- Auth: `Authorization: Bearer $XAI_API_KEY`
- Key management: console.x.ai → API Keys.
- Supports:
  - Multi-turn chat / responses API.
  - Structured Outputs (enforce JSON schema or specific sections for reviews).
  - Reasoning effort parameter.
  - File uploads (for PDFs, images, but text source code is fine via messages).
  - Tools (web search, code execution, X search) — optional; for pure codebase review we can keep them off.

### Other Notes from Official Docs
- Knowledge cutoff: Nov 2024 for Grok 3/4 (fine for reviewing timeless doctrines + user code).
- No realtime without explicit search tools enabled.
- Large context + good reasoning makes it suitable for "whole project" or scoped reviews without constant chunking.
- "Coding" use case explicitly points to grok-build, but general intelligence + low hallucination of grok-4.3 makes it stronger for *evaluation against principles*.

## Alignment with This Project's Doctrines

The request fits the spirit:
- External heavy model does the "smart" work.
- Local side is thin (Markdown doctrines + small Python or sh behaviour).
- Preserves "Filesystem is the single source of truth" — the review prompt is built from real .md files and source files on disk.
- Produces reviewable artifacts (markdown reports) that can live in the target's filesystem.

Tensions to manage:
- Adding any runtime dependency (SDK) slightly violates extreme minimalism (SPEC-v0.1 wants tiny POSIX sh + optional tiny Python).
- Solution options: offer a curl+jq path as the "pure" implementation; optional Python for convenience.

## Feasibility for Externally Evaluated Reviews

High feasibility.
- 1M context on grok-4.3 easily holds: full doctrines (~few k tokens) + target's .context.md + dozens of source files or a distilled view.
- Doctrines are small, stable, and explicit (perfect for "constitution" in system prompt).
- Structured outputs allow forcing output format that mirrors the principles (e.g. sections: "Filesystem Truth Violations", "Markdown/Python Purity", "Sidecar Health", "Inspectability Score", "Recommendations").
- "Externally evaluated" = the judgment happens on the cloud instance using the injected immutable rules. Local machine only orchestrates gathering + calling + storing result.

No need for any Grok CLI / TUI. This is direct API client + doctrine packager.

## Gaps / Things to Validate in Discussion
- Exact `reasoning_effort` param name and values (docs mention it; needs confirmation in full model-capabilities docs).
- Rate limits / quotas on API keys (separate from consumer Heavy subscription).
- Whether grok-build-0.1 is available to standard API keys or requires specific early access.
- Best practice for sending many source files (one big message vs multiple messages vs "files" feature if available).
- Cost for realistic review size.

Artifacts in this stage will propose concrete ways forward.
