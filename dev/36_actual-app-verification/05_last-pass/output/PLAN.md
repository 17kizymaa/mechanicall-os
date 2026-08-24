# PLAN — last pass (swarm)

**Not Yes.** Three FAILs, three files.

| id | Change | Not |
|----|--------|-----|
| B3 | `PlanModule.kt` only: live CURRENT read-only; `OutlinedTextField` + `writeSchemaDraft` for DRAFT. SAVE DRAFT · not Yes | Live CURRENT edit; Yes on PLAN |
| B4 | `ChatHome.kt`: delete `LazyColumn`/thread. Six LIVE vs DRAFT rows + one last say + SEND | Chat identity; Send→GATE; `…` |
| B7 | Same file: busy label stays `SEND`. GATE strip already thinks | Typing dots |

`app_verify.py` probes are string scans. After execute, update `tests/test_app_verify.py` expects to PASS. Decide untouched. CURRENT untouched.
