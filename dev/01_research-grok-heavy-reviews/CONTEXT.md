## Inputs
- Layer 0 / Project Doctrines (L3 references):
  - /home/awareness-agent/CORE_PRINCIPLES.md
  - /home/awareness-agent/AGENTS.md
  - /home/awareness-agent/ARCHITECTURE.md
  - /home/awareness-agent/SPEC-v0.1.md
  - /home/awareness-agent/.context.md
  - /home/awareness-agent/README.md
- Layer 4 (user request): The query "I wanted Grok Heavy to do externally evaluated codebase reviews: I do not require the Grok CLI for this, just maybe let us use the codebase doctrines to create a /review-codebase command that lets Grok Heavy be queried through some sort of API, using official capability documents to gauge the right approach on this. Let us discuss this"
- Official capability documents (fetched Layer 3/4):
  - xAI API docs: https://docs.x.ai/developers/models , https://x.ai/api , https://docs.x.ai/developers/quickstart
  - Key models: grok-4.3 (1M context, flagship reasoning + agentic, low hallucination, configurable reasoning_effort), grok-build-0.1 (256k, "fast coding model trained specifically for agentic coding workflows", early access)
  - API: OpenAI-compatible (or official xai-sdk), base https://api.x.ai/v1 , XAI_API_KEY from console.x.ai
  - Capabilities relevant: tool calling, structured outputs, large context for file/code ingestion, reasoning modes, file uploads (PDFs etc but for source: text primarily)

## Process
You are the single meta-agent / researcher following Interpretable Context Methodology and this project's locked doctrines exactly.

**Scope strictly to the request**:
- Focus on **externally evaluated** reviews using Grok Heavy (i.e. top-tier xAI models via official API, not the local Grok Build TUI/CLI).
- Do **not** propose using or extending the Grok CLI TUI.
- Use the **codebase doctrines** (the md files above) as the core "personality" / evaluation criteria injected into prompts.
- Gauge approach using the **official documents** fetched (model choice, context limits, auth, SDK vs minimal, structured output suitability for reviews, file handling).
- Produce discussion-friendly, reviewable artifacts. No code that violates Core Principles (no heavy frameworks in core path; keep any Python tiny and optional; prefer plain files + curl/sh where possible).
- Consider how a lightweight `/review-codebase` (or `aether review-codebase`, or standalone script) could work:
  - Invocation (CLI command, script in PATH, integrated with aether sidecars).
  - How to feed doctrines + target project's .context.md + selected source (respect .scope, use ripgrep or simple find).
  - Context management for large codebases (1M context on grok-4.3 is strong advantage; summarize via aether first? chunk? attach key files?).
  - Output: clean markdown report, perhaps written as sidecar or to output/ dir.
  - "Externally evaluated": the heavy lifting (deep critique against principles) happens on the cloud model; this local thing only prepares context + calls API + formats.
- Identify tensions with this project's minimalism (e.g. adding SDK dep vs pure stdlib + requests or curl).
- Surface options, tradeoffs, concrete next artifacts (e.g. prompt template in md, tiny behaviour script sketch).
- Keep everything `cat`/`grep` friendly. Emit self-contained md.

Use only the listed inputs. Do not wander into unrelated repo files.

For mechanical work (scaffolding files, etc.): already done; if more needed later call Python behaviours.

End by writing clear artifacts to output/. Explicitly list them.

## Outputs (to output/)
- research-summary.md : Synthesis of official capabilities + relevance to codebase reviews.
- doctrine-injection.md : How to package and inject CORE_PRINCIPLES etc. as prompt context.
- options.md : 2-4 concrete architectural options for the /review-codebase command, with pros/cons vs principles.
- proposed-interface.md : Suggested command signature, inputs, outputs, example usage.
- discussion-points.md : Open questions and recommendations for next steps / human decisions.
- (optional small) draft-review-prompt.md : A starter system + user prompt template that bakes in the doctrines.
- summary.md : One-page overview + paths to all artifacts for quick review.

Halt after writing outputs. Present for human review and discussion. Do not create further stages.
