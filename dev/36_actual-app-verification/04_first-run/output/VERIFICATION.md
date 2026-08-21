# VERIFICATION — first run + swarm

**Not Decide. Not Yes.**

1. Mechanical: `python3 python/app_verify.py` → first **8/10** (B3, B4 FAIL).
2. Workflow `/actual-app-verification` (complete, ~7m): fail-closed. Did **not** upgrade B3/B4. **Added B7:** Send busy label is `"…"` (typing dots). CURRENT/FACE-SPEC: GATE is thinking, not dots.
3. Scorer tightened: `"…"` on Send now fails B7. Re-score **7/10**.

| id | mechanical | swarm | now |
|----|------------|-------|-----|
| B1-bind-first | PASS | PASS | PASS |
| B2-plan-readable | PASS | PASS | PASS |
| B3-plan-manual-edit | FAIL | FAIL | **FAIL** |
| B4-draft-is-workshop | FAIL | FAIL | **FAIL** |
| B5-propose-not-current | PASS | PASS | PASS |
| B6-decide-only-yes | PASS | PASS | PASS |
| B7-gate-instrument | PASS (weak) | FAIL (`…`) | **FAIL** |
| B8-receipt-tomorrow | PASS | PASS | PASS |
| B9-window-honest | PASS | PASS | PASS |
| B10-bind-not-repo | PASS | PASS | PASS |

**Failed:** B3-plan-manual-edit, B4-draft-is-workshop, B7-gate-instrument  
**Biggest gap:** manual plan edit (B3), then Draft-as-thread (B4).

Swarm one-sentence: PLAN is readable and not writable. Draft is ChatHome (composer+bubbles). Not Yes.

**CURRENT mismatch (do not rewrite here):** header Next `ACTUAL-APP-VERIFICATION` vs body Action id `mechanicall-debug-window`.

Walkers did not tap Confirm. Models did not approve.
