## Inputs
- Layer 4 from previous stage: ../01_research-grok-heavy-reviews/output/verification-supergrok-free-rates.md (key verification)
- Layer 4 from previous: ../01_research-grok-heavy-reviews/output/changes-and-explorations-from-original-prompt.md, multi-agent-doctrine-review-strategy.md, gauged-api-approach-examples.md, research-summary.md, discussion-points.md
- Layer 3 doctrines (L0/L3): /home/awareness-agent/CORE_PRINCIPLES.md, AGENTS.md, ARCHITECTURE.md, SPEC-v0.1.md, .context.md
- User direction: "I want to use my free usage rates from my SuperGrok account." + "move to test "/code-review" command stage"
- Official model: grok-4.20-multi-agent for Grok Heavy (16-agent), separate billing from consumer SuperGrok.

## Process
You are the single meta-agent.

**Verification first (must address explicitly)**:
From the verification artifact: Consumer SuperGrok subscriptions and xAI API billing are separate. A pure direct-to-api.x.ai thin client using an API key will **not** consume the consumer SuperGrok included "free usage rates" / message allowances. It uses API metering.

To enable the user's goal:
- Prioritize a design where the `/code-review` command prepares a self-contained, doctrine-rich prompt + context that the user can feed into their logged-in grok.com chat (consumer interface). This uses their SuperGrok account's rates and full Grok Heavy multi-agent access.
- Optionally support direct API (with clear note that it uses separate credits).
- Keep the command extremely thin (sh or tiny Python), filesystem-based, Markdown templates for the prompt, outputs review artifacts to FS.
- Name: support `/code-review` (or `code-review` executable).
- Leverage multi-agent: Include instructions in the generated prompt for 16-agent collaboration on doctrines.

**Scope for this test stage**:
- Design a minimal `/code-review` command prototype.
- Focus on subscription-rate-friendly path (prompt generator for consumer Grok Heavy).
- Use doctrines for the review constitution.
- Test conceptually or with a small script that outputs a ready-to-use prompt.
- Produce runnable/testable artifacts (e.g. a scripts/code-review or bin/ prototype).
- Document how it enables (or works around) the SuperGrok free rates.
- Respect all Core Principles: no heavy frameworks, outputs as Markdown sidecar-like artifacts, inspectable.

**Do not**:
- Assume direct API calls will use consumer rates.
- Re-introduce Grok CLI TUI dependency.
- Create heavy code; keep prototype minimal.

Write clear, reviewable outputs to this stage's output/.

## Outputs (to output/)
- verification-summary.md : Explicit yes/no on enabling SuperGrok rates + any adjustments made.
- code-review-design.md : Command spec, how it supports subscription rates, multi-agent prompt strategy, invocation examples (including as /code-review).
- prototype-code-review.sh or .py : Minimal working prototype (in output/ or scripts/ under stage) that gathers doctrines + target context and outputs a pasteable prompt optimized for grok.com Grok Heavy.
- test-instructions.md : How to test the prototype (e.g. point at a small target, run, paste resulting prompt into grok.com with SuperGrok login, observe multi-agent review).
- updated-prompt-template.md : Refined draft-review-prompt.md adapted for multi-agent Heavy + subscription path.
- summary.md : Overview of the test stage, paths, next steps (e.g. 03_implement full version).

Halt after outputs for human review before further advancement. Align with ICM and doctrines.
