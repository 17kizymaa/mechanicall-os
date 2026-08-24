# Proposed CURRENT update (draft — not authority)

**Project:** mechanicall-os  
**Date:** 2026-08-19  
**Author:** agent propose only (human applies)

## Observations

- Live Next is `people-app-phone-seat`, SELECT / REJECTED.
- Sequential A33 walk (`dev/31_sequential-walk/`) scored the APK **5/20** against: local AI structured support; selected directory; chat-app; workspace bridge (`dev/31_sequential-walk/04_gate-client/output/STORM.md`).
- Operator: redesign is **one phase**, not multiple Nexts. Conclude with a review. Research CI with agents (multiple SDKs) so Grok can spawn simultaneous reviews to redefine the product.
- Deterministic CI already exists: `sh tests/run.sh`, `sh scripts/ci-control-layer-gates.sh`, `.github/workflows/test.yml`.
- Grok workflows support `parallel()` with `agent_budget` 128–1024; reviewers can be read-only.

## Inferences

- Phone-seat as a product Next is concluded as **lab**. Keeping it as live Next repeats Rooms.
- Product redefinition should be one Next: a review-swarm factory whose only write to law is a propose file, then human Yes.
- Optional Codex/Claude panels are extra files, not extra Nexts.

## Unknowns

- Whether the first swarm should include non-Grok SDKs or Grok-only.
- Whether GitHub should run `grok -p` (needs secrets not in git).

## Proposed CURRENT change

```markdown
**Objective:** Close people-app-phone-seat as lab. One phase: a Grok review-swarm factory (optional extra SDKs) that writes REVIEW.md so the product can be redefined. Models never approve. Not Play Store. Not four Nexts.
**Phase:** SELECT
**Status:** DRAFT
**Baseline:** 2026-08-19 · STORM 5/20 on A33 · operator: one phase + agent CI
**Next:** agent-review-ci
**Approval:** PENDING

## Product (non-negotiable identity)
- **Is:** local-first authority protocol.
- **This Next:** factory for simultaneous read-only reviews → one REVIEW.md → propose-current. Phone APK stays lab.
- **Not core:** Play Store, Funnel, model-auto-approve, dual-concurrent-next.

## Keep
- One Next; models never approve; silence ≠ Yes
- GET / open app is not Yes
- `tests/run.sh` / control-layer gates as deterministic CI
- Phone bind ≠ this repo

## Reject
- dual-concurrent-next
- model-auto-approve / model-auto-write-current
- --yolo / full-auto against CURRENT
- splitting redesign into logo / picker / chat / decide Nexts
- Play Store this Next
- Funnel / public Ollama

## Limits
- Reviewers read-only; swarm does not write CURRENT
- No secrets in git
- First swarm cap: 8 parallel + 1 synthesizer unless a human raises budget

## Next allowed action
**Action id:** `agent-review-ci`

1. Run `.grok/workflows/product-review.rhai` (Grok `/product-review` or workflow tool).
2. Land `REVIEW.md` under `dev/32_phase-close-agent-ci/03_setup/output/` (or the run’s output/).
3. Human reads REVIEW, edits propose if needed, `aether approve` with a real reason only if this factory is the Next they want.

## Approval condition
Human `aether approve` with a real reason when the review-swarm factory is the Next they want.
```

## Conflicts with existing authority

- Header **Next:** `people-app-phone-seat` would become `agent-review-ci`.
- Objective (phone seat) would be closed as lab, not continued as live Next.
- Approval stays human-only; this file is not Yes.

## Human decision required

- [ ] Apply proposed fields to CURRENT.md  
- [ ] Reject and leave CURRENT unchanged  
- [ ] Revise and re-propose  

**Do not** run `aether approve` from a model or agent.
