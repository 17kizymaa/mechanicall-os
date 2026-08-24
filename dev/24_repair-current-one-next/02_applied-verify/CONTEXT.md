## Inputs
- Layer 1: `../CONTEXT.md`
- Layer 1: `../../../CURRENT.md`
- Layer 3: `../01_propose/output/CURRENT-A-mobile-planning-demo.md`
- Layer 3: `../01_propose/output/APPLY.md`
- Layer 3: `../01_propose/output/check_current_pin.py`
- Layer 4: human message “applied A”

## Process
You are the **verifier**. Confirm the human applied A. Do not write CURRENT. Do not approve/next/reject. Do not implement the demo.

Run pin checker, `aether current validate`, `aether probe mobile-planning-demo`, `aether probe casual-core-interface` (expect refuse). Diff against A. Record residuals (missing `next_selected`).

## Outputs
- RECEIPT.md -> output/
- summary.md -> output/
