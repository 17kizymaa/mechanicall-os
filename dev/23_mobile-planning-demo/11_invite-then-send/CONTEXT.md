## Inputs
- Layer 1: `../CONTEXT.md`, `../../../CURRENT.md` (Next = `mobile-planning-demo`)
- Layer 1: `../../../.continue-here.md` (human picked option 1)
- Layer 4: `../10_handoff/output/HANDOFF.md`, `../output/BRAKE.md`
- Layer 3: `../../../scripts/send-brake.sh`, `../../../python/aether_pocket_serve.py`

## Process
You are **starting the tailnet face after the human chose invite-then-send**.

The operator must invite the friend’s **own** email at https://login.tailscale.com/admin/users. This CLI cannot invite. Do not suggest `17kizymaa@gmail.com`. Do not Funnel. Do not public-bind Ollama. Do not POST Yes. Do not rewrite operator CURRENT.

Bind `~/brake-friend-sit` (not the operator tree). Host `100.90.85.68:8765`. `POCKET_SYNC=0`.

## Outputs
- RECEIPT.md -> output/
- summary.md -> output/
