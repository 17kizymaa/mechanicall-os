# VERIFICATION

**Not Decide. Not Yes.** Mechanical score of the demo face against BEHAVIOURS.md.

**Score:** 10/10

**STORM host:** no adb devices. Round 1 is **source-only**. Serial RZCW2038KHN was not used. Confirm was not tapped.

| id | verdict | evidence |
|----|---------|----------|
| B1-bind-first | PASS | landingFrom → Bind when unbound; prefs pocket_one; operator copy on bind |
| B2-plan-readable | PASS | PlanModule CAPITALISED fields; uidump if given |
| B3-plan-manual-edit | PASS | PlanModule editor + writeSchemaDraft |
| B4-draft-is-workshop | PASS | hunks LIVE/DRAFT; not a message thread |
| B5-propose-not-current | PASS | local stage owns PROPOSE write; test present |
| B6-decide-only-yes | PASS | two-tap + Why-required Confirm in DecideModule |
| B7-gate-instrument | PASS | GateStrip LOAD then STREAM; Send not labelled GATE; no typing dots |
| B8-receipt-tomorrow | PASS | honest empty copy on ReceiptModule |
| B9-window-honest | PASS | resizeableActivity; painted 360×560 letterbox gone |
| B10-bind-not-repo | PASS | operator-tree refuse in engine + tests |

**Failed:** none

Walkers did not tap Confirm. Models did not approve.

`python3 python/app_verify.py` exit 0. `--serial RZCW2038KHN` exit 3.
