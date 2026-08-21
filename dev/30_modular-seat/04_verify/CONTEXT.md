## Inputs
- Layer 4 (working): ../03_implement/output/
- Layer 3 (reference): ../../references/coding-style.md   # (create if missing; or link to project rules)
- Layer 3 (reference): ../../CORE_PRINCIPLES.md
- Layer 1: ../CONTEXT.md

## Process
You are the **Verify / Test** stage.

Follow the Meta-Agent skill (this workspace's .grok/skills/meta-agent/SKILL.md) and all Layer 3 references.

Run tests, lint, manual checks. Fix issues. Produce verification report.

- Load *only* the inputs listed above.
- Prefer calling Python behaviours (scripts/) for any non-intelligent work.
- Write clear, self-contained artifacts.
- Place all deliverables under this stage's `output/`.
- Stop after writing output for human review.

## Outputs
- verification.md -> output/
- summary.md -> output/
- (any other files the next stage or user will need)
