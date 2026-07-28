# CURRENT

**Objective:** Client-one usable path on operator host first: tether SSH runbook, plain-language panel, simple Grok install; two tools on one TTY without claiming a fused product.
**Phase:** EXECUTE
**Status:** READY-FOR-REVIEW
**Baseline:** session/client-one-delroy-reconfigure
**Next:** plain-panel-labels
**Approval:** PENDING

## Keep
- Artifacts and code on this operator machine (no transfer P0)
- Plain language for panel and client-facing install sheets
- Grok Build = AI chat/work; aether panel = plan + human yes/no
- Same physical TTY for both (tmux or open-from-panel) as **ops convenience only**
- Delroy / project INIT deferred until later Next
- SSH over USB tether before another wlan0 attempt

## Reject
- Realtime chat facade inside panel
- Dual-agent / pending-until-STOP session mode
- Marketing “one product UI” for Grok+panel
- Package transfer as P0
- WLAN-first networking
- Wipe disks / GUI as install prerequisite

## Limits
- Panel does not sandbox Grok
- Models never approve; human only for approve/reject
- Do not commit auth.json or secrets

## Next allowed action
Ship plain-language panel labels (and short help) in `python/aether_panel.py`; keep internal action keys stable. Action id: `plain-panel-labels`.

## Approval condition
Human reviews dump/TUI labels, then `aether approve "labels stick"` from this stage dir (or chat proceed).

## Prohibited
- chat-facade-in-panel
- dual-agent-mirror
- transfer-package-p0
- wlan-first
- wipe-disk
