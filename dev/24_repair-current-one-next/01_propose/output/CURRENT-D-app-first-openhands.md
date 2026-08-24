# CURRENT

**Objective:** Ship the smallest **people-facing app**: `docker compose up` starts OpenHands (does the work) plus Mechanicall law (one readable plan, human Yes/Not yet, receipts). One project folder. Not a protocol demo. Not a swarm console. Not a Play Store listing this Next.
**Phase:** SELECT
**Status:** ACTIVE
**Baseline:** 2026-08-18 · repair A parked as lab · human asked for usefulness from the actual app
**Next:** app-first-openhands-compose
**Approval:** PENDING
**Host:** myarch

## Product (non-negotiable identity)
- **Is:** local-first **authority protocol** inside **one app** people can run.
- **This Next:** Compose file + OpenHands agent host + Yes/Not yet on a bound project folder. Docker is packaging. OpenHands is not law.
- **Not core:** Hyprland rice; H3 dashboard; phone sitting as the product; Play Store listing; multi-agent swarm UI.

## Done (keep)
- **Claim-1 CERTIFIED** — protocol, plugin, B1, G1
- **mobile-planning-demo** — lab. Face/spike exist. Sitting cancelled. **Not this Next**
- **Casual-core** — still missing `docs/CASUAL-CORE-INTERFACE.md`; not this Next

## Keep
- Law not stack; one Next; silence ≠ permission; models never approve
- OpenHands may edit the project and may write PROPOSE; it must not write CURRENT or self-approve
- One bound folder per run (not this repo’s CURRENT unless you deliberately open it)
- Filesystem remains truth: CURRENT, events, artifacts

## Reject
- dual-concurrent-next
- model-auto-approve / model-as-authority / model-auto-write-current
- claim-session-is-core-product
- Swarm-first / multi-OpenHands as this Next
- Play Store listing as this Next (sideload or compose first)
- Pretending the LAN pocket face is already the people app
- Second protocol clone inside OpenHands

## Limits
- One Compose stack on this host first. No public bind of Ollama or the agent API.
- No secrets in git.
- Phone / store / swarm only after a stranger (or you pretending to be one) can: clone or pull → compose up → see a plan → get work → tap Yes.
- Do not fold `~/mechanicall-pocket` into this repo.

## Next allowed action
**Action id:** `app-first-openhands-compose`

Brief: one Compose app people can run

1. Write `compose.yml` (name TBD in-tree lab path) that starts OpenHands + a thin Mechanicall Yes/plan face + bind-mount for **one** project dir.
2. OpenHands talks to that dir. Mechanicall shows CURRENT + receipts. Yes = apply PROPOSE + `aether approve` in that dir.
3. README: ten-line “how a person uses this.” No CLI required for the happy path after `compose up`.
4. Prove: operator-tree refuse if they bind this repo by mistake; GET is not Yes; OpenHands cannot approve.

## Approval condition
Human: `aether approve "…"` when the Compose happy path is written enough to implement. Then preflight `app-first-openhands-compose` only.

Silence is never permission.

## Prohibited
- automatic-approve
- commit-secrets
- dual-concurrent-next
- model-auto-approve-session
- model-auto-write-current
- uncapped-registration
- send-email-for-real
- host-smtp
- live-graph-oauth
- reopen-public-pipeline-register
- claim-session-is-core-product
- claim-conversation-auto-sync
- claim-personal-model-is-security-jail
