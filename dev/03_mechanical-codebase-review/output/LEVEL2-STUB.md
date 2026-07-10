# Level 2 — Tool-calling codebase review (stub)

**Approved**: 2026-07-10 (gate G2). **Status**: stub only — no implementation yet.

## Scope (from mechanical-design.md §Progressive Autonomy / Level 2)

Extend `scripts/codebase_review.py` so Grok Heavy can explore the target at runtime
instead of receiving one upfront snapshot:

- Define tools in the API request: `read_file(path)`, `grep_codebase(pattern)`,
  `list_dir(path)`.
- Implement the local tool loop in Python (stdlib only): execute each tool call against
  the filesystem/sidecars, feed results back, repeat until the model returns the final
  review.
- Log every tool invocation to a sidecar (`.memory/` or review artifact appendix) so the
  exploration stays observable — no hidden state.
- Keep Level 0 (prompt paste) and Level 1 (snapshot) modes working; Level 2 is a flag,
  not a replacement.

## Explicitly out of scope

- Full MCP server (G2: minimal-only, and only if ever needed).
- Any non-stdlib dependency.
- Write-capable tools — review remains read-only against the target.

## Acceptance sketch

- One command runs a Level 2 review end-to-end on this repo.
- Tool-call transcript is inspectable next to the review output.
- Doctrine check: pure MD+Python, cat-able, sidecar-based. 
