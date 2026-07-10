# Doctrine Injection for Grok Heavy Codebase Reviews

## Core Idea
The locked doctrines in this repo become the **immutable constitution** that the external Grok Heavy instance must use to evaluate any target codebase.

Primary doctrine files (small, stable, human+machine readable):
- CORE_PRINCIPLES.md (non-negotiable: FS truth, Markdown+Python only, sidecars, low overhead)
- AGENTS.md (meta-agent / ICM protocol, numbered stages, CONTEXT.md, output/ gates, single orchestrating agent)
- ARCHITECTURE.md (three layers)
- SPEC-v0.1.md (brutalist minimal, sidecar layout, aether command contract)
- .context.md of the *target* project (its living self-awareness)

## Recommended Injection Strategy

### System Prompt Skeleton (put this in the review command behaviour)
```markdown
You are an extremely strict, high-signal codebase reviewer.

You evaluate ONLY against the following immutable doctrines. Quote them when you cite violations or strengths. Never invent new rules.

=== DOCTRINE: CORE PRINCIPLES (LOCKED) ===
[insert full or key excerpts of CORE_PRINCIPLES.md here]

=== DOCTRINE: INTERPRETABLE CONTEXT METHODOLOGY + AGENTS.md ===
[insert relevant sections or full AGENTS.md]

=== DOCTRINE: ARCHITECTURE (three layers) ===
[...]

=== DOCTRINE: BRUTALIST MINIMAL SPEC (SPEC-v0.1.md) ===
[...]

You must produce reviews that are:
- Principle-first (start from the locked rules)
- Evidence-based (point to specific files, lines, or sidecar content)
- Actionable but non-prescriptive beyond the doctrines
- Written in clear Markdown with sections that map to the principles

Target project's self-awareness context follows.
```

### How to Supply Target Context
1. Always include the target's `.context.md` (it is the distilled truth).
2. Optionally include `.aether/state.json` or `.aether/.scope`.
3. For source: 
   - Prefer pre-distilled view when possible (run `aether distill` on target first).
   - Or use lightweight selection: git-tracked files under a size limit, or files matching certain patterns.
   - Or let user specify `--files` or rely on the model having tool use (but keep review pure unless needed).

Because grok-4.3 has 1M tokens, we can afford to send:
- Full doctrines ( ~5-10k tokens combined)
- Full target .context.md
- 50-200k tokens of actual source + docs
This is realistic for meaningful scoped reviews.

### Structured Output Recommendation
Use the API's structured outputs (or strong instruction + schema in prompt) to force:

```json
{
  "overall_alignment_score": 0-100,
  "principle_violations": [{"principle": "...", "evidence": "...", "severity": "high|med|low"}],
  "strengths": [...],
  "recommendations": [{"title": "...", "rationale": "tied directly to doctrine X", "example": "..."}],
  "sidecar_health": "...",
  "inspectability_assessment": "..."
}
```

Then also emit a human-friendly Markdown rendering of the same.

This keeps the review "externally evaluated" yet reproducible and machine-consumable.

## Practical Packing in a Thin Client
- The review command (Python or sh) reads the doctrine files from a known location (this repo, or vendored copy, or `--doctrines-dir`).
- It can embed them verbatim into the prompt.
- For repeated use, doctrines can be cached locally in the behaviour or referenced by hash.

Because doctrines are the product, they should be versioned and committed alongside the review tool.

## Why This Is Powerful
Injecting the *exact* text of CORE_PRINCIPLES etc. removes ambiguity. The external heavy model is forced to reason inside the same frame the project itself uses.

This is "using the codebase doctrines" exactly as requested.
