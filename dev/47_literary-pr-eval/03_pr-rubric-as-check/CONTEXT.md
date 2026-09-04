## Inputs
- Layer 4: `../02_eval/output/PR-RUBRIC.md`
- Layer 4: `../02_eval/output/EVALUATION.md`
- Layer 3: `PRODUCT.md`, `docs/ALPHA-LIMITATIONS.md`
- Live git: this checkout (`feat/sit-rack-lab`), `gh pr` 7 and 8 (no open PRs)
- Layer 1: `../CONTEXT.md`

## Process
You are the **PR rubric check** stage (`pr-rubric-as-check`).

Turn the scorecard into a cat-able Python behaviour. Run it on named PRs and on the dirty tree. Write a human REVIEW.md (do not `gh pr review`; human posts). Do not apply CURRENT. Do not assemble.

Header Next is `pr-rubric-as-check`. Body of the overlay still says keep `sit-mvp-rack`. This stage does the header action only.

## Outputs
- `scripts/score_pr.py` — mechanical greps against B1–B6 / S1–S6
- `output/score-pr8.json` `output/score-pr7.json` `output/score-dirty.json`
- `output/REVIEW.md` — verdicts a stranger can post or reject
- `output/summary.md`
