# Receipt — applied A

**When:** 2026-08-18T06:32:02Z  
**Claim:** human applied option A  
**Verifier:** agent (read-only)

## Checks

| Check | Result |
|-------|--------|
| `CURRENT.md` vs `CURRENT-A-mobile-planning-demo.md` | byte-identical |
| Header `**Next:**` | `mobile-planning-demo` |
| Body `**Action id:**` | `mobile-planning-demo` |
| `check_current_pin.py` | OK (exit 0) |
| `aether current validate` | OK (no lifecycle warning) |
| `aether probe mobile-planning-demo` | ALLOW · Phase=IMPLEMENT Status=APPROVED |
| `aether probe casual-core-interface` | REFUSE exit 3 (not Next) |
| `next_selected` → `mobile-planning-demo` | **still absent** (expected; `aether next` would refuse unchanged) |

## Residuals (not defects of the apply)

- Events last `next_selected` remains `casual-core-interface` (2026-08-11). Do not bounce Next to invent a row.
- Phone sitting still PARKED (`dev/23_mobile-planning-demo/PARKED.md`).
- `docs/CASUAL-CORE-INTERFACE.md` still missing (honest in A).
- Play Store / OpenHands still Reject on this Next.

## What law allows now

Preflight `mobile-planning-demo` only.

CURRENT step 1 is a **human** choice:

1. **Resume** the parked spike (`dev/23_mobile-planning-demo/output/SPIKE.md`), or
2. **Close** — human `aether reject` with a real reason, then re-SELECT.

Agent does not choose. Silence is not resume.
