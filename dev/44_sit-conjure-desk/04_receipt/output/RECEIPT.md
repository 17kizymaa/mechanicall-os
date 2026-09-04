# RECEIPT — sit-conjure-desk (this sitting)

**Not Yes. Not Confirm. Not Funnel. Not Play Console.**  
Header **Next:** `sit-conjure-desk` APPROVED. Preflight allowed.  
Approve reasons: `sit-conjure-desk: S3 / wol-pi doorbell / sitter WAKE` · bind-page dialogue / concurrent errors.

## Done

| Piece | Result |
|-------|--------|
| Doorbell code | `scripts/wol-wake-listen.py` already refused `0.0.0.0`. Tests: `tests/test_wol_wake.py` green. |
| wol-pi deploy | **Not this sitting.** `ssh wol-pi` host-key fail; `anphuni@100.91.173.127` publickey denied. `curl wol-pi:7077/wake` connection refused. Human: copy script to wol-pi, `WOL_MAC` / `WOL_BIND=<tailnet IP>` off git, not `0.0.0.0`. |
| Bind overlay | CLOSE/scrim always dismiss (was stuck unless already bound). Picker no longer double-calls bind. |
| WAKE strip | Enabled when bound (`projectOn`). JOIN still not Yes. POST still needs tailnet to reach wol-pi. |
| HOLD → S3 | `scripts/desk-hold-sleep.sh` — 15 min stamp, skip if loginctl session, **no suspend unless `MECHANICALL_ALLOW_SUSPEND=1`**. This sitting: local session → skip. Did **not** suspend myarch. |
| E3b / k3s | `k3s` **inactive** on myarch. Left off. |
| Sit on A33 | Rebuilt + `adb install -r` `0.17.1-api36` vc 22. `MANAGE_EXTERNAL_STORAGE` appops allow (lab). Opening is not Yes. Wi-Fi still disabled. |

## Not done

- wol-pi process actually listening on 7077  
- Magic packet tested against myarch S3 (would drop this session)  
- Play internal / Go-git (parked under previous Next; not this pin)  
- CURRENT **body** Action id still says `sit-distro-gate` while **header** Next is `sit-conjure-desk` — human should align the body; model did not rewrite CURRENT  

WAKE on the phone will stay sleeping until wol-pi serves `/wake` on the tailnet.
