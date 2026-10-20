# Facts — CURRENT draft complete (looked up, not asked)

**Sitting:** 2026-09-09  
**Stage:** `dev/61_current-service-entry/01_analyze/`  
**Not law.**

## Live parse (`aether current .`)

| Field | Disk now |
|-------|----------|
| Objective | Negotiate **Mechanicall: You Decide** concierge web-app — validate as human-operated project recovery service before expanding the APK or building generalized infrastructure |
| Phase | `SELECT` (SPEC-valid; was `SERVICE ENTRY` before human edit) |
| Status | `REJECTED` |
| Baseline | `needs /grill` |
| Next (header) | `publish-pilot-page` |
| Approval | `REJECTED` (human `aether reject` 2026-09-09: “REJECTED”; then “Just don't feel like it.”) |
| Host | myarch · A33 lab USB via mbp-edge (USB ≠ LTE) · chromium |
| Body Action id | `you-decide-ritual` |
| Next allowed action body | `...` |
| Validate | `OK` (parser is lenient) |
| probe(`publish-pilot-page`) | **ALLOW** (matches Next even when Approval=REJECTED) |

Cold start: if header Next and body Action id differ, **stop and ask**. They differ.

## Git

- `CURRENT.md` is **modified, uncommitted**.
- HEAD CURRENT is dest millwork / `first-sit-look` (look-closed), not this concierge file.
- This rewrite is already sitting in the live CURRENT slot.

## Internal contradictions on disk

1. Offer: “Go to anphuni.com.” Limits: “anphuni.com later; never stamps.”
2. Header Next `publish-pilot-page` vs body `you-decide-ritual`.
3. Two `## Limits` blocks (service limits, then leftover APK millwork limits).
4. Two `## Prohibited` blocks (service + protocol).
5. Keep ends `( ... incomplete; /grill-me)`.
6. Approval `REJECTED` after human reject; Approval condition still says copy onto live Domain then `aether next` / `approve`. Baseline still `needs /grill`. Probe still ALLOW on Next match.
7. Offer “per-user (500MB total limit)” vs Prohibited “accounts and multi-client infrastructure”.
8. Keep still names APK ritual: Send folder, she stamps / he runs.
9. Success evidence “a dozen to one hundred requests” vs Prohibited accounts + “adding features before completing a real session”.

## SPEC-v0.2 header enums

- **Phase:** `CAPTURE | SELECT | COMMIT | EXECUTE | REVIEW | APPROVE`
- **Status:** `DRAFT | READY-FOR-REVIEW | APPROVED | REJECTED | BLOCKED | BLOCKED-PENDING-HUMAN`
- **Approval:** `PENDING | APPROVED | REJECTED`

`SERVICE ENTRY` and `ACTIVE ― NOT YET VALIDATED` are human labels, not schema.

## PRODUCT.md (normative, yields to live CURRENT)

- Mechanicall **core** = local filesystem authority protocol (`aether`, CURRENT, preflight, events).
- **anphuni.com Session** = separate capped hosted alpha lab. **Not** core.
- A Domain CURRENT may still authorize a service instance; that recants “website later” *for this folder*, not the protocol definition.

## Prior law (not this sitting’s face)

- 2026-09-08 proposal: `.aether/proposals/CURRENT-proposal-20260908-0830.md` — Next `you-decide-ritual`, APK sprint, website later, F1=2 SitRackView, F5=APK, F4 later.
- Toy: `examples/propose-current/CURRENT-you-decide-ritual.md`.
- `decision-tree.md` C/G/M/W/R series is APK millwork. Header of that file is stale (still claims Next `you-decide-ritual`).

## Offer loop as written (keep as the draft’s intent)

Bring a messy project → (optional) LLM CURRENT.md → receive: short brief, proposed Next, decision boundary, one bounded approved work, returned files, truthful receipt, following proposal **inactive until approved**.

## Done (keep) as written

- Agents made for UI-shiz
- git and directory for anphuni, locally

No anphuni.com tree on this Kingston `opt/` mount (only `mechanicall-os`). Site code is not in this workspace.

## This factory will not

- Overwrite `CURRENT.md`
- Run `aether approve` / `aether next` / `aether reject`
- Execute `publish-pilot-page`
- Invent a second Next
