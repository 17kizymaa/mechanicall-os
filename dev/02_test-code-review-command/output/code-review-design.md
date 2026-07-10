# /code-review Command Design (Test Stage)

**Command name**: `code-review` (executable) or invocable as `/code-review` in compatible interfaces.

**Primary Goal Alignment** (per user):
- Enable Grok Heavy (grok-4.20-multi-agent, 16-agent) for externally evaluated codebase reviews.
- Use codebase doctrines (CORE_PRINCIPLES, AGENTS.md, etc.) as the evaluation constitution.
- Allow the user to leverage their SuperGrok account's usage rates (consumer interface path).
- No dependency on the Grok Build TUI/CLI.
- Thin, inspectable, follows doctrines (Markdown + minimal Python/sh, FS outputs).

## Two Modes (to support rates + flexibility)
1. **Consumer Subscription Mode (default, recommended for free/included rates)**:
   - Assembles a complete prompt.
   - Outputs it to stdout or a file (e.g. `review-prompt.md`).
   - User copies/pastes into grok.com (logged in with SuperGrok account) and runs with Grok Heavy.
   - This uses the SuperGrok account's message allowances and Heavy multi-agent access.

2. **Direct API Mode (advanced)**:
   - Calls the API directly (requires XAI_API_KEY).
   - Uses separate API billing/quotas.
   - Warning printed: "This uses xAI API credits, not your SuperGrok consumer rates."

## Invocation Examples
```bash
# Basic - prepare prompt for consumer Grok Heavy (uses your SuperGrok rates)
code-review .

# Target a different project, output the prompt file
code-review /path/to/target --output review-for-grok.md

# Direct API mode (separate billing)
code-review --api --model grok-4.20-multi-agent .

# Limit files or use scope
code-review --files "src/**/*.py" --agents 16 .
```

## How Multi-Agent Grok Heavy is Leveraged
The generated prompt includes explicit instructions for 16-agent collaboration:
- Specialized sub-agents for different doctrines.
- Leader synthesizes the final review report.

See `multi-agent-doctrine-review-strategy.md` (carried from prior stage) and the prototype template.

## Inputs Gathered by the Command (FS only)
- Doctrines from known location (configurable, default relative to script or env).
- Target's `.context.md` (recommend running aether distill first on target).
- Selected source files (git ls-files aware, .gitignore respected, size limits or globs).
- Optional local AGENTS.md or other rules.

## Outputs
- In consumer mode: Clean Markdown prompt file ready for grok.com.
- The final review (after user runs in chat or API) should be saved by user as e.g. `reviews/code-review-$(date).md` (doctrine-compliant artifact).
- Command itself produces minimal side effects.

## Prototype Scope for This Test Stage
- Minimal shell/Python script that builds the prompt.
- Hardcode or simple config for doctrines location.
- Focus on consumer mode first.
- Include the multi-agent specialization instructions.
- Test by running against a small target (e.g. this repo or examples/) and inspecting the output prompt.

This design enables the SuperGrok rates while keeping everything minimal and doctrine-aligned.
