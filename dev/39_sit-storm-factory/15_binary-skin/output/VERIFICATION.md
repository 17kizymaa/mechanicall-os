# VERIFICATION

**Not Decide. Not Yes.** Mechanical score of the demo face against BEHAVIOURS.md.

**Score:** 10/10

| id | verdict | evidence |
|----|---------|----------|
| B1-bind-first | PASS | landingFrom → Bind when unbound; prefs pocket_one; operator copy on bind |
| B2-plan-readable | PASS | PLAN shows CURRENT.md plus Changes plus a Proposal segment |
| B3-plan-manual-edit | PASS | Proposal edits write PROPOSE (Plan and/or Draft). draft_editor=True draft_writes=True plan_editor=True |
| B4-draft-is-workshop | PASS | PASS only if field chips exist and the page is not a message thread. chips=False hunks=True thread=False |
| B5-propose-not-current | PASS | local stage owns PROPOSE write; test present |
| B6-decide-only-yes | PASS | two-tap + Why-required Confirm in DecideModule |
| B7-gate-instrument | PASS | GateStrip LOAD then STREAM; Send not labelled GATE; busy must not be typing dots. typing_dots=False |
| B8-receipt-tomorrow | PASS | honest empty copy on ReceiptModule |
| B9-window-honest | PASS | resizeableActivity; painted 360×560 letterbox gone |
| B10-bind-not-repo | PASS | operator-tree refuse in engine + tests |

**Failed:** none

Walkers did not tap Confirm. Models did not approve.
