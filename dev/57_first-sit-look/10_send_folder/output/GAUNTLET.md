# GAUNTLET

**Not Decide. Not Yes.** Stateful play on storm-0. Never Confirm.

**Score:** 12/12 ran=12

| id | verdict | evidence |
|----|---------|----------|
| G0-launch | PASS | sit=True launcher=False |
| G1-bound | PASS | desc='   PLAN published CURRENT.md in LCD        ' next_on_disk=True |
| G2-plan-disk | PASS | sha=407fd698de5f92b8 next=True |
| G3-crt-open | PASS | current_sha 407fd698de5f92b8 -> 407fd698de5f92b8 |
| G4-crt-dismiss | PASS | current_sha 407fd698de5f92b8 |
| G5-send-open | PASS | current_sha 407fd698de5f92b8 |
| G11-send-stage | PASS | current_stable=True notice_len=217 not_yes=True |
| G6-send-dismiss | PASS | current_sha 407fd698de5f92b8 |
| G7-draft-propose | PASS | current_stable=True propose_len=121 has_type=True |
| G8-decide-why | PASS | desc='   DECIDE why       why  ' |
| G9-not-yet | PASS | next_kept=True propose_not_applied=True receipt_not_yet=True |
| G10-relaunch | PASS | next_kept=True propose_kept=True receipt_not_yet=True desc='   PLAN published CURRENT.md in LCD        ' |

**Failed:** none

PASS is not human Yes. Confirm was not tapped.
