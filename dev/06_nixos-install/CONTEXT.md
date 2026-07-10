# ICM Task Context (Layer 1 Routing)

This folder follows the Interpretable Context Methodology (arXiv:2603.16021).

Folder structure = the agent architecture.
Markdown files = skills, contracts, context.
Python = behaviours.
Single agent (Grok) orchestrates by reading the structure.

## Pipeline
- 01_analyze: Analyze / Research
- 02_plan: Plan / Design
- 03_implement: Implement
- 04_verify: Verify / Test
- 05_review: Review & Polish

## How to run
1. Review / edit anything in 01_analyze/output/ after it completes.
2. Tell the agent "proceed to 02" (or the next stage) after review.
3. Human edits at output/ gates are the primary way to steer.

References (Layer 3) live in `references/` (create shared ones at top level or in project root).
Working outputs live in each stage's `output/`.

See .grok/skills/meta-agent/SKILL.md for the full protocol.
