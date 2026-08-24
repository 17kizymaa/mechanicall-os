# VERIFICATION

**Not Decide. Not Yes.** Mechanical score of the demo face against BEHAVIOURS.md.

Glass: storm-0 `emulator-5554` uidumps in `../output/storm-0/verify/` (home, plan, draft, decide, receipt). OEM Files dump excluded from the scorer blob. Confirm was not tapped. A33 `--serial RZCW2038KHN` exit 3.

**Score:** 10/10 (source) · 10/10 (glass)

| id | verdict | evidence |
|----|---------|----------|
| B1-bind-first | PASS | Unbound uidump is FOLDER-only (no PLAN/DRAFT/DECIDE). landingFrom → Bind; prefs pocket_one; operator copy on bind |
| B2-plan-readable | PASS | Glass PLAN shows published CURRENT with Objective/Next first; Draft chips OBJECTIVE |
| B3-plan-manual-edit | PASS | PlanModule field editor calls writeSchemaDraft. editor=True call=True bridge_has_write=True |
| B4-draft-is-workshop | PASS | Glass: LIVE vs DRAFT hunks, ACCEPT/REJECT HUNK, not a message thread. chips=False hunks=True thread=False |
| B5-propose-not-current | PASS | local stage owns PROPOSE write; test present |
| B6-decide-only-yes | PASS | two-tap + Why-required Confirm in DecideModule. Glass first screen is YES/NOT YET arm pads; Confirm dialog not opened; walker did not tap YES |
| B7-gate-instrument | PASS | Glass GATE IDLE/QUIET labels; SEND stays SEND; no `…`. Source LOAD then STREAM |
| B8-receipt-tomorrow | PASS | Glass: “No sitting yet… Opening this page is not a Yes.” Source honest empty copy |
| B9-window-honest | PASS | fillMaxSize on 1080×2340; resizeableActivity; no 360.dp letterbox |
| B10-bind-not-repo | PASS | Bound `/sdcard/mechanicall-pocket` (demo client). Operator-tree refuse in engine + tests |

**Failed:** none

Walkers did not tap Confirm. Models did not approve.

```
python3 python/app_verify.py
python3 python/app_verify.py --uidump-dir dev/39_sit-storm-factory/output/storm-0/verify
python3 python/app_verify.py --serial RZCW2038KHN   # exit 3
```
