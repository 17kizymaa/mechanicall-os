# Plate-cycle behaviour — you-decide-sit

**Not Yes.** Glue from A33 inbox `18_E2E-SPRINT-THREAD.md` §7. FLAG is iterate.

## Commands

```bash
# one mechanical cycle (orchestrator patches between calls)
python3 python/you_decide_plate_cycle.py --plate L2 \
  --stills-dir dev/57_first-sit-look/06_still_again/output/stills
# same:
sh scripts/you-decide-plate-cycle.sh --plate L2 \
  --stills-dir dev/57_first-sit-look/06_still_again/output/stills
```

## Exit

| code | meaning |
|------|---------|
| 0 | this plate PASS and law green — next plate |
| 1 | STOP — N exhausted or clock; human carry vs continue |
| 2 | ITERATE — this plate FLAG/FAIL; patch one gap, re-run |
| 3 | REFUSE live A33 |
| 4 | ENV — no storm, assemble miss, unknown plate |

`--score-only` skips assemble+walk. `--loop` repeats only with `--patch-cmd` (model patches; this script does not millwork). Law default is source `app_verify` (not dest uidumps). Other-row FLAG does not fail this plate. Never Confirm. USB ≠ LTE. Do not invent `dev/58`.
