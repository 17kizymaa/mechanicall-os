# Proposed /review-codebase Interface (Discussion Draft)

## Command Names (pick one)
- `review-codebase` (standalone, as user said "/review-codebase")
- `aether review-codebase` (integrates with existing awareness tool)
- `python -m awareness.review` or simple `bin/review-codebase`

## Core Signature (Option 2 style)
```bash
review-codebase [OPTIONS] [TARGET_DIR]

# Examples
review-codebase .
review-codebase /path/to/other-project --effort high --output review.md
review-codebase --doctrines /path/to/this-repo/doctrines --files "src/**/*.py" .
aether review-codebase --model grok-4.3
```

## Key Options (minimal surface)
- `--model grok-4.3` (default; allow override to grok-build-0.1 if desired)
- `--effort high|max` (maps to reasoning_effort)
- `--output FILE` (default: stdout; or write timestamped file under TARGET/reviews/)
- `--include-doctrines` / `--no-doctrines` (default on)
- `--files GLOB` or `--scope` (respect .aether/.scope or .gitignore)
- `--json` (emit structured + human md)
- `--dry-run` (print the prompt that would be sent, for debugging/audit)
- `--key-from-env` (XAI_API_KEY)

## Inputs the Command Gathers (all from FS)
1. Doctrine files (from a configured or sibling location, or vendored).
2. Target's `.context.md` (required for good results; suggest running aether distill first).
3. Selected source + docs from TARGET (text only).
4. Optional: target's AGENTS.md / other local rules.

## Output
- Clean, principle-quoted Markdown report.
- Optionally parallel structured JSON for tooling.
- Written to FS so it becomes part of the project's artifacts (can be committed, sidecar-ed, etc.).

## Example Flow (ideal)
```bash
cd my-project
aether distill                 # refresh .context.md using local doctrines
review-codebase . --effort max --output reviews/principles-review-$(date +%F).md
cat reviews/principles-review-....md
git add reviews/ .context.md
```

The external Grok Heavy does the actual evaluation using the injected doctrines.

## Invocation as "Slash Command"
If this is later used inside other agents (including future Grok CLI or other tools), the command can be exposed as `/review-codebase <args>` via skills or simple wrappers. The core remains a plain executable/script.

This design keeps the heavy model external and the local footprint tiny.
