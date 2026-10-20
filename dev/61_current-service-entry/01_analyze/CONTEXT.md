## Inputs
- Layer 4 (working): ../../CURRENT.md (live, uncommitted concierge rewrite)
- Layer 4 (working): ../../decision-tree.md (Y-series prepend; do not wipe C/G/M/W/R)
- Layer 4 (working): ../../.aether/proposals/CURRENT-proposal-20260908-0830.md (APK ritual, superseded as *this* sitting's face)
- Layer 3 (reference): ../../SPEC-v0.2.md (CURRENT schema + Phase/Status/Approval enums)
- Layer 3 (reference): ../../PRODUCT.md (core vs anphuni.com Session)
- Layer 3 (reference): ../../examples/propose-current/CURRENT-you-decide-ritual.md
- Layer 3 (reference): ../../docs/AGENT-AGNOSTIC-COLD-START.md (header Next vs body Action id)
- Layer 1: ../CONTEXT.md
- Layer 0: ../../AGENTS.md · grilling skill · propose-current command

## Process
You are the **Grill / Analyze** stage for completing the CURRENT.md *draft*.

- Look up facts. Do not ask the operator for disk state.
- Ask the **whole frontier** in one round (grilling skill). Persist each round to `decision-tree.md` (grill-me-store-decisions).
- Do **not** overwrite live `CURRENT.md`.
- Do **not** run `aether approve`, `aether reject`, or `aether next`.
- Stop after writing this round's `output/` for human review.

## Outputs
- FACTS.md -> output/
- ROUND-01.md -> output/
- summary.md -> output/
