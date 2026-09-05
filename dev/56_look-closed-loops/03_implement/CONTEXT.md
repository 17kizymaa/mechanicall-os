## Inputs
- Layer 4: ../02_plan/output/LOOK-VERIFY-SPEC.md
- Layer 4: ../02_plan/output/VISUAL-REVIEWER-DEST.md
- Layer 3: ../../python/app_verify.py (leave as law probes)
- Layer 3: ../../scripts/storm-walk.sh
- Layer 1: ../CONTEXT.md

## Process
You are the **behaviour writer**.

Only after the human says proceed: write `python/look_verify.py` and a dest walker that taps CRects on **storm-0** (never A33 as testers). Keep `app_verify.py` as the law scorer. Do not implement Generate. Do not rewrite CURRENT.

## Outputs
- RECEIPT.md -> output/
- (scripts land in repo `python/` and `scripts/` only if this stage is activated)
